# Gravity toys (5): manufacturing manual

> **Status: designs with calculations and 2D starting files; nothing built.** Vendor names are unverified directory/background leads; costs and mould prices are planning assumptions. The prototype build recipes already exist in `prototypes/guides/gravity-prototypes.md` (cut lists, groove build, tests); this manual consolidates what to make, in what order, with which files and which acceptance tests, and lists exactly what is still missing.

## 1. Launch order and status
| # | Toy | Files that exist | Missing before production |
|---|---|---|---|
| 3 | Galton Board Plinko Lab (6+) | `gravity-toys/cad/out/galton_back_mdf.svg`, `galton_front_acrylic.svg` | assembly guide, teacher guide, 500-ball data sheet, test reports |
| 4 | Santulan balance set (3+) | `cad/out/santulan_wing.svg` | CoG worksheet, **lathe drawings for the turned bird**, paint-pattern guide, artisan training sheet |
| 1 | Timber Tower Marble Run (4+) | `cad/out/marble_tower_plate.svg` | CNC groove toolpath, lathe drawings (balls, posts), challenge cards, leaflet, dieline |
| 5 | Ramp Racers Physics Lab (5+) | `cad/out/ramp_racer_ramp.svg` | car/wheel/axle drawings, ladder stand, experiment workbook, teacher guide |
| 2 | Drop Quest (8+) | none (v0 build description only) | puzzle solver and 60 verified levels, tower/tube CAD, mould design (v2) |

Regenerate cut files: `python3 -I gravity-toys/cad/generate_laser_svgs.py gravity-toys/cad/out` (asserts guard the ball-clearance rules). Physics checks: `gravity-toys/sim/verify_designs.py` (it corrected three designs: ramps 6-8 degrees not 8-12; balancing-bird weights about 95 mm forward of the beak; felt wheels need 10 degrees or more).

## 2. Per-toy build specification
**3. Galton Board:** back 300 x 400 class MDF panel and acrylic front per the SVGs; pegs and steel balls (warning label; the back gate must close so balls cannot fall out in use); sand and polish acrylic edges, sealed screw heads. Landed cost about Rs 480 (acrylic 160, MDF 70, pins/balls 90, laser 60, assembly 45, box 55). Test: 500-ball drop gives the binomial bell curve within sampling error; no jam (the design has a jam guard).

**4. Santulan balance set:** turned wooden bird, wings from `santulan_wing.svg`, weight screws, perch with R3 mm dimple. **Balance rule: total centre of gravity at least 25 mm below the beak contact point**, computed as sum(m y)/sum(m) from the beak tip, tuned with the weight screws. Cost about Rs 320. Test: every unit balances on the perch and recovers from a 20 degree nudge.

**1. Timber Tower:** 100 x 100 x 10 mm plates on 20 x 20 mm posts with 6 mm pin holes every 50 mm; 28 mm wide x 12 mm deep U-groove (3 mm radius); straight ramps 6-8 degrees (about 4.2 s for the starter route); spiral one turn on 100 mm centreline with 33 mm drop; funnel 90 to 28 mm, 35 degree wall; 25 mm wooden ball (label 4+ with small-parts caution; the 3+ variant needs a 45 mm ball). Cost about Rs 650 landed. Test: 10 runs of the longest route, 3.5-5.5 s, no jams, ball clears the groove by at least 1 mm each side.

**5. Ramp Racers:** 1200 x 140 mm 12 mm birch ply ramp with two 60 mm lanes and 6 mm rails; ladder stand with 5 positions (5/10/15/20/25 degrees, rise 105/208/311/410/507 mm); four cars (body 90 x 45 x 30 mm, wheels 30 mm, 3 mm steel axle in brass bush; wheel variants hard wood, rubber, felt, plastic); weight slots 20/40/60 g with captive screw cover; cork stop block. Cost about Rs 730 landed. Tests: wheel/axle pull test, no pinch point at the ladder hinge (cam-lock), edges R2 mm or more, run times against the simulation table (e.g. 1.26/1.35/1.61 s at 10 degrees for hard/rubber/felt).

**2. Drop Quest:** do not manufacture yet: the solver and levels do not exist and v2 needs a mould (Rs 12-20 lakh assumed) plus an IP/patent review.

## 3. Procedures
Laser parts: `manuals/STANDARD_PROCEDURES.md` H. Wood turning/painting: artisan workshop with a trained operator; finish with lacquer that passes IS 9873 Part 3 (non-toxic). Inspection per batch: dimensions against the drawing (+-0.5 mm), small-part cylinder test (31.7 mm cylinder: confirm the figure in IS 9873), edge/point check, pull test on every wheel/axle, pinch-point check.

## 4. Ordering
Use `gravity-toys/business/02-manufacturer-rfq-pack.md` (RFQ email, vendor scorecard, product annexes, QC checklist). Do a factory visit and sample test before committing; no Hyderabad toy-test lab or 3D-print bureau was found in research.

## 5. Compliance and limits
IS 9873 (Part 1:2025 and others), EN 71, ASTM F963: confirm clauses (small-part cylinder, ball exemption, magnets) in the current standards; label age grade; Legal Metrology marks. The unit-economics file shows original retail prices lose money on Amazon: use the prices in the business plan.
