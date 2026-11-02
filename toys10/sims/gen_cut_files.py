"""PROVISIONAL laser files for toys that had calculations but no drawings: Rubber-band Racer (3 mm MDF) and Marble Cricket (6 mm MDF back, 3 mm acrylic front).
Geometry is my first-pass layout from the design notes (12 mm marble, Galton-board pitch, 4.2 mm axle holes); it has NEVER been cut: do a cardboard test first.
Outputs ../out/racer_parts.{svg,dxf} and ../out/marble_cricket_parts.{svg,dxf}. Units mm, red stroke = CUT."""
import os, math, sys
import ezdxf
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"); os.makedirs(OUT, exist_ok=True)
KERF = 0.2   # laser kerf (mm): outlines offset outward, holes and slots inward by half the kerf
def kerf_poly(pts, d):
    """offset an axis-aligned rectangle-like polygon by d (positive = outward)"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return [(x + (d if x > cx else -d), y + (d if y > cy else -d)) for x, y in pts]
class Sheet:
    def __init__(s, w, h): s.w, s.h, s.items, s.labels = w, h, [], []
    def poly(s, pts, name=None, hole=False): s.items.append(("poly", kerf_poly(pts, -KERF / 2 if hole else KERF / 2))); name and s.labels.append((pts[0][0] + 1, pts[0][1] + 4, name))
    def rect(s, x, y, w, h, name=None, hole=False): s.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], name, hole)
    def circ(s, cx, cy, r, outer=False): s.items.append(("circ", (cx, cy, r + KERF / 2 if outer else r - KERF / 2)))   # kerf: outer discs grow, holes shrink, so parts keep nominal size
    def save(s, base):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}mm" height="{s.h}mm" viewBox="0 0 {s.w} {s.h}"><g fill="none" stroke="red" stroke-width="0.2">']
        doc = ezdxf.new("R2010"); doc.layers.add("CUT", color=1); msp = doc.modelspace()
        for k, v in s.items:
            if k == "poly": svg.append('<polygon points="' + " ".join(f"{x:.3f},{y:.3f}" for x, y in v) + '"/>'); msp.add_lwpolyline([(x, s.h - y) for x, y in v], close=True, dxfattribs={"layer": "CUT"})
            else: cx, cy, r = v; svg.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}"/>'); msp.add_circle((cx, s.h - cy), r, dxfattribs={"layer": "CUT"})
        for x, y, t in s.labels: svg.append(f'<text x="{x}" y="{y}" font-size="3" fill="blue" stroke="none">{t}</text>')
        svg.append("</g></svg>"); open(base + ".svg", "w").write("\n".join(svg)); doc.saveas(base + ".dxf")
# ---------------- Racer: 150 x 60 chassis, 4 wheels (outer 50 mm + inner 46 mm discs glued = O-ring groove), thumb wheel ----------------
r = Sheet(300, 200)
r.rect(5, 5, 150, 60, "chassis")
for cx in (35, 125): r.circ(cx, 12, 2.1); r.circ(cx, 58, 2.1)                              # axle holes (4.2 mm for 4 mm dowel) near both long edges
r.rect(70, 25, 12, 4, hole=True); r.rect(70, 41, 12, 4, hole=True)                                                 # band hook slots
for i in range(4):
    r.circ(30 + i * 56, 100, 25, outer=True); r.circ(30 + i * 56, 100, 2.1)                              # outer wheel discs
    r.circ(30 + i * 56, 160, 23, outer=True); r.circ(30 + i * 56, 160, 2.1)                              # inner (groove) discs: glue between two outer discs
r.circ(262, 40, 17.5, outer=True); r.circ(262, 40, 2.1)
for a in range(4): r.circ(262 + 9 * math.cos(a * math.pi / 2), 40 + 9 * math.sin(a * math.pi / 2), 2.5)   # grip holes in the thumb wheel
r.save(os.path.join(OUT, "racer_parts"))
# ---------------- Marble Cricket: 300 x 400 back panel (6 mm MDF) with a Galton peg layout, pocket dividers ----------------
c = Sheet(940, 450); P = 300 / 9; ROWS = 8
c.rect(5, 5, 300, 400, "back_panel_6mm_MDF")
for k in range(1, ROWS + 1):
    y = 5 + 70 + (k - 1) * P * 0.866
    for i in range(k): c.circ(5 + 150 + (i - (k - 1) / 2) * P, y, 3.1)                      # 6 mm dowel pegs (holes 6.2 mm)
c.circ(155, 40, 8)                                                                           # feed hole, 16 mm: marble drops in here
for j in range(1, 9): c.rect(625 + (j - 1) * 36, 5, 3, 70, "dividers" if j == 1 else None)    # 8 pocket dividers, 3 x 70 mm each (glued to the back panel at the pocket boundaries)
c.rect(315, 5, 300, 400, "front_panel_3mm_acrylic")
c.save(os.path.join(OUT, "marble_cricket_parts"))
print("racer_parts and marble_cricket_parts written")
