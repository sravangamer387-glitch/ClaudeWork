#include <math.h>
#include <stdio.h>
#include "../lib/prayog_core.h"
static int pass, fail;
#define CHECK(c) do { if (c) pass++; else { fail++; printf("  FAIL %s:%d %s\n", __FILE__, __LINE__, #c); } } while (0)
#define NEAR(a, b, tol) CHECK(fabsf((float)(a) - (float)(b)) <= (tol))

static uint16_t adc_for_ntc(float tc) {                       /* inverse of the divider + beta model */
    float t = tc + 273.15f, r = 10000.0f * expf(3950.0f * (1.0f / t - 1.0f / 298.15f));
    return (uint16_t)lroundf(1023.0f * 10000.0f / (10000.0f + r));
}
int main(void) {
    puts("temperature");
    for (float t = 0; t <= 80; t += 10) NEAR(conv_ntc_c(adc_for_ntc(t)), t, 0.6f);     /* 10-bit ADC resolution limits accuracy */
    NEAR(conv_ntc_c(512), 25.0f, 0.3f);
    puts("light, magnetism, voltage, soil");
    CHECK(conv_ldr_lux(900) > conv_ldr_lux(500) && conv_ldr_lux(500) > conv_ldr_lux(100));   /* brighter = more counts */
    NEAR(conv_hall_mt(512), 0.0f, 0.2f);                       /* 2.5 V = 0 mT */
    CHECK(conv_hall_mt(600) > 0 && conv_hall_mt(400) < 0);
    NEAR(conv_volt(1023, 3.0f), 15.0f, 0.01f);
    NEAR(conv_volt(341, 3.0f), 5.0f, 0.02f);
    NEAR(conv_soil_pct(620, 620, 300), 0.0f, 0.01f); NEAR(conv_soil_pct(300, 620, 300), 100.0f, 0.01f);
    NEAR(conv_soil_pct(460, 620, 300), 50.0f, 0.01f); NEAR(conv_soil_pct(100, 620, 300), 100.0f, 0.01f);   /* clamped */
    uint16_t quiet[8] = {512, 512, 512, 512, 512, 512, 512, 512}, loud[8] = {412, 612, 412, 612, 412, 612, 412, 612};
    NEAR(conv_mic_level(quiet, 8), 0.0f, 0.01f); NEAR(conv_mic_level(loud, 8), 100.0f, 0.01f);
    puts("ultrasonic");
    NEAR(speed_of_sound_ms(20.0f), 343.4f, 0.05f);
    NEAR(echo_to_cm(5824, 20.0f), 100.0f, 0.2f);               /* 1 m round trip 2 m at 343.4 m/s = 5824 us */
    NEAR(echo_to_cm(5824, 35.0f), 102.6f, 0.4f);               /* hot air: sound is faster, same echo reads longer */
    puts("photogate");
    gate_t g; gate_init(&g); float period, dt;
    for (int i = 0; i < 6; i++) { gate_push(&g, 100000u + (uint32_t)i * 2006000u, 1); gate_push(&g, 100000u + (uint32_t)i * 2006000u + 15000u, 0); }
    CHECK(gate_period_s(&g, &period)); NEAR(period, 2.006f, 0.001f);       /* pendulum of length 1 m: T = 2.006 s */
    gate_init(&g); gate_push(&g, 5000, 1); gate_push(&g, 5000 + 25000, 0);
    CHECK(gate_transit_s(&g, &dt)); NEAR(dt, 0.025f, 1e-6f); NEAR(speed_from_transit(0.05f, dt), 2.0f, 0.001f);
    gate_init(&g); CHECK(!gate_period_s(&g, &period)); gate_push(&g, 1, 1); CHECK(!gate_period_s(&g, &period));
    for (int i = 0; i < 40; i++) { gate_push(&g, (uint32_t)i * 1000u, (uint8_t)(i & 1)); }
    CHECK(g.n == GATE_MAX);   /* ring buffer never overflows */
    puts("statistics and commands");
    float x[5] = {10, 11, 9, 10, 12}; stats_t s = stats_of(x, 5); NEAR(s.mean, 10.4f, 0.001f); NEAR(s.sd, 1.1402f, 0.001f);
    float spike[5] = {10, 10, 500, 10, 10}; NEAR(median5(spike), 10.0f, 0.001f);
    uint8_t ch; sensor_t st;
    CHECK(parse_set("SET 3 HALL", &ch, &st) == 0 && ch == 3 && st == S_HALL);
    CHECK(parse_set("SET 0 NTC\n", &ch, &st) == 0 && ch == 0 && st == S_NTC);
    CHECK(parse_set("SET 9 NTC", &ch, &st) != 0); CHECK(parse_set("SET 1 BOGUS", &ch, &st) != 0); CHECK(parse_set("GET 1 NTC", &ch, &st) != 0);
    printf("\n%d checks passed, %d failed\n", pass, fail);
    return fail ? 1 : 0;
}
