// KINETIC controller firmware skeleton (ESP32-S3, Arduino-ESP32 core 2.x).
// STATUS: not compiled for the ESP32 and not run on hardware. The portable code it calls (../lib: kn_motion, kn_vib) is host-tested with
// `make test`; this file only connects it to pins, a hardware timer, SPI and the serial port. Bench-review it before first power-up.
#include <Arduino.h>
#include <SPI.h>
extern "C" {
#include "kn_motion.h"
#include "kn_vib.h"
}
#include "kinetic_pins.h"

static const int STEP_PIN[3] = {PIN_X_STEP, PIN_Y_STEP, PIN_Z_STEP}, DIR_PIN[3] = {PIN_X_DIR, PIN_Y_DIR, PIN_Z_DIR};
static const int EN_PIN[3] = {PIN_X_EN, PIN_Y_EN, PIN_Z_EN}, ES_PIN[3] = {PIN_ES_X, PIN_ES_Y, PIN_ES_Z};
static const double TICK_HZ = 20000.0;                 // motion tick: one step per axis per tick at most, so 10 kHz max step rate with a 1-tick pulse
static const double STEPS_PER_REV = 200.0 * 16.0;      // 1.8 deg motor at 1/16 microstepping: change for your motor/driver
static kn_limits_t LIM = {2000.0, 20000.0, 400000.0};  // steps/s, steps/s^2, steps/s^3
static kn_move_t MV;
static volatile bool moving = false, halted = false;
static volatile int32_t pos[3] = {0, 0, 0};
static volatile double v_min = 0, v_max = 0;           // speed range seen during the current vibration window
static volatile int endstop_hit = -1;
static hw_timer_t *tmr;

void IRAM_ATTR onTick() {
    for (int i = 0; i < 3; i++) digitalWrite(STEP_PIN[i], LOW);                    // end the pulse started on the previous tick
    if (!moving) return;
    for (int i = 0; i < 3; i++) if (!digitalRead(ES_PIN[i])) { endstop_hit = i; halted = true; moving = false; return; }   // endstop = switch to GND: stop at once
    int8_t st[3]; kn_move_tick(&MV, 1.0 / TICK_HZ, st);
    for (int i = 0; i < 3; i++) if (st[i]) { digitalWrite(DIR_PIN[i], st[i] > 0 ? HIGH : LOW); digitalWrite(STEP_PIN[i], HIGH); pos[i] += st[i]; }
    double v = fabs(kn_eval(&MV.prof, MV.t, 1.0).v); if (v < v_min) v_min = v; if (v > v_max) v_max = v;
    if (MV.done) moving = false;
}

// ---- ADXL345 on SPI (mode 3), 3200 Hz output rate, one Z-axis sample per 312.5 us poll ----
static SPIClass spi(FSPI);
static uint8_t adxl_rw(uint8_t reg, uint8_t val, bool write) {
    digitalWrite(PIN_S_CS, LOW); spi.transfer(write ? reg : (reg | 0x80)); uint8_t r = spi.transfer(write ? val : 0); digitalWrite(PIN_S_CS, HIGH); return r; }
static float adxl_z_g() {
    digitalWrite(PIN_S_CS, LOW); spi.transfer(0x36 | 0xC0); uint8_t lo = spi.transfer(0), hi = spi.transfer(0); digitalWrite(PIN_S_CS, HIGH);   // DATAZ0/1, multi-byte read
    return (int16_t)((hi << 8) | lo) * 0.0039f; }
static bool adxl_init() {
    pinMode(PIN_S_CS, OUTPUT); digitalWrite(PIN_S_CS, HIGH); spi.begin(PIN_S_SCLK, PIN_S_MISO, PIN_S_MOSI, PIN_S_CS); spi.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE3));
    if (adxl_rw(0x00, 0, false) != 0xE5) return false;                              // DEVID
    adxl_rw(0x2C, 0x0F, true); adxl_rw(0x31, 0x0B, true); adxl_rw(0x2D, 0x08, true); return true; }   // BW_RATE 3200 Hz, DATA_FORMAT full-res +-16 g, POWER_CTL measure
