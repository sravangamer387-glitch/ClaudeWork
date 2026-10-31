#include "toycore.h"
uint32_t tc_rand(uint32_t *s) { uint32_t x = *s ? *s : 2463534242u; x ^= x << 13; x ^= x >> 17; x ^= x << 5; *s = x; return x; }

void rr_init(rr_t *r, uint32_t seed) { r->st = RR_IDLE; r->seed = seed ? seed : 1; r->locked = 0; r->winner = -1; for (int i = 0; i < 4; i++) r->score[i] = 0; r->react_ms = 0; r->tie = false; r->t_go = r->t_state = 0; }
void rr_step(rr_t *r, uint32_t now, uint8_t b) {
    b &= 0x0F;
    switch (r->st) {
    case RR_IDLE: case RR_RESULT:
        if (b && (uint32_t)(now - r->t_state) > 800u) { r->st = RR_WAIT; r->locked = 0; r->winner = -1; r->tie = false; r->t_state = now; r->t_go = now + 2000u + tc_rand(&r->seed) % 4001u; }
        break;
    case RR_WAIT:
        for (int i = 0; i < 4; i++) if ((b >> i & 1) && !(r->locked >> i & 1)) { r->locked |= (uint8_t)(1u << i); if (r->score[i] > -9) r->score[i]--; }   /* false start */
        if (r->locked == 0x0F) { r->st = RR_RESULT; r->t_state = now; }                                    /* everybody jumped the gun: round void */
        else if ((int32_t)(now - r->t_go) >= 0) r->st = RR_GO;
        break;
    case RR_GO: {
        uint8_t live = b & (uint8_t)~r->locked;
        if (live) {
            int n = 0, first = -1; for (int i = 0; i < 4; i++) if (live >> i & 1) { n++; if (first < 0) first = i; }
            r->react_ms = (uint16_t)(now - r->t_go); r->st = RR_RESULT; r->t_state = now;
            if (n == 1) { r->winner = (int8_t)first; if (r->score[first] < 99) r->score[first]++; } else r->tie = true;   /* same-millisecond press: replay, no point */
        } else if ((uint32_t)(now - r->t_go) > 5000u) { r->st = RR_RESULT; r->t_state = now; }              /* nobody pressed in 5 s */
        break; }
    }
}

void tm_init(tm_t *m, uint32_t seed) { m->seed0 = seed ? seed : 1; m->s = m->seed0; m->len = 1; m->pos = 0; m->showing = true; m->show_i = 0; m->t = 0; m->over = false; m->best = 0; }
uint8_t tm_note(const tm_t *m, uint8_t i) { uint32_t s = m->seed0; uint8_t n = 0; for (uint8_t k = 0; k <= i; k++) n = (uint8_t)(tc_rand(&s) & 3u); return n; }
int tm_press(tm_t *m, uint8_t pad) {
    if (m->over || m->showing) return 0;
    if (pad != tm_note(m, m->pos)) { m->over = true; return 3; }
    m->pos++;
    if (m->pos == m->len) { if (m->len > m->best) m->best = m->len; m->len++; m->pos = 0; m->showing = true; m->show_i = 0; return 2; }
    return 1;
}

void ab_init(ab_t *a, uint32_t seed) { a->seed = seed ? seed : 1; a->running = a->exploded = false; a->t0 = a->fuse_ms = 0; }
void ab_start(ab_t *a, uint32_t now, uint32_t mn, uint32_t mx) { a->t0 = now; a->fuse_ms = mn + tc_rand(&a->seed) % (mx - mn + 1u); a->running = true; a->exploded = false; }
void ab_step(ab_t *a, uint32_t now) { if (a->running && (uint32_t)(now - a->t0) >= a->fuse_ms) { a->running = false; a->exploded = true; } }
uint16_t ab_beep_interval_ms(const ab_t *a, uint32_t now) {
    if (!a->running) return 0;
    uint32_t left = a->fuse_ms - (uint32_t)(now - a->t0); if ((int32_t)left < 0) left = 0;
    if (left > 20000u) return 1000;
    if (left > 10000u) return 600;
    if (left > 5000u) return 300;
    return 120;     /* beeps speed up as the fuse burns down */
}

void br_init(br_t *b, uint32_t seed) { b->notes = 0; b->seed = seed ? seed : 1; b->t_move = 0; b->speed_ms = 400; b->score = 0; b->combo = 0; b->misses = 0; b->over = false; b->moves = 0; }
void br_step(br_t *b, uint32_t now) {
    if (b->over || (uint32_t)(now - b->t_move) < b->speed_ms) return;
    b->t_move = now; b->moves++;
    if (b->notes & 1u) { b->misses++; b->combo = 0; if (b->misses >= 5) b->over = true; }                 /* note left the hit zone unplayed */
    b->notes >>= 1;
    if (tc_rand(&b->seed) % 3u == 0) b->notes |= (uint16_t)(1u << (BR_LEDS - 1));                       /* spawn at the far end */
    if (b->moves % 40 == 0 && b->speed_ms > 150) b->speed_ms -= 25;                                      /* gets faster */
}
int br_press(br_t *b) {
    if (b->over) return 0;
    int pts = 0;
    if (b->notes & 1u) { pts = 3; b->notes &= ~1u; } else if (b->notes & 2u) { pts = 1; b->notes &= ~2u; }
    if (pts) { if (b->combo < 255) b->combo++; b->score += pts * (1 + b->combo / 5); } else { b->combo = 0; b->misses++; if (b->misses >= 5) b->over = true; }
    return pts;
}
