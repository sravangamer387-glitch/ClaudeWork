# KINETIC test plan (none of the bench steps has been run)

## A. Done on a PC
`make test` (370 checks): profile endpoints exact; velocity, acceleration, jerk within limits for 48 limit/distance combinations; numerical derivatives agree with the analytic ones; 3-axis move ends exactly with at most 1 step per tick and path error under 1.6 steps; follower stays within limits and converges; protocol parse/CRC cases. Vibration: C features equal Python features to 0.05 %, class agreement 24/24.

## B. Bench, power and board (first article, one board)
1. Visual check against `2_assembly/` and the BOM; continuity GND to 24 V terminal reversed polarity must not conduct.
2. Current-limited supply at 24 V, no drivers fitted: TP1 = 24 V, TP2 = 5.0 V +-0.1, TP3 = 3.3 V +-0.1; idle current under 150 mA.
3. Reverse the supply polarity once (current limited to 100 mA): no damage, no current.
4. USB only (no 24 V): ESP32 enumerates, 5 V through SS14, no voltage appears on the 24 V rail.
5. Flash firmware; send `MOVE` with no driver fitted: STEP pins toggle (scope), correct count, direction pin changes with sign.

## C. Motor tests
1. One driver, motor disconnected, set Vref for the motor current; then connect the motor with power OFF.
2. Move 1000 steps at 500 steps/s: smooth, no stall. Increase F to the stall speed; set vmax to 70 % of it.
3. Jerk test: log position at 1 kHz externally; confirm no velocity overshoot at the end of a move; compare move time with `kn_plan` (expect within 5 %).
4. Three axes together: a diagonal line on paper with a pen: straightness visible by eye.
5. Endstops: pressing one during motion halts it within one tick; `CLEAR` required.

## D. Vibration
1. Sensor ID 0xE5; rest reading Z = +1 g +-0.1.
2. Record 5 minutes at 8, 12, 16, 20, 25 Hz shaft speed with a healthy motor; the classifier must say healthy for at least 90 % of windows.
3. Add an unbalance (small screw on a coupling): class 3 must dominate.
4. Replace one motor bearing with a deliberately damaged one (scratched outer race): record and retrain the model on the recordings; report held-out accuracy honestly.
