#ifndef GT_FEAT_H
#define GT_FEAT_H
#include <stdint.h>
/* Geotechnical node features: identical definition to gateway/anomaly.py features() (window 400 samples at 200 Hz). */
#define GT_N 400
#define GT_FS 200.0
typedef struct { float rms, low_frac, high_frac, kurtosis, crest, peak; } gt_feat_t;
void gt_features(const float *x, gt_feat_t *f);
/* 12-byte LoRa-sized summary frame: id, flags, 6 features quantised, CRC-8 */
#define GT_FRAME_LEN 12
int gt_pack(uint8_t node_id, uint8_t flags, const gt_feat_t *f, uint8_t out[GT_FRAME_LEN]);
int gt_unpack(const uint8_t in[GT_FRAME_LEN], uint8_t *node_id, uint8_t *flags, gt_feat_t *f);   /* 0 on CRC failure */
uint8_t gt_crc8(const uint8_t *p, int n);
#endif
