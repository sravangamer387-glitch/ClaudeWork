/* Jal-Rakshak host tests: controller core against a simulated tank/sump/pump/household (100 ms steps). */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../lib/jal_core.h"

static int pass, fail;
#define CHECK(c) do { if (c) pass++; else { fail++; printf("  FAIL %s:%d %s\n", __FILE__, __LINE__, #c); } } while (0)
static uint32_t rs = 123456789u;
static double rnd(void) { rs ^= rs << 13; rs ^= rs >> 17; rs ^= rs << 5; return (rs >> 8) / 16777216.0; }

typedef struct {
    double tank, sump;                 /* litres */
    double overflow, dry_s, tank_min;  /* statistics */
    int full_stuck_dry, sump_supply_on, ripple;
    double day_s;
} plant_t;
#define TANK_CAP 1000.0
#define PUMP_LPS 0.5
#define DT 0.1

static double consumption_lps(double hour) {
    if (hour < 6) { return 0.003; }
    if (hour < 9) { return 0.03; }
    if (hour < 17) { return 0.004; }
    if (hour < 22) { return 0.015; }
    return 0.002;
}
static jal_inputs_t probes(plant_t *p, bool pump_on) {
    jal_inputs_t in;
    bool sump_wet = p->sump > 30.0, low_wet = p->tank > 200.0, full_wet = p->tank >= 950.0;
    if (p->ripple) {                                                 /* surface turbulence near each threshold */
        if (pump_on && fabs(p->tank - 950.0) < 25.0 && rnd() < 0.35) full_wet = !full_wet;
        if (fabs(p->tank - 200.0) < 12.0 && rnd() < 0.25) low_wet = !low_wet;
        if (pump_on && fabs(p->sump - 30.0) < 10.0 && rnd() < 0.25) sump_wet = !sump_wet;
    }
    if (p->full_stuck_dry) full_wet = false;
    in.sump_wet = sump_wet; in.tank_low_wet = low_wet; in.tank_full_wet = full_wet; return in;
}
static void plant_step(plant_t *p, bool pump_on, double hour) {
    double flow = 0;
    if (pump_on) { flow = PUMP_LPS * DT; if (flow > p->sump) { p->dry_s += DT; flow = p->sump; } }
    p->sump -= flow; p->tank += flow;
    if (p->sump_supply_on) { double in = 0.6 * DT; if (p->sump + in > 1000.0) in = 1000.0 - p->sump; p->sump += in; }
    p->tank -= consumption_lps(hour) * DT; if (p->tank < 0) p->tank = 0;
    if (p->tank > TANK_CAP) { p->overflow += p->tank - TANK_CAP; p->tank = TANK_CAP; }
    if (p->tank < p->tank_min) p->tank_min = p->tank;
}

/* ---- scenario 1: 30 normal days with random power cuts and probe ripple */
static void test_thirty_days(void) {
    puts("30 simulated days, power cuts, ripple");
    plant_t p = {600, 500, 0, 0, 1e9, 0, 0, 1, 0}; jal_cfg_t cfg; jal_default_cfg(&cfg); jal_t j; uint32_t now = 1000; jal_init(&j, &cfg, now);
    bool power = true, prev_pump = false; uint32_t last_boot = now, last_stop = now, run_start = 0; int starts = 0, short_runs = 0, early_starts = 0, shortgap = 0;
    double next_cut = 3 * 86400.0 * rnd() + 86400.0, t = 0, cut_end = 0, min_stop_level = 1e9;
    for (long step = 0; step < 30L * 864000L; step++) {
        t = step * DT; double hour = fmod(t / 3600.0, 24.0); now = 1000u + (uint32_t)(step * 100u);
        p.sump_supply_on = (hour >= 6 && hour < 8) || (hour >= 18 && hour < 20); p.ripple = 1;
        if (power && t >= next_cut) { power = false; cut_end = t + 3600.0 * (1 + 3 * rnd()); if (j.pump) prev_pump = false; j.pump = false; }
        if (!power && t >= cut_end) { power = true; jal_init(&j, &cfg, now); last_boot = now; next_cut = t + 86400.0 * (2 + 4 * rnd()); }
        if (power && (step % 1 == 0)) jal_step(&j, now, probes(&p, j.pump));
        bool pump_on = power && jal_pump(&j);
        if (pump_on && !prev_pump) {
            starts++; run_start = now; if (now - last_boot < 60000u) early_starts++; if (now - last_stop < 120000u && starts > 1) shortgap++;
        }
        if (!pump_on && prev_pump) { last_stop = now; if (now - run_start < 300000u) short_runs++; if (p.tank < min_stop_level) min_stop_level = p.tank; }
        prev_pump = pump_on;
        plant_step(&p, pump_on, hour);
    }
    printf("  starts %d (%.1f/day), overflow %.1f L, min tank %.0f L, dry-run %.1f s, runs shorter than 5 min %d, starts within 60 s of power return %d, restarts within 120 s of a stop %d, lowest tank at a stop %.0f L\n",
           starts, starts / 30.0, p.overflow, p.tank_min, p.dry_s, short_runs, early_starts, shortgap, min_stop_level);
    CHECK(p.overflow < 1.0); CHECK(p.tank_min > 50.0); CHECK(starts / 30.0 <= 3.0); CHECK(p.dry_s < 30.0); CHECK(short_runs == 0);
    CHECK(early_starts == 0); CHECK(shortgap == 0); CHECK(min_stop_level > 900.0);                         /* stops only when really full */
}

