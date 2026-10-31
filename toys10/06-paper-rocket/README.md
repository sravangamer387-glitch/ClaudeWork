# 06 · Paper Rocket Air Launcher

*Pump the chamber, pull the trigger, send a rolled-paper rocket across the garden.*

**Ages 8+ · Players 1+ · Plumbing/pneumatic (pressure-tested).** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**

## How it plays
1. Roll and tape a paper rocket (templates included), pump the chamber until the relief valve hisses, aim at the sky (never at people), release.
2. Compete for distance; adjust the launch angle (about 40°) and nose weight.

## Design
PVC chamber and 19 mm barrel, bicycle-pump connector, spring relief valve set at about 0.3 bar gauge, rocket tube of rolled paper with foam nose. `sims/sim_rocket.py`.

## What I verified (and what I did not)
`docs/results_rocket.md`: with a relief valve at about 0.29 bar the launch energy is 0.5 J, range about 16 m at 42° (estimate). **The first draft with a 1 bar valve gave 2.8 J, five times my placeholder energy limit; the design was changed to the low-pressure valve.** Nothing measured: the loss factor and drag are guesses. The legal energy limit must be taken from the toy standard (not verified).

## Prototype budget (Rs 1100, limit Rs 3,000)
| Item | Rs |
|---|---|
| PVC pipe, caps, glue | 350 |
| Bicycle pump (reuse) / hand pump | 250 |
| Valves | 300 |
| Paper, foam | 80 |
| Tools / tape | 120 |
| **Total** | **1100** |

(Local-market estimates; verify with quotes.)

## Designed production BOM (~2,000 units, estimate: Rs 310)
| Item | Rs |
|---|---|
| PVC chamber + barrel + fittings | 90 |
| Bike-pump connector/valve | 45 |
| Relief valve (spring) | 40 |
| Trigger valve | 35 |
| Paper rocket pack + foam noses | 25 |
| Box + manual | 40 |
| Assembly + leak test | 35 |

## Economics (marketplace; GST 5 % assumed)
Price **Rs 799** → contribution **Rs 188 (25%)**; with BOM +30 %: Rs 80 (10%). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).

## Manufacturing
Plumbing parts assembled and pressure-tested (1.5 × relief pressure) at a small workshop; 100 % leak test.
RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; paint/ink heavy-metal report; no licensed names or logos.

## Listing title (draft)
Paper Rocket Air Launcher – Pump Launch Toy | 8+ (adult supervision)

## Risks
Projectile safety is the whole risk: eye injuries, misuse. Needs a design review against the toy standard, a pressure-vessel safety margin, and a clear 'never aim at people' label. Consider selling only after a lab review.

## Next steps
Build the prototype from the budget above → test with 5 children → adjust → RFQ.
