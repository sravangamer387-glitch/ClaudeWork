# Gas Taraju (LPG cylinder scale): manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** The cylinder stands on a 330 mm plate over four load cells. After the cylinder is placed and still for 3 s the scale subtracts the tare stamped on the collar and shows % and kg left. It learns daily use and shows days left; a low LED/buzzer warns at 15%.

**Product line / price in the plan:** Tier B · low-voltage electronics · prototype Rs 1730 · price Rs 2499. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/gastaraju/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/gas_taraju.hex`) | `utility10/firmware/release/8MHz/boards/gas_taraju.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/02-gas-taraju/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **3 x AA**.

## 3. Bill of materials

### 3a. Circuit board parts (32 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| U4 | HX711 | SOIC-16_3.9x9.9mm_P1.27mm | Avia HX711 SOP-16 | C43656 | SMT (JLC) |
| R14 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| C10 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C11 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C12 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C13 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R15 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| C14 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C15 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| J3 | Load cell bridge E+ E- A+ A- | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| J4 | TM1637 4-digit | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| SW2 | Tare / zero | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| D5 | Amber | LED_0603_1608Metric | Everlight 19-213/Y2C-CQ2R2L/3T yellow 591 nm (marked obsolete by some distributors: check) | C72038 | SMT (JLC) |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| D6 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R9 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| 4 × 50 kg load cells | 360 |
| HX711 amp | 15 |
| MCU | 45 |
| 3-digit display + LEDs | 40 |
| Laser-cut plate + frame (MDF/acrylic) | 120 |
| PCB | 30 |
| Buzzer | 12 |
| Battery/USB | 30 |
| Packaging | 45 |
| Assembly + calibration | 60 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/gastaraju/1_fabrication/gas_taraju_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/gastaraju/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (3 x AA).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 2.7 V (the 8 MHz speed-grade limit): the unit resets cleanly when the battery is flat).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/8MHz/boards/gas_taraju.hex:i` then `-U flash:v:utility10/firmware/release/8MHz/boards/gas_taraju.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D3 | 1 | HX_SCK |
| D5 | 9 | LED_G |
| D6 | 10 | LED_A |
| D7 | 11 | LED_R |
| D8 | 12 | TARE |
| D9 | 13 | BUZ |
| A4 | 27 | DIO |
| A5 | 28 | DCLK |
| D2 | 32 | HX_DOUT |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Bridge disconnected: DOUT idles high; with a 20 kg reference weight reading is stable within 0.1 kg after calibration.
2. Zero with the plate empty (tare button).

## 8. Step 5: sensors, cables and mechanical assembly

- **Plate and load cells.** Laser-cut the 330 mm plate from the SVG/DXF in `utility10/out/` (check the product README for the file name); fit four load cells (half-bridge or full-bridge, wiring to the HX711 E+/E-/A+/A- inputs) under the plate corners on a rigid, level base with four rubber feet. A warped base or a plate that rocks destroys accuracy.
- Bonded-load-cell wiring: keep cable lengths equal and short; shield away from the buzzer lead.

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (90×60×26 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- Per-unit calibration is mandatory. Zero the empty plate, place a certified 20 kg reference weight, record counts per kg and offset, store in EEPROM; repeat at 5, 10, 15 kg to check linearity (error under +-0.1 kg). The user enters the cylinder tare weight stamped on the collar.

## 11. Step 8: end-of-line functional test (every unit)

1. Zero the plate; place a 20 kg reference weight: reading within +-0.1 kg; remove: returns to 0 +-0.05 kg.
2. Place a 14.2 kg net cylinder-equivalent (use test weights): reads 100 %; check the LED/buzzer low warning at 15 %.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Reading drifts | plate not rigid, one load cell loaded unevenly, or HX711 supply noisy: check the 4V5 rail ripple |
| This is not a leak detector | do not describe it as a gas safety device: it is a weight scale only |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests (110 checks incl. other tools): calibration, rejects readings while the cylinder is being placed or bumped, full cylinder reads 14.2 kg / 100%, learned consumption within 0.05 kg/day, empty reads 0%. A real bug was found: the sample history froze after 255 samples (index stuck), fixed. Not verified: real load cell drift/temperature, hysteresis under 30 kg, creep.

Accuracy needs calibration per unit; load cell cost drives BOM; cylinders have different tare weights (user enters it).

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
