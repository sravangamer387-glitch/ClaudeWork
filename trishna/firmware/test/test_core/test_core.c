/* Host unit tests for the TRISHNA core library (Unity API).
 * PlatformIO: pio test -e native        Plain gcc (no PlatformIO): make -C test/host
 * The host build also writes test/host/golden_frames.bin, which tools/test_bridge.py decodes to prove the Python bridge matches the C layout. */
#include <unity.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include "trishna_frame.h"
#include "trishna_filters.h"
#include "trishna_sense.h"
#include "trishna_fsm.h"

void setUp(void) {}
void tearDown(void) {}

/* ------------------------------------------------------------------ frame */
static void test_frame_size_and_crc_vector(void) {
    TEST_ASSERT_EQUAL_INT(48, (int)sizeof(tr_frame_t));
    TEST_ASSERT_EQUAL_HEX16(0x29B1, tr_crc16((const uint8_t *)"123456789", 9));   /* CRC-16/CCITT-FALSE check value */
}
static tr_frame_t sample_frame(void) {
    tr_frame_t f; memset(&f, 0, sizeof f);
    f.type = TR_FT_RESULT; f.seq = 513; f.unix_s = 1793664000u; f.ms = 250; f.uptime_s = 3600; f.state = STATE_ANALYSIS; f.prev_state = STATE_SAMPLING;
    f.event_id = 42; f.flags = TR_FLAG_TIME_VALID | TR_FLAG_STREAM | TR_FLAG_TEMP_OK; f.error_code = 0; f.temp_cx100 = 3412; f.ec25_x100 = 1873;
    f.cell_ohm = 151; f.sg_x10000 = 10171; f.a450_x1000 = -12; f.turb_x1000 = 37; f.tx_blue_mv = 1540; f.tx_ir_mv = 2011; f.sc_ir_mv = 88; f.vin_mv = 12040;
    f.hydration = TR_HYD_ADEQUATE; f.quality = 90;
    return f;
}
static void test_frame_roundtrip_and_corruption(void) {
    tr_frame_t f = sample_frame(), g; uint8_t b[48];
    tr_frame_seal(&f, b);
    TEST_ASSERT_EQUAL_HEX8(0xA5, b[0]); TEST_ASSERT_EQUAL_HEX8(0x5A, b[1]); TEST_ASSERT_EQUAL_UINT8(1, b[2]);
    TEST_ASSERT_EQUAL_UINT8(0x01, b[4]); TEST_ASSERT_EQUAL_UINT8(0x02, b[5]);            /* seq 513 little-endian */
    TEST_ASSERT_EQUAL_INT(0, tr_frame_parse(b, &g));
    TEST_ASSERT_EQUAL_UINT16(513, g.seq); TEST_ASSERT_EQUAL_UINT32(1793664000u, g.unix_s); TEST_ASSERT_EQUAL_INT16(3412, g.temp_cx100);
    TEST_ASSERT_EQUAL_INT16(-12, g.a450_x1000); TEST_ASSERT_EQUAL_UINT16(10171, g.sg_x10000); TEST_ASSERT_EQUAL_UINT8(90, g.quality);
    for (int i = 3; i < 46; i++) { uint8_t c[48]; memcpy(c, b, 48); c[i] ^= 0x10; TEST_ASSERT_EQUAL_INT(-2, tr_frame_parse(c, &g)); }
    b[0] = 0x00; TEST_ASSERT_EQUAL_INT(-1, tr_frame_parse(b, &g));
}
static void test_saturation(void) {
    TEST_ASSERT_EQUAL_UINT16(0, tr_u16_sat(-3.0f)); TEST_ASSERT_EQUAL_UINT16(65535, tr_u16_sat(1e9f)); TEST_ASSERT_EQUAL_UINT16(12, tr_u16_sat(11.6f));
    TEST_ASSERT_EQUAL_INT16(-32767, tr_i16_sat(-1e9f)); TEST_ASSERT_EQUAL_INT16(INT16_MIN, tr_i16_sat(NAN));
}

