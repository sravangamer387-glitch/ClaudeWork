# Kalakriti Automata Kits: manufacturing manual (4 laser-cut mechanical kits)

> **Status: parts geometry is verified by calculation and by independent geometry tests; the frame layouts are provisional, the artwork is placeholder, nothing has been cut or assembled.** The first job is a cardboard mock-up, not a production run.

## 1. What is made
| Kit | Mechanism | File |
|---|---|---|
| Dancing Peacock | cam + roller follower, 12 mm lift | `products/02-automata/out/peacock_parts_sheet.svg` |
| Modak Ganesh | long-stroke cam, 25 mm lift | `.../ganesh_parts_sheet.svg` |
| Diya Wheel | 18:54 spur gear train (module 2) | `.../diya_parts_sheet.svg` |
| Bullock Cart | crank-slider + wheel rocker | `.../bullock_parts_sheet.svg` |

Each sheet is 400 mm wide and up to 250 mm tall (1.7-2.4 m of cut path, 2-3 minutes of laser time per kit, assuming 15 mm/s on 3 mm MDF). Design report: `products/02-automata/out/design_report.md`; generator: `src/automata.py`, check: `src/verify_geometry.py`.

## 2. Materials and hardware (per kit)
- 3 mm **E1-grade MDF** (formaldehyde class) sheets; measure real thickness (3.0 +-0.2 mm assumed).
- 4 mm dowel (crank shaft) and 6 mm dowel (cam follower), 2 small bearings or smooth holes, rubber band or string, PVA wood glue, water-based paint or lacquer, crank knob, sandpaper.
- Cost about Rs 220 per kit at volume (guess); prototype set about Rs 940.

## 3. Steps to a first working set
1. **Cardboard mock-up** of every kit at 1:1 from a printed SVG: check shaft heights, cam clearance, follower travel. Record changes (the frame positions are provisional).
2. **Kerf test:** cut a coupon with a 6 mm hole and a 4 mm slot in the real 3 mm MDF; measure. Adjust the laser kerf offset (0.2 mm assumed) until a 6 mm dowel is a sliding fit and a 4 mm dowel a snug fit.
3. Cut the four sheets (engrave first, then cut). Check the cam profile: it must sit exactly one roller radius (+ half kerf) from the pitch curve all around.
4. Sand edges (240 grit). Remove charring with a damp cloth.
5. Assemble per kit (outline from the product README, to be refined after the mock-up):
   - sand edges, glue base and side frames, check squareness;
   - fit shaft and cam (use a flat on the dowel or glue the cam), keep the follower guide free;
   - fit the follower dowel in its guide, attach the figure (peacock fan / Ganesh arm / ox head / cart);
   - add the crank and knob, fit a **cover plate over the gears** (finger-pinch protection);
   - test: the mechanism must turn freely with one finger; no chatter up to 120 rpm (limits: about 160 rpm for the peacock cam and 140 rpm for Ganesh before the follower can leave the cam).
6. Paint with water-based paint; cure 24 h.

## 4. Artwork and instructions still missing
- Illustrator to finish the peacock fan, Ganesh and ox silhouettes (placeholders now).
- Exploded drawings and a step-by-step leaflet in English/Hindi/Telugu (the outline above is the text source).
- Actual crank torque and friction are unmeasured; test with a child.

## 5. Quality checks per kit
Parts count matches the sheet; all slots fit without force; cam rotates without binding; follower returns by gravity at 60-120 rpm; no sharp edges; no finger-trap near gears; crank force by hand estimated under 5 N (measure with a spring scale).

## 6. Packaging and compliance
Labels: 8+, small parts, "not a toy for under 3", Legal Metrology marks. Verify with a lab: Toys QCO/IS 9873 scope, MDF formaldehyde grade (E1/E0), heavy-metal report for paint. Sell as single kits (Rs 899) or a 4-kit gift set (Rs 2,999).

## 7. Ordering laser cutting
RFQ to three laser shops: the SVGs, material 3 mm E1 MDF, kerf 0.2 mm, tolerance +-0.2 mm, packing, price per kit at 100/500/1,000.

## 8. Known limits
Frame layouts provisional; artwork placeholder; friction/torque not measured; laser kerf and MDF thickness tolerance unverified on your machine.
