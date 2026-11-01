# Chulha Timers: manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** Four buttons = four channels. Tap adds one minute, hold 1 s clears. Each channel rings separately; the display shows the soonest. Magnet back sticks to the fridge or hood.

**Product line / price in the plan:** Tier B · low-voltage electronics · prototype Rs 970 · price Rs 1199. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/chulha/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/chulha_timers.hex`) | `utility10/firmware/release/8MHz/boards/chulha_timers.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/06-chulha-timers/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **3 x AAA**.

## 3. Bill of materials

### 3a. Circuit board parts (19 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

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
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| SW2 | CH1 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW3 | CH2 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW4 | CH3 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| SW5 | CH4 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| J4 | TM1637 display | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU | 45 |
| 8-digit display module | 70 |
| 4 buttons + caps | 25 |
| Buzzer | 12 |
| Magnet back | 30 |
| Battery/USB | 30 |
| PCB | 30 |
| Enclosure | 50 |
| Packaging | 30 |
| Assembly + test | 40 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/chulha/1_fabrication/chulha_timers_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/chulha/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (3 x AAA).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 2.7 V (the 8 MHz speed-grade limit): the unit resets cleanly when the battery is flat).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/8MHz/boards/chulha_timers.hex:i` then `-U flash:v:utility10/firmware/release/8MHz/boards/chulha_timers.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D3 | 1 | B2 |
| D4 | 2 | B3 |
| D5 | 9 | B4 |
| D9 | 13 | BUZ |
| A4 | 27 | DIO |
| A5 | 28 | DCLK |
| D2 | 32 | B1 |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Power on: display shows 0; tap CH1: +1 min counts down.
2. Ring: each channel's buzzer pattern stops with its own button.

## 8. Step 5: sensors, cables and mechanical assembly

- **Magnet back.** Glue a flat ferrite or neodymium magnet (about 30 x 20 x 3 mm) to the back plate with epoxy; keep it away from the display ribbon. TM1637 display module goes on J4.

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (100×55×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- None. Check the timing accuracy over 10 minutes against a reference stopwatch: the internal RC oscillator is about +-1 to 2 %, which is 6-12 s in 10 minutes: decide whether that is acceptable (a crystal is not fitted) and say so on the pack.

## 11. Step 8: end-of-line functional test (every unit)

1. Set 1:00 on each of the four channels (tap adds one minute): four independent rings within +-1 s of each other.
2. Hold a button 1 s: the channel clears.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Timers run fast/slow | internal RC tolerance: calibrate OSCCAL on the unit if tighter accuracy is needed |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests: independent channels, acknowledge only one, add/subtract with floor at zero, 99-minute cap, wrap-safe. Not verified: display ergonomics and buzzer loudness.

Cheap multi-timers exist (₹250–500): compete on loudness, clarity and Indian packaging.

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
