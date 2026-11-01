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
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | verified |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | verified |
| J3 | Rain plate | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| BZ1 | Buzzer 85dB | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | verified |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| SW2 | Mute | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| D1 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | verified |
| D3 | TVS 5V bidir | D_SOD-323 | Nexperia PESD5V0S1BA,115 | C19224 | verified |
| D4 | TVS 5V bidir | D_SOD-323 | Nexperia PESD5V0S1BA,115 | C19224 | verified |
| R1 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R2 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R3 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| C5 | 2.2n | C_0603_1608Metric | Samsung CL10B222KB8NNNC X7R | C16033 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Insert 3 x AA, switch ON: TP1 = 4.2-4.6 V.
2. Connect the plate: SENSE (TP3) between readings = 0 V; during a reading about 0.2 V with a dry plate.
3. Wet the plate with a drop of water: SENSE rises to > 1.7 V during the 5 ms pulse; after 3 s of continuous wet readings the buzzer sounds.
4. Flash over ISP with fuses lfuse 0xE2, hfuse 0xD9, efuse 0xFD (8 MHz internal, BOD 2.7 V: the unit resets cleanly when the batteries fall below 2.7 V, which is the 8 MHz limit).

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
