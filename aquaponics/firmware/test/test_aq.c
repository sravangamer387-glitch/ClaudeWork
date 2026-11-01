#include <stdio.h>
#include <math.h>
#include "aq_core.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
int main(void) {
    /* DO saturation reference values (mg/L): 0 C 14.6, 10 C 11.3, 20 C 9.09, 25 C 8.26, 30 C 7.56 */
    CHECK(fabsf(aq_do_sat_mgl(0) - 14.6f) < 0.1f && fabsf(aq_do_sat_mgl(10) - 11.3f) < 0.1f && fabsf(aq_do_sat_mgl(20) - 9.09f) < 0.1f && fabsf(aq_do_sat_mgl(25) - 8.26f) < 0.1f && fabsf(aq_do_sat_mgl(30) - 7.56f) < 0.1f, "DO saturation table: 0C %.2f 10C %.2f 20C %.2f 25C %.2f 30C %.2f", aq_do_sat_mgl(0), aq_do_sat_mgl(10), aq_do_sat_mgl(20), aq_do_sat_mgl(25), aq_do_sat_mgl(30));
    /* forecaster: pH falling 0.05 per hour from 7.2 with noise; samples every 10 min (6 per hour) */
    aq_trend_t t; aq_trend_init(&t, 0.3f, 0.1f); unsigned s = 1; int alert_step = -1, cross_step = -1;
    for (int i = 0; i < 400; i++) {
        s = s * 1664525u + 1013904223u; float noise = ((s >> 8) / 16777216.0f - 0.5f) * 0.02f; float ph = 7.2f - 0.05f * (i / 6.0f) + noise;
        aq_trend_push(&t, ph); if (cross_step < 0 && ph < 6.4f) cross_step = i;
        if (alert_step < 0 && aq_steps_to_breach(&t, 6.4f, 7.8f, 2.0f, 18) >= 0) alert_step = i; }
    CHECK(cross_step > 0 && alert_step > 0 && alert_step < cross_step, "alert before crossing: alert %d crossing %d", alert_step, cross_step);
    CHECK(cross_step - alert_step >= 6 && cross_step - alert_step <= 40, "lead time %d samples (%.1f h)", cross_step - alert_step, (cross_step - alert_step) / 6.0f);
    aq_trend_t flat; aq_trend_init(&flat, 0.3f, 0.1f); int false_alerts = 0; s = 7;
    for (int i = 0; i < 2000; i++) { s = s * 1664525u + 1013904223u; float ph = 7.0f + (((s >> 8) / 16777216.0f) - 0.5f) * 0.04f; aq_trend_push(&flat, ph); if (aq_steps_to_breach(&flat, 6.4f, 7.8f, 2.0f, 18) >= 0) false_alerts++; }
    CHECK(false_alerts == 0, "no false alerts on a stable noisy series (%d)", false_alerts);
    CHECK(fabsf(aq_trend_forecast(&t, 0) - aq_trend_forecast(&t, 0)) == 0 && aq_trend_sigma(&t, 12) > aq_trend_sigma(&t, 1), "sigma grows with horizon");
    /* sensor sanity */
    aq_stuck_t st = {0, 0}; int bad_at = -1; for (int i = 0; i < 30; i++) if (!aq_sensor_ok(&st, 7.01f, 0.0f, 14.0f, 20)) { bad_at = i; break; } CHECK(bad_at == 20, "stuck sensor flagged at sample %d", bad_at);
    aq_stuck_t st2 = {0, 0}; CHECK(!aq_sensor_ok(&st2, 15.0f, 0, 14, 20) && !aq_sensor_ok(&st2, -1.0f, 0, 14, 20) && aq_sensor_ok(&st2, 7.0f, 0, 14, 20), "range check");
    /* seven-day dosing simulation: nitrification pushes pH down 0.02/h; each 30 s base pulse adds +0.04 */
    aq_dose_cfg_t c = {7.0f, 0.15f, 30, 1800, 600}; aq_dose_t d; aq_dose_init(&d); float ph = 7.0f; float mn = 9, mx = 0; int total = 0, lock_days = 0;
    for (int sec = 0; sec < 7 * 86400; sec += 60) {
        ph -= 0.02f / 60.0f; int p = aq_dose_step(&d, &c, ph, true, false, 60); if (p) { ph += 0.04f * p / 30.0f; total += p; } if (ph < mn) mn = ph; if (ph > mx) mx = ph; if (d.lockout && (sec % 86400) == 0) lock_days++; }
    CHECK(mn > 6.7f && mx < 7.3f, "pH stayed within %.2f-%.2f over 7 days", mn, mx); CHECK(total <= 7 * 600, "dosed %d s total, within the daily cap", total);
    /* demand above the daily cap (0.05 pH/h): the cap must lock out and the pH must be allowed to fall so that the forecaster alarm, not the pump, handles it */
    aq_dose_init(&d); float ph2 = 7.0f; int lockout_seen = 0; for (int sec = 0; sec < 2 * 86400; sec += 60) { ph2 -= 0.05f / 60.0f; int p = aq_dose_step(&d, &c, ph2, true, false, 60); if (p) ph2 += 0.04f * p / 30.0f; if (d.lockout) lockout_seen = 1; }
    CHECK(lockout_seen, "lockout reached when demand exceeds the cap");
    /* overdose protection: a broken probe stuck low would demand dosing forever; the daily cap and lockout must stop it */
    aq_dose_init(&d); int stuck_total = 0; for (int sec = 0; sec < 86400 - 60; sec += 60) stuck_total += aq_dose_step(&d, &c, 5.0f, true, false, 60);
    CHECK(stuck_total <= c.max_daily_s && d.lockout, "daily cap %d s enforced (dosed %d s), lockout set", c.max_daily_s, stuck_total);
    aq_dose_init(&d); int bad = 0; for (int i = 0; i < 100; i++) bad += aq_dose_step(&d, &c, 5.0f, false, false, 60); CHECK(bad == 0, "no dosing on a bad sensor");
    /* aerator */
    float sat = aq_do_sat_mgl(25); CHECK(aq_aerator(false, 0.5f * sat, sat, 0.6f, 0.9f) && !aq_aerator(true, 0.95f * sat, sat, 0.6f, 0.9f) && aq_aerator(true, 0.75f * sat, sat, 0.6f, 0.9f) && !aq_aerator(false, 0.75f * sat, sat, 0.6f, 0.9f), "aerator hysteresis");
    printf("%d checks, %d failures\n", checks, fails); return fails != 0; }
