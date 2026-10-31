/* Kheti-Mitra host tests: unit tests of the control rules and a 90-day soil water-balance simulation compared with timers. */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../lib/kheti_core.h"

static int pass, fail;
#define CHECK(c) do { if (c) pass++; else { fail++; printf("  FAIL %s:%d %s\n", __FILE__, __LINE__, #c); } } while (0)
static uint32_t rs = 987654321u;
static double rnd(void) { rs ^= rs << 13; rs ^= rs >> 17; rs ^= rs << 5; return (rs >> 8) / 16777216.0; }
static double gauss(void) { double u = rnd() + 1e-9, v = rnd(); return sqrt(-2 * log(u)) * cos(2 * M_PI * v); }

static uint16_t adc_for_pct(double pct) { return (uint16_t)lround(620.0 - pct / 100.0 * 320.0); }
#define MIN_MS 60000UL

/* ---------------- unit tests ---------------- */
static void unit_tests(void) {
    puts("control rules");
    kheti_cfg_t cfg; kheti_default_cfg(&cfg); kheti_t k; uint32_t now = 0; kheti_init(&k, &cfg, now);
    kheti_inputs_t dry = {{adc_for_pct(25), adc_for_pct(25)}, false, false}, wet = {{adc_for_pct(75), adc_for_pct(75)}, false, false}, mid = {{adc_for_pct(50), adc_for_pct(50)}, false, false};
    kheti_step(&k, now, mid); CHECK(!kheti_valve(&k));                         /* 50 % is between thresholds: no water */
    now += 1000; kheti_step(&k, now, dry); CHECK(kheti_valve(&k) && kheti_status_code(&k) == 2);   /* below 35 %: start */
    now += 1000; kheti_step(&k, now, mid); CHECK(kheti_valve(&k));            /* hysteresis: keeps watering until 70 % */
    now += 1000; kheti_step(&k, now, wet); CHECK(!kheti_valve(&k));           /* stop above 70 % */
    now += 1000; kheti_step(&k, now, dry); CHECK(!kheti_valve(&k));           /* min interval (3 h) blocks an immediate restart */
    now += 3UL * 3600000UL; kheti_step(&k, now, dry); CHECK(kheti_valve(&k));  /* after 3 h it may restart */

    puts("time limit when the sensor does not respond");
    kheti_init(&k, &cfg, 0); now = 0; kheti_step(&k, now, dry); CHECK(kheti_valve(&k));
    for (int m = 1; m <= 25; m++) { now = (uint32_t)m * MIN_MS; kheti_step(&k, now, dry); if (m == 19) CHECK(kheti_valve(&k)); }
    CHECK(!kheti_valve(&k));                                                    /* closed by the 20 min limit */

    puts("daily budget");
    kheti_cfg_t c2 = cfg; c2.min_interval_ms = 60000UL; kheti_init(&k, &c2, 0); now = 0; int opens = 0; bool prev = false;
    for (uint32_t m = 0; m < 24 * 60; m++) { now = m * MIN_MS; kheti_step(&k, now, dry); if (kheti_valve(&k) && !prev) opens++; prev = kheti_valve(&k); }
    printf("  with a 1 min interval and permanently dry readings the valve opened %d times; total on-time %lu min\n", opens, (unsigned long)(k.day_on_ms / MIN_MS));
    CHECK(k.day_on_ms <= 60UL * MIN_MS + 1000UL);                               /* never more than 60 min per day */

    puts("rain hold");
    kheti_init(&k, &cfg, 0); now = 3UL * 3600000UL; kheti_inputs_t rain = dry; rain.rain_wet = true;
    kheti_step(&k, now, rain); CHECK(!kheti_valve(&k));
    now += 3600000UL; kheti_step(&k, now, dry); CHECK(!kheti_valve(&k) && kheti_status_code(&k) == 3);     /* 1 h after rain: still held */
    now += 12UL * 3600000UL; kheti_step(&k, now, dry); CHECK(kheti_valve(&k));                              /* after 12 h: waters if dry */

    puts("sensor faults");
    kheti_inputs_t one_bad = {{adc_for_pct(20), 1023}, false, false};          /* second sensor open: first still works */
    kheti_init(&k, &cfg, 0); now = 5000; kheti_step(&k, now, one_bad); CHECK(kheti_valve(&k) && k.valid_mask == 1);
    kheti_inputs_t both_bad = {{1023, 5}, false, false};
    kheti_init(&k, &cfg, 0); now = 0; int fopens = 0; prev = false; uint32_t on_ms = 0;
    for (uint32_t m = 0; m < 3 * 24 * 60; m++) { now = m * MIN_MS; kheti_step(&k, now, both_bad); if (kheti_valve(&k)) on_ms += MIN_MS; if (kheti_valve(&k) && !prev) fopens++; prev = kheti_valve(&k); }
    printf("  both sensors failed for 3 days: %d fallback waterings, %lu min of water in total\n", fopens, (unsigned long)(on_ms / MIN_MS));
    CHECK(fopens >= 5 && fopens <= 7); CHECK(on_ms <= 7UL * 5UL * MIN_MS);     /* 5 min every 12 h */
}

