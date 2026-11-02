# Gas-Suraksha prototype and data-logging board (NOT a certified gas detector) (rev A)

Gas-Suraksha PROTOTYPE and data-logging board (84 x 60 mm), NOT a certified gas detector: ATmega328P at 16 MHz, socket for an MQ-6 module, USB-C 5 V and 3xAA backup OR-ed through Schottky diodes, active buzzer, three status LEDs, silence and test buttons, UART log header.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 84 x 60 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 164 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 45 parts, 33 nets.

## Circuit description
- **Power:** USB-C 5 V (PTC, TVS, CC 5.1 k) and 3 x AA through a reverse-polarity PMOS are OR-ed by two SS14 diodes into VSYS (about 4.1-4.7 V); the MQ-6 heater runs from VSYS, so calibrate per supply.
- **Sensor:** MQ-6 module on J3 (VCC, GND, DO, AO: check your module), AO through 1 k / 100 nF into A0; battery divider 220 k / 220 k on A1.
- **Alarm:** active 3 V buzzer through 47 ohm and an MMBT3904 on D8; LEDs on D9 (green), D10 (amber), D11 (red, shares MOSI); buttons on D2 (silence) and D3 (test).
- **Firmware:** `products/06-gas-suraksha/firmware` (alarm engine, 34 host checks); flash `release/gas_suraksha_demo.hex` through the ISP header with external-crystal fuses; logs at 115200 baud on J4.

## Power
About 150 mA for the MQ-6 heater plus about 10 mA logic: run from USB; 3 x AA last only hours.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [84.1, 60.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 99.2 x 75.2 x 39.8 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| F1 | PTC 500mA | Fuse_1206_3216Metric | Littelfuse 1206L050YR (6 V) | C163512 | verified |
| D3 | SMAJ5.0A | D_SMA | Littelfuse SMAJ5.0A | C83329 | verified |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| C5 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| J5 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | verified |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| BZ1 | Buzzer active 3V | Buzzer_12x9.5RM7.6 | S&S SUN-1275Y-0327-50P7.6 | C3015483 | verified |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | verified |
| R20 | 47 | R_0603_1608Metric | UNI-ROYAL 0603WAF470JT5E | C23182 | verified |
| D6 | SS14 | D_SMA | SS14 | C84343 | verified |
| D7 | SS14 | D_SMA | SS14 | C84343 | verified |
| C20 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| Y1 | 16 MHz | Crystal_SMD_3225-4Pin_3.2x2.5mm | YXC X322516MOB4SI 16 MHz 12 pF 3225 (LCSC listing seen in search results; matches the 22 pF load caps) | C12668 | verified |
| C9 | 22p | C_0603_1608Metric | Samsung CL10C220JB8NNNC C0G | C1653 | verified |
| C10 | 22p | C_0603_1608Metric | Samsung CL10C220JB8NNNC C0G | C1653 | verified |
| J3 | MQ-6 module: VCC GND DO AO | PinHeader_1x04_P2.54mm_Vertical | ZHOURI 2.54-1*4 | C5116483 | verified |
| R10 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C11 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R11 | 220k | R_0603_1608Metric | UNI-ROYAL 0603WAF2203T5E | C22961 | verified |
| R12 | 220k | R_0603_1608Metric | UNI-ROYAL 0603WAF2203T5E | C22961 | verified |
| C12 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| J4 | UART log (adapter RX, TX) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| SW2 | Silence | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW3 | Test | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| D1 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D4 | Amber | LED_0603_1608Metric | Hubei KENTO KT-0603Y yellow (Everlight 19-213 was out of stock) | C2287 | verified |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D5 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| R9 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Without the sensor: VSYS 4.6 V on USB, 4.2 V on fresh AA; no back-feed from USB into the cells.
2. Flash, press TEST: buzzer and red LED; SILENCE quiets it.
3. Fit the MQ-6 module, let it warm 24-48 h, log clean-air counts on the UART for a day before setting thresholds.
4. Never test with gas indoors; never rely on it as a safety device.

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
