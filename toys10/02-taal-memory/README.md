# 02 · Taal Memory

*Repeat the growing tune on four colour pads, each with its own note.*

**Ages 5+ · Players 1–4 · Electronic (low voltage, battery).** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. The toy plays a note sequence (one note, then two, then three...). Repeat it on the pads.
2. A wrong pad ends the game; the longest sequence you remembered flashes as your score.
3. Players take turns; highest score wins. A seed is read from analog noise so every game differs but a replay inside a game is exact.

## Design
Same hardware as Reflex Raja with pad colours. Engine `tm_*` regenerates the sequence from its seed rather than storing it (RAM-free).

## What I verified (and what I did not)
Host tests: correct note advances, round completion grows the sequence, wrong note ends and records best, a perfect player reaches 60 notes, all four pads are used, the sequence is repeatable. Nano demo `taal_memory.hex`.

## Prototype budget (Rs 1070, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| 4 push buttons | 80 |
| LEDs, resistors | 40 |
| Buzzer | 30 |
| Breadboard, wires | 250 |
| Battery holder + cells | 120 |
| Box | 150 |
| **Total** | **1070** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 310)
| Item | Rs |
|---|---|
| MCU + crystal | 55 |
| PCB | 30 |
| 4 coloured pads (dome buttons) | 60 |
| 4 LEDs + resistors | 10 |
| Piezo buzzer | 12 |
| Battery holder + switch | 18 |
| Enclosure | 55 |
| Packaging + manual | 30 |
| Assembly + test | 40 |

## Economics (marketplace; GST 18 % assumed)
Price **Rs 899** → contribution **Rs 189 (25%)**; with BOM +30 %: Rs 80 (11%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).
First-draft price Rs 599 lost or barely made money, so it was raised.

## Manufacturing
Shares PCB and housing tooling with Reflex Raja (one board, two firmware images) to cut tooling cost.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

## Listing title (draft)
Taal Memory – Musical Memory Game with Lights | Ages 5+ | 1–4 Players

## Risks
Many Simon clones exist; differentiate with Indian instruments (tabla/dholak/flute/veena samples) and a Hindi/Telugu name.

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
