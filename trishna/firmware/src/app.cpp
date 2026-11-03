#include "app.h"
#include <Arduino.h>
#include <WiFi.h>
#include <time.h>
#include <math.h>
#include "board_pins.h"
#include "settings.h"
#include "telemetry.h"
#include "trishna_filters.h"
#include "trishna_sense.h"

tr_fsm_t g_fsm;
Live g_live;
Result g_last, g_blank;

static tr_inputs_t g_in;
static bool g_tof_present = false, g_temp_present = false;
static uint8_t g_presence_hits = 0, g_leak_hits = 0;
static uint32_t g_presence_last = 0, g_t_probe = 0, g_t_vin = 0, g_t_hb = 0, g_t_live = 0, g_t_vin_err = 0;
static float g_med[5]; static uint8_t g_med_n = 0;
static tr_ema_t g_ec_ema;
static uint8_t g_fallback_evt = 0;

// ---- analysis job (runs across ticks so the leak check and the watchdog keep running) ----
enum AJ { AJ_IDLE, AJ_SETTLE };
static AJ g_aj = AJ_IDLE;
static uint32_t g_aj_t0 = 0, g_aj_last = 0;
static tr_settle_t g_settle;
static float g_aj_ec = 0, g_aj_ohm = -1;
static bool g_aj_air = false;

static float ec_from_raw(const EcRaw &r, float &ohm) {
    ohm = tr_ec_cell_ohm(r.ratio, &g_set.cal);
    return tr_ec_mscm(ohm, &g_set.cal);
}

static bool time_valid() { return time(nullptr) > 1700000000; }

uint16_t app_flags() {
    uint16_t f = 0;
    if (time_valid()) f |= TR_FLAG_TIME_VALID;
    if (g_live.presence) f |= TR_FLAG_PRESENCE;
    if (g_live.stream) f |= TR_FLAG_STREAM;
    if (g_fsm.valve) f |= TR_FLAG_VALVE_OPEN;
    if (g_fsm.pump == PUMP_FWD) f |= TR_FLAG_PUMP_FWD;
    if (g_fsm.pump == PUMP_REV) f |= TR_FLAG_PUMP_REV;
    if (g_live.leak) f |= TR_FLAG_LEAK;
    if (tlm_sd_ok()) f |= TR_FLAG_SD_OK;
    if (g_tof_present) f |= TR_FLAG_TOF_OK;
    if (g_temp_present) f |= TR_FLAG_TEMP_OK;
    if (!g_set.cal.calibrated || !g_set.cal.sg_fitted) f |= TR_FLAG_CAL_DEFAULT;
    if (g_fsm.fault != ERR_NONE) f |= TR_FLAG_FAULT_LATCH;
    if (g_fsm.fallback) f |= TR_FLAG_FALLBACK_TRG;
    return f;
}

void app_emit(uint8_t type, uint16_t error, uint8_t prev_state) {
    tr_frame_t f{};
    struct timeval tv; gettimeofday(&tv, nullptr);
    f.type = type;
    f.unix_s = time_valid() ? (uint32_t)tv.tv_sec : 0;
    f.ms = time_valid() ? (uint16_t)(tv.tv_usec / 1000) : (uint16_t)(millis() % 1000);
    f.uptime_s = millis() / 1000;
    f.state = (uint8_t)g_fsm.state; f.prev_state = prev_state;
    f.event_id = g_fsm.event_id;
    f.error_code = error;
    const Result &r = g_last;                               // latest event result rides along in every frame
    f.flags = (type == TR_FT_RESULT) ? (uint16_t)(r.flags | app_flags()) : app_flags();
    float t = isnan(g_live.temp_c) ? r.temp_c : g_live.temp_c;
    f.temp_cx100 = isnan(t) ? INT16_MIN : tr_i16_sat(t * 100.0f);
    if (type == TR_FT_LIVE) {
        f.ec25_x100 = tr_u16_sat(g_live.ec_live * 100.0f);
        float ohm; ec_from_raw(g_live.ec, ohm); f.cell_ohm = ohm > 0 ? tr_u16_sat(ohm) : 65535;
    } else {
        f.ec25_x100 = tr_u16_sat(r.ec25 * 100.0f);
        f.cell_ohm = r.cell_ohm > 0 ? tr_u16_sat(r.cell_ohm) : 65535;
        f.sg_x10000 = tr_u16_sat(r.sg * 10000.0f);
        f.a450_x1000 = tr_i16_sat(r.a450 * 1000.0f);
        f.turb_x1000 = tr_u16_sat(r.turb * 1000.0f);
        f.tx_blue_mv = tr_u16_sat(r.opt.blue_tx); f.tx_ir_mv = tr_u16_sat(r.opt.ir_tx); f.sc_ir_mv = tr_u16_sat(r.opt.ir_sc);
        f.hydration = r.hydration; f.quality = r.quality;
    }
    f.vin_mv = tr_u16_sat(g_live.vin_mv);
    if (!tlm_send(f)) { /* queue full: counted in tlm_dropped(); reported in the next heartbeat via the console */ }
}

