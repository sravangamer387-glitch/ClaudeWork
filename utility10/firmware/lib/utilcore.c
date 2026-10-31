#include <math.h>
#include "utilcore.h"
static bool after(uint32_t now, uint32_t t) { return (int32_t)(now - t) >= 0; }

float ut_goertzel(const int16_t *x, int n, float f, float fs) {
    float w = 2.0f * 3.14159265f * f / fs, c = 2.0f * cosf(w), s1 = 0, s2 = 0;
    for (int i = 0; i < n; i++) { float s0 = (float)x[i] + c * s1 - s2; s2 = s1; s1 = s0; }
    return s1 * s1 + s2 * s2 - c * s1 * s2;
}
void seeti_init(seeti_t *s, uint16_t target) { s->t_start = s->t_end = 0; s->in_whistle = s->tone_prev = false; s->count = 0; s->target = target; s->min_ms = 400; s->gap_ms = 1500; s->ratio = 0.35f; s->done = false; }
void seeti_block(seeti_t *s, uint32_t now, float tone, float total, int n) {
    /* a pure tone puts almost all its energy in one Goertzel bin: tone_power / (n/2 * total_energy) approaches 1 for a pure sine and ~ (1/n)*k for noise */
    bool tone_now = total > 1.0f && (tone / ((float)n * 0.5f * total)) > s->ratio;
    if (tone_now) {
        if (!s->tone_prev) s->t_start = now;
        s->tone_prev = true; s->t_end = now;
        if ((uint32_t)(now - s->t_start) >= s->min_ms) s->in_whistle = true;           /* a tone must last min_ms to count: rejects clinks and beeps */
    }
    else if (s->tone_prev && (uint32_t)(now - s->t_end) > 200u) {                      /* tone gone for 200 ms: whistle over */
        if (s->in_whistle) { s->count++; if (s->count >= s->target) s->done = true; }
        s->in_whistle = false; s->tone_prev = false;
    }
}

void gs_init(gas_scale_t *g, int32_t zero, float cpk, float tare, float net) { g->zero_counts = zero; g->counts_per_kg = cpk; g->tare_kg = tare; g->net_kg = net; g->w_kg = 0; g->stable = false; g->nh = 0; g->hi = 0; g->last_stable = 0; g->fast = 0; g->t_stable = 0; g->kg_per_day = 0; }
void gs_calibrate(gas_scale_t *g, int32_t zero, int32_t known, float kg) { g->zero_counts = zero; g->counts_per_kg = (float)(known - zero) / kg; }
void gs_sample(gas_scale_t *g, uint32_t now, int32_t counts) {
    float w = (float)(counts - g->zero_counts) / g->counts_per_kg;
    g->fast = g->nh == 0 ? w : g->fast + 0.5f * (w - g->fast);                    /* quick filter for detecting movement */
    g->hist[g->hi] = g->fast; g->hi = (uint8_t)((g->hi + 1) & 7u); if (g->nh < 8) g->nh++;      /* ring of the last 8 filtered samples */
    int m = g->nh < 8 ? g->nh : 8; float mn = 1e9f, mx = -1e9f, sum = 0; for (int i = 0; i < m; i++) { if (g->hist[i] < mn) mn = g->hist[i]; if (g->hist[i] > mx) mx = g->hist[i]; sum += g->hist[i]; }
    bool calm = m == 8 && (mx - mn) < 0.05f;                                       /* 50 g window over 0.8 s */
    if (!calm) g->t_stable = now;
    if (calm && (uint32_t)(now - g->t_stable) >= 3000u) { g->stable = true; g->w_kg = sum / m; } else if (!calm) g->stable = false;
}
float gs_remaining_kg(const gas_scale_t *g) { float r = g->w_kg - g->tare_kg; if (r < 0) r = 0; if (r > g->net_kg * 1.1f) r = g->net_kg * 1.1f; return r; }
int gs_percent(const gas_scale_t *g) { int p = (int)(100.0f * gs_remaining_kg(g) / g->net_kg + 0.5f); return p > 100 ? 100 : p; }
void gs_daily(gas_scale_t *g) { if (!g->stable) return; if (g->last_stable > 0 && g->w_kg < g->last_stable) { float used = g->last_stable - g->w_kg; g->kg_per_day = g->kg_per_day == 0 ? used : 0.8f * g->kg_per_day + 0.2f * used; } g->last_stable = g->w_kg; }
float gs_days_left(const gas_scale_t *g) { return g->kg_per_day > 0.02f ? gs_remaining_kg(g) / g->kg_per_day : -1.0f; }

