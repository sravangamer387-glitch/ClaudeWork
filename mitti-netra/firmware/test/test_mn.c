#include <stdio.h>
#include <math.h>
#include <string.h>
#include "mn_core.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
int main(void) {
    mn_soil_cal_t S = {2800, 1200}; CHECK(mn_soil_pct(&S, 2800) == 0 && mn_soil_pct(&S, 1200) == 100 && fabsf(mn_soil_pct(&S, 2000) - 50) < 1e-4f && mn_soil_pct(&S, 3500) == 0 && mn_soil_pct(&S, 100) == 100, "soil cal and clamp");
    float r, p; mn_tilt_deg(0, 0, 1, &r, &p); CHECK(fabsf(r) < 1e-4f && fabsf(p) < 1e-4f, "level");
    mn_tilt_deg(0, sinf(0.1745329f), cosf(0.1745329f), &r, &p); CHECK(fabsf(r - 10) < 1e-3f && fabsf(p) < 1e-3f, "roll 10 deg (%f)", r);
    mn_tilt_deg(-sinf(0.2617994f), 0, cosf(0.2617994f), &r, &p); CHECK(fabsf(p - 15) < 1e-3f && fabsf(r) < 1e-3f, "pitch 15 deg (%f)", p);
    mn_strain_cfg_t C = {5.0f, 3.3f, 128, 2.0f, 4}; float fs = 0.5f * 3.3f / 128; CHECK(fabsf(mn_hx711_volts(&C, 8388607) - fs) < 1e-6f, "full scale %g", mn_hx711_volts(&C, 8388607));
    /* quarter bridge, GF 2, 100 microstrain => dR/R = 2e-4 => Vout = Vex * 2e-4 / 4 = 0.25 mV */
    int32_t raw = (int32_t)lroundf(0.25e-3f / (fs / 8388608.0f)); CHECK(fabsf(mn_microstrain(&C, raw, 0) - 100.0f) < 1.0f, "microstrain %f from raw %ld", mn_microstrain(&C, raw, 0), (long)raw);
    CHECK(fabsf(mn_microstrain(&C, raw + 1000, 1000) - mn_microstrain(&C, raw, 0)) < 1e-3f, "zero offset");
    /* alarm */
    mn_thresh_t T = {0.5f, 1.0f, 0.1f, 3}; mn_alarm_t a; mn_alarm_init(&a);
    mn_alarm_update(&a, &T, 1.2f); mn_alarm_update(&a, &T, 1.2f); CHECK(a.level == MN_OK, "debounce holds 2 readings"); mn_alarm_update(&a, &T, 1.2f); CHECK(a.level == MN_ALARM, "alarm after 3");
    mn_alarm_update(&a, &T, 0.95f); CHECK(a.level == MN_ALARM, "hysteresis keeps alarm at 0.95"); mn_alarm_update(&a, &T, 0.85f); CHECK(a.level == MN_WATCH, "drops to watch"); mn_alarm_update(&a, &T, 0.45f); CHECK(a.level == MN_WATCH, "hysteresis keeps watch"); mn_alarm_update(&a, &T, 0.3f); CHECK(a.level == MN_OK, "back to ok");
    mn_alarm_init(&a); mn_alarm_update(&a, &T, 1.2f); mn_alarm_update(&a, &T, 0.1f); mn_alarm_update(&a, &T, 1.2f); mn_alarm_update(&a, &T, 1.2f); CHECK(a.level == MN_OK, "a single dip resets the debounce");
    mn_alarm_init(&a); for (int i = 0; i < 3; i++) mn_alarm_update(&a, &T, -1.5f); CHECK(a.level == MN_ALARM, "negative magnitude uses |x|");
    /* interval */
    CHECK(mn_next_interval_s(MN_OK, 4.0f, false) == 21600 && mn_next_interval_s(MN_OK, 4.0f, true) == 3600 && mn_next_interval_s(MN_WATCH, 4.0f, false) == 1800 && mn_next_interval_s(MN_ALARM, 4.0f, false) == 600, "intervals");
    CHECK(mn_next_interval_s(MN_OK, 3.4f, false) == 4 * 21600 && mn_next_interval_s(MN_ALARM, 3.4f, false) == 600, "low battery stretches routine reports but never an alarm");
    /* frame */
    mn_report_t R = {1234, 1767225600u, 437, 261, -1250, 875, -321, 3987, MN_WATCH, 5}, Q; uint8_t f[MN_FRAME_LEN]; CHECK(mn_pack(&R, f) == MN_FRAME_LEN, "frame length");
    CHECK(mn_unpack(f, &Q) && !memcmp(&R, &Q, sizeof R), "round trip"); uint8_t g[MN_FRAME_LEN]; memcpy(g, f, sizeof f); g[9] ^= 0x10; CHECK(!mn_unpack(g, &Q), "bit flip detected");
    memcpy(g, f, sizeof f); g[0] = 0; CHECK(!mn_unpack(g, &Q), "bad magic"); memcpy(g, f, sizeof f); g[1] = 2; CHECK(!mn_unpack(g, &Q), "bad version");
    const uint8_t chk[] = "123456789"; CHECK(mn_crc16(chk, 9) == 0x29B1, "CRC-16/CCITT-FALSE check value %04X", mn_crc16(chk, 9));
    printf("%d checks, %d failures\n", checks, fails); return fails != 0; }
