# 01 · Reflex Raja

*Four giant buttons, one hidden random timer: who is quickest when the light and buzzer say GO?*

**Ages 6+ · Players 2–4 · Electronic (low voltage, battery).** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Anyone presses a button to start a round. After a hidden random 2–6 s all four lamps light and the buzzer sounds.
2. First player to press wins a point. Pressing early loses a point and locks you out for that round. Two presses in the same millisecond is a tie (replay).
3. First to 5 points wins; the lamp of the round winner stays lit.

## Design
Nano-class MCU, 4 arcade-style buttons, 4 LEDs, buzzer, 3 × AAA. Engine: `electronic/lib/toycore.c` (`rr_*`).

## What I verified (and what I did not)
Host tests: false-start penalty and lock-out, locked player cannot win, tie handling, all-false-start voids the round, delay always 2.0–6.0 s with mean 4.0 s, equal players win equally often (±12 % in 4,000 simulated rounds), 800 ms debounce. Nano demo `electronic/release/reflex_raja.hex` (3.9 KB).

## Prototype budget (Rs 1090, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| 4 push buttons (large) | 100 |
| 4 LEDs + resistors | 40 |
| Buzzer | 30 |
| Breadboard + wires | 250 |
| AAA holder + cells | 120 |
| Cardboard / printed box | 150 |
| **Total** | **1090** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 310)
| Item | Rs |
|---|---|
| MCU + crystal | 55 |
| PCB 2-layer | 30 |
| 4 arcade buttons 30 mm | 60 |
| 4 LEDs + resistors | 10 |
| Buzzer | 12 |
| 3×AAA holder + switch | 18 |
| Enclosure (injection, amortised) | 55 |
| Packaging + manual (3 languages) | 30 |
| Assembly + test | 40 |

## Economics (marketplace; GST 18 % assumed)
Price **Rs 999** → contribution **Rs 263 (31%)**; with BOM +30 %: Rs 155 (18%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).
First-draft price Rs 699 lost or barely made money, so it was raised.

## Manufacturing
PCBA at a Hyderabad EMS; ABS injection housing or (for the first 500) 3D-printed/laser-cut MDF housing; button caps from stock arcade buttons.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

## Listing title (draft)
Reflex Raja – 4-Player Reaction Game | Light & Buzzer Party Game | Ages 6+

## Risks
Button wear, 'toy electronics' certification (battery + BIS toy electrics), cheap imported reaction toys.

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
