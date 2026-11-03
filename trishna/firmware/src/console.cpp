#include "console.h"
#include <Arduino.h>
#include <esp_task_wdt.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "app.h"
#include "board_pins.h"
#include "settings.h"
#include "telemetry.h"
#include "trishna_sense.h"

static char g_line[96]; static uint8_t g_len = 0;
static struct { bool ok; float std_mscm, ratio, temp; } g_pt[2];
static uint32_t g_last_prime_ms = 0;

static void help() {
    Serial.println(F(
        "TRISHNA console\n"
        "  status                      state, fault, live probes, last result\n"
        "  raw                         one EC + optics + temperature reading now (IDLE only)\n"
        "  event                       simulate a user event (bench test: runs blank, sample, analysis, purge)\n"
        "  purge                       run the backwash now\n"
        "  clear                       clear a latched fault (leak, reservoir)\n"
        "  prime fwd|rev <ms>          run the pump (IDLE only, max 30000 ms)\n"
        "  valve <ms>                  open the fresh-water valve (IDLE only, max 30000 ms)\n"
        "  cal ec1 <mS/cm>             capture EC standard 1 (e.g. 1.413) - chamber filled with it\n"
        "  cal ec2 <mS/cm>             capture EC standard 2 (e.g. 12.88)\n"
        "  cal ec solve                fit cell constant K and offset, then 'save'\n"
        "  cal flow <mL>               volume you collected during the last 'prime fwd' -> pump flow\n"
        "  cal sg <c_ec> <c_a450> <c0> SG model from tools/trishna_fit_sg.py\n"
        "  set <key> <value>           keys: sample_ml purge_ml purge_cycles stream_delay_ms lockout_ms fallback_ms\n"
        "                              presence_mm presence_required stream_abs_mv stream_rel leak_mv\n"
        "  wifi <ssid> <password>      for SNTP time stamps (reboot after 'save')\n"
        "  save | defaults | reboot"));
}

static bool idle_only() {
    if (g_fsm.state == STATE_IDLE || g_fsm.state == STATE_LOCKOUT) return true;
    Serial.println(F("busy: wait for IDLE")); return false;
}

// run an actuator for ms while watching the leak probe and feeding the watchdog
static void timed_run(tr_pump_t pump, bool valve, uint32_t ms) {
    if (ms > 30000) ms = 30000;
    uint32_t t0 = millis();
    hal_pump(pump, 255); hal_valve(valve);
    while (millis() - t0 < ms) {
        float s, l; hal_probes(s, l);
        if (l < g_set.leak_mv) { Serial.println(F("LEAK - stopped")); break; }
        esp_task_wdt_reset(); delay(50);
    }
    hal_pump(PUMP_OFF, 0); hal_valve(false);
}

static void print_status() {
    Serial.printf("state %s  fault %s  event %u  flags 0x%04X\n", tr_state_name(g_fsm.state), tr_error_name(g_fsm.fault), g_fsm.event_id, app_flags());
    Serial.printf("sump %.0f mV (base %.0f) stream %d liquid %d | leak %.0f mV %d | presence %d tof %u mm | vin %.2f V\n",
                  g_live.sump_mv, g_live.sump_base, g_live.stream, g_live.liquid, g_live.leak_mv, g_live.leak, g_live.presence, g_live.tof.mm, g_live.vin_mv / 1000.0f);
    Serial.printf("last: EC25 %.2f mS/cm  cell %.0f ohm  T %.2f C  SG %.4f  A450 %.3f  turb %.3f  hyd %u  quality %u  flags 0x%04X\n",
                  g_last.ec25, g_last.cell_ohm, g_last.temp_c, g_last.sg, g_last.a450, g_last.turb, g_last.hydration, g_last.quality, g_last.flags);
    Serial.printf("cal: K %.3f /cm  Rb %.1f ohm  (%s)  SG c_ec %.6f c_a450 %.4f c0 %.4f (%s)  flow %.3f mL/s\n", g_set.cal.k_cell, g_set.cal.rb_ohm,
                  g_set.cal.calibrated ? "calibrated" : "DEFAULT", g_set.cal.c_ec, g_set.cal.c_a450, g_set.cal.c0, g_set.cal.sg_fitted ? "fitted" : "DEFAULT", g_set.flow_ml_s);
    Serial.printf("telemetry: sent %lu dropped %lu  SD %s\n", (unsigned long)tlm_sent(), (unsigned long)tlm_dropped(), tlm_sd_ok() ? "ok" : "absent");
}

