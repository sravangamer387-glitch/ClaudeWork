# Bijli Log (power-cut logger) - main board (rev B)

Power-cut logger: USB-C 5 V, 3.3 V LDO, 2 x AAA backup (Schottky OR), OLED, RTC module, mains-present sense.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 68 x 52 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 78 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 31 parts, 19 nets.

## Circuit description
- VBUS -> PTC -> +5V -> AP2112K-3.3 -> +3V3 -> Schottky -> VSYS; battery -> Schottky -> VSYS. Drop about 0.3 V; at 4 MHz the MCU runs down to 1.8 V.
- MAINS = VBUS divided by 100 k/100 k: high while the adapter is powered, low in a cut; the firmware stamps the start (RTC) and measures the duration (pc_* engine).

## Power
Run about 3 mA incl. OLED off most of the time; on battery only during cuts.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 4 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [68.1, 52.1] mm, match |

DRC breakdown: silk_over_copper:warning x4

Enclosure (prototype shell for 3D printing): outer 73.2 x 57.2 x 19.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| F1 | PTC 500mA | Fuse_1206_3216Metric |  |  |  |
| D3 | SMAJ5.0A | D_SMA |  |  |  |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | memory |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | memory |
| C5 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 |  |  |  |
| C6 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C7 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| D5 | BAT54WS | D_SOD-323 |  |  |  |
| D6 | BAT54WS | D_SOD-323 |  |  |  |
| J6 | BATT 2xAAA backup | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| C8 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| R12 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R13 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J4 | OLED 0.91in I2C | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| J5 | RTC DS3231 module | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| R10 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | memory |
| R11 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | memory |
| SW2 | Scroll / clear | SW_SPST_B3U-1000P |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Plug USB: +3V3 = 3.3 V, VSYS about 3.0 V, MAINS (TP3) about 2.5 V.
2. Unplug: MAINS goes low, unit stays alive on the battery, cut logged; replug: duration shown.

## Files
`bijli_log.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `bijli_log_JLC_BOM.csv`, `bijli_log_JLC_CPL.csv`, `bijli_log_BOM_full.csv`, `bijli_log.step`, `bijli_log_schematic.pdf`, `bijli_log_assembly_top.pdf`, `bijli_log_copper.pdf`, `bijli_log_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
