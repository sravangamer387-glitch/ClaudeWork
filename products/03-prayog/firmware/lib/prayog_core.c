#include "prayog_core.h"
#include <math.h>
#include <string.h>

static float clampf(float v, float lo, float hi) { return v < lo ? lo : (v > hi ? hi : v); }
static float r_from_adc_top(uint16_t adc, float r_fixed) {          /* sensor on top, fixed resistor to GND */
    float a = clampf((float)adc, 1.0f, ADC_MAX - 1.0f);
    return r_fixed * (ADC_MAX / a - 1.0f);
}

float conv_ntc_c(uint16_t adc) {
    const float R0 = 10000.0f, B = 3950.0f, T0 = 298.15f;
    float r = r_from_adc_top(adc, 10000.0f);
    return 1.0f / (1.0f / T0 + logf(r / R0) / B) - 273.15f;
}
float conv_ldr_lux(uint16_t adc) {
    float r = r_from_adc_top(adc, 10000.0f);                         /* LDR resistance */
    return 10.0f * powf(15000.0f / r, 1.43f);                        /* typical: 15 kOhm at 10 lux, gamma 0.7 */
}
float conv_hall_mt(uint16_t adc) {
    float v = (float)adc * 5.0f / ADC_MAX;
    float gauss = (v - 2.5f) / 0.0014f;                                 /* 1.4 mV per gauss */
    return gauss * 0.1f;                                                /* 10 gauss = 1 mT */
}
float conv_volt(uint16_t adc, float divider) { return (float)adc * 5.0f / ADC_MAX * divider; }
float conv_soil_pct(uint16_t adc, uint16_t dry, uint16_t wet) {
    if (dry == wet) return 0.0f;
    return clampf(100.0f * ((float)dry - (float)adc) / ((float)dry - (float)wet), 0.0f, 100.0f);   /* capacitive: wetter -> lower counts */
}
float conv_mic_level(const uint16_t *s, uint16_t n) {
    uint32_t sum = 0; uint16_t i; float mean, acc = 0;
    if (!n) return 0.0f;
    for (i = 0; i < n; i++) sum += s[i];
    mean = (float)sum / (float)n;
    for (i = 0; i < n; i++) acc += fabsf((float)s[i] - mean);
    return acc / (float)n;
}
float conv_generic(sensor_t s, uint16_t adc) {
    switch (s) {
    case S_NTC: return conv_ntc_c(adc);
    case S_LDR: return conv_ldr_lux(adc);
    case S_HALL: return conv_hall_mt(adc);
    case S_VOLT: return conv_volt(adc, 3.0f);                          /* default probe divider 3:1 -> 0..15 V */
    case S_SOIL: return conv_soil_pct(adc, 620, 300);
    default: return (float)adc;
    }
}
static const char *NAMES[S_COUNT] = {"NONE", "NTC", "LDR", "MIC", "HALL", "SOIL", "VOLT", "IR", "COND"};
static const char *UNITS[S_COUNT] = {"", "C", "lux", "counts", "mT", "%", "V", "counts", "counts"};
const char *sensor_name(sensor_t s) { return s < S_COUNT ? NAMES[s] : "?"; }
const char *sensor_unit(sensor_t s) { return s < S_COUNT ? UNITS[s] : ""; }

float speed_of_sound_ms(float t) { return 331.3f + 0.606f * t; }
float echo_to_cm(uint32_t us, float t) { return (float)us * 0.5f * speed_of_sound_ms(t) / 10000.0f; }

void gate_init(gate_t *g) { memset(g, 0, sizeof *g); }
void gate_push(gate_t *g, uint32_t t, uint8_t lv) {
    if (g->n == GATE_MAX) { memmove(g->t, g->t + 1, (GATE_MAX - 1) * sizeof g->t[0]); memmove(g->level, g->level + 1, GATE_MAX - 1); g->n--; }
    g->t[g->n] = t; g->level[g->n] = lv; g->n++;
}
bool gate_period_s(const gate_t *g, float *period) {
    uint32_t first = 0, last = 0; uint8_t count = 0, i;
    for (i = 0; i < g->n; i++) if (g->level[i] == 1) { if (!count) first = g->t[i]; last = g->t[i]; count++; }
    if (count < 2) return false;
    *period = (float)(last - first) / 1e6f / (float)(count - 1);
    return true;
}
bool gate_transit_s(const gate_t *g, float *dt) {
    uint8_t i;
    for (i = 0; i + 1 < g->n; i++) if (g->level[i] == 1 && g->level[i + 1] == 0) { *dt = (float)(g->t[i + 1] - g->t[i]) / 1e6f; return true; }
    return false;
}
float speed_from_transit(float w, float dt) { return dt > 0 ? w / dt : 0.0f; }

stats_t stats_of(const float *x, uint16_t n) {
    stats_t s = {0, 0, n}; uint16_t i; float acc = 0;
    if (!n) return s;
    for (i = 0; i < n; i++) s.mean += x[i];
    s.mean /= (float)n;
    for (i = 0; i < n; i++) acc += (x[i] - s.mean) * (x[i] - s.mean);
    s.sd = n > 1 ? sqrtf(acc / (float)(n - 1)) : 0.0f;
    return s;
}
float median5(const float *x) {
    float a[5]; int i, j;
    for (i = 0; i < 5; i++) a[i] = x[i];
    for (i = 1; i < 5; i++) { float v = a[i]; for (j = i - 1; j >= 0 && a[j] > v; j--) a[j + 1] = a[j]; a[j + 1] = v; }
    return a[2];
}
int parse_set(const char *line, uint8_t *ch, sensor_t *out) {
    const char *p = line; int i, k;
    if (strncmp(p, "SET ", 4) != 0) return -1;
    p += 4;
    if (*p < '0' || *p > '7') return -1;
    *ch = (uint8_t)(*p - '0'); p++;
    if (*p != ' ') return -1;
    p++;
    for (k = 0; k < (int)S_COUNT; k++) {
        const char *n = NAMES[k]; i = 0;
        while (n[i] && p[i] == n[i]) i++;
        if (!n[i] && (p[i] == '\0' || p[i] == '\n' || p[i] == '\r')) { *out = (sensor_t)k; return 0; }
    }
    return -1;
}
