// BioTray firmware skeleton (ESP32-S3, Arduino-ESP32 core 2.x, libraries: PubSubClient, OneWire, DallasTemperature, BH1750).
// STATUS: NOT compiled for the ESP32 and not run on hardware. All control logic is in ../lib/bt_core.c (host-tested with `make test`).
// Copy secrets.h.example to secrets.h and fill in WiFi and broker settings; never commit secrets.
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <BH1750.h>
#include <time.h>
extern "C" {
#include "bt_core.h"
}
#include "biotray_pins.h"
#include "secrets.h"      // WIFI_SSID, WIFI_PASS, MQTT_HOST, MQTT_PORT, TRAY_ID

static WiFiClient net; static PubSubClient mqtt(net); static OneWire ow(PIN_ONEWIRE); static DallasTemperature ds(&ow); static BH1750 lux;
static bt_light_cfg_t LIGHT = {6 * 60, 22 * 60, 30, 255};
static bt_pump_cfg_t PUMP = {3600, 30, 60, 120};                    // every hour run 30 s, never longer than 60 s, at least 2 minutes between runs
static bt_cal2_t PH_CAL = {2.50f, 7.00f, 3.00f, 4.00f}, EC_CAL = {0.0f, 0.0f, 2.0f, 5.0f};   // PLACEHOLDERS: calibrate with buffer solutions (see manual)
static bt_pump_t pump1; static bt_filter_t fph, fec, ftemp; static bt_state_t st;
static uint32_t last_pub = 0, last_tick = 0;

static float adc_volts(int pin) { return analogReadMilliVolts(pin) / 1000.0f; }
static void mqtt_connect() { if (mqtt.connected()) return; mqtt.connect(TRAY_ID, nullptr, nullptr, (String("farm/") + TRAY_ID + "/status").c_str(), 0, true, "offline"); }
static void on_msg(char *topic, byte *pl, unsigned n) {            // farm/<tray>/cmd/pump_clear -> clear the dry-run latch
    if (strstr(topic, "pump_clear")) bt_pump_clear_fault(&pump1); (void)pl; (void)n; }
void setup() {
    Serial.begin(115200); pinMode(PIN_PUMP1, OUTPUT); pinMode(PIN_PUMP2, OUTPUT); pinMode(PIN_FAN, OUTPUT); pinMode(PIN_LEVEL, INPUT); ledcSetup(0, 5000, 8); ledcAttachPin(PIN_LIGHT, 0);
    ds.begin(); Wire.begin(PIN_SDA, PIN_SCL); lux.begin(); bt_pump_init(&pump1); bt_filter_init(&fph); bt_filter_init(&fec); bt_filter_init(&ftemp);
    WiFi.begin(WIFI_SSID, WIFI_PASS); configTime(19800, 0, "pool.ntp.org");            // IST = UTC+5:30
    mqtt.setServer(MQTT_HOST, MQTT_PORT); mqtt.setCallback(on_msg); }
void loop() {
    uint32_t now = millis(); if (WiFi.status() == WL_CONNECTED) { mqtt_connect(); mqtt.loop(); }
    if (now - last_tick >= 1000) {                                                       // 1 Hz control tick
        last_tick = now; ds.requestTemperatures(); float t = ds.getTempCByIndex(0); if (t > -100) st.temp_c = bt_filter_push(&ftemp, t, 0.2f);
        st.ph = bt_cal_apply(&PH_CAL, bt_filter_push(&fph, adc_volts(PIN_PH_ADC), 0.1f)); st.ec_ms = bt_ec_compensate(bt_cal_apply(&EC_CAL, bt_filter_push(&fec, adc_volts(PIN_EC_ADC), 0.1f)), st.temp_c);
        st.lux = lux.readLightLevel(); st.water = !digitalRead(PIN_LEVEL); struct tm tmv; int minute = 0; if (getLocalTime(&tmv, 0)) minute = tmv.tm_hour * 60 + tmv.tm_min;
        st.light_pwm = bt_light_pwm(&LIGHT, minute); ledcWrite(0, st.light_pwm); st.pump_on = bt_pump_step(&pump1, &PUMP, st.water, 1); digitalWrite(PIN_PUMP1, st.pump_on); st.fault_dry = pump1.fault_dry;
        st.fan_on = bt_fan(st.fan_on, st.temp_c, 28.0f, 25.0f); digitalWrite(PIN_FAN, st.fan_on); st.uptime_s = now / 1000; digitalWrite(PIN_LED, st.fault_dry ? (now / 250) & 1 : 0); }
    if (now - last_pub >= 30000 && mqtt.connected()) { last_pub = now; char js[256]; if (bt_json(js, sizeof js, TRAY_ID, &st) > 0) mqtt.publish((String("farm/") + TRAY_ID + "/state").c_str(), js); }
}
