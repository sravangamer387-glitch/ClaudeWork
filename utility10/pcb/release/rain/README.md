# Rain Alert Bell - indoor unit (rev B)

Rain Alert Bell indoor unit: 3 x AA, ATmega328P-AU, loud buzzer, mute button, pulsed rain-plate interface with TVS protection.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 60 x 42 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 61 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 27 parts, 19 nets.

## Circuit description
- **Power:** 3 x AA (4.5 V fresh) -> slide switch -> AO3401A reverse-polarity PMOS -> +4V5. ATmega328P at 4.5 V, 8 MHz internal RC.
- **Rain plate interface:** DRV (PD5) is driven high for about 2-5 ms per reading through R1 1 k; the plate resistance (wet 1 k - 150 k) forms a divider with R2 100 k to GND at SENSE (ADC0); R3 1 k + C5 2.2 nF filter; D3/D4 bidirectional 5 V TVS diodes on both cable lines. Because the plate is powered only during measurement there is no DC across the wet gold plate: far less electrolytic corrosion.
- **Sleep:** firmware sleeps in power-down with a 1 s watchdog wake; average current is tens of microamperes plus about 5 mA x 5 ms per second.

### Simulation: `sim/rain_sense_results.md`
```
| plate resistance | V(SENSE) at 2 ms | at 5 ms (final) | ADC counts at 4.5 V ref | reads as |
|---|---|---|---|---|
| 1 kΩ (heavy rain, shorted) | 4.369 V | 4.369 V | 994 | WET (>=400) |
| 10 kΩ (wet) | 4.018 V | 4.018 V | 914 | WET (>=400) |
| 50 kΩ (wet) | 2.961 V | 2.961 V | 674 | WET (>=400) |
| 150 kΩ (damp) | 1.786 V | 1.786 V | 406 | WET (>=400) |
| 500 kΩ (dew/humid) | 0.747 V | 0.748 V | 170 | dry (<250) |
| 2 MΩ (dry-ish) | 0.214 V | 0.214 V | 49 | dry (<250) |
| open (dry) | 0.000 V | 0.000 V | 0 | dry (<250) |

Pulse 4.5 V for 5 ms through 1 kΩ; time constant (plate+2k)||100k x 2.2 nF is at most 0.22 ms, so the reading has settled long before 2 ms. Firmware must wait >= 2 ms (demo waits 2 ms).
```

## Power
Awake 5 ms per second at about 5 mA (average 25 uA) + power-down 6 uA + regulator-free supply: about 30 uA average -> 2500 mAh AA cells would last years; battery self-discharge dominates (alarm current about 30 mA for the buzzer while ringing).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [60.1, 42.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 65.2 x 47.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| SW1 | Power | SW_SPDT_PCM12 |  |  |  |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J3 | Rain plate | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| BZ1 | Buzzer 85dB | Buzzer_12x9.5RM7.6 |  |  |  |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| SW2 | Mute | SW_SPST_B3U-1000P |  |  |  |
| D1 | Red | LED_0603_1608Metric |  |  |  |
| D3 | TVS 5V bidir | D_SOD-323 |  |  |  |
| D4 | TVS 5V bidir | D_SOD-323 |  |  |  |
| R1 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R2 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | memory |
| R3 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | memory |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C5 | 2.2n | C_0603_1608Metric |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash `../../../firmware/release/*.hex` built for 8 MHz (`make hex` with F_CPU=8000000).

## Bring-up and test
1. Insert 3 x AA, switch ON: TP1 = 4.2-4.6 V.
2. Connect the plate: SENSE (TP3) between readings = 0 V; during a reading about 0.2 V with a dry plate.
3. Wet the plate with a drop of water: SENSE rises to > 1.7 V during the 5 ms pulse; after 3 s of continuous wet readings the buzzer sounds.
4. Flash over ISP with fuses lfuse 0xE2, hfuse 0xD9, efuse 0xFD (8 MHz internal, BOD 2.7 V: the unit resets cleanly when the batteries fall below 2.7 V, which is the 8 MHz limit).

## Files
`rain_alert_main.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `rain_alert_main_JLC_BOM.csv`, `rain_alert_main_JLC_CPL.csv`, `rain_alert_main_BOM_full.csv`, `rain_alert_main.step`, `rain_alert_main_schematic.pdf`, `rain_alert_main_assembly_top.pdf`, `rain_alert_main_copper.pdf`, `rain_alert_main_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
