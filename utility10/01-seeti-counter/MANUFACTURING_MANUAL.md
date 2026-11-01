# Seeti Counter: manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** A heat-shielded clip puts a small microphone about 10 cm from the whistle. A Goertzel filter looks for the whistle's narrow tone; a whistle must last 0.4 s to count. After N whistles (button picks 1–6) a buzzer rings 5 times.

**Product line / price in the plan:** Tier A · low-voltage electronics · prototype Rs 1080 · price Rs 999. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/seeti/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`seeti_prod.hex`) | `utility10/firmware/release/4MHz/seeti_prod.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/01-seeti-counter/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **2 x AAA**.

## 3. Bill of materials

### 3a. Circuit board parts (32 parts, 4 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| U2 | MCP6001 | SOT-23-5 | MCP6001T-I/OT | C116490 | SMT (JLC) |
| J1 | BATT 2xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J3 | MIC electret | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| J4 | UART | PinHeader_1x04_P2.54mm_Vertical | ZHOURI 2.54-1*4 | C5116483 | hand/THT |
| BZ1 | Buzzer 3V | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| SW2 | Target | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R1 | 2.2k | R_0603_1608Metric | 0603 2.2k 1% | C4190 | SMT (JLC) |
| R2 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R3 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R4 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| R8 | 33k | R_0603_1608Metric | UNI-ROYAL 0603WAF3302T5E | C4216 | SMT (JLC) |
| R9 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| C5 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | SMT (JLC) |
| C6 | 220n | C_0603_1608Metric | Samsung CL10B224KB8NNNC X7R 50V | C64705 | SMT (JLC) |
| C7 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| C8 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R10 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| C9 | 22n | C_0603_1608Metric | Samsung CL10B223KB8NNNC X7R | C21122 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU + crystal | 45 |
| Electret mic amp module | 40 |
| Buzzer | 12 |
| PCB | 30 |
| 2×AAA holder + switch | 18 |
| Heat-resistant clip/magnet mount | 40 |
| Enclosure | 50 |
| Packaging + Hindi/Telugu manual | 30 |
| Assembly + test | 40 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/seeti/1_fabrication/seeti_counter_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/seeti/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (2 x AAA).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz (2 x AAA supply may fall to 2.0 V)).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/4MHz/seeti_prod.hex:i` then `-U flash:v:utility10/firmware/release/4MHz/seeti_prod.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D7 | 11 | LED |
| D9 | 13 | BUZ |
| A0 | 23 | ADC_IN |
| D0 | 30 | RXD |
| D1 | 31 | TXD |
| D2 | 32 | BTN |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Insert 2 x AAA with switch OFF; measure BAT_P to GND (J1 pins) = 2.8-3.2 V.
2. Switch ON: TP1 (+3V0) = battery minus about 0.05 V; no heating.
3. VMID (R2/R3 junction) = VCC/2 +-0.05 V; TP3 (MIC_OUT) = VCC/2 +-0.1 V with no sound (same DC at the ADC pin through R10).
4. Flash firmware over ISP (J2): `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m` (internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz).
5. Play a 2.8 kHz tone from a phone at 10 cm: TP3 swings about +-100 mV peak and the firmware counts whistles.

## 8. Step 5: sensors, cables and mechanical assembly

- **Heat-resistant microphone clip.** Solder the electret capsule (J3, 2-pin JST-PH lead, + toward the marked pin) to a 30 cm 2-core lead. Fix the capsule in the clip behind a stainless-steel mesh window so steam cannot reach it. The clip must hold the capsule 10 cm from the cooker vent and be rated to 85 C (use a high-temperature ABS or metal spring clip; do not use a PLA part near the vent).
- Add a magnet or hook to the unit's back so it stays on the hood; the electronics unit itself must stay at least 10 cm from the vent.

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×45×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- Whistle frequency is an assumption (2.8 kHz in the tests). Record 5 real cookers of the brands you target, find the dominant whistle frequency and amplitude with a phone spectrum app, and set the filter frequency in `firmware/lib/utilcore.c` (`seeti_*`) before the production run. Re-run the 115 host tests (`make test`).

## 11. Step 8: end-of-line functional test (every unit)

1. Play a 2.8 kHz tone from a phone speaker at 10 cm for 1 s: the counter increments; play white noise: it must not count.
2. Press the button to select 1, 3 and 6 whistles; after the selected count the buzzer rings 5 times.
3. Battery: measure the supply current at 3.0 V; it should be a few mA (estimate 3.6 mA); a unit above 10 mA fails.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Counts nothing | microphone polarity reversed or gain too low: check TP3 swing at a 2.8 kHz tone, about +-100 mV |
| Counts noise | threshold or filter frequency wrong for this microphone placement; see the limit in the README (amplitude 300 against noise 1200 counted 0 of 3) |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Synthetic kitchen audio (noise + 100 Hz hum): 3/3 whistles counted, 0 counts for 100 ms clinks, 0 for loud noise alone, 0 for a different-frequency tone, 3/3 with whistle 1.5k vs noise 1.5k amplitude. **Limit found:** a whistle at amplitude 300 against noise 1200 counted 0 of 3, so mic placement and gain matter. The whistle frequency (2.8 kHz here) is an assumption: **record 5 real cookers and set it**.

Whistle frequency varies by cooker brand; steam moisture on the mic; kitchen heat; false counts from a second cooker.

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