/* ------------------------------------------------------------------ filters */
static void test_moving_average(void) {
    tr_ma_t m; tr_ma_init(&m, 4);
    tr_ma_push(&m, 1); tr_ma_push(&m, 2); tr_ma_push(&m, 3);
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 2.0f, tr_ma_mean(&m));
    tr_ma_push(&m, 4); tr_ma_push(&m, 10);                 /* window now 2,3,4,10 */
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 4.75f, tr_ma_mean(&m));
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 3.5940f, tr_ma_std(&m));
    TEST_ASSERT_TRUE(tr_ma_full(&m));
}
static void test_ema_and_median(void) {
    tr_ema_t e; tr_ema_init(&e, tr_ema_alpha(0.1f, 0.5f));
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 0.18127f, e.alpha);
    float y = 0; for (int i = 0; i < 50; i++) y = tr_ema_push(&e, 1.0f);   /* 5 s of steps at tau 0.5 s */
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 1.0f, y);
    float v[5] = {5, 100, 4, 6, 5};
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 5.0f, tr_median5(v));
    float w[4] = {9, 1, 5, 3};
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 4.0f, tr_median_n(w, 4));
}
static void test_settle_detector_ignores_sloshing(void) {
    tr_settle_t s; tr_settle_init(&s, 8, 0.01f, 3);
    int settled_at = -1;
    for (int i = 0; i < 80; i++) {                           /* decaying oscillation (sloshing) around 1000 */
        float x = 1000.0f + 200.0f * expf(-i / 8.0f) * ((i & 1) ? 1.0f : -1.0f);
        if (tr_settle_push(&s, x) && settled_at < 0) settled_at = i;
    }
    TEST_ASSERT_TRUE(settled_at > 20);                      /* not while it is still moving */
    TEST_ASSERT_TRUE(settled_at < 60);
}

/* ------------------------------------------------------------------ EC */
static void ec_forward(float rc, float *va, float *vb) {     /* electrical model of the board: 25 R GPIO sinks/sources, 330 R ref, 100 R on E2 */
    float rt = 25 + 330 + rc + 100 + 25;
    *va = 3300.0f * (rc + 125.0f) / rt;
    *vb = 3300.0f * (330.0f + 25.0f) / rt;
}
static void test_ec_recovers_conductivity(void) {
    tr_cal_t c; tr_cal_defaults(&c);
    float sig[] = {1.413f, 5.0f, 12.88f, 20.0f, 35.0f};
    for (int i = 0; i < 5; i++) {
        float rc = 1000.0f * c.k_cell / sig[i], va, vb;
        ec_forward(rc, &va, &vb);
        float ec = tr_ec_mscm(tr_ec_cell_ohm(tr_ec_ratio(va, vb), &c), &c);
        TEST_ASSERT_FLOAT_WITHIN(sig[i] * 0.005f, sig[i], ec);
    }
}
static void test_ec_two_point_calibration(void) {
    tr_cal_t c; tr_cal_defaults(&c);
    float k_true = 3.1f, va, vb;                               /* the real cell differs from the design value */
    /* standards at 22 degC: conductivity present = s25 (1 + 0.0191 (22 - 25)) */
    float g1 = 1.413f * (1 + 0.0191f * (22 - 25)), g2 = 12.88f * (1 + 0.0191f * (22 - 25));
    ec_forward(1000.0f * k_true / g1, &va, &vb); float q1 = tr_ec_ratio(va, vb);
    ec_forward(1000.0f * k_true / g2, &va, &vb); float q2 = tr_ec_ratio(va, vb);
    TEST_ASSERT_EQUAL_INT(0, tr_ec_calibrate(&c, 1.413f, q1, 22.0f, 12.88f, q2, 22.0f));
    TEST_ASSERT_FLOAT_WITHIN(0.01f, k_true, c.k_cell);
    TEST_ASSERT_FLOAT_WITHIN(1.0f, 125.0f, c.rb_ohm);
    ec_forward(1000.0f * k_true / 18.0f, &va, &vb);
    TEST_ASSERT_FLOAT_WITHIN(0.05f, 18.0f, tr_ec_mscm(tr_ec_cell_ohm(tr_ec_ratio(va, vb), &c), &c));
    TEST_ASSERT_EQUAL_INT(-1, tr_ec_calibrate(&c, 1.413f, q1, 22.0f, 1.413f, q1, 22.0f));   /* identical points rejected */
}
static void test_ec_temperature_and_air(void) {
    tr_cal_t c; tr_cal_defaults(&c);
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 10.0f, tr_ec_to25(10.0f * (1 + 0.0191f * 10), 35.0f, &c));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 7.0f, tr_ec_to25(7.0f, -100.0f, &c));       /* no temperature: unchanged */
    TEST_ASSERT_TRUE(tr_ec_is_air(3290.0f, 3.0f));
    float va, vb; ec_forward(1000.0f * 2.6f / 0.2f, &va, &vb);                  /* tap water 0.2 mS/cm must NOT look like air */
    TEST_ASSERT_FALSE(tr_ec_is_air(va, vb));
    TEST_ASSERT_TRUE(tr_ec_cell_ohm(1000.0f, &c) < 0);
}

