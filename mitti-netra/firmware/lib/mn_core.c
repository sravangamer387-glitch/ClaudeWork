#include <math.h>
#include <string.h>
#include "mn_core.h"
float mn_soil_pct(const mn_soil_cal_t *c, int raw) {
    if (c->dry_raw == c->wet_raw) return 0;
    float p = 100.0f * (float)(c->dry_raw - raw) / (float)(c->dry_raw - c->wet_raw);
    return p < 0 ? 0 : (p > 100 ? 100 : p); }
void mn_tilt_deg(float ax, float ay, float az, float *roll, float *pitch) {
    *roll = atan2f(ay, az) * 57.2957795f; *pitch = atan2f(-ax, sqrtf(ay * ay + az * az)) * 57.2957795f; }
float mn_hx711_volts(const mn_strain_cfg_t *c, int32_t raw) { return (float)raw * (0.5f * c->avdd / c->gain) / 8388608.0f; }
float mn_microstrain(const mn_strain_cfg_t *c, int32_t raw, int32_t zero) {
    float v = mn_hx711_volts(c, raw - zero);
    return 1e6f * c->bridge_k * v / (c->vex * c->gauge_factor); }          /* eps = k * Vout / (Vex * GF) */
void mn_alarm_init(mn_alarm_t *a) { a->level = MN_OK; a->up_count = 0; }
mn_level_t mn_alarm_update(mn_alarm_t *a, const mn_thresh_t *t, float m) {
    m = fabsf(m);
    mn_level_t want = m >= t->alarm ? MN_ALARM : (m >= t->watch ? MN_WATCH : MN_OK);
    if (want > a->level) { if (++a->up_count >= t->debounce) { a->level = want; a->up_count = 0; } }                  /* rising: needs 'debounce' consecutive readings */
    else { a->up_count = 0;
        if (a->level == MN_ALARM && m < t->alarm - t->hyst) a->level = (m >= t->watch) ? MN_WATCH : MN_OK;              /* falling: hysteresis */
        else if (a->level == MN_WATCH && m < t->watch - t->hyst) a->level = MN_OK; }
    return a->level; }
int mn_next_interval_s(mn_level_t w, float vb, bool rain) {
    int s = 6 * 3600;
    if (rain) s = 3600;
    if (w == MN_WATCH) s = 1800;
    if (w == MN_ALARM) s = 600;
    if (vb < 3.55f && w != MN_ALARM) s *= 4;                                          /* protect a low battery, never throttle an alarm */
    return s; }
uint16_t mn_crc16(const uint8_t *p, int n) { uint16_t c = 0xFFFF; for (int i = 0; i < n; i++) { c ^= (uint16_t)p[i] << 8; for (int b = 0; b < 8; b++) c = (c & 0x8000) ? (uint16_t)((c << 1) ^ 0x1021) : (uint16_t)(c << 1); } return c; }
static void p16(uint8_t *o, int *i, uint16_t v) { o[(*i)++] = (uint8_t)(v >> 8); o[(*i)++] = (uint8_t)v; }
static void p32(uint8_t *o, int *i, uint32_t v) { p16(o, i, (uint16_t)(v >> 16)); p16(o, i, (uint16_t)v); }
static uint16_t g16(const uint8_t *in, int *i) { uint16_t v = (uint16_t)(in[*i] << 8 | in[*i + 1]); *i += 2; return v; }
static uint32_t g32(const uint8_t *in, int *i) { uint32_t h = g16(in, i), l = g16(in, i); return h << 16 | l; }
int mn_pack(const mn_report_t *r, uint8_t o[MN_FRAME_LEN]) {
    int i = 0;
    o[i++] = 0xA5; o[i++] = 1; p16(o, &i, r->node_id); p32(o, &i, r->unix_time); p16(o, &i, (uint16_t)r->soil_pct_x10); p16(o, &i, (uint16_t)r->temp_c_x10); p16(o, &i, (uint16_t)r->roll_x100); p16(o, &i, (uint16_t)r->pitch_x100);
    p32(o, &i, (uint32_t)r->microstrain); p16(o, &i, r->battery_mv); o[i++] = r->level; o[i++] = r->flags; p16(o, &i, mn_crc16(o, i)); return i; }
bool mn_unpack(const uint8_t in[MN_FRAME_LEN], mn_report_t *r) {
    if (in[0] != 0xA5 || in[1] != 1) return false;
    if (mn_crc16(in, MN_FRAME_LEN - 2) != (uint16_t)(in[MN_FRAME_LEN - 2] << 8 | in[MN_FRAME_LEN - 1])) return false;
    int i = 2; r->node_id = g16(in, &i); r->unix_time = g32(in, &i); r->soil_pct_x10 = (int16_t)g16(in, &i); r->temp_c_x10 = (int16_t)g16(in, &i); r->roll_x100 = (int16_t)g16(in, &i); r->pitch_x100 = (int16_t)g16(in, &i);
    r->microstrain = (int32_t)g32(in, &i); r->battery_mv = g16(in, &i); r->level = in[i++]; r->flags = in[i++]; return true; }
