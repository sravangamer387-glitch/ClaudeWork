#include "fake_hal.h"

/* ---------- core: buttons + protocol ---------- */
static void sink_count(void *ctx, btn_evt_t e) { if (e.kind == BTN_EVT_PRESS) (*(int *)ctx)++; }

static void test_buttons(void) {
    puts("buttons");
    btn_scan_t b; int n = 0; btn_evt_t e;
    fake_reset(); btn_init(&b, &FAKE, 4);
    /* a 5 ms glitch must not register */
    f_btn[1] = true; f_now += 5; btn_update(&b); f_btn[1] = false; f_now += 30; btn_update(&b); f_now += 30; btn_update(&b);
    CHECK(!btn_pop(&b, &e));
    /* a clean tap gives exactly one PRESS */
    tap(&b, 2, sink_count, &n);
    CHECK(n == 1);
    /* hold 1 s: PRESS then LONG once */
    fake_reset(); btn_init(&b, &FAKE, 4);
    f_btn[0] = true;
    for (int i = 0; i < 120; i++) { f_now += 10; btn_update(&b); }
    CHECK(btn_pop(&b, &e) && e.idx == 0 && e.kind == BTN_EVT_PRESS);
    CHECK(btn_pop(&b, &e) && e.idx == 0 && e.kind == BTN_EVT_LONG);
    CHECK(!btn_pop(&b, &e));
    /* a tap also yields one RELEASE after the PRESS */
    fake_reset(); btn_init(&b, &FAKE, 1);
    f_btn[0] = true; for (int i = 0; i < 4; i++) { f_now += 10; btn_update(&b); }
    f_btn[0] = false; for (int i = 0; i < 4; i++) { f_now += 10; btn_update(&b); }
    CHECK(btn_pop(&b, &e) && e.kind == BTN_EVT_PRESS);
    CHECK(btn_pop(&b, &e) && e.kind == BTN_EVT_RELEASE);
    CHECK(!btn_pop(&b, &e));
    /* millis wrap-around */
    fake_reset(); btn_init(&b, &FAKE, 1); f_now = 0xFFFFFFF0u;
    f_btn[0] = true; for (int i = 0; i < 6; i++) { f_now += 10; btn_update(&b); }
    CHECK(btn_pop(&b, &e) && e.kind == BTN_EVT_PRESS);
}

static void test_protocol(void) {
    puts("protocol");
    uint8_t f[DF_FRAME_LEN], cmd; uint16_t p;
    /* known-good frame: set volume 30 -> 7E FF 06 06 00 00 1E FE D7 EF */
    df_build(f, DF_CMD_VOL_SET, 30);
    const uint8_t want[DF_FRAME_LEN] = {0x7E, 0xFF, 0x06, 0x06, 0x00, 0x00, 0x1E, 0xFE, 0xD7, 0xEF};
    CHECK(memcmp(f, want, DF_FRAME_LEN) == 0);
    CHECK(df_parse(f, DF_FRAME_LEN, &cmd, &p) && cmd == DF_CMD_VOL_SET && p == 30);
    f[6] ^= 1; CHECK(!df_parse(f, DF_FRAME_LEN, &cmd, &p));            /* corrupted */
    df_build(f, DF_CMD_FOLDER, 0x0305);
    CHECK(df_parse(f, DF_FRAME_LEN, &cmd, &p) && cmd == DF_CMD_FOLDER && p == 0x0305);
    fake_reset(); df_t d; df_init(&d, &FAKE, 20);
    CHECK(df_volume(&d, 30) == 20);                                    /* cap */
    CHECK(df_volume(&d, 5) == 5);
}

