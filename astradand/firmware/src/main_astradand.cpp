/* ASTRADAND wand firmware for the rev A board (ATmega328P-AU, 3.3 V, internal 8 MHz RC, fuses lfuse 0xE2 hfuse 0xD9 efuse 0xFD).
 * Pins (from utility10/pcb/boards/astradand.py): D2 IMU INT (active low, latched), D3 TRIGGER (to GND), D4 haptic transistor, D5 LED supply switch (high = on),
 * D6 WS2812B data, D9/D10 piezo (OC1A/OC1B, driven in antiphase), A0 battery divider (330k/100k, 1.1 V reference), A4/A5 I2C to the MPU-6050 (0x68).
 * STATUS: compiles and fits; the recogniser/spell/LED/sound engine in lib/ad_core.c is host-tested (83 checks); the MPU-6050 register sequence, the WS2812
 * bit-bang timing and the wake-on-motion sleep were written from the datasheets and have NEVER run on hardware: bring-up item 1 of the test plan. */
#include <Arduino.h>
#include <Wire.h>
#include <avr/sleep.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include "ad_core.h"
#define PIN_INT 2
#define PIN_TRIG 3
#define PIN_HAPT 4
#define PIN_LEDEN 5
#define PIN_LEDDIN 6
#define MPU 0x68
static ad_gesture_t gest; static ad_game_t game; static ad_power_t pwr;
static uint32_t cast_ms = 0; static int cast_spell = -1; static bool cast_combo = false;
static const ad_note_t *seq = 0; static int seq_n = 0, seq_i = 0; static uint32_t seq_next = 0; static uint32_t haptic_until = 0;
/* ---------------- MPU-6050 ---------------- */
static void wr(uint8_t reg, uint8_t v) { Wire.beginTransmission(MPU); Wire.write(reg); Wire.write(v); Wire.endTransmission(); }
static void imu_active() {
    wr(0x6B, 0x01);                 /* wake, PLL on gyro X */
    wr(0x6C, 0x00);                 /* all axes on */
    wr(0x1A, 0x03);                 /* DLPF 44 Hz */
    wr(0x19, 19);                   /* 1 kHz / 20 = 50 Hz */
    wr(0x1B, 0x10);                 /* gyro +-1000 dps */
    wr(0x1C, 0x00);                 /* accel +-2 g */
    wr(0x38, 0x00);                 /* no interrupts while awake */
}
static void imu_motion_wake() {     /* accel-only low power cycling with motion interrupt (INT active low, latched) */
    wr(0x6B, 0x00); wr(0x6C, 0x07); /* gyro axes in standby */
    wr(0x1C, 0x01);                 /* HPF 5 Hz, +-2 g */
    wr(0x1F, 12); wr(0x20, 1); wr(0x69, 0x15);   /* motion threshold ~24 mg, duration 1 ms, decrement counters */
    wr(0x37, 0xA0);                 /* INT active low, push-pull, latched until INT_STATUS is read */
    wr(0x38, 0x40);                 /* motion interrupt enable */
    wr(0x6C, 0x47); wr(0x6B, 0x28); /* LP wake 1.25 Hz, gyro standby; CYCLE=1, temp disabled */
}
static bool imu_read(ad_imu_t *m) {
    Wire.beginTransmission(MPU); Wire.write(0x3B); if (Wire.endTransmission(false) != 0) return false;
    if (Wire.requestFrom(MPU, 14) != 14) return false;
    int16_t v[7]; for (int i = 0; i < 7; i++) { uint8_t h = Wire.read(), l = Wire.read(); v[i] = (int16_t)((h << 8) | l); }
    m->ax = v[0]; m->ay = v[1]; m->az = v[2]; m->gx = v[4]; m->gy = v[5]; m->gz = v[6]; return true;
}
/* ---------------- WS2812B (8 MHz: 3-cycle '0', 6-cycle '1', 11 cycles per bit) ---------------- */
static inline void ws_byte(uint8_t b, uint8_t hi, uint8_t lo) {
    uint8_t n = 8;
    asm volatile("1: out %[p], %[hi]\n nop\n sbrs %[b], 7\n out %[p], %[lo]\n nop\n nop\n out %[p], %[lo]\n lsl %[b]\n dec %[n]\n brne 1b\n"
                 : [b] "+r"(b), [n] "+r"(n) : [p] "I"(_SFR_IO_ADDR(PORTD)), [hi] "r"((uint8_t)(PORTD | _BV(6))), [lo] "r"((uint8_t)(PORTD & ~_BV(6))));
    (void)hi; (void)lo;
}
static void leds_show(const ad_rgb_t px[AD_LEDS]) {
    uint8_t hi = PORTD | _BV(6), lo = PORTD & ~_BV(6); uint8_t sreg = SREG; cli();
    for (int i = 0; i < AD_LEDS; i++) { ws_byte(px[i].g, hi, lo); ws_byte(px[i].r, hi, lo); ws_byte(px[i].b, hi, lo); }
    SREG = sreg; delayMicroseconds(80);
}
static void leds_power(bool on) { digitalWrite(PIN_LEDEN, on ? HIGH : LOW); if (!on) digitalWrite(PIN_LEDDIN, LOW); }
/* ---------------- piezo: Timer1 CTC toggling OC1A/OC1B in antiphase ---------------- */
static void piezo_stop() { TCCR1A = 0; TCCR1B = 0; PORTB &= ~(_BV(1) | _BV(2)); }
static void piezo_hz(uint16_t hz) {
    if (hz == 0) { piezo_stop(); return; }
    uint16_t top = (uint16_t)((F_CPU / 16UL / hz) - 1); piezo_stop(); PORTB |= _BV(1); PORTB &= ~_BV(2); TCNT1 = 0; OCR1A = top; OCR1B = top;
    TCCR1A = _BV(COM1A0) | _BV(COM1B0); TCCR1B = _BV(WGM12) | _BV(CS11);                    /* prescaler 8, toggle on compare */
}
static void sound_start(int spell, bool combo) { seq_n = ad_sound(spell, combo, &seq); seq_i = 0; seq_next = millis(); }
static void sound_step(uint32_t now) {
    if (!seq || seq_i > seq_n) return;
    if ((int32_t)(now - seq_next) < 0) return;
    if (seq_i == seq_n) { piezo_stop(); seq_i++; return; }
    piezo_hz(ad_note_hz(&seq[seq_i])); seq_next = now + ad_note_ms(&seq[seq_i]); seq_i++;
}
static int battery_mv() { analogReference(INTERNAL); delay(2); (void)analogRead(A0); long a = analogRead(A0); analogReference(DEFAULT); return (int)(a * 4624L / 1000L); }
static void go_to_sleep() {
    leds_power(false); piezo_stop(); digitalWrite(PIN_HAPT, LOW); imu_motion_wake();
    uint8_t dummy; Wire.beginTransmission(MPU); Wire.write(0x3A); Wire.endTransmission(false); Wire.requestFrom(MPU, 1); dummy = Wire.read(); (void)dummy;     /* clear the latched interrupt */
    ADCSRA &= ~_BV(ADEN); set_sleep_mode(SLEEP_MODE_PWR_DOWN); sleep_enable();
    EIFR = _BV(INTF0) | _BV(INTF1); attachInterrupt(0, [] {}, LOW); attachInterrupt(1, [] {}, LOW);
    sleep_bod_disable(); sei(); sleep_cpu(); sleep_disable(); detachInterrupt(0); detachInterrupt(1); ADCSRA |= _BV(ADEN);
    imu_active(); leds_power(true); ad_power_init(&pwr, millis()); ag_init(&gest);
}
void setup() {
    pinMode(PIN_INT, INPUT_PULLUP); pinMode(PIN_TRIG, INPUT_PULLUP); pinMode(PIN_HAPT, OUTPUT); pinMode(PIN_LEDEN, OUTPUT); pinMode(PIN_LEDDIN, OUTPUT); pinMode(9, OUTPUT); pinMode(10, OUTPUT);
    Wire.begin(); Wire.setClock(400000); imu_active(); ag_init(&gest); ad_game_init(&game); ad_power_init(&pwr, millis()); leds_power(true);
    sound_start(-4, false);
}
void loop() {
    static uint32_t next = 0; uint32_t now = millis(); sound_step(now);
    if ((int32_t)(now - next) < 0) return; next += 20;                                                   /* 50 Hz */
    ad_imu_t m; bool ok = imu_read(&m); bool trig = digitalRead(PIN_TRIG) == LOW;
    if (!ok) { memset(&m, 0, sizeof m); m.az = 16384; }
    ad_game_tick(&game, now);
    if (!ad_power_step(&pwr, now, &m, trig)) { go_to_sleep(); next = millis(); return; }
    int r = ag_step(&gest, &m, trig, NULL, NULL);
    if (r != AG_NONE) {
        ad_cast_t c = ad_cast(&game, now, r);
        if (c.ok) { cast_spell = r; cast_combo = c.combo; cast_ms = now; sound_start(r, c.combo); haptic_until = now + 120; }
        else { cast_spell = -1; sound_start(-1, false); haptic_until = now + 40; }
    }
    static uint32_t lowchk = 0; static bool low = false; if (now - lowchk > 5000) { lowchk = now; low = ad_battery_low(battery_mv()); if (low && !trig) sound_start(-3, false); }
    digitalWrite(PIN_HAPT, (int32_t)(haptic_until - now) > 0 ? HIGH : LOW);
    ad_rgb_t px[AD_LEDS]; ad_led_frame(&game, now, cast_ms, cast_spell, cast_combo, low, px);
    if (trig && cast_spell < 0) { for (int i = 0; i < AD_LEDS; i++) { px[i].r = 0; px[i].g = 10; px[i].b = 40; } }   /* drawing: dim blue ready glow */
    leds_show(px);
}
