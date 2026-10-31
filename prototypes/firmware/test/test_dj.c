/* Host tests for dj_core: synthetic-audio beat detection, light safety invariants, MIDI helpers. */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../lib/dj_core.h"

static int g_pass, g_fail;
#define CHECK(c) do { if (c) g_pass++; else { g_fail++; printf("  FAIL %s:%d  %s\n", __FILE__, __LINE__, #c); } } while (0)

static uint32_t lcg = 12345;
static double rnd01(void) { lcg = lcg * 1664525u + 1013904223u; return (lcg >> 8) / 16777216.0; }

/* 8 kHz synthetic track: kick (55 Hz decaying burst) on every beat, softer hi-hat noise bursts on off-beats,
 * constant room noise. Returns frame energies (mean |x| over 10 ms, scaled x1000) in `e`. */
#define FS 8000
static int make_track(uint16_t *e, int seconds, double bpm, double kick_amp, double noise_amp, int hats) {
    int frames = seconds * 100, f, i;
    double period = 60.0 / bpm;
    for (f = 0; f < frames; f++) {
        double acc = 0;
        for (i = 0; i < FS / 100; i++) {
            double t = (f * (FS / 100) + i) / (double)FS;
            double ph = fmod(t, period);                       /* time since last beat */
            double x = noise_amp * (rnd01() - 0.5) * 2.0;
            x += kick_amp * exp(-ph * 22.0) * sin(2 * M_PI * 55.0 * ph);
            if (hats) { double ph2 = fmod(t + period / 2, period); x += 0.35 * exp(-ph2 * 90.0) * (rnd01() - 0.5) * 2.0; }
            acc += fabs(x);
        }
        e[f] = (uint16_t)(acc / (FS / 100) * 1000.0);
    }
    return frames;
}

static void test_bpm(void) {
    puts("bpm detection");
    static const double bpms[] = {90, 100, 120, 128, 140, 150};
    uint16_t e[3000];
    for (unsigned k = 0; k < sizeof bpms / sizeof bpms[0]; k++) {
        beat_t b; int frames = make_track(e, 25, bpms[k], 1.0, 0.05, 1);
        beat_init(&b);
        for (int f = 0; f < frames; f++) beat_push(&b, e[f]);
        int est = (int)beat_bpm(&b);
        printf("  true %.0f -> estimated %d\n", bpms[k], est);
        CHECK(abs(est - (int)bpms[k]) <= 3);
    }
}

static void test_beats_and_silence(void) {
    puts("beat flags, silence, noise");
    uint16_t e[3000]; beat_t b; int hits = 0, beats_expected = 0, total_flags = 0;
    int frames = make_track(e, 20, 120, 1.0, 0.05, 1);
    beat_init(&b);
    double period_frames = 50.0;                              /* 120 BPM = 50 frames */
    for (int f = 0; f < frames; f++) {
        bool flag = beat_push(&b, e[f]);
        if (flag) total_flags++;
        if (f >= 800 && flag) {                               /* after the 8 s warm-up: flag must be near a true beat */
            double pos = fmod(f, period_frames); if (pos > period_frames / 2) pos -= period_frames;
            if (fabs(pos) <= 6) hits++;
        }
        if (f >= 800 && fmod(f, period_frames) == 0) beats_expected++;
    }
    printf("  %d flags total, %d of %d late beats flagged within +-60 ms\n", total_flags, hits, beats_expected);
    CHECK(hits >= (beats_expected * 85) / 100);
    CHECK(total_flags <= (frames / 50) * 12 / 10);             /* no more than ~1.2 flags per beat */
    /* silence: no flags, bpm drops to 0 */
    beat_init(&b); int flags = 0;
    for (int f = 0; f < 2000; f++) if (beat_push(&b, 2)) flags++;
    CHECK(flags == 0 && beat_bpm(&b) == 0);
    /* music then silence: bpm resets after 3 s */
    beat_init(&b); frames = make_track(e, 15, 128, 1.0, 0.05, 1);
    for (int f = 0; f < frames; f++) beat_push(&b, e[f]);
    CHECK(beat_bpm(&b) > 0);
    for (int f = 0; f < 400; f++) beat_push(&b, 1);
    CHECK(beat_bpm(&b) == 0);
    /* steady loud noise (no beats) must not flag continuously */
    beat_init(&b); flags = 0;
    for (int f = 0; f < 3000; f++) if (beat_push(&b, (uint16_t)(300 + rnd01() * 30))) flags++;
    printf("  steady noise: %d flags in 30 s\n", flags);
    CHECK(flags <= 20);
}