/* ---------- rhymes player ---------- */
typedef struct { btn_scan_t b; rhymes_t r; } RH;
static void rh_sink(void *c, btn_evt_t e) { rhymes_event(&((RH *)c)->r, e); }
static void rh_init(RH *x) {
    static const uint8_t tr[3] = {5, 3, 4};
    fake_reset(); btn_init(&x->b, &FAKE, RH_BTN_COUNT); rhymes_init(&x->r, &FAKE, 3, tr);
}
static void test_rhymes(void) {
    puts("rhymes");
    RH x; uint8_t cmd; uint16_t p;
    rh_init(&x);
    CHECK(x.r.vol == RH_VOL_DEFAULT);
    tap(&x.b, RH_BTN_PLAY, rh_sink, &x);                               /* first play: folder 1 track 1 */
    CHECK(last_frame(&cmd, &p) && cmd == DF_CMD_FOLDER && p == 0x0101 && f_led[RH_LED_PLAY] == 255);
    tap(&x.b, RH_BTN_PLAY, rh_sink, &x);                               /* pause */
    CHECK(last_frame(&cmd, &p) && cmd == DF_CMD_PAUSE && f_led[RH_LED_PLAY] == 0);
    tap(&x.b, RH_BTN_PLAY, rh_sink, &x);                               /* resume */
    CHECK(last_frame(&cmd, &p) && cmd == DF_CMD_PLAY);
    for (int i = 0; i < 4; i++) tap(&x.b, RH_BTN_NEXT, rh_sink, &x);   /* 1 -> 5 */
    CHECK(x.r.track == 5);
    tap(&x.b, RH_BTN_NEXT, rh_sink, &x);                               /* wraps to 1 */
    CHECK(x.r.track == 1);
    tap(&x.b, RH_BTN_PREV, rh_sink, &x);                               /* wraps to 5 */
    CHECK(x.r.track == 5 && last_frame(&cmd, &p) && p == 0x0105);
    tap(&x.b, RH_BTN_LANG, rh_sink, &x);                               /* folder 2 track 1 */
    CHECK(x.r.lang == 1 && x.r.track == 1 && last_frame(&cmd, &p) && p == 0x0201);
    tap(&x.b, RH_BTN_LANG, rh_sink, &x); tap(&x.b, RH_BTN_LANG, rh_sink, &x);
    CHECK(x.r.lang == 0);                                              /* wraps over 3 languages */
    for (int i = 0; i < 20; i++) tap(&x.b, RH_BTN_VOLUP, rh_sink, &x);
    CHECK(x.r.vol == RH_VOL_CAP);                                      /* hearing cap holds */
    for (int i = 0; i < 20; i++) tap(&x.b, RH_BTN_VOLDN, rh_sink, &x);
    CHECK(x.r.vol == 0);
}
static void test_rhymes_sleep(void) {
    puts("rhymes sleep timer");
    RH x; rh_init(&x);
    tap(&x.b, RH_BTN_PLAY, rh_sink, &x);
    tap(&x.b, RH_BTN_SLEEP, rh_sink, &x);                              /* 15 min */
    CHECK(x.r.sleep_armed && f_led[RH_LED_SLEEP] == 255);
    uint32_t t0 = x.r.sleep_deadline;
    f_now = t0 - 1; rhymes_tick(&x.r); CHECK(x.r.playing);
    f_now = t0;     rhymes_tick(&x.r); CHECK(!x.r.playing && count_cmd(DF_CMD_STOP) == 1 && f_led[RH_LED_SLEEP] == 0);
    tap(&x.b, RH_BTN_PLAY, rh_sink, &x);                               /* after sleep: restart, not resume */
    uint8_t c; uint16_t p; CHECK(last_frame(&c, &p) && c == DF_CMD_FOLDER);
    for (int i = 0; i < 4; i++) tap(&x.b, RH_BTN_SLEEP, rh_sink, &x);  /* 4 presses cycles back to off */
    CHECK(!x.r.sleep_armed);
    /* timer survives millis wrap */
    rh_init(&x); f_now = 0xFFFFF000u; tap(&x.b, RH_BTN_PLAY, rh_sink, &x); tap(&x.b, RH_BTN_SLEEP, rh_sink, &x);
    f_now += 15u * 60000u + 10; rhymes_tick(&x.r); CHECK(!x.r.playing);
}

