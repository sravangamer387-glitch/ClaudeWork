# Bijli Meter Reader - main board (rev B)

Optical electricity-meter pulse reader: USB-C 5 V powered ATmega328P-AU, sensor-head connector (phototransistor), TM1637 4-digit display connector, reset button, LED.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 52 x 38 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 39 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 23 parts, 17 nets.

## Circuit description
- **Power:** USB-C power-only sink: CC1/CC2 each 5.1 k to GND (R1, R2) so a charger delivers 5 V; 0.5 A PTC fuse F1 (1206) then +5V; SMAJ5.0A TVS D3 on VBUS clamps spikes; 10 uF + 100 nF decoupling.
- **Sensor head:** phototransistor between SIG_H and GND, 10 k pull-up R4 to +5V, 100 ohm series R6 + 100 nF C5 on SIG; SIG falls when the meter LED lights. Firmware adapts its threshold to the observed minimum/maximum (swing must be >= 0.2 V).
- **MCU/display:** ATmega328P-AU at the internal 8 MHz RC, ADC0 reads SIG, TM1637 display module on JST-PH J4 (GND, +5V, DIO, CLK), reset-bill button on PD2, LED on PD7, ISP header.

### Simulation: `sim/bijli_head_results.md`
```
| condition (phototransistor collector current) | SIG voltage | ADC counts (5 V ref) | note |
|---|---|---|---|
| dark / meter LED off, dim room (1 uA) | 4.99 V | 1021 |  |
| indoor ambient light on the head (20 uA) | 4.80 V | 982 |  |
| bright window light (150 uA) | 3.49 V | 713 |  |
| meter LED lit, weak coupling (200 uA) | 2.98 V | 610 |  |
| meter LED lit, typical close clip (1 mA) | 0.20 V | 41 | saturated (collector near 0.2 V) |
| meter LED lit, strong (3 mA) | 0.20 V | 41 | saturated (collector near 0.2 V) |

SIG = 5 V - Ic x (10 k pull-up + 100 ohm), clamped at 0.2 V (saturation). The firmware looks for a swing of more than 40 counts (0.2 V) between its running minimum and maximum, so a lit LED (>= 0.2 mA) against indoor ambient (<= 20 uA) gives a swing of more than 1.5 V. Direct sunlight on the head (> 1 mA) would hide the pulses: use the black clip. Edge speed: 10 k x 100 nF = 1 ms time constant, meter LED pulses are tens of ms.
These phototransistor currents are typical-datasheet assumptions, not measurements of a real meter.
```

## Power
MCU 5 V 8 MHz about 6 mA + display 10-30 mA + LED: under 50 mA, far below the 500 mA default USB limit and the 0.5 A PTC.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 1 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [52.1, 38.1] mm, match |

DRC breakdown: silk_over_copper:warning x1

Enclosure (prototype shell for 3D printing): outer 57.2 x 43.2 x 19.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| F1 | PTC 500mA | Fuse_1206_3216Metric |  |  |  |
| D3 | SMAJ5.0A | D_SMA |  |  |  |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J3 | Sensor head | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical |  |  |  |
| J4 | TM1637 display | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical |  |  |  |
| SW1 | Reset bill | SW_SPST_B3U-1000P |  |  |  |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | memory |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | memory |
| R3 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | memory |
| R4 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | memory |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R6 | 100 | R_0603_1608Metric |  |  |  |
| C1 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C4 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C5 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash `../../../firmware/release/*.hex` built for 8 MHz (`make hex` with F_CPU=8000000).

## Bring-up and test
1. Plug a 5 V charger: VBUS (TP at J1/F1) = 5.0 V; +5V (TP1) = 4.9-5.0 V.
2. SIG with head disconnected = 5 V (pull-up); with the phototransistor in the dark about 4.9 V; under a lit meter LED a drop of at least 0.5 V.
3. Flash over ISP: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m` (internal 8 MHz, brown-out 2.7 V; USB supply is 5 V).
4. Hold the head over a 1 Hz test LED: display counts one pulse per second.

## Files
`bijli_meter_reader.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `bijli_meter_reader_JLC_BOM.csv`, `bijli_meter_reader_JLC_CPL.csv`, `bijli_meter_reader_BOM_full.csv`, `bijli_meter_reader.step`, `bijli_meter_reader_schematic.pdf`, `bijli_meter_reader_assembly_top.pdf`, `bijli_meter_reader_copper.pdf`, `bijli_meter_reader_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
