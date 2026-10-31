/* Prayog kit firmware for Arduino Nano: streams CSV on USB serial at 115200 baud.
 * Commands (line terminated):  SET <0-7> <NTC|LDR|MIC|HALL|SOIL|VOLT|IR|COND>  assigns a sensor type to analog socket A<n>.
 * Output 10 times a second: ms,A0,...,A7,echo_cm,gate_count   (converted values; raw counts for IR/COND/MIC)
 * Photogate events are streamed immediately as lines  G,<microseconds>,<1=beam interrupted>  (timestamps from micros()).
 * Photogate on D2 (interrupt), ultrasonic trigger D4 / echo D5. */
#include <Arduino.h>
#include "prayog_core.h"

static sensor_t type[8] = {S_NTC, S_LDR, S_MIC, S_HALL, S_SOIL, S_VOLT, S_IR, S_COND};
static volatile uint32_t gate_t_us[GATE_MAX]; static volatile uint8_t gate_lv[GATE_MAX]; static volatile uint8_t gate_head = 0, gate_count = 0; static uint8_t gate_tail = 0;
static char line[24]; static uint8_t len = 0;

static void gate_isr() {
    uint8_t h = gate_head; gate_t_us[h] = micros(); gate_lv[h] = (uint8_t)digitalRead(2); gate_head = (uint8_t)((h + 1) % GATE_MAX); gate_count++;
}

void setup() {
    Serial.begin(115200);
    pinMode(2, INPUT_PULLUP); pinMode(4, OUTPUT); pinMode(5, INPUT);
    attachInterrupt(digitalPinToInterrupt(2), gate_isr, CHANGE);
}

static float read_echo_cm() {
    digitalWrite(4, LOW); delayMicroseconds(2); digitalWrite(4, HIGH); delayMicroseconds(10); digitalWrite(4, LOW);
    unsigned long us = pulseIn(5, HIGH, 30000UL);
    return us ? echo_to_cm((uint32_t)us, 20.0f) : -1.0f;
}

void loop() {
    static uint32_t next = 0;
    while (Serial.available()) {
        char c = (char)Serial.read();
        if (c == '\n' || c == '\r') { line[len] = 0; uint8_t ch; sensor_t s; if (len && parse_set(line, &ch, &s) == 0) type[ch] = s; len = 0; }
        else if (len < sizeof line - 1) line[len++] = c;
    }
    while (gate_tail != gate_head) {                                  /* stream photogate events as they happen */
        noInterrupts(); uint32_t t = gate_t_us[gate_tail]; uint8_t lv = gate_lv[gate_tail]; interrupts();
        Serial.print(F("G,")); Serial.print(t); Serial.print(','); Serial.println(lv ? 0 : 1);   /* module output is LOW when the beam is interrupted */
        gate_tail = (uint8_t)((gate_tail + 1) % GATE_MAX);
    }
    if (millis() >= next) {
        next += 100;
        Serial.print(millis());
        for (uint8_t i = 0; i < 8; i++) {
            uint16_t adc = (uint16_t)analogRead(i);
            Serial.print(','); Serial.print(type[i] == S_NONE ? (float)adc : conv_generic(type[i], adc), 2);
        }
        Serial.print(','); Serial.print(read_echo_cm(), 1); Serial.print(','); Serial.println(gate_count);
    }
}
