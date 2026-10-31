#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../lib/utilcore.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static uint32_t rs = 1234567; static double rn(void) { rs = rs * 1664525u + 1013904223u; return ((rs >> 8) & 0xFFFF) / 65536.0 - 0.5; }

/* synthetic kitchen audio at 8 kHz: noise + 100 Hz hum + optional tone */
static double g_fs = 8000; static int g_N = 256;
static int run_audio(double f_detect, double f_whistle, const double *starts, const double *lens, int nw, double total_s, double amp_tone, double amp_noise, uint16_t target, seeti_t *s) {
    const int N = g_N; const double fs = g_fs; int16_t blk[512]; seeti_init(s, target); long sample = 0;
    for (double t = 0; t < total_s; t += N / fs) {
        double t0 = t; int on = 0; for (int w = 0; w < nw; w++) if (t0 >= starts[w] && t0 < starts[w] + lens[w]) on = 1;
        for (int i = 0; i < N; i++, sample++) { double tt = sample / fs; double v = amp_noise * 2 * rn() + 150 * sin(2 * 3.14159265 * 100 * tt) + (on ? amp_tone * sin(2 * 3.14159265 * f_whistle * tt) : 0); blk[i] = (int16_t)v; }
        float tone = ut_goertzel(blk, N, (float)f_detect, (float)fs); double tot = 0; for (int i = 0; i < N; i++) tot += (double)blk[i] * blk[i];
        seeti_block(s, (uint32_t)(t * 1000), tone, (float)tot, N);
    }
    return s->count;
}
int main(void) {
    /* ---- Seeti Counter ---- */
    seeti_t s; const double st[3] = {5, 12, 20}, ln[3] = {1.5, 1.2, 1.8};
    CHECK(run_audio(2800, 2800, st, ln, 3, 30, 900, 400, 3, &s) == 3 && s.done, "3 whistles counted, got %d", s.count);
    CHECK(run_audio(2800, 2800, st, ln, 3, 8, 900, 400, 3, &s) == 1 && !s.done, "only first whistle by 8 s");
    const double cs[5] = {2, 4, 6, 8, 10}, cl[5] = {0.1, 0.1, 0.1, 0.1, 0.1};
    CHECK(run_audio(2800, 2800, cs, cl, 5, 14, 900, 400, 3, &s) == 0, "short clinks (100 ms) rejected, got %d", s.count);
    CHECK(run_audio(2800, 2800, st, ln, 0, 30, 0, 1500, 3, &s) == 0, "loud noise alone gives no count, got %d", s.count);
    CHECK(run_audio(2800, 2800, st, ln, 3, 30, 1500, 1500, 3, &s) == 3, "whistle 1.5k vs loud noise 1.5k counted, got %d", s.count);
    int masked = run_audio(2800, 2800, st, ln, 3, 30, 300, 1200, 3, &s); printf("LIMIT: whistle amplitude 300 against noise amplitude 1200 counts %d of 3 whistles\n", masked);
    int off = 0; for (double f = 1500; f <= 4500; f += 500) { run_audio(2800, f, st, ln, 3, 30, 900, 400, 9, &s); (void)off; }
    CHECK(run_audio(2800, 1000, st, ln, 3, 30, 900, 400, 3, &s) == 0, "a 1 kHz tone (not the whistle frequency) is ignored, got %d", s.count);
    /* production configuration of the rev B board: 16 kS/s, 128-sample blocks */
    g_fs = 16000; g_N = 128;
    CHECK(run_audio(2800, 2800, st, ln, 3, 30, 900, 400, 3, &s) == 3 && s.done, "16 kS/s/128: 3 whistles counted, got %d", s.count);
    CHECK(run_audio(2800, 2800, st, ln, 3, 30, 1500, 1500, 3, &s) == 3, "16 kS/s/128: whistle in loud noise, got %d", s.count);
    CHECK(run_audio(2800, 2800, st, ln, 0, 30, 0, 1500, 3, &s) == 0, "16 kS/s/128: noise only gives no count, got %d", s.count);
    CHECK(run_audio(2800, 3300, st, ln, 3, 30, 900, 400, 3, &s) == 0, "16 kS/s/128: a 3.3 kHz tone is ignored by the 2.8 kHz detector, got %d", s.count);
    CHECK(run_audio(3300, 3300, st, ln, 3, 30, 900, 400, 3, &s) == 3, "retuned to 3.3 kHz (what the scan mode stores) it counts, got %d", s.count);
    g_fs = 8000; g_N = 256;
    /* ---- Gas Taraju ---- */
    gas_scale_t g; gs_init(&g, 0, 1000, 0, 14.2f);
    gs_calibrate(&g, 8000, 8000 + 20000, 20.0f); CHECK(fabs(g.counts_per_kg - 1000) < 1e-3 && g.zero_counts == 8000, "calibration");
    gs_init(&g, 8000, 1000, 15.3f, 14.2f); uint32_t t = 0; int32_t cnt;
    /* cylinder is lifted onto the scale: ramp + wobble, then settles at 29.5 kg */
    for (int i = 0; i < 60; i++) { t += 100; double w = i < 20 ? 29.5 * i / 20.0 : 29.5 + (i < 40 ? 0.4 * sin(i) : 0.0); cnt = 8000 + (int32_t)(w * 1000 + 8 * rn()); gs_sample(&g, t, cnt); CHECK(i >= 40 || !g.stable, "unstable while placing"); }
    for (int i = 0; i < 80; i++) { t += 100; gs_sample(&g, t, 8000 + (int32_t)(29500 + 8 * rn())); }
    CHECK(g.stable && fabs(g.w_kg - 29.5) < 0.03, "stable weight %.3f", g.w_kg); CHECK(fabs(gs_remaining_kg(&g) - 14.2) < 0.05 && gs_percent(&g) >= 99, "full cylinder: %.2f kg %d%%", gs_remaining_kg(&g), gs_percent(&g));
    gs_daily(&g); for (int day = 1; day <= 5; day++) { for (int i = 0; i < 120; i++) { t += 100; gs_sample(&g, t, 8000 + (int32_t)((29500 - day * 400) + 8 * rn())); } gs_daily(&g); }
    CHECK(fabs(g.kg_per_day - 0.4) < 0.05, "learned consumption %.3f kg/day", g.kg_per_day); CHECK(fabs(gs_days_left(&g) - (gs_remaining_kg(&g) / 0.4)) < 3, "days left %.1f", gs_days_left(&g));
    for (int i = 0; i < 60; i++) { t += 100; gs_sample(&g, t, 8000 + (int32_t)(15300 + 8 * rn())); }          /* empty: tare only */
    CHECK(gs_percent(&g) == 0 && gs_remaining_kg(&g) < 0.1f, "empty cylinder shows 0 %%: %d", gs_percent(&g));
    for (int i = 0; i < 20; i++) { t += 100; gs_sample(&g, t, 8000 + 1000 * (i % 2 ? 20 : 15)); } CHECK(!g.stable, "hose bump / pressing the scale is not a stable reading");
    /* ---- Fridge Door Guard ---- */
    fd_t f; fd_init(&f, 60000, 180000); uint32_t now = 1000; fd_step(&f, now, false);
    now += 5000; fd_step(&f, now, true); now += 30000; fd_step(&f, now, true); CHECK(f.st == FD_OPEN && f.sound == 0, "quiet within 60 s");
    now += 31000; fd_step(&f, now, true); CHECK(f.st == FD_WARN && f.sound == 1, "chirp after 60 s"); now += 1000; fd_step(&f, now, true); CHECK(f.sound == 0, "chirps, not continuous");
    now += 120000; fd_step(&f, now, true); CHECK(f.st == FD_ALARM && f.sound == 2, "alarm after 3 min"); now += 5000; fd_step(&f, now, false); CHECK(f.st == FD_CLOSED && f.sound == 0 && f.opens == 1 && f.open_total_s >= 180, "closing silences and logs %u s", (unsigned)f.open_total_s);
    for (int i = 0; i < 10; i++) { now += 2000; fd_step(&f, now, true); now += 20000; fd_step(&f, now, false); } CHECK(f.opens == 11 && f.st == FD_CLOSED, "short opens never warn, 11 opens counted");
    fd_init(&f, 60000, 180000); now = 0xFFFFFF00u; fd_step(&f, now, true); now += 61000; fd_step(&f, now, true); CHECK(f.st == FD_WARN, "wrap-safe");
    /* ---- Bijli Meter Reader ---- */
    bm_t m; bm_init(&m, 1600); now = 0; int pulses = 0;
    for (int ms = 0; ms < 3600000; ms += 5) { now = ms; double period = 1000.0 * 3600.0 * 1000.0 / 1600.0 / 1000.0; /* 1000 W -> 2250 ms */ bool on = fmod(ms, period) < 100.0; bm_sample(&m, now, on); if (ms % 5 == 0 && on && !m.light_prev) {} }
    pulses = (int)m.pulses; CHECK(abs(pulses - 1600) <= 2, "1000 W for 1 h = 1600 pulses, got %d", pulses); CHECK(fabs(bm_kwh(&m) - 1.0) < 0.002, "1 kWh, got %.4f", bm_kwh(&m)); CHECK(fabs(bm_watts(&m, now) - 1000) < 40, "1000 W estimated: %.0f", bm_watts(&m, now));
    CHECK(bm_watts(&m, now + 700000) == 0, "idle > 10 min gives 0 W");
    CHECK(fabs(bm_bill(&m, 150) - (100 * 3.0 + 50 * 5.0)) < 1e-3 && fabs(bm_bill(&m, 450) - (100 * 3 + 100 * 5 + 200 * 7.5 + 50 * 9)) < 1e-3, "slab bill (placeholder rates)");
    bm_init(&m, 1600); bm_sample(&m, 1000, true); bm_sample(&m, 1005, false); bm_sample(&m, 1010, true); CHECK(m.pulses == 1, "bounce within 20 ms is one pulse"); 
    /* ---- Power-cut logger ---- */
    pc_t p; pc_init(&p); uint32_t ts = 0;
    for (; ts < 100; ts++) pc_sample(&p, ts, true);
    for (; ts < 100 + 3600; ts++) pc_sample(&p, ts, false);
    for (; ts < 5000; ts++) pc_sample(&p, ts, true);
    CHECK(p.count == 1 && p.n == 1 && p.dur_s[0] >= 3598 && p.dur_s[0] <= 3602, "one 1-hour cut logged: %u s", (unsigned)p.dur_s[0]);
    pc_init(&p); ts = 0; for (; ts < 50; ts++) pc_sample(&p, ts, true); pc_sample(&p, ts++, false); pc_sample(&p, ts++, true); for (int i = 0; i < 50; i++) pc_sample(&p, ts++, true); CHECK(p.count == 0, "1-second flicker ignored");
    pc_init(&p); ts = 0; for (int k = 0; k < 40; k++) { for (int i = 0; i < 10; i++) pc_sample(&p, ts++, true); for (int i = 0; i < 20; i++) pc_sample(&p, ts++, false); } for (int i = 0; i < 10; i++) pc_sample(&p, ts++, true);
    CHECK(p.count == 40 && p.n == PC_LOG, "ring keeps the last %d of 40 cuts, count=%u", PC_LOG, (unsigned)p.count); CHECK(p.total_out_s >= 40 * 18, "total outage %u s", (unsigned)p.total_out_s);
    /* ---- Chulha timers ---- */
    ct_t c; ct_init(&c); now = 0; ct_set(&c, 0, now, 600); ct_set(&c, 1, now, 90); ct_set(&c, 3, now, 5);
    CHECK(ct_step(&c, 4999) == 0 && ct_remaining_s(&c, 3, 4999) == 1, "timers run"); CHECK(ct_step(&c, 5000) == 8, "channel 3 rings alone"); CHECK(ct_step(&c, 90000) == (8 | 2), "channels 1 and 3 ring");
    ct_ack(&c, 3); CHECK(ct_step(&c, 91000) == 2, "ack stops one channel only"); CHECK(ct_remaining_s(&c, 0, 91000) == 509, "600 s timer has 509 s left at 91 s, got %u", (unsigned)ct_remaining_s(&c, 0, 91000));
    ct_add(&c, 0, 91000, 60); CHECK(ct_remaining_s(&c, 0, 91000) == 569, "+1 min"); ct_add(&c, 0, 91000, -10000); CHECK(ct_remaining_s(&c, 0, 91000) == 0, "cannot go negative"); ct_set(&c, 2, 0xFFFFFFF0u, 1); CHECK(ct_step(&c, 0xFFFFFFF0u + 1000) & 4, "wrap-safe timer");
    /* ---- Rain alert ---- */
    rain_t r; rain_init(&r); now = 0; for (int i = 0; i < 100; i++) { now += 1000; rain_step(&r, now, 100, false); } CHECK(!r.raining && !r.alert, "dry day");
    for (int i = 0; i < 2; i++) { now += 1000; rain_step(&r, now, 600, false); } CHECK(!r.alert, "2 s of a water drop does not alert"); now += 5000; rain_step(&r, now, 600, false); CHECK(r.alert && r.raining, "alert after 3 s wet");
    rain_step(&r, now + 100, 600, true); CHECK(!r.alert && r.muted, "mute works"); now += 1800000 + 1000; rain_step(&r, now, 600, false); CHECK(r.alert, "rings again if still raining after 30 min");
    for (int i = 0; i < 125; i++) { now += 1000; rain_step(&r, now, 100, false); } CHECK(!r.raining && !r.alert, "dry after 2 minutes dry");
    rain_init(&r); now = 0; for (int i = 0; i < 20; i++) { now += 1000; rain_step(&r, now, i % 2 ? 600 : 100, false); } CHECK(!r.alert, "flickering sensor does not alert");
    /* ---- Tap litre meter ---- */
    tap_t tp; tap_init(&tp, 450); tp.target_l = 10; now = 0; for (int i = 0; i < 50; i++) { now += 100; tap_pulses(&tp, now, 450 * 5 / 50 * 1); } tap_step(&tp, now); CHECK(tp.in_session && fabs(tap_session_l(&tp) - 5.0) < 0.01, "5 L so far %.2f", tap_session_l(&tp)); CHECK(!tp.target_hit, "target not yet");
    for (int i = 0; i < 50; i++) { now += 100; tap_pulses(&tp, now, 45); } CHECK(tp.target_hit, "10 L target hit"); now += 5000; tap_step(&tp, now); CHECK(!tp.in_session && fabs(tp.last_session_l - 10.0) < 0.02, "session ended, %.2f L", tp.last_session_l);
    now += 100; tap_pulses(&tp, now, 450); CHECK(tp.in_session && fabs(tap_session_l(&tp) - 1.0) < 1e-3 && fabs(tap_day_l(&tp) - 11.0) < 0.03, "new session, day total %.2f", tap_day_l(&tp));
    printf("%d checks, %d failures\n", checks, fails); return fails ? 1 : 0;
}
