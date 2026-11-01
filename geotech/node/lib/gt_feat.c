#include <math.h>
#include <string.h>
#include "gt_feat.h"
void gt_features(const float *xin, gt_feat_t *f) {
    static double x[GT_N], w[GT_N]; double mean = 0; for (int i = 0; i < GT_N; i++) mean += xin[i]; mean /= GT_N;
    double s2 = 0, s4 = 0, pk = 0; for (int i = 0; i < GT_N; i++) { x[i] = xin[i] - mean; s2 += x[i] * x[i]; s4 += x[i] * x[i] * x[i] * x[i]; if (fabs(x[i]) > pk) pk = fabs(x[i]); }
    double r = sqrt(s2 / GT_N) + 1e-12; f->rms = (float)r; f->kurtosis = (float)((s4 / GT_N) / (r * r * r * r)); f->crest = (float)(pk / r); f->peak = (float)pk;
    for (int i = 0; i < GT_N; i++) w[i] = x[i] * (0.5 - 0.5 * cos(2.0 * M_PI * i / (GT_N - 1)));            /* numpy.hanning */
    double tot = 1e-18, low = 0, high = 0;
    for (int k = 0; k <= GT_N / 2; k++) {                                                                    /* naive DFT power: 201 bins x 400 samples, fine for a once-per-window task */
        double re = 0, im = 0, ph = 2.0 * M_PI * k / GT_N; for (int i = 0; i < GT_N; i++) { re += w[i] * cos(ph * i); im -= w[i] * sin(ph * i); }
        double p = re * re + im * im, fr = k * GT_FS / GT_N;
        tot += p;
        if (fr >= 3 && fr < 20) low += p;
        if (fr >= 30) high += p; }
    f->low_frac = (float)(low / tot); f->high_frac = (float)(high / tot);
}
uint8_t gt_crc8(const uint8_t *p, int n) { uint8_t c = 0; for (int i = 0; i < n; i++) { c ^= p[i]; for (int b = 0; b < 8; b++) c = (c & 0x80) ? (uint8_t)((c << 1) ^ 0x07) : (uint8_t)(c << 1); } return c; }
static uint8_t q8(float v, float lo, float hi) { if (v < lo) v = lo; if (v > hi) v = hi; return (uint8_t)lroundf((v - lo) / (hi - lo) * 255.0f); }
static float d8(uint8_t q, float lo, float hi) { return lo + (hi - lo) * q / 255.0f; }
int gt_pack(uint8_t id, uint8_t flags, const gt_feat_t *f, uint8_t o[GT_FRAME_LEN]) {
    o[0] = id; o[1] = flags; o[2] = q8(log10f(f->rms + 1e-6f), -4.0f, 0.0f); o[3] = q8(f->low_frac, 0, 1); o[4] = q8(f->high_frac, 0, 1); o[5] = q8(f->kurtosis, 0, 60); o[6] = q8(f->crest, 0, 30); o[7] = q8(log10f(f->peak + 1e-6f), -4.0f, 1.0f); o[8] = o[9] = o[10] = 0;
    o[11] = gt_crc8(o, 11); return GT_FRAME_LEN; }
int gt_unpack(const uint8_t in[GT_FRAME_LEN], uint8_t *id, uint8_t *flags, gt_feat_t *f) {
    if (gt_crc8(in, 11) != in[11]) return 0;
    *id = in[0]; *flags = in[1]; f->rms = powf(10.0f, d8(in[2], -4.0f, 0.0f)); f->low_frac = d8(in[3], 0, 1); f->high_frac = d8(in[4], 0, 1); f->kurtosis = d8(in[5], 0, 60); f->crest = d8(in[6], 0, 30); f->peak = powf(10.0f, d8(in[7], -4.0f, 1.0f)); return 1; }
