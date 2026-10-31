#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../lib/gas_core.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static uint32_t rng = 12345;
static double rnd(void) { rng = rng * 1664525u + 1013904223u; return ((rng >> 8) & 0xFFFF) / 65536.0 - 0.5; }
typedef uint16_t (*sig_t)(double t_s);
static gas_t g; static uint32_t now;
static gas_inputs_t in0(uint16_t adc) { gas_inputs_t i = {0}; i.adc = adc; return i; }
static void boot(uint16_t first, bool wd) { gas_cfg_t c; gas_default_cfg(&c); now = 100000; gas_init(&g, &c, now, wd); (void)first; }
static void run(double secs, sig_t f, double t0) { for (double s = 0; s < secs; s += 1) { now += 1000; gas_step(&g, now, in0(f(t0 + s))); } }
static uint16_t clean(double t) { (void)t; return (uint16_t)(185 + 6 * rnd()); }
static uint16_t hi(double t) { (void)t; return 500; }
static uint16_t zero(double t) { (void)t; return 0; }
static uint16_t spike5(double t) { return (t >= 0 && t < 5) ? 480 : clean(t); }
static uint16_t spike10(double t) { return (t >= 0 && t < 10) ? 480 : clean(t); }
static uint16_t fastleak(double t) { double d = t * 0.5; if (d > 300) d = 300; return (uint16_t)(185 + d + 5 * rnd()); }   /* +0.5 counts/s */
static uint16_t slowleak(double t) { double d = t / 3600.0 * 25.0; return (uint16_t)(185 + d + 4 * rnd()); }              /* +25 counts/hour */
static uint16_t drift2(double t) { return (uint16_t)(185 + t / 3600.0 * 2.0 + 4 * rnd()); }                               /* +2 counts/hour */
static uint16_t drift_fast(double t) { return (uint16_t)(185 + t / 3600.0 * 10.0 + 4 * rnd()); }                          /* +10 counts/hour */
static uint16_t diurnal(double t) { return (uint16_t)(185 + 25 * sin(t / 86400.0 * 6.2832) + 4 * rnd()); }              /* +-25 counts day/night */

