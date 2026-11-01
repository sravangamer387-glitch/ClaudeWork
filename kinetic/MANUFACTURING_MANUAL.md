# KINETIC motion controller + vibration puck: manufacturing manual

> **Status: design only; nothing built, powered or run on a motor.** Controller PCB: **PCB not released yet: do not send to a fab**. Vibration puck PCB: **PCB not released yet: do not send to a fab**. AI model: trained on synthetic data only. Firmware: motion/vibration core host-tested; ESP32 glue syntax-checked only.

## 1. What is made

A 112 x 80 mm controller (ESP32-S3, three StepStick driver sockets, 24 V input, 5 V buck, endstops, host UART/USB) and a 25 x 26 mm ADXL345 vibration puck on a 6-pin SPI cable. Drivers (A4988 / DRV8825 / TMC2209 modules) and motors are bought separately.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| Controller PCB (Gerbers, BOM, CPL, KiCad, STEP) | `utility10/pcb/release/kinetic_ctl/` and `kinetic/hardware/kinetic_ctl/` | **PCB not released yet: do not send to a fab** |
| Vibration puck PCB | `utility10/pcb/release/kinetic_vib/` and `kinetic/hardware/kinetic_vib/` | **PCB not released yet: do not send to a fab** |
| Motion + protocol library and tests | `kinetic/firmware/lib/kn_motion.[ch]`, `kinetic/firmware/test/test_kn.c` | `make test` passes (370 checks) |
| Vibration model | `kinetic/sim/vib.py`, `kinetic/firmware/lib/kn_vib*.{c,h}` | synthetic data; C matches Python |
| ESP32 skeleton | `kinetic/firmware/src/main_kinetic.cpp` | syntax-checked, never compiled for ESP32 |
| Enclosure STL (printed) | `utility10/pcb/release/kinetic_ctl/4_enclosure/` | generated from the board outline; unprototyped |
| Docs | `kinetic/docs/` (CONCEPT, DESIGN, PROTOCOL, TEST_PLAN, economics, vib_results) | |

### Bought-in

StepStick driver modules (1-3), NEMA17 motors, 12-28 V supply (24 V recommended) with current limit capability for bring-up, 1x8 female socket strips are on the BOM, endstop switches, 6-wire cable for the puck (under 30 cm), M2.5 screws.

## 4. Make the boards

1. Upload `utility10/pcb/release/kinetic_ctl/1_fabrication/kinetic_ctl_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; order 2 oz copper if you will drive more than about 1 A per motor phase: the motor traces are 0.4 mm). 2. For assembly upload `2_assembly/kinetic_ctl_JLC_BOM.csv` and `kinetic_ctl_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.
Repeat for `kinetic_vib` (1 oz is fine).

## 5. Program

Build with Arduino-ESP32 core 2.x or PlatformIO (`esp32-s3-devkitc-1`): sources `kinetic/firmware/src/main_kinetic.cpp` plus `kinetic/firmware/lib/*.c`. First flash over USB-C (hold BOOT, tap RESET). **Review the skeleton on a bench first: it has never been compiled for the ESP32.**

## 6. Commissioning (see `kinetic/docs/TEST_PLAN.md` for the full list)

1. Current-limited 24 V, no drivers fitted: TP1 24 V, TP2 5.0 V, TP3 3.3 V. 2. Reverse the supply once with 100 mA limit: nothing conducts. 3. Fit ONE driver with the motor disconnected; set its current limit; power off; connect the motor. 4. `MOVE X=1000` and watch STEP/DIR on a scope. 5. Endstop trip stops motion and needs `CLEAR`. 6. Puck: device ID 0xE5, rest Z = +1 g.

## 7. Safety and limits

Never plug or unplug a motor with power on (destroys drivers). The TVS and bulk capacitor assume at most 28 V. No ESD protection on USB data. The 3.3 V LDO is limited to 600 mA. The vibration classifier is a demonstration trained on simulated faults: do not use it to decide maintenance without retraining on real recordings. Not safety-rated: it is not an emergency-stop system.
