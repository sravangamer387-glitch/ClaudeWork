#ifndef MN_CORE_H
#define MN_CORE_H
#include <stdint.h>
#include <stdbool.h>
/* MITTI-NETRA node core (portable C, host-tested): soil moisture, tilt/strain structural alarms, report scheduling, compact binary frame with CRC. */
/* ---- soil moisture (capacitive probe, raw ADC counts fall as moisture rises) ---- */
typedef struct { int dry_raw, wet_raw; } mn_soil_cal_t;
float mn_soil_pct(const mn_soil_cal_t *c, int raw);                       /* 0..100 %, clamped */
/* ---- tilt from a 3-axis accelerometer at rest (g) ---- */
void mn_tilt_deg(float ax, float ay, float az, float *roll, float *pitch);
/* ---- strain from an HX711 reading ---- */
typedef struct { float vex, avdd, gain, gauge_factor, bridge_k; } mn_strain_cfg_t;       /* bridge_k: 4 for a quarter bridge, 2 half, 1 full */
float mn_hx711_volts(const mn_strain_cfg_t *c, int32_t raw24);
float mn_microstrain(const mn_strain_cfg_t *c, int32_t raw24, int32_t zero_raw);
/* ---- structural alarm with hysteresis and debounce ---- */
typedef enum { MN_OK = 0, MN_WATCH = 1, MN_ALARM = 2 } mn_level_t;
typedef struct { float watch, alarm, hyst; int debounce; } mn_thresh_t;
typedef struct { mn_level_t level; int up_count; } mn_alarm_t;
void mn_alarm_init(mn_alarm_t *a);
mn_level_t mn_alarm_update(mn_alarm_t *a, const mn_thresh_t *t, float magnitude);        /* magnitude = |tilt change| or |microstrain| */
/* ---- reporting interval ---- */
int mn_next_interval_s(mn_level_t worst, float battery_v, bool rain_recent);
/* ---- frame ---- */
typedef struct { uint16_t node_id; uint32_t unix_time; int16_t soil_pct_x10, temp_c_x10, roll_x100, pitch_x100; int32_t microstrain; uint16_t battery_mv; uint8_t level, flags; } mn_report_t;
#define MN_FRAME_LEN 26
int mn_pack(const mn_report_t *r, uint8_t out[MN_FRAME_LEN]);
bool mn_unpack(const uint8_t in[MN_FRAME_LEN], mn_report_t *r);                           /* false if magic, version or CRC is wrong */
uint16_t mn_crc16(const uint8_t *p, int n);                                                /* CRC-16/CCITT-FALSE */
#endif