/* ---------- lamp ---------- */
typedef struct { btn_scan_t b; lamp_t l; } LP;
static void lp_sink(void *c, btn_evt_t e) { lamp_event(&((LP *)c)->l, e); }
static void lp_run(LP *x, uint32_t ms) { for (uint32_t t = 0; t < ms; t += 10) { f_now += 10; lamp_tick(&x->l); } }
/* largest single-step change on any RGB channel over `steps` ticks of 20 ms */
static int lamp_max_step(LP *x, int steps) {
    uint8_t pr = f_led[0], pg = f_led[1], pb = f_led[2];
    int worst = 0;
    for (int i = 0; i < steps; i++) {
        f_now += 20;
        lamp_tick(&x->l);
        int d = abs(f_led[0] - pr);
        if (abs(f_led[1] - pg) > d) d = abs(f_led[1] - pg);
        if (abs(f_led[2] - pb) > d) d = abs(f_led[2] - pb);
        if (d > worst) worst = d;
        pr = f_led[0]; pg = f_led[1]; pb = f_led[2];
    }
    return worst;
}
static void test_lamp(void) {
    puts("lamp");
    LP x; fake_reset(); btn_init(&x.b, &FAKE, LAMP_BTN_COUNT); lamp_init(&x.l, &FAKE);
    lp_run(&x, 100); CHECK(f_led[0] == 0 && f_led[1] == 0 && f_led[2] == 0);
    tap(&x.b, LAMP_BTN_MODE, lp_sink, &x); CHECK(x.l.on && x.l.mode == 0);
    lp_run(&x, 6000);                                                  /* warm white reached */
    CHECK(f_led[0] == 255 && f_led[1] == 170 && f_led[2] == 90);
    tap(&x.b, LAMP_BTN_MODE, lp_sink, &x); CHECK(x.l.mode == 1);
    /* photosensitivity: no channel may move by more than 1 level per 20 ms step, ever */
    int worst = lamp_max_step(&x, 3000);
    CHECK(worst <= 1);
    for (int i = 0; i < 3; i++) tap(&x.b, LAMP_BTN_MODE, lp_sink, &x); /* modes 2,3,4 (rainbow) */
    CHECK(x.l.mode == 4);
    int worst2 = lamp_max_step(&x, 3500);                              /* ~70 s of rainbow = 11 colour changes */
    CHECK(worst2 <= 1 && x.l.rainbow_idx != 0);
    tap(&x.b, LAMP_BTN_SONG, lp_sink, &x); CHECK(x.l.song && count_cmd(DF_CMD_LOOP_FOLDER) == 1);
    tap(&x.b, LAMP_BTN_TIMER, lp_sink, &x); CHECK(x.l.timer_armed);
    uint32_t dl = x.l.deadline;
    f_now = dl - LAMP_FADE_MS - 1000; lamp_tick(&x.l);
    CHECK(x.l.tr != 0 || x.l.tg != 0 || x.l.tb != 0);                  /* not yet fading */
    f_now = dl - LAMP_FADE_MS + 1; lamp_tick(&x.l);
    CHECK(x.l.tr == 0 && x.l.tg == 0 && x.l.tb == 0);                  /* fade begins */
    f_now = dl + 1; lamp_tick(&x.l);
    CHECK(!x.l.on && !x.l.song && count_cmd(DF_CMD_STOP) == 1);        /* off + song stopped */
    lp_run(&x, 6000); CHECK(f_led[0] == 0 && f_led[1] == 0 && f_led[2] == 0);
}

/* ---------- cricket ---------- */
typedef struct { btn_scan_t b; cricket_t c; } CRX;
static void cr_sink(void *c, btn_evt_t e) { cricket_event(&((CRX *)c)->c, e); }
static void cr_init(CRX *x, uint32_t seed) { fake_reset(); btn_init(&x->b, &FAKE, CR_BTN_COUNT); cricket_init(&x->c, &FAKE, seed); }
/* advance time until the ball is at `pos`, return false if it never gets there */
static bool cr_wait_pos(CRX *x, uint8_t pos) {
    for (int i = 0; i < 2000; i++) { if (x->c.phase == CR_BOWLING && x->c.pos == pos) return true; f_now += 5; cricket_tick(&x->c); }
    return false;
}
static void cr_finish_result(CRX *x) { for (int i = 0; i < 400 && x->c.phase == CR_RESULT; i++) { f_now += 5; cricket_tick(&x->c); } }

