# ASTRADAND gesture wand: manufacturing manual

> **Status: design only; nothing built or tested on hardware.** PCB: **order-ready: every automatic check passes**. Printed shell: generated, never printed. Firmware: engine host-tested, board code compiled only. Expect to correct this manual after the first 5-unit prototype run.

## 1. What is made

A 232 mm hilt: two FDM-printed shell halves holding a 146 x 26 mm PCB (ATmega328P, MPU-6050 IMU, six WS2812B pixels, piezo, haptic motor), three AAA cells in line, a diffuser crystal, trigger cap, tip and pommel; a laser-cut display stand, a carton, nine spell cards. See `astradand/docs/CONCEPT.md` for play and `DESIGN` notes there.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB (Gerbers, BOM, CPL, KiCad, STEP) | `utility10/pcb/release/astradand/` | **order-ready: every automatic check passes** |
| Firmware | `astradand/firmware/release/astradand_8MHz.hex`; source `astradand/firmware/lib/ad_core.c`, `src/main_astradand.cpp` | engine 83 host checks; board code compiled (19.7 KB flash, 1.1 KB RAM) |
| Shell STL | `astradand/cad/out/hilt_upper.stl`, `hilt_lower.stl`, `crystal.stl`, `trigger_cap.stl`, `tip_cap.stl`, `pommel.stl` | watertight; unprototyped |
| Stand (laser) | `astradand/cad/out/stand_laser.svg/.dxf` | 6 mm MDF; unprototyped |
| Carton dieline | `astradand/cad/out/carton_dieline.svg/.dxf` | inside 250 x 64 x 54 mm |
| Spell cards | `astradand/spellbook/out/spell_cards_A4.pdf` (+ one SVG per card) | Hindi names unreviewed |
| Assembly section | `astradand/cad/out/assembly_section.png` | drawing |
| Test plan / economics | `astradand/docs/TEST_PLAN.md`, `economics.md` | |

## 3. Circuit board bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | BATT 3xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| D11 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C20 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D12 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C21 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D13 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C22 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D14 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C23 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D15 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C24 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| D16 | WS2812B-Mini | LED_WS2812B-Mini_PLCC4_3.5x3.5mm | Worldsemi WS2812B-Mini 3535 (LCSC listing; confirm the variant suffix against the datasheet) | C114583 | SMT (JLC) |
| C25 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| U2 | MPU-6050 | InvenSense_QFN-24_4x4mm_P0.5mm | MPU-6050 | C24112 | SMT (JLC) |
| C10 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C11 | 2.2n | C_0603_1608Metric | Samsung CL10B222KB8NNNC X7R | C16033 | SMT (JLC) |
| C12 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C13 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R20 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| R21 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| U3 | AP2112K-3.3 | SOT-23-5 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | SMT (JLC) |
| C5 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C6 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| D20 | SS14 | D_SMA | Starsea SS14 SMA | C84343 | SMT (JLC) |
| Q3 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| Q4 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| R33 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R34 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C7 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R30 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| R31 | 330k | R_0603_1608Metric | UNI-ROYAL 0603WAF3303T5E | C23137 | SMT (JLC) |
| R32 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| BZ1 | PKLCS1212E4001 | Buzzer_Murata_PKLCS1212E | PKLCS1212E4001-R1 | C113159 | SMT (JLC) |
| SW2 | Cast trigger | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| J4 | Haptic motor | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |

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
