/* Prayog STEM kit core: sensor conversions, photogate timing, ultrasonic distance, statistics, command parser.
 * C99, no heap, float only (runs on ATmega328 and on the host for tests). Calibration constants are typical values:
 * the experiments include a calibration step because real modules differ. */
#ifndef PRAYOG_CORE_H
#define PRAYOG_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef enum { S_NONE = 0, S_NTC, S_LDR, S_MIC, S_HALL, S_SOIL, S_VOLT, S_IR, S_COND, S_COUNT } sensor_t;
#define ADC_MAX 1023.0f

float conv_ntc_c(uint16_t adc);                 /* 10k NTC (beta 3950) on top, 10k fixed to GND: degrees C */
float conv_ldr_lux(uint16_t adc);               /* GL5528-style LDR on top, 10k to GND: approximate lux (log-log law) */
float conv_hall_mt(uint16_t adc);               /* linear Hall sensor 49E-type at 5 V: millitesla, zero at 2.5 V */
float conv_volt(uint16_t adc, float divider);   /* volts at the probe for a divider ratio (probe / adc pin) */
float conv_soil_pct(uint16_t adc, uint16_t dry, uint16_t wet);   /* 0..100 % */
float conv_mic_level(const uint16_t *samples, uint16_t n);       /* mean absolute deviation of n samples (counts) */
float conv_generic(sensor_t s, uint16_t adc);   /* dispatch with default parameters; S_COND/S_IR return raw counts (relative units) */
const char *sensor_name(sensor_t s);
const char *sensor_unit(sensor_t s);

float echo_to_cm(uint32_t echo_us, float temp_c);          /* ultrasonic: round-trip time -> distance */
float speed_of_sound_ms(float temp_c);

#define GATE_MAX 16
typedef struct { uint32_t t[GATE_MAX]; uint8_t level[GATE_MAX]; uint8_t n; } gate_t;
void gate_init(gate_t *g);
void gate_push(gate_t *g, uint32_t t_us, uint8_t level);           /* level 1 = beam interrupted */
bool gate_period_s(const gate_t *g, float *period);                /* mean time between successive interruptions (pendulum) */
bool gate_transit_s(const gate_t *g, float *dt);                   /* time the beam stayed interrupted (object passing) */
float speed_from_transit(float width_m, float dt_s);

typedef struct { float mean, sd; uint16_t n; } stats_t;
stats_t stats_of(const float *x, uint16_t n);
float median5(const float *x);                                     /* median of 5 values: spike rejection */

int parse_set(const char *line, uint8_t *channel, sensor_t *s);    /* "SET 0 NTC" -> 0 on success */
#ifdef __cplusplus
}
#endif
#endif
