/* Kheti-Mitra prototype on Arduino Nano. LOW-VOLTAGE: 12 V solenoid valve through a logic-level MOSFET (flyback diode across the valve!).
 * Soil sensors (capacitive, analog) on A0 and A1; rain sensor module digital output on D3 (LOW = wet); valve MOSFET gate D6;
 * status LED D13; hold button D2 (to GND, press to toggle hold). Serial 115200 prints % moisture every 10 s for calibration:
 * put each sensor in dry air and in water and set cfg.dry_adc / cfg.wet_adc below. */
#include <Arduino.h>
#include "kheti_core.h"

static kheti_t k; static kheti_cfg_t cfg; static bool hold = false;
void setup() {
    pinMode(6, OUTPUT); pinMode(13, OUTPUT); pinMode(3, INPUT_PULLUP); pinMode(2, INPUT_PULLUP);
    Serial.begin(115200);
    kheti_default_cfg(&cfg);                       /* TODO per sensor: cfg.dry_adc[i] = <counts in air>, cfg.wet_adc[i] = <counts in water> */
    kheti_init(&k, &cfg, millis());
}
void loop() {
    static uint32_t next = 0, next_print = 0; static bool last_btn = true;
    uint32_t now = millis();
    bool btn = digitalRead(2); if (last_btn && !btn) hold = !hold; last_btn = btn;
    if ((int32_t)(now - next) >= 0) {
        next = now + 1000;
        kheti_inputs_t in; in.adc[0] = (uint16_t)analogRead(A0); in.adc[1] = (uint16_t)analogRead(A1);
        in.rain_wet = digitalRead(3) == LOW; in.manual_hold = hold;
        kheti_step(&k, now, in);
        digitalWrite(6, kheti_valve(&k) ? HIGH : LOW);
        uint8_t code = kheti_status_code(&k); uint32_t ph = now % (uint32_t)(code * 400u + 1500u);
        digitalWrite(13, (ph < (uint32_t)code * 400u && (ph % 400u) < 200u) ? HIGH : LOW);
        if (now >= next_print) { next_print = now + 10000; Serial.print(F("moisture% ")); Serial.print(k.last_pct_x10 / 10.0, 1); Serial.print(F(" valve ")); Serial.print(kheti_valve(&k)); Serial.print(F(" status ")); Serial.println(code); }
    }
}
