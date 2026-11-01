#include "kn_motion.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
bool kn_plan(kn_profile_t *p, double dist, kn_limits_t L) {
    memset(p, 0, sizeof *p); p->L = L; double D = fabs(dist);
    if (!(L.vmax > 0 && L.amax > 0 && L.jmax > 0) || D <= 0) return false;
    p->D = D; double Tj, Ta, vp, ap;
    /* velocity-limited case: does the S-curve reach vmax? */
    if (L.vmax * L.jmax < L.amax * L.amax) { Tj = sqrt(L.vmax / L.jmax); Ta = 2 * Tj; ap = L.jmax * Tj; }                    /* acceleration limit never reached */
    else { Tj = L.amax / L.jmax; Ta = Tj + L.vmax / L.amax; ap = L.amax; }
    vp = L.vmax;
    if (D >= vp * Ta) { p->Tv = (D - vp * Ta) / vp; }
    else {                                                                                                                     /* distance too short to reach vmax */
        p->Tv = 0;
        if (D >= 2 * pow(L.amax, 3) / (L.jmax * L.jmax)) { Tj = L.amax / L.jmax; Ta = (Tj + sqrt(Tj * Tj + 4 * D / L.amax)) / 2; ap = L.amax; }
        else { Tj = cbrt(D / (2 * L.jmax)); Ta = 2 * Tj; ap = L.jmax * Tj; }
        vp = ap * (Ta - Tj);
    }
    p->Tj = Tj; p->Ta = Ta; p->vp = vp; p->ap = ap; p->T = 2 * Ta + p->Tv; p->ok = true; return true;
}
/* acceleration phase (0..Ta) of a symmetric profile; returns s, v, a, j relative to the start of the phase */
static kn_state_t accel_phase(const kn_profile_t *p, double t) {
    double J = p->L.jmax, Tj = p->Tj, Ta = p->Ta, ap = p->ap; kn_state_t r = {0, 0, 0, 0};
    double Tc = Ta - 2 * Tj;                                   /* constant-acceleration time */
    if (t < Tj) { r.j = J; r.a = J * t; r.v = J * t * t / 2; r.s = J * t * t * t / 6; }
    else if (t < Tj + Tc) { double u = t - Tj, v1 = J * Tj * Tj / 2, s1 = J * Tj * Tj * Tj / 6; r.j = 0; r.a = ap; r.v = v1 + ap * u; r.s = s1 + v1 * u + ap * u * u / 2; }
    else { double u = t - Tj - Tc, v1 = J * Tj * Tj / 2, s1 = J * Tj * Tj * Tj / 6, v2 = v1 + ap * Tc, s2 = s1 + v1 * Tc + ap * Tc * Tc / 2;
           r.j = -J; r.a = ap - J * u; r.v = v2 + ap * u - J * u * u / 2; r.s = s2 + v2 * u + ap * u * u / 2 - J * u * u * u / 6; }
    return r;
}
kn_state_t kn_eval(const kn_profile_t *p, double t, double sign) {
    kn_state_t r; double Ta = p->Ta, T = p->T;
    if (t <= 0) { r.s = r.v = r.a = r.j = 0; return r; }
    if (t >= T) { r.s = p->D; r.v = r.a = r.j = 0; r.s *= sign; return r; }
    if (t < Ta) r = accel_phase(p, t);
    else if (t < Ta + p->Tv) { kn_state_t e = accel_phase(p, Ta); r.s = e.s + p->vp * (t - Ta); r.v = p->vp; r.a = r.j = 0; }
    else { double u = t - Ta - p->Tv; kn_state_t m = accel_phase(p, Ta), d = accel_phase(p, Ta - u);                 /* deceleration mirrors the acceleration */
           double s_end = p->D; r.s = s_end - d.s; r.v = d.v; r.a = -d.a; r.j = d.j; (void)m; }
    r.s *= sign; r.v *= sign; r.a *= sign; r.j *= sign; return r;
}
bool kn_move_start(kn_move_t *m, int n, const int32_t from[], const int32_t to[], kn_limits_t L) {
    memset(m, 0, sizeof *m); m->n = n; double dom = 0;
    for (int i = 0; i < n; i++) { m->delta[i] = (double)to[i] - (double)from[i]; m->target[i] = to[i]; if (fabs(m->delta[i]) > dom) dom = fabs(m->delta[i]); }
    if (dom <= 0) { m->done = true; return false; }
    m->dom = dom; for (int i = 0; i < n; i++) m->frac[i] = m->delta[i] / dom;
    m->sign = 1.0; if (!kn_plan(&m->prof, dom, L)) { m->done = true; return false; }
    return true;
}
void kn_move_tick(kn_move_t *m, double dt, int8_t steps_out[]) {
    for (int i = 0; i < m->n; i++) steps_out[i] = 0;
    if (m->done) return;
    m->t += dt; kn_state_t s = kn_eval(&m->prof, m->t, 1.0); bool last = m->t >= m->prof.T;
    for (int i = 0; i < m->n; i++) {
        double want = s.s * m->frac[i]; int32_t w = last ? (int32_t)llround(m->delta[i]) : (int32_t)(want >= 0 ? floor(want) : ceil(want));       /* whole steps reached so far */
        int d = w - m->emitted[i]; if (d > 1) d = 1; if (d < -1) d = -1; if (d) { m->emitted[i] += d; steps_out[i] = (int8_t)d; }
    }
    if (last) { bool fin = true; for (int i = 0; i < m->n; i++) if (m->emitted[i] != (int32_t)llround(m->delta[i])) fin = false; if (fin) m->done = true; }
}
/* ------------------------------ online follower ------------------------------ */
void kn_follow_init(kn_follow_t *f, kn_limits_t L, double pos) { f->L = L; f->st.s = pos; f->st.v = f->st.a = f->st.j = 0; }
/* distance travelled while bringing (v, a) to rest with jerk-limited braking (assumes v >= 0 after the a-ramp; sign handled by the caller) */
/* Online jerk-limited follower. Position loop -> desired velocity (square-root law = constant-deceleration approach, linear near the
   target so it settles without chatter); velocity loop -> acceleration target a = sat(sqrt(2*J*|dv|)) which lets a reach 0 exactly when
   v reaches v_des; jerk is then slew-limited to +-J. No iteration, constant time per call (suitable for the MCU control ISR). */
