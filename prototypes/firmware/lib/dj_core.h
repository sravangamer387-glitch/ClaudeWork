/* DJ prototype cores (C99, no heap, no floating point): beat/BPM detector, beat-synced light engine,
 * MIDI controller helpers (pot filter, quadrature encoder, message builders).
 * Runs on an ATmega328 (Arduino Nano, 2 KB RAM) and in host tests. */
#ifndef DJ_CORE_H
#define DJ_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ---------------- beat / BPM detector ----------------
 * Feed one value per 10 ms frame: the mean absolute deviation of the microphone ADC samples (any consistent unit).
 * Beat flag: energy rises above 1.5x its ~160 ms moving average AND is at least half of the recent energy peak
 * (ignores soft hi-hats), with a 250 ms refractory period.
 * BPM: autocorrelation of a 6 s onset-strength history, refreshed once per second, octave-folded into 70..170 BPM. */
#define BEAT_HIST 600u            /* 6 s at 100 frames/s */
#define BEAT_LAG_MIN 30u          /* 200 BPM */
#define BEAT_LAG_MAX 150u         /* 40 BPM */
#define BEAT_REFRACTORY 25u       /* 250 ms */
#define BEAT_QUIET 6u             /* energy below this counts as silence */

typedef struct {
    uint8_t onset[BEAT_HIST];
    uint16_t head, filled;
    uint16_t avg_x16;             /* moving average of energy, x16 fixed point */
    uint16_t prev;
    uint16_t peak_x16;            /* slow peak tracker for onset scaling */
    uint16_t peak_e;              /* recent energy peak (decays ~1 %/frame): soft hits below half of it are ignored */
    uint16_t since_beat, frames_since_bpm, bpm;
    uint16_t quiet_frames;
} beat_t;

void beat_init(beat_t *b);
bool beat_push(beat_t *b, uint16_t frame_energy);   /* true on a beat frame */
uint16_t beat_bpm(const beat_t *b);                 /* 0 = unknown / silence */

/* ---------------- beat-synced light engine ----------------
 * Photosensitivity rules enforced here (and tested): at most 3 pulses per second, brightness slews at most
 * LIGHT_ATTACK per 10 ms frame up and LIGHT_DECAY down, never below LIGHT_BASE while music plays. */
#define LIGHT_ATTACK 64u
#define LIGHT_DECAY 10u
#define LIGHT_BASE 50u
#define LIGHT_MIN_PULSE_GAP 34u   /* frames (~340 ms) => <= 3 pulses/s */
#define LIGHT_IDLE_FRAMES 300u    /* 3 s without music -> idle glow */

typedef struct {
    uint8_t level, target, palette_idx, r, g, b;
    uint16_t since_pulse, silent;
    bool playing;
} light_t;

void light_init(light_t *l);
void light_frame(light_t *l, bool beat, bool silence);   /* call every 10 ms */

/* ---------------- MIDI controller helpers ---------------- */
typedef struct { uint16_t filt_x4; uint8_t sent; bool init; } pot_t;
bool pot_update(pot_t *p, uint16_t adc10, uint8_t *midi7);       /* true when the 7-bit value changed */

typedef struct { uint8_t prev; int8_t acc; } enc_t;
int8_t enc_update(enc_t *e, uint8_t a, uint8_t b);               /* -1, 0, +1 per detent */

size_t midi_cc(uint8_t ch, uint8_t cc, uint8_t val, uint8_t out[3]);
size_t midi_note(uint8_t ch, uint8_t note, bool on, uint8_t out[3]);

#ifdef __cplusplus
}
#endif
#endif
