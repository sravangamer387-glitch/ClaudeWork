import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(os.path.join(HERE, "release", "summary.json")))
rows = "\n".join(f"| {s['board']} | {s['parts']} / {s['nets']} | {s['erc_errors']} | {s['drc_errors']} ({s['drc_warnings']} warnings) | {s['unconnected']} | {'yes' if s['netlist'] else 'NO'} | {s['failures']} |" for s in S)
txt = f"""# PCB designs for the Tier A electronic tools - rev B (engineering release)

Boards: **Seeti Counter** (64 x 44 mm), **Bijli Meter Reader** (52 x 38 mm, USB-C), **Rain Alert Bell** indoor unit (60 x 42 mm) and its **rain plate** (38 x 60 mm). The two laser-cut Tier A tools (Masala Rack, Laptop Stand) have no PCB.

**Status: software-verified engineering release. Nothing here has been built, reviewed by a second engineer, or sent to a fab. Before ordering, an electronics engineer must complete `REVIEW_CHECKLIST.md`.** Order 5 prototypes first.

## What rev B adds over the first draft
Reverse-battery protection (P-MOSFET), TVS surge protection on the USB-C VBUS line and on the rain-plate cable, PTC fuse, correct USB-C sink resistors (HRO Type-C receptacle, 5.1 k on CC1/CC2), test points, four M2.5 mounting holes and two fiducials per board, rounded corners, ground pours on both layers with stitching vias, power traces 0.4 mm, JLCPCB-format BOM/CPL with LCSC numbers (the ones I could verify are marked), a 3D STEP model, fabrication-notes PDF, assembly drawing PDF, a parametric enclosure shell generated from the finished board with a collision check, SPICE simulations of the analog stages, and a readable schematic with real wires where it was safe to draw them. Two **design errors were found by simulation and fixed**: the microphone amplifier's feedback return into a weakly bypassed bias node had destroyed the low-frequency gain (fixed with a 10 uF bypass), and its first gain/bandwidth claim (101x, 9 kHz) did not match the final component values (34x, 26 kHz, so an anti-alias filter was added).

## Verification summary (all software)
| Board | Parts / nets | Own ERC errors | KiCad DRC errors | Unconnected | Schematic netlist = PCB netlist | Router failures |
|---|---|---|---|---|---|---|
{rows}

How it was checked: (1) own ERC on the netlist (unconnected pins, single-pin nets, output conflicts, unpowered supply nets, symbol-to-footprint pin match; KiCad 7's command line has no ERC); (2) KiCad 7 DRC through its Python API (clearance, hole spacing, courtyards, mask bridges, silkscreen); (3) schematic export compared pin-group by pin-group with the PCB netlist (this caught an accidental short that my own auto-wiring had drawn between CC2 and VBUS); (4) independent Gerber parse with a second library (gerbonara): layers read, outline size equals the design; (5) SPICE (ngspice) for the Seeti amplifier and rain-plate sense; arithmetic model for the Bijli sensor head. The rain plate's mask-bridge errors are waived on purpose (one mask opening spans both gold electrodes).

## Folder map
| Path | Contents |
|---|---|
| `release/<board>/` | everything to review or order: KiCad 7 project, Gerber zip, JLC BOM/CPL, full BOM with LCSC status, STEP, schematic PDF, assembly and copper PDFs, fab-notes PDF, enclosure STLs, board images, board README (design notes, simulations, bring-up) |
| `boards/*.py` | design source: parts, positions, nets, schematic layout, enclosure cut-outs |
| `build.py` `route.py` `sch2.py` `erc.py` `placecheck.py` `retouch.py` | toolchain: schematic writer, 0.05 mm-grid two-layer router, placement check, silkscreen touch-up |
| `outputs.py` `package.py` `docgen.py` `fabdoc.py` `enclosure.py` `gerbercheck.py` | verification and manufacturing outputs |
| `sim/` | SPICE decks and results |
| `REVIEW_CHECKLIST.md` | engineer sign-off list |

Rebuild one board: `python3 build.py seeti` (3-8 minutes for the largest), then `python3 package.py seeti` (system Python with KiCad 7 `pcbnew`; the PNG/PDF/STL steps use a venv with cairosvg, matplotlib, trimesh, gerbonara).

## Honest limits
1. **Routing and placement are software-generated** (my own router; Freerouting could not be used here). The result passes every rule check, but a person should look at the analog routing, ground return paths and connector mechanics.
2. **Schematics are structured and partly wired, but not hand-drawn quality**; the engineer should tidy them for presentation.
3. **Parts:** LCSC numbers marked `verified` were found by web search (ATmega328P-AU C14877, MCP6001T-I/OT C116490, MMBT3904 C20526, 1N4148WS C2128, AO3401A C15127, TYPE-C-31-M-12 C165948); passive numbers are from memory and **must be checked**; connectors, switches, buzzer and TVS/PTC parts have no number yet. No price or stock was checked.
4. **Clock/voltage:** the 2 x AAA board must run at 4 MHz (8 MHz needs 2.7 V); the board README gives fuse values; confirm against the current ATmega328P datasheet.
5. **Not verified:** real sensor behaviour (microphone capsule, meter LED coupling, plate resistance in real rain), EMC/ESD tests, battery life (estimates only), thermal, mechanical fit of the enclosure with real parts (the STEP uses KiCad's stock 3D models).
6. Seeti's anti-alias filter is first-order only (about 8 dB at 16 kHz); production firmware should use timer-triggered ADC sampling at 16 kS/s.
"""
open(os.path.join(HERE, "README.md"), "w").write(txt); print("written")
