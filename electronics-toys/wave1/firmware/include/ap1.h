/* AP1 audio/toy platform - portable C core (C99, no heap, no libc state).
 * Hardware access goes through ap1_hal_t so the same code runs on the MCU and in host tests. */
#ifndef AP1_H
#define AP1_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* ---------------- HAL ---------------- */
typedef struct {
    uint32_t (*millis)(void);
    bool (*button_raw)(uint8_t idx);                  /* true = pressed */
    void (*uart_write)(const uint8_t *d, size_t n);   /* to the MP3 module */
    void (*led_set)(uint8_t idx, uint8_t level);      /* 0..255 (PWM or on/off) */
    void (*seg_write)(uint8_t digit, uint8_t mask);   /* bit0..6 = a..g, bit7 = dp */
    void (*buzzer)(uint16_t freq_hz, uint16_t ms);    /* freq 0 = silence */
} ap1_hal_t;

/* ---------------- buttons: debounce + press/long events ---------------- */
#define BTN_MAX 8
#define BTN_DEBOUNCE_MS 20u
#define BTN_LONG_MS 800u
#define BTN_QUEUE 16

typedef enum { BTN_EVT_PRESS = 1, BTN_EVT_LONG = 2 } btn_kind_t;
typedef struct { uint8_t idx; uint8_t kind; } btn_evt_t;

typedef struct {
    const ap1_hal_t *hal;
    uint8_t n;
    bool stable[BTN_MAX], last_raw[BTN_MAX], long_sent[BTN_MAX];
    uint32_t t_change[BTN_MAX], t_press[BTN_MAX];
    btn_evt_t q[BTN_QUEUE];
    uint8_t qh, qt, qn;
} btn_scan_t;

void btn_init(btn_scan_t *b, const ap1_hal_t *hal, uint8_t n);
void btn_update(btn_scan_t *b);
bool btn_pop(btn_scan_t *b, btn_evt_t *out);

/* ---------------- MP3 module (YX5200 / DFPlayer-Mini style serial protocol) ----------------
 * Frame: 7E FF 06 <cmd> <fb> <p1> <p2> <chk_hi> <chk_lo> EF ; chk = -(FF+06+cmd+fb+p1+p2).
 * Command codes and the 0..30 volume range are from the module datasheet as I remember it:
 * VERIFY against the datasheet of the exact module before release. */
#define DF_FRAME_LEN 10
enum {
    DF_CMD_NEXT = 0x01, DF_CMD_PREV = 0x02, DF_CMD_TRACK = 0x03, DF_CMD_VOL_SET = 0x06,
    DF_CMD_SRC = 0x09, DF_CMD_RESET = 0x0C, DF_CMD_PLAY = 0x0D, DF_CMD_PAUSE = 0x0E,
    DF_CMD_FOLDER = 0x0F, DF_CMD_STOP = 0x16, DF_CMD_LOOP_FOLDER = 0x17
};
#define DF_VOL_MAX 30u

typedef struct { const ap1_hal_t *hal; uint8_t vol_cap; uint8_t frames; } df_t;

size_t df_build(uint8_t out[DF_FRAME_LEN], uint8_t cmd, uint16_t param);
bool df_parse(const uint8_t *in, size_t n, uint8_t *cmd, uint16_t *param);
void df_init(df_t *d, const ap1_hal_t *hal, uint8_t vol_cap);
void df_cmd(df_t *d, uint8_t cmd, uint16_t param);
uint8_t df_volume(df_t *d, uint8_t v);                       /* clamps to cap, returns value sent */
void df_play_folder_track(df_t *d, uint8_t folder, uint8_t track);

/* ---------------- App 1: regional-language rhymes & stories player ---------------- */
#define RH_MAX_LANG 8
#define RH_VOL_DEFAULT 12u
#define RH_VOL_CAP 20u            /* hearing-safety cap, tune after acoustic test */
enum { RH_BTN_PLAY, RH_BTN_NEXT, RH_BTN_PREV, RH_BTN_VOLUP, RH_BTN_VOLDN, RH_BTN_LANG, RH_BTN_SLEEP, RH_BTN_COUNT };
enum { RH_LED_PLAY, RH_LED_SLEEP };

typedef struct {
    const ap1_hal_t *hal;
    df_t df;
    uint8_t lang_count, tracks[RH_MAX_LANG];
    uint8_t lang, track, vol, sleep_idx;
    bool playing, started, sleep_armed;
    uint32_t sleep_deadline;
} rhymes_t;

void rhymes_init(rhymes_t *r, const ap1_hal_t *hal, uint8_t lang_count, const uint8_t *tracks_per_lang);
void rhymes_event(rhymes_t *r, btn_evt_t e);
void rhymes_tick(rhymes_t *r);

/* ---------------- App 2: star-projector night lamp ---------------- */
enum { LAMP_BTN_MODE, LAMP_BTN_TIMER, LAMP_BTN_SONG, LAMP_BTN_COUNT };
enum { LAMP_LED_R, LAMP_LED_G, LAMP_LED_B };
#define LAMP_STEP_MS 20u          /* one colour step per 20 ms => 255 steps = 5.1 s (no flashing) */
#define LAMP_FADE_MS 10000u
#define LAMP_MODES 5              /* warm white, blue, green, red, slow rainbow */

typedef struct {
    const ap1_hal_t *hal;
    df_t df;
    bool on, song, timer_armed;
    uint8_t mode, timer_idx, r, g, b, tr, tg, tb, rainbow_idx;
    uint32_t t_step, t_rainbow, deadline;
} lamp_t;

void lamp_init(lamp_t *l, const ap1_hal_t *hal);
void lamp_event(lamp_t *l, btn_evt_t e);
void lamp_tick(lamp_t *l);

/* ---------------- App 3: handheld cricket game ---------------- */
enum { CR_BTN_BAT, CR_BTN_START, CR_BTN_COUNT };
#define CR_LANE 6                 /* LEDs 0..5 show the ball; LED 6 = result flash */
#define CR_BALLS 12               /* two overs */
#define CR_MAX_WICKETS 2
#define CR_RESULT_MS 900u
typedef enum { CR_IDLE, CR_BOWLING, CR_RESULT, CR_OVER } cr_phase_t;
typedef enum { RES_NONE, RES_DOT, RES_1, RES_2, RES_4, RES_6, RES_OUT_EARLY, RES_OUT_BOWLED } cr_result_t;

typedef struct {
    const ap1_hal_t *hal;
    cr_phase_t phase;
    uint8_t runs, wickets, balls_left, pos, last_result;
    uint16_t step_ms;
    uint32_t rng, t_next;
} cricket_t;

void cricket_init(cricket_t *c, const ap1_hal_t *hal, uint32_t seed);
void cricket_event(cricket_t *c, btn_evt_t e);
void cricket_tick(cricket_t *c);
uint8_t seg_encode(uint8_t digit);   /* 0..9 -> segment mask, others -> blank */

#endif
