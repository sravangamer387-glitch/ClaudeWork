#include "ad_core.h"
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "ad_templates.h"
#define DT (1.0f / AD_FS)
#define GLSB 32.8f
#define ALSB 16384.0f
void ag_init(ad_gesture_t *g) { memset(g, 0, sizeof *g); g->c = 1; }
static void rot_pt(float x, float y, float a, float *ox, float *oy) { float c = cosf(a), s = sinf(a); *ox = x * c - y * s; *oy = x * s + y * c; }
static int classify_impl(const float *fx, const float *fy, const int16_t *ix, const int16_t *iy, int n, float *dist, float *conf) {
#define PX(i) (fx ? fx[i] : (float)ix[i] / 16.0f)
#define PY(i) (fy ? fy[i] : (float)iy[i] / 16.0f)
    if (dist) *dist = 9.0f;
    if (conf) *conf = 0.0f;
    if (n < 5) return AG_FIZZLE;
    float minx = PX(0), maxx = PX(0), miny = PY(0), maxy = PY(0), len = 0, cum[AD_MAXPTS];
    cum[0] = 0;
    for (int i = 1; i < n; i++) { float dx = PX(i) - PX(i - 1), dy = PY(i) - PY(i - 1); len += sqrtf(dx * dx + dy * dy); cum[i] = len; if (PX(i) < minx) minx = PX(i); if (PX(i) > maxx) maxx = PX(i); if (PY(i) < miny) miny = PY(i); if (PY(i) > maxy) maxy = PY(i); }
    float ext = fmaxf(maxx - minx, maxy - miny);
    if (len < 1e-6f || ext < AD_MIN_EXTENT) return AG_FIZZLE;                   /* tremor has length but no size */
    float qx[AD_M], qy[AD_M]; int j = 0;
    for (int m = 0; m < AD_M; m++) {                                              /* equal arc-length resampling */
        float target = len * (float)m / (AD_M - 1);
        while (j < n - 2 && cum[j + 1] < target) j++;
        float seg = cum[j + 1] - cum[j], u = seg > 1e-9f ? (target - cum[j]) / seg : 0.0f; if (u < 0) u = 0; if (u > 1) u = 1;
        qx[m] = PX(j) + (PX(j + 1) - PX(j)) * u; qy[m] = PY(j) + (PY(j + 1) - PY(j)) * u;
    }
    float cx = 0, cy = 0, x0 = qx[0], x1 = qx[0], y0 = qy[0], y1 = qy[0];
    for (int m = 0; m < AD_M; m++) { cx += qx[m]; cy += qy[m]; if (qx[m] < x0) x0 = qx[m]; if (qx[m] > x1) x1 = qx[m]; if (qy[m] < y0) y0 = qy[m]; if (qy[m] > y1) y1 = qy[m]; }
    cx /= AD_M; cy /= AD_M; float sc = fmaxf(x1 - x0, y1 - y0); if (sc < 1e-9f) return AG_FIZZLE;
    for (int m = 0; m < AD_M; m++) { qx[m] = (qx[m] - cx) / sc; qy[m] = (qy[m] - cy) / sc; }
    float best = 9, second = 9; int bi = -1;
    for (int t = 0; t < AD_NT; t++) {
        float dmin = 9;
        for (int r = -2; r <= 2; r++) {                                           /* +-20 degrees in 10 degree steps (same convention as the reference: Q @ [[c,s],[-s,c]]) */
            float a = (float)r * 10.0f * 3.14159265f / 180.0f, acc = 0;
            for (int m = 0; m < AD_M; m++) { float rx, ry; rot_pt(qx[m], qy[m], -a, &rx, &ry); float dx = rx - AD_RF(AD_TEMPL[t][m][0]), dy = ry - AD_RF(AD_TEMPL[t][m][1]); acc += sqrtf(dx * dx + dy * dy); }
            acc /= AD_M; if (acc < dmin) dmin = acc;
        }
        if (dmin < best) { second = best; best = dmin; bi = t; } else if (dmin < second) second = dmin;
    }
    float cf = second > 1e-9f ? (second - best) / second : 0.0f; if (dist) *dist = best; if (conf) *conf = cf;
    if (best > AD_D_MAX || cf < AD_MARGIN) return AG_FIZZLE;
    return bi;
}
int ag_classify(const float *px, const float *py, int n, float *dist, float *conf) { return classify_impl(px, py, 0, 0, n, dist, conf); }
int ag_classify_q(const int16_t *px, const int16_t *py, int n, float *dist, float *conf) { return classify_impl(0, 0, px, py, n, dist, conf); }
static void integrate(ad_gesture_t *g, float gy, float gz) {
    float wy = gy - g->by, wz = gz - g->bz, wyw = g->c * wy - g->s * wz, wzw = g->s * wy + g->c * wz;
    g->x += wzw * DT; g->y += wyw * DT;
    if (g->n < AD_MAXPTS) { g->px[g->n] = (int16_t)(g->x * 16.0f); g->py[g->n] = (int16_t)(g->y * 16.0f); g->n++; } else g->overflow = true;
}
int ag_step(ad_gesture_t *g, const ad_imu_t *imu, bool trigger, float *dist, float *conf) {
    float gy = imu->gy / GLSB, gz = imu->gz / GLSB;
    if (!trigger) {
        int res = AG_NONE;
        if (g->pressed) { res = ag_classify_q(g->px, g->py, g->n, dist, conf); g->pressed = false; g->n = 0; g->k = 0; g->overflow = false; }
        g->ring[g->ring_i][0] = gy; g->ring[g->ring_i][1] = gz; g->ring_i = (uint8_t)((g->ring_i + 1) % 12); if (g->ring_n < 12) g->ring_n++;
        return res;
    }
    if (!g->pressed) {
        g->pressed = true; g->k = 0; g->n = 0; g->x = g->y = 0; g->overflow = false; g->ay_sum = g->az_sum = 0;
        float sy = 0, sz = 0; for (int i = 0; i < g->ring_n; i++) { sy += g->ring[i][0]; sz += g->ring[i][1]; }
        g->by = g->ring_n >= 6 ? sy / g->ring_n : 0; g->bz = g->ring_n >= 6 ? sz / g->ring_n : 0; g->c = 1; g->s = 0;
    }
    if (g->k < 5) {                                                               /* buffer the first samples until the roll angle (from gravity) is known */
        g->hy[g->k] = gy; g->hz[g->k] = gz; g->ay_sum += imu->ay / ALSB; g->az_sum += imu->az / ALSB; g->k++;
        if (g->k == 5) { float phi = atan2f(g->ay_sum, g->az_sum); g->c = cosf(phi); g->s = sinf(phi); for (int i = 0; i < 5; i++) integrate(g, g->hy[i], g->hz[i]); }
    } else integrate(g, gy, gz);
    return AG_NONE;
}
/* ------------------------------ spell engine ------------------------------ */
static const int COST[AD_NSPELL] = {25, 35, 20, 30, 10, 15};
static const char *NAME[AD_NSPELL] = {"Agni", "Vajra", "Jala", "Raksha", "Prakash", "Vayu"};
int ad_cost(int s) { return s >= 0 && s < AD_NSPELL ? COST[s] : 5; }
const char *ad_name(int s) { return s >= 0 && s < AD_NSPELL ? NAME[s] : "Fizzle"; }
void ad_game_init(ad_game_t *s) { memset(s, 0, sizeof *s); s->mana = 100; s->last_spell = -1; }
void ad_game_tick(ad_game_t *s, uint32_t now) { while ((int32_t)(now - s->t_regen) >= 500) { s->t_regen += 500; if (s->mana < 100) s->mana++; } s->last_ms = now; }
ad_cast_t ad_cast(ad_game_t *s, uint32_t now, int spell) {
    ad_cast_t r = {spell, false, false, s->mana, ""};
    if (spell < 0 || spell >= AD_NSPELL) { s->mana -= 5; if (s->mana < 0) s->mana = 0; r.mana_after = s->mana; r.reason = "fizzle"; return r; }
    if ((int32_t)(s->cd_until[spell] - now) > 0) { r.reason = "cooldown"; return r; }
    if (s->mana < COST[spell]) { r.reason = "no mana"; return r; }
    s->mana -= COST[spell]; s->cd_until[spell] = now + 1000; s->casts[spell]++;
    r.ok = true; r.reason = "ok";
    if (s->last_spell == AD_AGNI && spell == AD_VAJRA && (uint32_t)(now - s->last_cast_ms) <= 4000) r.combo = true;      /* Agni then Vajra within 4 s = Mahastra */
    s->last_spell = spell; s->last_cast_ms = now; r.mana_after = s->mana; return r;
}
/* ------------------------------ LEDs ------------------------------ */
static const ad_rgb_t COL[AD_NSPELL] = {{255, 70, 0}, {200, 200, 255}, {0, 90, 255}, {0, 220, 160}, {255, 220, 120}, {80, 255, 80}};
static uint8_t tri(uint32_t t, uint32_t period) { uint32_t p = t % period, h = period / 2; return (uint8_t)((p < h ? p : period - p) * 255 / h); }
static uint32_t lcg(uint32_t x) { return x * 1664525u + 1013904223u; }
void ad_led_limit(ad_rgb_t px[AD_LEDS], int budget) {
    int sum = 0; for (int i = 0; i < AD_LEDS; i++) sum += px[i].r + px[i].g + px[i].b;
    if (sum <= budget || sum == 0) return;
    for (int i = 0; i < AD_LEDS; i++) { px[i].r = (uint8_t)(px[i].r * budget / sum); px[i].g = (uint8_t)(px[i].g * budget / sum); px[i].b = (uint8_t)(px[i].b * budget / sum); }
}
void ad_led_frame(const ad_game_t *s, uint32_t now, uint32_t started, int spell, bool combo, bool low, ad_rgb_t out[AD_LEDS]) {
    memset(out, 0, sizeof(ad_rgb_t) * AD_LEDS);
    uint32_t age = now - started; bool casting = spell >= 0 && spell < AD_NSPELL && age < 1400;
    if (casting) {
        ad_rgb_t c = COL[spell]; if (combo) { c.r = 255; c.g = 0; c.b = 160; }
        for (int i = 0; i < AD_LEDS; i++) {
            uint32_t seed = lcg(now / 40 * 7 + i * 131); uint8_t v;
            switch (spell) {
            case AD_AGNI: v = (uint8_t)(120 + (seed >> 24) % 135); break;                                            /* flicker */
            case AD_VAJRA: v = ((now / 70 + i) % 7 == 0) ? 255 : 20; break;                                           /* flashes */
            case AD_JALA: v = tri(age * 2 + (uint32_t)i * 120, 700); break;                                           /* travelling wave */
            case AD_RAKSHA: v = tri(age, 500); break;                                                                  /* pulse */
            case AD_PRAKASH: v = (uint8_t)(age < 200 ? age * 255 / 200 : 255 - (age - 200) * 160 / 1200); break;    /* flash then glow */
            default: v = tri(age + (uint32_t)(AD_LEDS - i) * 90, 600); break;                                          /* sweep */
            }
            uint32_t fade = age > 1000 ? (1400 - age) * 255 / 400 : 255;
            out[i].r = (uint8_t)(c.r * v / 255 * fade / 255); out[i].g = (uint8_t)(c.g * v / 255 * fade / 255); out[i].b = (uint8_t)(c.b * v / 255 * fade / 255);
        }
    } else {                                                                                                          /* idle: mana bar with a slow breath */
        int lit = (s->mana * AD_LEDS + 99) / 100; uint8_t br = (uint8_t)(14 + tri(now, 3000) * 14 / 255);
        for (int i = 0; i < AD_LEDS; i++) if (i < lit) { out[i].r = br / 4; out[i].g = br / 2; out[i].b = br; }
        if (low && ((now / 500) % 2 == 0)) { out[0].r = 120; out[0].g = 0; out[0].b = 0; }
    }
    ad_led_limit(out, AD_LED_BUDGET);
}
/* ------------------------------ sound ------------------------------ */
static const ad_note_t S_AGNI[] AD_ROM = {{220, 80}, {330, 80}, {440, 160}, {330, 80}, {550, 200}};
static const ad_note_t S_VAJRA[] AD_ROM = {{2000, 40}, {0, 30}, {3000, 40}, {0, 30}, {1500, 60}, {3500, 120}};
static const ad_note_t S_JALA[] AD_ROM = {{523, 120}, {659, 120}, {784, 120}, {659, 120}, {523, 200}};
static const ad_note_t S_RAKSHA[] AD_ROM = {{392, 200}, {523, 300}};
static const ad_note_t S_PRAKASH[] AD_ROM = {{1047, 100}, {1319, 100}, {1568, 250}};
static const ad_note_t S_VAYU[] AD_ROM = {{300, 80}, {400, 80}, {500, 80}, {600, 80}, {700, 120}};
static const ad_note_t S_COMBO[] AD_ROM = {{220, 80}, {330, 80}, {2000, 40}, {3000, 40}, {440, 120}, {880, 120}, {1760, 300}};
static const ad_note_t S_FIZZ[] AD_ROM = {{200, 150}, {150, 250}};
static const ad_note_t S_LOW[] AD_ROM = {{800, 100}, {0, 100}, {800, 100}};
static const ad_note_t S_ON[] AD_ROM = {{523, 100}, {784, 100}, {1047, 200}};
uint16_t ad_note_hz(const ad_note_t *n) { return AD_RW(n->hz); }
uint16_t ad_note_ms(const ad_note_t *n) { return AD_RW(n->ms); }
#define NN(a) (int)(sizeof(a) / sizeof(a[0]))
int ad_sound(int spell, bool combo, const ad_note_t **seq) {
    if (combo) { *seq = S_COMBO; return NN(S_COMBO); }
    switch (spell) {
    case AD_AGNI: *seq = S_AGNI; return NN(S_AGNI);
    case AD_VAJRA: *seq = S_VAJRA; return NN(S_VAJRA);
    case AD_JALA: *seq = S_JALA; return NN(S_JALA);
    case AD_RAKSHA: *seq = S_RAKSHA; return NN(S_RAKSHA);
    case AD_PRAKASH: *seq = S_PRAKASH; return NN(S_PRAKASH);
    case AD_VAYU: *seq = S_VAYU; return NN(S_VAYU);
    case -3: *seq = S_LOW; return NN(S_LOW);
    case -4: *seq = S_ON; return NN(S_ON);
    default: *seq = S_FIZZ; return NN(S_FIZZ);
    }
}
/* ------------------------------ power ------------------------------ */
void ad_power_init(ad_power_t *p, uint32_t now) { p->last_active_ms = now; p->asleep = false; }
bool ad_power_step(ad_power_t *p, uint32_t now, const ad_imu_t *imu, bool trigger) {
    int g = abs(imu->gx) + abs(imu->gy) + abs(imu->gz);
    if (trigger || g > 30 * 33 * 3 / 3) { p->last_active_ms = now; p->asleep = false; }                                /* about 30 deg/s on any axis */
    else if (now - p->last_active_ms > 45000UL) p->asleep = true;
    return !p->asleep;
}
bool ad_battery_low(int mv) { return mv < 3300; }
