# MITTI-NETRA soil and structure telemetry node (ESP32-S3 + LTE-M modem socket) (rev A)

MITTI-NETRA soil and structure telemetry node (90 x 80 mm): ESP32-S3, TP4056 solar/USB charger for one Li-ion cell, 3.3 V LDO, switched socket for a SIM7080G breakout, ADXL345, HX711 strain input, soil-probe and DS18B20 inputs.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 90 x 80 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 3 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 206 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 64 parts, 42 nets.

## Circuit description
- **Charging:** solar (JST-PH 2) and USB VBUS OR-ed by SS14 diodes into a TP4056 with PROG = 2.2 k (about 0.58 A); a protected 1S Li-ion cell on JST-PH 2 (no protection IC on the board).
- **Rails:** AP2112K 3.3 V from the cell (stops regulating near 3.55 V); modem VBAT through an AO3401A high-side switch driven by an AO3400A, with 100 uF + 22 uF burst capacitors.
- **Sensors:** ADXL345 on I2C (address 0x53, INT1 wakes the MCU); HX711 (as on Gas Taraju) for a strain bridge; capacitive soil probe through 1 k + 100 nF to an ADC pin; DS18B20 on 1-Wire.

## Power
Target under 100 uA in deep sleep with the modem off (not measured); modem bursts up to about 0.5 A while transmitting.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [90.1, 80.1] mm, match |

Enclosure: printed mounting plate 106 x 96 mm for an IP65 box of at least 110 x 100 x 38 mm inside. field node: mount on this plate inside an IP65 ABS junction box with cable glands and a vent membrane; place the 18650 holder and the modem breakout in the same box; keep the NTC TH1 side of the board next to the cell; shade the box from direct sun

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | verified |
| C37 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| J1 | USB-C (charge + program) | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| J2 | Solar panel 5-6 V | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| D1 | SS14 | D_SMA | SS14 | C84343 | verified |
| D2 | SS14 | D_SMA | SS14 | C84343 | verified |
| C1 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| U4 | TP4056 | HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm | TPOWER TP4056 | C382139 | verified |
| R1 | 2.2k | R_0603_1608Metric | 0603 2.2k 1% | C4190 | verified |
| R16 | 6.2k | R_0603_1608Metric | UNI-ROYAL 0603WAF6201T5E | C4260 | verified |
| TH1 | NTC 10k B3950 | R_0805_2012Metric | FH CMFB103F3950FANT | C51597 | verified |
| C2 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| D3 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| R2 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D4 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R3 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J3 | Li-ion cell (protected!) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | verified |
| C3 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R4 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | verified |
| R5 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | verified |
| C5 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| Q1 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| R6 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| Q2 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R7 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R8 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| C6 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VZH101M1VTR-0607 | C176683 | verified |
| C7 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| J6 | Cellular modem (SIM7080G breakout) | PinHeader_2x03_P2.54mm_Vertical | HCTL PZ254-2-03-Z-8.5 | C2894964 | verified |
| U5 | ADXL345 | LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y | ADXL345BCCZ-RL7 | C9667 | verified |
| C8 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C9 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R9 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R10 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| U2 | HX711 | SOIC-16_3.9x9.9mm_P1.27mm | HX711 | C43656 | verified |
| R11 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| C10 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C11 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C12 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C13 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R12 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| C14 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C15 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| J4 | Strain-gauge bridge E+ E- A+ A- | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| J5 | Soil probe (capacitive, 3.3 V) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| J7 | DS18B20 temp | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S | C131339 | verified |
| R13 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R15 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C16 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D5 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R14 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J8 | UART flash/debug (USB-serial adapter) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Fit a protected cell and check TP2 = 3.3 V.
2. Charge LEDs with solar or USB.
3. Check ADXL345 ID 0xE5, soil probe reading, DS18B20.
4. Modem socket: MODEM_EN switches VBAT_M.

## Files
`1_fabrication/` Gerber + drill zip (upload to JLCPCB/any fab), fab notes, copper plot
`2_assembly/` JLC BOM + CPL (SMD parts JLC assembles), full BOM with LCSC numbers for every part, pick-and-place, assembly drawing
`3_design/` KiCad 7 project (pcb, schematic, libs), netlist, STEP model, schematic PDF, renders
`4_enclosure/` printable enclosure (base, screwed lid, battery door, plungers / light pipes / switch extensions) or a mounting plate for a bought IP65 box; dimensions and notes in enclosure.json
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
