# 03 · Aloo Bomb

*A hot-potato with a hidden fuse: pass it fast, beeps speed up, somebody gets the BOOM.*

**Ages 6+ · Players 3–10 · Electronic (low voltage, battery).** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Press start; the fuse is hidden and random (20–60 s). Beeps every 1 s, then 0.6, 0.3 and 0.12 s in the last 5 s.
2. Pass the potato round the circle. Whoever holds it at the explosion loses a life / does a silly task from the card.

## Design
Squeezable silicone potato shell over a small board; one button, buzzer, 4 LEDs. Engine `ab_*`.

## What I verified (and what I did not)
Host tests: fuse always within the set range with mean 40.0 s, beep tempo bands, explosion exactly at the fuse, millis() wrap-around safe.

## Prototype budget (Rs 940, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| Button, LEDs, buzzer | 90 |
| Breadboard, wires | 250 |
| Battery holder + cells | 100 |
| Cardboard shell | 100 |
| **Total** | **940** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 227)
| Item | Rs |
|---|---|
| MCU (smaller, ATmega-class) | 45 |
| PCB | 25 |
| Button | 8 |
| LEDs + resistors | 8 |
| Buzzer | 12 |
| 2×AAA holder + switch | 14 |
| Silicone shell or ABS potato (amortised) | 50 |
| Packaging + task cards | 30 |
| Assembly + test | 35 |

## Economics (marketplace; GST 18 % assumed)
Price **Rs 699** → contribution **Rs 137 (23%)**; with BOM +30 %: Rs 57 (10%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).
First-draft price Rs 499 lost or barely made money, so it was raised.

## Manufacturing
Silicone over-mould is costly; start with an ABS two-piece housing.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

## Listing title (draft)
Aloo Bomb – Hot Potato Party Game with Random Timer | 3–10 Players

## Risks
Choking/battery-compartment safety (screw-closed battery door is mandatory), noise level of the buzzer (keep ≤ 85 dB at 25 cm; verify).

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
