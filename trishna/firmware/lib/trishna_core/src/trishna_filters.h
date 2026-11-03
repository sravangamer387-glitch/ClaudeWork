/* Digital filters for the TRISHNA sensor streams (no dynamic memory; fixed capacity TR_MA_MAX).
 *  - tr_ma_t      : moving average over the last N samples (N <= TR_MA_MAX), also gives the window standard deviation
 *  - tr_ema_t     : first-order IIR low-pass y += alpha * (x - y); alpha = 1 - exp(-dt / tau)
 *  - tr_median5   : median of 5, removes single-sample spikes (bubbles, electrode contact flicker) before averaging
 *  - tr_settle_t  : "has the reading stopped moving?" detector used to wait out kinetic sloshing after the pump stops:
 *                   settled when the moving window's relative standard deviation stays below tol for hold consecutive updates. */
#ifndef TRISHNA_FILTERS_H
#define TRISHNA_FILTERS_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

#define TR_MA_MAX 32

typedef struct { float buf[TR_MA_MAX]; uint8_t n, idx, count; float sum; } tr_ma_t;
void  tr_ma_init(tr_ma_t *m, uint8_t n);
float tr_ma_push(tr_ma_t *m, float x);      /* returns the current average */
float tr_ma_mean(const tr_ma_t *m);
float tr_ma_std(const tr_ma_t *m);
uint8_t tr_ma_full(const tr_ma_t *m);

typedef struct { float y, alpha; uint8_t primed; } tr_ema_t;
void  tr_ema_init(tr_ema_t *e, float alpha);
float tr_ema_alpha(float dt_s, float tau_s);
float tr_ema_push(tr_ema_t *e, float x);

float tr_median5(const float v[5]);
float tr_median_n(float *v, int n);         /* sorts v in place (n <= 64) */

typedef struct { tr_ma_t win; float tol; uint8_t hold, run; } tr_settle_t;
void    tr_settle_init(tr_settle_t *s, uint8_t window, float rel_tol, uint8_t hold);
uint8_t tr_settle_push(tr_settle_t *s, float x);   /* 1 when settled */

#ifdef __cplusplus
}
#endif
#endif
