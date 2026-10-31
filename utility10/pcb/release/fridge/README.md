# Fridge Door Guard - main board (rev B)

Fridge door alarm: reed switch + magnet, quiet for 60 s, chirps then sounds continuously; counts openings.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 64 x 44 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 63 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 24 parts, 17 nets.

## Circuit description
- 2 x AAA -> slide switch -> reverse-polarity PMOS -> +3V0; ATmega328P sleeps (< 2 uA) and wakes on INT1 when the reed opens (series 1 k, 10 nF filter, bidirectional TVS on the cable).
- Buzzer driver and LED as on the other boards; silence button on PD2; ISP header.

## Power
Sleep about 2 uA (BOD off, WDT off); an alarm minute at 30 mA = 0.5 mAh; 20 door openings/day -> battery life limited by self-discharge (years).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 1 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [64.1, 44.1] mm, match |

DRC breakdown: silk_over_copper:warning x1

Enclosure (prototype shell for 3D printing): outer 69.2 x 49.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J1 | BATT 2xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| SW1 | Power | SW_SPDT_PCM12 |  |  |  |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 |  |  |  |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| SW2 | Silence | SW_SPST_B3U-1000P |  |  |  |
| J3 | Reed switch | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C9 | 10n | C_0603_1608Metric | 0603 10nF X7R | C57112 | verified |
| D4 | TVS 5V bidir | D_SOD-323 |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Magnet next to reed: REED (TP3) low; remove: high and INT1 wakes the unit.
2. After 60 s open: chirp every 10 s; after 180 s: continuous; closing silences.

## Files
`fridge_door_guard.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `fridge_door_guard_JLC_BOM.csv`, `fridge_door_guard_JLC_CPL.csv`, `fridge_door_guard_BOM_full.csv`, `fridge_door_guard.step`, `fridge_door_guard_schematic.pdf`, `fridge_door_guard_assembly_top.pdf`, `fridge_door_guard_copper.pdf`, `fridge_door_guard_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
