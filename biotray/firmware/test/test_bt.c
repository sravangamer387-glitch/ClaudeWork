#include <stdio.h>
#include <string.h>
#include <math.h>
#include "bt_core.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
int main(void) {
    /* light: 06:00-22:00, 30 min ramps, 255 max */
    bt_light_cfg_t L = {6 * 60, 22 * 60, 30, 255};
    CHECK(bt_light_pwm(&L, 5 * 60 + 59) == 0, "dark before dawn"); CHECK(bt_light_pwm(&L, 22 * 60) == 0, "off at 22:00"); CHECK(bt_light_pwm(&L, 12 * 60) == 255, "full at noon");
    int prev = -1, mono = 1; for (int m = 6 * 60; m < 6 * 60 + 30; m++) { int v = bt_light_pwm(&L, m); if (v < prev) mono = 0; prev = v; } CHECK(mono && prev > 200 && bt_light_pwm(&L, 6 * 60) < 20, "sunrise ramp monotonic (%d)", prev);
    prev = 1000; mono = 1; for (int m = 21 * 60 + 30; m < 22 * 60; m++) { int v = bt_light_pwm(&L, m); if (v > prev) mono = 0; prev = v; } CHECK(mono && prev < 20, "sunset ramp monotonic down");
    bt_light_cfg_t N = {20 * 60, 4 * 60, 10, 200}; CHECK(bt_light_pwm(&N, 23 * 60) == 200 && bt_light_pwm(&N, 2 * 60) == 200 && bt_light_pwm(&N, 12 * 60) == 0, "light over midnight");
    bt_light_cfg_t Z = {600, 600, 10, 255}; CHECK(bt_light_pwm(&Z, 600) == 0, "zero-length photoperiod means dark");
    /* pump: every 600 s run 20 s; dry protection */
    bt_pump_cfg_t P = {600, 20, 60, 30}; bt_pump_t p; bt_pump_init(&p); int on_s = 0, starts = 0; bool last = false;
    for (int t = 0; t < 3600; t++) { bool on = bt_pump_step(&p, &P, true, 1); if (on) on_s++; if (on && !last) starts++; last = on; }
    CHECK(starts >= 5 && starts <= 7, "starts %d", starts); CHECK(on_s == starts * 20, "run time %d for %d starts", on_s, starts);
    bt_pump_init(&p); int ran = 0; for (int t = 0; t < 700; t++) { bool w = t < 5; if (bt_pump_step(&p, &P, w, 1)) ran++; }
    CHECK(p.fault_dry && ran <= 5, "dry-run latched after %d s", ran); CHECK(!bt_pump_step(&p, &P, true, 1), "stays off while faulted"); bt_pump_clear_fault(&p); bool again = false; for (int t = 0; t < 700; t++) again |= bt_pump_step(&p, &P, true, 1); CHECK(again, "runs again after clear");
    bt_pump_cfg_t Pm = {60, 500, 15, 5}; bt_pump_init(&p); int mx = 0, cur = 0; for (int t = 0; t < 600; t++) { if (bt_pump_step(&p, &Pm, true, 1)) { cur++; if (cur > mx) mx = cur; } else cur = 0; } CHECK(mx <= 15, "max run enforced (%d)", mx);
    /* fan */
    CHECK(!bt_fan(false, 26, 28, 25), "below on"); CHECK(bt_fan(false, 28, 28, 25), "on at threshold"); CHECK(bt_fan(true, 26.5f, 28, 25), "hysteresis keeps on"); CHECK(!bt_fan(true, 25, 28, 25), "off at low threshold");
    /* calibration */
    bt_cal2_t ph = {2.5f, 7.0f, 3.0f, 4.0f}; CHECK(fabsf(bt_cal_apply(&ph, 2.5f) - 7.0f) < 1e-5f && fabsf(bt_cal_apply(&ph, 3.0f) - 4.0f) < 1e-5f && fabsf(bt_cal_apply(&ph, 2.75f) - 5.5f) < 1e-5f, "two-point cal");
    CHECK(fabsf(bt_ec_compensate(2.0f, 25) - 2.0f) < 1e-6f && bt_ec_compensate(2.2f, 30) < 2.2f && fabsf(bt_ec_compensate(2.2f, 30) - 2.0f) < 1e-3f, "ec compensation");
    /* filter: spike rejection */
    bt_filter_t f; bt_filter_init(&f); float y = 0; for (int i = 0; i < 30; i++) y = bt_filter_push(&f, (i == 15) ? 99.0f : 5.0f, 0.3f); CHECK(fabsf(y - 5.0f) < 0.05f, "median rejects spike (%f)", y);
    /* json */
    bt_state_t s = {22.4f, 6.05f, 1.83f, 12000, true, false, true, false, 255, 3600}; char b[256]; int n = bt_json(b, sizeof b, "tray1", &s);
    CHECK(n > 0 && strstr(b, "\"tray\":\"tray1\"") && strstr(b, "\"ph\":6.05") && strstr(b, "\"water\":true") && b[n - 1] == '}', "json %s", b); char tiny[20]; CHECK(bt_json(tiny, sizeof tiny, "tray1", &s) == -1, "json overflow detected");
    printf("%d checks, %d failures\n", checks, fails); return fails != 0;
}
