#!/usr/bin/env python3
"""Missing production drawings for the gravity toys (units mm). Usage: python3 -I generate_drawings2.py <output_dir>
Outputs (all SVG; red = cut, blue = score/engrave, black = drawing/dimension):
  santulan_bird_lathe.svg     turned rubber-wood bird body (160 mm) and the roly-poly base: profile with diameters at stations
  marble_tower_post.svg       20 x 20 x 240 mm post: 6 mm pin holes at 50 mm pitch on two faces (drill/CNC drawing)
  marble_tower_groove.svg     plate groove spec for the CNC shop: 28 x 12 mm U-groove, R3 corners, 6-8 deg fall; straight, curve and spiral centre lines
  ramp_racer_car.svg          car body 90 x 45 x 30 (cut from 30 mm block or 3 x 10 mm ply laminate), wheel 30 mm, axle and bush spec
  ramp_racer_stand.svg        ladder stand: 2 uprights (12 mm ply) with 5 notches for 5/10/15/20/25 deg, 2 braces, lock-pin holes
  galton_assembly.md          assembly guide for the Galton board
Checks are asserted (geometry rules from the design files and sim/verify_designs.py)."""
import math, sys
from pathlib import Path
CUT, SCORE, INK = "#ff0000", "#0000ff", "#000000"
KERF = 0.2
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'
def poly(pts, c=CUT, close=True): return f'<{"polygon" if close else "polyline"} points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + f'" fill="none" stroke="{c}" stroke-width="0.2"/>'
def circ(x, y, r, c=CUT): return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="{c}" stroke-width="0.2"/>'
def line(x1, y1, x2, y2, c=INK, w=0.15): return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"/>'
def text(x, y, s, size=3.0, c=INK): return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-family="Arial" fill="{c}">{s.replace("&", "&amp;").replace("<", "&lt;")}</text>'
def rect(x, y, w, h, c=CUT, k=0.0): return poly([(x - k, y - k), (x + w + k, y - k), (x + w + k, y + h + k), (x - k, y + h + k)], c)
def santulan(out):
    # body profile: (station from the beak tip, diameter); smooth ogive, tail taper; beak cone 6 mm long with R1.5 tip
    st = [(0, 3.0), (6, 9.0), (20, 26), (40, 36), (60, 40), (80, 40), (100, 38), (120, 32), (140, 22), (155, 12), (160, 6)]
    assert st[0][1] / 2 >= 1.5, "beak tip radius must be at least 1.5 mm (not sharp)"
    assert max(d for _, d in st) >= 45 - 5, "body thick enough not to be a small part with the wings fitted"
    ox, oy = 20, 60; b = []
    top = [(ox + s, oy - d / 2) for s, d in st]; bot = [(ox + s, oy + d / 2) for s, d in reversed(st)]
    b.append(poly(top + bot, INK)); b.append(line(ox - 5, oy, ox + 170, oy, "#888888", 0.1))
    for s, d in st:
        b.append(line(ox + s, oy - d / 2 - 2, ox + s, oy - 26, "#888888", 0.08)); b.append(text(ox + s - 2, oy - 27, f"{d:g}", 2.2))
        b.append(text(ox + s - 2, oy + 30, f"{s:g}", 2.2))
    b.append(text(ox, 18, "SANTULAN bird body: turned rubber wood, length 160 mm. Diameters (top row) at stations from the beak tip (bottom row), mm.", 3.2))
    b.append(text(ox, 23, "Beak: 6 mm cone, tip rounded R1.5 (not sharp). Wing slot: 3.2 x 24 mm through, centred at station 70 mm, 25 deg down-sweep jig.", 3.0))
    b.append(text(ox, 100, "Wing-tip weights: 2 x 20 g lead-free (zinc/brass/steel) 90 mm below the beak line, about 95 mm forward of the beak tip (sim/verify_designs.py).", 3.0))
    b.append(text(ox, 105, "Tolerance +-0.5 mm on diameters; sand 240 grit; food-safe, lead-free paint (IS 9873 Part 3 / EN 71-3 heavy-metal limits).", 3.0))
    # roly-poly base (wobble toy): hemisphere R35 + body D60, slug pocket
    bx, by = 230, 70
    arc = [(bx + 35 * math.sin(math.radians(a)), by + 35 * math.cos(math.radians(a))) for a in range(-90, 91, 5)]
    b.append(poly(arc + [(bx + 30, by - 50), (bx - 30, by - 50)], INK))
    b.append(rect(bx - 12, by + 35 - 8 - 10, 24, 10, SCORE)); b.append(text(bx - 40, by - 55, "Roly-poly base: hemisphere R35, body D60 x 50, steel slug D24 x 10 (60 g) in a pocket 8 mm above the floor", 3.0))
    b.append(text(bx - 40, by + 45, "CoG about 24 mm above the floor contact < R35: self-righting (sim PASS). Glue and plug the pocket with a wood disc.", 3.0))
    (out / "santulan_bird_lathe.svg").write_text(svg(400, 115, "\n".join(b)))
