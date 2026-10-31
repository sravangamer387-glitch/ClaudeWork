/* Jal-Rakshak prototype on Arduino Nano. LOW-VOLTAGE ONLY: drive a 12 V mini pump or an LED, never mains.
 * Probes use AC excitation (no electrolysis/corrosion): common electrode driven D7, sense pins D8 (sump), D9 (tank LOW), D10 (tank FULL),
 * each sense pin pulled to GND with 100k. A probe is wet only if the sense pin follows the drive pin HIGH and LOW.
 * Outputs: D6 pump relay/MOSFET, D13 status LED (blink count = status code), D12 buzzer on faults. Button D2 (to GND) clears faults. */
#include <Arduino.h>
#include "jal_core.h"

#define DRIVE 7
static const uint8_t SENSE[3] = {8, 9, 10};
static jal_t jal; static jal_cfg_t cfg;

static bool wet(uint8_t pin) {
    digitalWrite(DRIVE, HIGH); delayMicroseconds(300); bool a = digitalRead(pin);
    digitalWrite(DRIVE, LOW);  delayMicroseconds(300); bool b = digitalRead(pin);
    return a && !b;
}
void setup() {
    pinMode(DRIVE, OUTPUT); digitalWrite(DRIVE, LOW);
    for (uint8_t i = 0; i < 3; i++) pinMode(SENSE[i], INPUT);
    pinMode(6, OUTPUT); pinMode(13, OUTPUT); pinMode(12, OUTPUT); pinMode(2, INPUT_PULLUP);
    jal_default_cfg(&cfg); jal_init(&jal, &cfg, millis());
}
void loop() {
    static uint32_t next = 0;
    uint32_t now = millis();
    if ((int32_t)(now - next) >= 0) {
        next = now + 100;
        jal_inputs_t in = {wet(SENSE[0]), wet(SENSE[1]), wet(SENSE[2])};
        if (digitalRead(2) == LOW) jal_reset_faults(&jal, now);
        jal_step(&jal, now, in);
        digitalWrite(6, jal_pump(&jal) ? HIGH : LOW);
        uint8_t code = jal_status_code(&jal);                              /* blink code: N short blinks then a 1.5 s pause */
        uint32_t phase = now % (uint32_t)(code * 400u + 1500u);
        digitalWrite(13, (phase < (uint32_t)code * 400u && (phase % 400u) < 200u) ? HIGH : LOW);
        digitalWrite(12, (code >= 3 && (now % 2000u) < 150u) ? HIGH : LOW);   /* short beep every 2 s while faulted */
    }
}
