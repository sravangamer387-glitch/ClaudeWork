# Build guide · Gravity toy prototypes (G1–G5)

Cut files come from `gravity-toys/cad/generate_laser_svgs.py` (SVG: red = cut, blue = engrave). The physics targets below come from `gravity-toys/sim/verify_designs.py`. Costs are in `prototypes/budget/prototype_budgets.md`.

## G1 Timber Tower Marble Run (MDF prototype, about Rs 1,000)
- **Cut:** `marble_tower_plate.svg` x 8 on 6 mm MDF; 6 posts 20 x 20 x 240 mm from pine strip with 6 mm pin holes every 50 mm.
- **Groove:** the design groove is **28 mm wide x 12 mm deep**. For the MDF prototype skip routing: glue two 6 mm MDF strips to each plate with a 28 mm gap between them (and a 6 mm strip under for depth) so the ball runs in a channel; the SVG engrave line marks the channel centre.
- **Ramps at 6–8°**, not 10°+: simulation shows the full starter route takes about 4.2 s at 6° (with see-saw, funnel and bell) but only 3.5 s at 10°.
- **Spiral:** 1 turn on a 100 mm centreline with about 33 mm drop per turn.
- **Test:** time 10 runs of the longest route. Pass: 3.5–5.5 s, no jams, ball never leaves the groove, chime rings. Check the ball (25 mm) clears the groove with ≥ 1 mm each side.

## G2 Drop Quest v0 (about Rs 700)
- 5 x 5 grid base (230 x 230 mm), towers of heights 1, 2, 3 units (20 mm each) with a 16 mm bore, tubes with 17 mm bore, 14 mm marble.
- **Test:** 5 children (age 8+) try 10 hand-written puzzles; note puzzles that nobody solves in 5 minutes and any marble jams (bore 16.5/17/17.5 mm test). The puzzle solver is **not yet written**: it is the next engineering task for this toy.

## G3 Galton Board (about Rs 1,430)
- **Cut:** `galton_back_mdf.svg` (peg holes) and `galton_front_acrylic.svg`; press 55 pegs (O4 x 55 mm) into the back, 6 mm protruding.
- **Test:** drop 100 balls and count bins. Ideal fractions for 10 rows: 0.1 %, 1.0 %, 4.4 %, 11.7 %, 20.5 %, 24.6 %, 20.5 %, 11.7 %, 4.4 %, 1.0 %, 0.1 %. With 100 balls expect the middle three bins to hold about 65 %; with 300+ balls the shape is smooth. **No jams** (gap 20 mm = 1.67 x ball).

## G4 Santulan balance set (about Rs 1,280)
- **Bird:** turned body 160 mm; wings `santulan_wing.svg` x 2 (3 mm ply) **swept forward so the weights sit about 95 mm in front of the beak tip and 90 mm below the beak line**; two 20 g lead-free weights on adjustable screws.
- **Trim:** balance the bird on a 3 mm dimple on your fingertip; move the weights until it stays level for 60 s; expect 5 mm of weight error to tilt it about 3°. Rocking period after a nudge should be about 1 s.
- **Roly-poly:** 60 g steel slug low in the base; **pass = self-rights 10 out of 10 times from 90° tilt**.
- **Test the paint** with a lead test kit or lab report before any child touches it.

## G5 Ramp Racers (about Rs 1,570)
- Ramp 1200 x 140 mm (`ramp_racer_ramp.svg`), stand with positions for 5°, 10°, 15°, 20°, 25° (rise = 105, 208, 311, 410, 507 mm).
- **Test:** time each car over 1.2 m, three runs each. Expected (simulation): at 10° hard wood 1.26 s, rubber 1.35 s, felt 1.61 s; at 25° about 0.8 s. **Felt wheels barely move at 5°** (5.7 s), so use ≥ 10°. Weights of 20/40/60 g should NOT change the time (within a few percent).

## Common safety checks before kids play
Sand all edges (R ≥ 2 mm), no splinters, balls and small parts labelled with age warnings, no lead in paint or weights, nothing that pinches fingers at hinges.
