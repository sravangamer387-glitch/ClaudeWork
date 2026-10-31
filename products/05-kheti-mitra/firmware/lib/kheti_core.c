#include "kheti_core.h"

void kheti_default_cfg(kheti_cfg_t *c) {
    c->dry_adc[0] = c->dry_adc[1] = 620; c->wet_adc[0] = c->wet_adc[1] = 300;
    c->start_x10 = 480; c->stop_x10 = 720;
    c->min_interval_ms = 3UL * 3600000UL; c->max_run_ms = 20UL * 60000UL; c->max_daily_ms = 60UL * 60000UL; c->rain_hold_ms = 12UL * 3600000UL;
    c->fallback_run_ms = 5UL * 60000UL; c->fallback_interval_ms = 12UL * 3600000UL;
}
void kheti_init(kheti_t *k, const kheti_cfg_t *c, uint32_t now) {
    k->cfg = *c; k->st = K_IDLE; k->valve = false; k->t_start = now; k->t_last_stop = now - c->min_interval_ms; k->t_rain = now; k->t_day_start = now;
    k->day_on_ms = 0; k->t_valve_on = now; k->had_rain = false; k->last_pct_x10 = 500; k->valid_mask = 3; k->waterings = 0;
}
int kheti_pct_x10(const kheti_cfg_t *c, uint8_t i, uint16_t adc) {
    int dry = c->dry_adc[i], wet = c->wet_adc[i];
    if (adc > dry + 60 || adc + 60 < wet) return -1;                    /* open or shorted sensor */
    long v = 1000L * (dry - (long)adc) / (dry - wet);
    return (int)(v < 0 ? 0 : (v > 1000 ? 1000 : v));
}
static void close_valve(kheti_t *k, uint32_t now) {
    if (k->valve) { k->valve = false; k->t_last_stop = now; k->day_on_ms += (uint32_t)(now - k->t_valve_on); }
}
void kheti_step(kheti_t *k, uint32_t now, kheti_inputs_t in) {
    const kheti_cfg_t *c = &k->cfg;
    if ((uint32_t)(now - k->t_day_start) >= 86400000UL) { k->t_day_start = now; k->day_on_ms = 0; }
    int p0 = kheti_pct_x10(c, 0, in.adc[0]), p1 = kheti_pct_x10(c, 1, in.adc[1]);
    k->valid_mask = (uint8_t)((p0 >= 0 ? 1 : 0) | (p1 >= 0 ? 2 : 0));
    int pct = -1;
    if (p0 >= 0 && p1 >= 0) pct = (p0 + p1) / 2; else if (p0 >= 0) pct = p0; else if (p1 >= 0) pct = p1;
    if (pct >= 0) k->last_pct_x10 = (uint16_t)pct;
    if (in.rain_wet) { k->t_rain = now; k->had_rain = true; }
    bool rain_hold = k->had_rain && (uint32_t)(now - k->t_rain) < c->rain_hold_ms;
    uint32_t day_used = k->day_on_ms + (k->valve ? (uint32_t)(now - k->t_valve_on) : 0u);

    if (k->valve) {                                                     /* stop conditions */
        uint32_t run = (uint32_t)(now - k->t_valve_on);
        uint32_t limit = k->st == K_FAULT_FALLBACK ? c->fallback_run_ms : c->max_run_ms;
        bool done = (k->st == K_WATERING && pct >= (int)c->stop_x10) || run >= limit || day_used >= c->max_daily_ms || in.manual_hold || in.rain_wet || (k->st == K_WATERING && pct < 0);
        if (done) { close_valve(k, now); k->st = pct < 0 ? K_FAULT_FALLBACK : K_IDLE; }
        return;
    }
    if (pct < 0) {                                                       /* both sensors failed: safe fallback timer */
        k->st = K_FAULT_FALLBACK;
        if (!rain_hold && !in.manual_hold && day_used < c->max_daily_ms && (uint32_t)(now - k->t_last_stop) >= c->fallback_interval_ms) { k->valve = true; k->t_valve_on = now; k->waterings++; }
        return;
    }
    k->st = rain_hold ? K_RAIN_HOLD : K_IDLE;
    if (rain_hold || in.manual_hold) return;
    if (pct <= (int)c->start_x10 && (uint32_t)(now - k->t_last_stop) >= c->min_interval_ms && day_used < c->max_daily_ms) {
        k->valve = true; k->t_valve_on = now; k->st = K_WATERING; k->waterings++;
    }
}
bool kheti_valve(const kheti_t *k) { return k->valve; }
uint8_t kheti_status_code(const kheti_t *k) {
    if (k->st == K_WATERING || (k->valve && k->st == K_FAULT_FALLBACK)) return 2;
    if (k->st == K_RAIN_HOLD) return 3;
    if (k->st == K_FAULT_FALLBACK) return 4;
    if (k->day_on_ms >= k->cfg.max_daily_ms) return 5;
    return 1;
}
