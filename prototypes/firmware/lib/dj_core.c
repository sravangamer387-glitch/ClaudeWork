#include "dj_core.h"

/* ================= beat / BPM ================= */
void beat_init(beat_t *b) {
    uint16_t i;
    for (i = 0; i < BEAT_HIST; i++) b->onset[i] = 0;
    b->head = 0; b->filled = 0; b->avg_x16 = 0; b->prev = 0; b->peak_x16 = 16; b->peak_e = 0;
    b->since_beat = 1000; b->frames_since_bpm = 0; b->bpm = 0; b->quiet_frames = 0;
}

/* Autocorrelation score for one lag over the last `n` onset values (oldest..newest wrap via head). */
static uint32_t ac_score(const beat_t *b, uint16_t lag, uint16_t n) {
    uint32_t sum = 0;
    uint16_t i;
    for (i = lag; i < n; i++) {
        uint16_t a = (uint16_t)((b->head + BEAT_HIST - 1u - i) % BEAT_HIST);
        uint16_t c = (uint16_t)((b->head + BEAT_HIST - 1u - i + lag) % BEAT_HIST);
        sum += (uint32_t)b->onset[a] * b->onset[c];
    }
    return sum;
}

static void estimate_bpm(beat_t *b) {
    uint16_t n = b->filled, lag, best_lag = 0;
    uint32_t best = 0, s_prev = 0, s_cur = 0, s_next = 0, score[BEAT_LAG_MAX + 2u];
    if (n < 300u || b->quiet_frames > 300u) return;   /* need 3 s of history; stay at 0 after 3 s of silence */
    for (lag = BEAT_LAG_MIN; lag <= BEAT_LAG_MAX; lag++) {
        uint32_t s = ac_score(b, lag, n) / (n - lag);   /* normalise for overlap length */
        score[lag] = s;
    }
    for (lag = BEAT_LAG_MIN; lag <= BEAT_LAG_MAX; lag++) {
        uint32_t s = score[lag];
        if (lag * 2u <= BEAT_LAG_MAX) s += score[lag * 2u] / 2u;     /* reward multiples of the period */
        if (s > best) { best = s; best_lag = lag; }
    }
    if (best == 0 || best_lag == 0) { b->bpm = 0; return; }
    /* parabolic interpolation on the raw score for sub-frame resolution (x10) */
    s_cur = score[best_lag];
    s_prev = best_lag > BEAT_LAG_MIN ? score[best_lag - 1u] : s_cur;
    s_next = best_lag < BEAT_LAG_MAX ? score[best_lag + 1u] : s_cur;
    {
        int32_t denom = (int32_t)(s_prev + s_next) - 2 * (int32_t)s_cur;
        int32_t shift10 = 0;                      /* tenths of a frame */
        if (denom != 0) shift10 = (int32_t)(5 * ((int32_t)s_prev - (int32_t)s_next)) * 2 / denom / 2;
        if (shift10 > 5) shift10 = 5;
        if (shift10 < -5) shift10 = -5;
        {
            uint32_t lag10 = (uint32_t)((int32_t)best_lag * 10 + shift10);
            uint32_t bpm = 60000UL / lag10;       /* 6000 / (lag10/10) */
            while (bpm < 70u) bpm *= 2u;          /* octave folding into 70..170 */
            while (bpm > 170u) bpm /= 2u;
            b->bpm = (uint16_t)bpm;
        }
    }
}

bool beat_push(beat_t *b, uint16_t e) {
    bool beat = false;
    uint16_t flux = e > b->prev ? (uint16_t)(e - b->prev) : 0u;
    uint16_t avg = (uint16_t)(b->avg_x16 >> 4);
    uint16_t scaled;
    /* slow peak tracker (x16): rises instantly, decays ~1%/frame */
    if ((uint32_t)flux * 16u > b->peak_x16) b->peak_x16 = (uint16_t)((uint32_t)flux * 16u);
    else b->peak_x16 = (uint16_t)(b->peak_x16 - (b->peak_x16 >> 7));
    if (b->peak_x16 < 16u) b->peak_x16 = 16u;
    scaled = (uint16_t)(((uint32_t)flux * 16u * 255u) / b->peak_x16);
    b->onset[b->head] = (uint8_t)(scaled > 255u ? 255u : scaled);
    b->head = (uint16_t)((b->head + 1u) % BEAT_HIST);
    if (b->filled < BEAT_HIST) b->filled++;

    if (e > b->peak_e) b->peak_e = e; else b->peak_e = (uint16_t)(b->peak_e - (b->peak_e >> 7) - (b->peak_e > 0 && (b->peak_e >> 7) == 0 ? 1u : 0u));
    if (b->since_beat < 60000u) b->since_beat++;
    if (e > BEAT_QUIET && e > (uint16_t)(avg + (avg >> 1)) && e > b->prev && (uint32_t)e * 2u >= b->peak_e &&
        b->since_beat >= BEAT_REFRACTORY) {
        beat = true;
        b->since_beat = 0;
    }
    b->avg_x16 = (uint16_t)(b->avg_x16 + e - (b->avg_x16 >> 4));   /* ~16-frame (160 ms) smoothing */
    /* slower reference: blend towards the longer average to track ~1 s */
    b->prev = e;

    if (e <= BEAT_QUIET) { if (b->quiet_frames < 60000u) b->quiet_frames++; }
    else b->quiet_frames = 0;
    if (b->quiet_frames > 300u) { b->bpm = 0; }
    if (++b->frames_since_bpm >= 100u) { b->frames_since_bpm = 0; estimate_bpm(b); }
    return beat;
}

