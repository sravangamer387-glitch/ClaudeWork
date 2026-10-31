/* Four tiny game engines for 10-toys pack (C99, no heap, host-testable). Time in ms (uint32, wrap-safe). */
#ifndef TOYCORE_H
#define TOYCORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
uint32_t tc_rand(uint32_t *s);                       /* xorshift32; never returns state 0 */

/* ---- Reflex Raja: 4 players, first to press after GO wins; early press = false start (lose a point, locked out) ---- */
typedef enum { RR_IDLE = 0, RR_WAIT, RR_GO, RR_RESULT } rr_state_t;
typedef struct { rr_state_t st; uint32_t seed, t_go, t_state; uint8_t locked; int8_t winner; int8_t score[4]; uint16_t react_ms; bool tie; } rr_t;
void rr_init(rr_t *r, uint32_t seed);
void rr_step(rr_t *r, uint32_t now, uint8_t buttons);   /* buttons: bit i = player i pressed. Press any button in IDLE/RESULT starts a round */
/* ---- Taal Memory: Simon-like, 4 pads, sequence grows by one per round ---- */
typedef struct { uint32_t seed0, s; uint8_t len, pos; bool showing; uint8_t show_i; uint32_t t; bool over; uint8_t best; } tm_t;
void tm_init(tm_t *m, uint32_t seed);
uint8_t tm_note(const tm_t *m, uint8_t i);              /* i-th note of the current sequence (0..3) */
/* returns: 0 nothing, 1 correct note, 2 round complete (sequence grows), 3 wrong (game over) */
int tm_press(tm_t *m, uint8_t pad);
/* ---- Aloo Bomb: hot potato, hidden random fuse; faster beeps near the end ---- */
typedef struct { uint32_t seed, t0, fuse_ms; bool running, exploded; } ab_t;
void ab_init(ab_t *a, uint32_t seed);
void ab_start(ab_t *a, uint32_t now, uint32_t min_ms, uint32_t max_ms);
uint16_t ab_beep_interval_ms(const ab_t *a, uint32_t now);   /* 0 after explosion */
void ab_step(ab_t *a, uint32_t now);
/* ---- Beat Runner: notes scroll along 16 LEDs toward a hit zone at LED 0; press in the window to score ---- */
#define BR_LEDS 16
typedef struct { uint16_t notes; uint32_t seed, t_move; uint16_t speed_ms; int32_t score; uint8_t combo, misses; bool over; uint32_t moves; } br_t;
void br_init(br_t *b, uint32_t seed);
void br_step(br_t *b, uint32_t now);                    /* scroll and spawn */
int br_press(br_t *b);                                  /* returns points: 3 perfect (LED0), 1 good (LED1), 0 miss */
#ifdef __cplusplus
}
#endif
#endif
