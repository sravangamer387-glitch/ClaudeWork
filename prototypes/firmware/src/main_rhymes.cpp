/* Prototype 1: regional-language rhymes player on Arduino Nano + DFPlayer-Mini-style MP3 module. */
#include <Arduino.h>
#include "hal_nano.h"

static btn_scan_t scan;
static rhymes_t rh;
static const uint8_t TRACKS[3] = {10, 10, 10};     /* files per language folder (01, 02, 03) on the SD card */

void setup() {
    hal_init();
    btn_init(&scan, &HAL, RH_BTN_COUNT);
    rhymes_init(&rh, &HAL, 3, TRACKS);
}

void loop() {
    btn_evt_t e;
    btn_update(&scan);
    while (btn_pop(&scan, &e)) rhymes_event(&rh, e);
    rhymes_tick(&rh);
    delay(1);
}
