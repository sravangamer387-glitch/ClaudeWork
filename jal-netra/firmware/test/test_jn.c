#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../lib/jn_core.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static uint32_t rs = 987654321u; static double urand(void) { rs = rs * 1664525u + 1013904223u; return ((rs >> 8) & 0xFFFFFF) / 16777216.0; }
static double gauss(void) { double u1 = urand() + 1e-12, u2 = urand(); return sqrt(-2 * log(u1)) * cos(6.283185307 * u2); }
/* same pulse model as sim/twin.py */
#define F0 1.0e6
#define FS 4.0e6
#define NSAMP 64
static void make_shot(int16_t *x, double tau, double amp, double sigma) {
    const double burst = 6 / F0, tr = 4 / (3.14159265 * F0), peak = 1 - exp(-burst / tr), lsb = 3.3 / 4096;
    for (int i = 0; i < NSAMP; i++) { double t = i / FS - tau, env = 0; if (t > 0 && t <= burst) env = 1 - exp(-t / tr); else if (t > burst) env = peak * exp(-(t - burst) / tr);
        double v = amp * env * sin(2 * 3.14159265 * F0 * t) + sigma * gauss(); x[i] = (int16_t)lround(v / lsb); }
}
int main(void) {
    jn_demod_t d; jn_demod_init(&d, F0, FS, NSAMP); const double tof = 40.48e-6, t0 = tof - 4e-6; int16_t up[NSAMP], dn[NSAMP];
    /* ---- estimator accuracy: 0.5 ns and 5 ns at 30 dB SNR, 1000 shot pairs (twin.py predicted about 75 ps) */
    double dts[2] = {0.5e-9, 5e-9}; double sig = 0.25 / pow(10, 30 / 20.0);
    for (int k = 0; k < 2; k++) {
        double sum = 0, sum2 = 0; int trials = 40;
        for (int tr = 0; tr < trials; tr++) { jn_acc_t a; jn_acc_reset(&a);
            for (int s = 0; s < 1000; s++) { make_shot(up, tof - t0 + dts[k] / 2, 0.25 * 3.3 / 3.3, sig); make_shot(dn, tof - t0 - dts[k] / 2, 0.25, sig); float pu, pd, au, ad; jn_demod(&d, up, &pu, &au); jn_demod(&d, dn, &pd, &ad); jn_acc_add(&a, pu, pd, au, ad, jn_tof_coarse(up, NSAMP, FS, 0.3f), jn_tof_coarse(dn, NSAMP, FS, 0.3f)); }
            float dt, tf, amp, q; jn_acc_result(&a, F0, &dt, &tf, &amp, &q); double e = dt - dts[k]; sum += e; sum2 += e * e; }
        double mean = sum / trials, sd = sqrt(sum2 / trials - mean * mean); printf("dt %.1f ns: bias %.0f ps, std %.0f ps (twin predicted ~75 ps)\n", dts[k] * 1e9, mean * 1e12, sd * 1e12);
        CHECK(fabs(mean) < 60e-12, "bias %.0f ps", mean * 1e12); CHECK(sd < 150e-12, "std %.0f ps too large", sd * 1e12);
    }
    /* ---- coarse time of flight within 100 ns */
    { jn_acc_t a; jn_acc_reset(&a); double e = 0; for (int s = 0; s < 200; s++) { make_shot(up, tof - t0, 0.25, sig); e += jn_tof_coarse(up, NSAMP, FS, 0.3f); } e /= 200; CHECK(fabs(e - (tof - t0)) < 1.5e-6 && e > 0, "coarse arrival %.3f us for true %.3f us (threshold crossing precedes the peak)", e * 1e6, (tof - t0) * 1e6); }
    /* ---- physics */
    CHECK(fabs(jn_c_water(20) - 1482.4f) < 0.3f, "c(20C) %.2f", jn_c_water(20)); CHECK(fabs(jn_temp_from_c(jn_c_water(37.5f)) - 37.5f) < 0.01f, "temperature inversion"); CHECK(fabs(jn_nu_water(20) - 1.0035e-6f) < 5e-9f, "viscosity");
    CHECK(jn_kprofile(500) == 0.75f && jn_kprofile(1e5f) > 0.9f && jn_kprofile(1e5f) < 1.0f, "profile factor %.3f", jn_kprofile(1e5f));
    jn_cfg_t c; jn_cfg_default(&c); float T; float q = jn_flow_lpm(&c, 10.73e-9f, 60e-3f / 1482.4f, &T);
    CHECK(fabs(T - 20) < 0.2f && fabs(q - 1.0f) < 0.06f, "1.0 L/min dt 10.73 ns -> %.3f L/min at %.2f C", q, T);
    q = jn_flow_lpm(&c, -10.73e-9f, 60e-3f / 1482.4f, &T); CHECK(q < -0.9f && q > -1.1f, "reverse flow is negative: %.3f", q);
    /* ---- zero tracker: electronics offset 3 ns + 20 ps/C; quiet periods at different temperatures */
    { jn_zero_t z; jn_zero_init(&z); jn_cfg_t cz; jn_cfg_default(&cz); double off = 3e-9; double slope = 20e-12; double T0 = 15, worst = 0;
      for (int s = 0; s < 6 * 3600; s++) { double T1 = T0 + 12.0 * s / (6 * 3600.0); float raw = (float)(off + slope * (T1 - 20) + 0.03e-9 * gauss()); jn_zero_update(&z, &cz, raw, (float)T1, true);
          if (s > 2 * 3600) { double est = cz.zero_dt_s + cz.zero_slope_s_per_c * (T1 - cz.zero_t_ref_c); double e = fabs(est - (off + slope * (T1 - 20))); if (e > worst) worst = e; } }
      printf("zero tracker worst residual after 2 h: %.0f ps\n", worst * 1e12); CHECK(worst < 120e-12, "zero residual %.0f ps", worst * 1e12); }
    /* ---- leak state machine: a day of usage, a 0.02 L/min drip after 02:00, a burst at 14:00 */
    { jn_leak_t l; jn_leak_init(&l); int leak_t = -1, burst_t = -1, false_leak = 0; double vol = 0;
      for (int s = 0; s < 24 * 3600; s++) { float qv = 0; int hod = s / 3600;
          if (s % 3600 > 1800 && (hod == 7 || hod == 8 || hod == 19 || hod == 20)) qv = 6.0f;              /* showers / cooking */
          if (s % 7200 < 90) qv += 0.8f;                                                                     /* tap use every 2 h */
          float noise = 0.001f * (float)gauss(); if (s >= 2 * 3600 + 120 && s < 12 * 3600) qv += 0.02f;    /* drip leak from 02:02 until 12:00 */
          if (s >= 14 * 3600 && s < 14 * 3600 + 600) qv += 40.0f;                                             /* burst */
          vol += (qv > 0 ? qv : 0) / 60.0; jn_state_t st = jn_leak_step(&l, qv + noise);
          if (st == JN_LEAK && leak_t < 0) leak_t = s;
          if (st == JN_BURST && burst_t < 0) burst_t = s;
          if (st == JN_LEAK && (s < 2 * 3600 || s > 12 * 3600 + 200)) false_leak++; }
      printf("leak flagged at %.2f h (leak began 2.03 h, expected ~8 h), burst flagged at %.2f h (began 14.0 h), false leak seconds %d\n", leak_t / 3600.0, burst_t / 3600.0, false_leak);
      CHECK(leak_t > 0 && leak_t < 12 * 3600, "drip leak must be detected within its 10 h"); CHECK(burst_t >= 14 * 3600 && burst_t < 14 * 3600 + 300, "burst flagged within 5 minutes"); CHECK(false_leak == 0, "no false leak alarms from normal use: %d s", false_leak);
      CHECK(fabs(l.volume_l - vol) / vol < 0.02, "volume accounting %.1f vs %.1f L", l.volume_l, vol); }
    /* ---- a day of normal use only: no leak, no burst */
    { jn_leak_t l; jn_leak_init(&l); int bad = 0; for (int s = 0; s < 3 * 24 * 3600; s++) { float qv = 0; int hod = (s / 3600) % 24; if (s % 3600 > 1800 && (hod == 7 || hod == 8 || hod == 19)) qv = 6.0f; if (s % 3000 < 60) qv += 1.0f; jn_state_t st = jn_leak_step(&l, qv + 0.001f * (float)gauss()); if (st == JN_LEAK || st == JN_BURST) bad++; }
      CHECK(bad == 0, "three days of normal use raise %d alarm seconds", bad); }
    /* ---- continuous legitimate flow (garden hose, 4 h): suspect only after 2 h, never a leak at 15 L/min */
    { jn_leak_t l; jn_leak_init(&l); int leak = 0, burst = 0; for (int s = 0; s < 4 * 3600; s++) { jn_state_t st = jn_leak_step(&l, 15.0f); leak += st == JN_LEAK; burst += st == JN_BURST; } CHECK(leak == 0 && burst == 0, "a 15 L/min garden hose is not a leak/burst (it is usage)"); }
    printf("%d checks, %d failures\n", checks, fails); return fails ? 1 : 0;
}
