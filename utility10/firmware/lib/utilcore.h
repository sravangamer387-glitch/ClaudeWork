/* Eight small utility-tool engines (C99, no heap, host-testable). Time in ms or s as stated; wrap-safe. */
#ifndef UTILCORE_H
#define UTILCORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/* ---- Seeti Counter: counts pressure-cooker whistles from audio blocks ---- */
float ut_goertzel(const int16_t *x, int n, float f_hz, float fs_hz);          /* power at f_hz */
typedef struct { uint32_t t_start, t_end; bool in_whistle, tone_prev; uint16_t count, target; uint16_t min_ms, gap_ms; float ratio; bool done; } seeti_t;
void seeti_init(seeti_t *s, uint16_t target);
/* tone_power: Goertzel power at the whistle frequency, total_power: sum of squares of the block; call once per block */
void seeti_block(seeti_t *s, uint32_t now_ms, float tone_power, float total_power, int n);
/* ---- Gas Taraju: LPG cylinder weight -> remaining gas (NOT a leak detector) ---- */
typedef struct { int32_t zero_counts; float counts_per_kg; float tare_kg, net_kg; float w_kg; bool stable; float hist[8]; uint8_t nh, hi; float last_stable; float fast; uint32_t t_stable; float kg_per_day; } gas_scale_t;
void gs_init(gas_scale_t *g, int32_t zero, float counts_per_kg, float tare_kg, float net_kg);
void gs_calibrate(gas_scale_t *g, int32_t zero_counts, int32_t counts_with_known, float known_kg);
void gs_sample(gas_scale_t *g, uint32_t now_ms, int32_t counts);               /* ~10 Hz */
float gs_remaining_kg(const gas_scale_t *g);
int gs_percent(const gas_scale_t *g);
float gs_days_left(const gas_scale_t *g);
void gs_daily(gas_scale_t *g);                                                  /* call once per day with a stable reading to learn consumption */
/* ---- Fridge Door Guard ---- */
typedef enum { FD_CLOSED = 0, FD_OPEN, FD_WARN, FD_ALARM } fd_state_t;
typedef struct { fd_state_t st; uint32_t t_open, t_next; uint32_t open_total_s, opens; bool door_prev; uint32_t warn_ms, alarm_ms; uint8_t sound; } fd_t;   /* sound 0 off,1 chirp,2 continuous */
void fd_init(fd_t *f, uint32_t warn_ms, uint32_t alarm_ms);
void fd_step(fd_t *f, uint32_t now_ms, bool door_open);
/* ---- Bijli Meter Reader: counts meter LED pulses, estimates units and bill ---- */
#define BM_SLABS 4
typedef struct { uint16_t imp_per_kwh; uint32_t pulses, day_pulses; uint32_t t_last_pulse; bool light_prev; uint32_t last_gap_ms; float slab_upto[BM_SLABS]; float slab_rate[BM_SLABS]; float fixed_charge; } bm_t;
void bm_init(bm_t *m, uint16_t imp_per_kwh);
void bm_sample(bm_t *m, uint32_t now_ms, bool light_on);                       /* debounced rising-edge count; >= 20 ms apart */
float bm_kwh(const bm_t *m);
float bm_watts(const bm_t *m, uint32_t now_ms);                                 /* from the last pulse interval, 0 if idle > 10 min */
float bm_bill(const bm_t *m, float kwh);                                        /* slab estimate (rates are PLACEHOLDERS) */
/* ---- Bijli Log: power-cut logger ---- */
#define PC_LOG 32
typedef struct { uint32_t start_s[PC_LOG], dur_s[PC_LOG]; uint8_t n, head; bool out, raw_prev; uint32_t t_change_s; uint32_t total_out_s, count; } pc_t;
void pc_init(pc_t *p);
void pc_sample(pc_t *p, uint32_t now_s, bool mains_ok);                         /* 1 Hz; 2 s debounce */
/* ---- Chulha Timers: 4 independent countdowns ---- */
typedef struct { uint32_t end_ms[4]; bool active[4], ringing[4]; } ct_t;
void ct_init(ct_t *c);
void ct_set(ct_t *c, uint8_t ch, uint32_t now_ms, uint32_t seconds);
void ct_add(ct_t *c, uint8_t ch, uint32_t now_ms, int32_t delta_s);            /* + / - buttons */
void ct_ack(ct_t *c, uint8_t ch);
uint8_t ct_step(ct_t *c, uint32_t now_ms);                                      /* returns bitmask of ringing channels */
uint32_t ct_remaining_s(const ct_t *c, uint8_t ch, uint32_t now_ms);
/* ---- Rain Alert ---- */
typedef struct { uint16_t wet_thr, dry_thr; uint32_t t_wet, t_dry, mute_until; bool raining, alert; uint32_t wet_ms, dry_ms, mute_ms; bool muted; } rain_t;
void rain_init(rain_t *r);
void rain_step(rain_t *r, uint32_t now_ms, uint16_t adc, bool mute_button);     /* adc: higher = wetter */
/* ---- Tap Litre Meter ---- */
typedef struct { float pulses_per_litre; uint32_t pulses, session_pulses, day_pulses, last_pulse_ms; bool in_session; float last_session_l; float target_l; bool target_hit; } tap_t;
void tap_init(tap_t *t, float pulses_per_litre);
void tap_pulses(tap_t *t, uint32_t now_ms, uint32_t new_pulses);
void tap_step(tap_t *t, uint32_t now_ms);                                       /* ends a session after 5 s of no flow */
float tap_session_l(const tap_t *t);
float tap_day_l(const tap_t *t);
#ifdef __cplusplus
}
#endif
#endif
