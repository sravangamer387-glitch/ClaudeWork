#include <math.h>
#include <string.h>
#include "kn_vib.h"
#include "kn_vib_model.h"
#define DEC 8
#define NE (KV_N / DEC)
#define FSE (KV_FS / DEC)
#define BPFO 3.58f
#define BPFI 5.42f
static const float LP_HP = 0.4157f, LP_EN = 0.2536f;   /* filled below by exact values */
static float goertzel(const float *y, int n, float f, float fs) {
    float w = 2.0f * (float)M_PI * f / fs, c = 2.0f * cosf(w), s1 = 0, s2 = 0;
    for (int i = 0; i < n; i++) { float s0 = y[i] + c * s1 - s2; s2 = s1; s1 = s0; }
    return (s1 * s1 + s2 * s2 - c * s1 * s2) * 4.0f / ((float)n * (float)n);
}
static float peak3(const float *y, int n, float f, float fs) {
    float d = fs / (float)n, m = -1;
    for (int k = -1; k <= 1; k++) { float p = goertzel(y, n, f + (float)k * d, fs); if (p > m) m = p; }
    return m;
}
void kv_features(const float *xin, float fr, float *feat) {
    float lp_hp = 1.0f - expf(-2.0f * (float)M_PI * 300.0f / KV_FS), lp_en = 1.0f - expf(-2.0f * (float)M_PI * 150.0f / KV_FS); (void)LP_HP; (void)LP_EN;
    static float x[KV_N]; double mean = 0; for (int i = 0; i < KV_N; i++) mean += xin[i]; mean /= KV_N;
    double s2 = 0, s4 = 0, mx = 0; for (int i = 0; i < KV_N; i++) { x[i] = (float)(xin[i] - mean); double v = x[i]; s2 += v * v; s4 += v * v * v * v; if (fabs(v) > mx) mx = fabs(v); }
    double r = sqrt(s2 / KV_N) + 1e-9, k = (s4 / KV_N) / (r * r * r * r), cr = mx / r;
    float e[NE]; float lp = 0, en = 0; int ne = 0; double em = 0;
    for (int i = 0; i < KV_N; i++) { lp += lp_hp * (x[i] - lp); float h = x[i] - lp; en += lp_en * (fabsf(h) - en); if (i % DEC == DEC / 2 && ne < NE) { e[ne++] = en; em += en; } }
    em /= NE; double ev = 0; for (int i = 0; i < NE; i++) { e[i] -= (float)em; ev += (double)e[i] * e[i]; } ev = ev / NE + 1e-12;
    float rr = (float)(r * r);
#define EP(f) fminf((float)(peak3(e, NE, (f), FSE) / ev), 4.0f)
#define RP(f) fminf(peak3(x, KV_N, (f), KV_FS) / rr, 4.0f)
    feat[0] = log10f((float)r); feat[1] = (float)k; feat[2] = (float)cr; feat[3] = EP(fr); feat[4] = EP(BPFO * fr); feat[5] = EP(2 * BPFO * fr); feat[6] = EP(BPFI * fr);
    feat[7] = 0.5f * (EP(BPFI * fr + fr) + EP(BPFI * fr - fr)); feat[8] = RP(fr); feat[9] = RP(2 * fr);
}
int kv_classify_features(const float *feat, int32_t *logits) {
    int32_t a0[KV_NF], a1[KV_H1], a2[KV_H2], lg[4];
    for (int i = 0; i < KV_NF; i++) { float z = (feat[i] - kv_mu[i]) / kv_sd[i]; float q = floorf(z / kv_sin + 0.5f); a0[i] = q > 127 ? 127 : (q < -127 ? -127 : (int32_t)q); }
    for (int o = 0; o < KV_H1; o++) { int32_t acc = kv_b1[o]; for (int i = 0; i < KV_NF; i++) acc += (int32_t)kv_w1[o][i] * a0[i]; float q = floorf((float)acc * kv_m1 + 0.5f); a1[o] = q < 0 ? 0 : (q > 127 ? 127 : (int32_t)q); }
    for (int o = 0; o < KV_H2; o++) { int32_t acc = kv_b2[o]; for (int i = 0; i < KV_H1; i++) acc += (int32_t)kv_w2[o][i] * a1[i]; float q = floorf((float)acc * kv_m2 + 0.5f); a2[o] = q < 0 ? 0 : (q > 127 ? 127 : (int32_t)q); }
    for (int o = 0; o < 4; o++) { int32_t acc = kv_b3[o]; for (int i = 0; i < KV_H2; i++) acc += (int32_t)kv_w3[o][i] * a2[i]; lg[o] = acc; }
    int best = 0; for (int o = 1; o < 4; o++) if (lg[o] > lg[best]) best = o;
    if (logits) memcpy(logits, lg, sizeof lg);
    return best;
}
int kv_classify(const float *x, float fr, int32_t *logits) { float f[KV_NF]; kv_features(x, fr, f); return kv_classify_features(f, logits); }
const char *kv_name(int c) { static const char *n[] = {"healthy", "outer-race fault", "inner-race fault", "unbalance/misalignment"}; return (c >= 0 && c < 4) ? n[c] : "?"; }
