# BioTray vertical-farm tray controller: manufacturing manual

> **Status: design only; nothing built.** PCB: **order-ready: every automatic check passes**. Firmware control core host-tested (22 checks); ESP32 glue never compiled. pH/EC calibration values are placeholders.

## 1. What is made

A 100 x 80 mm controller: 12 V in, ESP32-S3 (WiFi/MQTT), four low-side 12 V outputs (2 pumps, fan, PWM grow light), DS18B20, I2C (BH1750/SHT31), water-level switch, analog pH and EC inputs.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB | `utility10/pcb/release/biotray/` and `biotray/hardware/` | **order-ready: every automatic check passes** |
| Control core + tests | `biotray/firmware/lib/bt_core.[ch]`, `test/test_bt.c` | passes |
| ESP32 skeleton | `biotray/firmware/src/main_biotray.cpp` | not compiled |

## 3. Bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| J2 | 12 V DC in | BarrelJack_CUI_PJ-063AH_Horizontal | CUI/Same Sky PJ-063AH | C22434582 | hand/THT |
| F1 | PTC 1A 16V | Fuse_1812_4532Metric | Littelfuse 1812L110/16DR | C142746 | SMT (JLC) |
| D3 | SMBJ15A | D_SMB | Littelfuse SMBJ15A | C83846 | SMT (JLC) |
| Q5 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| D4 | BZT52C12 | D_SOD-123 | DIODES BZT52C12-7-F | C124196 | SMT (JLC) |
| R40 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C30 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VZH101M1VTR-0607 | C176683 | SMT (JLC) |
| C31 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | SMT (JLC) |
| U2 | AP63205WU-7 | TSOT-23-6 | AP63205WU-7 | C2071056 | SMT (JLC) |
| R41 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| C32 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| L1 | 4.7u | L_Changjiang_FNR5040S | Changjiang FNR5040S4R7MT | C167963 | SMT (JLC) |
| C33 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| C34 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| D5 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | SMT (JLC) |
| C35 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C36 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | SMT (JLC) |
| C37 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| J1 | USB-C | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| D6 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | SMT (JLC) |
| R45 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| J7 | Water temp DS18B20 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| R46 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| J8 | I2C (BH1750 / SHT31) | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| R47 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| R48 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| J9 | Water-level float switch | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| R49 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J10 | pH module (0-3 V analog) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| R50 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C40 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| J11 | EC module (0-3 V analog) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| R51 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C41 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| J12 | UART flash/debug (USB-serial adapter) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| Q1 | AO3400A | SOT-23 | AO3400A | C20917 | SMT (JLC) |
| R10 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| R14 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| J3 | Pump 1 | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| D10 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| Q2 | AO3400A | SOT-23 | AO3400A | C20917 | SMT (JLC) |
| R11 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| R15 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| J4 | Pump 2 | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| D11 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |
| Q3 | AO3400A | SOT-23 | AO3400A | C20917 | SMT (JLC) |
| R12 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| R16 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| J5 | Grow light (PWM) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| Q4 | AO3400A | SOT-23 | AO3400A | C20917 | SMT (JLC) |
| R13 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| R17 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| J6 | Fan | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| D13 | SS14 | D_SMA | SS14 | C84343 | SMT (JLC) |

### Bought-in

12 V 3 A adapter (barrel 5.5/2.1, centre positive), 12 V peristaltic or submersible pumps, 12 V fan, 12 V LED grow strip (total under 1.1 A or replace the PTC), DS18B20 probe, BH1750 module, float switch, pH module and probe, EC module and probe, tubing, tray.

## 4. Make the board

1. Upload `utility10/pcb/release/biotray/1_fabrication/biotray_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; 1 oz is fine for loads up to about 1 A total). 2. For assembly upload `2_assembly/biotray_JLC_BOM.csv` and `biotray_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.

## 5. Program and configure

Arduino-ESP32 core 2.x with PubSubClient, OneWire, DallasTemperature, BH1750. Copy `secrets.h.example` to `secrets.h`. Calibrate pH with pH 4 and pH 7 buffers and EC with a standard solution, then edit `PH_CAL`, `EC_CAL`. MQTT topics: see `biotray/docs/DESIGN.md`.

## 6. Test (see `biotray/docs/TEST_PLAN.md`)

Supply rails, reverse-polarity test, dummy loads on every output, dry-run test (remove water: pump stops and latches), 48 h run.

## 7. Limits

Water, mains adapter and electricity together: use a GFCI-protected supply and an enclosure with proper sealing. No isolation on the pH probe. Not tested on hardware.