static void raw_reading() {
    EcRaw e = hal_ec_measure(64);
    float ohm = tr_ec_cell_ohm(e.ratio, &g_set.cal), ec = tr_ec_mscm(ohm, &g_set.cal);
    hal_temp_request(); delay(800); float t = hal_temp_read();
    OptRaw o = hal_optics_measure(3);
    Serial.printf("EC: Va %.1f mV  Vb %.1f mV  ratio %.4f  cell %.1f ohm  EC(T) %.3f  EC25 %.3f mS/cm  air %d\n", e.va_mv, e.vb_mv, e.ratio, ohm, ec,
                  tr_ec_to25(ec, t, &g_set.cal), tr_ec_is_air(e.va_mv, e.vb_mv));
    Serial.printf("T %.3f C | optics dark tx %.0f sc %.0f | blue tx %.0f | IR tx %.0f sc %.0f | sat %d (target: clear water 1500-2500 mV on blue and IR tx)\n",
                  t, o.dark_tx, o.dark_sc, o.blue_tx, o.ir_tx, o.ir_sc, o.saturated);
}

static bool set_key(const char *k, const char *v) {
    float f = atof(v);
    if (!strcmp(k, "sample_ml")) g_set.sample_ml = f;
    else if (!strcmp(k, "purge_ml")) g_set.purge_ml = f;
    else if (!strcmp(k, "purge_cycles")) g_set.purge_cycles = (uint8_t)f;
    else if (!strcmp(k, "stream_delay_ms")) g_set.stream_delay_ms = (uint32_t)f;
    else if (!strcmp(k, "lockout_ms")) g_set.lockout_ms = (uint32_t)f;
    else if (!strcmp(k, "fallback_ms")) g_set.fallback_ms = (uint32_t)f;
    else if (!strcmp(k, "presence_mm")) g_set.presence_mm = (uint16_t)f;
    else if (!strcmp(k, "presence_required")) g_set.presence_required = (uint8_t)f;
    else if (!strcmp(k, "stream_abs_mv")) g_set.stream_abs_mv = (uint16_t)f;
    else if (!strcmp(k, "stream_rel")) g_set.stream_rel = f;
    else if (!strcmp(k, "leak_mv")) g_set.leak_mv = (uint16_t)f;
    else return false;
    app_apply_settings();
    return true;
}

static void cal_point(int i, float std_mscm) {
    EcRaw e = hal_ec_measure(128);
    hal_temp_request(); delay(800); float t = hal_temp_read();
    if (isnan(t)) { Serial.println(F("no temperature probe: cannot calibrate")); return; }
    if (tr_ec_is_air(e.va_mv, e.vb_mv)) { Serial.println(F("chamber empty (air): fill it with the standard first")); return; }
    g_pt[i] = {true, std_mscm, e.ratio, t};
    Serial.printf("point %d: %.3f mS/cm at %.2f C -> ratio %.5f\n", i + 1, std_mscm, t, e.ratio);
}

