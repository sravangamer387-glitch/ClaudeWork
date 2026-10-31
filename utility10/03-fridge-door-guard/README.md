# 03 · Fridge Door Guard

**Tier B** · low-voltage electronics · prototype Rs 610 · price Rs 599. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
A fridge door left ajar wastes electricity and spoils food; many fridges (esp. older ones) have no alarm.

## How it works
A reed switch and magnet stick on the door gap. Quiet for 60 s, then a chirp every 10 s, continuous after 3 min; closing silences it. It also counts openings and total open time (for kids' door habits).

## What I verified (and what I did not)
Host tests: quiet in the first minute, chirps then continuous alarm at the thresholds, closing silences and logs time, 11 short opens never warn, millis() wrap-safe. Not verified: magnet alignment tolerance and battery life.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`fd_*`), demo build `firmware/release/fridge_guard.hex`. Nano pins: reed D2 (to GND), buzzer D9 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (60×30×18 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Magnet near reed: silent; magnet away 65 s: chirp; 185 s: continuous.

## Prototype budget (Rs 610, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| Reed switch + magnet | 40 |
| Buzzer | 30 |
| Wires, tape | 100 |
| Battery holder | 40 |
| **Total** | **610** |

## Designed production BOM (~2,000 units, estimate Rs 162)
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

## Economics (marketplace, GST 18 % assumed)
Price Rs 599 → contribution Rs 138 (27%); BOM +30 %: Rs 81 (16%). The first-draft price was Rs 349, which made too little margin, so it was raised.

## Manufacturing
Very simple PCBA; ABS two-piece housing with 3M adhesive.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Price pressure (₹150–300 door alarms exist), needs strong differentiation (open-time log, loudness, battery life).

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
