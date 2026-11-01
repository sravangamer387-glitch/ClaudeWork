#ifndef KN_VIB_H
#define KN_VIB_H
#include <stdint.h>
/* KINETIC bearing/shaft condition classifier: order-tracked envelope features + int8 MLP. Window 1024 samples @ 3200 Hz, shaft speed 8..25 Hz.
   Synthetic-data model (see docs/vib_results.md); retrain with sim/vib.py on real recordings before relying on it. */
#define KV_N 1024
#define KV_FS 3200.0f
typedef enum { KV_HEALTHY = 0, KV_OUTER = 1, KV_INNER = 2, KV_UNBALANCE = 3 } kv_class_t;
void kv_features(const float *x, float shaft_hz, float *feat);                 /* x: KV_N samples in g. feat: KV_NF floats. */
int kv_classify_features(const float *feat, int32_t *logits);                  /* int8 MLP; returns class index */
int kv_classify(const float *x, float shaft_hz, int32_t *logits);              /* window -> class */
const char *kv_name(int cls);
#endif
