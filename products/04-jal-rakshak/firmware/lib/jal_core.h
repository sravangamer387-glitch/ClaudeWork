/* Jal-Rakshak: overhead-tank pump controller core (C99, no heap). Inputs are probe states (true = probe in water);
 * the core filters them, decides whether the pump may run, and reports a status code. Safety rules:
 *  - power-return delay (default 60 s) before the pump may start after any reset/outage
 *  - start only when the tank is below LOW and the sump has water; stop at FULL
 *  - dry-run protection: sump dry for 5 s stops the pump; auto-retry after 10 min, three tries, then latched
 *  - minimum off time (default 120 s) against short-cycling
 *  - probe-fault detection (FULL wet while LOW dry) and run-time limit learned from previous fills */
#ifndef JAL_CORE_H
#define JAL_CORE_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef enum { JAL_BOOT_WAIT = 0, JAL_IDLE, JAL_PUMPING, JAL_FAULT_DRY, JAL_FAULT_PROBE, JAL_FAULT_TIMEOUT } jal_state_t;

typedef struct {
    uint32_t power_return_ms;      /* 60000 */
    uint32_t min_off_ms;           /* 120000 */
    uint32_t dry_confirm_ms;       /* 5000 */
    uint32_t sump_wet_confirm_ms;  /* 3000 */
    uint32_t full_confirm_ms;      /* 3000: ignores water ripple */
    uint32_t low_confirm_ms;       /* 5000 */
    uint32_t probe_fault_ms;       /* 5000 */
    uint32_t default_timeout_ms;   /* 1800000 until a fill has been learned */
    uint32_t dry_retry_ms;         /* 600000 */
    uint8_t max_dry_retries;       /* 3 */
} jal_cfg_t;

typedef struct { bool sump_wet, tank_low_wet, tank_full_wet; } jal_inputs_t;
typedef struct { bool stable, raw; uint32_t t_change; } jal_filt_t;

typedef struct {
    jal_cfg_t cfg; jal_state_t st;
    jal_filt_t sump, low, full;
    uint32_t t_boot, t_pump_start, t_last_off, t_fault, t_probe_bad, learned_fill_ms;
    bool pump, need_fill, run_from_low, probe_bad_active;
    uint8_t dry_count;
    uint32_t pump_starts;
} jal_t;

void jal_default_cfg(jal_cfg_t *c);
void jal_init(jal_t *j, const jal_cfg_t *c, uint32_t now);
void jal_step(jal_t *j, uint32_t now, jal_inputs_t in);   /* call about every 100 ms */
void jal_reset_faults(jal_t *j, uint32_t now);            /* user button */
bool jal_pump(const jal_t *j);
uint8_t jal_status_code(const jal_t *j);                  /* blink count: 1 idle, 2 pumping, 3 dry, 4 probe fault, 5 run-time limit; 0 booting */
uint32_t jal_run_limit_ms(const jal_t *j);

#ifdef __cplusplus
}
#endif
#endif
