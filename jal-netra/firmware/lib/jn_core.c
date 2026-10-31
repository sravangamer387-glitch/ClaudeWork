#include <math.h>
#include "jn_core.h"
#define PI_F 3.14159265f
void jn_demod_init(jn_demod_t *d, float f0, float fs, uint16_t n) {
    d->f0 = f0; d->fs = fs; d->n = n > JN_MAXN ? JN_MAXN : n;
    for (uint16_t k = 0; k < d->n; k++) { d->win[k] = 0.5f - 0.5f * cosf(2 * PI_F * k / (d->n - 1)); float a = -2 * PI_F * f0 * k / fs; d->c_re[k] = cosf(a); d->c_im[k] = sinf(a); }
}
void jn_demod(const jn_demod_t *d, const int16_t *x, float *phase, float *amp) {
    float re = 0, im = 0; for (uint16_t k = 0; k < d->n; k++) { float v = d->win[k] * (float)x[k]; re += v * d->c_re[k]; im += v * d->c_im[k]; }
    *phase = atan2f(im, re); *amp = sqrtf(re * re + im * im);
}
float jn_tof_coarse(const int16_t *x, uint16_t n, float fs, float frac) {
    /* envelope = |x| smoothed over about one carrier period (4 samples); first crossing of frac * peak, linearly interpolated */
    float env[JN_MAXN], pk = 0; uint16_t m = n > JN_MAXN ? JN_MAXN : n;
    for (uint16_t i = 0; i < m; i++) { float s = 0; uint16_t c = 0; for (int j = -2; j <= 1; j++) { int k = (int)i + j; if (k >= 0 && k < (int)m) { s += fabsf((float)x[k]); c++; } } env[i] = s / c; if (env[i] > pk) pk = env[i]; }
    if (pk < 1.0f) return -1.0f;
    float th = frac * pk;
    for (uint16_t i = 1; i < m; i++) if (env[i] >= th && env[i - 1] < th) return ((float)(i - 1) + (th - env[i - 1]) / (env[i] - env[i - 1])) / fs;
    return -1.0f;
}
void jn_acc_reset(jn_acc_t *a) { a->sx = a->sy = a->amp_up = a->amp_dn = a->tof_up = a->tof_dn = 0; a->n = 0; }
void jn_acc_add(jn_acc_t *a, float pu, float pd, float au, float ad, float tu, float td) {
    float d = pu - pd; a->sx += cosf(d); a->sy += sinf(d); a->amp_up += au; a->amp_dn += ad; a->tof_up += tu; a->tof_dn += td; a->n++;
}
bool jn_acc_result(const jn_acc_t *a, float f0, float *dt, float *tof, float *amp, float *quality) {
    if (!a->n) return false;
    float dphi = atan2f(a->sy, a->sx); *dt = -dphi / (2 * PI_F * f0);                 /* later arrival upstream = negative phase difference */
    *tof = 0.5f * (a->tof_up + a->tof_dn) / a->n; *amp = 0.5f * (a->amp_up + a->amp_dn) / a->n; *quality = sqrtf(a->sx * a->sx + a->sy * a->sy) / a->n; return true;
}
float jn_c_water(float T) { return 1402.385f + 5.038813f * T - 5.799136e-2f * T * T + 3.287156e-4f * T * T * T - 1.398845e-6f * T * T * T * T + 2.787860e-9f * T * T * T * T * T; }
float jn_temp_from_c(float c) { float T = 20.0f; for (int i = 0; i < 6; i++) { float f = jn_c_water(T) - c, d = (jn_c_water(T + 0.1f) - jn_c_water(T - 0.1f)) / 0.2f; T -= f / d; } return T; }
float jn_nu_water(float T) { float mu = 2.414e-5f * powf(10.0f, 247.8f / (T + 273.15f - 140.0f)); float rho = 1000.0f * (1.0f - (T + 288.9414f) / (508929.2f * (T + 68.12963f)) * (T - 3.9863f) * (T - 3.9863f)); return mu / rho; }
float jn_kprofile(float Re) {
    if (Re <= 2000.0f) return 0.75f;
    float lr = log10f(Re), t = (lr - 3.3f) / 1.7f; t = t < 0 ? 0 : t > 1 ? 1 : t; float n = 6.0f + 2.0f * t;
    float kt = 2 * n * n / ((n + 1) * (2 * n + 1)) / (n / (n + 1)); if (Re >= 4000.0f) return kt;
    float w = (Re - 2000.0f) / 2000.0f; return 0.75f * (1 - w) + kt * w;
}
void jn_cfg_default(jn_cfg_t *c) { c->length_m = 0.060f; c->bore_m = 0.012f; c->zero_dt_s = 0; c->zero_slope_s_per_c = 0; c->zero_t_ref_c = 20.0f; c->k_cal = 1.0f; }
float jn_flow_lpm(const jn_cfg_t *c, float dt, float tof, float *temp_c) {
    float cs = c->length_m / tof, T = jn_temp_from_c(cs); if (temp_c) *temp_c = T;
    float dt0 = c->zero_dt_s + c->zero_slope_s_per_c * (T - c->zero_t_ref_c); float v = (dt - dt0) * cs * cs / (2.0f * c->length_m);
    float A = PI_F * c->bore_m * c->bore_m / 4.0f; float Re = fabsf(v) * c->bore_m / jn_nu_water(T); if (Re < 1.0f) Re = 1.0f;
    return v * A * jn_kprofile(Re) * c->k_cal * 60000.0f;
}
void jn_zero_init(jn_zero_t *z) { z->dt_s = 0; z->t_c = 20; z->ema = 0; z->quiet_s = 0; z->n = 0; }
void jn_zero_update(jn_zero_t *z, jn_cfg_t *c, float dt_raw, float T, bool quiet) {
    if (!quiet) { z->quiet_s = 0; return; }
    z->quiet_s++; if (z->quiet_s < 120) return;                                  /* need 2 quiet minutes before trusting the offset */
    float expect = c->zero_dt_s + c->zero_slope_s_per_c * (T - c->zero_t_ref_c); float err = dt_raw - expect;
    float g = z->n < 30 ? 0.2f : 0.02f; c->zero_dt_s += g * err; z->n++;          /* slow integrator keeps the zero at the temperature seen while quiet */
    if (z->n > 60 && fabsf(T - z->t_c) > 3.0f) { float slope = (dt_raw - z->dt_s) / (T - z->t_c); c->zero_slope_s_per_c += 0.1f * (slope - c->zero_slope_s_per_c); }
    if (fabsf(T - z->t_c) > 3.0f || z->n == 1) { z->dt_s = dt_raw; z->t_c = T; }
}
void jn_leak_init(jn_leak_t *l) {
    l->q_noise_lpm = 0.004f; l->q_leak_min_lpm = 0.008f; l->q_burst_lpm = 25.0f; l->leak_after_s = 6 * 3600; l->quiet_needed_s = 300; l->burst_after_s = 120; l->suspect_after_s = 2 * 3600;
    l->st = JN_IDLE; l->run_s = l->nonzero_s = l->since_quiet_s = l->burst_s = 0; l->volume_l = l->volume_event_l = 0; l->q_lp = 0; l->events = 0;
}
jn_state_t jn_leak_step(jn_leak_t *l, float q) {
    float a = fabsf(q); l->q_lp += 0.2f * (a - l->q_lp); l->volume_l += (q > 0 ? q : 0) / 60.0f;
    bool flowing = l->q_lp > l->q_noise_lpm;
    if (flowing) { l->nonzero_s++; l->since_quiet_s++; l->volume_event_l += (q > 0 ? q : 0) / 60.0f; } else { l->nonzero_s = l->nonzero_s > 10 ? l->nonzero_s - 10 : 0; if (l->nonzero_s == 0) { l->since_quiet_s = 0; l->volume_event_l = 0; } }
    if (l->q_lp > l->q_burst_lpm) l->burst_s++; else l->burst_s = 0;
    jn_state_t s = JN_IDLE;
    if (l->burst_s >= l->burst_after_s) s = JN_BURST;
    else if (flowing && l->since_quiet_s >= l->leak_after_s && l->q_lp < 1.0f && l->q_lp >= l->q_leak_min_lpm) s = JN_LEAK;     /* tiny continuous flow with no 5-min pause for 6 h */
    else if (flowing && l->since_quiet_s >= l->suspect_after_s && l->q_lp < 1.0f) s = JN_SUSPECT;
    else if (flowing) s = JN_USE;
    if (s == JN_USE && l->st == JN_IDLE) l->events++;
    l->st = s; return s;
}
