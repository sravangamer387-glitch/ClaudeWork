# Bijli Meter Reader: manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** A clip-on photodiode head sits on the meter's pulse LED. The unit counts pulses (20 ms debounce), shows live watts, kWh since reset and an estimated bill from slab rates you enter. **No mains contact.**

**Product line / price in the plan:** Tier A · low-voltage electronics · prototype Rs 900 · price Rs 1299. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/bijli/` | **order-ready: every automatic check passes** (DRC errors 0, netlist match True) |
| Firmware (`boards/bijli_meter.hex`) | `utility10/firmware/release/8MHz/boards/bijli_meter.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/04-bijli-meter-reader/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **5 V USB charger (not supplied with the PCB)**.

## 3. Bill of materials

### 3a. Circuit board parts (20 parts, 3 test points)

SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| F1 | PTC 500mA | Fuse_1206_3216Metric | Littelfuse 1206L050YR (6 V) | C163512 | SMT (JLC) |
| D3 | SMAJ5.0A | D_SMA | Littelfuse SMAJ5.0A | C83329 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J3 | Sensor head | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J4 | TM1637 display | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| SW1 | Reset bill | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R3 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| R4 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| R6 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | SMT (JLC) |
| C1 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C4 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C5 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)

| Item | Rs |
|---|---|
| MCU + crystal | 45 |
| Photodiode + amp | 25 |
| 4-digit display | 35 |
| Clip head + cable | 40 |
| Battery/USB | 30 |
| PCB | 30 |
| Enclosure | 50 |
| Packaging | 30 |
| Assembly + test | 40 |

## 4. Step 1: fabricate the PCB

Upload `utility10/pcb/release/bijli/1_fabrication/bijli_meter_reader_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: HASL lead-free.
Board size and layer list are in `utility10/pcb/release/bijli/README.md`.

## 5. Step 2: assemble the board

1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).
2. Solder the through-hole parts listed `hand/THT` in 3a.
3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.

## 6. Step 3: program the microcontroller

1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered (5 V USB charger (not supplied with the PCB)).
2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m`  (internal 8 MHz RC, CKDIV8 off, brown-out 2.7 V (the 8 MHz speed-grade limit): the unit resets cleanly when the battery is flat).
3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:utility10/firmware/release/8MHz/boards/bijli_meter.hex:i` then `-U flash:v:utility10/firmware/release/8MHz/boards/bijli_meter.hex:i`.
4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).

If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool).

Firmware pin map (generated from the PCB spec, so firmware and board agree):

| Arduino pin | ATmega pin | Net |
|---|---|---|
| D3 | 1 | DCLK |
| D4 | 2 | DIO |
| D7 | 11 | LED |
| A0 | 23 | SIG |
| D2 | 32 | BTN |

**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.


## 7. Step 4: electrical bring-up

1. Plug a 5 V charger: VBUS (TP at J1/F1) = 5.0 V; +5V (TP1) = 4.9-5.0 V.
2. SIG with head disconnected = 5 V (pull-up); with the phototransistor in the dark about 4.9 V; under a lit meter LED a drop of at least 0.5 V.
3. Flash over ISP: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m` (internal 8 MHz, brown-out 2.7 V; USB supply is 5 V).
4. Hold the head over a 1 Hz test LED: display counts one pulse per second.

## 8. Step 5: sensors, cables and mechanical assembly

- **Clip-on sensor head.** Solder the phototransistor/photodiode (J3 3-pin lead: +5 V, SIG, GND) on a 1.5 m cable inside a black ABS clip that blocks ambient light and sits over the meter's pulse LED; use heat-shrink at the cable exit. **There is no mains contact: never open the meter or touch its terminals.**
- Display: a TM1637 4-digit module plugs into the 4-pin JST-PH J4 (GND, +5V, DIO, CLK).

## 9. Step 6: enclosure and final assembly

1. Print the shell (STANDARD_PROCEDURES section G). Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (80×50×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.
2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.
3. Label: serial number, rev, battery type/polarity, warnings.

## 10. Step 7: calibration

- Enter the meter constant (pulses per kWh, printed on the meter) in the setup; verify with a known load (a 100 W lamp for 10 minutes gives about 0.017 kWh).

## 11. Step 8: end-of-line functional test (every unit)

1. Flash a 1 Hz LED at the head: count = 1 per second; cover with ambient light: no spurious counts.
2. Check that watts and kWh are displayed and the estimated bill uses the slab rates entered.

Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.

## 12. Packaging, documents, compliance

- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.
- Compliance items to verify before sale: Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims..
- Labelling: STANDARD_PROCEDURES K.

## 13. Troubleshooting (product specific)

| Symptom | Cause / action |
|---|---|
| No pulses | head not aligned to the pulse LED: check SIG voltage swing, at least 0.5 V drop when the LED is lit |
| Count too high | ambient light leak: improve the clip shielding |

General issues: STANDARD_PROCEDURES section L.

## 14. Known limits and risks

Host tests: 1000 W for one simulated hour produces 1600 pulses and 1.000 kWh; watts from the pulse gap within 4%; idle shows 0 W; slab bill arithmetic; bounce rejected. Slab rates in the code are placeholders, **not a real DISCOM tariff**. Not verified: sensing under sunlight, different LED colours/meter types.

Meter types differ; some new smart meters have no accessible LED; customers may expect an app.

Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.