uint16_t beat_bpm(const beat_t *b) { return b->bpm; }

/* ================= light engine ================= */
static const uint8_t PAL[6][3] = {{255, 40, 40}, {255, 150, 20}, {40, 255, 80}, {30, 140, 255}, {170, 50, 255}, {255, 60, 180}};

void light_init(light_t *l) {
    l->level = LIGHT_BASE; l->target = LIGHT_BASE; l->palette_idx = 0; l->since_pulse = 1000; l->silent = 0; l->playing = false;
    l->r = l->g = l->b = 0;
}

void light_frame(light_t *l, bool beat, bool silence) {
    if (silence) { if (l->silent < 60000u) l->silent++; } else l->silent = 0;
    l->playing = l->silent < LIGHT_IDLE_FRAMES;
    if (l->since_pulse < 60000u) l->since_pulse++;
    if (l->playing && beat && l->since_pulse >= LIGHT_MIN_PULSE_GAP) {
        l->since_pulse = 0;
        l->target = 255;
        l->palette_idx = (uint8_t)((l->palette_idx + 1u) % 6u);
    }
    if (l->level >= l->target) l->target = l->playing ? LIGHT_BASE : 30u;   /* idle glow is dimmer */
    if (l->level < l->target) {                                              /* slew up */
        uint16_t v = (uint16_t)(l->level + LIGHT_ATTACK);
        l->level = v > l->target ? l->target : (uint8_t)v;
    } else if (l->level > l->target) {                                       /* slew down */
        l->level = (uint8_t)(l->level - LIGHT_DECAY < l->target ? l->target : l->level - LIGHT_DECAY);
    }
    l->r = (uint8_t)(((uint16_t)PAL[l->palette_idx][0] * l->level) / 255u);
    l->g = (uint8_t)(((uint16_t)PAL[l->palette_idx][1] * l->level) / 255u);
    l->b = (uint8_t)(((uint16_t)PAL[l->palette_idx][2] * l->level) / 255u);
}

/* ================= MIDI controller helpers ================= */
bool pot_update(pot_t *p, uint16_t adc10, uint8_t *midi7) {
    uint16_t x4 = (uint16_t)(adc10 << 2);
    uint8_t v;
    if (!p->init) { p->filt_x4 = x4; p->init = true; p->sent = 255; }
    else p->filt_x4 = (uint16_t)(p->filt_x4 + ((int32_t)x4 - (int32_t)p->filt_x4) / 4);   /* light low-pass */
    v = (uint8_t)(p->filt_x4 >> 5);                                    /* 12-bit -> 7-bit */
    if (v > 127u) v = 127u;
    if (p->sent != 255u) {                                             /* hysteresis: ignore +-1 flicker */
        int16_t d = (int16_t)v - (int16_t)p->sent;
        if (d == 1 || d == -1) {
            uint16_t centre = (uint16_t)(((uint16_t)p->sent << 5) + 16u);
            int16_t off = (int16_t)p->filt_x4 - (int16_t)centre;
            if (off < 0) off = (int16_t)-off;
            if (off < 28) return false;
        }
        if (d == 0) return false;
    }
    p->sent = v;
    *midi7 = v;
    return true;
}

int8_t enc_update(enc_t *e, uint8_t a, uint8_t b) {
    /* quadrature table over (previous AB, current AB); four valid steps make one detent */
    static const int8_t T[16] = {0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0};
    uint8_t cur = (uint8_t)(((a & 1u) << 1) | (b & 1u));
    e->acc = (int8_t)(e->acc + T[((e->prev & 3u) << 2) | cur]);
    e->prev = cur;
    if (e->acc >= 4) { e->acc = 0; return 1; }
    if (e->acc <= -4) { e->acc = 0; return -1; }
    return 0;
}

size_t midi_cc(uint8_t ch, uint8_t cc, uint8_t val, uint8_t out[3]) {
    out[0] = (uint8_t)(0xB0u | (ch & 0x0Fu)); out[1] = cc & 0x7Fu; out[2] = val & 0x7Fu; return 3;
}
size_t midi_note(uint8_t ch, uint8_t note, bool on, uint8_t out[3]) {
    out[0] = (uint8_t)((on ? 0x90u : 0x80u) | (ch & 0x0Fu)); out[1] = note & 0x7Fu; out[2] = on ? 0x7Fu : 0x00u; return 3;
}
