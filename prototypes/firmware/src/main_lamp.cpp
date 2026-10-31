/* Prototype 2: star projector night lamp (RGB via MOSFETs, rotor, lullabies from the MP3 module). */
#include <Arduino.h>
#include "hal_nano.h"

static btn_scan_t scan;
static lamp_t lamp;

void setup() {
    hal_init();
    btn_init(&scan, &HAL, LAMP_BTN_COUNT);
    lamp_init(&lamp, &HAL);
}

void loop() {
    btn_evt_t e;
    btn_update(&scan);
    while (btn_pop(&scan, &e)) lamp_event(&lamp, e);
    lamp_tick(&lamp);
    delay(1);
}
