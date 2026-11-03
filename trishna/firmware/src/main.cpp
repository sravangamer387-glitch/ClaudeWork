// TRISHNA reagentless urinal hydration / biomarker monitor - ESP32-DevKitC-32E firmware entry point.
// loop(): 10 ms tick on core 1 (application + state machine); telemetry task on core 0; task watchdog 8 s.
#include <Arduino.h>
#include <esp_task_wdt.h>
#include "app.h"
#include "board_pins.h"
#include "console.h"
#include "settings.h"
#include "telemetry.h"

void setup() {
    Serial.begin(CONSOLE_BAUD);
    settings_load();
    tlm_init();
    app_init();
    esp_task_wdt_init(8, true);
    esp_task_wdt_add(nullptr);
    Serial.printf("\nTRISHNA fw 1.0 - event %u - type 'help'\n", g_fsm.event_id);
}

void loop() {
    static uint32_t next = 0;
    uint32_t now = millis();
    if ((int32_t)(now - next) >= 0) {
        next = now + 10;
        app_tick(now);
    }
    console_poll();
    esp_task_wdt_reset();
    delay(1);
}
