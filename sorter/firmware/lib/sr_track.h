#ifndef SR_TRACK_H
#define SR_TRACK_H
#include <stdint.h>
#include <stdbool.h>
/* Belt-position item tracker for a camera + pick/reject station. All timing is in BELT STEPS (an encoder or the stepper step count), not seconds,
   so conveyor stops, speed changes and S-curve ramps do not break synchronisation. Portable C, host-tested. */
#define SR_MAX_ITEMS 16
typedef enum { SR_PASS = 0, SR_PICK_A = 1, SR_PICK_B = 2 } sr_action_t;     /* what the station should do with an item */
typedef struct { float cam_to_pick_mm, lead_mm, window_mm, dedupe_mm, steps_per_mm; } sr_cfg_t;
typedef struct { bool used; int id; sr_action_t action; int64_t detect_steps; bool fired; } sr_item_t;
typedef struct { sr_cfg_t c; sr_item_t it[SR_MAX_ITEMS]; int next_id; int missed, dropped, fired; int64_t last_det_steps; sr_action_t last_det_action; bool have_last; } sr_t;
void sr_init(sr_t *s, const sr_cfg_t *c);
/* camera result for the item currently at the camera line; returns item id, 0 if it was a duplicate of the previous detection, -1 if the table is full */
int sr_detect(sr_t *s, sr_action_t action, int64_t belt_steps);
/* call whenever the belt position changes; returns the id of an item whose pick should fire now (action in *action), or 0. Call repeatedly until it returns 0. */
int sr_poll(sr_t *s, int64_t belt_steps, sr_action_t *action);
#endif
