# Gas Taraju (LPG cylinder scale): manufacturing manual

> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).

**Product summary.** The cylinder stands on a 330 mm plate over four load cells. After the cylinder is placed and still for 3 s the scale subtracts the tare stamped on the collar and shows % and kg left. It learns daily use and shows days left; a low LED/buzzer warns at 15%.

**Product line / price in the plan:** Tier B · low-voltage electronics · prototype Rs 1730 · price Rs 2499. Status: designed and verified as far as a computer can; no prototype built, nothing field-tested.

## 1. What you are building: deliverables

| Deliverable | Where | State |
|---|---|---|
| PCB | `utility10/pcb/` (layout in progress) | **not released**: do not send to a fab |
| Firmware (`boards/gas_taraju.hex`) | `utility10/firmware/release/8MHz/boards/gas_taraju.hex`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |
| Enclosure STL (prototype shell) | `utility10/02-gas-taraju/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |
| Mechanical / bought-in parts | section 3 | listed |
| Test sheet | `manuals/templates/eol_test_sheet.md` | template |

**The Gas Taraju PCB is not yet in the order-ready set** (see section 'Status of the PCB'). Until it passes the checks the board files should not be sent to a fab.

## 2. Before you start
- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).
- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.
- Power source for this product: **3 x AA**.

## 3. Bill of materials

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

The PCB for this product is not released yet: see section 'Status of the PCB'.

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

Not available until the PCB is released.

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

## Status of the PCB
The board is still being routed or reviewed. When it passes all automatic checks its folder appears in `utility10/pcb/release/` and this manual is regenerated.
