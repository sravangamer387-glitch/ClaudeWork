#include <stdio.h>
#include <math.h>
#include <string.h>
#include "gt_feat.h"
#include "gt_vectors.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
int main(void) {
    const char *nm[6] = {"rms", "low_frac", "high_frac", "kurtosis", "crest", "peak"};
    for (int i = 0; i < GV_N; i++) {
        gt_feat_t f; gt_features(gv_win[i], &f); float c[6] = {f.rms, f.low_frac, f.high_frac, f.kurtosis, f.crest, f.peak};
        for (int j = 0; j < 6; j++) { double ref = gv_feat[i][j], d = fabs(c[j] - ref) / (fabs(ref) + 1e-4); CHECK(d < 2e-3, "%s %s: C %.6g python %.6g", gv_kind[i], nm[j], c[j], ref); }
        uint8_t fr[GT_FRAME_LEN], id, fl; gt_feat_t g; gt_pack(7, 3, &f, fr); CHECK(gt_unpack(fr, &id, &fl, &g) && id == 7 && fl == 3, "round trip %d", i);
        CHECK(fabs(g.low_frac - f.low_frac) < 0.01 && fabs(g.high_frac - f.high_frac) < 0.01 && fabs(log10f(g.rms) - log10f(f.rms)) < 0.02, "quantisation error %d", i);
        fr[5] ^= 0x10; CHECK(!gt_unpack(fr, &id, &fl, &g), "bit flip detected %d", i); }
    printf("%d checks, %d failures\n", checks, fails); return fails != 0; }