/* ------------------------------------------------------------------ optics + model */
static void test_optics(void) {
    TEST_ASSERT_FLOAT_WITHIN(1e-3f, 0.30103f, tr_absorbance(2000.0f, 1000.0f));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 0.0f, tr_absorbance(2.0f, 1000.0f));
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 0.05f, tr_turbidity(150.0f, 1500.0f, 100.0f, 2000.0f));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 0.0f, tr_turbidity(10.0f, 2000.0f, 100.0f, 2000.0f));
}
static void test_sg_and_hydration(void) {
    tr_cal_t c; tr_cal_defaults(&c);
    float sg = tr_sg_estimate(20.0f, 0.2f, &c);
    TEST_ASSERT_FLOAT_WITHIN(1e-4f, 1.019f, sg);
    TEST_ASSERT_EQUAL_INT(TR_HYD_ADEQUATE, tr_hydration_class(sg));
    TEST_ASSERT_EQUAL_INT(TR_HYD_WELL, tr_hydration_class(1.005f));
    TEST_ASSERT_EQUAL_INT(TR_HYD_LOW, tr_hydration_class(1.025f));
    TEST_ASSERT_EQUAL_INT(TR_HYD_DEHYDRATED, tr_hydration_class(1.034f));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 1.040f, tr_sg_estimate(500.0f, 0, &c));
    TEST_ASSERT_FLOAT_WITHIN(1e-6f, 0.0f, tr_sg_estimate(0.0f, 0, &c));
}
static void test_quality_and_dilution(void) {
    tr_quality_in_t q = {1, 1, 1, 1, 18.0f, 0.4f, 0}; uint8_t d;
    TEST_ASSERT_EQUAL_UINT8(100, tr_quality(&q, &d)); TEST_ASSERT_EQUAL_UINT8(0, d);
    q.ec_sample = 1.0f; TEST_ASSERT_EQUAL_UINT8(60, tr_quality(&q, &d)); TEST_ASSERT_EQUAL_UINT8(1, d);
    q.chamber_full = 0; TEST_ASSERT_EQUAL_UINT8(0, tr_quality(&q, &d));
}

