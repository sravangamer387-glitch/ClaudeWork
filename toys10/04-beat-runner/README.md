# 04 · Beat Runner

*A 16-LED strip of falling notes; hit one big button exactly when a note reaches the end.*

**Ages 7+ · Players 1–2 · Electronic (low voltage, battery).** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Notes spawn at the far end and scroll toward LED 0, getting faster every 40 steps (400 ms → 150 ms).
2. Press when a note is on LED 0 (perfect, 3 points) or LED 1 (good, 1 point). Combos multiply score; 5 misses end the game.
3. Two players alternate; highest score wins.

## Design
Two 74HC595 shift registers drive 16 LEDs, one arcade button, buzzer. Engine `br_*`.

## What I verified (and what I did not)
Host tests: scoring windows, a perfect player never loses over 500+ notes, an idle player loses after 5 misses, speed-up bounded to 150 ms.

## Prototype budget (Rs 1140, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| 2 × 74HC595 | 60 |
| 16 LEDs + resistors | 120 |
| Button, buzzer | 60 |
| Breadboard, wires | 250 |
| USB power bank cable | 100 |
| Box | 150 |
| **Total** | **1140** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 326)
| Item | Rs |
|---|---|
| MCU + crystal | 55 |
| PCB | 35 |
| 2 × 74HC595 | 14 |
| 16 LEDs + resistor arrays | 30 |
| Arcade button | 15 |
| Buzzer | 12 |
| Battery/USB power | 30 |
| Enclosure | 60 |
| Packaging + manual | 30 |
| Assembly + test | 45 |

## Economics (marketplace; GST 18 % assumed)
Price **Rs 1299** → contribution **Rs 365 (33%)**; with BOM +30 %: Rs 251 (23%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).
First-draft price Rs 799 lost or barely made money, so it was raised.

## Manufacturing
Same EMS as above; LED lens strip from laser-cut diffusing acrylic.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

## Listing title (draft)
Beat Runner – 16-LED Rhythm Reflex Game | Ages 7+

## Risks
Perceived value vs mobile games; keep price ≤ Rs 799.

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
