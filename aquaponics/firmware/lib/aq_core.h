#ifndef AQ_CORE_H
#define AQ_CORE_H
#include <stdint.h>
#include <stdbool.h>
/* Aquaponics control + edge forecasting core (portable C, host-tested). Hardware glue is the BioTray board (see ../src). */
/* ---- dissolved oxygen saturation (mg/L, fresh water, sea level), Benson-Krause polynomial in temperature ---- */
float aq_do_sat_mgl(float temp_c);
/* ---- Holt linear-trend forecaster with residual-based uncertainty ---- */
typedef struct { float level, trend, var; float alpha, beta; int n; bool init; } aq_trend_t;
void aq_trend_init(aq_trend_t *t, float alpha, float beta);
void aq_trend_push(aq_trend_t *t, float x);                                   /* one sample per fixed interval */
float aq_trend_forecast(const aq_trend_t *t, int steps_ahead);
float aq_trend_sigma(const aq_trend_t *t, int steps_ahead);                    /* 1-sigma forecast error, grows with horizon */
/* steps until the forecast (minus k sigma, plus k sigma for the opposite bound) reaches the band edge; -1 = not within `max_steps` */
int aq_steps_to_breach(const aq_trend_t *t, float lo, float hi, float k_sigma, int max_steps);
/* ---- sensor sanity ---- */
typedef struct { float last; int same_count; } aq_stuck_t;
bool aq_sensor_ok(aq_stuck_t *s, float x, float lo, float hi, int stuck_limit);   /* false if outside the physical range or unchanged for stuck_limit samples */
/* ---- pH dosing (acid or base pump pulses) with dead-band, minimum interval, daily cap and lockout ---- */
typedef struct { float setpoint, deadband; int pulse_s, min_interval_s, max_daily_s; } aq_dose_cfg_t;
typedef struct { int since_last_s, dosed_today_s, day_s; bool lockout; } aq_dose_t;
void aq_dose_init(aq_dose_t *d);
int aq_dose_step(aq_dose_t *d, const aq_dose_cfg_t *c, float ph, bool ph_ok, bool direction_down, int dt_s);   /* returns pulse length in seconds (0 = no pulse) */
/* ---- aerator ---- */
bool aq_aerator(bool was_on, float do_mgl, float do_sat, float on_frac, float off_frac);    /* on below on_frac*sat, off above off_frac*sat */
#endif