void app_apply_settings() {
    tr_fsm_cfg_t c; settings_to_fsm(g_set, c);
    if (!g_tof_present) c.presence_required = 0;      // no ToF fitted/working: the sump probe alone triggers
    g_fsm.cfg = c;
}

void app_init() {
    hal_init();
    hal_all_off();
    g_tof_present = hal_tof_init();
    g_temp_present = hal_temp_present();
    tr_fsm_cfg_t c; settings_to_fsm(g_set, c);
    tr_fsm_init(&g_fsm, &c, g_set.event_id);
    app_apply_settings();
    tr_ema_init(&g_ec_ema, tr_ema_alpha(0.25f, 0.75f));
    if (g_set.wifi_ssid[0]) { WiFi.mode(WIFI_STA); WiFi.begin(g_set.wifi_ssid, g_set.wifi_pass); configTime(0, 0, "pool.ntp.org", "time.google.com"); }
    g_live.vin_mv = hal_vin_mv();
    app_emit(TR_FT_HEARTBEAT, ERR_NONE, (uint8_t)g_fsm.state);
    if (!g_tof_present) app_emit(TR_FT_ERROR, ERR_TOF, (uint8_t)g_fsm.state);
    if (!g_temp_present) app_emit(TR_FT_ERROR, ERR_TEMP_SENSOR, (uint8_t)g_fsm.state);
    if (!tlm_sd_ok()) app_emit(TR_FT_ERROR, ERR_SD, (uint8_t)g_fsm.state);
}

// ---------------------------------------------------------------- measurements requested by the FSM
static void do_blank() {
    EcRaw r = hal_ec_measure(32);
    float ohm; float ec = ec_from_raw(r, ohm);
    hal_temp_request();
    g_blank = Result();
    g_blank.cell_ohm = ohm;
    g_blank.ec25 = tr_ec_to25(ec, g_live.temp_c, &g_set.cal);
    g_blank.opt = hal_optics_measure(3);
    if (tr_ec_is_air(r.va_mv, r.vb_mv)) g_blank.flags |= TR_FLAG_AIR;   // chamber was empty: absorbance falls back to the last good blank
}

