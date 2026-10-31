# 08 · Tap Litre Meter

**Tier B** · low-voltage electronics · prototype Rs 1200 · price Rs 1199. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Water is scarce in many Indian cities and tanker-fed; people cannot see how many litres a bath, bucket or garden watering uses.

## How it works
An inline flow sensor on a tap or hose; the display shows litres this session and today, and a buzzer rings when a set target (e.g. 20 L bucket) is reached.

## What I verified (and what I did not)
Host tests: litres from pulses, a session ends after 5 s without flow, target alarm at 10 L, new session starts cleanly, day total adds. Pulses per litre (450) is a typical datasheet value, **the pack includes a 10 L bucket calibration**.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`tap_*`), demo build `firmware/release/tap_litre.hex`. Nano pins: flow D3 (interrupt), display I2C (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×50×24 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Run 10 L from a calibrated bucket: reading 10 L ±0.2 L (adjust pulses/L).

## PCB (rev B, engineering release)
See `../pcb/README.md`; files in `../pcb/release/tap/`.

## Prototype budget (Rs 1200, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| Flow sensor | 250 |
| Display | 150 |
| Hose fittings, tape | 200 |
| Bucket, wires, box | 200 |
| **Total** | **1200** |

## Designed production BOM (~2,000 units, estimate Rs 380)
| Item | Rs |
|---|---|
| Hall flow sensor G1/2 | 90 |
| MCU | 45 |
| Display | 35 |
| Battery | 25 |
| PCB | 30 |
| Enclosure | 50 |
| Hose adapters | 35 |
| Packaging | 30 |
| Assembly + test | 40 |

## Economics (marketplace, GST 18 % assumed)
Price Rs 1199 → contribution Rs 235 (23%); BOM +30 %: Rs 102 (10%). The first-draft price was Rs 999, which made too little margin, so it was raised.

## Manufacturing
Flow sensor sourced from a supplier with a lot calibration sheet; potted electronics for splash.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Accuracy at low flow; sensors clog with sediment (add a filter screen); seals.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
