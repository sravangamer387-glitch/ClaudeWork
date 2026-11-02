/* AP1 board HAL for the ATmega328P (8 MHz internal) and the app selector. Build: make avr  (PRODUCT=1 rhymes, 3 lamp, 4 cricket).
 * Pin map (board utility10/pcb/boards/ap1.py): D0/D1 MP3 UART (9600), D2 MP3 BUSY, D3/D5/D6 lamp PWM R/G/B, D9 buzzer (tone),
 * D10 motor PWM, D11/D13/D12 = 74HC595 SER/SRCLK/RCLK (U4 segments, U5 ball lane chained from U4 QH'), A0..A3 digit drivers,
 * A4/A5 status LEDs, A6 seven-button resistor ladder (10 k pull-up), A7 battery divider (1:2), D4 factory test (pulled up). */
#include <Arduino.h>
#include "ap1.h"
#ifndef PRODUCT
#define PRODUCT 1
#endif
#define P_SER 11
#define P_CLK 13
#define P_LAT 12
static const uint8_t DIG[4] = {A0, A1, A2, A3};
static uint8_t seg_mask[4] = {0, 0, 0, 0}, lane = 0, cur_digit = 0;
/* ladder thresholds: button k pulls ADC6 to R_k / (R_k + 10 k) of VCC; R = 1k 2.2k 3.9k 6.8k 12k 22k 47k -> 0.091 0.180 0.281 0.405 0.545 0.688 0.825 */
static const uint16_t LADDER_HI[7] = {138, 235, 350, 486, 630, 774, 935};   /* upper bounds (ADC counts, 0..1023): midpoints between levels; above 935 = none */
static int8_t ladder_now = -1;
static uint32_t hal_millis(void) { return millis(); }
static bool hal_button(uint8_t idx) { return ladder_now == (int8_t)idx; }
static void hal_uart(const uint8_t *d, size_t n) { Serial.write(d, n); }
static void hal_led(uint8_t idx, uint8_t level) {
#if PRODUCT == 3
    static const uint8_t pin[3] = {3, 5, 6}; if (idx < 3) analogWrite(pin[idx], level);
#elif PRODUCT == 4
    if (idx < 7) { if (level) lane |= (uint8_t)(1u << idx); else lane &= (uint8_t)~(1u << idx); }
#else
    if (idx == 0) digitalWrite(A4, level ? HIGH : LOW); else if (idx == 1) digitalWrite(A5, level ? HIGH : LOW);
#endif
}
static void hal_seg(uint8_t digit, uint8_t mask) { if (digit < 4) seg_mask[digit] = mask; }
static void hal_buzzer(uint16_t f, uint16_t ms) { if (f) tone(9, f, ms); else noTone(9); }
static const ap1_hal_t HAL = {hal_millis, hal_button, hal_uart, hal_led, hal_seg, hal_buzzer};
__attribute__((unused)) static void refresh_display(void) {                 /* one digit per call (call every 2 ms): lane byte then segment byte, then latch */
    for (uint8_t i = 0; i < 4; i++) digitalWrite(DIG[i], LOW);
    digitalWrite(P_LAT, LOW); shiftOut(P_SER, P_CLK, MSBFIRST, lane); shiftOut(P_SER, P_CLK, MSBFIRST, seg_mask[cur_digit]); digitalWrite(P_LAT, HIGH);
    digitalWrite(DIG[cur_digit], HIGH); cur_digit = (uint8_t)((cur_digit + 1) & 3u);
}
static void read_ladder(void) {
    uint16_t a = (uint16_t)analogRead(A6); int8_t k = -1;
    for (uint8_t i = 0; i < 7; i++) if (a < LADDER_HI[i]) { k = (int8_t)i; break; }
    ladder_now = k;
}
static btn_scan_t btn;
#if PRODUCT == 1
static rhymes_t app; static const uint8_t TRACKS[3] = {20, 20, 20};   /* placeholder: songs per language folder on the SD card */
#elif PRODUCT == 3
static lamp_t app;
#else
static cricket_t app;
#endif
void setup() {
    Serial.begin(9600);
    pinMode(P_SER, OUTPUT); pinMode(P_CLK, OUTPUT); pinMode(P_LAT, OUTPUT); for (uint8_t i = 0; i < 4; i++) pinMode(DIG[i], OUTPUT);
    pinMode(A4, OUTPUT); pinMode(A5, OUTPUT); pinMode(3, OUTPUT); pinMode(5, OUTPUT); pinMode(6, OUTPUT); pinMode(10, OUTPUT); pinMode(2, INPUT); pinMode(4, INPUT_PULLUP);
    delay(1500);                                   /* MP3 module boot time */
#if PRODUCT == 1
    btn_init(&btn, &HAL, RH_BTN_COUNT); rhymes_init(&app, &HAL, 3, TRACKS);
#elif PRODUCT == 3
    btn_init(&btn, &HAL, LAMP_BTN_COUNT); lamp_init(&app, &HAL);
#else
    btn_init(&btn, &HAL, CR_BTN_COUNT); cricket_init(&app, &HAL, (uint32_t)analogRead(A7) * 2654435761u + micros());
#endif
}
void loop() {
    static uint32_t t_scan = 0, t_disp = 0; uint32_t now = millis();
    if (now - t_scan >= 5u) { t_scan = now; read_ladder(); btn_update(&btn); btn_evt_t e;
        while (btn_pop(&btn, &e)) {
#if PRODUCT == 1
            rhymes_event(&app, e);
#elif PRODUCT == 3
            lamp_event(&app, e);
#else
            cricket_event(&app, e);
#endif
        }
#if PRODUCT == 1
        rhymes_tick(&app);
#elif PRODUCT == 3
        lamp_tick(&app);
#else
        cricket_tick(&app);
#endif
    }
#if PRODUCT == 4
    if (now - t_disp >= 2u) { t_disp = now; refresh_display(); }
#else
    (void)t_disp;
#endif
}