/* ------------------------------------------------------------------ state machine */
typedef struct { tr_fsm_t f; tr_inputs_t in; tr_outputs_t o; uint32_t t; tr_state_t seen[64]; int nseen; int req[4]; int errs[16]; } sim_t;
static void sim_init(sim_t *s, int presence_required) {
    memset(s, 0, sizeof *s); tr_fsm_cfg_t c; tr_fsm_cfg_defaults(&c); c.presence_required = (uint8_t)presence_required;
    tr_fsm_init(&s->f, &c, 7); s->t = 1000;
}
static void sim_run(sim_t *s, uint32_t ms) {                  /* 10 ms ticks, like the firmware */
    for (uint32_t k = 0; k < ms / 10; k++) {
        s->t += 10; tr_fsm_step(&s->f, s->t, &s->in, &s->o);
        if (s->o.state_changed && s->nseen < 64) s->seen[s->nseen++] = s->f.state;
        if (s->o.request) s->req[s->o.request]++;
        if (s->o.error) s->errs[s->o.error]++;
        s->in.analysis_done = 0; s->in.check_done = 0;          /* one-shot inputs */
        if (s->o.request == REQ_SAMPLE) s->in.analysis_done = 0;
    }
}
static void test_fsm_full_event_sequence(void) {
    sim_t s; sim_init(&s, 1);
    sim_run(&s, 500); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
    s.in.presence = 1; s.in.sump_liquid = 1; sim_run(&s, 1000);  TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
    s.in.stream = 1; sim_run(&s, 200); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);                 /* still debouncing */
    sim_run(&s, 200); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, s.f.state); TEST_ASSERT_EQUAL_INT(1, s.req[REQ_BLANK]);
    TEST_ASSERT_EQUAL_UINT16(8, s.f.event_id);
    sim_run(&s, 1900); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, s.f.state); TEST_ASSERT_EQUAL_INT(PUMP_OFF, s.o.pump);
    sim_run(&s, 200); TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state); TEST_ASSERT_EQUAL_INT(PUMP_FWD, s.o.pump); TEST_ASSERT_EQUAL_UINT8(0, s.o.valve);
    sim_run(&s, 5800); TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state);
    sim_run(&s, 300); TEST_ASSERT_EQUAL_INT(STATE_ANALYSIS, s.f.state); TEST_ASSERT_EQUAL_INT(PUMP_OFF, s.o.pump); TEST_ASSERT_EQUAL_INT(1, s.req[REQ_SAMPLE]);
    s.in.stream = 0; s.in.presence = 0;
    sim_run(&s, 3000); TEST_ASSERT_EQUAL_INT(STATE_ANALYSIS, s.f.state);
    s.in.analysis_done = 1; sim_run(&s, 10); TEST_ASSERT_EQUAL_INT(STATE_PURGE_CLEANING, s.f.state);
    sim_run(&s, 100); TEST_ASSERT_EQUAL_INT(PUMP_REV, s.o.pump); TEST_ASSERT_EQUAL_UINT8(1, s.o.valve);
    sim_run(&s, 8000); TEST_ASSERT_EQUAL_INT(PUMP_OFF, s.o.pump); TEST_ASSERT_EQUAL_UINT8(0, s.o.valve);      /* pause */
    sim_run(&s, 500); TEST_ASSERT_EQUAL_INT(PUMP_REV, s.o.pump); TEST_ASSERT_EQUAL_UINT8(1, s.o.valve);       /* second cycle */
    sim_run(&s, 8500); TEST_ASSERT_EQUAL_INT(1, s.req[REQ_PURGE_CHECK]); TEST_ASSERT_EQUAL_INT(STATE_PURGE_CLEANING, s.f.state);
    s.in.check_done = 1; s.in.check_air = 0; sim_run(&s, 10); TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state);
    s.in.presence = 1; s.in.stream = 1; sim_run(&s, 20000); TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state);  /* triggers ignored */
    s.in.presence = 0; s.in.stream = 0; sim_run(&s, 11000); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
    tr_state_t want[] = {STATE_STREAM_DETECTED, STATE_SAMPLING, STATE_ANALYSIS, STATE_PURGE_CLEANING, STATE_LOCKOUT, STATE_IDLE};
    TEST_ASSERT_EQUAL_INT(6, s.nseen);
    for (int i = 0; i < 6; i++) TEST_ASSERT_EQUAL_INT(want[i], s.seen[i]);
    TEST_ASSERT_EQUAL_INT(0, s.errs[ERR_PUMP_LIMIT]);
}
static void test_fsm_short_event_and_presence_gate(void) {
    sim_t s; sim_init(&s, 1);
    s.in.stream = 1; sim_run(&s, 1000); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);          /* flush water without a user: ignored */
    s.in.presence = 1; sim_run(&s, 100); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, s.f.state);
    s.in.stream = 0; sim_run(&s, 600); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state); TEST_ASSERT_EQUAL_INT(1, s.errs[ERR_SHORT_EVENT]);
    sim_t u; sim_init(&u, 0);                                  /* ToF missing: sump alone triggers */
    u.in.stream = 1; sim_run(&u, 400); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, u.f.state);
}
static void test_fsm_splash_does_not_abort(void) {
    sim_t s; sim_init(&s, 1);
    s.in.presence = 1; s.in.stream = 1; sim_run(&s, 400); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, s.f.state);
    s.in.stream = 0; sim_run(&s, 200); s.in.stream = 1; sim_run(&s, 2000);                 /* 200 ms dropout */
    TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state);
}
static void test_fsm_fallback_trigger(void) {
    sim_t s; sim_init(&s, 1);
    s.in.presence = 1; s.in.sump_liquid = 1; sim_run(&s, 3900); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
    sim_run(&s, 200); TEST_ASSERT_EQUAL_INT(STATE_STREAM_DETECTED, s.f.state); TEST_ASSERT_EQUAL_UINT8(1, s.f.fallback);
    sim_run(&s, 2100); TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state);                     /* no short-event abort in fallback mode */
}
static void test_fsm_leak_latches(void) {
    sim_t s; sim_init(&s, 0);
    s.in.stream = 1; sim_run(&s, 3000); TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state);
    s.in.leak = 1; sim_run(&s, 10); TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state); TEST_ASSERT_EQUAL_INT(PUMP_OFF, s.o.pump); TEST_ASSERT_EQUAL_UINT8(0, s.o.valve);
    s.in.leak = 0; s.in.stream = 0; sim_run(&s, 120000); TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state); TEST_ASSERT_EQUAL_INT(ERR_LEAK, s.f.fault);
    tr_fsm_clear_fault(&s.f, s.t); sim_run(&s, 31000); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
}
static void test_fsm_reservoir_empty_retries(void) {
    sim_t s; sim_init(&s, 0);
    tr_fsm_force_purge(&s.f, s.t); sim_run(&s, 17100); TEST_ASSERT_EQUAL_INT(1, s.req[REQ_PURGE_CHECK]);
    s.in.check_done = 1; s.in.check_air = 1; sim_run(&s, 10);
    TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state); TEST_ASSERT_EQUAL_INT(ERR_RESERVOIR_EMPTY, s.f.fault);
    sim_run(&s, 100000); TEST_ASSERT_EQUAL_INT(STATE_LOCKOUT, s.f.state);                     /* no events while empty */
    sim_run(&s, 510000); TEST_ASSERT_EQUAL_INT(STATE_PURGE_CLEANING, s.f.state);              /* retry after 10 min */
    sim_run(&s, 17000); s.in.check_done = 1; s.in.check_air = 0; sim_run(&s, 10);
    TEST_ASSERT_EQUAL_INT(ERR_NONE, s.f.fault); sim_run(&s, 31000); TEST_ASSERT_EQUAL_INT(STATE_IDLE, s.f.state);
}
static void test_fsm_analysis_timeout_and_forced_event(void) {
    sim_t s; sim_init(&s, 1);
    tr_fsm_force_event(&s.f, s.t); sim_run(&s, 10); TEST_ASSERT_EQUAL_INT(1, s.req[REQ_BLANK]); TEST_ASSERT_EQUAL_UINT16(8, s.f.event_id);
    sim_run(&s, 2100); TEST_ASSERT_EQUAL_INT(STATE_SAMPLING, s.f.state);
    sim_run(&s, 6100); TEST_ASSERT_EQUAL_INT(STATE_ANALYSIS, s.f.state);
    sim_run(&s, 15100); TEST_ASSERT_EQUAL_INT(STATE_PURGE_CLEANING, s.f.state); TEST_ASSERT_EQUAL_INT(1, s.errs[ERR_ANALYSIS_TIMEOUT]);
}

