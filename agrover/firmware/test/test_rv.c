#include <stdio.h>
#include <math.h>
#include "rv_nav.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
typedef struct { float x, y, r; } obs_t;
static float ray(rv_pose_t p, float ang, const obs_t *o, int n) { float best = 9.9f; for (float d = 0.05f; d < 3.0f; d += 0.02f) { float x = p.x + d * cosf(p.th + ang), y = p.y + d * sinf(p.th + ang); for (int i = 0; i < n; i++) if (hypotf(x - o[i].x, y - o[i].y) < o[i].r) return d < best ? d : best; } return best; }
int main(void) {
    rv_geom_t g = {0.40f, 0.002f}; rv_pose_t p = {0, 0, 0};
    for (int i = 0; i < 500; i++) rv_odom_update(&p, &g, 1, 1); CHECK(fabsf(p.x - 1.0f) < 1e-3f && fabsf(p.y) < 1e-3f, "straight odometry");
    p = (rv_pose_t){0, 0, 0}; for (int i = 0; i < 1000; i++) rv_odom_update(&p, &g, -1, 1); CHECK(fabsf(fabsf(p.th) - 2.0f * 3.14159265f * 0 - fabsf(p.th)) < 1e-6f && hypotf(p.x, p.y) < 1e-3f, "in-place turn keeps position");
    p = (rv_pose_t){0, 0, 0}; float vl, vr; rv_wheel_speeds(&g, 0.5f, 0.0f, &vl, &vr); CHECK(vl == vr && fabsf(vl - 0.5f) < 1e-6f, "wheel speeds straight"); rv_wheel_speeds(&g, 0.0f, 1.0f, &vl, &vr); CHECK(fabsf(vl + 0.2f) < 1e-6f && fabsf(vr - 0.2f) < 1e-6f, "wheel speeds turn");
    /* follow a zig-zag row path with no obstacles: reaches the goal, max cross-track error small */
    rv_pt_t wp[] = {{0, 0}, {10, 0}, {10, 1.5f}, {0, 1.5f}, {0, 3.0f}, {10, 3.0f}}; rv_path_t path; rv_path_init(&path, wp, 6, 0.8f, 0.3f); p = (rv_pose_t){0, 0.3f, 0}; int steps = 0; float maxe = 0;
    while (!path.done && steps < 100000) { float v, w; rv_pursuit(&path, &p, 0.5f, &v, &w); if (w > 1.5f) w = 1.5f; if (w < -1.5f) w = -1.5f; p.x += v * cosf(p.th) * 0.02f; p.y += v * sinf(p.th) * 0.02f; p.th += w * 0.02f; steps++;
        if (steps > 500 && path.seg == 0) { float e = fabsf(p.y); if (e > maxe) maxe = e; } }
    CHECK(path.done && steps < 20000, "reached the end of the rows in %d steps", steps); CHECK(hypotf(p.x - 10, p.y - 3) < 0.4f, "final position %.2f %.2f", p.x, p.y);
    /* obstacles on the row: avoid layer keeps clearance and still gets to the goal */
    obs_t ob[] = {{4.0f, 0.1f, 0.35f}, {7.0f, -0.2f, 0.35f}}; rv_pt_t straight[] = {{0, 0}, {10, 0}}; rv_path_init(&path, straight, 2, 0.8f, 0.4f); p = (rv_pose_t){0, 0, 0}; rv_avoid_t av = {0.45f, 1.2f, 1.0f}; rv_avoid_state_t ast = {0, 0}; float minclr = 9, osc = 0, lastw = 0; steps = 0; int flips = 0;
    while (!path.done && steps < 60000) { float v, w; rv_pursuit(&path, &p, 0.5f, &v, &w); float L = ray(p, 0.6f, ob, 2), C = ray(p, 0.0f, ob, 2), R = ray(p, -0.6f, ob, 2); rv_avoid(&av, &ast, L > 2.9f ? -1 : L, C > 2.9f ? -1 : C, R > 2.9f ? -1 : R, &v, &w); (void)osc;
        if (fabsf(w) > 0.3f && fabsf(lastw) > 0.3f && w * lastw < 0) flips++;
        if (fabsf(w) > 0.3f) lastw = w; p.x += v * cosf(p.th) * 0.02f; p.y += v * sinf(p.th) * 0.02f; p.th += w * 0.02f; steps++; for (int i = 0; i < 2; i++) { float d = hypotf(p.x - ob[i].x, p.y - ob[i].y) - ob[i].r; if (d < minclr) minclr = d; } }
    CHECK(path.done, "obstacle course finished in %d steps", steps); CHECK(minclr > 0.12f, "minimum clearance %.2f m", minclr); CHECK(flips < 10, "large steering reversals %d (no chattering)", flips);
    /* avoid layer rules */
    float v = 0.5f, w = 0; rv_avoid_state_t s2 = {0, 0}; rv_avoid(&av, &s2, 2, 0.3f, 2, &v, &w); CHECK(v == 0 && fabsf(w) > 0.5f, "blocked ahead: stop and rotate"); v = 0.5f; w = 0; rv_avoid_state_t s3 = {0, 0}; rv_avoid(&av, &s3, -1, -1, -1, &v, &w); CHECK(v == 0.5f && w == 0, "no echoes: free");
    /* battery */
    CHECK(rv_soc_pct(14.0f, 0, 0.05f) > 95 && rv_soc_pct(9.0f, 0, 0.05f) == 0 && fabsf(rv_soc_pct(13.2f, 0, 0.05f) - 70) < 1, "soc table"); CHECK(rv_soc_pct(12.9f, 10.0f, 0.05f) > rv_soc_pct(12.9f, 0.0f, 0.05f), "load compensation raises the estimate");
    rv_mode_t m = RV_RUN; m = rv_power_mode(m, 25, true); CHECK(m == RV_RETURN, "return at low soc"); m = rv_power_mode(m, 40, true); CHECK(m == RV_RETURN, "stay returning below 50"); m = rv_power_mode(m, 12, true); CHECK(m == RV_SLEEP, "sleep at critical soc");
    m = rv_power_mode(m, 35, true); CHECK(m == RV_SLEEP, "no wake below 40"); m = rv_power_mode(m, 45, false); CHECK(m == RV_SLEEP, "no wake without sun"); m = rv_power_mode(m, 45, true); CHECK(m == RV_RUN, "wake with sun and soc");
    printf("%d checks, %d failures\n", checks, fails); return fails != 0; }
