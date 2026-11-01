/* ASTRADAND core (C99, no heap, host-testable): gesture recogniser, spell/mana engine, LED effect frames, sound tables, power manager.
 * Wand axes: x along the wand (tip), y left, z up. IMU: +-1000 dps gyro (32.8 LSB/dps), +-2 g accel (16384 LSB/g), sampled at 50 Hz.
 * Hold the trigger, draw a shape in the air, release: the shape is matched against six templates. */
#ifndef AD_CORE_H
#define AD_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define AD_FS 50
#define AD_MAXPTS 112                   /* 2.24 s of drawing; points are stored as int16 in 1/16 degree to fit the ATmega's 2 KB RAM */
#define AD_M 16
#define AD_NSPELL 6
#define AD_LEDS 6
typedef enum { AD_AGNI = 0, AD_VAJRA, AD_JALA, AD_RAKSHA, AD_PRAKASH, AD_VAYU } ad_spell_t;
typedef struct { int16_t gx, gy, gz, ax, ay, az; } ad_imu_t;
#define AG_NONE (-2)                    /* no result yet (still drawing / idle) */
#define AG_FIZZLE (-1)                  /* gesture ended but matched no spell */
typedef struct {
    float ring[12][2]; uint8_t ring_n, ring_i;      /* last 12 resting gyro samples (y, z), deg/s */
    float by, bz;                                     /* bias at the moment the trigger went down */
    bool pressed; uint8_t k;                          /* samples since the trigger went down */
    float hy[5], hz[5], ay_sum, az_sum;               /* first 5 samples are buffered until the roll angle is known */
    float c, s, x, y; uint8_t n; int16_t px[AD_MAXPTS], py[AD_MAXPTS]; bool overflow;
} ad_gesture_t;
void ag_init(ad_gesture_t *g);
/* call at 50 Hz; returns AG_NONE while idle/drawing, and on the trigger release the spell index or AG_FIZZLE. dist/conf may be NULL */
int ag_step(ad_gesture_t *g, const ad_imu_t *imu, bool trigger, float *dist, float *conf);
/* classify a finished path (degrees); exposed for tests */
int ag_classify(const float *px, const float *py, int n, float *dist, float *conf);
int ag_classify_q(const int16_t *px, const int16_t *py, int n, float *dist, float *conf);   /* same, points in 1/16 degree */
/* ---- spell engine ---- */
typedef struct { int mana; uint32_t last_ms, t_regen, cd_until[AD_NSPELL]; int last_spell; uint32_t last_cast_ms; uint32_t casts[AD_NSPELL]; } ad_game_t;
typedef struct { int spell; bool ok; bool combo; int mana_after; const char *reason; } ad_cast_t;
void ad_game_init(ad_game_t *s);
void ad_game_tick(ad_game_t *s, uint32_t now_ms);                         /* mana regeneration, +2 per second up to 100 */
ad_cast_t ad_cast(ad_game_t *s, uint32_t now_ms, int spell);              /* spell < 0 = fizzle: costs 5 mana, never casts */
int ad_cost(int spell);
const char *ad_name(int spell);
/* ---- LED frames (6 pixels, GRB order is the driver's business; here R,G,B) ---- */
typedef struct { uint8_t r, g, b; } ad_rgb_t;
#define AD_LED_BUDGET 1500                                              /* max sum of the 18 channel values (about 20 mA per 255 -> about 120 mA) */
void ad_led_frame(const ad_game_t *s, uint32_t now_ms, uint32_t cast_started_ms, int spell, bool combo, bool low_battery, ad_rgb_t out[AD_LEDS]);
void ad_led_limit(ad_rgb_t px[AD_LEDS], int budget);
/* ---- sound ---- */
typedef struct { uint16_t hz, ms; } ad_note_t;      /* the tables live in flash on the AVR: read with ad_note_hz()/ad_note_ms() */
uint16_t ad_note_hz(const ad_note_t *n);
uint16_t ad_note_ms(const ad_note_t *n);
int ad_sound(int spell, bool combo, const ad_note_t **seq);              /* returns number of notes; spell -1 = fizzle, -3 = low battery, -4 = power-on */
/* ---- power manager: sleeps after 45 s without motion or trigger ---- */
typedef struct { uint32_t last_active_ms; bool asleep; } ad_power_t;
void ad_power_init(ad_power_t *p, uint32_t now_ms);
bool ad_power_step(ad_power_t *p, uint32_t now_ms, const ad_imu_t *imu, bool trigger);   /* returns true while awake */
/* battery: 3 x AAA through a divider; mv = pack voltage in millivolts */
bool ad_battery_low(int mv);
#ifdef __cplusplus
}
#endif
#endif
