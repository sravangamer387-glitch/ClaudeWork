# KINETIC motion controller + vibration puck: manufacturing manual

> **Status: design only; nothing built, powered or run on a motor.** Controller PCB: **order-ready: every automatic check passes**. Vibration puck PCB: **order-ready: every automatic check passes**. AI model: trained on synthetic data only. Firmware: motion/vibration core host-tested; ESP32 glue syntax-checked only.

## 1. What is made

A 112 x 80 mm controller (ESP32-S3, three StepStick driver sockets, 24 V input, 5 V buck, endstops, host UART/USB) and a 25 x 26 mm ADXL345 vibration puck on a 6-pin SPI cable. Drivers (A4988 / DRV8825 / TMC2209 modules) and motors are bought separately.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| Controller PCB (Gerbers, BOM, CPL, KiCad, STEP) | `utility10/pcb/release/kinetic_ctl/` and `kinetic/hardware/kinetic_ctl/` | **order-ready: every automatic check passes** |
| Vibration puck PCB | `utility10/pcb/release/kinetic_vib/` and `kinetic/hardware/kinetic_vib/` | **order-ready: every automatic check passes** |
| Motion + protocol library and tests | `kinetic/firmware/lib/kn_motion.[ch]`, `kinetic/firmware/test/test_kn.c` | `make test` passes (370 checks) |
| Vibration model | `kinetic/sim/vib.py`, `kinetic/firmware/lib/kn_vib*.{c,h}` | synthetic data; C matches Python |
| ESP32 skeleton | `kinetic/firmware/src/main_kinetic.cpp` | syntax-checked, never compiled for ESP32 |
| Enclosure STL (printed) | `utility10/pcb/release/kinetic_ctl/4_enclosure/` | generated from the board outline; unprototyped |
| Docs | `kinetic/docs/` (CONCEPT, DESIGN, PROTOCOL, TEST_PLAN, economics, vib_results) | |

## 3. Controller bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| J5 | 24 V in | TerminalBlock_bornier-2_P5.08mm | KF128-5.08-2P-AA | C474952 | hand/THT |
| D3 | SMBJ28A | D_SMB | Littelfuse SMBJ28A | C178227 | SMT (JLC) |
| Q5 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| D4 | BZT52C12 | D_SOD-123 | DIODES BZT52C12-7-F | C124196 | SMT (JLC) |
| R40 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C30 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VEJ101M1VTT-0607L | C7442639 | SMT (JLC) |
| C31 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | SMT (JLC) |
| U2 | AP63205WU-7 | TSOT-23-6 | AP63205WU-7 | C2071056 | SMT (JLC) |
| R41 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| C32 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| L1 | 4.7u | L_Changjiang_FNR5040S | Changjiang FNR5040S4R7MT | C167963 | SMT (JLC) |
| C33 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| C34 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| D5 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | SMT (JLC) |
| C35 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C36 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | SMT (JLC) |
| C37 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| J1 | USB-C | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| D6 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R45 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R46 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R47 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C40 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| J7 | Host UART (Pi/PC) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J3 | Vibration sensor SPI | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J8 | Endstop X | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J9 | Endstop Y | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J10 | Endstop Z | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| R48 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C41 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R49 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C42 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R50 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C43 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| J11 | X driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J12 | X driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J20 | Motor X | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| R51 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J13 | Y driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J14 | Y driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J21 | Motor Y | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| R52 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J15 | Z driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J16 | Z driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | hand/THT |
| J22 | Motor Z | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| R53 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |

### Vibration puck bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ADXL345 | LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y | ADXL345BCCZ-RL7 | C9667 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| J3 | SPI to controller | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |

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
