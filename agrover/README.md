# AGROVER: solar-powered 4x4 field rover (navigation, obstacle avoidance, power management)

Programme 7 (mechanical + agriculture + civil + AI). **Status: navigation/avoidance/power core host-tested in a simulated field (19 checks); chassis plates generated; NO custom PCB; nothing built, driven or taken outdoors.**

## What exists
- `firmware/lib/rv_nav.[ch]`: skid-steer kinematics and odometry; pure-pursuit path following; three-ultrasonic obstacle avoidance with a committed evasion side (no left-right chatter) that fades out the path command near an obstacle (no deadlock); 4S LiFePO4 state-of-charge estimate with load compensation; RUN / RETURN / SLEEP power modes with hysteresis (return below 30 %, sleep below 15 %, wake above 40 % with sun).
- `firmware/test/test_rv.c` (`make test`): straight and in-place-turn odometry, wheel-speed maths, a zig-zag row path, an obstacle course with minimum-clearance and no-chatter checks, and the power state machine. Two real deadlock/chatter bugs were found and fixed by these tests.
- `cad/chassis.py` -> `cad/out/*.svg`: laser-cut base plate (motor slots, battery strap slots, M3 grid), top deck for the solar panel, ultrasonic sensor bracket.

## Hardware (all bought-in; no custom PCB)
| Part | Spec (suggested) | Note |
|---|---|---|
| Controller | ESP32-S3 dev board | runs `rv_nav`; MQTT over WiFi for telemetry |
| Motors | 4 x 12 V geared DC motors with quadrature encoders | choose torque for your slope and soil |
| Drivers | 2 x dual H-bridge modules rated at least 2x stall current | PWM + direction from the ESP32 |
| Battery | 4S LiFePO4, 12.8 V nominal, with its own BMS | the SoC curve in `rv_soc_pct` assumes this chemistry |
| Solar | 50 W panel + MPPT charge controller made for LiFePO4 (14.4 V absorption) | the controller sets safety limits, not this firmware |
| Sensors | 3 x ultrasonic (left, centre, right), optional camera/multispectral payload on a Pi | 5 V sensors need level shifting to 3.3 V |
| Protection | 20 A fuse at the battery, inline switch, reverse-polarity protection | mandatory |

## Honest limits
Navigation is dead-reckoning plus reactive avoidance: no GPS fix, no visual SLAM, no map. Wheel slip on soil will drift the pose; add GNSS/IMU fusion before any unattended use. Ultrasonic sensing misses thin stalks and soft vegetation. The SoC table is typical, not your pack. Solar charging, BMS limits and wiring are the responsibility of the commercial modules you pick. A moving robot with batteries outdoors needs a hardware emergency stop and a safety review. Visual SLAM and the multispectral payload are described as the next step, not implemented.
