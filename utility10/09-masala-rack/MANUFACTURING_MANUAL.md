# Masala Rack (12-jar stepped spice rack): manufacturing manual

> **Status: design only.** Nothing has been cut or assembled. The geometry has been checked by calculation (fit, bending, tipping) but not by building it.

**What it is.** Laser-cut 9 mm MDF: two stepped side panels, three shelves with end tabs that pass through the side slots, glue and wipe-clean finish.

## 1. Deliverables

| Deliverable | Where |
|---|---|
| Cutting files | `utility10/out/masala_rack.svg` and `utility10/out/masala_rack.dxf` (CUT layer through, ENGRAVE layer marks; mm, 1:1) |
| Design checks | `utility10/docs/results_rack.md` |
| Test sheet | `manuals/templates/eol_test_sheet.md` |

## 2. Materials, tools and bought-in items

- Sheet: **9 mm** MDF (interior) or BWP/marine plywood or bamboo for kitchens with damp air; cutting area **600 x 450 mm**.
- Tools: caliper, try square, clamps, sandpaper (120/240), brush, PVA glue (D3), water-based polyurethane or paint, rubber/felt feet.
- Cost per unit (about 2,000 units, estimate; replace with quotes):

| Item | Rs |
|---|---|
| MDF 9 mm (0.35 m²) | 110 |
| Laser cutting | 120 |
| Finish (melamine/lacquer) | 40 |
| Packaging | 70 |
| Assembly/glue | 40 |

## 3. Parts in the file

- 2 stepped side panels
- 3 shelves with end tabs that pass through the side slots

Joint rule: 8.95 mm slots for 9 mm board (press fit; the file assumes the laser shop already compensates the 0.2 mm kerf: cut a test coupon first).

## 4. Making it (step by step)

1. Measure the real board thickness with calipers at 4 points. If it is more than 9.1 mm or less than 8.9 mm, scale the slot width in the DXF by the same amount (edit in the CAD tool), do not force parts.
2. Laser-cut one **test coupon**: a 30 x 30 mm square with a 8.95 x 20 mm slot and a tab of the real board; the tab must press-fit with light mallet force. Adjust the shop's kerf offset until it does.
3. Cut the full sheet (nesting 54 % utilisation, no overlaps). Engrave layer first, then through cuts.
4. Remove the char with a dry cloth, sand edges with 240 grit, break sharp edges.
5. Dry-fit the rack without glue: side panels vertical, shelves through the slots; check squareness with a try square.
6. Glue with PVA wood glue (water-resistant D3 for the kitchen) in each slot, clamp or tape for 30 min, wipe squeeze-out immediately.
7. Seal **all edges and faces** with water-based polyurethane or food-safe lacquer, two coats with a light sand between; cure 24 h. MDF edges swell in humidity if unsealed (known risk).
8. Fit four self-adhesive felt or rubber feet if the shelf is to stand on a polished counter.

## 5. Inspection and test (every unit / sample)

- Dimensional check: shelf spacing within +-1 mm of the drawing; the rack stands without rocking on a flat table.
- Load test: place 12 jars (about 1.4 kg on one shelf of 4) for 24 h: sag under 1 mm, no joint opening.
- Jar fit: the design assumes jars of 62 mm diameter and 72 mm depth: measure your jars first (the result file lists the spare space).

Record on `manuals/templates/eol_test_sheet.md`.

## 6. Packaging and labelling

Flat-pack carton with edge protectors, assembly leaflet (pictorial), care instructions (wipe with a damp cloth, no soaking), Legal Metrology marks (STANDARD_PROCEDURES K).

## 7. Ordering from a laser shop (RFQ)

Send the DXF + this manual. Ask for: price at 500/1,000/2,000 units, MOQ, lead time, kerf and tolerance (+-0.2 mm), sample cost, deburr/sand service, packing. Own the files; give the shop only the CUT/ENGRAVE layers.

## 8. Risks and limits

- Weight and fragility in shipping (damage claims): use corner protectors and a double-wall carton.
- MDF swelling in kitchens: seal every edge.
- Creep over months is not modelled: a 6 mm shelf would sag; do not reduce the thickness.

Compliance to verify: Finish/lacquer must be food-safe if jars may touch it; Legal Metrology labelling.