static void finish_analysis() {
    float t = hal_temp_read();
    if (!isnan(t)) g_live.temp_c = t;
    Result r;
    r.temp_c = t;
    r.cell_ohm = g_aj_ohm;
    r.ec25 = tr_ec_to25(g_aj_ec, t, &g_set.cal);
    r.opt = hal_optics_measure(5);
    static OptRaw last_good_blank{0, 0, 2000, 2000, 50, false};
    const OptRaw &b = (g_blank.flags & TR_FLAG_AIR) ? last_good_blank : g_blank.opt;
    if (!(g_blank.flags & TR_FLAG_AIR)) last_good_blank = g_blank.opt;
    r.a450 = tr_absorbance(b.blue_tx, r.opt.blue_tx);
    r.turb = tr_turbidity(r.opt.ir_sc, r.opt.ir_tx, b.ir_sc, b.ir_tx);
    r.sg = tr_sg_estimate(r.ec25, r.a450, &g_set.cal);
    tr_quality_in_t q;
    q.chamber_full = !g_aj_air; q.ec_settled = g_settle.run >= g_settle.hold; q.temp_ok = !isnan(t);
    q.optics_ok = !r.opt.saturated && !b.saturated && b.blue_tx > 20; q.ec_sample = r.ec25; q.ec_blank = g_blank.ec25; q.fallback_trigger = g_fallback_evt;
    uint8_t diluted = 0;
    r.quality = tr_quality(&q, &diluted);
    r.hydration = (r.quality >= 50) ? (uint8_t)tr_hydration_class(r.sg) : (uint8_t)TR_HYD_UNKNOWN;
    if (g_aj_air) r.flags |= TR_FLAG_AIR;
    if (r.opt.saturated) r.flags |= TR_FLAG_OPT_SAT;
    if (diluted) r.flags |= TR_FLAG_DILUTED;
    r.error = g_aj_air ? ERR_NO_SAMPLE : (r.opt.saturated ? ERR_OPT_SAT : ERR_NONE);
    g_last = r;
    app_emit(TR_FT_RESULT, r.error, (uint8_t)STATE_SAMPLING);
    if (r.error) app_emit(TR_FT_ERROR, r.error, (uint8_t)g_fsm.state);
    g_aj = AJ_IDLE;
    g_in.analysis_done = 1;
}

static void analysis_tick(uint32_t now) {
    if (g_aj != AJ_SETTLE || now - g_aj_last < 200) return;
    g_aj_last = now;
    EcRaw r = hal_ec_measure(32);
    g_live.ec = r;
    g_aj_air = tr_ec_is_air(r.va_mv, r.vb_mv);
    float ohm; float ec = ec_from_raw(r, ohm);
    g_aj_ec = ec; g_aj_ohm = ohm;
    bool settled = tr_settle_push(&g_settle, r.ratio);   // ratio, not EC: well-defined even for weak samples
    bool temp_ready = now - g_aj_t0 >= 800;               // DS18B20 12-bit conversion
    // done when the reading has stopped moving (after at least 2 s of settling), or at 9 s, or at once if the chamber is empty
    if (g_aj_air || now - g_aj_t0 >= 9000 || (settled && temp_ready && now - g_aj_t0 >= 2000)) finish_analysis();
}

// ---------------------------------------------------------------- inputs
static void poll_inputs(uint32_t now) {
    if (now - g_t_probe >= 50) {
        g_t_probe = now;
        hal_probes(g_live.sump_mv, g_live.leak_mv);
        g_live.liquid = g_live.sump_mv < 3000;
        bool may_learn = g_fsm.state == STATE_IDLE && !g_live.presence;
        if (g_live.sump_base < 0) g_live.sump_base = g_live.sump_mv;
        else if (may_learn) g_live.sump_base += 0.02f * (g_live.sump_mv - g_live.sump_base);   // slow idle baseline (flush/rinse water)
        g_live.stream = g_live.sump_mv < g_set.stream_abs_mv && g_live.sump_mv < g_set.stream_rel * g_live.sump_base;
        g_leak_hits = (g_live.leak_mv < g_set.leak_mv) ? (uint8_t)min(255, g_leak_hits + 1) : 0;
        g_live.leak = g_leak_hits >= 3;
    }
    TofRaw t = hal_tof_poll();
    if (t.ok && t.valid) g_live.tof = t;
    if (t.ok && t.valid && t.mm > 30 && t.mm < g_set.presence_mm) {
        if (g_presence_hits < 3) g_presence_hits++;
        if (g_presence_hits >= 3) { g_live.presence = true; g_presence_last = now; }
    } else if (t.ok && (t.valid || t.mm == 0)) {
        g_presence_hits = 0;
    }
    if (g_live.presence && now - g_presence_last > 2000) g_live.presence = false;      // 2 s hold after the last near reading
    if (now - g_t_vin >= 1000) {
        g_t_vin = now; g_live.vin_mv = hal_vin_mv();
        if ((g_live.vin_mv < 10500 || g_live.vin_mv > 14000) && now - g_t_vin_err > 60000) {
            g_t_vin_err = now; app_emit(TR_FT_ERROR, g_live.vin_mv < 10500 ? ERR_VIN_LOW : ERR_VIN_HIGH, (uint8_t)g_fsm.state);
        }
    }
    g_in.presence = g_live.presence; g_in.stream = g_live.stream; g_in.sump_liquid = g_live.liquid; g_in.leak = g_live.leak;
}

