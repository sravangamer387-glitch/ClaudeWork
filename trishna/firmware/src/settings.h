// Persistent settings (NVS via Preferences): calibration, timings and thresholds. Changed from the serial console, saved with "save".
#pragma once
#include <stdint.h>
#include "trishna_sense.h"
#include "trishna_fsm.h"

struct Settings {
    tr_cal_t cal;
    float flow_ml_s;         // pump flow at full speed, from "cal flow" (default 1.0 mL/s)
    float sample_ml;         // volume pushed through the 2 mL chamber per event (default 6 mL = 3 chamber volumes)
    float purge_ml;          // backwash volume per purge cycle (default 8 mL)
    uint32_t stream_delay_ms, lockout_ms, fallback_ms;
    uint8_t purge_cycles, presence_required;
    uint16_t presence_mm;    // ToF distance that counts as "user present" (default 800)
    uint16_t stream_abs_mv;  // sump probe below this = urine-like conductivity (default 600 mV)
    float stream_rel;        // ... and below this fraction of the idle baseline (default 0.6)
    uint16_t leak_mv;        // leak probe below this = wet (default 2500 mV)
    uint16_t event_id;       // persists across reboots
    char wifi_ssid[33], wifi_pass[65];
};

extern Settings g_set;
void settings_defaults(Settings &s);
void settings_load();
void settings_save();
void settings_save_event_id();
// FSM configuration derived from the settings (pump times from volumes and the calibrated flow)
void settings_to_fsm(const Settings &s, tr_fsm_cfg_t &c);
