# Gatekeeper audit: final prototype sign-off (2026-11-02)

Scope: all 20 released boards, the generated enclosures (`utility10/pcb/enclosure.py`), the ASTRADAND hilt CAD, the automata gear/cam CAD, the toy manuals, and the live LCSC BOM data. Evidence: tool output and the files themselves; nothing has been built.

## Status: HOLD FOR REVISION (portfolio). Bare-PCB bench prototypes are approved per the table below; enclosures and anything for children are not.

## Blocking issues (ranked)
1. **MITTI-NETRA: TP4056 exposed pad (U4 pad 9) has no net.** Measured in the released PCB. About 0.8 W at the start of a charge (4.65 V in, 3.2 V cell, 0.55 A) with no thermal path: the IC will thermally throttle and run hot. Fix: tie pad 9 to GND (pour), re-run DRC.
2. **MITTI-NETRA: Li-ion charging outdoors with no temperature cut-off.** TEMP pin is tied to GND (disables the TP4056 NTC function); a sealed box in Indian sun exceeds 45 C, where Li-ion must not be charged. Fix: 10 k NTC divider on TEMP placed against the cell, or switch to LiFePO4 with a matching charger.
3. **All generated enclosures: the lid is held only by a friction lip** (no screws, no snap). It falls off on a drop, and any battery inside is reachable without a tool. Fix: add 2 to 4 lid screw bosses (M2.5 into 2.1 mm pilots) or snap hooks with a defined interference.
4. **All generated enclosures: tact switches are unreachable.** The B3U switch top sits 10.4 to 11.4 mm below the lid surface under a 5 mm hole (12 boards). Fix: printed plunger caps with a retaining flange, or a taller switch (12 x 12 mm tactile with cap).
5. **Toy products (Desi Arcade, Beat Runner): the manuals promise a screw-closed battery door; the CAD has no battery bay at all** (inner height 11 to 12 mm; a 3 x AAA holder is about 14 mm tall). Fix: design a base with a screw-retained battery compartment before any child testing.
6. **KINETIC and MITTI-NETRA enclosures ignore plug-in modules.** StepStick drivers with heatsinks (about 20 mm above the socket) and the SIM7080G breakout plus the 18650 cell are not in the height model; the lid collides, and the driver box has no ventilation.
7. **BioTray / AQUAPONICS: enclosure is not water-resistant** (friction lid, open side cut-outs) for a wet environment with 12 V pumps.
8. **Gas-Suraksha: board not finished and the product is not certified**; Jal-Rakshak and the AP1 audio platform have no board.

## Fixed during this review (already in the released files)
- Reversed power diodes: MITTI-NETRA D1/D2, KINETIC D5, BioTray D5 (would have blocked charging or back-fed USB).
- Out-of-stock and low-stock parts replaced with in-stock, same-footprint parts (see `costing/DESIGN_REVIEW_LOG.md`).

## Non-blocking findings
- Laser-cut automata gears and cams: kerf is applied in the shrinking direction twice (design reduction plus no outward offset of the cutting path): effective gear backlash about 0.55 mm at module 2 (works, a little loose); cams about 0.2 mm small. Correct the offset sign before the production cut file.
- Passive magnetic buzzers (16 ohm) at 4.2 to 4.5 V exceed the 30 mA rating in continuous tones; add 22 ohm series for loud continuous alarms.
- SK6812MINI-B substitute on ASTRADAND: footprint fit unproven; order 2 boards first.
- Lid indicator holes over 0603 LEDs 10 mm below the lid: add light pipes or the LEDs will be hard to see.
- Generated boxes have sharp 90 degree external edges: add a 1 to 2 mm fillet for hand-held products and toys.
- Single-source and thin stock: BQ25570 (391), ESP32-S3-WROOM-1-N8 at LCSC (774, widely available elsewhere), 12 mm buzzer (140), PESD5V0S1BA (175); MPU-6050 is a mature part from one maker.

## Checked and found correct
Diode, TVS, Zener, LED, polarised-capacitor and transistor orientation on all boards; supply and ground pin names of every IC (0 errors, `pincheck.py`); ESP32 pin maps against the firmware headers; crystal-less ATmega boards have matching 8 MHz firmware builds; reverse-polarity PMOS on battery inputs; TVS on external inputs; ESP32 EN RC; I2C pull-ups; decoupling present within 16 mm of every IC (the ESP32 module within 25 mm); DRC 0, ERC 0, netlist match and the Gerber check on all 20 boards; ASTRADAND hilt: 12 screws, battery behind the screwed shell, fit-check PASS on the modelled volumes.
