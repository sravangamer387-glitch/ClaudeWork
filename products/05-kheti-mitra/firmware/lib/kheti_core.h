/* Kheti-Mitra: soil-moisture irrigation controller core (C99, no heap). Two capacitive soil sensors, optional rain sensor,
 * one valve output. Water when the soil is dry, stop when it is wet enough or after a time limit; hold after rain;
 * a daily water budget; a safe fallback timer if the sensors fail. Percentages are x10 (350 = 35.0 %). */
#ifndef KHETI_CORE_H
#define KHETI_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef enum { K_IDLE = 0, K_WATERING, K_RAIN_HOLD, K_FAULT_FALLBACK } kheti_state_t;
typedef struct {
    uint16_t dry_adc[2], wet_adc[2];       /* calibration counts: sensor in dry air / sensor in water */
    uint16_t start_x10, stop_x10;          /* 480 / 720: start below 48 %, stop above 72 % of the sensor's dry-to-wet range (loam: about 50 % and 90 % of plant-available water) */
    uint32_t min_interval_ms;              /* 3 h between waterings so water can soak in before the sensor is read again */
    uint32_t max_run_ms;                   /* 20 min per watering */
    uint32_t max_daily_ms;                 /* 60 min per 24 h of operation */
    uint32_t rain_hold_ms;                 /* 12 h after the rain sensor was last wet */
    uint32_t fallback_run_ms, fallback_interval_ms;   /* both sensors failed: 5 min every 12 h */
} kheti_cfg_t;
typedef struct { uint16_t adc[2]; bool rain_wet, manual_hold; } kheti_inputs_t;
typedef struct {
    kheti_cfg_t cfg; kheti_state_t st; bool valve;
    uint32_t t_start, t_last_stop, t_rain, t_day_start, day_on_ms, t_valve_on;
    bool had_rain; uint16_t last_pct_x10; uint8_t valid_mask; uint32_t waterings;
} kheti_t;

void kheti_default_cfg(kheti_cfg_t *c);
void kheti_init(kheti_t *k, const kheti_cfg_t *c, uint32_t now);
void kheti_step(kheti_t *k, uint32_t now, kheti_inputs_t in);        /* call about once per second */
bool kheti_valve(const kheti_t *k);
uint8_t kheti_status_code(const kheti_t *k);                          /* 1 idle, 2 watering, 3 rain/hold, 4 sensor fault (fallback), 5 daily limit */
int kheti_pct_x10(const kheti_cfg_t *c, uint8_t i, uint16_t adc);     /* -1 if the reading is outside the plausible range (sensor fault) */

#ifdef __cplusplus
}
#endif
#endif
