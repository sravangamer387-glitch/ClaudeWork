# KINETIC stepper / servo motion controller - main board (rev A)

KINETIC motion controller main board (112 x 80 mm): ESP32-S3 module with native USB, three StepStick-style stepper-driver sockets (A4988 / DRV8825 / TMC2209 modules), 24 V input with TVS and reverse-polarity PMOS, 5 V buck (AP63205) and 3.3 V LDO, three endstop inputs, SPI header for the vibration sensor and a host UART.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 112 x 80 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 3 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 263 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 59 parts, 53 nets.

## Circuit description
- **Power:** 12-28 V in on a 5.08 mm terminal; SMBJ28A TVS; AO3401A reverse-polarity PMOS with a 12 V zener gate clamp (so it survives 24 V); 100 uF + 10 uF bulk; AP63205 buck makes 5 V (4.7 uH, 2 x 22 uF); AP2112K LDO makes 3.3 V for the ESP32 (600 mA limit: do not enable heavy WiFi traffic while all axes run, or add a bigger LDO). USB VBUS joins +5V through an SS14 so the board can be programmed without the motor supply.
- **Drivers:** each of the three sockets takes a 16-pin StepStick module. ENABLE, STEP, DIR come from the ESP32; MS1-3 are tied high (1/16 step on A4988, 1/32 on DRV8825) and RESET/SLEEP are pulled up. VMOT is the switched 24 V rail. Motor leads go to JST-PH 4 connectors (rated about 2 A per pin; set the module current limit accordingly).
- **Inputs:** three endstops (1 k + 100 nF filtered, pull-ups in firmware), battery/supply sense divider (100 k / 10 k) on IO1, native USB on IO19/IO20, boot and reset buttons, status LED, host UART on a JST-PH 3.
- **Sensor:** 6-pin SPI header (3.3 V, GND, SCLK, MOSI, MISO, CS) for the KINETIC vibration puck.

## Power
Idle about 0.1 A at 24 V (ESP32, buck quiescent, LED). Each driver adds its motor current; the buck is limited to 2 A on the 5 V side (logic only).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [112.1, 80.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 117.2 x 85.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| J5 | 24 V in | TerminalBlock_bornier-2_P5.08mm | KF128-5.08-2P-AA | C474952 | verified |
| D3 | SMBJ28A | D_SMB | Littelfuse SMBJ28A | C178227 | verified |
| Q5 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| D4 | BZT52C12 | D_SOD-123 | DIODES BZT52C12-7-F | C124196 | verified |
| R40 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C30 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VEJ101M1VTT-0607L | C7442639 | verified |
| C31 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | verified |
| U2 | AP63205WU-7 | TSOT-23-6 | AP63205WU-7 | C2071056 | verified |
| R41 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| C32 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| L1 | 4.7u | L_Changjiang_FNR5040S | Changjiang FNR5040S4R7MT | C167963 | verified |
| C33 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| C34 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| D5 | SS14 | D_SMA | SS14 | C84343 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | verified |
| C35 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C36 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | verified |
| C37 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| J1 | USB-C | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| D6 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R45 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R46 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R47 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C40 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| J7 | Host UART (Pi/PC) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| J3 | Vibration sensor SPI | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | verified |
| J8 | Endstop X | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| J9 | Endstop Y | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| J10 | Endstop Z | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R48 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C41 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R49 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C42 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R50 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C43 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| J11 | X driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J12 | X driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J20 | Motor X | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R51 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J13 | Y driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J14 | Y driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J21 | Motor Y | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R52 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J15 | Z driver logic | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J16 | Z driver power/motor | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P | C22438158 | verified |
| J22 | Motor Z | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R53 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Before fitting any driver: apply 24 V with a current-limited supply; TP1 = 24 V, TP2 = 5.0 V, TP3 = 3.3 V.
2. Plug USB: the ESP32-S3 enumerates; flash the firmware.
3. Fit ONE driver module with the motor DISCONNECTED, set its current limit (Vref), then connect the motor. Never plug or unplug a motor with power on.
4. Run the `kn_motion` self-test move and the endstop check before connecting all axes.

## Files
`1_fabrication/` Gerber + drill zip (upload to JLCPCB/any fab), fab notes, copper plot
`2_assembly/` JLC BOM + CPL (SMD parts JLC assembles), full BOM with LCSC numbers for every part, pick-and-place, assembly drawing
`3_design/` KiCad 7 project (pcb, schematic, libs), netlist, STEP model, schematic PDF, renders
`4_enclosure/` printable base and lid STL
`5_verification/` DRC, ERC, verification and readiness reports

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.

## Manufacturing readiness (automatic check)

| Check | Result |
|---|---|
| gerber layers and drill present | PASS |
| drc errors 0 | PASS |
| unconnected 0 | PASS |
| netlist matches schematic | PASS |
| erc errors 0 | PASS |
| independent gerber check clean | PASS |
| every part has lcsc number | PASS |
| every lcsc number verified | PASS |
| cpl rows equal jlc bom parts | PASS |
| step model | PASS |
| KiCad DRC warnings | 0 |
| **Order ready** | **YES** |

Order steps: (1) upload `1_fabrication/*_gerbers.zip`; (2) for assembly upload `2_assembly/*_JLC_BOM.csv` and `*_JLC_CPL.csv`, check the 3D/rotation preview for every polarised part (diodes, ICs, LEDs, electrolytics) because CPL rotations are generated, not hand-checked; (3) buy the through-hole parts listed in `*_BOM_full.csv` marked hand/THT and solder them; (4) re-check stock and the exact LCSC listing for every line before paying.

Limits: the layout is software-generated and has not been reviewed by a PCB engineer; no prototype has been built; the first batch should be treated as a prototype run (order 5 boards).
