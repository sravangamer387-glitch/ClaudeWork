#include <stdio.h>
#include "sr_track.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static sr_cfg_t C = {300.0f, 12.0f, 10.0f, 15.0f, 10.0f};        /* camera 300 mm before the picker, fire 12 mm early (actuator latency), 10 mm window, 15 mm dedupe, 10 steps/mm */
int main(void) {
    sr_t s; sr_init(&s, &C); sr_action_t a;
    /* three items 80 mm apart, belt moving one step at a time with a stop in the middle: each must fire exactly once at the right belt position */
    int64_t det[3] = {1000, 1800, 2600}; sr_action_t cls[3] = {SR_PICK_A, SR_PASS, SR_PICK_B}; int fired_ids[3] = {0, 0, 0}; int64_t fired_at[3] = {0, 0, 0};
    for (int i = 0; i < 3; i++) CHECK(sr_detect(&s, cls[i], det[i]) == i + 1, "detect %d", i);
    int nfire = 0; for (int64_t b = 1000; b < 8000; b++) { if (b >= 3000 && b < 3200) continue; int id; while ((id = sr_poll(&s, b, &a)) != 0) { fired_ids[nfire] = id; fired_at[nfire] = b; CHECK((a == SR_PICK_A && id == 1) || (a == SR_PICK_B && id == 3), "action matches item %d", id); nfire++; } }
    CHECK(nfire == 2 && fired_ids[0] == 1 && fired_ids[1] == 3 && s.missed == 0, "fired %d items, missed %d", nfire, s.missed);
    CHECK(fired_at[0] == 1000 + 2880 && fired_at[1] == 2600 + 2880, "fire positions %lld %lld", (long long)fired_at[0], (long long)fired_at[1]);
    /* duplicate detection of the same item in the next frame is ignored; a different class at the same place is not */
    sr_init(&s, &C); CHECK(sr_detect(&s, SR_PICK_A, 500) == 1 && sr_detect(&s, SR_PICK_A, 540) == 0 && sr_detect(&s, SR_PICK_B, 545) == 2 && sr_detect(&s, SR_PICK_A, 900) == 3, "dedupe");
    /* belt jumps over the window (poll too late): no late action, counted as missed */
    sr_init(&s, &C); sr_detect(&s, SR_PICK_A, 0); int id = sr_poll(&s, 5000, &a); CHECK(id == 0 && s.missed == 1 && s.fired == 0, "late poll does not act (missed %d)", s.missed);
    /* belt reverses by 20 mm after an item fired: no second fire */
    sr_init(&s, &C); sr_detect(&s, SR_PICK_A, 0); int cnt = 0; for (int64_t b = 0; b < 3200; b++) while (sr_poll(&s, b, &a)) cnt++; for (int64_t b = 3200; b > 3000; b--) while (sr_poll(&s, b, &a)) cnt++; for (int64_t b = 3000; b < 3500; b++) while (sr_poll(&s, b, &a)) cnt++; CHECK(cnt == 1, "single fire despite reversal (%d)", cnt);
    /* table full: the 17th item is dropped and counted; slots are recycled after the item leaves */
    sr_init(&s, &C); for (int i = 0; i < SR_MAX_ITEMS; i++) CHECK(sr_detect(&s, SR_PASS, 200 * i) > 0, "fill %d", i); CHECK(sr_detect(&s, SR_PASS, 5000) == -1 && s.dropped == 1, "full table");
    for (int64_t b = 0; b < 9000; b += 1) { while (sr_poll(&s, b, &a)) {} }
    CHECK(sr_detect(&s, SR_PASS, 9000) > 0, "slots recycled");
    printf("%d checks, %d failures\n", checks, fails); return fails != 0; }
