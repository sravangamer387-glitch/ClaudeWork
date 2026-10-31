/* Gas-Suraksha DEMO on Arduino Nano -- *** NOT A SAFETY DEVICE, NOT CERTIFIED, uses a hobby MQ-6 module ***.
 * MQ-6 module AO -> A0; buzzer (active) D8; green LED D9; amber D10; red D11; silence button D2 and test button D3 (to GND).
 * Serial 115200 prints counts/state every 10 s so you can calibrate: record clean-air counts, then counts in a gas-test
 * enclosure (lighter gas released into a bag, NEVER near ignition) and set cfg below. */
#include <Arduino.h>
#include <avr/wdt.h>
#include "gas_core.h"
static gas_t g; static gas_cfg_t cfg;
void setup() {
    bool wd = (MCUSR & (1 << WDRF)) != 0; MCUSR = 0; wdt_disable();
    pinMode(8, OUTPUT); pinMode(9, OUTPUT); pinMode(10, OUTPUT); pinMode(11, OUTPUT); pinMode(2, INPUT_PULLUP); pinMode(3, INPUT_PULLUP);
    Serial.begin(115200); gas_default_cfg(&cfg);      /* TODO: cfg.clean_air_nominal / alarm_delta / alarm_abs from your own calibration */
    gas_init(&g, &cfg, millis(), wd); wdt_enable(WDTO_2S);
}
void loop() {
    static uint32_t next = 0, next_print = 0;
    uint32_t now = millis();
    if ((int32_t)(now - next) >= 0) {
        next += 1000; wdt_reset();
        gas_inputs_t in = {0}; in.adc = (uint16_t)analogRead(A0); in.button_silence = digitalRead(2) == LOW; in.button_test = digitalRead(3) == LOW;
        gas_step(&g, now, in);
        digitalWrite(9, g.led == 1); digitalWrite(10, g.led == 2 || (g.led == 4 && (now / 500) % 2)); digitalWrite(11, g.led == 3);
        if (now >= next_print) { next_print = now + 10000; Serial.print(F("adc ")); Serial.print(in.adc); Serial.print(F(" delta ")); Serial.print(gas_delta(&g, in.adc)); Serial.print(F(" state ")); Serial.println((int)g.st); }
    }
    uint16_t ph = now % 1000;                     /* buzzer pattern, evaluated continuously */
    bool on = g.buzzer == BZ_CONTINUOUS || (g.buzzer == BZ_SLOW && ph < 150) || (g.buzzer == BZ_CHIRP && ph < 60);
    digitalWrite(8, on ? HIGH : LOW);
}
