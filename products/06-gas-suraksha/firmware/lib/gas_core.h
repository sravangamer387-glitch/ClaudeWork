/* Gas-Suraksha: LPG leak alarm engine (C99, no heap). Input: one ADC reading per second from a metal-oxide gas sensor
 * (higher counts = more gas). The engine tracks a clean-air baseline that can follow daily temperature/humidity drift but
 * can NOT absorb a developing leak, confirms alarms, supports a limited silence, and reports sensor faults.
 * *** NOT CERTIFIED. A prototype built from this must not be relied on for safety. *** */
#ifndef GAS_CORE_H
#define GAS_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef enum { G_WARMUP = 0, G_NORMAL, G_PREALARM, G_ALARM, G_FAULT } gas_state_t;
typedef enum { BZ_OFF = 0, BZ_CHIRP, BZ_SLOW, BZ_CONTINUOUS } gas_buzzer_t;

typedef struct {
    uint16_t clean_air_nominal;  /* factory-calibrated reading in clean air (burned-in sensor, 25 C, 50 % RH), e.g. 180 */
    uint16_t clean_air_max;      /* a power-up reading above this is NOT clean air: the baseline is not adopted (e.g. nominal + 60) */
    uint16_t alarm_delta;        /* counts above baseline = about 10 % LEL (set by calibration with test gas), e.g. 150 */
    uint16_t prealarm_delta;     /* about 5 % LEL, e.g. 75 */
    uint16_t alarm_abs;          /* absolute alarm level no baseline can hide (nominal + alarm_delta + max drift), e.g. 410 */
    uint32_t warmup_ms;          /* 120 s preheat settling */
    uint32_t alarm_confirm_ms;   /* 8 s above the alarm level before sounding: rejects short alcohol/aerosol spikes */
    uint32_t prealarm_confirm_ms;/* 30 s */
    uint32_t clear_hold_ms;      /* 60 s below 60 % of the alarm level before the alarm clears */
    uint32_t silence_ms;         /* 5 min */
    uint16_t fault_low, fault_high;     /* readings at or beyond these (open/short sensor) are a fault */
    uint32_t fault_confirm_ms;   /* 10 s */
    uint16_t base_up_per_h;      /* the baseline may rise at most this many counts per hour (6): a developing leak cannot be learned */
    uint16_t base_down_per_h;    /* and fall at most this fast (60) */
    uint16_t base_max_rise;      /* baseline may never exceed its first value by more than this (80): beyond it the sensor is aged -> fault */
} gas_cfg_t;

typedef struct { uint16_t adc; bool button_silence, button_test, on_battery, battery_low, watchdog_reset; } gas_inputs_t;

typedef struct {
    gas_cfg_t cfg; gas_state_t st; gas_buzzer_t buzzer; uint8_t led;     /* led: 0 off, 1 green (ok), 2 amber (pre-alarm/warm-up), 3 red (alarm), 4 flashing red (fault) */
    uint32_t t0, t_last, t_over, t_pre, t_clear, t_good, t_abs, silenced_until, t_test_end, warmup_ms_eff;
    int32_t base;                /* baseline in counts x 65536 */
    int32_t base_first;
    int16_t delta_at_silence; bool silenced, base_init, base_trackable, aged, relay_shutoff, test_ok;
} gas_t;

void gas_default_cfg(gas_cfg_t *c);
void gas_init(gas_t *g, const gas_cfg_t *c, uint32_t now, bool watchdog_reset);
void gas_step(gas_t *g, uint32_t now, gas_inputs_t in);                  /* about once per second */
int16_t gas_delta(const gas_t *g, uint16_t adc);

#ifdef __cplusplus
}
#endif
#endif
