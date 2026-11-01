#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include "ad_core.h"
#include "vectors.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static int run_vec(const ad_vec_t *v, float *dist, float *conf) {
    ad_gesture_t g; ag_init(&g); int res = AG_NONE;
    for (int i = 0; i < v->n; i++) {
        ad_imu_t m = {v->g[i * 3], v->g[i * 3 + 1], v->g[i * 3 + 2], v->a[i * 3], v->a[i * 3 + 1], v->a[i * 3 + 2]};
        int r = ag_step(&g, &m, v->trig[i], dist, conf); if (r != AG_NONE) res = r;
    }
    ad_imu_t z = {0}; int r = ag_step(&g, &z, false, dist, conf); if (r != AG_NONE) res = r;       /* release (trace may end while still pressed) */
    return res;
}
int main(void) {
    int agree = 0, correct = 0, pos = 0, negfalse = 0, neg = 0;
    for (int i = 0; i < AD_NVEC; i++) {
        float d, c; int r = run_vec(&AD_VECS[i], &d, &c);
        if (r == AG_NONE) { CHECK(0, "vector %d produced no result", i); continue; }
        if (r == AD_VECS[i].expect_py) agree++;
        if (AD_VECS[i].truth >= 0) { pos++; if (r == AD_VECS[i].truth) correct++; } else { neg++; if (r >= 0) negfalse++; }
    }
    printf("C vs Python reference agreement: %d/%d; spells recognised %d/%d; non-spells wrongly cast %d/%d\n", agree, AD_NVEC, correct, pos, negfalse, neg);
    CHECK(agree >= AD_NVEC - 2, "C and Python verdicts differ on %d vectors", AD_NVEC - agree);
    CHECK(correct >= pos * 90 / 100, "recognition %d/%d below 90%%", correct, pos);
    CHECK(negfalse <= neg / 3, "too many false casts %d/%d", negfalse, neg);
    /* idle: no result and no crash on a long run of zero samples */
    { ad_gesture_t g; ag_init(&g); ad_imu_t z = {0}; int bad = 0; for (int i = 0; i < 2000; i++) if (ag_step(&g, &z, false, NULL, NULL) != AG_NONE) bad++; CHECK(bad == 0, "idle produced results"); }
    /* trigger held for more than the buffer: overflow is handled, release still returns a verdict */
    { ad_gesture_t g; ag_init(&g); ad_imu_t m = {0, 800, 0, 0, 0, 16384}; int r = AG_NONE; for (int i = 0; i < 400; i++) ag_step(&g, &m, true, NULL, NULL); ad_imu_t z = {0}; r = ag_step(&g, &z, false, NULL, NULL); CHECK(r == AG_FIZZLE || (r >= 0 && r < AD_NSPELL), "long hold verdict %d", r); }
    /* trigger tapped without motion: fizzle */
    { ad_gesture_t g; ag_init(&g); ad_imu_t z = {0, 0, 0, 0, 0, 16384}; for (int i = 0; i < 20; i++) ag_step(&g, &z, false, NULL, NULL); for (int i = 0; i < 10; i++) ag_step(&g, &z, true, NULL, NULL); int r = ag_step(&g, &z, false, NULL, NULL); CHECK(r == AG_FIZZLE, "still tap gave %d", r); }
    /* spell engine */
    ad_game_t s; ad_game_init(&s); CHECK(s.mana == 100, "start mana");
    ad_cast_t c = ad_cast(&s, 1000, AD_AGNI); CHECK(c.ok && s.mana == 75, "agni costs 25, mana %d", s.mana);
    c = ad_cast(&s, 1500, AD_AGNI); CHECK(!c.ok && !strcmp(c.reason, "cooldown"), "cooldown 1 s");
    c = ad_cast(&s, 2100, AD_VAJRA); CHECK(c.ok && c.combo && s.mana == 40, "Agni then Vajra within 4 s is a combo; mana %d", s.mana);
    c = ad_cast(&s, 8000, AD_VAJRA); CHECK(c.ok && !c.combo && s.mana == 5, "no combo after 4 s; mana %d", s.mana);
    c = ad_cast(&s, 9500, AD_RAKSHA); CHECK(!c.ok && !strcmp(c.reason, "no mana"), "not enough mana");
    int m0 = s.mana; ad_game_tick(&s, 10000); ad_game_tick(&s, 12000); CHECK(s.mana > m0, "regen"); for (uint32_t t = 12000; t < 200000; t += 100) ad_game_tick(&s, t); CHECK(s.mana == 100, "regen caps at 100 (%d)", s.mana);
    c = ad_cast(&s, 300000, -1); CHECK(!c.ok && s.mana == 95, "fizzle costs 5 mana");
    ad_game_t w; ad_game_init(&w); ad_cast(&w, 4000000000u, AD_JALA); ad_cast_t w2 = ad_cast(&w, 4000000500u, AD_JALA); CHECK(!w2.ok, "cooldown across ms counter"); ad_cast_t w3 = ad_cast(&w, 4294967000u + 1500u, AD_JALA); CHECK(w3.ok, "cooldown ends across 32-bit wrap");
    /* LEDs: never exceed the current budget, all spells, all times */
    ad_game_init(&s); int maxsum = 0, nonzero = 0;
    for (int sp = -1; sp < AD_NSPELL; sp++) for (int combo = 0; combo < 2; combo++) for (uint32_t t = 0; t < 3000; t += 7) { ad_rgb_t px[AD_LEDS]; ad_led_frame(&s, 1000 + t, 1000, sp, combo, false, px); int sum = 0; for (int i = 0; i < AD_LEDS; i++) sum += px[i].r + px[i].g + px[i].b; if (sum > maxsum) maxsum = sum; if (sum) nonzero++; }
    printf("max LED channel sum %d (budget %d), non-dark frames %d\n", maxsum, AD_LED_BUDGET, nonzero);
    CHECK(maxsum <= AD_LED_BUDGET, "LED budget exceeded: %d", maxsum); CHECK(nonzero > 100, "LED effects dark");
    { ad_rgb_t px[AD_LEDS]; for (int i = 0; i < AD_LEDS; i++) { px[i].r = px[i].g = px[i].b = 255; } ad_led_limit(px, AD_LED_BUDGET); int sum = 0; for (int i = 0; i < AD_LEDS; i++) sum += px[i].r + px[i].g + px[i].b; CHECK(sum <= AD_LED_BUDGET && sum > AD_LED_BUDGET - 20, "limiter scales full white to the budget (%d)", sum); }
    /* sound tables */
    for (int sp = -4; sp < AD_NSPELL; sp++) { const ad_note_t *q; int n = ad_sound(sp, false, &q); CHECK(n >= 2 && n <= 8, "sound %d length %d", sp, n); int ms = 0; for (int i = 0; i < n; i++) { ms += ad_note_ms(&q[i]); CHECK(ad_note_hz(&q[i]) == 0 || (ad_note_hz(&q[i]) >= 100 && ad_note_hz(&q[i]) <= 4200), "note range"); } CHECK(ms < 1500, "sound %d too long", sp); }
    /* power manager */
    ad_power_t p; ad_power_init(&p, 0); ad_imu_t rest = {0, 0, 0, 0, 0, 16384}, moving = {0, 2000, 0, 0, 0, 16384};
    CHECK(ad_power_step(&p, 30000, &rest, false), "awake at 30 s"); CHECK(!ad_power_step(&p, 46000, &rest, false), "asleep after 45 s of nothing");
    CHECK(ad_power_step(&p, 46100, &moving, false), "wakes on motion"); CHECK(ad_power_step(&p, 60000, &rest, true), "trigger keeps awake");
    CHECK(ad_battery_low(3200) && !ad_battery_low(3600), "battery threshold");
    CHECK(!strcmp(ad_name(AD_VAJRA), "Vajra") && !strcmp(ad_name(-1), "Fizzle"), "names"); CHECK(ad_cost(AD_PRAKASH) == 10, "cost");
    printf("%d checks, %d failures\n", checks, fails); return fails != 0;
}
