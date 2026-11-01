# Rain Alert Bell (indoor unit + rain plate): manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** A comb-trace rain plate on the terrace wall, a cable to an indoor bell unit. A 3 s wet threshold avoids dew and splashes, rings, mutes for 30 min and rings again if it is still raining; resets after 2 min dry.

**Product line / price in the plan:** Tier A · low-voltage electronics · prototype Rs 780 · price Rs 899. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/rain/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/rain_alert.hex`) | `utility10/firmware/release/8MHz/boards/rain_alert.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/07-rain-alert/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **3 x AA**.

## 3. Bill of materials

### 3a. Circuit board parts (24 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J3 | Rain plate | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| BZ1 | Buzzer 85dB | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| SW2 | Mute | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| D1 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| D3 | TVS 5V bidir | D_SOD-323 | Nexperia PESD5V0S1BA,115 | C19224 | SMT (JLC) |
| D4 | TVS 5V bidir | D_SOD-323 | Nexperia PESD5V0S1BA,115 | C19224 | SMT (JLC) |
| R1 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R2 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R3 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| C5 | 2.2n | C_0603_1608Metric | Samsung CL10B222KB8NNNC X7R | C16033 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU (small) | 30 |
| Rain plate PCB | 25 |
| Loud buzzer | 25 |
| 3×AA holder | 25 |
| 5 m cable | 25 |
| Enclosure | 45 |
| Packaging | 30 |
| Assembly + test | 35 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/rain/1_fabrication/rain_alert_main_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: **ENIG** for the rain plate, HASL lead-free for this board.
Board size and layer list are in `utility10/pcb/release/rain/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (3 x AA).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 2.7 V (the 8 MHz speed-grade limit): the unit resets cleanly when the battery is flat).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/8MHz/boards/rain_alert.hex:i` then `-U flash:v:utility10/firmware/release/8MHz/boards/rain_alert.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D7 | 11 | LED |
| D9 | 13 | BUZ |
| A0 | 23 | SENSE |
| A2 | 25 | DRV_MCU |
| D2 | 32 | BTN |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Insert 3 x AA, switch ON: TP1 = 4.2-4.6 V.
2. Connect the plate: SENSE (TP3) between readings = 0 V; during a reading about 0.2 V with a dry plate.
3. Wet the plate with a drop of water: SENSE rises to > 1.7 V during the 5 ms pulse; after 3 s of continuous wet readings the buzzer sounds.
4. Flash over ISP with fuses lfuse 0xE2, hfuse 0xD9, efuse 0xFD (8 MHz internal, BOD 2.7 V: the unit resets cleanly when the batteries fall below 2.7 V, which is the 8 MHz limit).

## 8. Step 5: sensors, cables and mechanical assembly

- **Rain plate** (separate PCB, `utility10/pcb/release/rainplate`): order **ENIG** finish and no mask over the comb; solder a 2-core outdoor cable (UV-resistant, up to 10 m) to the two pads and seal the solder joints and cable entry with silicone or hot-melt. Mount the plate tilted about 10 degrees so water drains. A TVS diode on the indoor unit protects against surge on the long cable.
- Connect to J3 on the indoor unit (DRV, SENSE).

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×45×24 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- Wet threshold and 3 s debounce are firmware constants; check with tap water and with dew (a damp cloth should not trigger within 3 s).

## 11. Step 8: end-of-line functional test (every unit)

1. Wet the plate with a drop of water for 4 s: alert rings; dry the plate: the alert clears after 2 minutes.
2. Mute button: rings stop for 30 minutes; check it rings again if still wet afterwards.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| Corrodes in monsoon | check ENIG was ordered, plate not exposed to current continuously (the circuit pulses 5 ms) |
| False alerts | cable pickup: use twisted pair, shorter cable |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests: no alert for a 2 s wet blip or a flickering sensor, alert after 3 s, mute, re-ring after mute, clears after dry. Not verified: plate corrosion (use gold-plated or carbon traces), cable length effect.

Corrosion; smart-home rain alerts compete but need WiFi/apps.

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