static void write_golden(void) {                             /* frames for the Python bridge test */
    FILE *fp = fopen("golden_frames.bin", "wb"); if (!fp) return;
    tr_frame_t f = sample_frame(); uint8_t b[48];
    for (int i = 0; i < 3; i++) { f.seq = (uint16_t)(513 + i); f.type = (uint8_t)(i == 2 ? TR_FT_ERROR : TR_FT_RESULT); f.error_code = (uint16_t)(i == 2 ? ERR_LEAK : 0); tr_frame_seal(&f, b); fwrite(b, 1, 48, fp); }
    fclose(fp);
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_frame_size_and_crc_vector); RUN_TEST(test_frame_roundtrip_and_corruption); RUN_TEST(test_saturation);
    RUN_TEST(test_moving_average); RUN_TEST(test_ema_and_median); RUN_TEST(test_settle_detector_ignores_sloshing);
    RUN_TEST(test_ec_recovers_conductivity); RUN_TEST(test_ec_two_point_calibration); RUN_TEST(test_ec_temperature_and_air);
    RUN_TEST(test_optics); RUN_TEST(test_sg_and_hydration); RUN_TEST(test_quality_and_dilution);
    RUN_TEST(test_fsm_full_event_sequence); RUN_TEST(test_fsm_short_event_and_presence_gate); RUN_TEST(test_fsm_splash_does_not_abort);
    RUN_TEST(test_fsm_fallback_trigger); RUN_TEST(test_fsm_leak_latches); RUN_TEST(test_fsm_reservoir_empty_retries);
    RUN_TEST(test_fsm_analysis_timeout_and_forced_event);
    write_golden();
    return UNITY_END();
}
