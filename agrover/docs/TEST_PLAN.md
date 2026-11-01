# AGROVER test plan (bench and field steps not yet run)
A (PC): `cd firmware && make test`; `python3 cad/chassis.py`.
B (bench, wheels off the ground): motor directions and encoder counts per metre (set `dist_per_tick_m`), emergency stop cuts motor power in hardware, fuse and polarity checks.
C (yard, flat ground): straight run 10 m (drift), 360-degree turn (pose closure), waypoint square 5 m x 5 m (end error), then repeat on soil and on a slope.
D (obstacles): foam-block course; sonar false-negative test with thin poles and grass; verify stop distance at full speed.
E (power): drain test from 100 % to the RETURN threshold; compare `rv_soc_pct` with a coulomb counter; solar charge over a day and wake-up behaviour.
