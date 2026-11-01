# KINETIC design

## 1. Architecture
ESP32-S3 module (native USB) -> three StepStick sockets (STEP/DIR/EN each) -> motors. Endstops (3), SPI vibration puck, host over USB-CDC or UART (JST-PH 3). 24 V in -> AO3401A reverse-polarity PMOS (12 V zener gate clamp) -> VM rail to drivers and to an AP63205 5 V buck -> AP2112K 3.3 V LDO. USB VBUS can power the logic through an SS14 so the board can be flashed without the motor supply.

## 2. Motion library (`firmware/lib/kn_motion.c`)
- **Point-to-point:** symmetric 7-segment S-curve with limits vmax, amax, jmax. Closed-form phase times: if vmax*jmax < amax^2 the acceleration never saturates (Tj = sqrt(vmax/jmax)); otherwise Tj = amax/jmax and Ta = Tj + vmax/amax. Short moves reduce the peak velocity (or the acceleration or both) to hit the exact distance. Position, velocity, acceleration and jerk are evaluated analytically, so there is no integration drift.
- **Coordinated moves:** the dominant axis (largest delta) follows the S-curve; other axes keep a fixed ratio; each tick emits at most one step per axis using exact integer bookkeeping, so the final position is exact and the path stays within 1 step of the straight line (tested: 0.9 step).
- **Online follower:** for streamed AI setpoints; square-root approach law for the desired velocity, an acceleration target a = sat(sqrt(2*J*|dv|)) so acceleration reaches zero as velocity reaches the target, and a jerk slew limit. Constant time per call. Tracking lag at constant target speed v is about v/K with K = 2*sqrt(J/V) (7 steps at 200 steps/s with the test limits).
- **Protocol:** `MOVE X=1000 Y=-250 F=2000*5A` ASCII lines with optional CRC-8 (poly 0x07), commands MOVE/HOME/STOP/LIMITS (see PROTOCOL.md).
- **Timing:** one 20 kHz timer tick; at most one step per axis per tick => 10 kHz maximum step rate per axis at a one-tick pulse width (the driver minimum pulse is about 1-2 us, satisfied by a 50 us tick).

## 3. Vibration monitoring (`sim/vib.py`, `firmware/lib/kn_vib.c`)
- Window 1024 samples at 3200 Hz; shaft speed 8-25 Hz (480-1500 rpm), known from the planner.
- Features (10): log rms, kurtosis, crest factor, envelope-spectrum power at 1x, BPFO, 2*BPFO, BPFI, BPFI +- 1x sidebands, and raw spectrum power at 1x and 2x. The envelope comes from a 300 Hz high-pass, rectification and a 150 Hz low-pass, decimated to 400 Hz.
- Model: 10-16-8-4 MLP, int8 weights (320 bytes), float requantisation. Classes: healthy, outer-race, inner-race, unbalance.
- Cross-check: the C features match the Python features within 0.05 % and the classes agree on every test vector.

## 4. Hardware choices
| Block | Choice | Reason |
|---|---|---|
| MCU | ESP32-S3-WROOM-1-N8 | native USB, 3 timers + SPI + enough GPIO, cheap |
| Drivers | sockets for StepStick modules | user picks A4988 (cheap), DRV8825 (1/32) or TMC2209 (silent); current set by module Vref |
| Buck | AP63205WU-7 (4.7 uH, 2 x 22 uF) | 3.8-32 V in, 2 A, fixed 5 V |
| Protection | SMBJ28A, AO3401A + BZT52C12 | 28 V standoff TVS; PMOS survives 24 V because the zener clamps Vgs to 12 V |
| Sensor | ADXL345 on SPI | 3200 Hz output rate, +-16 g, widely available |

## 5. Known risks
LDO headroom for WiFi bursts; no ESD diodes on USB data lines; hot-plugging motors destroys drivers (warn in manual); TVS and bulk capacitor ratings assume a supply of 28 V maximum; ESP32-S3 antenna keep-out on the right edge must stay free of metal enclosure parts.