void fd_init(fd_t *f, uint32_t warn, uint32_t alarm) { f->st = FD_CLOSED; f->t_open = f->t_next = 0; f->open_total_s = 0; f->opens = 0; f->door_prev = false; f->warn_ms = warn; f->alarm_ms = alarm; f->sound = 0; }
void fd_step(fd_t *f, uint32_t now, bool open) {
    if (open && !f->door_prev) { f->t_open = now; f->opens++; f->st = FD_OPEN; f->t_next = now; }
    if (!open && f->door_prev) { f->open_total_s += (now - f->t_open) / 1000u; f->st = FD_CLOSED; f->sound = 0; }
    f->door_prev = open;
    if (!open) return;
    uint32_t el = now - f->t_open;
    if (el >= f->alarm_ms) { f->st = FD_ALARM; f->sound = 2; }
    else if (el >= f->warn_ms) { f->st = FD_WARN; f->sound = 0; if (after(now, f->t_next)) { f->t_next = now + 10000u; f->sound = 1; } }
}

void bm_init(bm_t *m, uint16_t ipk) { m->imp_per_kwh = ipk; m->pulses = m->day_pulses = 0; m->t_last_pulse = 0; m->light_prev = false; m->last_gap_ms = 0; m->fixed_charge = 0;
    float up[BM_SLABS] = {100, 200, 400, 1e9f}, rate[BM_SLABS] = {3.0f, 5.0f, 7.5f, 9.0f}; for (int i = 0; i < BM_SLABS; i++) { m->slab_upto[i] = up[i]; m->slab_rate[i] = rate[i]; } }
void bm_sample(bm_t *m, uint32_t now, bool on) {
    if (on && !m->light_prev) { if (m->pulses == 0 || (uint32_t)(now - m->t_last_pulse) >= 20u) { if (m->pulses) m->last_gap_ms = now - m->t_last_pulse; m->pulses++; m->day_pulses++; m->t_last_pulse = now; } }
    m->light_prev = on;
}
float bm_kwh(const bm_t *m) { return (float)m->pulses / (float)m->imp_per_kwh; }
float bm_watts(const bm_t *m, uint32_t now) { if (m->last_gap_ms == 0 || (uint32_t)(now - m->t_last_pulse) > 600000u) return 0; uint32_t since = now - m->t_last_pulse; uint32_t gap = since > m->last_gap_ms ? since : m->last_gap_ms; return 3600.0f * 1000.0f / (float)m->imp_per_kwh / ((float)gap / 1000.0f); }
float bm_bill(const bm_t *m, float kwh) { float bill = m->fixed_charge, lo = 0; for (int i = 0; i < BM_SLABS && kwh > lo; i++) { float hi = m->slab_upto[i], used = (kwh < hi ? kwh : hi) - lo; bill += used * m->slab_rate[i]; lo = hi; } return bill; }

void pc_init(pc_t *p) { p->n = p->head = 0; p->out = false; p->raw_prev = true; p->t_change_s = 0; p->total_out_s = 0; p->count = 0; for (int i = 0; i < PC_LOG; i++) p->start_s[i] = p->dur_s[i] = 0; }
void pc_sample(pc_t *p, uint32_t now, bool ok) {
    if (ok != p->raw_prev) { p->t_change_s = now; p->raw_prev = ok; }
    if ((uint32_t)(now - p->t_change_s) < 2u) return;                              /* 2 s debounce */
    if (!ok && !p->out) { p->out = true; p->count++; p->start_s[p->head] = p->t_change_s; p->dur_s[p->head] = 0; }
    if (!ok && p->out) { p->dur_s[p->head] = now - p->start_s[p->head]; }
    if (ok && p->out) { p->out = false; p->dur_s[p->head] = p->t_change_s - p->start_s[p->head]; p->total_out_s += p->dur_s[p->head]; p->head = (uint8_t)((p->head + 1) % PC_LOG); if (p->n < PC_LOG) p->n++; }
}

