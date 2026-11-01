# Tilt Maze Labyrinth: manufacturing manual

> **Status: design only; nothing has been cut or assembled.**

## 1. What is made

1. Turn two side knobs to tilt the maze; roll the marble from start to goal without falling in the trap holes.
2. Three interchangeable maze plates (9×9, 13×13, 17×17); race a friend by timing.

## 2. Files and materials

- Maze plates: `toys10/out/maze_easy.svg` (9x9), `maze_medium.svg` (13x13), `maze_hard.svg` (17x17): perfect mazes, trap holes on dead ends only, 19 mm corridors for a 12 mm marble; checks `toys10/docs/results_maze.md`
- **Gimbal frame and knobs: no drawing exists yet** (outer frame, inner tilt frame, two knobs, bearings): it must be designed before production. The parts list in section 2 is the intended content.

- Material: **3 mm MDF or acrylic (plates with glued 3 mm walls)**; layout/sheet: per SVG.

Cost per set (about 2,000 units, estimate):

| Item | Rs |
|---|---|
| Laser-cut frame + 3 plates | 110 |
| Wall strips | 25 |
| Knobs + dowels + bearings | 40 |
| Marbles ×3 | 10 |
| Box | 45 |
| Assembly | 30 |

## 3. Making it

Follow `manuals/STANDARD_PROCEDURES.md` section H (laser cutting) for kerf tests and finishing, then:

1. Cut the three plates; glue the 3 mm wall strips to the plates along the maze lines (PVA, clamp, wipe squeeze-out; corridors must stay 19 mm wide: check with a 12 mm marble).
2. **Design and cut the gimbal frame** (not available): outer frame on a stand, inner frame carrying the interchangeable plate, two side knobs on 6 mm dowels; make a cardboard mock-up first and record tilt range and friction.
3. Fit marbles (12 mm or larger: choking hazard, age 7+), check that no marble can jam in a trap hole.
4. Sand, seal, assemble knobs and bearings.

## 4. Inspection (sample per batch)

- Every plate: marble can reach the goal; traps only on dead ends (verified by BFS in the design).
- Knobs tilt the board smoothly; marble rolls without sticking.
- Marble choking-hazard label present (age 7+).

Record on `manuals/templates/eol_test_sheet.md`.

## 5. Packaging and compliance

Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; paint/ink heavy-metal report; no licensed names or logos.

Add the age grade, small-parts warning, Legal Metrology marks and a printed instruction leaflet.

## 6. Risks and limits

- Tilt feel and friction not tested.
- Marble choking hazard: marble 12 mm or larger, 7+ label.

Marble is a choking hazard: use age 7+ labelling and a marble ≥ 12 mm.

`docs/results_maze.md`: all three mazes are perfect (one solution, BFS-checked); trap holes sit on dead ends only, so no hole blocks the solution; corridor 19 mm for a 12 mm marble. Not tested: tilt feel and friction.
