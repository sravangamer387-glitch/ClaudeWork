/* Utility-tool demos on Arduino Nano: compile with -DTOOL=1..8. LOW-VOLTAGE ONLY (USB power bank / 3 x AA). Serial 115200 prints readings for bench calibration.
 * 1 Seeti Counter  : mic module (MAX4466/electret amp) A0, buzzer D9, button D2 = target+1 (cycles 1..6), LED D13
 * 2 Gas Taraju     : HX711 DT D4 SCK D5 (4 load cells in a bridge under a 33 cm plate), LEDs D6 green D7 amber D8 red, buzzer D9. Serial: 'z' = zero (empty plate), 'c' = calibrate with a known 20 kg weight
 * 3 Fridge Door Guard: reed switch D2 to GND (magnet on the door closes the reed when shut: pin LOW = closed, HIGH = open), buzzer D9
 * 4 Bijli Meter Reader: photodiode/LDR + comparator or divider on A0 pointing at the meter's pulse LED, LED D13; set IMP_PER_KWH from the meter label
 * 5 Bijli Log      : mains-present sense D2 (5 V USB adapter through a divider, HIGH = mains ok), prints each cut
 * 6 Chulha Timers  : buttons D2..D5 add 1 minute to channels 1..4 (hold 1 s = acknowledge/clear), buzzer D9, serial display
 * 7 Rain Alert     : plate drive D5 (pulsed), plate sense A0 (higher = wetter, 100k pull-down), mute button D2, buzzer D9
 * 8 Tap Litre Meter: YF-S201-type hall flow sensor on D3 (interrupt), K = pulses per litre (set after a bucket test) */
