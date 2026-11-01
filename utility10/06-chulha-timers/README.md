# 06 · Chulha Timers (4 kitchen timers)

**Tier B** · low-voltage electronics · prototype Rs 970 · price Rs 1199. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Indian cooking runs several dishes at once; phone timers share one alarm sound and are buried in menus.

## How it works
Four buttons = four channels. Tap adds one minute, hold 1 s clears. Each channel rings separately; the display shows the soonest. Magnet back sticks to the fridge or hood.

## What I verified (and what I did not)
Host tests: independent channels, acknowledge only one, add/subtract with floor at zero, 99-minute cap, wrap-safe. Not verified: display ergonomics and buzzer loudness.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`ct_*`), demo build `firmware/release/chulha_timers.hex`. Nano pins: buttons D2-D5, buzzer D9 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. The rev B PCB is laid out (see below). The hex above is the **Nano bench demo**; firmware for the custom board is `firmware/src/main_board.cpp` (Seeti: `seeti_prod.cpp`), built by `make boards`, hex in `firmware/release/<clock>/boards/` - compiled but not yet run on hardware.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (100×55×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Set 1:00 on each channel, check four independent rings within ±1 s.

## PCB (rev B, engineering release)
See `../pcb/README.md`; files in `../pcb/release/chulha/`.

## Prototype budget (Rs 970, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| 8-digit display | 180 |
| 4 buttons | 60 |
| Buzzer | 30 |
| Wires, box | 200 |
| Power bank cable | 100 |
| **Total** | **970** |

## Designed production BOM (~2,000 units, estimate Rs 362)
| Item | Rs |
|---|---|
| MCU | 45 |
| 8-digit display module | 70 |
| 4 buttons + caps | 25 |
| Buzzer | 12 |
| Magnet back | 30 |
| Battery/USB | 30 |
| PCB | 30 |
| Enclosure | 50 |
| Packaging | 30 |
| Assembly + test | 40 |

## Economics (marketplace, GST 18 % assumed)
Price Rs 1199 → contribution Rs 256 (25%); BOM +30 %: Rs 129 (13%). The first-draft price was Rs 899, which made too little margin, so it was raised.

## Manufacturing
EMS PCBA, ABS case, magnet over-moulded or glued.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Cheap multi-timers exist (₹250–500): compete on loudness, clarity and Indian packaging.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