int main(void) {
    /* 1. clean air for 24 h with day/night swing: never leaves NORMAL after warm-up */
    boot(185, false); int bad = 0, worst = 0;
    for (double s = 0; s < 86400; s++) { now += 1000; gas_step(&g, now, in0(diurnal(s))); if (s > 150 && g.st != G_NORMAL) bad++; }
    CHECK(bad == 0, "diurnal clean air: %d seconds not NORMAL", bad); (void)worst;
    /* 2. warm-up then normal */
    boot(185, false); run(60, clean, 0); CHECK(g.st == G_WARMUP, "still warming at 60 s"); run(100, clean, 60); CHECK(g.st == G_NORMAL, "normal after 160 s, st=%d", g.st);
    CHECK(g.buzzer == BZ_OFF && g.led == 1, "silent green in clean air");
    /* 3. fast leak: time to alarm */
    boot(185, false); run(200, clean, 0); uint32_t t_start = now; int first = -1;
    for (int s = 0; s < 1200; s++) { now += 1000; gas_step(&g, now, in0(fastleak(s))); if (g.st == G_ALARM && first < 0) first = s; }
    CHECK(first > 0, "fast leak never alarmed"); if (first > 0) printf("fast leak (+0.5 counts/s): alarm after %d s (%.0f%% of alarm_delta reached)\n", first, 100.0 * (0.5 * first) / 150);
    CHECK(first > 0 && first < 400, "alarm too late: %d", first); CHECK(g.buzzer == BZ_CONTINUOUS && g.led == 3, "alarm outputs"); (void)t_start;
    /* 4. slow leak 25 counts/h must still alarm (baseline may only follow 6/h) */
    boot(185, false); run(200, clean, 0); first = -1;
    for (int s = 0; s < 3600 * 14; s++) { now += 1000; gas_step(&g, now, in0(slowleak(s))); if (g.st == G_ALARM && first < 0) first = s; }
    CHECK(first > 0, "slow leak (25/h) never alarmed in 14 h"); if (first > 0) printf("slow leak (+25 counts/h): alarm after %.1f h\n", first / 3600.0);
    /* 5. 5 s alcohol-like spike ignored; 10 s spike alarms */
    boot(185, false); run(200, clean, 0); bad = 0; for (int s = 0; s < 120; s++) { now += 1000; gas_step(&g, now, in0(spike5(s))); if (g.st == G_ALARM) bad++; }
    CHECK(bad == 0, "5 s spike must not alarm");
    boot(185, false); run(200, clean, 0); bad = 0; for (int s = 0; s < 120; s++) { now += 1000; gas_step(&g, now, in0(spike10(s))); if (g.st == G_ALARM) bad++; }
    CHECK(bad > 0, "10 s spike should alarm");
    /* 6. alarm clears after gas gone, needs hold time */
    run(30, clean, 0); /* spike over */ CHECK(g.st == G_ALARM || g.st == G_NORMAL, "state sane"); run(120, clean, 0); CHECK(g.st == G_NORMAL, "alarm cleared after clean air, st=%d", g.st);
    /* 7. sensor open/short -> fault, recovers */
    boot(185, false); run(200, clean, 0); run(5, zero, 0); CHECK(g.st == G_NORMAL, "5 s zero tolerated"); run(10, zero, 0); CHECK(g.st == G_FAULT && g.led == 4 && g.buzzer == BZ_CHIRP, "open sensor -> FAULT st=%d", g.st);
    run(5, clean, 0); CHECK(g.st != G_ALARM, "no false alarm on recovery"); run(200, clean, 0); CHECK(g.st == G_NORMAL, "recovered from fault, st=%d", g.st);
    /* 8. gas present at power-up (warm-up guard): must still alarm, baseline NOT adopted */
    boot(500, false); run(100, hi, 0); CHECK(g.st == G_ALARM, "gas at power-up must alarm, st=%d", g.st);
    run(3600, hi, 0); CHECK(g.st == G_ALARM, "stays alarmed for an hour of gas, st=%d", g.st);
    /* 9. silence: quiet for 5 min then re-sounds; escalation re-sounds sooner */
    boot(185, false); run(200, clean, 0); run(60, hi, 0); CHECK(g.st == G_ALARM && g.buzzer == BZ_CONTINUOUS, "alarm before silence");
    gas_inputs_t b = in0(500); b.button_silence = true; now += 1000; gas_step(&g, now, b); CHECK(g.buzzer == BZ_OFF, "silenced");
    run(200, hi, 0); CHECK(g.buzzer == BZ_OFF, "still silent at ~200 s"); run(120, hi, 0); CHECK(g.buzzer == BZ_CONTINUOUS, "re-alarm after 5 min");
    boot(185, false); run(200, clean, 0); run(60, hi, 0); now += 1000; gas_step(&g, now, b); CHECK(g.buzzer == BZ_OFF, "silenced again");
    for (int s = 0; s < 60; s++) { now += 1000; gas_step(&g, now, in0(700)); } CHECK(g.buzzer == BZ_CONTINUOUS, "gas worsening re-sounds despite silence");
    /* 10. normal slow temperature/ageing drift is followed (36 h) ; faster drift than limit never stays silently NORMAL while above abs level */
    boot(185, false); bad = 0; for (double s = 0; s < 3600 * 36; s++) { now += 1000; gas_step(&g, now, in0(drift2(s))); if (s > 150 && g.st != G_NORMAL) bad++; }
    CHECK(bad == 0, "2 counts/h drift over 36 h (+72, inside the +80 limit): %d s not NORMAL", bad);
    for (double s = 3600 * 36; s < 3600 * 72; s++) { now += 1000; gas_step(&g, now, in0(drift2(s))); }
    CHECK(g.st == G_FAULT, "sensor aged beyond the +80 drift limit must report FAULT, not hide, st=%d", g.st);
    boot(185, false); int silent_high = 0; for (double s = 0; s < 3600 * 60; s++) { now += 1000; uint16_t a = drift_fast(s); gas_step(&g, now, in0(a)); if (s > 150 && a >= g.cfg.alarm_abs + 20 && g.st == G_NORMAL) silent_high++; }
    CHECK(silent_high == 0, "reading above absolute alarm level while NORMAL: %d s", silent_high);
    for (int s = 0; s < 60; s++) { now += 1000; gas_step(&g, now, in0(600)); }
    CHECK(g.st == G_ALARM, "aged sensor still alarms on real gas, st=%d", g.st);
    /* 11. self test button */
    boot(185, false); run(200, clean, 0); gas_inputs_t t = in0(185); t.button_test = true; now += 1000; gas_step(&g, now, t); CHECK(g.buzzer == BZ_CONTINUOUS, "self test beeps");
    run(5, clean, 0); CHECK(g.buzzer == BZ_OFF, "self test ends");
    /* 12. watchdog reset: short warm-up, gas present still alarms */
    boot(185, true); run(30, clean, 0); CHECK(g.st == G_NORMAL, "after watchdog reset normal within 30 s, st=%d", g.st);
    /* 13. low battery chirp */
    boot(185, false); run(200, clean, 0); gas_inputs_t l = in0(185); l.battery_low = true; now += 1000; gas_step(&g, now, l); CHECK(g.buzzer == BZ_CHIRP, "battery chirp");
    /* 14. fuzz: random inputs never crash, state in range */
    boot(185, false); for (int s = 0; s < 200000; s++) { now += 1000; gas_inputs_t r = in0((uint16_t)(rnd() * 3000 + 1500)); r.button_silence = (rng >> 3) % 50 == 0; r.button_test = (rng >> 5) % 80 == 0; gas_step(&g, now, r); if (g.st > G_FAULT) { CHECK(0, "bad state"); break; } }
    /* 15. millis wrap-around */
    boot(185, false); now = 0xFFFFFF00u; gas_init(&g, &g.cfg, now, false); run(300, clean, 0); CHECK(g.st == G_NORMAL, "normal across millis wrap, st=%d", g.st); run(60, hi, 0); CHECK(g.st == G_ALARM, "alarm across wrap");
    printf("%d checks, %d failures\n", checks, fails); return fails ? 1 : 0;
}
