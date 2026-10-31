/* Desi Arcade: three games on one board. Hold a button while switching ON to choose: none/button 1 = Reflex Raja, button 2 = Taal Memory, button 3 = Aloo Bomb.
 * Hardware as main_toys.cpp: buttons D2..D5 (to GND), LEDs D6..D9, buzzer D10, noise seed from floating A0. LOW-VOLTAGE ONLY. */
#include <Arduino.h>
#include "toycore.h"
static uint32_t seed_from_noise() { uint32_t s = 0; for (int i = 0; i < 32; i++) { s = (s << 1) ^ (analogRead(A0) & 1); delayMicroseconds(40 + (i * 7)); } return s ^ micros() ^ 0x9E3779B9u; }
static uint8_t buttons() { uint8_t b = 0; for (int i = 0; i < 4; i++) if (digitalRead(2 + i) == LOW) b |= 1u << i; return b; }
static void leds(uint8_t mask) { for (int i = 0; i < 4; i++) digitalWrite(6 + i, (mask >> i) & 1); }
static uint8_t game = 0; static rr_t rr; static tm_t tm; static ab_t ab; static uint32_t next_beep = 0; static const uint16_t FREQ[4] = {262, 330, 392, 523};
void setup() {
    for (int i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); for (int i = 6; i < 11; i++) pinMode(i, OUTPUT);
    delay(50); uint8_t b = buttons(); game = (b & 2) ? 1 : (b & 4) ? 2 : 0;
    for (uint8_t k = 0; k <= game; k++) { leds(0x0F); tone(10, 880, 80); delay(150); leds(0); delay(150); }    /* blink count = game number */
    uint32_t s = seed_from_noise(); rr_init(&rr, s); tm_init(&tm, s); ab_init(&ab, s);
    while (buttons()) {}
}
static void loop_reflex() { rr_step(&rr, millis(), buttons()); if (rr.st == RR_GO) { leds(0x0F); tone(10, 1500); } else if (rr.st == RR_RESULT && rr.winner >= 0) { leds(1 << rr.winner); noTone(10); } else { leds(0); noTone(10); } }
static void loop_taal() {
    if (tm.showing) { delay(500); for (uint8_t i = 0; i < tm.len; i++) { uint8_t n = tm_note(&tm, i); leds(1 << n); tone(10, FREQ[n]); delay(400); noTone(10); leds(0); delay(150); } tm.showing = false; }
    uint8_t b = buttons(); if (!b) return; uint8_t pad = 0; while (!((b >> pad) & 1)) pad++;
    leds(1 << pad); tone(10, FREQ[pad], 200); int r = tm_press(&tm, pad); while (buttons()) {} leds(0);
    if (r == 3) { for (uint8_t k = 0; k < tm.best; k++) { leds(0x0F); delay(120); leds(0); delay(120); } tm_init(&tm, seed_from_noise()); }
}
static void loop_aloo() {
    uint32_t now = millis(); ab_step(&ab, now);
    if (!ab.running && !ab.exploded && buttons()) { ab_start(&ab, now, 20000, 60000); delay(300); }
    if (ab.running && (int32_t)(now - next_beep) >= 0) { next_beep = now + ab_beep_interval_ms(&ab, now); tone(10, 880, 40); leds(0x0F); delay(20); leds(0); }
    if (ab.exploded) { for (int i = 0; i < 20; i++) { tone(10, 200 + 40 * i, 60); leds(i & 1 ? 0x0F : 0); delay(60); } leds(0); ab_init(&ab, seed_from_noise()); }
}
void loop() { if (game == 0) loop_reflex(); else if (game == 1) loop_taal(); else loop_aloo(); }
