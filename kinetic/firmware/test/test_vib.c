#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "kn_vib.h"
#include "kn_vib_model.h"
#include "../test/vib_vectors.h"
int main(void) {
    int fails = 0, pred_ok = 0, lab_ok = 0; double worst = 0;
    for (int i = 0; i < VV_N; i++) {
        static float x[KV_N]; for (int k = 0; k < KV_N; k++) x[k] = (float)vv_win[i][k] * VV_LSB;
        float f[KV_NF]; kv_features(x, vv_fr[i], f);
        for (int j = 0; j < KV_NF; j++) { double ref = vv_feat[i][j], d = fabs(f[j] - ref) / (fabs(ref) + 1e-3); if (d > worst) worst = d; if (d > 2e-3) { fails++; printf("feature %d of vector %d: C %.6g python %.6g\n", j, i, f[j], ref); } }
        int c = kv_classify_features(f, 0); pred_ok += (c == vv_pred[i]); lab_ok += (c == vv_label[i]);
    }
    printf("max relative feature difference C vs python: %.2e\nclass agreement with python int8: %d/%d, accuracy vs truth on the vectors: %d/%d\n", worst, pred_ok, VV_N, lab_ok, VV_N);
    if (pred_ok < VV_N - 1) { fails++; printf("FAIL class agreement\n"); }
    printf("%s\n", fails ? "FAILED" : "vib: OK"); return fails != 0;
}
