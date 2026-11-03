#include "trishna_fsm.h"
#include <string.h>

void tr_fsm_cfg_defaults(tr_fsm_cfg_t *c) {
    c->debounce_ms = 300; c->stream_delay_ms = 2000; c->fallback_ms = 4000; c->sample_pump_ms = 6000; c->analysis_timeout_ms = 15000;
    c->purge_ms = 8000; c->pause_ms = 500; c->purge_cycles = 2; c->lockout_ms = 30000; c->retry_ms = 600000;
    c->pump_max_ms = 30000; c->stream_lost_ms = 500; c->valve_max_ms = 30000; c->presence_required = 1;
}

void tr_fsm_init(tr_fsm_t *f, const tr_fsm_cfg_t *cfg, uint16_t event_id) {
    memset(f, 0, sizeof(*f));
    f->cfg = *cfg; f->state = STATE_IDLE; f->event_id = event_id; f->fault = ERR_NONE;
}

static void go(tr_fsm_t *f, tr_state_t s, uint32_t now, tr_outputs_t *o) {
    if (f->state != s) { o->state_changed = 1; o->prev_state = f->state; }
    f->state = s; f->t_state = now; f->t_phase = now; f->phase = 0; f->cycle = 0;
}
static void set_pump(tr_fsm_t *f, tr_pump_t p, uint32_t now) { if (p != f->pump) { f->pump = p; f->t_pump_on = now; } }
static void set_valve(tr_fsm_t *f, uint8_t v, uint32_t now) { if (v != f->valve) { f->valve = v; f->t_valve_on = now; } }
static void raise(tr_outputs_t *o, tr_error_t e) { if (o->error == ERR_NONE) o->error = e; }

void tr_fsm_clear_fault(tr_fsm_t *f, uint32_t now_ms) { f->fault = ERR_NONE; f->t_state = now_ms; }
void tr_fsm_force_event(tr_fsm_t *f, uint32_t now_ms) {
    if (f->state == STATE_IDLE && f->fault == ERR_NONE) { f->state = STATE_STREAM_DETECTED; f->t_state = now_ms; f->fallback = 1; f->force_evt = 1; }
}
void tr_fsm_force_purge(tr_fsm_t *f, uint32_t now_ms) {
    if ((f->state == STATE_IDLE || f->state == STATE_LOCKOUT) && f->fault != ERR_LEAK) { f->state = STATE_PURGE_CLEANING; f->t_state = now_ms; f->t_phase = now_ms; f->phase = 0; f->cycle = 0; f->check_pending = 0; }
}

