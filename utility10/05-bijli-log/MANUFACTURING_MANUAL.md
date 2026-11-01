# Bijli Log: manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** Plugs into a wall 5 V USB adapter (supplied). When mains disappears it keeps running from a backup cell, timestamps start and duration, keeps the last 32 cuts in a ring and shows count, total hours without power and the last cut.

**Product line / price in the plan:** Tier B · low-voltage electronics · prototype Rs 1220 · price Rs 1499. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/bijlilog/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/bijli_log.hex`) | `utility10/firmware/release/4MHz/boards/bijli_log.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/05-bijli-log/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **5 V USB charger + 2 x AAA backup**.

## 3. Bill of materials

### 3a. Circuit board parts (28 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| F1 | PTC 500mA | Fuse_1206_3216Metric | Littelfuse 1206L050YR (6 V) | C163512 | SMT (JLC) |
| D3 | SMAJ5.0A | D_SMA | Littelfuse SMAJ5.0A | C83329 | SMT (JLC) |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| C5 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| U3 | AP2112K-3.3 | SOT-23-5 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | SMT (JLC) |
| C6 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C7 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| D5 | BAT54WS | D_SOD-323 | BORN BAT54WS (300 mA listing) | C5148476 | SMT (JLC) |
| D6 | BAT54WS | D_SOD-323 | BORN BAT54WS (300 mA listing) | C5148476 | SMT (JLC) |
| J6 | BATT 2xAAA backup | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| C8 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| R12 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R13 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| J4 | OLED 0.91in I2C | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| J5 | RTC DS3231 module | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| R10 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| R11 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | SMT (JLC) |
| SW2 | Scroll / clear | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU | 45 |
| RTC module | 60 |
| Display 0.91 in OLED | 90 |
| Backup cell + charger | 40 |
| USB adapter (BIS-registered, bought in) | 90 |
| PCB | 30 |
| Enclosure | 50 |
| Packaging | 30 |
| Assembly + test | 40 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/bijlilog/1_fabrication/bijli_log_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/bijlilog/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (5 V USB charger + 2 x AAA backup).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz (2 x AAA supply may fall to 2.0 V)).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/4MHz/boards/bijli_log.hex:i` then `-U flash:v:utility10/firmware/release/4MHz/boards/bijli_log.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D7 | 11 | LED |
| A0 | 23 | MAINS |
| A4 | 27 | SDA |
| A5 | 28 | SCL |
| D2 | 32 | BTN |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Plug USB: +3V3 = 3.3 V, VSYS about 3.0 V, MAINS (TP3) about 2.5 V.
2. Unplug: MAINS goes low, unit stays alive on the battery, cut logged; replug: duration shown.

## 8. Step 5: sensors, cables and mechanical assembly

- **Modules.** OLED 0.91 in I2C module on J4 and DS3231 RTC module on J5 (GND, +V, SDA, SCL order is printed on the board). Fit a CR2032/AAA backup as per the README; use a certified, BIS-registered 5 V adapter: the unit itself is low voltage.

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×50×24 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- Set the RTC time once at the factory (and again by the user after a battery replacement). Check the RTC drift over 24 h (module spec about +-2 ppm for DS3231; clone modules vary).

## 11. Step 8: end-of-line functional test (every unit)

1. Remove 5 V for 10 s: one cut of 10 s +-1 s is logged; restore power.
2. Pull the cable again twice: the count increases and the last-cut screen updates.
3. Check the log survives a full power removal (backup cell holds the RTC).

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Time resets after power loss | RTC battery missing or dead |
| OLED blank | wrong module pinout: some modules swap GND and VCC |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests: a 1-hour cut is logged with the right duration, 1 s flickers are ignored (2 s debounce), 40 cuts keep the last 32 and total outage adds up. Not verified: real clock drift (needs an RTC), backup cell life.

Adapter compliance, a crowded smart-plug market (but none give a simple log), feature creep.

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
