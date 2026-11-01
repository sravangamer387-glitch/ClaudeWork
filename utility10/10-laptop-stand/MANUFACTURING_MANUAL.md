# Laptop Stand (fold-flat, three angles): manufacturing manual

> **Status: design only.** Nothing has been cut or assembled. The geometry has been checked by calculation (fit, bending, tipping) but not by building it.

**What it is.** Laser-cut 6 mm plate on a base with a notched strut for three angles (12°, 18°, 25°). Fold-flat for travel.

## 1. Deliverables

| Deliverable | Where |
|---|---|
| Cutting files | `utility10/out/laptop_stand.svg` and `utility10/out/laptop_stand.dxf` (CUT layer through, ENGRAVE layer marks; mm, 1:1) |
| Design checks | `utility10/docs/results_stand.md` |
| Test sheet | `manuals/templates/eol_test_sheet.md` |

## 2. Materials, tools and bought-in items

- Sheet: **6 mm** plywood (BWP) or bamboo for stiffness; MDF is acceptable only for prototypes; cutting area **600 x 600 mm**.
- Tools: caliper, try square, clamps, sandpaper (120/240), brush, PVA glue (D3), water-based polyurethane or paint, rubber/felt feet.
- Cost per unit (about 2,000 units, estimate; replace with quotes):

| Item | Rs |
|---|---|
| MDF/ply 6 mm | 90 |
| Laser cutting | 70 |
| Rubber feet ×4 | 15 |
| Hinge/tape | 30 |
| Packaging | 40 |
| Assembly | 25 |

## 3. Parts in the file

- plate
- base
- notched strut for three angles (12, 18, 25 degrees)
- hinge (2 mm piano hinge, or cloth tape for a prototype)

Joint rule: strut slots sized for the 6 mm sheet; verify with a test coupon.

## 4. Making it (step by step)

1. Measure the real sheet thickness; plywood often measures 5.6-6.2 mm. Adjust slot widths accordingly.
2. Cut a test coupon with one notch and a 6 mm tab; the strut must fit with a light press.
3. Cut the sheet (parts nest on one 600 x 600 mm sheet). Engrave first, cuts second.
4. Sand, break edges, seal with water-based paint or lacquer, cure 24 h.
5. Fit the hinge between plate and base (pilot holes, M2 or No. 4 screws) or use cloth tape for a prototype; fit four rubber feet (about 10 mm diameter) under the base.
6. Check that all three strut notches engage and the stand folds flat.

## 5. Inspection and test (every unit / sample)

- Place a 2.5 kg laptop on each of the three angles; type on it: no rocking, plate deflection visually under 1 mm (calculated 0.64 mm).
- Push test: a firm 15 N sideways shove can slide the stand and nearly tips it at 25 degrees (honest limit in the design): state 'do not use as a desk shelf' and test your rubber feet's friction.
- Hinge check: 50 open/close cycles without loosening.

Record on `manuals/templates/eol_test_sheet.md`.

## 6. Packaging and labelling

Flat-pack carton with edge protectors, assembly leaflet (pictorial), care instructions (wipe with a damp cloth, no soaking), Legal Metrology marks (STANDARD_PROCEDURES K).

## 7. Ordering from a laser shop (RFQ)

Send the DXF + this manual. Ask for: price at 500/1,000/2,000 units, MOQ, lead time, kerf and tolerance (+-0.2 mm), sample cost, deburr/sand service, packing. Own the files; give the shop only the CUT/ENGRAVE layers.

## 8. Risks and limits

- Cheap aluminium stands cost Rs 300-600; wood is a style choice.
- The hard-shove stability limit above.

Compliance to verify: Finish safety; Legal Metrology labelling.