static float win[KV_N]; static int wn = 0; static uint32_t next_us = 0; static bool sensor_ok = false;
static void vib_poll() {
    if (!sensor_ok || (int32_t)(micros() - next_us) < 0) return;
    next_us += 313;
    if (wn == 0) { noInterrupts(); v_min = v_max = fabs(kn_eval(&MV.prof, MV.t, 1.0).v); interrupts(); }
    win[wn++] = adxl_z_g();
    if (wn < KV_N) return;
    wn = 0;
    noInterrupts(); double lo = v_min, hi = v_max; bool mv = moving; interrupts();
    double hz = 0.5 * (lo + hi) / STEPS_PER_REV;
    if (mv && hz >= 8.0 && hz <= 25.0 && (hi - lo) < 0.03 * hi) { int c = kv_classify(win, (float)hz, nullptr); Serial.printf("VIB %d %s hz=%.1f\n", c, kv_name(c), hz); }   // only a steady-speed window is meaningful
}

// ---- line protocol (docs/PROTOCOL.md) ----
static void handle(const char *line) {
    kn_cmd_t c = kn_parse(line);
    switch (c.kind) {
    case KN_CMD_NONE: return;
    case KN_CMD_BAD: Serial.printf("ERR %s\n", c.err); return;
    case KN_CMD_STOP: moving = false; halted = true; Serial.println("OK STOP"); return;
    case KN_CMD_LIMITS: if (c.feed > 0) LIM.vmax = c.feed; if (c.accel > 0) LIM.amax = c.accel; if (c.jerk > 0) LIM.jmax = c.jerk; Serial.println("OK LIMITS"); return;
    case KN_CMD_HOME: Serial.println("ERR HOME is not implemented in this skeleton"); return;
    case KN_CMD_MOVE: {
        if (moving) { Serial.println("ERR busy"); return; }
        if (halted) { if (endstop_hit >= 0) { Serial.printf("ERR endstop %c active: back off by hand, then send CLEAR\n", "XYZ"[endstop_hit]); return; } halted = false; }
        int32_t from[3], to[3]; for (int i = 0; i < 3; i++) { from[i] = pos[i]; to[i] = c.has[i] ? c.pos[i] : pos[i]; }
        kn_limits_t L = LIM; if (c.feed > 0 && c.feed < L.vmax) L.vmax = c.feed;
        if (!kn_move_start(&MV, 3, from, to, L)) { Serial.println("OK no motion"); return; }
        moving = true; Serial.println("OK MOVE"); return; }
    }
}
void setup() {
    Serial.begin(115200);
    for (int i = 0; i < 3; i++) { pinMode(STEP_PIN[i], OUTPUT); pinMode(DIR_PIN[i], OUTPUT); pinMode(EN_PIN[i], OUTPUT); digitalWrite(EN_PIN[i], LOW); pinMode(ES_PIN[i], INPUT_PULLUP); }   // driver ENABLE is active low
    pinMode(PIN_LED, OUTPUT); sensor_ok = adxl_init(); if (!sensor_ok) Serial.println("WARN vibration sensor not found"); next_us = micros() + 1000;
    tmr = timerBegin(0, 80, true); timerAttachInterrupt(tmr, &onTick, true); timerAlarmWrite(tmr, (uint64_t)(1e6 / TICK_HZ), true); timerAlarmEnable(tmr);
    Serial.println("KINETIC ready"); }
void loop() {
    static char buf[96]; static int n = 0; vib_poll();
    while (Serial.available()) {
        char ch = Serial.read();
        if (ch == '\n' || ch == '\r') { buf[n] = 0; if (n && !strcmp(buf, "CLEAR")) { halted = false; endstop_hit = -1; Serial.println("OK CLEAR"); } else if (n) handle(buf); n = 0; }
        else if (n < (int)sizeof(buf) - 1) buf[n++] = ch; }
    digitalWrite(PIN_LED, moving ? HIGH : LOW); }
