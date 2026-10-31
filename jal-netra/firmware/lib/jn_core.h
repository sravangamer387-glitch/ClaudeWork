/* Jal-Netra measurement and leak-detection core (C99, float, no heap). Host-testable; the STM32G4 firmware wraps it with DMA capture. */
#ifndef JN_CORE_H
#define JN_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define JN_MAXN 128                                         /* max samples per capture window */
typedef struct { float f0, fs; uint16_t n; float win[JN_MAXN]; float c_re[JN_MAXN], c_im[JN_MAXN]; } jn_demod_t;
void jn_demod_init(jn_demod_t *d, float f0_hz, float fs_hz, uint16_t n);       /* Hann window + reference tables */
void jn_demod(const jn_demod_t *d, const int16_t *x, float *phase, float *amp);  /* x = ADC codes minus mid-scale */
float jn_tof_coarse(const int16_t *x, uint16_t n, float fs_hz, float thresh_frac); /* envelope threshold crossing with interpolation (seconds from window start) */

/* accumulator: averages many up/down shot pairs (circular mean of phase difference) */
typedef struct { float sx, sy, amp_up, amp_dn, tof_up, tof_dn; uint32_t n; } jn_acc_t;
void jn_acc_reset(jn_acc_t *a);
void jn_acc_add(jn_acc_t *a, float phase_up, float phase_dn, float amp_up, float amp_dn, float tof_up, float tof_dn);
bool jn_acc_result(const jn_acc_t *a, float f0_hz, float *dt_s, float *tof_s, float *amp, float *quality);   /* quality: resultant length 0..1 (1 = no phase scatter) */

/* physics */
float jn_c_water(float t_c);                                 /* Marczak polynomial */
float jn_temp_from_c(float c);                               /* Newton inversion, deg C */
float jn_nu_water(float t_c);
float jn_kprofile(float re);                                 /* area mean / line mean velocity (assumed model, to be calibrated) */
typedef struct { float length_m, bore_m; float zero_dt_s; float zero_slope_s_per_c; float zero_t_ref_c; float k_cal; } jn_cfg_t;
void jn_cfg_default(jn_cfg_t *c);
float jn_flow_lpm(const jn_cfg_t *c, float dt_s, float tof_s, float *temp_c);     /* signed litres per minute, temperature from the time of flight */

/* zero tracker: learns the electronic offset only when the pipe is quiet, with a temperature slope */
typedef struct { float dt_s, t_c, ema; uint32_t quiet_s, n; } jn_zero_t;
void jn_zero_init(jn_zero_t *z);
void jn_zero_update(jn_zero_t *z, jn_cfg_t *c, float dt_raw_s, float temp_c, bool quiet);

/* leak / usage state machine, one call per second with the flow in L/min */
typedef enum { JN_IDLE = 0, JN_USE, JN_SUSPECT, JN_LEAK, JN_BURST } jn_state_t;
typedef struct { float q_noise_lpm, q_leak_min_lpm, q_burst_lpm; uint32_t leak_after_s, quiet_needed_s, burst_after_s, suspect_after_s;
                 jn_state_t st; uint32_t run_s, nonzero_s, since_quiet_s, burst_s; float volume_l, volume_event_l, q_lp; uint32_t events; } jn_leak_t;
void jn_leak_init(jn_leak_t *l);
jn_state_t jn_leak_step(jn_leak_t *l, float q_lpm);          /* call at 1 Hz */
#ifdef __cplusplus
}
#endif
#endif
