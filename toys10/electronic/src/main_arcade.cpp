/* Desi Arcade: three games on one board. Hold a button while switching ON to choose: none/button 1 = Reflex Raja, button 2 = Taal Memory, button 3 = Aloo Bomb.
 * Hardware as main_toys.cpp: buttons D2..D5 (to GND), LEDs D6..D9, buzzer D10, noise seed from floating A0. LOW-VOLTAGE ONLY. */
#include <Arduino.h>
#include "toycore.h"
/* Pin maps: default = Nano bench wiring (buttons D2..D5, LEDs D6..D9, buzzer D10). -DPCB_REV_B = the Desi Arcade rev B board (utility10/pcb/boards/arcade.py):
 * buttons D0 D1 D2 A5, lamp LEDs A1..A4, buzzer D9, noise seed on A0. */
#ifdef PCB_REV_B
static const uint8_t BTN[4] = {0, 1, 2, A5}, LMP[4] = {A1, A2, A3, A4}; static const uint8_t BUZ = 9;
#else
static const uint8_t BTN[4] = {2, 3, 4, 5}, LMP[4] = {6, 7, 8, 9}; static const uint8_t BUZ = 10;
#endif
static uint32_t seed_from_noise() { uint32_t s = 0; for (int i = 0; i < 32; i++) { s = (s << 1) ^ (analogRead(A0) & 1); delayMicroseconds(40 + (i * 7)); } return s ^ micros() ^ 0x9E3779B9u; }
static uint8_t buttons() { uint8_t b = 0; for (int i = 0; i < 4; i++) if (digitalRead(BTN[i]) == LOW) b |= 1u << i; return b; }
static void leds(uint8_t mask) { for (int i = 0; i < 4; i++) digitalWrite(LMP[i], (mask >> i) & 1); }
static uint8_t game = 0; static rr_t rr; static tm_t tm; static ab_t ab; static uint32_t next_beep = 0; static const uint16_t FREQ[4] = {262, 330, 392, 523};
void setup() {
    for (int i = 0; i < 4; i++) { pinMode(BTN[i], INPUT_PULLUP); pinMode(LMP[i], OUTPUT); } pinMode(BUZ, OUTPUT);
    delay(50); uint8_t b = buttons(); game = (b & 2) ? 1 : (b & 4) ? 2 : 0;
    for (uint8_t k = 0; k <= game; k++) { leds(0x0F); tone(BUZ, 880, 80); delay(150); leds(0); delay(150); }    /* blink count = game number */
    uint32_t s = seed_from_noise(); rr_init(&rr, s); tm_init(&tm, s); ab_init(&ab, s);
    while (buttons()) {}
}
static void loop_reflex() { rr_step(&rr, millis(), buttons()); if (rr.st == RR_GO) { leds(0x0F); tone(BUZ, 1500); } else if (rr.st == RR_RESULT && rr.winner >= 0) { leds(1 << rr.winner); noTone(BUZ); } else { leds(0); noTone(BUZ); } }
static void loop_taal() {
    if (tm.showing) { delay(500); for (uint8_t i = 0; i < tm.len; i++) { uint8_t n = tm_note(&tm, i); leds(1 << n); tone(BUZ, FREQ[n]); delay(400); noTone(BUZ); leds(0); delay(150); } tm.showing = false; }
    uint8_t b = buttons(); if (!b) return; uint8_t pad = 0; while (!((b >> pad) & 1)) pad++;
    leds(1 << pad); tone(BUZ, FREQ[pad], 200); int r = tm_press(&tm, pad); while (buttons()) {} leds(0);
    if (r == 3) { for (uint8_t k = 0; k < tm.best; k++) { leds(0x0F); delay(120); leds(0); delay(120); } tm_init(&tm, seed_from_noise()); }
}
static void loop_aloo() {
    uint32_t now = millis(); ab_step(&ab, now);
    if (!ab.running && !ab.exploded && buttons()) { ab_start(&ab, now, 20000, 60000); delay(300); }
    if (ab.running && (int32_t)(now - next_beep) >= 0) { next_beep = now + ab_beep_interval_ms(&ab, now); tone(BUZ, 880, 40); leds(0x0F); delay(20); leds(0); }
    if (ab.exploded) { for (int i = 0; i < 20; i++) { tone(BUZ, 200 + 40 * i, 60); leds(i & 1 ? 0x0F : 0); delay(60); } leds(0); ab_init(&ab, seed_from_noise()); }
}
void loop() { if (game == 0) loop_reflex(); else if (game == 1) loop_taal(); else loop_aloo(); }
