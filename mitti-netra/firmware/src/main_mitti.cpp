// MITTI-NETRA firmware skeleton (ESP32-S3, Arduino-ESP32 core 2.x). NOT compiled for the ESP32 and not run on hardware.
// The decision logic is in ../lib/mn_core.c (host-tested). The cellular part is an outline: see docs/DESIGN.md.
#include <Arduino.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <esp_sleep.h>
extern "C" {
#include "mn_core.h"
}
#include "mitti_pins.h"

static OneWire ow(PIN_ONEWIRE); static DallasTemperature ds(&ow);
static mn_soil_cal_t SOIL = {2800, 1200};                                   // PLACEHOLDER ADC counts: measure in dry air and in water
static mn_strain_cfg_t STRAIN = {3.3f, 3.3f, 128.0f, 2.0f, 4.0f};          // excitation 3.3 V, AVDD 3.3 V, gain 128, GF 2.0, quarter bridge: set to your wiring
static mn_thresh_t TILT_T = {0.3f, 1.0f, 0.1f, 3}, STRAIN_T = {150.0f, 400.0f, 30.0f, 3};   // degrees of drift, microstrain: tune per structure
RTC_DATA_ATTR static mn_alarm_t tilt_alarm, strain_alarm; RTC_DATA_ATTR static float base_roll = NAN, base_pitch = NAN; RTC_DATA_ATTR static int32_t strain_zero = 0; RTC_DATA_ATTR static uint32_t boots = 0;

static bool adxl_read(float *ax, float *ay, float *az) {                      // ADXL345 at 0x53, DATAX0..DATAZ1
    Wire.beginTransmission(0x53); Wire.write(0x32); if (Wire.endTransmission(false)) return false; if (Wire.requestFrom(0x53, 6) != 6) return false;
    int16_t x = Wire.read() | Wire.read() << 8, y = Wire.read() | Wire.read() << 8, z = Wire.read() | Wire.read() << 8; *ax = x * 0.0039f; *ay = y * 0.0039f; *az = z * 0.0039f; return true; }
static void adxl_init() { Wire.beginTransmission(0x53); Wire.write(0x2D); Wire.write(0x08); Wire.endTransmission(); Wire.beginTransmission(0x53); Wire.write(0x31); Wire.write(0x08); Wire.endTransmission(); }
static int32_t hx711_read() {                                                 // 24-bit two's complement, gain 128 (one extra clock)
    uint32_t t0 = millis(); while (digitalRead(PIN_HX_DT)) if (millis() - t0 > 500) return 0; int32_t v = 0;
    for (int i = 0; i < 24; i++) { digitalWrite(PIN_HX_SCK, HIGH); delayMicroseconds(2); v = (v << 1) | digitalRead(PIN_HX_DT); digitalWrite(PIN_HX_SCK, LOW); delayMicroseconds(2); }
    digitalWrite(PIN_HX_SCK, HIGH); delayMicroseconds(2); digitalWrite(PIN_HX_SCK, LOW); if (v & 0x800000) v |= 0xFF000000; return v; }
static bool send_cellular(const uint8_t *frame, int n) { (void)frame; (void)n; return false; }   // TODO: modem power-up, registration and send (outline in docs/DESIGN.md)

void setup() {
    Serial.begin(115200); pinMode(PIN_HX_DT, INPUT); pinMode(PIN_HX_SCK, OUTPUT); pinMode(PIN_MODEM_EN, OUTPUT); digitalWrite(PIN_MODEM_EN, LOW); Wire.begin(PIN_SDA, PIN_SCL); adxl_init(); ds.begin();
    if (boots++ == 0) { mn_alarm_init(&tilt_alarm); mn_alarm_init(&strain_alarm); }
    float ax, ay, az, roll = 0, pitch = 0; if (adxl_read(&ax, &ay, &az)) mn_tilt_deg(ax, ay, az, &roll, &pitch);
    if (isnan(base_roll)) { base_roll = roll; base_pitch = pitch; int32_t s = 0; for (int i = 0; i < 8; i++) s += hx711_read(); strain_zero = s / 8; }   // first boot after installation = baseline
    float drift = fmaxf(fabsf(roll - base_roll), fabsf(pitch - base_pitch)); int32_t raw = hx711_read(); float ue = mn_microstrain(&STRAIN, raw, strain_zero);
    mn_level_t lv1 = mn_alarm_update(&tilt_alarm, &TILT_T, drift), lv2 = mn_alarm_update(&strain_alarm, &STRAIN_T, ue), worst = lv1 > lv2 ? lv1 : lv2;
    ds.requestTemperatures(); float tc = ds.getTempCByIndex(0); float vb = analogReadMilliVolts(PIN_VBAT_ADC) * 2.0f / 1000.0f;
    mn_report_t r = {1, 0 /* unix time: set from the modem clock */, (int16_t)(mn_soil_pct(&SOIL, analogRead(PIN_SOIL_ADC)) * 10), (int16_t)(tc * 10), (int16_t)(roll * 100), (int16_t)(pitch * 100), (int32_t)ue, (uint16_t)(vb * 1000), (uint8_t)worst, 0};
    uint8_t frame[MN_FRAME_LEN]; mn_pack(&r, frame); bool sent = send_cellular(frame, MN_FRAME_LEN); (void)sent;
    esp_sleep_enable_timer_wakeup((uint64_t)mn_next_interval_s(worst, vb, false) * 1000000ULL); esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_ACC_INT, 1);   // wake on accelerometer interrupt too
    esp_deep_sleep_start(); }
void loop() {}
