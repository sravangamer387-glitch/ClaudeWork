# Product 2 · Kalakriti Automata Kits

Four hand-cranked, laser-cut mechanical toys for ages 8+. No electronics, no batteries. Status: **mechanism geometry designed and verified by simulation and independent geometry tests; frame layouts are provisional; artwork is placeholder; nothing has been cut or assembled.**

## 1. The kits
| Kit | Mechanism | What moves | Verified numbers |
|---|---|---|---|
| **Dancing Peacock** | cam and roller follower | tail fan lifts 12 mm and dwells | base circle 11 mm, max pressure angle 29.5°, no undercut |
| **Modak Ganesh** | cam and follower with long stroke | hand lifts a modak 25 mm to the mouth, dwells | base circle 18.5 mm, pressure angle 30.0°, no undercut |
| **Diya Wheel** | 18:54 spur gear train (module 2) | decorative platform turns 1 per 3 crank turns | contact ratio 1.65, no undercut, no tooth interference |
| **Bullock Cart** | crank-slider (10 mm crank, 45 mm rod) + wheel rocker | ox head nods 20 mm, cart rocks | max rod angle 12.8° |

## 2. Verification (`out/design_report.md`, `src/automata.py`, `src/verify_geometry.py`)
- **Cams:** cycloidal rise/fall (zero velocity and acceleration at the ends, so no jerk) with the **smallest base circle that keeps the pressure angle ≤ 30° and avoids undercutting**; at 120 rpm the follower acceleration is 2.7 and 3.6 m/s², under 0.5 g, so a gravity-return follower stays on the cam (limit about 160 and 140 rpm: a child cranking faster may make it chatter).
- **Independent cam check:** the cut profile sits exactly one roller radius (+ half the laser kerf) from the pitch curve all the way round.
- **Gears:** a **bug was found by the interference test, not by the formulas**: my first involute tooth widened toward the tip, so meshing teeth overlapped by 6 mm² (a contact-ratio formula passed anyway). After fixing the sign the two gears, rasterised through a full turn, overlap by only 0.11 mm² (pixel noise).
- **Laser sheets:** four 400 mm-wide sheets (each ≤ 250 mm tall), 1.7–2.4 m of cut path, about 2–3 minutes of laser time per kit (assumed 15 mm/s on 3 mm MDF).

## 3. What is NOT done
1. **Assembly CAD:** frame, shaft heights and guide positions are provisional starting layouts; build a cardboard mock-up first and adjust.
2. **Artwork:** the peacock fan, Ganesh and ox are simple placeholders; an illustrator should finish the silhouettes.
3. **Real friction and crank torque** (idealised kinematics only), kerf and MDF thickness tolerance (test 3 mm ±0.2 on your laser).
4. **Instructions:** exploded drawings and step-by-step manual (outline below).

## 4. Parts and assembly outline (per kit)
Laser parts (3 mm MDF, from `out/<kit>_parts_sheet.svg`) plus hardware: 4 mm dowel for the crank shaft, 6 mm dowel for cam followers, 2 small bearings or smooth holes, rubber band or string, wood glue, paint. Steps: sand edges → glue base and side frames → fit shaft and cam (keep a flat or glue) → fit follower in guide → attach figure → add crank → test turning by hand (should turn freely with one finger).
Safety: no exposed pinch points near gears (add a cover plate), age 8+, small-parts warning, sanded edges.

## 5. Prototype (about Rs 940)
MDF 3 mm 600 x 450 sheet Rs 200 · laser cutting 4 sheets Rs 300 · dowels Rs 60 · paint/brushes Rs 200 · glue, sandpaper Rs 100 · string/rubber bands Rs 40 · crank knobs Rs 40 = **Rs 940** (estimates).

## 6. Economics (marketplace; GST 5 % assumed – verify)
Price Rs 899, BOM guess Rs 220 (laser, MDF, hardware, pack, assembly), contribution about Rs 377 = **44 %**, 35 % if BOM +30 %. Sell as a 4-kit gift set at Rs 2,999. Fixed launch costs about Rs 1.5 lakh (artwork, laser jigs, testing, photography; assumption).

## 7. Compliance and RFQ
- Toys QCO/IS 9873 scope and **MDF formaldehyde grade (E1/E0)**; paint/lacquer heavy-metal report; age grade and small-parts warnings; Legal Metrology.
- RFQ to 3 Hyderabad laser shops with the SVGs: material 3 mm E1 MDF, kerf 0.2, tolerance ±0.2, packing, price per kit at 100/500/1,000.

## 8. Listing copy draft
"Kalakriti Automata – Build a Dancing Peacock | Hand-Crank Wooden Mechanical Model Kit | Ages 8+": build and learn cams, gears and cranks; no electronics; laser-cut; gift-ready. Do not claim STEM outcomes without evidence.

## 9. Risks
Assembly frustration (instructions and mock-up tests), laser tolerance, cheap imported wooden puzzles, artwork quality, child finger-pinch hazards.

## 10. Next steps
Cardboard mock-up → fix frame layouts → illustrator → cut one set → 5-child assembly test → RFQ.
