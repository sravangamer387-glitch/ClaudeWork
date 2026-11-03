/* TRISHNA measurement maths (pure functions, host-testable).
 *
 * EC CELL (bipolar ratiometric drive, see the controller schematic):
 *   phase A: GPIO25 high, GPIO26 low  -> V_A = Vdd (Rc + Rb) / Rt     (Rb: 100 R + GPIO26 sink resistance)
 *   phase B: GPIO25 low,  GPIO26 high -> V_B = Vdd (Rref + Ra) / Rt   (Ra: GPIO25 sink resistance)
 *   ratio q = V_A / V_B = (Rc + Rb) / (Rref + Ra)  ->  Rc = q (Rref + Ra) - Rb   (Vdd and the high-side drop cancel)
 *   conductivity sigma [S/cm] = K / Rc, K = cell constant [1/cm]; reported in mS/cm.
 *   Two-point calibration with KCl standards (1.413 mS/cm and 12.88 mS/cm at 25 degC) solves K and Rb with Rref + Ra fixed.
 *   Temperature compensation to 25 degC: EC25 = EC_T / (1 + alpha (T - 25)), alpha = 0.0191 /degC (KCl-like electrolytes).
 *
 * OPTICS (dark-subtracted photodiode voltages):
 *   absorbance A450 = log10( blank_blue / sample_blue )            (blank = rinse water in the same chamber, measured at the start of each event)
 *   turbidity index = sample (scatter_ir / tx_ir) - blank (scatter_ir / tx_ir)   (ratio method: cancels LED drift and window fouling to first order)
 *
 * SPECIFIC-GRAVITY / HYDRATION MODEL (a reagentless ESTIMATE, not a refractometer):
 *   SG_est = 1 + c_ec * EC25[mS/cm] + c_a450 * A450 + c0, clamped to 1.000..1.040.
 *   Defaults c_ec = 0.00085, c_a450 = 0.010, c0 = 0 come from typical adult urine (EC 5..35 mS/cm for SG 1.005..1.030);
 *   they MUST be refitted per user against a handheld urine refractometer (tools/trishna_fit_sg.py).
 *   Hydration class from SG_est (Armstrong-style bands): < 1.010 well hydrated, 1.010-1.020 adequate, 1.021-1.030 low, > 1.030 dehydrated. */
#ifndef TRISHNA_SENSE_H
#define TRISHNA_SENSE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float rref_ohm;      /* 330 R reference resistor (1 %) */
    float ra_ohm;        /* GPIO25 low-side resistance (about 25 R; part of the calibrated slope) */
    float rb_ohm;        /* 100 R + GPIO26 low-side resistance (fitted by calibration) */
    float k_cell;        /* cell constant [1/cm] (fitted by calibration; design value about 2.6) */
    float alpha_t;       /* temperature coefficient [1/degC] */
    float c_ec, c_a450, c0;   /* SG model */
    uint8_t calibrated;  /* 1 when k_cell/rb come from a 2-point calibration */
    uint8_t sg_fitted;   /* 1 when the SG model was fitted to refractometer readings */
} tr_cal_t;

void  tr_cal_defaults(tr_cal_t *c);

#define TR_EC_RATIO_MAX 400.0f     /* q above this is outside the cell's useful range (below about 0.02 mS/cm) */
float tr_ec_ratio(float v_a_mv, float v_b_mv);                 /* returns 1000 when V_B ~ 0 */
/* Chamber-empty check on the raw phase voltages: with air the cell is open, V_A sits at the rail and V_B near 0.
 * Tap water (0.1..1 mS/cm) gives V_B of about 40..400 mV, so the rinse reservoir must hold tap water, not RO/distilled water. */
int   tr_ec_is_air(float v_a_mv, float v_b_mv);
float tr_ec_cell_ohm(float ratio, const tr_cal_t *c);          /* <= 0 => invalid */
float tr_ec_mscm(float cell_ohm, const tr_cal_t *c);            /* conductivity at T, mS/cm (0 when invalid) */
float tr_ec_to25(float ec_mscm, float temp_c, const tr_cal_t *c);
/* Two-point calibration: standards s1, s2 [mS/cm at 25 degC], measured ratios q1, q2 at temperatures t1, t2. Returns 0 ok, -1 bad input. */
int   tr_ec_calibrate(tr_cal_t *c, float s1_25, float q1, float t1, float s2_25, float q2, float t2);

float tr_absorbance(float blank_mv, float sample_mv);           /* log10(blank/sample); 0 if invalid */
float tr_turbidity(float sc_mv, float tx_mv, float blank_sc_mv, float blank_tx_mv);

typedef enum { TR_HYD_UNKNOWN = 0, TR_HYD_WELL = 1, TR_HYD_ADEQUATE = 2, TR_HYD_LOW = 3, TR_HYD_DEHYDRATED = 4 } tr_hydration_t;
float tr_sg_estimate(float ec25_mscm, float a450, const tr_cal_t *c);
tr_hydration_t tr_hydration_class(float sg);

/* Sample-quality score 0..100 from the checks done during an event. */
typedef struct {
    uint8_t chamber_full;     /* EC cell not open */
    uint8_t ec_settled;       /* settle detector reached */
    uint8_t temp_ok;
    uint8_t optics_ok;        /* no saturation, blank usable */
    float   ec_sample, ec_blank;   /* mS/cm at 25 degC */
    uint8_t fallback_trigger;
} tr_quality_in_t;
uint8_t tr_quality(const tr_quality_in_t *q, uint8_t *diluted);

#ifdef __cplusplus
}
#endif
#endif