// ---------------------------------------------------------------- main tick
void app_tick(uint32_t now) {
    poll_inputs(now);
    tr_outputs_t o;
    tr_fsm_step(&g_fsm, now, &g_in, &o);
    g_in.analysis_done = 0; g_in.check_done = 0; g_in.check_air = 0;          // one-shot inputs consumed
    hal_pump(o.pump, o.pump_duty);
    hal_valve(o.valve);

    if (o.state_changed) {
        app_emit(TR_FT_STATE, ERR_NONE, (uint8_t)o.prev_state);
        if (g_fsm.state == STATE_STREAM_DETECTED) { g_set.event_id = g_fsm.event_id; settings_save_event_id(); g_fallback_evt = g_fsm.fallback; }
        if (g_fsm.state == STATE_SAMPLING) { g_med_n = 0; tr_ema_init(&g_ec_ema, tr_ema_alpha(0.25f, 0.75f)); }
        if (g_fsm.state == STATE_IDLE || g_fsm.state == STATE_LOCKOUT) hal_all_off();
    }
    if (o.error) app_emit(TR_FT_ERROR, (uint16_t)o.error, (uint8_t)g_fsm.state);

    switch (o.request) {
    case REQ_BLANK: do_blank(); break;
    case REQ_SAMPLE:
        g_aj = AJ_SETTLE; g_aj_t0 = now; g_aj_last = 0; g_aj_air = false;
        tr_settle_init(&g_settle, 8, 0.01f, 3);
        hal_temp_request();
        break;
    case REQ_PURGE_CHECK: {
        EcRaw r = hal_ec_measure(32); g_live.ec = r;
        g_in.check_done = 1; g_in.check_air = tr_ec_is_air(r.va_mv, r.vb_mv);
        float ohm; float ec = ec_from_raw(r, ohm); g_blank.ec25 = tr_ec_to25(ec, g_live.temp_c, &g_set.cal);
        break; }
    default: break;
    }
    if (g_fsm.state == STATE_ANALYSIS) analysis_tick(now);
    else if (g_aj != AJ_IDLE) g_aj = AJ_IDLE;                                  // FSM left ANALYSIS (timeout): drop the job

    // live conductivity while the sample is being pulled in: median-of-5 against bubbles, then EMA (tau 0.75 s) against sloshing
    if (g_fsm.state == STATE_SAMPLING && now - g_t_live >= 250) {
        g_t_live = now;
        EcRaw r = hal_ec_measure(8); g_live.ec = r;
        float ohm; float ec = ec_from_raw(r, ohm);
        g_med[g_med_n % 5] = ec; g_med_n++;
        float x = (g_med_n >= 5) ? tr_median5(g_med) : ec;
        g_live.ec_live = tr_ema_push(&g_ec_ema, x);
        if (g_med_n % 4 == 0) app_emit(TR_FT_LIVE, ERR_NONE, (uint8_t)g_fsm.state);   // 1 frame per second while sampling
    }
    if (now - g_t_hb >= 60000) { g_t_hb = now; app_emit(TR_FT_HEARTBEAT, ERR_NONE, (uint8_t)g_fsm.state); }
}
