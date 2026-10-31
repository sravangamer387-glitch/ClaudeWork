/* Prototype 4: beat-synced light controller. Mic module (MAX9814 or similar analog-out) on A2,
 * 12 V RGB strip through three logic-level MOSFETs on D5/D6/D9. Prints energy + BPM on USB serial (115200). */
#include <Arduino.h>
#include "hal_nano.h"
#include "dj_core.h"

#define MIC_PIN A2
#define ENERGY_SCALE 2          /* tune: silence should read < 6, a kick drum > 40 (watch the serial monitor) */

static beat_t beat;
static light_t light;
static float dc = 512.0f;       /* running ADC mean (DC removal) */

void setup() {
    hal_init();
    Serial.begin(115200);
    beat_init(&beat);
    light_init(&light);
}

void loop() {
    static uint32_t t_frame = 0, t_print = 0;
    static uint32_t acc = 0; static uint16_t n = 0;
    int raw = analogRead(MIC_PIN);                       /* ~9 kHz sampling in a free-running loop */
    dc += (raw - dc) * (1.0f / 64.0f);
    int d = raw - (int)dc; acc += (uint32_t)(d < 0 ? -d : d); n++;
    uint32_t now = millis();
    if (now - t_frame >= 10) {
        t_frame += 10;
        uint16_t e = n ? (uint16_t)(acc * ENERGY_SCALE / n) : 0;
        acc = 0; n = 0;
        bool b = beat_push(&beat, e);
        light_frame(&light, b, e <= BEAT_QUIET);
        analogWrite(5, light.r); analogWrite(6, light.g); analogWrite(9, light.b);
        if (now - t_print >= 1000) {
            t_print = now;
            Serial.print(F("energy ")); Serial.print(e); Serial.print(F("  bpm ")); Serial.println(beat_bpm(&beat));
        }
    }
}
