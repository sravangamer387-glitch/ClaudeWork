#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "../lib/toycore.h"
static int fails = 0, checks = 0;
#define CHECK(c, ...) do { checks++; if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
int main(void) {
    /* rand: nonzero, roughly uniform */
    uint32_t s = 1; int bins[8] = {0}; for (int i = 0; i < 80000; i++) { uint32_t v = tc_rand(&s); CHECK(v != 0, "zero"); bins[v % 8]++; }
    for (int i = 0; i < 8; i++) CHECK(abs(bins[i] - 10000) < 400, "rand bin %d = %d", i, bins[i]);
    uint32_t z = 0; CHECK(tc_rand(&z) != 0, "zero seed handled");
    /* Reflex Raja */
    rr_t r; rr_init(&r, 7); uint32_t t = 1000;
    rr_step(&r, t, 1); CHECK(r.st == RR_WAIT, "round starts"); uint32_t go = r.t_go; CHECK(go - t >= 2000 && go - t <= 6000, "delay %u", (unsigned)(go - t));
    t += 1000; rr_step(&r, t, 2); CHECK(r.score[1] == -1 && (r.locked & 2), "false start penalised");
    t = go; rr_step(&r, t, 0); CHECK(r.st == RR_GO, "go");
    rr_step(&r, t + 5, 2); CHECK(r.st == RR_GO, "locked-out player cannot win");
    rr_step(&r, t + 180, 4); CHECK(r.st == RR_RESULT && r.winner == 2 && r.score[2] == 1 && r.react_ms == 180, "winner p2 180 ms (%d)", r.winner);
    rr_step(&r, t + 190, 1); CHECK(r.st == RR_RESULT, "debounce: new round blocked 800 ms");
    rr_init(&r, 9); rr_step(&r, 1000, 1); go = r.t_go; rr_step(&r, go, 0); rr_step(&r, go + 50, 3); CHECK(r.tie && r.winner == -1 && r.score[0] == 0, "same-tick press is a tie, no point");
    rr_init(&r, 9); rr_step(&r, 1000, 1); rr_step(&r, 1100, 15); CHECK(r.st == RR_RESULT, "all false start voids round");
    /* delay distribution: 2-6 s, mean about 4 s, cannot be predicted from previous (different values) */
    double sum = 0; uint32_t mn = 99999, mx = 0; rr_init(&r, 12345); for (int i = 0; i < 2000; i++) { r.st = RR_IDLE; r.t_state = 0; rr_step(&r, 100000u * (i + 1), 1); uint32_t d = r.t_go - 100000u * (i + 1); sum += d; if (d < mn) mn = d; if (d > mx) mx = d; }
    CHECK(mn >= 2000 && mx <= 6000 && fabs(sum / 2000 - 4000) < 120, "delay stats min %u max %u mean %.0f", (unsigned)mn, (unsigned)mx, sum / 2000);
    /* fairness: with equal 200 ms reaction every player equally often... simulated reactions N(220, 40) per player; wins roughly equal */
    int wins[4] = {0}; uint32_t rs = 77; for (int i = 0; i < 4000; i++) { double best = 1e9; int bw = 0; for (int p = 0; p < 4; p++) { double u1 = (tc_rand(&rs) % 10000 + 1) / 10001.0, u2 = (tc_rand(&rs) % 10000) / 10000.0; double x = 220 + 40 * sqrt(-2 * log(u1)) * cos(6.2832 * u2); if (x < best) { best = x; bw = p; } } wins[bw]++; }
    for (int p = 0; p < 4; p++) CHECK(abs(wins[p] - 1000) < 120, "equal players win about equally: %d", wins[p]);
    /* Taal Memory */
    tm_t m; tm_init(&m, 99); m.showing = false; uint8_t first = tm_note(&m, 0); CHECK(tm_press(&m, first) == 2 && m.len == 2 && m.showing, "round 1 complete grows sequence");
    m.showing = false; CHECK(tm_press(&m, tm_note(&m, 0)) == 1, "first note ok"); CHECK(tm_press(&m, (uint8_t)((tm_note(&m, 1) + 1) & 3)) == 3 && m.over && m.best == 1, "wrong note ends game, best=1");
    CHECK(tm_press(&m, 0) == 0, "no input after game over");
    tm_init(&m, 5); int perfect = 1; for (int round = 1; round <= 60; round++) { m.showing = false; for (int i = 0; i < round; i++) { int r2 = tm_press(&m, tm_note(&m, (uint8_t)i)); if (r2 == 0 || r2 == 3) perfect = 0; } } CHECK(perfect && m.best == 60, "perfect player reaches 60, best=%d", m.best);
    int cnt[4] = {0}; for (int i = 0; i < 4000; i++) cnt[tm_note(&m, (uint8_t)(i % 100))]++; /* not exact, check all pads used */ for (int p = 0; p < 4; p++) CHECK(cnt[p] > 600, "pad %d used %d", p, cnt[p]);
    tm_init(&m, 1); uint8_t a0 = tm_note(&m, 3), a1 = tm_note(&m, 3); CHECK(a0 == a1, "sequence is repeatable");
    /* Aloo Bomb */
    ab_t a; ab_init(&a, 3); double fs = 0; uint32_t fmin = 1e9, fmax = 0; for (int i = 0; i < 3000; i++) { ab_start(&a, 0, 20000, 60000); fs += a.fuse_ms; if (a.fuse_ms < fmin) fmin = a.fuse_ms; if (a.fuse_ms > fmax) fmax = a.fuse_ms; }
    CHECK(fmin >= 20000 && fmax <= 60000 && fabs(fs / 3000 - 40000) < 800, "fuse stats %u..%u mean %.0f", (unsigned)fmin, (unsigned)fmax, fs / 3000);
    ab_start(&a, 1000, 30000, 30000); CHECK(ab_beep_interval_ms(&a, 1000) == 1000 && ab_beep_interval_ms(&a, 1000 + 24000) == 300 && ab_beep_interval_ms(&a, 1000 + 28000) == 120, "beeps speed up");
    ab_step(&a, 1000 + 29999); CHECK(!a.exploded, "not yet"); ab_step(&a, 1000 + 30000); CHECK(a.exploded && ab_beep_interval_ms(&a, 99999) == 0, "explodes at fuse");
    ab_start(&a, 0xFFFFFF00u, 1000, 1000); ab_step(&a, 0xFFFFFF00u + 999); CHECK(!a.exploded, "wrap ok"); ab_step(&a, 0xFFFFFF00u + 1000); CHECK(a.exploded, "wrap explode");
    /* Beat Runner */
    br_t b; br_init(&b, 4); uint32_t tt = 0; int played = 0, pts = 0;
    for (int i = 0; i < 4000 && !b.over; i++) { tt += 400; br_step(&b, tt); if (b.notes & 1u) { pts += br_press(&b); played++; } }
    CHECK(!b.over && played > 500 && b.score > 1000, "perfect player never loses: played %d score %d", played, (int)b.score);
    br_init(&b, 4); tt = 0; for (int i = 0; i < 400 && !b.over; i++) { tt += 500; br_step(&b, tt); } CHECK(b.over, "idle player loses after 5 misses");
    br_init(&b, 4); b.notes = 2; CHECK(br_press(&b) == 1, "good window"); b.notes = 1; CHECK(br_press(&b) == 3, "perfect window"); CHECK(br_press(&b) == 0 && b.misses == 1, "empty press is a miss");
    br_init(&b, 4); for (int i = 0; i < 3000; i++) { tt += 400; br_step(&b, tt); b.misses = 0; } CHECK(b.speed_ms >= 150 && b.speed_ms < 400, "speeds up but stays playable: %d", b.speed_ms);
    printf("%d checks, %d failures\n", checks, fails); return fails ? 1 : 0;
}