/* ---- scenario 2: power-return delay */
static void test_power_return(void) {
    puts("power-return delay");
    jal_cfg_t cfg; jal_default_cfg(&cfg); jal_t j; uint32_t now = 5000; jal_init(&j, &cfg, now);
    jal_inputs_t low_tank = {true, false, false};                    /* tank below LOW, sump has water */
    for (uint32_t t = 0; t < 59000u; t += 100u) { now = 5000u + t; jal_step(&j, now, low_tank); }
    CHECK(!jal_pump(&j) && jal_status_code(&j) == 0);                /* still waiting at 59 s */
    for (uint32_t t = 59000u; t < 75000u; t += 100u) { now = 5000u + t; jal_step(&j, now, low_tank); }
    CHECK(jal_pump(&j));                                             /* running by 75 s */
}

/* ---- scenario 3: dry sump */
static void test_dry_sump(void) {
    puts("dry sump protection (sump runs out while pumping)");
    plant_t p = {300, 60, 0, 0, 1e9, 0, 0, 0, 0}; jal_cfg_t cfg; jal_default_cfg(&cfg); jal_t j; uint32_t now = 1000; jal_init(&j, &cfg, now);
    int starts = 0; bool prev = false;
    for (long step = 0; step < 3L * 864000L; step++) {               /* 3 days with no municipal supply */
        double hour = fmod(step * DT / 3600.0, 24.0); now = 1000u + (uint32_t)(step * 100u);
        jal_step(&j, now, probes(&p, j.pump)); bool on = jal_pump(&j); if (on && !prev) starts++; prev = on;
        plant_step(&p, on, hour);
    }
    printf("  pump starts in 3 dry days: %d, dry-run %.1f s, final state code %d\n", starts, p.dry_s, jal_status_code(&j));
    CHECK(starts >= 1 && starts <= 3); CHECK(p.dry_s < 40.0); CHECK(jal_status_code(&j) == 3);
    p.sump = 800; jal_reset_faults(&j, now);                          /* supply returns, user presses reset */
    for (long step = 0; step < 2000; step++) { now += 100; jal_step(&j, now, probes(&p, j.pump)); plant_step(&p, jal_pump(&j), 7.0); }
    CHECK(jal_pump(&j) || p.tank > 300.0);                           /* resumes filling */
}

/* ---- scenario 4: impossible probe combination */
static void test_probe_fault(void) {
    puts("probe fault");
    jal_cfg_t cfg; jal_default_cfg(&cfg); jal_t j; uint32_t now = 0; jal_init(&j, &cfg, now);
    jal_inputs_t bad = {true, false, true};                          /* FULL wet but LOW dry */
    for (uint32_t t = 0; t < 70000u; t += 100u) { now = t; jal_step(&j, now, bad); }
    CHECK(jal_status_code(&j) == 4 && !jal_pump(&j));
    jal_inputs_t ok = {true, true, false}; jal_reset_faults(&j, now);
    for (uint32_t t = 0; t < 5000u; t += 100u) { now += 100; jal_step(&j, now, ok); }
    CHECK(jal_status_code(&j) == 1);
}

/* ---- scenario 5: FULL probe dead (corroded): the learned run-time limit must stop the pump */
static double stuck_probe_overflow(bool learn_first) {
    plant_t p = {250, 800, 0, 0, 1e9, 0, 1, 1, 0}; jal_cfg_t cfg; jal_default_cfg(&cfg); jal_t j; uint32_t now = 1000; jal_init(&j, &cfg, now);
    if (learn_first) {                                               /* three normal fills so the controller learns the fill time */
        for (long step = 0; step < 2L * 864000L; step++) {
            double hour = fmod(step * DT / 3600.0, 24.0); now = 1000u + (uint32_t)(step * 100u); p.sump_supply_on = 1;
            jal_step(&j, now, probes(&p, j.pump)); plant_step(&p, jal_pump(&j), hour);
        }
        printf("  learned fill time %.1f min, run limit %.1f min\n", j.learned_fill_ms / 60000.0, jal_run_limit_ms(&j) / 60000.0);
    }
    p.full_stuck_dry = 1; p.overflow = 0; p.tank = 150; p.sump = 900; uint32_t base = now;
    for (long step = 0; step < 864000L / 2; step++) {
        now = base + (uint32_t)(step * 100u); p.sump_supply_on = 1;
        jal_step(&j, now, probes(&p, j.pump)); plant_step(&p, jal_pump(&j), 12.0);
    }
    CHECK(jal_status_code(&j) == 5);
    return p.overflow;
}
static void test_stuck_full(void) {
    puts("dead FULL probe");
    double learned = stuck_probe_overflow(true), unlearned = stuck_probe_overflow(false);
    printf("  overflow with learned limit %.0f L; with the factory default limit (never filled before) %.0f L\n", learned, unlearned);
    CHECK(learned <= 0.10 * TANK_CAP);
    CHECK(unlearned > 0.0);        /* limitation: with the factory 30 min limit a dead FULL probe still lets some water overflow; set the limit to about 1.1 x the tank's fill time */
}

int main(void) {
    test_power_return(); test_probe_fault(); test_dry_sump(); test_stuck_full(); test_thirty_days();
    printf("\n%d checks passed, %d failed\n", pass, fail);
    return fail ? 1 : 0;
}
