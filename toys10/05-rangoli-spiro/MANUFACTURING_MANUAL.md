# Rangoli Spiro Gears: manufacturing manual

> **Status: design only; nothing has been cut or assembled.**

## 1. What is made

1. Pin the ring to paper, place a wheel gear inside, put a pen in a hole, and turn it round the ring.
2. Different wheel sizes and holes give 3-, 5-, 12- or 32-petal flowers; a printed chart lists the combinations.

## 2. Files and materials

- `toys10/out/spiro_parts.svg` (ring with 96 teeth, 6 wheels of 24-63 teeth, module 2 mm, 8 pen holes per wheel); previews `toys10/out/spiro_previews.png`; checks `toys10/docs/results_spiro.md`

- Material: **3 mm MDF or acrylic**; layout/sheet: see the SVG size.

Cost per set (about 2,000 units, estimate):

| Item | Rs |
|---|---|
| Laser-cut MDF set (ring + 6 wheels) | 70 |
| Pens ×3 | 20 |
| Pins / Blu-tack | 8 |
| Paper pad A4 | 25 |
| Box + insert + chart | 45 |
| Assembly + packing | 25 |

## 3. Making it

Follow `manuals/STANDARD_PROCEDURES.md` section H (laser cutting) for kerf tests and finishing, then:

1. Cut a **kerf test**: 20 mm of gear teeth in the real material; check two teeth mesh without binding or skipping (the risk named in the design is teeth skipping if kerf is large).
2. Cut the sheet, sand, remove char; do not paint gear teeth (paint thickness changes the fit).
3. Pen holes: test that the intended pen fits snugly (hole size unverified).
4. Assemble the set: ring, 6 wheels, 3 pens, pins/Blu-tack, A4 paper pad, printed chart of combinations (3-, 5-, 12- or 32-petal flowers, from `results_spiro.md`).
5. Draw one pattern per wheel/hole pair on the chart and check the petal count against the chart.

## 4. Inspection (sample per batch)

- All wheels mesh with the ring at every position; no skipping while drawing a full pattern.
- Patterns close and have the predicted petals (checked for 8 sampled gear pairs in the simulation).
- No loose fragments; pen holes smooth.

Record on `manuals/templates/eol_test_sheet.md`.

## 5. Packaging and compliance

Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; paint/ink heavy-metal report; no licensed names or logos.

Add the age grade, small-parts warning, Legal Metrology marks and a printed instruction leaflet.

## 6. Risks and limits

- Teeth skipping if the kerf is large.
- Gear counts are original; do not copy Western spirograph product designs or names.

Teeth skipping if kerf is large; copy of Western spirograph designs (we use own gear counts and Indian pattern chart).

`docs/results_spiro.md`: all 8 sampled gear pairs close after the predicted wheel turns, have the predicted petal count and stay inside the ring. A first petal-counting method was wrong (my checker, not the design) and was replaced by a mid-radius crossing count. Not verified: tooth fit/kerf on a real laser, pen-hole size.
