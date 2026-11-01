#include <string.h>
#include <math.h>
#include <stdlib.h>
#include "sr_track.h"
void sr_init(sr_t *s, const sr_cfg_t *c) { memset(s, 0, sizeof *s); s->c = *c; s->next_id = 1; }
int sr_detect(sr_t *s, sr_action_t a, int64_t steps) {
    if (s->have_last && llabs(steps - s->last_det_steps) < (int64_t)(s->c.dedupe_mm * s->c.steps_per_mm) && a == s->last_det_action) return 0;      /* same item seen in two consecutive frames */
    for (int i = 0; i < SR_MAX_ITEMS; i++) if (!s->it[i].used) {
        s->it[i] = (sr_item_t){true, s->next_id, a, steps, false}; s->last_det_steps = steps; s->last_det_action = a; s->have_last = true; return s->next_id++; }
    s->dropped++; return -1; }
int sr_poll(sr_t *s, int64_t steps, sr_action_t *act) {
    int64_t fire_at = (int64_t)((s->c.cam_to_pick_mm - s->c.lead_mm) * s->c.steps_per_mm), win = (int64_t)(s->c.window_mm * s->c.steps_per_mm), gone = (int64_t)(s->c.cam_to_pick_mm * s->c.steps_per_mm) + win;
    for (int i = 0; i < SR_MAX_ITEMS; i++) { sr_item_t *t = &s->it[i]; if (!t->used) continue; int64_t travelled = steps - t->detect_steps;
        if (!t->fired && travelled >= fire_at) {
            if (travelled > fire_at + win) { t->fired = true; s->missed++; }                       /* we were not polled in time (belt jumped or firmware stalled): do not act late */
            else { t->fired = true; if (t->action != SR_PASS) { s->fired++; *act = t->action; return t->id; } } }
        if (travelled > gone) t->used = false; }                                                  /* item has left the station: free the slot */
    return 0; }
