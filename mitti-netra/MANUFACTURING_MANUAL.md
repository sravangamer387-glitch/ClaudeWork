# MITTI-NETRA soil and structure telemetry node: manufacturing manual

> **Status: design only; nothing built or connected to a mobile network.** PCB: **order-ready: every automatic check passes**. The cellular modem is a plug-in SIM7080G breakout (not on the board). Firmware core host-tested; ESP32 glue syntax-checked only.

## 1. What is made

A 90 x 80 mm solar/USB-charged node: ESP32-S3, TP4056 charger for one protected Li-ion cell, 3.3 V LDO, switched socket for a SIM7080G breakout, ADXL345 tilt/vibration, HX711 strain bridge input, capacitive soil probe input, DS18B20 input. An optional Raspberry Pi/Banana Pi runs `camera/crop_index.py`.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB | `utility10/pcb/release/mitti/` and `mitti-netra/hardware/` | **order-ready: every automatic check passes** |
| Core library and tests | `mitti-netra/firmware/lib/mn_core.[ch]`, `test/test_mn.c` | `make test` passes (23 checks) |
| ESP32 skeleton | `mitti-netra/firmware/src/` | syntax-checked only; cellular send is a TODO |
| Camera analysis | `mitti-netra/camera/crop_index.py` | self-test passes on synthetic scenes |

## 3. Bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | SMT (JLC) |
| C37 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| J1 | USB-C (charge + program) | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| J2 | Solar panel 5-6 V | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| D1 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| D2 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| C1 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| U4 | TP4056 | HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm | TPOWER TP4056 | C382139 | SMT (JLC) |
| R1 | 2.2k | R_0603_1608Metric | 0603 2.2k 1% | C4190 | SMT (JLC) |
| C2 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| D3 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R2 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| D4 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R3 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| J3 | Li-ion cell (protected!) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | SMT (JLC) |
| C3 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R4 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | SMT (JLC) |
| R5 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | SMT (JLC) |
| C5 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| Q1 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| R6 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| Q2 | AO3400A | SOT-23 | AO3400A | C20917 | SMT (JLC) |
| R7 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| R8 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| C6 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VEJ101M1VTT-0607L | C7442639 | SMT (JLC) |
| C7 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| J6 | Cellular modem (SIM7080G breakout) | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| U5 | ADXL345 | LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y | ADXL345BCCZ-RL7 | C9667 | SMT (JLC) |
| C8 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C9 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R9 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| R10 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| U2 | HX711 | SOIC-16_3.9x9.9mm_P1.27mm | HX711 | C43656 | SMT (JLC) |
| R11 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| C10 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C11 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C12 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C13 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R12 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| C14 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C15 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| J4 | Strain-gauge bridge E+ E- A+ A- | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| J5 | Soil probe (capacitive, 3.3 V) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J7 | DS18B20 temp | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S | C131339 | hand/THT |
| R13 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| R15 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C16 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D5 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R14 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| J8 | UART flash/debug (USB-serial adapter) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |

### Bought-in

SIM7080G (LTE-M/NB-IoT) breakout board with nano-SIM holder and antenna; protected 18650 cell (or protected pouch cell) with JST-PH 2 lead; 5-6 V solar panel (2 W) with JST-PH 2 lead; capacitive soil moisture probe (3.3 V, analog) with JST-PH 3 lead; DS18B20 waterproof probe; strain gauges (350 ohm, GF about 2) with bridge completion; IP65 enclosure with cable glands; a SIM and data plan.

## 4. Make the board

1. Upload `utility10/pcb/release/mitti/1_fabrication/mitti_netra_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; 1 oz is fine). 2. For assembly upload `2_assembly/mitti_netra_JLC_BOM.csv` and `mitti_netra_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.
The ADXL345 is an LGA-14 part: use the fab's reflow assembly; do not hand-solder it.

## 5. Program and configure

Arduino-ESP32 core 2.x: `mitti-netra/firmware/src/main_mitti.cpp` plus `firmware/lib/mn_core.c`. Set the placeholders: soil calibration counts (dry air, water), strain excitation/gauge factor/bridge type, tilt and strain thresholds. Install: tilt the node into its final position, power up once: that boot stores the baseline (tilt angles and strain zero) in RTC memory; a power loss loses the baseline.

## 6. Test (see `mitti-netra/docs/TEST_PLAN.md`)

Charge LEDs; TP2 3.3 V; deep-sleep current; modem switch toggles VBAT_M; ADXL345 ID 0xE5; tilt plate 10 degrees reads 10 +-0.5; HX711 shunt-resistor check; 7-day outdoor run.

## 7. Limits

No cell protection on the board (use protected cells). LDO stops below about 3.55 V on the cell. Strain numbers are conversions, not a calibrated instrument. Carrier APN, bands and a server are not provided. Not safety-rated.