void ct_init(ct_t *c) { for (int i = 0; i < 4; i++) { c->active[i] = c->ringing[i] = false; c->end_ms[i] = 0; } }
void ct_set(ct_t *c, uint8_t ch, uint32_t now, uint32_t s) { if (ch > 3) return; c->end_ms[ch] = now + s * 1000u; c->active[ch] = s > 0; c->ringing[ch] = false; }
uint32_t ct_remaining_s(const ct_t *c, uint8_t ch, uint32_t now) { if (ch > 3 || !c->active[ch]) return 0; int32_t d = (int32_t)(c->end_ms[ch] - now); return d <= 0 ? 0 : ((uint32_t)d + 999u) / 1000u; }
void ct_add(ct_t *c, uint8_t ch, uint32_t now, int32_t delta) { if (ch > 3) return; int32_t cur = (int32_t)ct_remaining_s(c, ch, now) + delta; if (cur < 0) cur = 0; if (cur > 99 * 60) cur = 99 * 60; ct_set(c, ch, now, (uint32_t)cur); }
void ct_ack(ct_t *c, uint8_t ch) { if (ch > 3) return; c->ringing[ch] = false; c->active[ch] = false; }
uint8_t ct_step(ct_t *c, uint32_t now) { uint8_t m = 0; for (int i = 0; i < 4; i++) { if (c->active[i] && after(now, c->end_ms[i])) c->ringing[i] = true; if (c->ringing[i]) m |= (uint8_t)(1u << i); } return m; }

void rain_init(rain_t *r) { r->wet_thr = 400; r->dry_thr = 250; r->t_wet = r->t_dry = r->mute_until = 0; r->raining = r->alert = r->muted = false; r->wet_ms = 3000; r->dry_ms = 120000; r->mute_ms = 1800000; }
void rain_step(rain_t *r, uint32_t now, uint16_t adc, bool mute) {
    if (adc < r->wet_thr) r->t_wet = now;
    if (adc > r->dry_thr) r->t_dry = now;
    if (!r->raining && (uint32_t)(now - r->t_wet) >= r->wet_ms) { r->raining = true; r->alert = true; r->muted = false; }
    if (r->raining && (uint32_t)(now - r->t_dry) >= r->dry_ms) { r->raining = false; r->alert = false; r->muted = false; }
    if (mute && r->alert) { r->alert = false; r->muted = true; r->mute_until = now + r->mute_ms; }
    if (r->muted && after(now, r->mute_until)) { r->muted = false; if (r->raining) r->alert = true; }                 /* still raining after the mute: ring again */
}

void tap_init(tap_t *t, float ppl) { t->pulses_per_litre = ppl; t->pulses = t->session_pulses = t->day_pulses = 0; t->last_pulse_ms = 0; t->in_session = false; t->last_session_l = 0; t->target_l = 0; t->target_hit = false; }
void tap_pulses(tap_t *t, uint32_t now, uint32_t n) { if (!n) return; if (!t->in_session) { t->in_session = true; t->session_pulses = 0; t->target_hit = false; } t->session_pulses += n; t->day_pulses += n; t->pulses += n; t->last_pulse_ms = now; if (t->target_l > 0 && tap_session_l(t) >= t->target_l) t->target_hit = true; }
void tap_step(tap_t *t, uint32_t now) { if (t->in_session && (uint32_t)(now - t->last_pulse_ms) >= 5000u) { t->in_session = false; t->last_session_l = tap_session_l(t); } }
float tap_session_l(const tap_t *t) { return (float)t->session_pulses / t->pulses_per_litre; }
float tap_day_l(const tap_t *t) { return (float)t->day_pulses / t->pulses_per_litre; }
