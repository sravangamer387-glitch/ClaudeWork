#include "ap1.h"

static const uint8_t TIMER_MIN[] = {0, 15, 30, 60};
#define TIMER_N ((uint8_t)(sizeof TIMER_MIN / sizeof TIMER_MIN[0]))
/* warm white, blue, green, red */
static const uint8_t PALETTE[LAMP_MODES][3] = {
    {255, 170, 90}, {20, 40, 255}, {20, 255, 60}, {255, 20, 20}, {0, 0, 0}};
/* slow rainbow waypoints (each reached by 20 ms steps, so no abrupt change) */
static const uint8_t RAINBOW[][3] = {
    {255, 40, 40}, {255, 160, 20}, {40, 255, 60}, {30, 120, 255}, {160, 40, 255}};
#define RAINBOW_N ((uint8_t)(sizeof RAINBOW / sizeof RAINBOW[0]))
#define RAINBOW_HOLD_MS 6000u

static void set_target(lamp_t *l, uint8_t r, uint8_t g, uint8_t b) { l->tr = r; l->tg = g; l->tb = b; }

static void apply_mode(lamp_t *l) {
    if (l->mode == LAMP_MODES - 1) {
        l->rainbow_idx = 0;
        l->t_rainbow = l->hal->millis();
        set_target(l, RAINBOW[0][0], RAINBOW[0][1], RAINBOW[0][2]);
    } else {
        set_target(l, PALETTE[l->mode][0], PALETTE[l->mode][1], PALETTE[l->mode][2]);
    }
}

static void write_leds(lamp_t *l) {
    l->hal->led_set(LAMP_LED_R, l->r);
    l->hal->led_set(LAMP_LED_G, l->g);
    l->hal->led_set(LAMP_LED_B, l->b);
}

static uint8_t approach(uint8_t cur, uint8_t tgt) {
    if (cur < tgt) return (uint8_t)(cur + 1u);
    if (cur > tgt) return (uint8_t)(cur - 1u);
    return cur;
}

static void power_off(lamp_t *l) {
    l->on = false;
    l->timer_armed = false;
    l->timer_idx = 0;
    if (l->song) { df_cmd(&l->df, DF_CMD_STOP, 0); l->song = false; }
    set_target(l, 0, 0, 0);
}

void lamp_init(lamp_t *l, const ap1_hal_t *hal) {
    *l = (lamp_t){0};
    l->hal = hal;
    df_init(&l->df, hal, 14);                /* quiet lullaby volume cap */
    l->t_step = hal->millis();
    write_leds(l);
}

void lamp_event(lamp_t *l, btn_evt_t e) {
    uint32_t now = l->hal->millis();
    if (e.idx == LAMP_BTN_MODE) {
        if (e.kind == BTN_EVT_LONG) { if (l->on) power_off(l); return; }
        if (e.kind != BTN_EVT_PRESS) return;
        if (!l->on) { l->on = true; l->mode = 0; }
        else l->mode = (uint8_t)((l->mode + 1u) % LAMP_MODES);
        apply_mode(l);
    } else if (e.idx == LAMP_BTN_TIMER && e.kind == BTN_EVT_PRESS && l->on) {
        l->timer_idx = (uint8_t)((l->timer_idx + 1u) % TIMER_N);
        l->timer_armed = TIMER_MIN[l->timer_idx] != 0;
        if (l->timer_armed) l->deadline = now + (uint32_t)TIMER_MIN[l->timer_idx] * 60000u;
        apply_mode(l);
    } else if (e.idx == LAMP_BTN_SONG && e.kind == BTN_EVT_PRESS) {
        if (l->song) { df_cmd(&l->df, DF_CMD_STOP, 0); l->song = false; }
        else {
            df_cmd(&l->df, DF_CMD_SRC, 2);
            df_volume(&l->df, 10);
            df_cmd(&l->df, DF_CMD_LOOP_FOLDER, 1); /* loop folder 01 = lullabies */
            l->song = true;
        }
    }
}

void lamp_tick(lamp_t *l) {
    uint32_t now = l->hal->millis();
    if (l->on && l->timer_armed) {
        int32_t left = (int32_t)(l->deadline - now);
        if (left <= 0) power_off(l);
        else if (left <= (int32_t)LAMP_FADE_MS) set_target(l, 0, 0, 0);   /* last 10 s: fade out */
    }
    if (l->on && l->mode == LAMP_MODES - 1 && (uint32_t)(now - l->t_rainbow) >= RAINBOW_HOLD_MS &&
        !(l->timer_armed && (int32_t)(l->deadline - now) <= (int32_t)LAMP_FADE_MS)) {
        l->rainbow_idx = (uint8_t)((l->rainbow_idx + 1u) % RAINBOW_N);
        l->t_rainbow = now;
        set_target(l, RAINBOW[l->rainbow_idx][0], RAINBOW[l->rainbow_idx][1], RAINBOW[l->rainbow_idx][2]);
    }
    /* At most ONE colour step per tick, even if the main loop stalled: output can never jump
     * (photosensitivity safety). If we fell behind, resynchronise instead of catching up. */
    if ((uint32_t)(now - l->t_step) >= LAMP_STEP_MS) {
        l->t_step += LAMP_STEP_MS;
        if ((uint32_t)(now - l->t_step) >= LAMP_STEP_MS) l->t_step = now;
        l->r = approach(l->r, l->tr);
        l->g = approach(l->g, l->tg);
        l->b = approach(l->b, l->tb);
    }
    write_leds(l);
}