void tr_fsm_step(tr_fsm_t *f, uint32_t now, const tr_inputs_t *in, tr_outputs_t *o) {
    memset(o, 0, sizeof(*o));
    o->prev_state = f->state;
    /* forced transitions from the console arrive with state already changed: announce them once */
    if (f->force_evt) { f->force_evt = 0; o->state_changed = 1; o->prev_state = STATE_IDLE; o->request = REQ_BLANK; f->event_id++; }

    /* ---- safety first: a leak stops everything and latches ---- */
    if (in->leak && f->fault != ERR_LEAK) { f->fault = ERR_LEAK; raise(o, ERR_LEAK); go(f, STATE_LOCKOUT, now, o); }
    if (f->fault == ERR_LEAK) { set_pump(f, PUMP_OFF, now); set_valve(f, 0, now); f->state = STATE_LOCKOUT; goto out; }

    /* ---- stream debounce (sump probe) ---- */
    if (in->stream) { if (f->t_stream_on == 0) f->t_stream_on = now ? now : 1; if (now - f->t_stream_on >= f->cfg.debounce_ms) f->stream_deb = 1; f->t_stream_off = 0; }
    else { if (f->t_stream_off == 0) f->t_stream_off = now ? now : 1; f->t_stream_on = 0; f->stream_deb = 0; }
    if (in->presence) { if (!f->presence_seen) { f->presence_seen = 1; f->t_presence_on = now; } }
    else f->presence_seen = 0;

    switch (f->state) {
    case STATE_IDLE: {
        set_pump(f, PUMP_OFF, now); set_valve(f, 0, now); f->fallback = 0;
        if (f->fault != ERR_NONE) { go(f, STATE_LOCKOUT, now, o); break; }
        uint8_t armed = f->cfg.presence_required ? f->presence_seen : 1;
        if (armed && f->stream_deb) { f->event_id++; go(f, STATE_STREAM_DETECTED, now, o); o->request = REQ_BLANK; }
        else if (f->cfg.fallback_ms && f->presence_seen && in->sump_liquid && !in->stream && now - f->t_presence_on >= f->cfg.fallback_ms) {
            f->event_id++; f->fallback = 1; go(f, STATE_STREAM_DETECTED, now, o); o->request = REQ_BLANK;
        }
        break; }
    case STATE_STREAM_DETECTED:
        set_pump(f, PUMP_OFF, now); set_valve(f, 0, now);
        if (!f->fallback && f->t_stream_off && now - f->t_stream_off >= f->cfg.stream_lost_ms) { raise(o, ERR_SHORT_EVENT); go(f, STATE_IDLE, now, o); break; }
        if (now - f->t_state >= f->cfg.stream_delay_ms) go(f, STATE_SAMPLING, now, o);
        break;
    case STATE_SAMPLING:
        set_valve(f, 0, now); set_pump(f, PUMP_FWD, now); o->pump_duty = 255;
        if (now - f->t_state >= f->cfg.sample_pump_ms) { set_pump(f, PUMP_OFF, now); go(f, STATE_ANALYSIS, now, o); o->request = REQ_SAMPLE; }
        break;
    case STATE_ANALYSIS:
        set_pump(f, PUMP_OFF, now); set_valve(f, 0, now);
        if (in->analysis_done) go(f, STATE_PURGE_CLEANING, now, o);
        else if (now - f->t_state >= f->cfg.analysis_timeout_ms) { raise(o, ERR_ANALYSIS_TIMEOUT); go(f, STATE_PURGE_CLEANING, now, o); }
        break;
    case STATE_PURGE_CLEANING:
        if (f->phase == 0) {                                   /* valve open + reverse backwash */
            set_valve(f, 1, now); set_pump(f, PUMP_REV, now); o->pump_duty = 255;
            if (now - f->t_phase >= f->cfg.purge_ms) { f->phase = 1; f->t_phase = now; set_pump(f, PUMP_OFF, now); set_valve(f, 0, now); }
        } else if (f->phase == 1) {                            /* pause: let bubbles rise, valve closed */
            set_pump(f, PUMP_OFF, now); set_valve(f, 0, now);
            if (now - f->t_phase >= f->cfg.pause_ms) {
                f->cycle++;
                if (f->cycle < f->cfg.purge_cycles) { f->phase = 0; f->t_phase = now; }
                else { f->phase = 2; f->t_phase = now; o->request = REQ_PURGE_CHECK; f->check_pending = 1; }
            }
        } else {                                               /* check: chamber must now hold rinse water */
            set_pump(f, PUMP_OFF, now); set_valve(f, 0, now);
            if (in->check_done || now - f->t_phase >= 5000) {
                f->check_pending = 0;
                if (in->check_done && in->check_air) { f->fault = ERR_RESERVOIR_EMPTY; raise(o, ERR_RESERVOIR_EMPTY); f->t_retry = now; }
                else if (f->fault == ERR_RESERVOIR_EMPTY) f->fault = ERR_NONE;      /* a retry succeeded */
                go(f, STATE_LOCKOUT, now, o);
            }
        }
        break;
    case STATE_LOCKOUT:
        set_pump(f, PUMP_OFF, now); set_valve(f, 0, now);
        if (f->fault == ERR_RESERVOIR_EMPTY) { if (now - f->t_retry >= f->cfg.retry_ms) go(f, STATE_PURGE_CLEANING, now, o); }
        else if (f->fault == ERR_NONE && now - f->t_state >= f->cfg.lockout_ms) go(f, STATE_IDLE, now, o);
        break;
    }

    /* ---- hard limits on the actuators ---- */
    if (f->pump != PUMP_OFF && now - f->t_pump_on > f->cfg.pump_max_ms) { set_pump(f, PUMP_OFF, now); raise(o, ERR_PUMP_LIMIT); go(f, STATE_LOCKOUT, now, o); }
    if (f->valve && now - f->t_valve_on > f->cfg.valve_max_ms) { set_valve(f, 0, now); raise(o, ERR_PUMP_LIMIT); go(f, STATE_LOCKOUT, now, o); }
out:
    o->pump = f->pump; o->valve = f->valve;
    if (o->pump == PUMP_OFF) o->pump_duty = 0; else if (o->pump_duty == 0) o->pump_duty = 255;
}

const char *tr_state_name(tr_state_t s) {
    static const char *n[] = {"STATE_IDLE", "STATE_STREAM_DETECTED", "STATE_SAMPLING", "STATE_ANALYSIS", "STATE_PURGE_CLEANING", "STATE_LOCKOUT"};
    return (unsigned)s < 6 ? n[s] : "STATE_?";
}
const char *tr_error_name(tr_error_t e) {
    static const char *n[] = {"none", "leak", "reservoir empty", "temperature sensor", "SD card", "ToF sensor", "optics saturated", "short event",
                              "supply low", "supply high", "actuator time limit", "no sample", "analysis timeout", "telemetry queue full"};
    return (unsigned)e < 14 ? n[e] : "?";
}
