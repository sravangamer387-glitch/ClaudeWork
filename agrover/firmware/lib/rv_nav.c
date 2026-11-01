#include <math.h>
#include "rv_nav.h"
static float wrap(float a) { while (a > (float)M_PI) a -= 2 * (float)M_PI; while (a < -(float)M_PI) a += 2 * (float)M_PI; return a; }
void rv_odom_update(rv_pose_t *p, const rv_geom_t *g, int dl, int dr) {
    float sl = dl * g->dist_per_tick_m, sr = dr * g->dist_per_tick_m, s = 0.5f * (sl + sr), dth = (sr - sl) / g->track_m; float mid = p->th + 0.5f * dth;
    p->x += s * cosf(mid); p->y += s * sinf(mid); p->th = wrap(p->th + dth); }
void rv_wheel_speeds(const rv_geom_t *g, float v, float w, float *vl, float *vr) { *vl = v - 0.5f * g->track_m * w; *vr = v + 0.5f * g->track_m * w; }
void rv_path_init(rv_path_t *p, const rv_pt_t *wp, int n, float L, float tol) { p->wp = wp; p->n = n; p->seg = 0; p->lookahead_m = L; p->goal_tol_m = tol; p->done = n < 2; }
void rv_pursuit(rv_path_t *p, const rv_pose_t *pose, float v_cmd, float *v, float *w) {
    *v = 0; *w = 0; if (p->done) return;
    float gx = p->wp[p->n - 1].x - pose->x, gy = p->wp[p->n - 1].y - pose->y; if (hypotf(gx, gy) < p->goal_tol_m) { p->done = true; return; }
    while (p->seg < p->n - 2) {                                                                  /* advance to the next segment when the pose has passed the end of this one */
        float ax = p->wp[p->seg].x, ay = p->wp[p->seg].y, bx = p->wp[p->seg + 1].x, by = p->wp[p->seg + 1].y, dx = bx - ax, dy = by - ay, t = ((pose->x - ax) * dx + (pose->y - ay) * dy) / (dx * dx + dy * dy);
        if (t > 1.0f) p->seg++; else break; }
    float tx = p->wp[p->n - 1].x, ty = p->wp[p->n - 1].y;                                          /* look-ahead point: walk along the polyline from the closest point */
    float ax = p->wp[p->seg].x, ay = p->wp[p->seg].y, bx = p->wp[p->seg + 1].x, by = p->wp[p->seg + 1].y, dx = bx - ax, dy = by - ay, len = hypotf(dx, dy);
    float t = ((pose->x - ax) * dx + (pose->y - ay) * dy) / (len * len); if (t < 0) t = 0; float remain = p->lookahead_m, px = ax + t * dx, py = ay + t * dy; int sg = p->seg;
    for (;;) { float ex = p->wp[sg + 1].x, ey = p->wp[sg + 1].y, d = hypotf(ex - px, ey - py); if (d >= remain || sg >= p->n - 2) { float f = d > 1e-6f ? (remain < d ? remain / d : 1.0f) : 0; tx = px + (ex - px) * f; ty = py + (ey - py) * f; break; } remain -= d; px = ex; py = ey; sg++; }
    float ang = wrap(atan2f(ty - pose->y, tx - pose->x) - pose->th), ld = hypotf(tx - pose->x, ty - pose->y); if (ld < 1e-3f) ld = 1e-3f;
    float k = 2.0f * sinf(ang) / ld; float vs = v_cmd; if (fabsf(ang) > 1.2f) vs = 0.0f;                  /* facing far from the target: turn in place */
    *v = vs; *w = (vs > 0) ? vs * k : (ang > 0 ? 0.8f : -0.8f); }
void rv_avoid(const rv_avoid_t *a, rv_avoid_state_t *st, float l, float c, float r, float *v, float *w) {
    float L = l > 0 ? l : 9.9f, C = c > 0 ? c : 9.9f, R = r > 0 ? r : 9.9f, m = fminf(C, fminf(L, R));
    if (m >= a->slow_m) {                                                                                    /* nothing in range: keep gently moving away for 60 calls, then forget the evasion side */
        if (st->dir != 0) { if (++st->clear_count > 60) st->dir = 0; else { float k = 1.0f - (float)st->clear_count / 60.0f; *v *= 0.6f; *w = *w * (1.0f - 0.7f * k) + st->dir * a->turn_rate * 0.3f * k; } }
        return; }
    st->clear_count = 0; if (st->dir == 0) st->dir = (L >= R) ? 1.0f : -1.0f;                                  /* +w turns left; commit to the more open side and keep it (no left-right chatter) */
    if (C <= a->stop_m) { *v = 0; *w = st->dir * a->turn_rate; return; }
    float f = (m - a->stop_m) / (a->slow_m - a->stop_m); if (f < 0) f = 0; *v *= f; *w = *w * f + st->dir * a->turn_rate * (1.0f - m / a->slow_m); }          /* the path command fades out near the obstacle: no cancellation deadlock */
float rv_soc_pct(float v, float load_a, float r) {
    static const float tv[] = {10.0f, 12.0f, 12.8f, 13.0f, 13.2f, 13.3f, 13.4f, 14.4f}, ts[] = {0, 10, 30, 50, 70, 80, 90, 100};       /* 4S LiFePO4 open-circuit curve (typical, flat middle) */
    float oc = v + load_a * r; if (oc <= tv[0]) return 0; for (int i = 1; i < 8; i++) if (oc <= tv[i]) return ts[i - 1] + (ts[i] - ts[i - 1]) * (oc - tv[i - 1]) / (tv[i] - tv[i - 1]); return 100; }
rv_mode_t rv_power_mode(rv_mode_t m, float soc, bool sun) {
    if (m == RV_RUN) { if (soc < 15) return RV_SLEEP; if (soc < 30) return RV_RETURN; return RV_RUN; }
    if (m == RV_RETURN) { if (soc < 15) return RV_SLEEP; if (soc > 50 && sun) return RV_RUN; return RV_RETURN; }
    if (soc > 40 && sun) return RV_RUN; return RV_SLEEP; }                                         /* sleep until 40 % and sunlight: hysteresis avoids chattering */
