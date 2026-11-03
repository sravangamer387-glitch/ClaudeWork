/* TRISHNA event state machine (pure logic; the HAL feeds inputs and executes the outputs).
 *
 *  IDLE --(presence armed AND sump stream for debounce_ms)----------------------------> STREAM_DETECTED   [request: BLANK measurement]
 *  IDLE --(presence for fallback_ms, sump liquid, no stream signature)-----------------> STREAM_DETECTED   [fallback trigger, flagged]
 *  STREAM_DETECTED --(stream_delay_ms elapsed, stream still present)-------------------> SAMPLING           [pump FORWARD]
 *  STREAM_DETECTED --(stream lost before the delay)-------------------------------------> IDLE               [error SHORT_EVENT]
 *  SAMPLING --(sample_pump_ms elapsed)--------------------------------------------------> ANALYSIS           [pump OFF, request SAMPLE measurement]
 *  ANALYSIS --(HAL reports analysis done, or analysis_timeout_ms)-----------------------> PURGE_CLEANING
 *  PURGE_CLEANING: purge_cycles x [valve OPEN + pump REVERSE for purge_ms, then pause_ms with both off], then a CHECK step
 *                  (request PURGE_CHECK measurement: chamber must hold rinse water)  -> LOCKOUT
 *  LOCKOUT --(lockout_ms elapsed)--------------------------------------------------------> IDLE
 *  any state --(leak)---------------------------------------------------------------------> LOCKOUT, fault latched (cleared only by tr_fsm_clear_fault)
 *  PURGE CHECK finds air (reservoir empty) -> LOCKOUT with fault RESERVOIR_EMPTY; the purge is retried every retry_ms and the fault clears itself
 *  when a retry succeeds.
 *  Hard limits: the pump never runs longer than pump_max_ms in one state, the valve never stays open longer than valve_max_ms. */
#ifndef TRISHNA_FSM_H
#define TRISHNA_FSM_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

typedef enum { STATE_IDLE = 0, STATE_STREAM_DETECTED = 1, STATE_SAMPLING = 2, STATE_ANALYSIS = 3, STATE_PURGE_CLEANING = 4, STATE_LOCKOUT = 5 } tr_state_t;
typedef enum { PUMP_OFF = 0, PUMP_FWD = 1, PUMP_REV = 2 } tr_pump_t;
typedef enum { REQ_NONE = 0, REQ_BLANK = 1, REQ_SAMPLE = 2, REQ_PURGE_CHECK = 3 } tr_request_t;
typedef enum {
    ERR_NONE = 0, ERR_LEAK = 1, ERR_RESERVOIR_EMPTY = 2, ERR_TEMP_SENSOR = 3, ERR_SD = 4, ERR_TOF = 5, ERR_OPT_SAT = 6, ERR_SHORT_EVENT = 7,
    ERR_VIN_LOW = 8, ERR_VIN_HIGH = 9, ERR_PUMP_LIMIT = 10, ERR_NO_SAMPLE = 11, ERR_ANALYSIS_TIMEOUT = 12, ERR_QUEUE_FULL = 13
} tr_error_t;

typedef struct {
    uint32_t debounce_ms;        /* stream signature must persist this long (300) */
    uint32_t stream_delay_ms;    /* mid-stream delay before the catch (2000) */
    uint32_t fallback_ms;        /* presence-only trigger after this long (4000); 0 disables */
    uint32_t sample_pump_ms;     /* forward pumping time = sample volume / flow (6000 for 6 mL at 1 mL/s) */
    uint32_t analysis_timeout_ms;/* (15000) */
    uint32_t purge_ms;           /* per purge cycle (8000) */
    uint32_t pause_ms;           /* between purge cycles (500) */
    uint8_t  purge_cycles;       /* (2) */
    uint32_t lockout_ms;         /* refractory time after an event (30000) */
    uint32_t retry_ms;           /* reservoir-empty purge retry period (600000) */
    uint32_t pump_max_ms;        /* hard limit per state (30000) */
    uint32_t stream_lost_ms;     /* stream absent this long during the delay = short event (500) */
    uint32_t valve_max_ms;       /* hard limit (30000) */
    uint8_t  presence_required;  /* 1: stream trigger needs the ToF presence; 0: sump alone (ToF missing) */
} tr_fsm_cfg_t;
void tr_fsm_cfg_defaults(tr_fsm_cfg_t *c);

typedef struct {
    uint8_t presence;            /* debounced ToF presence */
    uint8_t stream;              /* sump probe stream signature (raw, debounced inside) */
    uint8_t sump_liquid;         /* sump probe immersed (any liquid) */
    uint8_t leak;
    uint8_t analysis_done;       /* HAL finished the SAMPLE measurement */
    uint8_t check_done, check_air; /* HAL finished the PURGE_CHECK measurement; air found */
} tr_inputs_t;

typedef struct {
    tr_pump_t pump; uint8_t pump_duty;   /* duty 0..255 */
    uint8_t valve;
    tr_request_t request;                /* one-shot: set on the step a measurement is wanted */
    uint8_t state_changed; tr_state_t prev_state;
    tr_error_t error;                    /* one-shot: an error to report this step */
} tr_outputs_t;

typedef struct {
    tr_fsm_cfg_t cfg;
    tr_state_t state;
    uint32_t t_state, t_stream_on, t_presence_on, t_phase, t_retry;
    uint8_t stream_deb, presence_seen, fallback, phase, cycle, check_pending, force_evt;
    uint32_t t_stream_off;              /* when the stream signature last disappeared (0 = present) */
    tr_error_t fault;                    /* latched / sticky fault (ERR_NONE when clear) */
    uint16_t event_id;
    uint32_t t_pump_on, t_valve_on;
    tr_pump_t pump; uint8_t valve;
} tr_fsm_t;

void tr_fsm_init(tr_fsm_t *f, const tr_fsm_cfg_t *cfg, uint16_t event_id);
void tr_fsm_step(tr_fsm_t *f, uint32_t now_ms, const tr_inputs_t *in, tr_outputs_t *out);
void tr_fsm_clear_fault(tr_fsm_t *f, uint32_t now_ms);
void tr_fsm_force_event(tr_fsm_t *f, uint32_t now_ms);    /* bench test: start an event without a stream */
void tr_fsm_force_purge(tr_fsm_t *f, uint32_t now_ms);    /* maintenance: run a purge now */
const char *tr_state_name(tr_state_t s);
const char *tr_error_name(tr_error_t e);

#ifdef __cplusplus
}
#endif
#endif
