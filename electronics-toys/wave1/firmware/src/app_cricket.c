#include "ap1.h"

/* segment masks a..g = bit0..6 */
static const uint8_t SEG[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};
uint8_t seg_encode(uint8_t digit) { return digit < 10u ? SEG[digit] : 0u; }

static uint32_t rnd(cricket_t *c) {            /* xorshift32 */
    uint32_t x = c->rng;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    c->rng = x;
    return x;
}

static void show(cricket_t *c) {
    uint8_t r = c->runs > 99u ? 99u : c->runs;
    c->hal->seg_write(0, seg_encode((uint8_t)(r / 10u)));
    c->hal->seg_write(1, seg_encode((uint8_t)(r % 10u)));
    c->hal->seg_write(2, seg_encode(c->wickets));
    c->hal->seg_write(3, seg_encode(c->balls_left > 9u ? 9u : c->balls_left)); /* "9" = 9 or more */
    for (uint8_t i = 0; i < CR_LANE; i++)
        c->hal->led_set(i, (c->phase == CR_BOWLING && c->pos == i) ? 255 : 0);
    c->hal->led_set(CR_LANE, (c->phase == CR_RESULT && c->last_result >= RES_4 && c->last_result <= RES_6) ? 255 : 0);
}

static void new_ball(cricket_t *c) {
    c->phase = CR_BOWLING;
    c->pos = 0;
    c->t_next = c->hal->millis() + c->step_ms;
}

static void end_ball(cricket_t *c, cr_result_t res) {
    static const uint8_t RUNS[] = {0, 0, 1, 2, 4, 6, 0, 0};
    c->last_result = (uint8_t)res;
    c->balls_left--;
    c->runs = (uint8_t)(c->runs + RUNS[res]);
    if (c->runs > 99u) c->runs = 99u;
    if (res == RES_OUT_EARLY || res == RES_OUT_BOWLED) {
        c->wickets++;
        c->hal->buzzer(200, 400);
    } else if (res >= RES_4) {
        c->hal->buzzer(1200, 250);
    } else {
        c->hal->buzzer(600, 80);
    }
    c->phase = CR_RESULT;
    c->t_next = c->hal->millis() + CR_RESULT_MS;
    /* the ball just played also speeds up the next ones slightly (faster every 2 balls, floor 140 ms) */
    if (((CR_BALLS - c->balls_left) % 2u) == 0u && c->step_ms > 140u) c->step_ms = (uint16_t)(c->step_ms - 15u);
}

void cricket_init(cricket_t *c, const ap1_hal_t *hal, uint32_t seed) {
    *c = (cricket_t){0};
    c->hal = hal;
    c->rng = seed ? seed : 0x2545F491u;
    c->phase = CR_IDLE;
    c->step_ms = 300;
    show(c);
}

void cricket_event(cricket_t *c, btn_evt_t e) {
    if (e.kind != BTN_EVT_PRESS) return;
    if (e.idx == CR_BTN_START && (c->phase == CR_IDLE || c->phase == CR_OVER)) {
        c->runs = 0; c->wickets = 0; c->balls_left = CR_BALLS; c->step_ms = 300;
        new_ball(c);
    } else if (e.idx == CR_BTN_BAT && c->phase == CR_BOWLING) {
        static const cr_result_t BY_POS[CR_LANE] = {RES_OUT_EARLY, RES_OUT_EARLY, RES_1, RES_2, RES_4, RES_6};
        end_ball(c, BY_POS[c->pos]);
    }
    show(c);
}

void cricket_tick(cricket_t *c) {
    uint32_t now = c->hal->millis();
    if ((int32_t)(now - c->t_next) < 0) return;
    if (c->phase == CR_BOWLING) {
        if (c->pos + 1u < CR_LANE) {
            c->pos++;
            c->t_next = now + c->step_ms;
        } else {                                 /* ball passed the bat unplayed */
            end_ball(c, (rnd(c) % 3u) == 0u ? RES_OUT_BOWLED : RES_DOT);
        }
    } else if (c->phase == CR_RESULT) {
        if (c->balls_left == 0 || c->wickets >= CR_MAX_WICKETS) c->phase = CR_OVER;
        else new_ball(c);
    }
    show(c);
}