#include <Arduino.h>
#include "utilcore.h"
#ifndef TOOL
#define TOOL 1
#endif
static void beep(int ms) { tone(9, 2400, ms); }
#if TOOL == 1
static seeti_t S; static uint8_t target = 3;
void setup() { Serial.begin(115200); pinMode(2, INPUT_PULLUP); pinMode(13, OUTPUT); seeti_init(&S, target); ADCSRA = (ADCSRA & 0xF8) | 0x04; /* ADC clock /16: ~60 kS/s raw, loop below paces to ~9 kHz */ }
void loop() {
    static int16_t buf[128]; const float fs = 8000; uint32_t t0 = micros();
    for (int i = 0; i < 128; i++) { buf[i] = (int16_t)analogRead(A0) - 512; while ((micros() - t0) < (uint32_t)((i + 1) * 125)) {} }
    float tone_p = ut_goertzel(buf, 128, 2800, fs); float tot = 0; for (int i = 0; i < 128; i++) tot += (float)buf[i] * buf[i];
    seeti_block(&S, millis(), tone_p, tot, 128); digitalWrite(13, S.in_whistle);
    static bool last = true; bool b = digitalRead(2); if (last && !b) { target = target % 6 + 1; seeti_init(&S, target); for (uint8_t i = 0; i < target; i++) { beep(80); delay(200); } } last = b;
    static uint16_t shown = 0; if (S.count != shown) { shown = S.count; Serial.print(F("whistles ")); Serial.println(shown); }
    if (S.done) { for (int i = 0; i < 5; i++) { beep(300); delay(500); } seeti_init(&S, target); }
}
#elif TOOL == 2
static gas_scale_t G;
static int32_t hx_read() { while (digitalRead(4)) {} int32_t v = 0; noInterrupts(); for (int i = 0; i < 24; i++) { digitalWrite(5, HIGH); delayMicroseconds(1); v = (v << 1) | digitalRead(4); digitalWrite(5, LOW); delayMicroseconds(1); } digitalWrite(5, HIGH); delayMicroseconds(1); digitalWrite(5, LOW); interrupts(); if (v & 0x800000) v |= 0xFF000000; return v; }
void setup() { Serial.begin(115200); pinMode(4, INPUT); pinMode(5, OUTPUT); for (int i = 6; i < 10; i++) pinMode(i, OUTPUT); gs_init(&G, 0, 22000, 15.3f, 14.2f); /* TODO calibrate: send z then c over serial; tare = stamped weight on the cylinder collar */ }
void loop() {
    int32_t c = hx_read(); gs_sample(&G, millis(), c);
    if (Serial.available()) { char ch = Serial.read(); static int32_t z = 0; if (ch == 'z') { z = c; G.zero_counts = c; Serial.println(F("zeroed")); } if (ch == 'c') { gs_calibrate(&G, z, c, 20.0f); Serial.print(F("counts/kg ")); Serial.println(G.counts_per_kg); } }
    static uint32_t nx = 0; if (millis() > nx) { nx = millis() + 2000; Serial.print(F("kg ")); Serial.print(G.w_kg, 2); Serial.print(G.stable ? F(" stable gas_kg ") : F(" moving gas_kg ")); Serial.print(gs_remaining_kg(&G), 2); Serial.print(F(" pct ")); Serial.println(gs_percent(&G)); }
    int p = gs_percent(&G); digitalWrite(6, G.stable && p > 30); digitalWrite(7, G.stable && p <= 30 && p > 15); digitalWrite(8, G.stable && p <= 15);
}
#elif TOOL == 3
static fd_t F;
void setup() { pinMode(2, INPUT_PULLUP); pinMode(9, OUTPUT); fd_init(&F, 60000UL, 180000UL); }
void loop() { fd_step(&F, millis(), digitalRead(2) == HIGH); if (F.sound == 1) beep(80); if (F.sound == 2) tone(9, 2000); else if (F.sound == 0) noTone(9); delay(50); }
#elif TOOL == 4
static bm_t M;
void setup() { Serial.begin(115200); pinMode(13, OUTPUT); bm_init(&M, 1600); /* TODO IMP_PER_KWH from the meter label */ }
void loop() {
    static int lo = 1023, hi = 0; int a = analogRead(A0); if (a < lo) lo = a; if (a > hi) hi = a; static uint32_t decay = 0; if (millis() > decay) { decay = millis() + 20000; lo++; hi--; }
    bool on = hi - lo > 40 && a < (lo + hi) / 2;                       /* board rev A: 10k pull-up + phototransistor to GND, so SIG goes LOW when the meter LED is lit */ digitalWrite(13, on); bm_sample(&M, millis(), on);
    static uint32_t nx = 0; if (millis() > nx) { nx = millis() + 10000; Serial.print(F("kWh ")); Serial.print(bm_kwh(&M), 3); Serial.print(F("  W ")); Serial.print(bm_watts(&M, millis()), 0); Serial.print(F("  bill~Rs ")); Serial.println(bm_bill(&M, bm_kwh(&M)), 1); }
    delay(2);
}
#elif TOOL == 5
static pc_t P;
void setup() { Serial.begin(115200); pinMode(2, INPUT); pc_init(&P); }
void loop() { static uint32_t last = 0; if (millis() - last >= 1000) { last += 1000; bool was = P.out; pc_sample(&P, millis() / 1000, digitalRead(2) == HIGH); if (was && !P.out) { uint8_t i = (P.head + PC_LOG - 1) % PC_LOG; Serial.print(F("cut #")); Serial.print(P.count); Serial.print(F(" lasted s ")); Serial.println(P.dur_s[i]); } } }
#elif TOOL == 6
static ct_t C; static uint32_t press[4];
void setup() { Serial.begin(115200); for (int i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); pinMode(9, OUTPUT); ct_init(&C); }
void loop() {
    uint32_t now = millis();
    for (uint8_t i = 0; i < 4; i++) { bool d = digitalRead(2 + i) == LOW; if (d && !press[i]) press[i] = now ? now : 1; if (!d && press[i]) { if (now - press[i] < 1000) ct_add(&C, i, now, 60); press[i] = 0; } if (d && press[i] && now - press[i] >= 1000) { ct_ack(&C, i); press[i] = now + 3600000UL; } }
    uint8_t r = ct_step(&C, now); if (r) { if ((now / 250) % 2) tone(9, 2000); else noTone(9); } else noTone(9);
    static uint32_t nx = 0; if (now > nx) { nx = now + 1000; for (uint8_t i = 0; i < 4; i++) { uint32_t s = ct_remaining_s(&C, i, now); Serial.print(i + 1); Serial.print(':'); Serial.print(s / 60); Serial.print('m'); Serial.print(s % 60); Serial.print(F("s ")); } Serial.println(); }
}
#elif TOOL == 7
static rain_t R;
void setup() { pinMode(2, INPUT_PULLUP); pinMode(9, OUTPUT); rain_init(&R); R.wet_thr = 400; R.dry_thr = 250; /* TODO tune on your plate */ }
void loop() { pinMode(5, OUTPUT); digitalWrite(5, HIGH); delay(2); uint16_t v = analogRead(A0); digitalWrite(5, LOW);          /* board rev A drives the plate only for ~2 ms per reading (limits corrosion) */
    rain_step(&R, millis(), v, digitalRead(2) == LOW); if (R.alert && (millis() / 400) % 2) tone(9, 1800); else noTone(9); delay(20); }
#else
static tap_t T; static volatile uint32_t pulses;
static void isr() { pulses++; }
void setup() { Serial.begin(115200); pinMode(3, INPUT_PULLUP); attachInterrupt(digitalPinToInterrupt(3), isr, FALLING); tap_init(&T, 450.0f); T.target_l = 10; /* TODO K from a bucket test */ }
void loop() { noInterrupts(); uint32_t n = pulses; pulses = 0; interrupts(); tap_pulses(&T, millis(), n); tap_step(&T, millis()); if (T.target_hit) { beep(100); } static uint32_t nx = 0; if (millis() > nx) { nx = millis() + 2000; Serial.print(F("session L ")); Serial.print(tap_session_l(&T), 2); Serial.print(F(" today L ")); Serial.println(tap_day_l(&T), 1); } delay(20); }
#endif
