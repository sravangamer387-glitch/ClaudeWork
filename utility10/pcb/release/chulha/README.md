# Chulha Timers - main board (rev B)

Four independent kitchen timers: four channel buttons, TM1637 6-digit display module, loud buzzer, 3 x AAA.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 72 x 48 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 86 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 22 parts, 18 nets.

## Circuit description
- Channel buttons CH1-CH4 on PD2-PD5 (internal pull-ups); TM1637 on PC4/PC5 (DIO/CLK) through the J4 module header; buzzer driver as on the other boards.
- Tap adds one minute, hold 1 s clears; each channel rings separately (firmware engine ct_*, tested).

## Power
Display on: about 10 mA + MCU 3 mA; sleep between button presses and blank the display after 20 s idle -> months on 3 x AAA.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 2 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [72.1, 48.1] mm, match |

DRC breakdown: silk_overlap:warning x2

Enclosure (prototype shell for 3D printing): outer 77.2 x 53.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J1 | BATT 3xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| SW1 | Power | SW_SPDT_PCM12 |  |  |  |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 |  |  |  |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| SW2 | CH1 | SW_SPST_B3U-1000P |  |  |  |
| SW3 | CH2 | SW_SPST_B3U-1000P |  |  |  |
| SW4 | CH3 | SW_SPST_B3U-1000P |  |  |  |
| SW5 | CH4 | SW_SPST_B3U-1000P |  |  |  |
| J4 | TM1637 display | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Power on: display shows 0; tap CH1: +1 min counts down.
2. Ring: each channel's buzzer pattern stops with its own button.

## Files
`chulha_timers.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `chulha_timers_JLC_BOM.csv`, `chulha_timers_JLC_CPL.csv`, `chulha_timers_BOM_full.csv`, `chulha_timers.step`, `chulha_timers_schematic.pdf`, `chulha_timers_assembly_top.pdf`, `chulha_timers_copper.pdf`, `chulha_timers_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