static void test_light_safety(void) {
    puts("light safety");
    light_t l; light_init(&l);
    /* worst case: a beat flag on EVERY frame (a detector gone mad) for 10 s */
    int pulses = 0, max_up = 0, max_down = 0, min_level = 255, last_level = l.level;
    int window_pulses[1100] = {0};
    for (int f = 0; f < 1000; f++) {
        uint8_t before = l.since_pulse > 255 ? 255 : (uint8_t)l.since_pulse; (void)before;
        uint16_t sp = l.since_pulse;
        light_frame(&l, true, false);
        if (l.since_pulse == 0 && sp != 0) { pulses++; window_pulses[f] = 1; }
        int d = (int)l.level - last_level;
        if (d > max_up) max_up = d;
        if (-d > max_down) max_down = -d;
        if (l.level < min_level) min_level = l.level;
        last_level = l.level;
    }
    int worst_window = 0;                                      /* pulses in any 1-second (100-frame) window */
    for (int s = 0; s + 100 <= 1000; s++) { int c = 0; for (int k = 0; k < 100; k++) c += window_pulses[s + k]; if (c > worst_window) worst_window = c; }
    printf("  %d pulses in 10 s, worst 1 s window %d, max step up %d down %d, min level %d\n", pulses, worst_window, max_up, max_down, min_level);
    CHECK(worst_window <= 3);
    CHECK(max_up <= (int)LIGHT_ATTACK && max_down <= (int)LIGHT_DECAY);
    CHECK(min_level >= (int)LIGHT_BASE);                       /* never blacks out while music plays */
    /* silence -> idle glow, no pulses */
    light_init(&l);
    for (int f = 0; f < 400; f++) light_frame(&l, false, true);
    CHECK(!l.playing && l.level <= 30);
    /* beats at 120 BPM give ~2 pulses/s with visible contrast */
    light_init(&l); int hi = 0;
    for (int f = 0; f < 1000; f++) { light_frame(&l, f % 50 == 0, false); if (l.level > 200) hi++; }
    CHECK(hi > 0);
}

static void test_midi(void) {
    puts("midi helpers");
    uint8_t m[3]; pot_t p = {0}; uint8_t v = 0;
    CHECK(midi_cc(0, 7, 100, m) == 3 && m[0] == 0xB0 && m[1] == 7 && m[2] == 100);
    CHECK(midi_note(1, 60, true, m) == 3 && m[0] == 0x91 && m[1] == 60 && m[2] == 127);
    CHECK(midi_note(1, 60, false, m) == 3 && m[0] == 0x81 && m[2] == 0);
    /* pot: first reading is always sent; jitter of +-3 counts around 512 must not spam */
    CHECK(pot_update(&p, 512, &v) && v == 64);
    int sent = 0;
    for (int i = 0; i < 500; i++) if (pot_update(&p, (uint16_t)(512 + (int)(rnd01() * 7) - 3), &v)) sent++;
    printf("  jitter: %d messages in 500 noisy readings\n", sent);
    CHECK(sent <= 5);
    /* a real sweep reaches both ends and is monotonic */
    pot_t q = {0}; uint8_t last = 0, first = 255, top = 0; int mono = 1;
    for (int a = 0; a <= 1023; a++) { if (pot_update(&q, (uint16_t)a, &v)) { if (first == 255) first = v; if (v < last) mono = 0; last = v; top = v; } }
    CHECK(first == 0 && top >= 126 && mono);
    /* encoder: a full detent clockwise then counter-clockwise */
    enc_t e = {0, 0}; int sum = 0;
    static const uint8_t cw[][2] = {{0,1},{1,1},{1,0},{0,0}};   /* A,B Gray sequence */
    for (int d = 0; d < 5; d++) for (int s = 0; s < 4; s++) sum += enc_update(&e, cw[s][0], cw[s][1]);
    printf("  encoder 5 detents one way: %d\n", sum);
    CHECK(abs(sum) == 5);
    int dir = sum; sum = 0;
    for (int d = 0; d < 5; d++) for (int k = 0; k < 4; k++) { int s = (2 - k + 4) % 4; sum += enc_update(&e, cw[s][0], cw[s][1]); }   /* states 2,1,0,3 = reverse */
    CHECK(sum == -dir);
    /* contact bounce (back and forth between two states) produces no detents */
    enc_t b = {0, 0}; int bounce = 0;
    for (int i = 0; i < 100; i++) bounce += enc_update(&b, 0, (uint8_t)(i & 1));
    CHECK(bounce == 0);
}

int main(void) {
    test_bpm(); test_beats_and_silence(); test_light_safety(); test_midi();
    printf("\n%d checks passed, %d failed\n", g_pass, g_fail);
    return g_fail ? 1 : 0;
}
