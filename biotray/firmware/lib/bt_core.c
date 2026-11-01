#include <stdio.h>
#include <string.h>
#include <math.h>
#include "bt_core.h"
uint8_t bt_light_pwm(const bt_light_cfg_t *c, int m) {
    m = ((m % 1440) + 1440) % 1440; int len = (c->off_min - c->on_min + 1440) % 1440, t = (m - c->on_min + 1440) % 1440;
    if (len == 0 || t >= len) return 0;                                                   /* outside the photoperiod (len==0 means no light) */
    int r = c->ramp_min < 1 ? 1 : c->ramp_min; if (2 * r > len) r = len / 2; if (r < 1) r = 1;
    double f = 1.0; if (t < r) f = (double)(t + 1) / (r + 1); else if (len - 1 - t < r) f = (double)(len - t) / (r + 1);
    int v = (int)lround(f * c->max_pwm); return (uint8_t)(v > c->max_pwm ? c->max_pwm : v);
}
void bt_pump_init(bt_pump_t *p) { memset(p, 0, sizeof *p); p->since_start_s = 1 << 20; p->off_for_s = 1 << 20; }
void bt_pump_clear_fault(bt_pump_t *p) { p->fault_dry = false; }
bool bt_pump_step(bt_pump_t *p, const bt_pump_cfg_t *c, bool water, int dt) {
    if (p->fault_dry) { p->on = false; p->run_left_s = 0; return false; }
    if (p->on) {
        if (!water) { p->fault_dry = true; p->on = false; p->run_left_s = 0; p->off_for_s = 0; return false; }              /* never run dry */
        p->run_left_s -= dt; p->since_start_s += dt;
        if (p->run_left_s <= 0) { p->on = false; p->off_for_s = 0; }
        return p->on;
    }
    p->since_start_s += dt; if (p->off_for_s < (1 << 20)) p->off_for_s += dt;
    if (p->since_start_s >= c->period_s && p->off_for_s >= c->min_off_s && water) {
        int run = c->run_s < c->max_run_s ? c->run_s : c->max_run_s; if (run <= 0) return false;
        p->on = true; p->run_left_s = run; p->since_start_s = 0; }
    return p->on;
}
bool bt_fan(bool was_on, float t, float t_on, float t_off) { if (t >= t_on) return true; if (t <= t_off) return false; return was_on; }
float bt_cal_apply(const bt_cal2_t *c, float v) { float d = c->v2 - c->v1; if (fabsf(d) < 1e-6f) return c->p1; return c->p1 + (v - c->v1) * (c->p2 - c->p1) / d; }
float bt_ec_compensate(float ec, float t) { return ec / (1.0f + 0.02f * (t - 25.0f)); }
void bt_filter_init(bt_filter_t *f) { memset(f, 0, sizeof *f); }
float bt_filter_push(bt_filter_t *f, float x, float a) {
    f->buf[f->idx] = x; f->idx = (f->idx + 1) % 9; if (f->n < 9) f->n++;
    float s[9]; memcpy(s, f->buf, sizeof s); int n = f->n;
    for (int i = 1; i < n; i++) { float k = s[i]; int j = i - 1; while (j >= 0 && s[j] > k) { s[j + 1] = s[j]; j--; } s[j + 1] = k; }
    float med = (n & 1) ? s[n / 2] : 0.5f * (s[n / 2 - 1] + s[n / 2]);
    if (!f->have) { f->ema = med; f->have = true; } else f->ema += a * (med - f->ema);
    return f->ema;
}
int bt_json(char *o, int cap, const char *id, const bt_state_t *s) {
    int n = snprintf(o, (size_t)cap, "{\"tray\":\"%s\",\"temp_c\":%.1f,\"ph\":%.2f,\"ec_ms\":%.2f,\"lux\":%.0f,\"water\":%s,\"pump\":%s,\"fan\":%s,\"fault_dry\":%s,\"light_pwm\":%u,\"uptime_s\":%lu}",
        id, s->temp_c, s->ph, s->ec_ms, s->lux, s->water ? "true" : "false", s->pump_on ? "true" : "false", s->fan_on ? "true" : "false", s->fault_dry ? "true" : "false", (unsigned)s->light_pwm, (unsigned long)s->uptime_s);
    return (n < 0 || n >= cap) ? -1 : n;
}
