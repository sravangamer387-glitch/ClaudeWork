# Gas Taraju (LPG cylinder scale) - main board (rev B)

LPG cylinder scale: HX711 24-bit ADC, four load cells combined into one bridge, TM1637 display, three level LEDs, buzzer, 3 x AA. Weight only: **not a leak detector**.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 76 x 52 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 414 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 35 parts, 28 nets.

## Circuit description
- HX711 channel A, gain 128, 10 SPS, on 4.5 V with AVDD through 100 ohm + 100 nF, excitation through another 100 ohm + 100 nF; DOUT/SCK on PD2/PD3.
- Cylinder tare entered by the user; remaining % = (weight - tare) / 14.2 kg; consumption learned per day (gs_* engine, tested).

## Power
HX711 1.5 mA + MCU: wake once per minute and on tare; years on 3 x AA with sleeping firmware.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 6 errors, 9 warnings; unconnected pads: 6 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [76.1, 52.1] mm, match |

DRC breakdown: silk_over_copper:warning x7, silk_overlap:warning x2, unconnected_items:error x6

Enclosure (prototype shell for 3D printing): outer 81.2 x 57.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| SW1 | Power | SW_SPDT_PCM12 |  |  |  |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 |  |  |  |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| U4 | HX711 | SOIC-16_3.9x9.9mm_P1.27mm |  |  |  |
| R14 | 100 | R_0603_1608Metric |  |  |  |
| C10 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C11 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C12 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C13 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| R15 | 100 | R_0603_1608Metric |  |  |  |
| C14 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C15 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| J3 | Load cell bridge E+ E- A+ A- | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| J4 | TM1637 4-digit | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| SW2 | Tare / zero | SW_SPST_B3U-1000P |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D5 | Amber | LED_0603_1608Metric |  |  |  |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D6 | Red | LED_0603_1608Metric |  |  |  |
| R9 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Bridge disconnected: DOUT idles high; with a 20 kg reference weight reading is stable within 0.1 kg after calibration.
2. Zero with the plate empty (tare button).

## Files
`gas_taraju.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `gas_taraju_JLC_BOM.csv`, `gas_taraju_JLC_CPL.csv`, `gas_taraju_BOM_full.csv`, `gas_taraju.step`, `gas_taraju_schematic.pdf`, `gas_taraju_assembly_top.pdf`, `gas_taraju_copper.pdf`, `gas_taraju_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
