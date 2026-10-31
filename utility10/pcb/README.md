# PCB designs for the Tier A electronic tools (rev A)

Boards: **Seeti Counter** (60×40 mm), **Bijli Meter Reader** (48×34 mm), **Rain Alert Bell** indoor unit (56×38 mm) and its **rain plate** (36×58 mm). The two laser-cut Tier A tools (Masala Rack, Laptop Stand) have no PCB.

**Status: first-draft layouts generated and checked by software; NOT reviewed by an electronics engineer, NOT prototyped, NOT manufacturer-DFM-checked.** Treat them as a head start for the engineer you hire, not as ready-to-order boards. Order 5 prototype boards first.

## What is here
| Folder | Contents |
|---|---|
| `release/<board>/` | `.kicad_pcb`, `.kicad_sch` (KiCad 7), Gerbers + drill (zip), BOM CSV (with suggested parts to verify), pick-and-place CSV, schematic PDF, board PNG, netlist |
| `boards/*.py` | the design source: parts, footprints, positions, nets (edit these, then re-run) |
| `build.py`, `route.py`, `schematic.py`, `package.py` | toolchain: netlist → KiCad schematic, placement, own two-layer grid router, ground pour, DRC, Gerber/drill/CPL export, netlist cross-check |

Rebuild: `python3 package.py` (system Python with KiCad 7 `pcbnew`, `kicad-cli`; PNGs need cairosvg).

## Verification results (software only)
| Board | Parts / nets | DRC errors | Unconnected | Schematic netlist = PCB netlist | DRC warnings |
|---|---|---|---|---|---|
| Seeti Counter | 27 / 20 | 0 | 0 | yes | 29 (footprint-library link, 1 silkscreen overlap) |
| Bijli Meter Reader | 16 / 14 | 0 | 0 | yes | 17 (footprint-library link, silkscreen near edge) |
| Rain Alert indoor | 20 / 17 | 0 | 0 | yes | 30 (library link, silkscreen, 1 stub) |
| Rain plate | 1 / 2 | 0 | 0 | yes | 47 (45 = open comb-finger ends, intentional) |

DRC = KiCad 7 `WriteDRCReport` with default 0.2 mm clearance, 0.25 mm tracks, 0.6/0.3 mm vias. **No schematic ERC was run** (KiCad 7's command line has no ERC); instead the exported schematic netlist is compared pin-by-pin with the PCB netlist (identical for all four boards). The schematic is **netlist-style** (every pin has a labelled stub), not a hand-drawn functional schematic: readable by tools, tedious for humans; have the engineer redraw it.

Problems found while building: the first router version put via coordinates in grid units (23 false "unconnected" errors); unused-pin clearance was not modelled (22 clearance errors); round pads were reached at their bounding-box corners (dangling copper); the USB-C connector could not be fanned out (0.3 mm gaps between pads, no room for vias), so Bijli uses a **Micro-USB B** receptacle instead; two ground vias 0.3 mm apart violated hole spacing.

## Circuit notes
**Seeti Counter** (2×AAA = 3.0 V, ATmega328P at its internal 8 MHz RC, no crystal): electret mic biased by 2.2 kΩ → 1 µF AC coupling → MCP6001 non-inverting amplifier biased at VCC/2 (2×100 kΩ), gain 1+100k/1k = **101** (AC, 16 Hz high-pass from 1 kΩ·10 µF), op-amp bandwidth about 1 MHz/101 ≈ **9.9 kHz**, enough for a 2.8 kHz whistle. Output rests at 1.5 V (ADC ≈ 512 at 3 V reference, matching the firmware's `-512` offset). Buzzer 3 V through an NPN with a flyback diode; ISP header; target button on PD2; LED on PD7. **Firmware:** the demo build uses 16 MHz timing; for this board compile with `F_CPU=8000000` and set the fuses for the internal 8 MHz oscillator; at 3 V the ADC reference is the supply (it falls as the batteries age: consider the internal 1.1 V reference).
**Bijli Meter Reader** (5 V from a Micro-USB adapter or power bank, 0.5 A PTC fuse): head connector J3 (+5 V, SIG, GND) with a **phototransistor between SIG and GND and a 10 kΩ pull-up on the board**; SIG goes low when the meter LED lights (the demo firmware is written for this polarity); 100 nF filters spikes; TM1637 4-digit display module on J4; reset-bill button; ISP header. The head (phototransistor in a black clip) is not a separate board here.
**Rain Alert Bell** (3×AA = 4.5 V): the plate is **pulsed** (DRV pin driven about 2 ms per reading, SENSE pulled down by 100 kΩ with 10 nF filtering) so DC does not sit on the plate and corrode it; the demo firmware does this on D5. Loud 4.5 V buzzer through an NPN, mute button, LED, ISP. **Plate:** two interleaved 0.4 mm comb traces on a 36×58 mm board (0.4 mm gaps, 44 fingers), order **ENIG** (gold) finish; unvarnished copper corrodes within weeks outdoors; add a conformal coat on the spines and cable pads only, never over the fingers.

## Known limits and things a reviewer must check
1. **Placement is automatic and rough**; long ISP routes, no thermal/EMC optimisation. The MCP6001 input node is routed on the same layer as digital lines: review analog routing and add a guard ring if noisy.
2. **Ground pour** on the bottom layer with vias to it; the SMD ground pads connect through single vias.
3. **USB connector (Bijli):** footprint mechanics versus the enclosure edge are unverified; a Micro-USB B receptacle is chosen for routability, USB-C needs an engineer's fan-out (via-in-pad or 4 layers).
4. **Battery boards have no reverse-polarity protection and no low-battery detection** (the firmware has a low-battery input unused here). Add a P-MOSFET or Schottky if users will swap cells.
5. **Parts:** "suggested part" column in each BOM is from memory/typical choices: verify stock, price and footprints with the assembler. No cost quote was obtained.
6. No ESD protection, no EMC testing, no regulatory work; the Bijli adapter must be a BIS-registered one bought in.
7. Fab limits assumed: 0.2 mm clearance/track, 0.3 mm drill vias (standard 2-layer service). Confirm with the PCB vendor.
8. Mounting holes are not included: add them to match the enclosure STL (`../0X-*/enclosure_*.stl` are prototype shells with different dimensions: re-fit after layout is frozen).

## Next steps for the owner
Hire an electronics engineer for a 1–2 day review per board (check list above), then order 5 boards each from a PCB house + stencil, assemble by hand or via an EMS, flash `../firmware/release/*.hex` (adjust F_CPU for Seeti), run the end-of-line tests in each tool README.
