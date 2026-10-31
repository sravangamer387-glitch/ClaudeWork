# 07 · Tilt Maze Labyrinth

*Two knobs tilt a wooden board: guide the marble through a maze and around the trap holes.*

**Ages 7+ · Players 1–2 · Laser-cut MDF/acrylic.** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Turn two side knobs to tilt the maze; roll the marble from start to goal without falling in the trap holes.
2. Three interchangeable maze plates (9×9, 13×13, 17×17); race a friend by timing.

## Design
Gimbal frame with two knobs, replaceable laser-cut maze plates with glued 3 mm walls. `sims/sim_maze.py` → `out/maze_{easy,medium,hard}.svg`.

## What I verified (and what I did not)
`docs/results_maze.md`: all three mazes are perfect (one solution, BFS-checked); trap holes sit on dead ends only, so no hole blocks the solution; corridor 19 mm for a 12 mm marble. Not tested: tilt feel and friction.

## Prototype budget (Rs 950, limit Rs 3,000)
| Item | Rs |
|---|---|
| MDF sheet | 250 |
| Laser cutting | 400 |
| Dowels, knobs, glue | 150 |
| Marbles | 50 |
| Paint / sandpaper | 100 |
| **Total** | **950** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 260)
| Item | Rs |
|---|---|
| Laser-cut frame + 3 plates | 110 |
| Wall strips | 25 |
| Knobs + dowels + bearings | 40 |
| Marbles ×3 | 10 |
| Box | 45 |
| Assembly | 30 |

## Economics (marketplace; GST 5 % assumed)
Price **Rs 799** → contribution **Rs 246 (32%)**; with BOM +30 %: Rs 155 (20%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).

## Manufacturing
Laser shop + assembly in-house; reuse automata laser relationship.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; paint/ink heavy-metal report; no licensed names or logos.

## Listing title (draft)
Tilt Maze Labyrinth – Wooden Marble Maze with 3 Levels | Ages 7+

## Risks
Marble is a choking hazard: use age 7+ labelling and a marble ≥ 12 mm.

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
