#include <math.h>
#include <string.h>
#include "aq_core.h"
float aq_do_sat_mgl(float t) {                                                    /* Benson & Krause (1984) as used in many handbooks, valid 0-40 C, fresh water, 1 atm */
    double T = t + 273.15, l = -139.34411 + 1.575701e5 / T - 6.642308e7 / (T * T) + 1.243800e10 / (T * T * T) - 8.621949e11 / (T * T * T * T); return (float)exp(l); }
void aq_trend_init(aq_trend_t *t, float a, float b) { memset(t, 0, sizeof *t); t->alpha = a; t->beta = b; }
void aq_trend_push(aq_trend_t *t, float x) {
    if (!t->init) { t->level = x; t->trend = 0; t->var = 0; t->init = true; t->n = 1; return; }
    float pred = t->level + t->trend, err = x - pred;
    t->var = (t->n < 5) ? 0.5f * t->var + 0.5f * err * err : 0.95f * t->var + 0.05f * err * err;                 /* running one-step error variance */
    float prev = t->level; t->level = pred + t->alpha * err; t->trend = t->trend + t->beta * (t->level - prev - t->trend); t->n++; }
float aq_trend_forecast(const aq_trend_t *t, int h) { return t->level + t->trend * (float)h; }
float aq_trend_sigma(const aq_trend_t *t, int h) { return sqrtf(t->var) * sqrtf(1.0f + 0.3f * (float)h); }
int aq_steps_to_breach(const aq_trend_t *t, float lo, float hi, float k, int max_steps) {
    if (!t->init || t->n < 6) return -1;                                          /* need a few samples before trusting the trend */
    for (int h = 0; h <= max_steps; h++) { float f = aq_trend_forecast(t, h), s = k * aq_trend_sigma(t, h); if (f - s <= lo || f + s >= hi) { if (f <= lo + s || f >= hi - s) { if (f - s <= lo && t->trend < 0) return h; if (f + s >= hi && t->trend > 0) return h; } } }
    return -1; }
bool aq_sensor_ok(aq_stuck_t *s, float x, float lo, float hi, int lim) {
    if (!(x >= lo && x <= hi)) return false; if (x == s->last) s->same_count++; else { s->same_count = 0; s->last = x; } return s->same_count < lim; }
void aq_dose_init(aq_dose_t *d) { memset(d, 0, sizeof *d); d->since_last_s = 1 << 20; }
int aq_dose_step(aq_dose_t *d, const aq_dose_cfg_t *c, float ph, bool ok, bool down, int dt) {
    d->since_last_s += dt; d->day_s += dt; if (d->day_s >= 86400) { d->day_s = 0; d->dosed_today_s = 0; d->lockout = false; }
    if (!ok) return 0;                                                            /* never dose on a bad sensor reading */
    if (d->lockout) return 0;
    bool need = down ? (ph > c->setpoint + c->deadband) : (ph < c->setpoint - c->deadband); if (!need || d->since_last_s < c->min_interval_s) return 0;
    if (d->dosed_today_s + c->pulse_s > c->max_daily_s) { d->lockout = true; return 0; }                       /* daily cap reached: stop and wait for a human */
    d->since_last_s = 0; d->dosed_today_s += c->pulse_s; return c->pulse_s; }
bool aq_aerator(bool was, float d, float sat, float on_f, float off_f) { if (d < on_f * sat) return true; if (d > off_f * sat) return false; return was; }
