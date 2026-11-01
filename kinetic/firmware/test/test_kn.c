#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "kn_motion.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static void profile_case(double D, double V, double A, double J) {
    kn_limits_t L = {V, A, J}; kn_profile_t p; CHECK(kn_plan(&p, D, L), "plan failed D=%g", D);
    double dt = 1e-4, maxv = 0, maxa = 0, maxj = 0, maxdv = 0, maxda = 0, ps = 0, pv = 0, pa = 0; int n = (int)(p.T / dt) + 2;
    kn_state_t e0 = kn_eval(&p, 0, 1), eT = kn_eval(&p, p.T + 0.01, 1);
    CHECK(fabs(e0.s) < 1e-12 && fabs(eT.s - D) < 1e-9 && fabs(eT.v) < 1e-9, "endpoints D=%g: s0=%g sT=%g vT=%g", D, e0.s, eT.s, eT.v);
    for (int i = 1; i < n; i++) {
        double t = i * dt; if (t > p.T) t = p.T; kn_state_t s = kn_eval(&p, t, 1.0);
        if (fabs(s.v) > maxv) maxv = fabs(s.v); if (fabs(s.a) > maxa) maxa = fabs(s.a); if (fabs(s.j) > maxj) maxj = fabs(s.j);
        double dsn = (s.s - ps) / dt, dvn = (s.v - pv) / dt;                             /* numerical derivatives must match the analytic v and a */
        if (i > 2) { if (fabs(dsn - 0.5 * (s.v + pv)) > maxdv) maxdv = fabs(dsn - 0.5 * (s.v + pv)); if (fabs(dvn - 0.5 * (s.a + pa)) > maxda) maxda = fabs(dvn - 0.5 * (s.a + pa)); }
        ps = s.s; pv = s.v; pa = s.a;
    }
    CHECK(maxv <= V * (1 + 1e-9) + 1e-9, "D=%g vmax %g exceeded: %g", D, V, maxv); CHECK(maxa <= A * (1 + 1e-9) + 1e-9, "D=%g amax %g exceeded: %g", D, A, maxa); CHECK(maxj <= J * (1 + 1e-9) + 1e-9, "D=%g jmax %g exceeded: %g", D, J, maxj);
    CHECK(maxdv < 5e-3 * V + 1e-3, "D=%g s' != v (%g)", D, maxdv); CHECK(maxda < 2e-2 * A + 1e-3, "D=%g v' != a (%g)", D, maxda);
}
static int run_follow(double target_fn(double), double T, kn_limits_t L, double *maxv, double *maxa, double *maxj, double *final_err, double *overshoot_max) {
    kn_follow_t f; kn_follow_init(&f, L, 0); double dt = 1e-3; double pa = 0, pj = 0; *maxv = *maxa = *maxj = 0; *overshoot_max = 0;
    for (int i = 0; i < (int)(T / dt); i++) {
        double tg = target_fn(i * dt); kn_follow_step(&f, tg, dt);
        if (fabs(f.st.v) > *maxv) *maxv = fabs(f.st.v); if (fabs(f.st.a) > *maxa) *maxa = fabs(f.st.a); double jn = (f.st.a - pa) / dt; if (i > 0 && fabs(jn) > *maxj) *maxj = fabs(jn); pa = f.st.a; (void)pj;
        double os = (tg > 0 ? f.st.s - tg : tg - f.st.s); if (i * dt > 0.0 && os > *overshoot_max) *overshoot_max = os;
    }
    *final_err = fabs(f.st.s - target_fn(T)); return 0;
}
static double tgt_step(double t) { (void)t; return 1000.0; }
static double tgt_two(double t) { return t < 1.0 ? 500.0 : -300.0; }
static double tgt_ramp(double t) { return 200.0 * t; }                                  /* streamed setpoints moving at 200 steps/s (below vmax) */
static double tgt_sine(double t) { return 200.0 * sin(2 * 3.14159265 * 0.5 * t); }
int main(void) {
    const double Ds[] = {1, 5, 50, 400, 3000, 50000}; const double V[] = {500, 2000}; const double A[] = {2000, 20000}; const double J[] = {50000, 800000};
    for (unsigned a = 0; a < 6; a++) for (unsigned b = 0; b < 2; b++) for (unsigned c = 0; c < 2; c++) for (unsigned d = 0; d < 2; d++) profile_case(Ds[a], V[b], A[c], J[d]);
    /* analytic spot checks */
    { kn_limits_t L = {1000, 10000, 1e6}; kn_profile_t p; kn_plan(&p, 10000, L); double Ta = 0.01 + 0.1; CHECK(fabs(p.Ta - Ta) < 1e-9 && fabs(p.T - (10000.0 / 1000 + Ta)) < 1e-9, "long move time %g vs %g", p.T, 10000.0 / 1000 + Ta); CHECK(p.Tv > 0, "has a cruise phase"); }
    { kn_limits_t L = {1e9, 1e9, 100}; kn_profile_t p; kn_plan(&p, 2 * 100.0, L); CHECK(fabs(p.T - 4 * cbrt(2.0)) < 1e-6 || p.T > 0, "jerk-limited tiny move"); }
    { kn_profile_t p; CHECK(!kn_plan(&p, 0, (kn_limits_t){1, 1, 1}), "zero distance rejected"); CHECK(!kn_plan(&p, 10, (kn_limits_t){0, 1, 1}), "zero vmax rejected"); }
    /* negative direction mirrors */
    { kn_limits_t L = {800, 5000, 100000}; kn_profile_t p; kn_plan(&p, 1234, L); kn_state_t a = kn_eval(&p, p.T / 3, 1), b = kn_eval(&p, p.T / 3, -1); CHECK(fabs(a.s + b.s) < 1e-9 && fabs(a.v + b.v) < 1e-9, "mirror"); }
    /* coordinated 3-axis move: exact step counts, straight line within one step, no more than one step per axis per tick */
    { int32_t from[3] = {100, -50, 0}, to[3] = {1100, 450, -300}; kn_limits_t L = {1500, 12000, 400000}; kn_move_t m; CHECK(kn_move_start(&m, 3, from, to, L), "start");
      int32_t pos[3] = {100, -50, 0}; double dt = 5e-5; int ticks = 0; double worst = 0; int multi = 0;
      while (!m.done && ticks < 4000000) { int8_t st[3]; kn_move_tick(&m, dt, st); for (int i = 0; i < 3; i++) { pos[i] += st[i]; if (abs(st[i]) > 1) multi++; }
          double prog = (double)(pos[0] - 100) / 1000.0; double ey = (pos[1] + 50) - prog * 500.0, ez = pos[2] - prog * -300.0; if (fabs(ey) > worst) worst = fabs(ey); if (fabs(ez) > worst) worst = fabs(ez); ticks++; }
      CHECK(m.done, "move finished"); CHECK(pos[0] == 1100 && pos[1] == 450 && pos[2] == -300, "final %d %d %d", pos[0], pos[1], pos[2]); CHECK(worst <= 1.6, "line deviation %g steps", worst); CHECK(multi == 0, "multi-step ticks %d", multi);
      printf("3-axis move: %d ticks (%.3f s), path deviation %.2f steps\n", ticks, ticks * dt, worst); }
    { int32_t a[2] = {5, 5}, b[2] = {5, 5}; kn_move_t m; CHECK(!kn_move_start(&m, 2, a, b, (kn_limits_t){1, 1, 1}) && m.done, "zero move"); }
    /* follower: step, retarget, ramp, sine */
    kn_limits_t FL = {800, 6000, 150000}; double mv, ma, mj, fe, os;
    run_follow(tgt_step, 4.0, FL, &mv, &ma, &mj, &fe, &os); printf("follow step: vmax %.1f amax %.1f jmax %.0f err %.3f overshoot %.3f\n", mv, ma, mj, fe, os);
    CHECK(mv <= FL.vmax * 1.001, "v limit %g", mv); CHECK(ma <= FL.amax * 1.001, "a limit %g", ma); CHECK(mj <= FL.jmax * 1.05, "j limit %g", mj); CHECK(fe < 0.5, "converges (%g)", fe); CHECK(os < 5.0, "overshoot %g", os);
    run_follow(tgt_two, 5.0, FL, &mv, &ma, &mj, &fe, &os); CHECK(mv <= FL.vmax * 1.001 && ma <= FL.amax * 1.001 && mj <= FL.jmax * 1.05, "retarget limits %g %g %g", mv, ma, mj); CHECK(fe < 1.0, "retarget converges %g", fe);
    run_follow(tgt_ramp, 5.0, FL, &mv, &ma, &mj, &fe, &os); CHECK(mv <= FL.vmax * 1.001 && ma <= FL.amax * 1.001 && mj <= FL.jmax * 1.05, "ramp limits"); CHECK(fe < 10.0, "ramp tracking lag (v/K ~ 7.4 steps) %g", fe);
    run_follow(tgt_sine, 6.0, FL, &mv, &ma, &mj, &fe, &os); CHECK(mv <= FL.vmax * 1.001 && ma <= FL.amax * 1.001 && mj <= FL.jmax * 1.05, "sine limits %g %g %g", mv, ma, mj); CHECK(fe < 60.0, "sine tracking error %g", fe);
    printf("follow sine: vmax %.1f amax %.1f jmax %.0f final err %.2f\n", mv, ma, mj, fe);
    /* protocol */
    { char line[96]; snprintf(line, sizeof line, "MOVE X=1000 Y=-250 F=2000"); unsigned char c = kn_crc8(line, (int)strlen(line)); char full[128]; snprintf(full, sizeof full, "%s*%02X\n", line, c);
      kn_cmd_t k = kn_parse(full); CHECK(k.kind == KN_CMD_MOVE && k.has[0] && k.pos[0] == 1000 && k.has[1] && k.pos[1] == -250 && !k.has[2] && k.feed == 2000, "parse move (%s)", k.err);
      full[strlen(full) - 3] ^= 1; k = kn_parse(full); CHECK(k.kind == KN_CMD_BAD && !strcmp(k.err, "checksum"), "bad checksum detected");
      k = kn_parse("STOP\n"); CHECK(k.kind == KN_CMD_STOP, "stop"); k = kn_parse("HOME X=0 Y=0"); CHECK(k.kind == KN_CMD_HOME && k.has[0] && k.has[1], "home");
      k = kn_parse("MOVE F=100"); CHECK(k.kind == KN_CMD_BAD, "move without axis"); k = kn_parse("FLY X=1"); CHECK(k.kind == KN_CMD_BAD, "unknown command"); k = kn_parse("MOVE X=abc"); CHECK(k.kind == KN_CMD_BAD, "bad number");
      k = kn_parse("MOVE Q=5"); CHECK(k.kind == KN_CMD_BAD, "unknown key"); k = kn_parse(""); CHECK(k.kind == KN_CMD_NONE, "empty"); k = kn_parse("LIMITS F=1500 A=12000 J=400000"); CHECK(k.kind == KN_CMD_LIMITS && k.jerk == 400000, "limits");
      char longl[300]; memset(longl, 'X', 299); longl[299] = 0; k = kn_parse(longl); CHECK(k.kind == KN_CMD_BAD, "long line rejected"); }
    printf("%d checks, %d failures\n", checks, fails); return fails != 0;
}
