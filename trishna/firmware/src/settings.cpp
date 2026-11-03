#include "settings.h"
#include <Preferences.h>
#include <string.h>

Settings g_set;
static Preferences prefs;
static const uint32_t SETTINGS_MAGIC = 0x54524931;   // "TRI1": bump when the struct layout changes

void settings_defaults(Settings &s) {
    memset(&s, 0, sizeof(s));
    tr_cal_defaults(&s.cal);
    s.flow_ml_s = 1.0f; s.sample_ml = 6.0f; s.purge_ml = 8.0f;
    s.stream_delay_ms = 2000; s.lockout_ms = 30000; s.fallback_ms = 4000;
    s.purge_cycles = 2; s.presence_required = 1; s.presence_mm = 800;
    s.stream_abs_mv = 600; s.stream_rel = 0.6f; s.leak_mv = 2500; s.event_id = 0;
}

void settings_load() {
    settings_defaults(g_set);
    prefs.begin("trishna", true);
    if (prefs.getUInt("magic", 0) == SETTINGS_MAGIC && prefs.getBytesLength("set") == sizeof(Settings)) prefs.getBytes("set", &g_set, sizeof(Settings));
    g_set.event_id = prefs.getUShort("evt", g_set.event_id);
    prefs.end();
}

void settings_save() {
    prefs.begin("trishna", false);
    prefs.putBytes("set", &g_set, sizeof(Settings));
    prefs.putUInt("magic", SETTINGS_MAGIC);
    prefs.putUShort("evt", g_set.event_id);
    prefs.end();
}

void settings_save_event_id() {
    prefs.begin("trishna", false);
    prefs.putUShort("evt", g_set.event_id);
    prefs.end();
}

void settings_to_fsm(const Settings &s, tr_fsm_cfg_t &c) {
    tr_fsm_cfg_defaults(&c);
    float flow = s.flow_ml_s > 0.05f ? s.flow_ml_s : 1.0f;
    c.stream_delay_ms = s.stream_delay_ms;
    c.sample_pump_ms = (uint32_t)(1000.0f * s.sample_ml / flow);
    c.purge_ms = (uint32_t)(1000.0f * s.purge_ml / flow);
    c.purge_cycles = s.purge_cycles ? s.purge_cycles : 1;
    c.lockout_ms = s.lockout_ms;
    c.fallback_ms = s.fallback_ms;
    c.presence_required = s.presence_required;
    if (c.sample_pump_ms > c.pump_max_ms - 1000) c.sample_pump_ms = c.pump_max_ms - 1000;   // never trip the hard limit in normal use
    if (c.purge_ms > c.pump_max_ms - 1000) c.purge_ms = c.pump_max_ms - 1000;
}
