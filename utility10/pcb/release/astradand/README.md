# ASTRADAND gesture wand - main board (rev A)

ASTRADAND gesture wand main board (146 x 26 mm): ATmega328P at 8 MHz and 3.3 V, MPU-6050 6-axis IMU on I2C, six WS2812B-Mini pixels, differential piezo, haptic motor driver, trigger switch, 3xAAA power with reverse-polarity PMOS.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 146 x 26 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 2 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 182 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 49 parts, 33 nets.

## Circuit description
- **Motion:** MPU-6050 on I2C (4.7k pull-ups, SDA/SCL taken under the board on the bottom layer), wake-on-motion interrupt to the MCU; AD0/FSYNC/CLKIN tied to GND.
- **Light:** six WS2812B-Mini pixels in a chain, each with 100 nF; data from D10 through 330 ohm; the LED supply is switched high-side (AO3401A driven by MMBT3904) through an SS14 so the pixels draw nothing in sleep and their 5 V-class data is met at 3.3 V logic by running the strip from the battery rail.
- **Sound/haptic:** piezo driven antiphase from Timer1 (OC1A/OC1B); vibration motor through an NPN with flyback diode.
- **Power:** 3xAAA, slide switch, AO3401A reverse-polarity PMOS, AP2112K 3.3 V LDO, battery divider to ADC for the low-battery warning.

## Power
Sleep with IMU wake-on-motion: target tens of microamps (not measured). Active casting with LEDs lit is dominated by the six pixels (tens of mA).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [146.1, 26.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 151.2 x 31.2 x 19.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | verified |
| J1 | BATT 3xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | verified |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| D11 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C20 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D12 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C21 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D13 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C22 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D14 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C23 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D15 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C24 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D16 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-MINI-V3/W SMD3535-4P (same footprint and pin order as the WS2812B-Mini C114583, which was out of stock) | C527089 | verified |
| C25 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| U2 | MPU-6050 | InvenSense_QFN-24_4x4mm_P0.5mm | MPU-6050 | C24112 | verified |
| C10 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C11 | 2.2n | C_0603_1608Metric | Samsung CL10B222KB8NNNC X7R | C16033 | verified |
| C12 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C13 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R20 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R21 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | verified |
| C5 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C6 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| D20 | SS14 | D_SMA | Starsea SS14 SMA | C84343 | verified |
| Q3 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| Q4 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| R33 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R34 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C7 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R30 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | verified |
| R31 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | verified |
| R32 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| BZ1 | PKLCS1212E4001 | Buzzer_Murata_PKLCS1212E | PKLCS1212E4001-R1 | C113159 | verified |
| SW2 | Cast trigger | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J4 | Haptic motor | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Battery in, switch on: +4V5 = 4.5 V at TP1, 3.3 V on U3 output.
2. Flash `astradand/firmware` over the ISP header (8 MHz internal, fuses in the manual).
3. Self test: pixels sweep, piezo chirps, shake wakes the IMU, trigger + gesture casts a spell.

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
