/* KINETIC motion core (C99, no heap, host-testable): jerk-limited point-to-point profiles, multi-axis coordination, an online jerk-limited follower for
 * streamed AI/physics-solver setpoints, step generation, and a checksummed line protocol. Units: steps, seconds. */
#ifndef KN_MOTION_H
#define KN_MOTION_H
#include <stdbool.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define KN_MAXAX 3
typedef struct { double vmax, amax, jmax; } kn_limits_t;
typedef struct { double D, Tj, Ta, Tv, vp, ap, T; kn_limits_t L; bool ok; } kn_profile_t;     /* symmetric 7-segment S-curve, D > 0 */
typedef struct { double s, v, a, j; } kn_state_t;
bool kn_plan(kn_profile_t *p, double dist, kn_limits_t L);                                  /* time-optimal under the three limits; dist may be negative (mirrored by the evaluator) */
kn_state_t kn_eval(const kn_profile_t *p, double t, double sign);                             /* exact position/velocity/acceleration/jerk at time t */
/* ---- coordinated move: the longest axis runs the profile, the others follow proportionally ---- */
typedef struct { kn_profile_t prof; double sign; int n; double delta[KN_MAXAX]; double dom; double frac[KN_MAXAX]; int32_t emitted[KN_MAXAX]; int32_t target[KN_MAXAX]; double t; bool done; } kn_move_t;
bool kn_move_start(kn_move_t *m, int n, const int32_t from[], const int32_t to[], kn_limits_t axis_limits);   /* limits apply along the path (dominant axis); returns false for zero-length or bad limits */
/* advance by dt and return the number of steps (-1, 0 or +1 per axis) to emit this tick */
void kn_move_tick(kn_move_t *m, double dt, int8_t steps_out[]);
/* ---- online follower: tracks a streamed target position without ever exceeding jerk/accel/velocity limits ---- */
typedef struct { kn_limits_t L; kn_state_t st; } kn_follow_t;
void kn_follow_init(kn_follow_t *f, kn_limits_t L, double pos);
void kn_follow_step(kn_follow_t *f, double target, double dt);
/* ---- command line protocol: "MOVE X=1000 Y=-250 F=2000*5A" -> checksum is CRC-8 (poly 0x07) of the text before '*' ---- */
typedef enum { KN_CMD_NONE = 0, KN_CMD_MOVE, KN_CMD_HOME, KN_CMD_STOP, KN_CMD_LIMITS, KN_CMD_BAD } kn_cmd_kind_t;
typedef struct { kn_cmd_kind_t kind; bool has[KN_MAXAX]; int32_t pos[KN_MAXAX]; double feed, accel, jerk; const char *err; } kn_cmd_t;
uint8_t kn_crc8(const char *s, int n);
kn_cmd_t kn_parse(const char *line);
#ifdef __cplusplus
}
#endif
#endif
