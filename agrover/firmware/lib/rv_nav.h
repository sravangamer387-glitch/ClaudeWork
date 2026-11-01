#ifndef RV_NAV_H
#define RV_NAV_H
#include <stdbool.h>
/* Ag-rover navigation, obstacle avoidance and power core (portable C, host-tested in a simulated field). */
typedef struct { float x, y, th; } rv_pose_t;                                                  /* metres, radians */
typedef struct { float track_m, dist_per_tick_m; } rv_geom_t;
void rv_odom_update(rv_pose_t *p, const rv_geom_t *g, int dticks_left, int dticks_right);    /* midpoint integration */
void rv_wheel_speeds(const rv_geom_t *g, float v, float w, float *vl, float *vr);             /* skid steer / differential */
/* pure pursuit along a polyline */
typedef struct { float x, y; } rv_pt_t;
typedef struct { const rv_pt_t *wp; int n; int seg; float lookahead_m, goal_tol_m; bool done; } rv_path_t;
void rv_path_init(rv_path_t *p, const rv_pt_t *wp, int n, float lookahead_m, float goal_tol_m);
void rv_pursuit(rv_path_t *p, const rv_pose_t *pose, float v_cmd, float *v, float *w);        /* sets p->done at the goal */
/* obstacle avoidance from three ultrasonic ranges (metres, <= 0 means no echo/invalid) */
typedef struct { float stop_m, slow_m; float turn_rate; } rv_avoid_t;
typedef struct { float dir; int clear_count; } rv_avoid_state_t;                                /* remembers the chosen evasion side until the way is clear for a while */
void rv_avoid(const rv_avoid_t *a, rv_avoid_state_t *st, float left_m, float centre_m, float right_m, float *v, float *w);
/* battery state of charge (4S LiFePO4 pack volts) with load compensation, and mission gating with hysteresis */
float rv_soc_pct(float pack_v, float load_a, float r_int_ohm);
typedef enum { RV_RUN = 0, RV_RETURN = 1, RV_SLEEP = 2 } rv_mode_t;
rv_mode_t rv_power_mode(rv_mode_t cur, float soc_pct, bool sun_ok);
#endif