/* ---------------- 90-day soil water balance ---------------- */
typedef struct { double theta, applied, perc, runoff, et_act, et_pot; int stress_days; double stress_minutes_today; double max_run_min; } soil_t;
#define Z 300.0
#define WP 0.12
#define FC 0.32
#define SAT 0.40
typedef enum { STRAT_CONTROLLER, STRAT_TIMER20, STRAT_TIMER10, STRAT_NONE } strat_t;

static soil_t simulate(strat_t strat, uint32_t weather_seed, uint16_t *max_single_run_min, uint32_t *max_day_on_min) {
    uint32_t keep = rs; rs = weather_seed;
    soil_t s = {0.26, 0, 0, 0, 0, 0, 0, 0, 0};
    kheti_cfg_t cfg; kheti_default_cfg(&cfg); kheti_t k; kheti_init(&k, &cfg, 0);
    double rain_left_mm = 0, rain_rate = 0; int rain_start_min = -1, rain_day_start = -1; double sensor_pct = 100.0 * (s.theta - 0.05) / (SAT - 0.05); double et_day = 4.5;
    bool valve = false; int run_min = 0; uint32_t day_on = 0; *max_single_run_min = 0; *max_day_on_min = 0; int rain_wet_until = -1;
    for (int day = 0; day < 90; day++) {
        et_day = 4.5 + 1.5 * sin(2 * M_PI * day / 90.0) + 0.7 * gauss(); if (et_day < 1.5) et_day = 1.5;
        if (rnd() < 0.18) { rain_day_start = (int)(rnd() * 20 * 60); rain_left_mm = -12.0 * log(rnd() + 1e-6); rain_rate = rain_left_mm / 60.0; rain_start_min = rain_day_start; } else rain_start_min = -1;
        s.stress_minutes_today = 0; day_on = 0;
        for (int m = 0; m < 1440; m++) {
            double rain_now = 0; if (rain_start_min >= 0 && m >= rain_start_min && m < rain_start_min + 60) { rain_now = rain_rate; rain_wet_until = m + 30; }
            bool rain_sensor = rain_start_min >= 0 && m >= rain_start_min && m < rain_start_min + 60 + 30;
            double irr = 0;
            if (strat == STRAT_CONTROLLER) {
                kheti_inputs_t in; in.adc[0] = (uint16_t)lround(620.0 - sensor_pct / 100.0 * 320.0 + 3 * gauss()); in.adc[1] = (uint16_t)lround(620.0 - sensor_pct / 100.0 * 320.0 + 3 * gauss());
                in.rain_wet = rain_sensor; in.manual_hold = false;
                uint32_t now_ms = (uint32_t)((long)(day * 1440 + m) * 60000L);       /* wraps after 49.7 days: the core must cope */
                kheti_step(&k, now_ms, in); valve = kheti_valve(&k);
            } else if (strat == STRAT_TIMER20) valve = (m >= 360 && m < 380);
            else if (strat == STRAT_TIMER10) valve = (m >= 360 && m < 370);
            else valve = false;
            if (valve) { irr = 0.25; run_min++; day_on++; if (run_min > *max_single_run_min) *max_single_run_min = (uint16_t)run_min; } else run_min = 0;
            if (day_on > *max_day_on_min) *max_day_on_min = day_on;
            double awc = (s.theta - WP) / (FC - WP); if (awc < 0) awc = 0;
            double et = et_day * (m > 360 && m < 1080 ? sin(M_PI * (m - 360) / 720.0) / 458.4 : 0.0); s.et_pot += et; if (awc < 0.5) et *= fmax(0.1, awc / 0.5); s.et_act += et;
            s.theta += (rain_now + irr - et) / Z; s.applied += irr;
            if (s.theta > FC) { double d = (s.theta - FC) / 360.0; s.theta -= d; s.perc += d * Z; }
            if (s.theta > SAT) { s.runoff += (s.theta - SAT) * Z; s.theta = SAT; }
            if (s.theta < 0.03) s.theta = 0.03;
            double target = 100.0 * (s.theta - 0.05) / (SAT - 0.05); sensor_pct += (target - sensor_pct) / 10.0;       /* 10 min sensor lag */
            if ((s.theta - WP) / (FC - WP) < 0.5) s.stress_minutes_today += 1;       /* below the usual 50 % allowed depletion */
        }
        if (s.stress_minutes_today >= 60) s.stress_days++;
    }
    (void)rain_wet_until; rs = keep; return s;
}

