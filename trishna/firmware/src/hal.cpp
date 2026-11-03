#include "hal.h"
#include <Arduino.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <VL53L1X.h>
#include <math.h>
#include "board_pins.h"
#include "trishna_filters.h"
#include "trishna_sense.h"

static OneWire g_ow(PIN_ONEWIRE);
static DallasTemperature g_ds(&g_ow);
static VL53L1X g_tof;
static bool g_tof_ok = false, g_ds_ok = false;
static const int PWM_CH_IN1 = 0, PWM_CH_IN2 = 1, PWM_FREQ = 20000, PWM_BITS = 8;

void hal_init() {
    // outputs low first: pump coast, valve closed, LEDs off, sensor drives off
    const int outs[] = {PIN_EC_DRV_A, PIN_EC_DRV_B, PIN_LVL_DRV, PIN_LED_BLU, PIN_LED_IR, PIN_VALVE};
    for (int p : outs) { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
    ledcSetup(PWM_CH_IN1, PWM_FREQ, PWM_BITS); ledcAttachPin(PIN_PUMP_IN1, PWM_CH_IN1); ledcWrite(PWM_CH_IN1, 0);
    ledcSetup(PWM_CH_IN2, PWM_FREQ, PWM_BITS); ledcAttachPin(PIN_PUMP_IN2, PWM_CH_IN2); ledcWrite(PWM_CH_IN2, 0);
    analogReadResolution(12);
    const int ains[] = {PIN_EC_ADC, PIN_OPT_TX_ADC, PIN_OPT_SC_ADC, PIN_VIN_ADC, PIN_SUMP_ADC, PIN_LEAK_ADC};
    for (int p : ains) analogSetPinAttenuation(p, ADC_11db);     // 0..~3.1 V, eFuse-calibrated by analogReadMilliVolts()
    g_ds.begin();
    g_ds.setResolution(12);
    g_ds.setWaitForConversion(false);
    g_ds_ok = g_ds.getDeviceCount() > 0;
}

void hal_pump(tr_pump_t dir, uint8_t duty) {
    // DRV8871: IN1 PWM / IN2 low = forward drive-coast; IN1 low / IN2 PWM = reverse; both low = coast (motor off)
    if (dir == PUMP_FWD) { ledcWrite(PWM_CH_IN2, 0); ledcWrite(PWM_CH_IN1, duty); }
    else if (dir == PUMP_REV) { ledcWrite(PWM_CH_IN1, 0); ledcWrite(PWM_CH_IN2, duty); }
    else { ledcWrite(PWM_CH_IN1, 0); ledcWrite(PWM_CH_IN2, 0); }
}

void hal_valve(bool open) { digitalWrite(PIN_VALVE, open ? HIGH : LOW); }

void hal_all_off() {
    hal_pump(PUMP_OFF, 0); hal_valve(false);
    digitalWrite(PIN_LED_BLU, LOW); digitalWrite(PIN_LED_IR, LOW);
    digitalWrite(PIN_EC_DRV_A, LOW); digitalWrite(PIN_EC_DRV_B, LOW); digitalWrite(PIN_LVL_DRV, LOW);
}

EcRaw hal_ec_measure(int cycles) {
    // Bipolar square wave, about 1.6 kHz: each half-period drives one polarity, waits for the double-layer charging edge to pass,
    // then samples node N1. Equal time in both polarities => no net DC through the sample (no electrolysis, no electrode plating).
    const uint32_t SETTLE_US = 120;
    float sa = 0, sb = 0;
    if (cycles < 1) cycles = 1;
    for (int i = 0; i < cycles; i++) {
        digitalWrite(PIN_EC_DRV_B, LOW); digitalWrite(PIN_EC_DRV_A, HIGH);
        delayMicroseconds(SETTLE_US); sa += analogReadMilliVolts(PIN_EC_ADC);
        digitalWrite(PIN_EC_DRV_A, LOW); digitalWrite(PIN_EC_DRV_B, HIGH);
        delayMicroseconds(SETTLE_US); sb += analogReadMilliVolts(PIN_EC_ADC);
    }
    digitalWrite(PIN_EC_DRV_A, LOW); digitalWrite(PIN_EC_DRV_B, LOW);
    EcRaw r; r.va_mv = sa / cycles; r.vb_mv = sb / cycles; r.ratio = tr_ec_ratio(r.va_mv, r.vb_mv);
    return r;
}

void hal_probes(float &sump_mv, float &leak_mv) {
    digitalWrite(PIN_LVL_DRV, HIGH);
    delayMicroseconds(150);                                   // 4.7 k / 47 k into 1 nF + cable: settles in well under 100 us
    sump_mv = analogReadMilliVolts(PIN_SUMP_ADC);
    leak_mv = analogReadMilliVolts(PIN_LEAK_ADC);
    digitalWrite(PIN_LVL_DRV, LOW);
}

static float read_avg(int pin, int n) { float s = 0; for (int i = 0; i < n; i++) s += analogReadMilliVolts(pin); return s / n; }

OptRaw hal_optics_measure(int repeats) {
    // TIA time constants: transmission 10 k x 10 nF = 0.1 ms, scatter 1 M x 1 nF = 1 ms; 25 ms settling is > 20 tau for both.
    const int N = 32; const uint32_t SETTLE_MS = 25;
    if (repeats < 1) repeats = 1;
    if (repeats > 9) repeats = 9;
    float dtx[9], dsc[9], btx[9], itx[9], isc[9];
    bool sat = false;
    for (int k = 0; k < repeats; k++) {
        digitalWrite(PIN_LED_BLU, LOW); digitalWrite(PIN_LED_IR, LOW); delay(SETTLE_MS);
        dtx[k] = read_avg(PIN_OPT_TX_ADC, N); dsc[k] = read_avg(PIN_OPT_SC_ADC, N);
        digitalWrite(PIN_LED_BLU, HIGH); delay(SETTLE_MS);
        float b = read_avg(PIN_OPT_TX_ADC, N);
        digitalWrite(PIN_LED_BLU, LOW); digitalWrite(PIN_LED_IR, HIGH); delay(SETTLE_MS);
        float t = read_avg(PIN_OPT_TX_ADC, N), s = read_avg(PIN_OPT_SC_ADC, N);
        digitalWrite(PIN_LED_IR, LOW);
        if (b > 3000 || t > 3000 || s > 3000) sat = true;
        btx[k] = b - dtx[k]; itx[k] = t - dtx[k]; isc[k] = s - dsc[k];
    }
    OptRaw r;
    r.dark_tx = tr_median_n(dtx, repeats); r.dark_sc = tr_median_n(dsc, repeats);
    r.blue_tx = tr_median_n(btx, repeats); r.ir_tx = tr_median_n(itx, repeats); r.ir_sc = tr_median_n(isc, repeats);
    r.saturated = sat;
    return r;
}

float hal_vin_mv() { return read_avg(PIN_VIN_ADC, 16) * VIN_DIVIDER; }

bool hal_temp_present() { return g_ds_ok; }
void hal_temp_request() { if (g_ds_ok) g_ds.requestTemperatures(); }
float hal_temp_read() {
    if (!g_ds_ok) { g_ds_ok = g_ds.getDeviceCount() > 0; return NAN; }     // allows a probe plugged in later
    float t = g_ds.getTempCByIndex(0);
    return (t == DEVICE_DISCONNECTED_C || t < -40.0f || t > 100.0f) ? NAN : t;
}

bool hal_tof_init() {
    Wire.begin(PIN_SDA, PIN_SCL, 400000);
    g_tof.setTimeout(100);
    g_tof_ok = g_tof.init();
    if (g_tof_ok) {
        g_tof.setDistanceMode(VL53L1X::Short);                  // up to about 1.3 m, best ambient-light immunity
        g_tof.setMeasurementTimingBudget(50000);
        g_tof.startContinuous(60);
    }
    return g_tof_ok;
}

TofRaw hal_tof_poll() {
    TofRaw r{g_tof_ok, false, 0};
    if (!g_tof_ok || !g_tof.dataReady()) return r;
    g_tof.read(false);
    r.valid = g_tof.ranging_data.range_status == VL53L1X::RangeValid;
    r.mm = g_tof.ranging_data.range_mm;
    return r;
}
