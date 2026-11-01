# 07 · Rain Alert Bell (terrace/clothesline)

**Tier A** · low-voltage electronics · prototype Rs 780 · price Rs 899. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Clothes, pickles and papads drying on the terrace get soaked when it rains and nobody is watching.

## How it works
A comb-trace rain plate on the terrace wall, a cable to an indoor bell unit. A 3 s wet threshold avoids dew and splashes, rings, mutes for 30 min and rings again if it is still raining; resets after 2 min dry.

## What I verified (and what I did not)
Host tests: no alert for a 2 s wet blip or a flickering sensor, alert after 3 s, mute, re-ring after mute, clears after dry. Not verified: plate corrosion (use gold-plated or carbon traces), cable length effect.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`rain_*`), demo build `firmware/release/rain_alert.hex`. Nano pins: rain A0, mute D2, buzzer D9 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. The rev B PCB is laid out (see below). The hex above is the **Nano bench demo**; firmware for the custom board is `firmware/src/main_board.cpp` (Seeti: `seeti_prod.cpp`), built by `make boards`, hex in `firmware/release/<clock>/boards/` - compiled but not yet run on hardware.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×45×24 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Wet the plate with a drop of water for 4 s: alert; dry: clears after 2 min.

## PCB (rev B, engineering release)
See `../pcb/README.md`; files in `../pcb/release/rain/`.

## Prototype budget (Rs 780, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| Rain sensor board | 80 |
| Buzzer, button | 60 |
| Cable | 50 |
| Wires, box | 150 |
| Battery holder | 40 |
| **Total** | **780** |

## Designed production BOM (~2,000 units, estimate Rs 240)
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

## Economics (marketplace, GST 18 % assumed)
Price Rs 899 → contribution Rs 271 (36%); BOM +30 %: Rs 187 (24%). The first-draft price was Rs 649, which made too little margin, so it was raised.

## Manufacturing
Rain plate: ENIG-finished PCB (gold) to survive corrosion; indoor unit in ABS.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Corrosion; smart-home rain alerts compete but need WiFi/apps.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
