// TRISHNA application: owns the state machine, turns sensor readings into FSM inputs, runs the measurements the FSM requests,
// builds the 48-byte frames. Called from loop() every 10 ms.
#pragma once
#include <stdint.h>
#include <math.h>
#include "hal.h"
#include "trishna_fsm.h"
#include "trishna_frame.h"

struct Live {
    float sump_mv = 3300, leak_mv = 3300, sump_base = -1;
    bool presence = false, stream = false, liquid = false, leak = false;
    TofRaw tof{false, false, 0};
    float vin_mv = 0, temp_c = NAN;
    EcRaw ec{0, 0, 0};
    float ec_live = 0;               // filtered conductivity during sampling, mS/cm (uncompensated)
};
struct Result {
    float temp_c = NAN, ec25 = 0, cell_ohm = -1, sg = 0, a450 = 0, turb = 0;
    OptRaw opt{};
    uint8_t hydration = 0, quality = 0;
    uint16_t flags = 0, error = 0;
};

extern tr_fsm_t g_fsm;
extern Live g_live;
extern Result g_last;
extern Result g_blank;

void app_init();
void app_tick(uint32_t now_ms);
void app_apply_settings();                 // re-derive the FSM timing after a console change
void app_emit(uint8_t type, uint16_t error, uint8_t prev_state);
uint16_t app_flags();
