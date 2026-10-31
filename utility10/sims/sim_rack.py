"""Masala Rack: 3-step spice rack for 12 jars (4 per step), laser-cut MDF with tab-and-slot joints.
Verifies: jar fit per step, shelf deflection under full jars for candidate thicknesses, tab/slot dimensions with kerf, nesting on a 600x450 sheet without overlap."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from cadlib import *
OUT = os.path.join(os.path.dirname(__file__), "..", "out"); DOC = os.path.join(os.path.dirname(__file__), "..", "docs")
JAR_D, JAR_H, JAR_KG = 62.0, 95.0, 0.35            # typical 100 ml round masala jar (assumed), full
W, DEPTH = 290.0, 72.0                             # inside width and shelf depth; 4 jars/row: 4 x 62 = 248 (+ 42 mm gaps)
RISE = 45.0; STEPS = 3                             # each step is 45 mm higher than the one in front so back rows are visible
E_MDF = 2500.0                                     # N/mm2 (assumption, check supplier data)
lines = [f"Jar fit: 4 jars x {JAR_D} mm = {4*JAR_D:.0f} mm in a {W:.0f} mm shelf ({W-4*JAR_D:.0f} mm spare); jar diameter {JAR_D} in depth {DEPTH} mm (spare {DEPTH-JAR_D:.0f} mm). {STEPS*4} jars total."]
res = []
for t in (4.0, 6.0, 9.0):
    load = 4 * JAR_KG * 9.81; w = load / W; I = DEPTH * t ** 3 / 12; d = 5 * w * W ** 4 / (384 * E_MDF * I)
    res.append((t, d, W / d)); lines.append(f"- shelf {t:.0f} mm MDF, 4 full jars ({4*JAR_KG:.1f} kg): deflection {d:.2f} mm = span/{W/d:.0f}" + ("  OK (limit span/300)" if W / d >= 300 else "  too flexible"))
T = next(t for t, d, r in res if r >= 300)
lines.append(f"Chosen thickness {T:.0f} mm (smallest that meets span/300; creep over months is NOT modelled, so a 6 mm shelf would sag over time).")
# geometry: side panels have step profile with slots for shelves
KERF = 0.2; CLEAR = -0.05                        # press-fit: slot = T + CLEAR
slot_w = T + CLEAR; TAB = 40.0                  # shelf end tab length
def side():
    h = JAR_H + 10; pts = []
    # stepped outline: width DEPTH+... simple: profile is three stacked steps of depth DEPTH each, rising RISE
    x = 0; prof = [(0, 0), (0, 10 + RISE * 0)]
    outline = [(0, 0), (DEPTH * 3 + 10, 0), (DEPTH * 3 + 10, RISE * 3 + 20), (DEPTH * 2 + 10, RISE * 3 + 20), (DEPTH * 2 + 10, RISE * 2 + 20), (DEPTH + 10, RISE * 2 + 20), (DEPTH + 10, RISE + 20), (0, RISE + 20)]
    slots = []
    for i in range(STEPS):
        sx = 10 + i * DEPTH + (DEPTH - TAB) / 2; sy = RISE * i + 12
        slots.append(rect(sx, sy, TAB, slot_w))          # horizontal slot (TAB long) for the shelf's end tab
    return dict(poly=[outline] + slots)
def shelf():
    """body W x DEPTH with a TAB-long, T-thick tab on each end (passes through the side panel slots); outline as one polygon"""
    m = (DEPTH - TAB) / 2
    return dict(poly=[[(0, m), (T, m), (T, 0), (T + W, 0), (T + W, m), (2 * T + W, m), (2 * T + W, m + TAB), (T + W, m + TAB), (T + W, DEPTH), (T, DEPTH), (T, m + TAB), (0, m + TAB)]])
parts = {"side_L": side(), "side_R": side(), "shelf_1": shelf(), "shelf_2": shelf(), "shelf_3": shelf(), "back_rail": dict(poly=[rect(0, 0, W, 30)])}
sheet_w, sheet_h = 600, 450
placed = nest(parts, sheet_w, sheet_h); bad = overlap(placed)
util = sum((bbox(p)[2] - bbox(p)[0]) * (bbox(p)[3] - bbox(p)[1]) for p in placed.values()) / (sheet_w * sheet_h)
lines.append(f"Slot width {slot_w:.2f} mm for {T:.0f} mm board (press fit, kerf {KERF} mm assumed already compensated by the laser shop: test coupon first). Parts nest on one {sheet_w}x{sheet_h} mm sheet with {'NO overlaps' if not bad else 'OVERLAPS '+str(bad)}; bounding-box utilisation {util:.0%}.")
write(placed, sheet_w, sheet_h, os.path.join(OUT, "masala_rack.svg"), os.path.join(OUT, "masala_rack.dxf"))
lines.append("Not verified: real jar sizes (measure yours), MDF modulus and moisture sag, glue-up squareness, finish.")
open(os.path.join(DOC, "results_rack.md"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines)); sys.exit(1 if bad else 0)
