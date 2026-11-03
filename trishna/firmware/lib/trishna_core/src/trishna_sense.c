#include "trishna_sense.h"
#include <math.h>

void tr_cal_defaults(tr_cal_t *c) {
    c->rref_ohm = 330.0f; c->ra_ohm = 25.0f; c->rb_ohm = 125.0f; c->k_cell = 2.6f; c->alpha_t = 0.0191f;
    c->c_ec = 0.00085f; c->c_a450 = 0.010f; c->c0 = 0.0f; c->calibrated = 0; c->sg_fitted = 0;
}

float tr_ec_ratio(float v_a_mv, float v_b_mv) {
    if (v_b_mv < 1.0f) return 1000.0f;            /* no current in phase B: open cell */
    return v_a_mv / v_b_mv;
}
int tr_ec_is_air(float v_a_mv, float v_b_mv) { return v_b_mv < 25.0f && v_a_mv > 2800.0f; }
float tr_ec_cell_ohm(float ratio, const tr_cal_t *c) {
    if (ratio >= TR_EC_RATIO_MAX) return -1.0f;
    return ratio * (c->rref_ohm + c->ra_ohm) - c->rb_ohm;
}
float tr_ec_mscm(float cell_ohm, const tr_cal_t *c) {
    if (cell_ohm <= 1.0f) return 0.0f;
    return 1000.0f * c->k_cell / cell_ohm;
}
float tr_ec_to25(float ec, float t, const tr_cal_t *c) {
    if (!(t > -20.0f && t < 80.0f)) return ec;      /* no valid temperature: report uncompensated */
    float d = 1.0f + c->alpha_t * (t - 25.0f);
    return d > 0.1f ? ec / d : ec;
}
int tr_ec_calibrate(tr_cal_t *c, float s1, float q1, float t1, float s2, float q2, float t2) {
    /* convert the 25 degC standard values to the conductivity actually present at the measurement temperature */
    float g1 = s1 * (1.0f + c->alpha_t * (t1 - 25.0f)) / 1000.0f;   /* S/cm */
    float g2 = s2 * (1.0f + c->alpha_t * (t2 - 25.0f)) / 1000.0f;
    float a = c->rref_ohm + c->ra_ohm;
    if (!(g1 > 0 && g2 > 0) || fabsf(g1 - g2) < 1e-6f || q1 >= TR_EC_RATIO_MAX || q2 >= TR_EC_RATIO_MAX || q1 <= 0 || q2 <= 0) return -1;
    /* g_i (a q_i - rb) = K for both standards -> rb = a (g1 q1 - g2 q2) / (g1 - g2) */
    float rb = a * (g1 * q1 - g2 * q2) / (g1 - g2);
    float k = g1 * (a * q1 - rb);
    if (!(k > 0.05f && k < 50.0f) || !(rb > -50.0f && rb < 2000.0f)) return -1;
    c->rb_ohm = rb; c->k_cell = k; c->calibrated = 1;
    return 0;
}

float tr_absorbance(float blank_mv, float sample_mv) {
    if (blank_mv < 5.0f || sample_mv < 0.5f) return 0.0f;
    return log10f(blank_mv / sample_mv);
}
float tr_turbidity(float sc, float tx, float bsc, float btx) {
    if (tx < 5.0f || btx < 5.0f) return 0.0f;
    float t = sc / tx - bsc / btx;
    return t < 0.0f ? 0.0f : t;
}

float tr_sg_estimate(float ec25, float a450, const tr_cal_t *c) {
    if (ec25 <= 0.0f) return 0.0f;
    float sg = 1.0f + c->c_ec * ec25 + c->c_a450 * a450 + c->c0;
    if (sg < 1.000f) sg = 1.000f;
    if (sg > 1.040f) sg = 1.040f;
    return sg;
}
tr_hydration_t tr_hydration_class(float sg) {
    if (sg < 1.0f) return TR_HYD_UNKNOWN;
    if (sg < 1.0100f) return TR_HYD_WELL;
    if (sg <= 1.0200f) return TR_HYD_ADEQUATE;
    if (sg <= 1.0300f) return TR_HYD_LOW;
    return TR_HYD_DEHYDRATED;
}

uint8_t tr_quality(const tr_quality_in_t *q, uint8_t *diluted) {
    int s = 100;
    *diluted = 0;
    if (!q->chamber_full) return 0;
    if (!q->ec_settled) s -= 25;
    if (!q->temp_ok) s -= 15;
    if (!q->optics_ok) s -= 15;
    if (q->fallback_trigger) s -= 10;
    /* rinse water is about 0.2..1 mS/cm, urine 5..40 mS/cm: a sample under 3x the blank (or under 2 mS/cm) is mostly flush/rinse water */
    if (q->ec_sample < 2.0f || q->ec_sample < 3.0f * q->ec_blank) { *diluted = 1; s -= 40; }
    return (uint8_t)(s < 0 ? 0 : s);
}