static void handle(char *line) {
    char *argv[6] = {0}; int argc = 0;
    for (char *tok = strtok(line, " \t"); tok && argc < 6; tok = strtok(nullptr, " \t")) argv[argc++] = tok;
    if (!argc) return;
    const char *c = argv[0];
    if (!strcmp(c, "help")) help();
    else if (!strcmp(c, "status")) print_status();
    else if (!strcmp(c, "raw")) { if (idle_only()) raw_reading(); }
    else if (!strcmp(c, "event")) { tr_fsm_force_event(&g_fsm, millis()); Serial.println(F("simulated event started")); }
    else if (!strcmp(c, "purge")) { tr_fsm_force_purge(&g_fsm, millis()); Serial.println(F("purge started")); }
    else if (!strcmp(c, "clear")) { tr_fsm_clear_fault(&g_fsm, millis()); Serial.println(F("fault cleared")); }
    else if (!strcmp(c, "prime") && argc == 3) {
        if (!idle_only()) return;
        g_last_prime_ms = (uint32_t)atol(argv[2]);
        timed_run(!strcmp(argv[1], "rev") ? PUMP_REV : PUMP_FWD, false, g_last_prime_ms);
        Serial.printf("pump %s %lu ms done\n", argv[1], (unsigned long)g_last_prime_ms);
    }
    else if (!strcmp(c, "valve") && argc == 2) { if (idle_only()) { timed_run(PUMP_OFF, true, (uint32_t)atol(argv[1])); Serial.println(F("valve closed")); } }
    else if (!strcmp(c, "cal") && argc >= 2) {
        if (!strcmp(argv[1], "ec1") && argc == 3) cal_point(0, atof(argv[2]));
        else if (!strcmp(argv[1], "ec2") && argc == 3) cal_point(1, atof(argv[2]));
        else if (!strcmp(argv[1], "ec") && argc == 3 && !strcmp(argv[2], "solve")) {
            if (!g_pt[0].ok || !g_pt[1].ok) { Serial.println(F("capture ec1 and ec2 first")); return; }
            if (tr_ec_calibrate(&g_set.cal, g_pt[0].std_mscm, g_pt[0].ratio, g_pt[0].temp, g_pt[1].std_mscm, g_pt[1].ratio, g_pt[1].temp) == 0)
                Serial.printf("K = %.4f /cm, Rb = %.2f ohm - type 'save'\n", g_set.cal.k_cell, g_set.cal.rb_ohm);
            else Serial.println(F("calibration rejected (points too close, or out of range): check the standards and the cell"));
        }
        else if (!strcmp(argv[1], "flow") && argc == 3) {
            float ml = atof(argv[2]);
            if (g_last_prime_ms < 2000 || ml <= 0) { Serial.println(F("run 'prime fwd 10000' into a measuring cylinder first")); return; }
            g_set.flow_ml_s = ml / (g_last_prime_ms / 1000.0f); app_apply_settings();
            Serial.printf("flow %.3f mL/s -> sample pumping %lu ms - type 'save'\n", g_set.flow_ml_s, (unsigned long)g_fsm.cfg.sample_pump_ms);
        }
        else if (!strcmp(argv[1], "sg") && argc == 5) {
            g_set.cal.c_ec = atof(argv[2]); g_set.cal.c_a450 = atof(argv[3]); g_set.cal.c0 = atof(argv[4]); g_set.cal.sg_fitted = 1;
            Serial.println(F("SG model set - type 'save'"));
        }
        else Serial.println(F("? cal ec1|ec2 <v> | cal ec solve | cal flow <mL> | cal sg <a> <b> <c>"));
    }
    else if (!strcmp(c, "set") && argc == 3) Serial.println(set_key(argv[1], argv[2]) ? "ok - type 'save' to keep it" : "unknown key");
    else if (!strcmp(c, "wifi") && argc == 3) {
        strncpy(g_set.wifi_ssid, argv[1], sizeof(g_set.wifi_ssid) - 1); strncpy(g_set.wifi_pass, argv[2], sizeof(g_set.wifi_pass) - 1);
        Serial.println(F("stored - type 'save' then 'reboot'"));
    }
    else if (!strcmp(c, "save")) { g_set.event_id = g_fsm.event_id; settings_save(); Serial.println(F("saved")); }
    else if (!strcmp(c, "defaults")) { uint16_t e = g_fsm.event_id; settings_defaults(g_set); g_set.event_id = e; app_apply_settings(); Serial.println(F("defaults loaded (not saved)")); }
    else if (!strcmp(c, "reboot")) { Serial.flush(); ESP.restart(); }
    else Serial.println(F("? type help"));
}

void console_poll() {
    while (Serial.available()) {
        char ch = (char)Serial.read();
        if (ch == '\r') continue;
        if (ch == '\n') { g_line[g_len] = 0; handle(g_line); g_len = 0; }
        else if (g_len < sizeof(g_line) - 1) g_line[g_len++] = ch;
    }
}
