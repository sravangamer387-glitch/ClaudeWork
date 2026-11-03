#include "trishna_filters.h"
#include <math.h>
#include <string.h>

void tr_ma_init(tr_ma_t *m, uint8_t n) {
    memset(m, 0, sizeof(*m));
    m->n = (n == 0) ? 1 : (n > TR_MA_MAX ? TR_MA_MAX : n);
}
float tr_ma_push(tr_ma_t *m, float x) {
    if (m->count == m->n) m->sum -= m->buf[m->idx]; else m->count++;
    m->buf[m->idx] = x; m->sum += x;
    m->idx = (uint8_t)((m->idx + 1) % m->n);
    return tr_ma_mean(m);
}
float tr_ma_mean(const tr_ma_t *m) { return m->count ? m->sum / (float)m->count : 0.0f; }
float tr_ma_std(const tr_ma_t *m) {
    if (m->count < 2) return 0.0f;
    float mu = tr_ma_mean(m), s = 0.0f;
    for (uint8_t i = 0; i < m->count; i++) { float d = m->buf[i] - mu; s += d * d; }
    return sqrtf(s / (float)(m->count - 1));
}
uint8_t tr_ma_full(const tr_ma_t *m) { return m->count == m->n; }

void tr_ema_init(tr_ema_t *e, float alpha) { e->y = 0.0f; e->alpha = alpha; e->primed = 0; }
float tr_ema_alpha(float dt_s, float tau_s) { return (tau_s <= 0.0f) ? 1.0f : 1.0f - expf(-dt_s / tau_s); }
float tr_ema_push(tr_ema_t *e, float x) {
    if (!e->primed) { e->y = x; e->primed = 1; } else e->y += e->alpha * (x - e->y);
    return e->y;
}

static void sortf(float *v, int n) {             /* insertion sort: n is small */
    for (int i = 1; i < n; i++) { float k = v[i]; int j = i - 1; while (j >= 0 && v[j] > k) { v[j + 1] = v[j]; j--; } v[j + 1] = k; }
}
float tr_median5(const float v[5]) { float t[5]; memcpy(t, v, sizeof t); sortf(t, 5); return t[2]; }
float tr_median_n(float *v, int n) {
    if (n <= 0) return 0.0f;
    if (n > 64) n = 64;
    sortf(v, n);
    return (n & 1) ? v[n / 2] : 0.5f * (v[n / 2 - 1] + v[n / 2]);
}

void tr_settle_init(tr_settle_t *s, uint8_t window, float rel_tol, uint8_t hold) { tr_ma_init(&s->win, window); s->tol = rel_tol; s->hold = hold ? hold : 1; s->run = 0; }
uint8_t tr_settle_push(tr_settle_t *s, float x) {
    tr_ma_push(&s->win, x);
    if (!tr_ma_full(&s->win)) { s->run = 0; return 0; }
    float mu = fabsf(tr_ma_mean(&s->win)), sd = tr_ma_std(&s->win);
    uint8_t ok = (mu > 1e-9f) ? (sd / mu <= s->tol) : (sd <= 1e-9f);
    s->run = ok ? (uint8_t)(s->run < 255 ? s->run + 1 : 255) : 0;
    return s->run >= s->hold;
}