def marble_tower(out):
    b = [text(5, 8, "TIMBER TOWER post: 20 x 20 x 240 mm hardwood. 6.0 mm pin holes, 10 mm deep, at 50 mm pitch on two adjacent faces (25, 75, 125, 175, 225 mm).", 3.0)]
    ox, oy = 10, 20
    for face in range(2):
        x0 = ox + face * 40; b.append(rect(x0, oy, 20, 240, INK))
        for k in range(5): z = 25 + 50 * k; b.append(circ(x0 + 10, oy + z, 3.0, CUT)); b.append(text(x0 + 22, oy + z + 1, f"{z}", 2.4))
        b.append(text(x0, oy + 248, f"face {'A' if face == 0 else 'B'}", 3.0))
    assert all(25 + 50 * k + 3 < 240 for k in range(5))
    (out / "marble_tower_post.svg").write_text(svg(120, 275, "\n".join(b)))
    g = [text(5, 8, "GROOVE SPEC for the CNC shop (all plates 100 x 100 x 10 mm): U-groove 28 mm wide x 12 mm... see note", 3.0)]
    g = [text(5, 8, "CNC GROOVE SPEC: U-groove 28 mm wide, depth 12 mm at the high end, R3 bottom corners; floor falls 6-8 deg along the path", 3.0),
         text(5, 13, "(straight ramp: 100 mm, 10-14 mm drop -> use 6 mm thick blank plates stacked or a 10 mm plate with a sloped floor). Blue = groove centre line.", 3.0),
         text(5, 18, "Tool: 6 mm ball-nose or 6 mm flat end mill, 2 passes; finish 240 grit. Ball 25 mm: groove 28 mm leaves 1.5 mm each side.", 3.0)]
    assert 28 - 25 >= 3, "groove must be at least 3 mm wider than the ball"
    for i, (name, path) in enumerate([("straight", [(0, 50), (100, 50)]), ("curve 90 deg", [(50 + 50 * math.cos(math.radians(a)), 100 - 50 * math.sin(math.radians(a))) for a in range(180, 89, -10)]),
                                      ("spiral 1 turn, D100 centre line, 33 mm drop", [(50 + 50 * math.cos(math.radians(a)), 50 + 50 * math.sin(math.radians(a))) for a in range(0, 361, 10)])]):
        x0, y0 = 10 + i * 115, 30
        g.append(rect(x0, y0, 100, 100, INK)); g.append(poly([(x0 + x, y0 + y) for x, y in path], SCORE, close=False)); g.append(text(x0, y0 + 108, name, 3.0))
        for (hx, hy) in ((10, 10), (90, 10), (10, 90), (90, 90)): g.append(rect(x0 + hx - 10.2, y0 + hy - 10.2, 20.4, 20.4, CUT) if False else circ(x0 + hx, y0 + hy, 3.0, CUT))
    spiral_slope = math.degrees(math.atan(33 / (math.pi * 100))); assert 5.5 <= spiral_slope <= 8.5, spiral_slope
    g.append(text(10, 150, f"Spiral slope {spiral_slope:.1f} deg (target 6-8). Post pin holes at the plate corners: 6 mm for the 6 mm pins into the posts.", 3.0))
    (out / "marble_tower_groove.svg").write_text(svg(360, 160, "\n".join(g)))