static void water_balance(void) {
    puts("90-day soil water balance (loam, 300 mm root zone, valve 0.25 mm/min)");
    const char *names[] = {"Kheti-Mitra controller", "Timer 20 min every day", "Timer 10 min every day", "No irrigation"};
    soil_t r[4]; uint16_t mr[4]; uint32_t md[4];
    double tot_applied[4] = {0}, tot_perc[4] = {0}, tot_rel[4] = {0}; int tot_stress[4] = {0}; int seeds = 10;
    for (int w = 0; w < seeds; w++)
        for (int s = 0; s < 4; s++) { r[s] = simulate((strat_t)s, 1000u + (uint32_t)w * 7919u, &mr[s], &md[s]); tot_applied[s] += r[s].applied; tot_perc[s] += r[s].perc; tot_stress[s] += r[s].stress_days; tot_rel[s] += r[s].et_act / r[s].et_pot; }
    printf("  average over %d weather seeds (90 days each):\n  | Strategy | Water applied mm | Deep percolation loss mm | Days below 50 %% available water | Plant water use as %% of potential |\n  |---|---|---|---|---|\n", seeds);
    for (int s = 0; s < 4; s++) printf("  | %s | %.0f | %.0f | %.1f | %.1f %% |\n", names[s], tot_applied[s] / seeds, tot_perc[s] / seeds, tot_stress[s] / (double)seeds, 100.0 * tot_rel[s] / seeds);
    uint16_t mrun; uint32_t mday; simulate(STRAT_CONTROLLER, 1000u, &mrun, &mday);
    printf("  controller: longest single watering %u min, most on-time in one day %u min\n", mrun, mday);
    CHECK(tot_stress[0] / (double)seeds <= 3.0);                                              /* keeps the soil above 50 % available water */
    CHECK(tot_rel[0] / seeds >= 0.97);                                                        /* plants get at least 97 % of their potential water use */
    CHECK(tot_applied[0] <= 0.8 * tot_applied[1]);                                            /* saves at least 20 % of a 20 min daily timer */
    CHECK(tot_perc[0] <= tot_perc[1]);                                                        /* wastes less to deep percolation */
    CHECK(tot_stress[0] <= tot_stress[2] && tot_stress[0] < tot_stress[3]);
    CHECK(mrun <= 20 && mday <= 60);
}

int main(void) { unit_tests(); water_balance(); printf("\n%d checks passed, %d failed\n", pass, fail); return fail ? 1 : 0; }
