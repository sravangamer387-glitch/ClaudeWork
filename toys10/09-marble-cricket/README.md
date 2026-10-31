# 09 · Marble Cricket

*Drop marbles down a pegboard into run pockets, score a wicket or six: tabletop cricket for two.*

**Ages 6+ · Players 2 · Laser-cut MDF/acrylic.** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Each team gets 2 overs (6 marbles each); drop a marble at the top and read the pocket: runs 0–6 or W (wicket).
2. Two wickets end an innings early. Highest total wins; a tie goes to a one-ball super-over.

## Design
Vertical board (300 × 400 mm) with 8 rows of pegs and 9 pockets; levelling screw. Pocket values chosen by search in `sims/sim_cricket.py`.

## What I verified (and what I did not)
`docs/results_cricket.md`: wicket chance per ball 14.5 %, mean 10.0 runs per over (10th–90th percentile 4–16), 2-over match tie rate 4.1 %. Pocket values found by search under rules (centre pockets cheap, 6 only on side pockets). Not verified: real marble bounce (likely biased; a 100-marble calibration test is part of the prototype).

## Prototype budget (Rs 1110, limit Rs 3,000)
| Item | Rs |
|---|---|
| MDF + acrylic front | 450 |
| Laser cutting | 400 |
| Pegs (nails/dowel) | 100 |
| Marbles | 60 |
| Paint, paper | 100 |
| **Total** | **1110** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 262)
| Item | Rs |
|---|---|
| Laser-cut back + front + pockets | 120 |
| Pegs ×55 | 20 |
| Marbles ×10 | 15 |
| Levelling screw + feet | 12 |
| Score pad + box | 55 |
| Assembly | 40 |

## Economics (marketplace; GST 5 % assumed)
Price **Rs 999** → contribution **Rs 412 (43%)**; with BOM +30 %: Rs 320 (34%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).

## Manufacturing
Laser shop; reuse the Galton board peg design from the gravity toys (same geometry).
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; paint/ink heavy-metal report; no licensed names or logos.

## Listing title (draft)
Marble Cricket – Tabletop Cricket Pachinko Game | 2 Players | Ages 6+

## Risks
Peg-board bias; cricket naming/IP (do not use team or league names).

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