static void test_cricket(void) {
    puts("cricket");
    CHECK(seg_encode(0) == 0x3F && seg_encode(8) == 0x7F && seg_encode(10) == 0);
    CRX x; cr_init(&x, 12345);
    CHECK(x.c.phase == CR_IDLE);
    tap(&x.b, CR_BTN_BAT, cr_sink, &x); CHECK(x.c.phase == CR_IDLE);   /* bat before start does nothing */
    tap(&x.b, CR_BTN_START, cr_sink, &x); CHECK(x.c.phase == CR_BOWLING && x.c.balls_left == CR_BALLS);
    /* every timing zone gives the intended result */
    static const struct { uint8_t pos; uint8_t runs; uint8_t wk; } Z[] = {{5, 6, 0}, {4, 4, 0}, {3, 2, 0}, {2, 1, 0}, {0, 0, 1}};
    for (unsigned z = 0; z < sizeof Z / sizeof Z[0]; z++) {
        cr_init(&x, 99);
        tap(&x.b, CR_BTN_START, cr_sink, &x);
        CHECK(cr_wait_pos(&x, Z[z].pos));
        btn_evt_t e = {CR_BTN_BAT, BTN_EVT_PRESS}; cricket_event(&x.c, e);
        CHECK(x.c.runs == Z[z].runs && x.c.wickets == Z[z].wk && x.c.balls_left == CR_BALLS - 1);
    }
    /* six sets the result LED */
    cr_init(&x, 7); tap(&x.b, CR_BTN_START, cr_sink, &x); cr_wait_pos(&x, 5);
    { btn_evt_t e = {CR_BTN_BAT, BTN_EVT_PRESS}; cricket_event(&x.c, e); }
    CHECK(f_led[CR_LANE] == 255 && f_seg[1] == seg_encode(6) && f_seg[0] == seg_encode(0));
    /* a full innings of perfect sixes: 12 balls -> 72 runs, then game over; ball speeds up but floors */
    cr_init(&x, 5); tap(&x.b, CR_BTN_START, cr_sink, &x);
    for (int b = 0; b < CR_BALLS; b++) {
        CHECK(cr_wait_pos(&x, 5));
        btn_evt_t e = {CR_BTN_BAT, BTN_EVT_PRESS}; cricket_event(&x.c, e);
        cr_finish_result(&x);
    }
    CHECK(x.c.phase == CR_OVER && x.c.runs == 72 && x.c.balls_left == 0 && x.c.step_ms >= 140);
    /* restart works from game over */
    tap(&x.b, CR_BTN_START, cr_sink, &x); CHECK(x.c.phase == CR_BOWLING && x.c.runs == 0);
    /* two wickets end the game early; never bat -> every ball is dot or bowled, game ends by 12 balls or 2 wickets */
    cr_init(&x, 31337); tap(&x.b, CR_BTN_START, cr_sink, &x);
    for (int i = 0; i < 20000 && x.c.phase != CR_OVER; i++) { f_now += 5; cricket_tick(&x.c); }
    CHECK(x.c.phase == CR_OVER && x.c.runs == 0 && (x.c.wickets == CR_MAX_WICKETS || x.c.balls_left == 0));
    /* determinism: same seed, same script -> same outcome */
    uint8_t w1, w2;
    cr_init(&x, 4242); tap(&x.b, CR_BTN_START, cr_sink, &x);
    for (int i = 0; i < 20000 && x.c.phase != CR_OVER; i++) { f_now += 5; cricket_tick(&x.c); }
    w1 = x.c.wickets;
    cr_init(&x, 4242); tap(&x.b, CR_BTN_START, cr_sink, &x);
    for (int i = 0; i < 20000 && x.c.phase != CR_OVER; i++) { f_now += 5; cricket_tick(&x.c); }
    w2 = x.c.wickets;
    CHECK(w1 == w2);
}

int main(void) {
    test_buttons(); test_protocol(); test_rhymes(); test_rhymes_sleep(); test_lamp(); test_cricket();
    printf("\n%d checks passed, %d failed\n", g_pass, g_fail);
    return g_fail ? 1 : 0;
}
