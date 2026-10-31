/* Fake hardware for host tests: scripted time, buttons, captured UART/LEDs/segments. */
#ifndef FAKE_HAL_H
#define FAKE_HAL_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/ap1.h"

static uint32_t f_now;
static bool f_btn[BTN_MAX];
static uint8_t f_uart[4096];
static size_t f_uart_n;
static uint8_t f_led[16], f_seg[8];
static unsigned f_buzz_calls;

static uint32_t f_millis(void) { return f_now; }
static bool f_button(uint8_t i) { return f_btn[i]; }
static void f_write(const uint8_t *d, size_t n) { if (f_uart_n + n <= sizeof f_uart) { memcpy(f_uart + f_uart_n, d, n); f_uart_n += n; } }
static void f_led_set(uint8_t i, uint8_t v) { f_led[i] = v; }
static void f_seg_write(uint8_t d, uint8_t m) { f_seg[d] = m; }
static void f_buzzer(uint16_t hz, uint16_t ms) { (void)hz; (void)ms; f_buzz_calls++; }

static const ap1_hal_t FAKE = {f_millis, f_button, f_write, f_led_set, f_seg_write, f_buzzer};

static void fake_reset(void) {
    f_now = 1000; f_uart_n = 0; f_buzz_calls = 0;
    memset(f_btn, 0, sizeof f_btn); memset(f_led, 0, sizeof f_led); memset(f_seg, 0, sizeof f_seg);
}

static int g_fail, g_pass;
#define CHECK(cond) do { if (cond) g_pass++; else { g_fail++; printf("  FAIL %s:%d  %s\n", __FILE__, __LINE__, #cond); } } while (0)

/* last frame sent to the MP3 module */
static bool last_frame(uint8_t *cmd, uint16_t *param) {
    if (f_uart_n < DF_FRAME_LEN) return false;
    return df_parse(f_uart + f_uart_n - DF_FRAME_LEN, DF_FRAME_LEN, cmd, param);
}
/* how many times a given command was sent */
static unsigned count_cmd(uint8_t want) {
    unsigned n = 0;
    for (size_t i = 0; i + DF_FRAME_LEN <= f_uart_n; i += DF_FRAME_LEN) {
        uint8_t c; uint16_t p;
        if (df_parse(f_uart + i, DF_FRAME_LEN, &c, &p) && c == want) n++;
    }
    return n;
}
/* press and release a button through the debouncer */
static void tap(btn_scan_t *b, uint8_t idx, void (*sink)(void *, btn_evt_t), void *ctx) {
    btn_evt_t e;
    f_btn[idx] = true;
    for (int i = 0; i < 4; i++) { f_now += 10; btn_update(b); }
    f_btn[idx] = false;
    for (int i = 0; i < 4; i++) { f_now += 10; btn_update(b); }
    while (btn_pop(b, &e)) sink(ctx, e);
}
#endif
