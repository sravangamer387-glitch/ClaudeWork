# Kheti-Mitra irrigation controller - main board (rev B)

Kheti-Mitra irrigation controller: 12 V DC input, 5 V regulator, solenoid-valve driver, two capacitive soil sensors, rain sensor.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 86 x 60 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 132 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 37 parts, 22 nets.

## Circuit description
- 12 V jack -> 1 A PTC -> SMBJ15A TVS -> reverse-polarity PMOS -> +12V; AMS1117-5.0 -> +5V (about 0.3 W at 40 mA).
- Valve: AO3400A low-side switch with 100 ohm gate resistor, 100 k pull-down and SS14 flyback diode; soil sensors on ADC0/ADC1 through 1 k + 100 nF; rain digital input with pull-up.

## Power
Idle about 15 mA at 5 V from 12 V (0.2 W); valve 12 V x 0.3 A during watering.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 7 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [86.1, 60.1] mm, match |

DRC breakdown: silk_over_copper:warning x7

Enclosure (prototype shell for 3D printing): outer 91.2 x 65.2 x 19.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J1 | 12 V DC in | BarrelJack_CUI_PJ-063AH_Horizontal |  |  |  |
| F1 | PTC 1A 16V | Fuse_1812_4532Metric |  |  |  |
| D3 | SMBJ15A | D_SMB |  |  |  |
| Q3 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| R17 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| U3 | AMS1117-5.0 | SOT-223-3_TabPin2 |  |  |  |
| C6 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C7 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C8 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| Q4 | AO3400A | SOT-23 |  |  |  |
| R16 | 100 | R_0603_1608Metric |  |  |  |
| R18 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| D7 | SS14 | D_SMA |  |  |  |
| J5 | Valve 12V | TerminalBlock_bornier-2_P5.08mm |  |  |  |
| J6 | Soil sensor 1 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical |  |  |  |
| J7 | Soil sensor 2 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical |  |  |  |
| J8 | Rain sensor | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical |  |  |  |
| R20 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C9 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R21 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C10 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R22 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R23 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C11 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| SW2 | Hold | SW_SPST_B3U-1000P |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Jack: +12V = 11.9 V, +5V = 5.0 V.
2. Force VALVE_G high from the ISP: the valve switches and the Schottky catches the flyback.
3. Soil sensors: dry about 520 counts / wet about 260 counts (to be calibrated).

## Files
`kheti_mitra.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `kheti_mitra_JLC_BOM.csv`, `kheti_mitra_JLC_CPL.csv`, `kheti_mitra_BOM_full.csv`, `kheti_mitra.step`, `kheti_mitra_schematic.pdf`, `kheti_mitra_assembly_top.pdf`, `kheti_mitra_copper.pdf`, `kheti_mitra_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
