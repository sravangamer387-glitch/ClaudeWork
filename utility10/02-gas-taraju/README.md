# 02 · Gas Taraju (LPG cylinder scale)

**Tier B** · low-voltage electronics · prototype Rs 1730 · price Rs 2499. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Nobody knows how much LPG is left. Cheap magnetic strips are approximate; dealer scales cost about ₹1,300 and are B2B [S]. **This is a weight scale, not a leak detector.**

## How it works
The cylinder stands on a 330 mm plate over four load cells. After the cylinder is placed and still for 3 s the scale subtracts the tare stamped on the collar and shows % and kg left. It learns daily use and shows days left; a low LED/buzzer warns at 15%.

## What I verified (and what I did not)
Host tests (110 checks incl. other tools): calibration, rejects readings while the cylinder is being placed or bumped, full cylinder reads 14.2 kg / 100%, learned consumption within 0.05 kg/day, empty reads 0%. A real bug was found: the sample history froze after 255 samples (index stuck), fixed. Not verified: real load cell drift/temperature, hysteresis under 30 kg, creep.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`gs_*`), demo build `firmware/release/gas_taraju.hex`. Nano pins: HX711 DT D4, SCK D5, LEDs D6-D8, buzzer D9 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (90×60×26 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Zero the plate, place a 20 kg reference weight: reading within ±0.1 kg; remove: returns to 0 ±0.05 kg; store counts/kg in EEPROM.

## PCB (rev B, engineering release)
See `../pcb/README.md`; files in `../pcb/release/gastaraju/`.

## Prototype budget (Rs 1730, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| 4 load cells + HX711 | 650 |
| MDF plate (cut) | 350 |
| LEDs, buzzer | 80 |
| Wires, screws | 150 |
| 20 kg test weight (bag of rice) | 100 |
| **Total** | **1730** |

## Designed production BOM (~2,000 units, estimate Rs 757)
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

## Economics (marketplace, GST 18 % assumed)
Price Rs 2499 → contribution Rs 661 (31%); BOM +30 %: Rs 396 (19%). The first-draft price was Rs 1799, which made too little margin, so it was raised.

## Manufacturing
Plate by laser shop (SVG/DXF in out/); electronics module PCBA at EMS. Cells need a rigid level plate and four rubber feet.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Accuracy needs calibration per unit; load cell cost drives BOM; cylinders have different tare weights (user enters it).

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
