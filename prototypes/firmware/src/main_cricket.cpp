/* Prototype 3: handheld electronic cricket game (TM1637 display, 7 LEDs, piezo, 2 buttons). */
#include <Arduino.h>
#include "hal_nano.h"

static btn_scan_t scan;
static cricket_t game;

void setup() {
    hal_init();
    btn_init(&scan, &HAL, CR_BTN_COUNT);
    cricket_init(&game, &HAL, (uint32_t)analogRead(A3) * 2654435761UL ^ (uint32_t)micros());
}

void loop() {
    btn_evt_t e;
    btn_update(&scan);
    while (btn_pop(&scan, &e)) cricket_event(&game, e);
    cricket_tick(&game);
    delay(1);
}
