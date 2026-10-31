#include "gas_core.h"
#define FP 65536LL                                  /* fixed-point scale of the baseline */

void gas_default_cfg(gas_cfg_t *c) {
    c->clean_air_nominal = 180; c->clean_air_max = 240; c->alarm_delta = 150; c->prealarm_delta = 75; c->alarm_abs = 410;
    c->warmup_ms = 120000UL; c->alarm_confirm_ms = 8000UL; c->prealarm_confirm_ms = 30000UL; c->clear_hold_ms = 60000UL; c->silence_ms = 300000UL;
    c->fault_low = 20; c->fault_high = 1010; c->fault_confirm_ms = 10000UL; c->base_up_per_h = 6; c->base_down_per_h = 60; c->base_max_rise = 80;
}

void gas_init(gas_t *g, const gas_cfg_t *c, uint32_t now, bool watchdog_reset) {
    g->cfg = *c; g->st = G_WARMUP; g->buzzer = BZ_OFF; g->led = 2;
    g->t0 = g->t_last = g->t_over = g->t_pre = g->t_clear = g->t_good = g->t_abs = now; g->silenced_until = g->t_test_end = now;
    g->base = (int32_t)(c->clean_air_nominal * FP); g->base_first = g->base;       /* start from the factory reference, never from the first reading */
    g->base_init = false; g->base_trackable = false; g->aged = false; g->silenced = false; g->relay_shutoff = false; g->test_ok = false; g->delta_at_silence = 0;
    g->warmup_ms_eff = watchdog_reset ? 15000UL : c->warmup_ms;                    /* after a watchdog reset the sensor is already warm */
}

int16_t gas_delta(const gas_t *g, uint16_t adc) { return (int16_t)((int32_t)adc - (int32_t)(g->base / FP)); }

static void update_baseline(gas_t *g, uint16_t adc, uint32_t dt_ms) {
    const gas_cfg_t *c = &g->cfg;
    int64_t err = (int64_t)adc * FP - g->base;
    int64_t step = err / 1024;                                                      /* about 17 min time constant at 1 Hz */
    int64_t up = (int64_t)c->base_up_per_h * FP * dt_ms / 3600000LL, down = (int64_t)c->base_down_per_h * FP * dt_ms / 3600000LL;
    if (step > up) step = up;
    if (step < -down) step = -down;
    g->base += (int32_t)step;
    int32_t cap = g->base_first + (int32_t)((int64_t)c->base_max_rise * FP);
    if (g->base > cap) g->base = cap;
}

