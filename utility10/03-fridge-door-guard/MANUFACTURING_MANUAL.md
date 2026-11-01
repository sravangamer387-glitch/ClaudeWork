# Fridge Door Guard: manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** A reed switch and magnet stick on the door gap. Quiet for 60 s, then a chirp every 10 s, continuous after 3 min; closing silences it. It also counts openings and total open time (for kids' door habits).

**Product line / price in the plan:** Tier B · low-voltage electronics · prototype Rs 610 · price Rs 599. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/fridge/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/fridge_guard.hex`) | `utility10/firmware/release/4MHz/boards/fridge_guard.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/03-fridge-door-guard/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **2 x AAA**.

## 3. Bill of materials

### 3a. Circuit board parts (21 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | BATT 2xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| SW2 | Silence | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| J3 | Reed switch | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C9 | 10n | C_0603_1608Metric | 0603 10nF X7R | C57112 | SMT (JLC) |
| D4 | TVS 5V bidir | D_SOD-323 | Nexperia PESD5V0S1BA,115 | C19224 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU (small) | 30 |
| Reed switch + magnet | 15 |
| Buzzer | 12 |
| PCB | 20 |
| 2×AAA holder | 15 |
| Stick-on enclosure | 25 |
| Packaging | 20 |
| Assembly + test | 25 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/fridge/1_fabrication/fridge_door_guard_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/fridge/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (2 x AAA).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz (2 x AAA supply may fall to 2.0 V)).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/4MHz/boards/fridge_guard.hex:i` then `-U flash:v:utility10/firmware/release/4MHz/boards/fridge_guard.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D3 | 1 | REED |
| D7 | 11 | LED |
| D9 | 13 | BUZ |
| D2 | 32 | BTN |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Magnet next to reed: REED (TP3) low; remove: high and INT1 wakes the unit.
2. After 60 s open: chirp every 10 s; after 180 s: continuous; closing silences.

## 8. Step 5: sensors, cables and mechanical assembly

- **Reed switch and magnet.** Solder the reed switch (J3) to a 20 cm 2-core lead and fix it in the housing edge; glue a small neodymium magnet into a second housing piece; mounting is by 3M adhesive so the two halves face each other across the door gap with under 5 mm separation (alignment tolerance is not verified: test with the real fridge).

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (60×30×18 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- None. Verify that the reed closes reliably at the real door gap and magnet distance (try 2, 4 and 6 mm).

## 11. Step 8: end-of-line functional test (every unit)

1. Magnet near the reed: silent; magnet away 65 s: chirp; 185 s: continuous alarm; magnet back: silent.
2. Count the openings logged after 11 short opens: no warning should have sounded.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Alarm sounds with the door closed | magnet too far or reed contact stuck: replace the reed |
| Battery empties early | check sleep behaviour; battery life is not measured |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests: quiet in the first minute, chirps then continuous alarm at the thresholds, closing silences and logs time, 11 short opens never warn, millis() wrap-safe. Not verified: magnet alignment tolerance and battery life.

Price pressure (₹150–300 door alarms exist), needs strong differentiation (open-time log, loudness, battery life).

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
