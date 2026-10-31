/* Prototype 5: DJ controller (8 analog controls, 8 buttons, 1 encoder) sending MIDI bytes on the USB serial port
 * at 115200 baud. Use a serial-to-MIDI bridge (e.g. Hairless MIDI) so Mixxx sees it as a MIDI device. */
#include <Arduino.h>
#include "hal_nano.h"
#include "dj_core.h"

#define ENC_A 10
#define ENC_B 11
#define CC_BASE 16              /* pots send CC 16..23 */
#define NOTE_BASE 36            /* buttons send notes 36..43 */
#define CC_JOG 40

static btn_scan_t scan;
static pot_t pots[8];
static enc_t enc;

static void send3(const uint8_t *m) { Serial.write(m, 3); }

void setup() {
    hal_init();
    pinMode(ENC_A, INPUT_PULLUP); pinMode(ENC_B, INPUT_PULLUP);
    Serial.begin(115200);
    btn_init(&scan, &HAL, 8);
}

void loop() {
    static uint8_t next_pot = 0; static uint32_t t_pot = 0;
    uint8_t m[3]; btn_evt_t e;
    btn_update(&scan);
    while (btn_pop(&scan, &e)) {
        if (e.kind == BTN_EVT_PRESS) { midi_note(0, (uint8_t)(NOTE_BASE + e.idx), true, m); send3(m); }
        else if (e.kind == BTN_EVT_RELEASE) { midi_note(0, (uint8_t)(NOTE_BASE + e.idx), false, m); send3(m); }
    }
    if (millis() - t_pot >= 2) {                      /* one analog channel every 2 ms => each pot read every 16 ms */
        uint8_t v;
        t_pot = millis();
        if (pot_update(&pots[next_pot], (uint16_t)analogRead(next_pot), &v)) { midi_cc(0, (uint8_t)(CC_BASE + next_pot), v, m); send3(m); }
        next_pot = (uint8_t)((next_pot + 1) & 7);
    }
    int8_t s = enc_update(&enc, (uint8_t)digitalRead(ENC_A), (uint8_t)digitalRead(ENC_B));
    if (s) { midi_cc(0, CC_JOG, s > 0 ? 1 : 127, m); send3(m); }   /* relative: 1 = +1, 127 = -1 */
}