void gas_step(gas_t *g, uint32_t now, gas_inputs_t in) {
    const gas_cfg_t *c = &g->cfg;
    uint32_t dt = (uint32_t)(now - g->t_last); g->t_last = now;
    bool bad = in.adc <= c->fault_low || in.adc >= c->fault_high;
    if (!bad) g->t_good = now;
    bool fault_now = bad && (uint32_t)(now - g->t_good) >= c->fault_confirm_ms;

    /* after the 30 s preheat transient: adopt the reading as the baseline ONLY if it is clean air; otherwise keep the factory reference */
    if (!g->base_init && (uint32_t)(now - g->t0) >= 30000UL && !bad) {
        g->base_init = true;
        if (in.adc <= c->clean_air_max) { g->base = (int32_t)((int64_t)in.adc * FP); g->base_first = g->base; g->base_trackable = true; }
    }
    int16_t d = gas_delta(g, in.adc);

    /* baseline follows slow drift only in clean air, never faster than the rise/fall limits */
    if (g->base_init && g->base_trackable && !bad && (g->st == G_NORMAL || g->st == G_WARMUP) && d < (int16_t)(c->prealarm_delta / 2)) update_baseline(g, in.adc, dt);
    d = gas_delta(g, in.adc);
    bool at_cap = g->base >= g->base_first + (int32_t)((int64_t)c->base_max_rise * FP) - 1 && g->base_trackable;

    /* timers count time CONTINUOUSLY above a level: they restart whenever the reading drops below it */
    bool above_alarm = g->base_init && (d >= (int16_t)c->alarm_delta || in.adc >= c->alarm_abs);
    bool above_pre = g->base_init && d >= (int16_t)c->prealarm_delta;
    if (!above_alarm) g->t_over = now;
    if (!above_pre) g->t_pre = now;

    switch (g->st) {
    case G_WARMUP:
        if (fault_now) g->st = G_FAULT;
        else if (g->base_init && (uint32_t)(now - g->t0) >= g->warmup_ms_eff) g->st = G_NORMAL;
        break;
    case G_FAULT:
        if (!bad && !g->aged) { g->st = G_WARMUP; g->t0 = now - g->warmup_ms_eff + 30000UL; g->base_init = false; }
        break;
    default: break;
    }
    if (g->st == G_FAULT && g->aged && above_alarm && (uint32_t)(now - g->t_over) >= c->alarm_confirm_ms) { g->st = G_ALARM; g->t_clear = now; g->silenced = false; }   /* an aged sensor still alarms on real gas */
    if (g->base_init && (g->st == G_WARMUP) && (uint32_t)(now - g->t0) >= 45000UL && above_alarm && (uint32_t)(now - g->t_over) >= c->alarm_confirm_ms) {
        g->st = G_ALARM; g->t_clear = now; g->silenced = false;                      /* gas during warm-up still alarms */
    }
    if (g->st == G_NORMAL || g->st == G_PREALARM || g->st == G_ALARM) {
        if (fault_now || (at_cap && !above_pre && g->st == G_NORMAL)) { if (!fault_now) g->aged = true; g->st = G_FAULT; }   /* open/shorted sensor, or aged beyond the drift limit */
        else {
            if (g->st != G_ALARM && (uint32_t)(now - g->t_over) >= c->alarm_confirm_ms) { g->st = G_ALARM; g->t_clear = now; g->silenced = false; }
            else if (g->st == G_NORMAL && (uint32_t)(now - g->t_pre) >= c->prealarm_confirm_ms) g->st = G_PREALARM;
            if (g->st == G_PREALARM && d < (int16_t)(c->prealarm_delta * 6 / 10)) g->st = G_NORMAL;
            if (g->st == G_ALARM) {
                if (d >= (int16_t)(c->alarm_delta * 6 / 10) || in.adc >= c->alarm_abs) g->t_clear = now;     /* still elevated: stays latched */
                if ((uint32_t)(now - g->t_clear) >= c->clear_hold_ms) g->st = G_NORMAL;
                if (in.button_silence && !g->silenced) { g->silenced = true; g->silenced_until = now + c->silence_ms; g->delta_at_silence = d; }
                if (g->silenced && ((int32_t)(now - g->silenced_until) >= 0 || d >= (int16_t)(g->delta_at_silence + g->delta_at_silence / 2))) g->silenced = false;
            }
        }
    }
    if (in.button_test) { g->t_test_end = now + 2000UL; g->test_ok = !bad; }
    bool testing = (int32_t)(g->t_test_end - now) > 0;

    g->relay_shutoff = (g->st == G_ALARM);                                          /* hook for a future shut-off valve (not used in v1) */
    switch (g->st) {
    case G_WARMUP: g->led = 2; g->buzzer = BZ_OFF; break;
    case G_NORMAL: g->led = 1; g->buzzer = in.battery_low ? BZ_CHIRP : BZ_OFF; break;
    case G_PREALARM: g->led = 2; g->buzzer = BZ_SLOW; break;
    case G_ALARM: g->led = 3; g->buzzer = g->silenced ? BZ_OFF : BZ_CONTINUOUS; break;
    case G_FAULT: g->led = 4; g->buzzer = BZ_CHIRP; break;
    }
    if (testing && g->st != G_ALARM) g->buzzer = g->test_ok ? BZ_CONTINUOUS : BZ_CHIRP;
}
