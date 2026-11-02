# KINETIC vibration puck (ADXL345, SPI) (rev A)

KINETIC vibration puck (25 x 26 mm): ADXL345 accelerometer on SPI with decoupling and a 6-pin header matching the controller.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 25 x 26 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.0 mm, 2 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 30 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 5 parts, 6 nets.

## Circuit description
- **Sensor:** ADXL345 (LGA-14) in 4-wire SPI mode 3; Vs and Vdd I/O both at 3.3 V; 100 nF at each supply pin and 10 uF bulk. INT pins unused.
- **Mounting:** two M2.5 holes; fix the puck rigidly to the motor end-cap (a flat face, short load path to the bearing); keep the cable under 30 cm.

## Power
About 0.1 mA at 3.2 kHz output data rate (datasheet figure; not measured).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [25.1, 26.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 30.2 x 31.2 x 18.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ADXL345 | LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y | ADXL345BCCZ-RL7 | C9667 | verified |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| J3 | SPI to controller | PinHeader_2x03_P2.54mm_Vertical | HCTL PZ254-2-03-Z-8.5 | C2894964 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Read the device ID register: it must return 0xE5.
2. Set 3200 Hz data rate and +-16 g full resolution; at rest Z reads about +1 g.
3. Tap the motor: spikes must appear on all axes.

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
