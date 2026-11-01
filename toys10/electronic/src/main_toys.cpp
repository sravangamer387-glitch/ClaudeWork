/* One sketch, four toys: compile with -DTOY=1 Reflex Raja, 2 Taal Memory, 3 Aloo Bomb, 4 Beat Runner.
 * Buttons D2..D5 (to GND, INPUT_PULLUP), LEDs D6..D9 (330 ohm), active/passive buzzer D10 (tone), start/pass button = any of D2..D5.
 * Beat Runner: two 74HC595 daisy-chained LED rows: data D11, clock D12, latch D13; play button D2.
 * LOW-VOLTAGE ONLY: 3 x AAA (4.5 V) or USB power bank. */
#include <Arduino.h>
#include "toycore.h"
#ifndef BUZ
#define BUZ 10     /* buzzer pin: 10 on the Nano bench wiring; the Beat Runner rev B board uses D9 (build with -DBUZ=9) */
#endif
#ifndef TOY
#define TOY 1
#endif
static uint32_t seed_from_noise() { uint32_t s = 0; for (int i = 0; i < 32; i++) { s = (s << 1) ^ (analogRead(A0) & 1); delayMicroseconds(40 + (i * 7)); } return s ^ micros() ^ 0x9E3779B9u; }
static uint8_t buttons() { uint8_t b = 0; for (int i = 0; i < 4; i++) if (digitalRead(2 + i) == LOW) b |= 1u << i; return b; }
static void leds(uint8_t mask) { for (int i = 0; i < 4; i++) digitalWrite(6 + i, (mask >> i) & 1); }
#if TOY == 1
static rr_t g;
void setup() { for (int i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); for (int i = 6; i < 11; i++) pinMode(i, OUTPUT); rr_init(&g, seed_from_noise()); }
void loop() { rr_step(&g, millis(), buttons()); if (g.st == RR_GO) { leds(0x0F); tone(BUZ, 1500); } else if (g.st == RR_RESULT && g.winner >= 0) { leds(1 << g.winner); noTone(BUZ); } else { leds(0); noTone(BUZ); } }
#elif TOY == 2
static tm_t g; static const uint16_t FREQ[4] = {262, 330, 392, 523};
void setup() { for (int i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); for (int i = 6; i < 11; i++) pinMode(i, OUTPUT); tm_init(&g, seed_from_noise()); }
void loop() {
    if (g.showing) { delay(500); for (uint8_t i = 0; i < g.len; i++) { uint8_t n = tm_note(&g, i); leds(1 << n); tone(BUZ, FREQ[n]); delay(400); noTone(BUZ); leds(0); delay(150); } g.showing = false; }
    uint8_t b = buttons(); if (!b) return; uint8_t pad = 0; while (!((b >> pad) & 1)) pad++;
    leds(1 << pad); tone(BUZ, FREQ[pad], 200); int r = tm_press(&g, pad); while (buttons()) {} leds(0);
    if (r == 3) { for (uint8_t k = 0; k < g.best; k++) { leds(0x0F); delay(120); leds(0); delay(120); } tm_init(&g, seed_from_noise()); }
}
#elif TOY == 3
static ab_t g; static uint32_t next_beep = 0;
void setup() { for (int i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); for (int i = 6; i < 11; i++) pinMode(i, OUTPUT); ab_init(&g, seed_from_noise()); }
void loop() {
    uint32_t now = millis(); ab_step(&g, now);
    if (!g.running && !g.exploded && buttons()) { ab_start(&g, now, 20000, 60000); delay(300); }
    if (g.running && (int32_t)(now - next_beep) >= 0) { next_beep = now + ab_beep_interval_ms(&g, now); tone(BUZ, 880, 40); leds(0x0F); delay(20); leds(0); }
    if (g.exploded) { for (int i = 0; i < 20; i++) { tone(BUZ, 200 + 40 * i, 60); leds(i & 1 ? 0x0F : 0); delay(60); } leds(0); ab_init(&g, seed_from_noise()); }
}
#else
static br_t g; static void show(uint16_t v) { digitalWrite(13, LOW); shiftOut(11, 12, MSBFIRST, v >> 8); shiftOut(11, 12, MSBFIRST, v & 0xFF); digitalWrite(13, HIGH); }
void setup() { pinMode(2, INPUT_PULLUP); pinMode(BUZ, OUTPUT); pinMode(11, OUTPUT); pinMode(12, OUTPUT); pinMode(13, OUTPUT); br_init(&g, seed_from_noise()); }
void loop() {
    static bool last = false; uint32_t now = millis(); br_step(&g, now); show(g.notes);
    bool p = digitalRead(2) == LOW; if (p && !last) { int pts = br_press(&g); tone(BUZ, pts == 3 ? 1047 : pts == 1 ? 784 : 150, 60); } last = p;
    if (g.over) { show(0xFFFF); delay(1500); br_init(&g, seed_from_noise()); }
}
#endif
