#include "jal_core.h"

void jal_default_cfg(jal_cfg_t *c) {
    c->power_return_ms = 60000u; c->min_off_ms = 120000u; c->dry_confirm_ms = 5000u; c->sump_wet_confirm_ms = 3000u;
    c->full_confirm_ms = 3000u; c->low_confirm_ms = 5000u; c->probe_fault_ms = 5000u; c->default_timeout_ms = 1800000u;
    c->dry_retry_ms = 600000u; c->max_dry_retries = 3;
}

static void filt_init(jal_filt_t *f, bool v, uint32_t now) { f->stable = f->raw = v; f->t_change = now; }
/* the stable value flips only after the raw value has been different for `confirm_ms` continuously */
static void filt(jal_filt_t *f, bool raw, uint32_t now, uint32_t confirm_to_wet, uint32_t confirm_to_dry) {
    if (raw != f->raw) { f->raw = raw; f->t_change = now; }
    if (f->raw != f->stable) {
        uint32_t need = f->raw ? confirm_to_wet : confirm_to_dry;
        if ((uint32_t)(now - f->t_change) >= need) f->stable = f->raw;
    }
}

void jal_init(jal_t *j, const jal_cfg_t *c, uint32_t now) {
    j->cfg = *c; j->st = JAL_BOOT_WAIT; j->t_boot = now; j->t_pump_start = 0; j->t_last_off = now - c->min_off_ms;   /* only the power-return delay applies after a reset */ j->t_fault = 0; j->t_probe_bad = 0;
    j->learned_fill_ms = 0; j->pump = false; j->need_fill = false; j->run_from_low = false; j->probe_bad_active = false; j->dry_count = 0; j->pump_starts = 0;
    filt_init(&j->sump, true, now); filt_init(&j->low, true, now); filt_init(&j->full, false, now);
    j->need_fill = false;
}

uint32_t jal_run_limit_ms(const jal_t *j) {
    if (j->learned_fill_ms == 0) return j->cfg.default_timeout_ms;
    uint32_t lim = j->learned_fill_ms + j->learned_fill_ms / 10u;       /* learned fill time + 10 % */
    return lim < 60000u ? 60000u : lim;
}

static void stop_pump(jal_t *j, uint32_t now) { if (j->pump) { j->pump = false; j->t_last_off = now; } }

void jal_step(jal_t *j, uint32_t now, jal_inputs_t in) {
    const jal_cfg_t *c = &j->cfg;
    filt(&j->sump, in.sump_wet, now, c->sump_wet_confirm_ms, c->dry_confirm_ms);
    filt(&j->low, in.tank_low_wet, now, c->low_confirm_ms, c->low_confirm_ms);
    filt(&j->full, in.tank_full_wet, now, c->full_confirm_ms, c->full_confirm_ms);

    /* tank level memory: below LOW -> a fill is needed until FULL is reached */
    if (!j->low.stable) j->need_fill = true;
    if (j->full.stable) j->need_fill = false;

    /* probe fault: FULL probe wet while LOW probe dry is physically impossible */
    bool impossible = j->full.stable && !j->low.stable;
    if (impossible && !j->probe_bad_active) { j->probe_bad_active = true; j->t_probe_bad = now; }
    if (!impossible) j->probe_bad_active = false;
    if (j->probe_bad_active && (uint32_t)(now - j->t_probe_bad) >= c->probe_fault_ms && j->st != JAL_FAULT_PROBE) {
        stop_pump(j, now); j->st = JAL_FAULT_PROBE; j->t_fault = now;
    }

    switch (j->st) {
    case JAL_BOOT_WAIT:
        if ((uint32_t)(now - j->t_boot) >= c->power_return_ms) j->st = JAL_IDLE;
        break;
    case JAL_IDLE:
        if (j->need_fill && j->sump.stable && (uint32_t)(now - j->t_last_off) >= c->min_off_ms) {
            j->pump = true; j->t_pump_start = now; j->st = JAL_PUMPING; j->pump_starts++;
            j->run_from_low = !j->low.stable;                              /* a clean fill from LOW to FULL can be learned */
        }
        break;
    case JAL_PUMPING:
        if (j->full.stable) {                                              /* tank full: normal stop */
            uint32_t run = (uint32_t)(now - j->t_pump_start);
            if (j->run_from_low && run > 30000u) j->learned_fill_ms = j->learned_fill_ms ? (j->learned_fill_ms * 3u + run) / 4u : run;
            stop_pump(j, now); j->st = JAL_IDLE; j->dry_count = 0;
        } else if (!j->sump.stable) {                                      /* dry run */
            stop_pump(j, now); j->dry_count++; j->t_fault = now; j->st = JAL_FAULT_DRY;
        } else if ((uint32_t)(now - j->t_pump_start) >= jal_run_limit_ms(j)) {   /* ran too long: leak, empty source or dead FULL probe */
            stop_pump(j, now); j->st = JAL_FAULT_TIMEOUT; j->t_fault = now;
        }
        break;
    case JAL_FAULT_DRY:
        if (j->dry_count < c->max_dry_retries && j->sump.stable && (uint32_t)(now - j->t_fault) >= c->dry_retry_ms) j->st = JAL_IDLE;
        break;
    case JAL_FAULT_PROBE:
    case JAL_FAULT_TIMEOUT:
        break;                                                             /* latched until the user presses reset */
    }
}

void jal_reset_faults(jal_t *j, uint32_t now) {
    if (j->st == JAL_FAULT_DRY || j->st == JAL_FAULT_PROBE || j->st == JAL_FAULT_TIMEOUT) { j->st = JAL_IDLE; j->dry_count = 0; j->t_last_off = now; j->probe_bad_active = false; }
}
bool jal_pump(const jal_t *j) { return j->pump; }
uint8_t jal_status_code(const jal_t *j) {
    switch (j->st) { case JAL_BOOT_WAIT: return 0; case JAL_IDLE: return 1; case JAL_PUMPING: return 2; case JAL_FAULT_DRY: return 3; case JAL_FAULT_PROBE: return 4; default: return 5; }
}
