/* Seeti Counter production firmware for the rev B board (ATmega328P-AU, 2 x AAA, F_CPU = 4 MHz).
 * Audio: Timer1 compare-match triggers the ADC at exactly 16 kS/s (no software timing jitter); the ADC ISR fills a 128-sample block (8 ms at 16 kS/s).
 * Detection: Goertzel at the whistle frequency (default 2800 Hz) -> seeti_block() counts whistles that last >= 400 ms.
 * Calibration: hold the button while switching on to enter SCAN mode: 30 s of Goertzel peak search 1.5-6 kHz printed on the UART (115200) and shown by LED blinks;
 *   the strongest bin is stored in EEPROM as the whistle frequency. Normal start reads it back.
 * Pins: ADC0 = amplifier (PC0), buzzer driver PB1, button PD2, LED PD7, UART header (PD0/PD1). Brown-out 1.8 V fuse. */
#include <Arduino.h>
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/eeprom.h>
#include "utilcore.h"
#define FS_HZ 16000UL
#define BLK 128
static volatile int16_t blk[2][BLK]; static volatile uint16_t pos = 0; static volatile uint8_t wr = 0, ready = 0xFF;
static seeti_t S; static uint16_t whistle_hz; static uint8_t target = 3; static const uint8_t PIN_BZ = 9, PIN_BTN = 2, PIN_LED = 7;
ISR(TIMER1_COMPB_vect) {}                                    /* needed so the compare flag is cleared and keeps triggering the ADC */
ISR(ADC_vect) { int16_t v = (int16_t)ADC - 512; blk[wr][pos++] = v; if (pos == BLK) { pos = 0; ready = wr; wr ^= 1; } }
static void adc_timer_start() {
    TCCR1A = 0; TCCR1B = _BV(WGM12) | _BV(CS10); OCR1A = F_CPU / FS_HZ - 1; OCR1B = F_CPU / FS_HZ - 1; TIMSK1 = _BV(OCIE1B);
    ADMUX = _BV(REFS0);                                      /* AVcc reference, channel 0 */
    ADCSRB = _BV(ADTS2) | _BV(ADTS0);                         /* auto-trigger source: Timer1 compare match B */
    ADCSRA = _BV(ADEN) | _BV(ADATE) | _BV(ADIE) | _BV(ADPS1) | _BV(ADPS0);   /* ADC clock F_CPU/8 = 500 kHz at 4 MHz */
}
static uint16_t vcc_mv() {                                    /* battery voltage from the 1.1 V bandgap (called rarely, interrupts the audio for ~2 ms) */
    uint8_t a = ADCSRA, m = ADMUX, b = ADCSRB; ADCSRA &= ~(_BV(ADATE) | _BV(ADIE)); ADMUX = _BV(REFS0) | 0x0E; delay(2);
    ADCSRA |= _BV(ADSC); while (ADCSRA & _BV(ADSC)) {} uint16_t r = ADC; ADMUX = m; ADCSRB = b; ADCSRA = a; return (uint16_t)(1125300UL / (r ? r : 1));
}
static bool take_block(float *tone, float *total, uint16_t hz) {
    uint8_t r; cli(); r = ready; ready = 0xFF; sei(); if (r == 0xFF) return false;
    static int16_t tmp[BLK]; for (uint16_t i = 0; i < BLK; i++) tmp[i] = blk[r][i];
    *tone = ut_goertzel(tmp, BLK, (float)hz, (float)FS_HZ); float t = 0; for (uint16_t i = 0; i < BLK; i++) t += (float)tmp[i] * tmp[i]; *total = t; return true;
}
static void beep(uint16_t ms, uint16_t f = 2400) { tone(PIN_BZ, f, ms); delay(ms + 20); }
static void scan_mode() {
    uint16_t best_hz = 0; float best = 0; uint32_t end = millis() + 30000UL; Serial.println(F("SCAN: whistle the cooker now"));
    while ((int32_t)(millis() - end) < 0) {
        float tone_p, total; if (!take_block(&tone_p, &total, 2800)) continue;
        for (uint16_t hz = 1500; hz <= 6000; hz += 100) {
            static int16_t tmp[BLK]; uint8_t r = wr ^ 1; for (uint16_t i = 0; i < BLK; i++) tmp[i] = blk[r][i];
            float p = ut_goertzel(tmp, BLK, (float)hz, (float)FS_HZ); float t2 = 0; for (uint16_t i = 0; i < BLK; i++) t2 += (float)tmp[i] * tmp[i];
            float ratio = t2 > 1000.0f ? p / (BLK * 0.5f * t2) : 0; if (ratio > best) { best = ratio; best_hz = hz; }
        }
        digitalWrite(PIN_LED, (millis() / 200) % 2);
    }
    Serial.print(F("best ")); Serial.print(best_hz); Serial.print(F(" Hz ratio ")); Serial.println(best, 3);
    if (best > 0.3f && best_hz) { eeprom_update_word((uint16_t *)0, best_hz); eeprom_update_word((uint16_t *)2, 0xA5A5); for (int i = 0; i < 3; i++) beep(150); } else beep(600, 300);
}
void setup() {
    clock_prescale_set(clock_div_2);                        /* 8 MHz RC / 2 = 4 MHz: valid down to 1.8 V */
    Serial.begin(115200); pinMode(PIN_BTN, INPUT_PULLUP); pinMode(PIN_LED, OUTPUT); pinMode(PIN_BZ, OUTPUT);
    whistle_hz = eeprom_read_word((uint16_t *)2) == 0xA5A5 ? eeprom_read_word((uint16_t *)0) : 2800; if (whistle_hz < 1000 || whistle_hz > 7000) whistle_hz = 2800;
    adc_timer_start(); sei(); delay(300);
    if (digitalRead(PIN_BTN) == LOW) { while (digitalRead(PIN_BTN) == LOW) {} scan_mode(); whistle_hz = eeprom_read_word((uint16_t *)0); }
    seeti_init(&S, target); for (uint8_t i = 0; i < target; i++) { beep(80); } Serial.print(F("whistle Hz ")); Serial.println(whistle_hz);
}
void loop() {
    static uint32_t last_v = 0, last_chirp = 0; static bool last_btn = true;
    float tone_p, total;
    if (take_block(&tone_p, &total, whistle_hz)) { seeti_block(&S, millis(), tone_p, total, BLK); digitalWrite(PIN_LED, S.in_whistle); }
    bool b = digitalRead(PIN_BTN); if (last_btn && !b) { target = target % 6 + 1; seeti_init(&S, target); for (uint8_t i = 0; i < target; i++) { beep(80); } } last_btn = b;
    if (S.done) { for (int i = 0; i < 5; i++) { beep(300); delay(300); } seeti_init(&S, target); }
    if (millis() - last_v > 10000UL) { last_v = millis(); uint16_t v = vcc_mv(); if (v < 2200 && millis() - last_chirp > 30000UL) { last_chirp = millis(); beep(40, 1500); } }
    set_sleep_mode(SLEEP_MODE_IDLE); sleep_mode();            /* wake on the next ADC interrupt */
}
