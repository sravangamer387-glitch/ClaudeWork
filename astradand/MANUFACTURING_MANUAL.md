# ASTRADAND gesture wand: manufacturing manual

> **Status: design only; nothing built or tested on hardware.** PCB: **not yet released: do not send to a fab**. Printed shell: generated, never printed. Firmware: engine host-tested, board code compiled only. Expect to correct this manual after the first 5-unit prototype run.

## 1. What is made

A 232 mm hilt: two FDM-printed shell halves holding a 146 x 26 mm PCB (ATmega328P, MPU-6050 IMU, six WS2812B pixels, piezo, haptic motor), three AAA cells in line, a diffuser crystal, trigger cap, tip and pommel; a laser-cut display stand, a carton, nine spell cards. See `astradand/docs/CONCEPT.md` for play and `DESIGN` notes there.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB (Gerbers, BOM, CPL, KiCad, STEP) | `utility10/pcb/release/astradand/` | **not yet released: do not send to a fab** |
| Firmware | `astradand/firmware/release/astradand_8MHz.hex`; source `astradand/firmware/lib/ad_core.c`, `src/main_astradand.cpp` | engine 83 host checks; board code compiled (19.7 KB flash, 1.1 KB RAM) |
| Shell STL | `astradand/cad/out/hilt_upper.stl`, `hilt_lower.stl`, `crystal.stl`, `trigger_cap.stl`, `tip_cap.stl`, `pommel.stl` | watertight; unprototyped |
| Stand (laser) | `astradand/cad/out/stand_laser.svg/.dxf` | 6 mm MDF; unprototyped |
| Carton dieline | `astradand/cad/out/carton_dieline.svg/.dxf` | inside 250 x 64 x 54 mm |
| Spell cards | `astradand/spellbook/out/spell_cards_A4.pdf` (+ one SVG per card) | Hindi names unreviewed |
| Assembly section | `astradand/cad/out/assembly_section.png` | drawing |
| Test plan / economics | `astradand/docs/TEST_PLAN.md`, `economics.md` | |

### Bought-in and mechanical (estimates for 2,000 units)

3 x AAA in-line holder with leads (JST-PH 2-pin), coin vibration motor with JST-PH 2-pin lead (3 V, 8-10 mm, under 80 mA), M2.5 x 8 mm self-tapping screws x 12, rubber grommet for the battery lead, translucent natural PETG or clear resin for the crystal, PETG (opaque, any dark colour) for the shell, 350 gsm board for the carton, 6 mm MDF for the stand, 300 gsm card for the spell cards.

## 4. Make the board

1. Order bare PCBs and SMT assembly per `manuals/STANDARD_PROCEDURES.md` A and B. The WS2812B-Mini, MPU-6050 (QFN, check the 0.5 mm pitch exposed-pad variant in the assembly preview), AP2112K, piezo and passives are on the JLC BOM when released. **The MPU-6050 is a not-recommended-for-new-designs part: confirm stock before ordering.**
2. Solder the hand/THT parts: ISP header J2, JST battery J1 and motor J4, slide switch SW1 (SMT), trigger SW2.
3. Check for shorts between +4V5, +3V3, VLED and GND before power.

## 5. Program

```
avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m
avrdude -p m328p -c usbasp -U flash:w:astradand/firmware/release/astradand_8MHz.hex:i
```
Pin map: D2 IMU INT, D3 trigger, D4 haptic, D5 LED supply switch, D6 WS2812 data, D9/D10 piezo, A0 battery divider, A4/A5 I2C. Then run Gate 1 of `astradand/docs/TEST_PLAN.md` before assembling any unit: it checks I2C, the WS2812 timing on a scope, sleep current and battery reading.

## 6. Print the shell (FDM prototype)

| Part | File | Size (mm) | Notes |
|---|---|---|---|
| hilt_upper | `hilt_upper.stl` | 232.0 x 35.6 x 17.8 | volume 29.84 cm3 |
| hilt_lower | `hilt_lower.stl` | 232.0 x 35.6 x 17.8 | volume 40.27 cm3 |
| crystal | `crystal.stl` | 51.4 x 6.8 x 12.4 | volume 4.29 cm3 |
| trigger_cap | `trigger_cap.stl` | 8.4 x 8.4 x 7.7 | volume 0.24 cm3 |
| tip_cap | `tip_cap.stl` | 22.0 x 34.0 x 34.0 | volume 6.65 cm3 |
| pommel | `pommel.stl` | 19.8 x 33.0 x 33.0 | volume 11.19 cm3 |

- Material: PETG for the shell (dark colour so the LEDs do not show through the wall), **translucent natural PETG or clear resin for the crystal**; nozzle 0.4 mm, layers 0.2 mm, 3 perimeters, 25 % infill, no supports for the halves (print each half with the split face on the bed, i.e. the open side down) except under the trigger hole bridge.
- The crystal needs a smooth top face: print with the long face down at 0.12 mm layers, sand 400-1000 grit and flame-polish lightly or finish with clear resin.
- Print one set first; test-fit the real PCB, battery tube and motor: the rails, bosses and the 0.3 mm tube clearance are first-pass numbers.

## 7. Assemble a unit

1. Seat the PCB (components up) on the rails of the upper half; the six pixels must sit under the crystal slit; the trigger button under the 6 mm hole.
2. Insert the three cells into the holder, route the leads to J1; seat the holder in the lower half's tube; press the motor into its pocket near J4 and plug it in (a drop of hot glue).
3. Place the diffuser crystal in the slit, add the trigger cap; close the halves and fasten the 12 screws (M2.5 x 8 into the pilot holes, 0.3 Nm): **the battery door is the shell itself, screw-closed**.
4. Press on the tip cap and pommel (friction fit, a dot of cyanoacrylate if loose).
5. Switch on: power-on tune, mana crystals lit.

## 8. End-of-line test (every unit)

Programme and verify; I2C scan; gyro rest bias under 5 dps; draw a circle and a Z (both must cast); colour sweep on all six pixels; sound and haptic; battery reading 4.5 V +-0.2; sleep current under 100 uA after 45 s; record on `manuals/templates/eol_test_sheet.md`.

## 9. Stand, carton, cards

- Stand: laser-cut `stand_laser.dxf` from 6 mm MDF (kerf test first), glue the two cradles into the base slots; seal with water-based lacquer; felt feet.
- Carton: print artwork on 350 gsm board, die-cut from `carton_dieline.dxf`, fold on the blue lines, glue the 14 mm flap.
- Cards: print `spell_cards_A4.pdf` on 300 gsm card at 100 %, cut on the crop marks (63 x 88 mm), round the corners. **Proofread the Devanagari names with a native speaker before printing.**

## 10. Packaging, compliance, limits

Label 9+ (small parts, battery), include a battery warning and a screw-closed compartment statement; Legal Metrology marks; verify toy-standard applicability, battery and EMC testing, LED eye safety (diffused, unmeasured) and e-waste obligations with a lab before selling (Gate 4). Not done: any hardware test, human gesture data, certification. Economics: marginal at Rs 2,499, target Rs 2,999 (`economics.md`).