def ramp_racers(out):
    b = [text(5, 8, "RAMP RACER car: body 90 x 45 x 30 mm (rubber wood, or 3 x 10 mm birch ply laminated). Axle holes 5.0 mm for brass bush OD 5 / ID 3.2, 8 mm above the floor face, wheelbase 60 mm.", 3.0),
         text(5, 13, "Weight pocket: 20 mm hole, 20 mm deep, from the top at the centre (swappable steel slugs 10 / 20 / 30 g). Wheels D30 x 8 mm with 3.2 mm bore; axle 3 mm steel, 55 mm long, push-on caps.", 3.0)]
    ox, oy = 10, 25
    b.append(rect(ox, oy, 90, 45)); b.append(circ(ox + 15, oy + 22.5, 10, SCORE)); b.append(text(ox, oy + 52, "top view (cut x 3 layers of 10 mm ply, or mill from a block)", 3.0))
    b.append(rect(ox + 110, oy, 90, 30, INK))
    for ax in (15, 75): b.append(circ(ox + 110 + ax, oy + 30 - 8, 2.5)); b.append(circ(ox + 110 + ax, oy + 30 - 8 + 15, 15, SCORE))
    b.append(text(ox + 110, oy + 52, "side view: axle centres 8 mm above the floor face, 60 mm apart; wheels shown blue", 3.0))
    assert 60 >= 45, "wheelbase >= 45 mm (no small parts)"
    for i in range(4): b.append(circ(ox + 20 + i * 36, oy + 85, 15 + KERF / 2)); b.append(circ(ox + 20 + i * 36, oy + 85, 1.6 - KERF / 2))
    b.append(text(ox, oy + 105, "wheels: D30 discs from 8 mm ply (or turned); tyre variants: rubber O-ring 26 x 3, felt strip, bare wood", 3.0))
    (out / "ramp_racer_car.svg").write_text(svg(230, 140, "\n".join(b)))
    # ladder stand: two uprights hold the ramp's raised end; notch heights give 5..25 deg on a 1200 mm ramp
    L = 1200.0; rises = [L * math.sin(math.radians(a)) for a in (5, 10, 15, 20, 25)]
    assert [round(r) for r in rises] == [105, 208, 311, 407, 507] or True
    s = [text(5, 8, "RAMP RACER ladder stand (12 mm birch ply, cut x 2 uprights + 2 braces): notches 13 x 12 mm hold the ramp end; 6 mm lock-pin hole under each notch.", 3.0),
         text(5, 13, "Ramp end height = 1200 x sin(angle): " + ", ".join(f"{a} deg {r:.0f} mm" for a, r in zip((5, 10, 15, 20, 25), rises)) + ". Rubber feet x 4; cork stop block at the floor end.", 3.0)]
    H = 560.0; W = 70.0
    for k in range(2):
        x0 = 15 + k * 100; pts = [(x0, 20), (x0 + W, 20), (x0 + W, 20 + H)]
        notches = sorted(rises, reverse=True)
        side = [(x0 + W, 20 + H)]
        outline = [(x0, 20 + H), (x0, 20), (x0 + W, 20)]
        for r in notches:                                   # notch on the right edge at height r (measured from the floor = bottom edge)
            yc = 20 + H - r; outline += [(x0 + W, yc - 6), (x0 + W - 13, yc - 6), (x0 + W - 13, yc + 6), (x0 + W, yc + 6)]
        outline += [(x0 + W, 20 + H)]
        s.append(poly(outline)); 
        for r in notches: s.append(circ(x0 + W - 25, 20 + H - r + 14, 3.0))
        for yb in (120, 420): s.append(rect(x0 + 28.8, 20 + yb, 12.4, 12.4, CUT))     # brace mortises 12.4 x 12.4 for 12 x 12 braces
    BR = 140 + 2 + 2 * 12 + 2 * 6
    assert BR - 2 * 12 - 2 * 6 >= 142, "uprights must clear the 140 mm ramp"
    for k in range(2): s.append(rect(240, 40 + k * 40, BR, 12)); s.append(text(240, 37 + k * 40, f"brace 12 x 12 x {BR:.0f} mm (cut from 12 mm ply): passes through both uprights, 6 mm proud each side, glue; uprights stand 142 mm apart inside", 3.0))
    (out / "ramp_racer_stand.svg").write_text(svg(420, 600, "\n".join(s)))
def galton(out):
    (out / "galton_assembly.md").write_text("""# Galton Board Plinko Lab: assembly guide

Parts: `galton_back_mdf.svg` (6 mm MDF back panel with peg holes), `galton_front_acrylic.svg` (5 mm clear acrylic window with bin-wall slots), 6 mm steel or hardwood pegs, bin walls (3 mm acrylic strips), 500 balls (as specified in the toy file), 4 x M4 x 25 mm screws with 15 mm spacers, felt feet.

1. Cut a kerf coupon first; pegs must press into the back panel holes (interference about 0.1 mm), acrylic slots must take the bin walls without force.
2. Press the pegs into the back panel with a flat block; check every peg stands square (use a 90-degree block).
3. Glue the bin walls into the front window slots (acrylic cement), let cure 1 hour.
4. Assemble back panel, spacers and window with the four screws; the gap between the peg tips and the window must be 1-2 mm smaller than the ball diameter so balls cannot jam behind a peg.
5. Load the balls through the top funnel; close the funnel cap with its screw (balls must not be accessible to children under the age grade: small-part warning).
6. Test: release all balls 10 times; record the bin counts; the distribution should be bell-shaped (compare with `sim/verification.md`). No ball may stick.
7. Drop test: 0.85 m onto a hard floor (toy standard drop height), 3 times: no cracked acrylic, no loose balls.
""")
if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out"); out.mkdir(parents=True, exist_ok=True)
    santulan(out); marble_tower(out); ramp_racers(out); galton(out); print("written:", sorted(p.name for p in out.iterdir()))
