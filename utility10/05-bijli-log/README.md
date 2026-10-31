# 05 · Bijli Log (power-cut logger)

**Tier B** · low-voltage electronics · prototype Rs 1220 · price Rs 1499. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Power cuts are common in many Indian cities; people have no proof of how often and how long, for complaints or to size an inverter.

## How it works
Plugs into a wall 5 V USB adapter (supplied). When mains disappears it keeps running from a backup cell, timestamps start and duration, keeps the last 32 cuts in a ring and shows count, total hours without power and the last cut.

## What I verified (and what I did not)
Host tests: a 1-hour cut is logged with the right duration, 1 s flickers are ignored (2 s debounce), 40 cuts keep the last 32 and total outage adds up. Not verified: real clock drift (needs an RTC), backup cell life.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`pc_*`), demo build `firmware/release/bijli_log.hex`. Nano pins: mains sense D2 (divider from 5 V), I2C display/RTC A4/A5 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×50×24 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Remove 5 V for 10 s: one cut of 10 s ±1 logged; restore.

## Prototype budget (Rs 1220, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| RTC module | 120 |
| OLED | 250 |
| USB adapter | 200 |
| Backup cell holder | 100 |
| Wires, box | 150 |
| **Total** | **1220** |

## Designed production BOM (~2,000 units, estimate Rs 475)
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

## Economics (marketplace, GST 18 % assumed)
Price Rs 1499 → contribution Rs 324 (26%); BOM +30 %: Rs 158 (12%). The first-draft price was Rs 1199, which made too little margin, so it was raised.

## Manufacturing
Use a certified bought-in adapter; the product itself is low-voltage.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Adapter compliance, a crowded smart-plug market (but none give a simple log), feature creep.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
