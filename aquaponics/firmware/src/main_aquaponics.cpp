// Aquaponics controller skeleton on the BioTray board (ESP32-S3). NOT compiled for the ESP32, never run on hardware.
// All decisions live in ../lib/aq_core.c (host-tested). Channel map on BioTray: PUMP1 = circulation pump, PUMP2 = pH dosing pump (peristaltic),
// FAN = aerator relay (12 V coil, flyback diode on board), LIGHT = optional grow light. DO probe: analog module read through an ADS1115 on the I2C header.
#include <Arduino.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Adafruit_ADS1X15.h>
extern "C" {
#include "aq_core.h"
}
#include "../../../biotray/firmware/src/biotray_pins.h"

static OneWire ow(PIN_ONEWIRE); static DallasTemperature ds(&ow); static Adafruit_ADS1115 ads;
static aq_trend_t t_ph, t_do, t_temp; static aq_stuck_t k_ph, k_do, k_temp; static aq_dose_t dose; static bool aer_on = false;
static const aq_dose_cfg_t DOSE = {7.0f, 0.15f, 20, 1800, 400};                      // pH setpoint 7.0, +-0.15 dead-band, 20 s pulses, 30 min apart, 400 s/day cap
static const float PH_LO = 6.4f, PH_HI = 7.8f, DO_LO_MGL = 5.0f, T_HI = 30.0f;     // PLACEHOLDER limits: use the values for YOUR fish and plants
static uint32_t pulse_end_ms = 0;
static float ph_from_volts(float v) { return 7.0f + (2.5f - v) * (3.0f / 0.5f) / 6.0f * 6.0f * 0.5f; }   // PLACEHOLDER: replace with a two-point calibration (bt_cal_apply from biotray)
void setup() { Serial.begin(115200); pinMode(PIN_PUMP1, OUTPUT); pinMode(PIN_PUMP2, OUTPUT); pinMode(PIN_FAN, OUTPUT); digitalWrite(PIN_PUMP1, HIGH); Wire.begin(PIN_SDA, PIN_SCL); ads.begin(); ds.begin();
    aq_trend_init(&t_ph, 0.3f, 0.1f); aq_trend_init(&t_do, 0.3f, 0.1f); aq_trend_init(&t_temp, 0.3f, 0.1f); aq_dose_init(&dose); }
void loop() {
    static uint32_t last = 0; uint32_t now = millis(); if (pulse_end_ms && (int32_t)(now - pulse_end_ms) >= 0) { digitalWrite(PIN_PUMP2, LOW); pulse_end_ms = 0; }
    if (now - last < 10000) return; last = now;                                         // 10 s control tick; trend samples every 10 min (every 60th tick)
    ds.requestTemperatures(); float temp = ds.getTempCByIndex(0); float ph = ph_from_volts(analogReadMilliVolts(PIN_PH_ADC) / 1000.0f);
    float do_v = ads.computeVolts(ads.readADC_SingleEnded(0)); float do_mgl = do_v * 10.0f;                         // PLACEHOLDER scale: calibrate in air-saturated water
    bool ok_ph = aq_sensor_ok(&k_ph, ph, 3.0f, 11.0f, 360), ok_do = aq_sensor_ok(&k_do, do_mgl, 0.0f, 20.0f, 360), ok_t = aq_sensor_ok(&k_temp, temp, 2.0f, 40.0f, 720);
    static int tick = 0; if (++tick >= 60) { tick = 0; if (ok_ph) aq_trend_push(&t_ph, ph); if (ok_do) aq_trend_push(&t_do, do_mgl); if (ok_t) aq_trend_push(&t_temp, temp); }
    int b_ph = aq_steps_to_breach(&t_ph, PH_LO, PH_HI, 2.0f, 12), b_do = aq_steps_to_breach(&t_do, DO_LO_MGL, 99.0f, 2.0f, 12), b_t = aq_steps_to_breach(&t_temp, 0.0f, T_HI, 2.0f, 12);   // 12 samples = 2 h ahead
    aer_on = aq_aerator(aer_on, do_mgl, aq_do_sat_mgl(temp), 0.6f, 0.9f) || (b_do >= 0); digitalWrite(PIN_FAN, aer_on);   // also pre-emptively aerate when the DO forecast breaches
    int pulse = aq_dose_step(&dose, &DOSE, ph, ok_ph, false, 10); if (pulse && !pulse_end_ms) { digitalWrite(PIN_PUMP2, HIGH); pulse_end_ms = now + pulse * 1000UL; }
    Serial.printf("T=%.1f pH=%.2f DO=%.2f aer=%d forecast_breach pH=%d DO=%d T=%d lockout=%d\n", temp, ph, do_mgl, aer_on, b_ph, b_do, b_t, dose.lockout);   // publish via MQTT as in BioTray
}
