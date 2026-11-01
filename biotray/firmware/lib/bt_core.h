#ifndef BT_CORE_H
#define BT_CORE_H
#include <stdint.h>
#include <stdbool.h>
/* BioTray control core: portable C, host-tested. Hardware glue lives in ../src. */
/* ---- grow-light photoperiod with sunrise/sunset ramps ---- */
typedef struct { int on_min, off_min, ramp_min; uint8_t max_pwm; } bt_light_cfg_t;      /* minutes since midnight; off may be < on (light over midnight) */
uint8_t bt_light_pwm(const bt_light_cfg_t *c, int minute_of_day);                          /* 0..max_pwm */
/* ---- irrigation pump with dry-run protection ---- */
typedef struct { int period_s, run_s, max_run_s, min_off_s; } bt_pump_cfg_t;
typedef struct { int since_start_s, run_left_s, off_for_s; bool on, fault_dry; } bt_pump_t;
void bt_pump_init(bt_pump_t *p);
bool bt_pump_step(bt_pump_t *p, const bt_pump_cfg_t *c, bool water_present, int dt_s);   /* call every second; returns pump on/off. Latches fault_dry when water is missing while it should run */
void bt_pump_clear_fault(bt_pump_t *p);
/* ---- fan with hysteresis ---- */
bool bt_fan(bool was_on, float temp_c, float t_on, float t_off);
/* ---- sensor conditioning ---- */
typedef struct { float v1, p1, v2, p2; } bt_cal2_t;                                          /* two-point linear calibration */
float bt_cal_apply(const bt_cal2_t *c, float volts);
float bt_ec_compensate(float ec_raw_ms, float temp_c);                                        /* to 25 C with 2 %/K */
typedef struct { float buf[9]; int n, idx; float ema; bool have; } bt_filter_t;               /* median of up to 9 then EMA */
void bt_filter_init(bt_filter_t *f);
float bt_filter_push(bt_filter_t *f, float x, float alpha);
/* ---- MQTT payload ---- */
typedef struct { float temp_c, ph, ec_ms, lux; bool water, pump_on, fan_on, fault_dry; uint8_t light_pwm; uint32_t uptime_s; } bt_state_t;
int bt_json(char *out, int cap, const char *tray_id, const bt_state_t *s);                    /* returns length or -1 if it does not fit */
#endif