void kn_follow_step(kn_follow_t *f, double target, double dt) {
    kn_state_t *st = &f->st; const kn_limits_t *L = &f->L; double J = L->jmax, A = L->amax, V = L->vmax;
    double err = target - st->s, e = fabs(err), dir = err >= 0 ? 1.0 : -1.0;
    double Ad = 0.6 * A;                                                                    /* braking margin: jerk lag and discretisation */
    double e_eff = e - 0.5 * fabs(st->v) * (Ad / J);                                          /* compensate the jerk ramp-in of the deceleration */
    double v_sqrt = e_eff > 0 ? sqrt(2 * Ad * e_eff) : 0.0, K = 0.5 * sqrt(J / V) * 4.0, v_lin = K * e;
    double v_des = v_sqrt < v_lin ? v_sqrt : v_lin; if (v_des > V) v_des = V; v_des *= dir;
    double dv = v_des - st->v, a_t = sqrt(2 * J * fabs(dv)); if (a_t > A) a_t = A; a_t = dv >= 0 ? a_t : -a_t;
    double a_t_lim = fabs(dv) / dt; if (fabs(a_t) > a_t_lim) a_t = dv >= 0 ? a_t_lim : -a_t_lim;      /* do not overshoot v_des inside one step */
    double j = (a_t - st->a) / dt; if (j > J) j = J; if (j < -J) j = -J;
    double aN = st->a + j * dt; if (aN > A) aN = A; if (aN < -A) aN = -A;
    double vN = st->v + 0.5 * (st->a + aN) * dt; if (vN > V) vN = V; if (vN < -V) vN = -V;
    st->s += 0.5 * (st->v + vN) * dt; st->v = vN; st->a = aN; st->j = j;
    if (fabs(target - st->s) < 1e-4 && fabs(st->v) < 1e-2 && fabs(st->a) < 1.0) { st->s = target; st->v = st->a = st->j = 0; }   /* settled */
}
/* ------------------------------ protocol ------------------------------ */
uint8_t kn_crc8(const char *s, int n) { uint8_t c = 0; for (int i = 0; i < n; i++) { c ^= (uint8_t)s[i]; for (int b = 0; b < 8; b++) c = (c & 0x80) ? (uint8_t)((c << 1) ^ 0x07) : (uint8_t)(c << 1); } return c; }
kn_cmd_t kn_parse(const char *line) {
    kn_cmd_t c; memset(&c, 0, sizeof c); c.kind = KN_CMD_NONE; c.err = "";
    while (*line == ' ') line++;
    if (!*line || *line == '\n' || *line == '\r') return c;
    const char *star = strrchr(line, '*');
    if (star) {                                                                                  /* checksum present: must match */
        unsigned want = 0; if (sscanf(star + 1, "%x", &want) != 1 || want != kn_crc8(line, (int)(star - line))) { c.kind = KN_CMD_BAD; c.err = "checksum"; return c; }
    }
    char buf[96]; size_t n = star ? (size_t)(star - line) : strcspn(line, "\r\n"); if (n >= sizeof buf) { c.kind = KN_CMD_BAD; c.err = "too long"; return c; }
    memcpy(buf, line, n); buf[n] = 0; char *save = 0, *tok = strtok_r(buf, " ", &save);
    if (!tok) return c;
    if (!strcmp(tok, "MOVE")) c.kind = KN_CMD_MOVE; else if (!strcmp(tok, "HOME")) c.kind = KN_CMD_HOME; else if (!strcmp(tok, "STOP")) c.kind = KN_CMD_STOP; else if (!strcmp(tok, "LIMITS")) c.kind = KN_CMD_LIMITS; else { c.kind = KN_CMD_BAD; c.err = "unknown command"; return c; }
    while ((tok = strtok_r(NULL, " ", &save))) {
        char *eq = strchr(tok, '='); if (!eq || eq == tok || eq[1] == 0) { c.kind = KN_CMD_BAD; c.err = "bad argument"; return c; }
        char key = tok[0]; char *end; double v = strtod(eq + 1, &end); if (*end) { c.kind = KN_CMD_BAD; c.err = "bad number"; return c; }
        if (key >= 'X' && key <= 'Z' && eq == tok + 1) { int ax = key - 'X'; c.has[ax] = true; c.pos[ax] = (int32_t)llround(v); }
        else if (key == 'F') c.feed = v; else if (key == 'A') c.accel = v; else if (key == 'J') c.jerk = v; else { c.kind = KN_CMD_BAD; c.err = "unknown key"; return c; }
    }
    if (c.kind == KN_CMD_MOVE && !(c.has[0] || c.has[1] || c.has[2])) { c.kind = KN_CMD_BAD; c.err = "MOVE needs an axis"; }
    if (c.kind == KN_CMD_MOVE && c.feed < 0) { c.kind = KN_CMD_BAD; c.err = "negative feed"; }
    return c;
}
