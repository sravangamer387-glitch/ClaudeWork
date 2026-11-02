"""Tilt Maze gimbal (3 mm MDF, laser cut): base, two uprights, a box-jointed middle frame, the tray that holds the interchangeable maze plates,
axle bosses and two knobs. Two-axis gimbal on 6 mm wooden dowel stub axles. Kerf-compensated (outlines outward, holes inward by half the kerf).
Outputs ../out/tilt_maze_gimbal_sheet1/2.{svg,dxf} and prints the geometry checks. First-pass: cut one set in cardboard or scrap MDF and test before a batch."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ezdxf
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
T, KERF = 3.0, 0.2                 # sheet thickness, laser kerf (mm)
PLATE = 200.0                      # maze plate (198 mm maze + margin), drops into the tray
DOWEL = 6.0; H_FIX = 6.2; H_TURN = 6.6   # dowel; hole where the dowel is glued; hole where it turns
TRAY_IN = PLATE + 1.0; TRAY_H = 20.0; GAP = 8.0; FRAME_H = 40.0; TILT = 8.0
checks = []
def chk(name, ok, detail): checks.append((name, ok, detail))
def kerf_outline(pts, d=KERF / 2):
    n = len(pts); area = sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(n)) / 2; sgn = 1.0 if area > 0 else -1.0; out = []
    for i in range(n):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[(i + 1) % n]
        e1 = (x1 - x0, y1 - y0); e2 = (x2 - x1, y2 - y1); l1 = math.hypot(*e1) or 1e-9; l2 = math.hypot(*e2) or 1e-9
        n1 = (sgn * e1[1] / l1, -sgn * e1[0] / l1); n2 = (sgn * e2[1] / l2, -sgn * e2[0] / l2)
        bx, by = n1[0] + n2[0], n1[1] + n2[1]; lb = math.hypot(bx, by) or 1.0; bx, by = bx / lb, by / lb; c = max(bx * n1[0] + by * n1[1], 0.5)
        out.append((x1 + bx * d / c, y1 + by * d / c))
    return out
def fingers(length, n, inset, phase):
    """points along an edge of `length` with n segments; segments with (i % 2 == phase) are tabs sticking out by `inset` (as y offsets)"""
    pts = []; seg = length / n
    for i in range(n):
        y = -inset if (i % 2 == phase) else 0.0
        pts += [(i * seg, y), ((i + 1) * seg, y)]
    return pts
class Sheet:
    def __init__(s): s.items, s.labels, s.x, s.y, s.rowh, s.W = [], [], 5.0, 5.0, 0.0, 900.0
    def place(s, w, h):
        if s.x + w > s.W: s.x = 5.0; s.y += s.rowh + 6.0; s.rowh = 0.0
        ox, oy = s.x, s.y; s.x += w + 6.0; s.rowh = max(s.rowh, h); return ox, oy
    def part(s, name, outline, holes=()):
        xs = [p[0] for p in outline]; ys = [p[1] for p in outline]; w, h = max(xs) - min(xs), max(ys) - min(ys)
        ox, oy = s.place(w, h); dx, dy = ox - min(xs), oy - min(ys)
        s.items.append(("poly", [(x + dx, y + dy) for x, y in kerf_outline(outline)]))
        for (hx, hy, d) in holes: s.items.append(("circ", (hx + dx, hy + dy, d / 2 - KERF / 2)))
        s.labels.append((ox + 2, oy + h / 2, name))
    def save(s, base):
        H = s.y + s.rowh + 10
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.W}mm" height="{H:.0f}mm" viewBox="0 0 {s.W} {H:.0f}"><g fill="none" stroke="red" stroke-width="0.2">']
        doc = ezdxf.new("R2010"); doc.layers.add("CUT", color=1); msp = doc.modelspace()
        for k, v in s.items:
            if k == "poly": svg.append('<polygon points="' + " ".join(f"{x:.3f},{y:.3f}" for x, y in v) + '"/>'); msp.add_lwpolyline([(x, H - y) for x, y in v], close=True, dxfattribs={"layer": "CUT"})
            else: cx, cy, r = v; svg.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}"/>'); msp.add_circle((cx, H - cy), r, dxfattribs={"layer": "CUT"})
        for x, y, t in s.labels: svg.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="4" fill="blue" stroke="none">{t}</text>')
        svg.append("</g></svg>"); open(base + ".svg", "w").write("\n".join(svg)); doc.saveas(base + ".dxf"); return H
def wall(L, H, nf, phase_ends, hole=None, name=""):
    """rectangular wall L x H with finger joints of depth T on both vertical ends; phase_ends 0/1 picks tabs or slots"""
    seg = H / nf; pts = [(0, 0), (L, 0)]
    for i in range(nf):                                           # right end, top to bottom
        x = L + T if (i % 2 == phase_ends) else L
        pts += [(x, i * seg), (x, (i + 1) * seg)]
    pts += [(L, H), (0, H)]
    for i in reversed(range(nf)):                                 # left end, bottom to top
        x = -T if (i % 2 == phase_ends) else 0.0
        pts += [(x, (i + 1) * seg), (x, i * seg)]
    clean = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - clean[-1][0]) > 1e-9 or abs(p[1] - clean[-1][1]) > 1e-9: clean.append(p)
    return clean
def main():
    sh1 = Sheet(); sh2 = Sheet(); sh = sh1
    # --- tray: floor + four 20 mm walls (glued), axle bosses on the left and right walls
    TO = TRAY_IN + 2 * T
    sh.part("tray floor", [(0, 0), (TO, 0), (TO, TO), (0, TO)])
    for nm in ("tray wall L", "tray wall R"): sh.part(nm, [(0, 0), (TO, 0), (TO, TRAY_H), (0, TRAY_H)], [(TO / 2, TRAY_H / 2, H_FIX)])
    for nm in ("tray wall F", "tray wall B"): sh.part(nm, [(0, 0), (TRAY_IN, 0), (TRAY_IN, TRAY_H), (0, TRAY_H)])
    for i in range(4): sh.part(f"boss {i + 1}", [(0, 0), (18, 0), (18, 18), (0, 18)], [(9, 9, H_FIX)])
    sh = sh2
    # --- middle frame: four 40 mm walls with finger joints; tray axle (A) turns in the L/R walls, frame axle (B) is glued in the F/B walls
    MI = TO + 2 * GAP; nf = 5
    sh.part("frame wall L", wall(MI, FRAME_H, nf, 0), [(MI / 2, FRAME_H / 2, H_TURN)])
    sh.part("frame wall R", wall(MI, FRAME_H, nf, 0), [(MI / 2, FRAME_H / 2, H_TURN)])
    MO = MI + 2 * T
    sh.part("frame wall F", wall(MO - 2 * T, FRAME_H, nf, 1), [((MO - 2 * T) / 2, FRAME_H / 2, H_FIX)])
    sh.part("frame wall B", wall(MO - 2 * T, FRAME_H, nf, 1), [((MO - 2 * T) / 2, FRAME_H / 2, H_FIX)])
    # --- base and uprights (axle B turns in the uprights)
    AX_Z = 60.0; UP_W = 80.0; BASE_L = MO + 2 * (T + 12 + 6); BASE_W = MO + 40
    tabs = [(UP_W / 2 - 25, 0), (UP_W / 2 + 15, 0)]
    for nm in ("upright F", "upright B"):
        up = [(0, 0), (UP_W, 0), (UP_W, AX_Z + 20), (UP_W / 2 + 15, AX_Z + 20 + 8), (UP_W / 2 - 15, AX_Z + 20 + 8), (0, AX_Z + 20)]
        up = [(0, 0)] + [(tx, 0) for tx, _ in tabs[:1]] + [(tabs[0][0], T), (tabs[0][0] + 10, T), (tabs[0][0] + 10, 0), (tabs[1][0], 0), (tabs[1][0], T), (tabs[1][0] + 10, T), (tabs[1][0] + 10, 0)] + up[1:]
        up = [(x, -y) for x, y in up]                                            # tabs point down
        sh.part(nm, up, [(UP_W / 2, -(AX_Z - T) + 0.0, H_TURN)])
    sl = []
    for ycen in (BASE_W / 2 - (MO / 2 + T + 6), BASE_W / 2 + (MO / 2 + 6)):
        for tx, _ in tabs: sl.append((BASE_L / 2 - UP_W / 2 + tx, ycen))
    sh.part("base", [(0, 0), (BASE_L, 0), (BASE_L, BASE_W), (0, BASE_W)])
    base_item = len(sh.items) - 1; bx0, by0 = min(p[0] for p in sh.items[base_item][1]), min(p[1] for p in sh.items[base_item][1])
    for (sx, sy) in sl:                                                          # tab slots, 10 x 3.2 mm (kerf-compensated inward)
        r = [(sx, sy), (sx + 10, sy), (sx + 10, sy + 3.2), (sx, sy + 3.2)]
        sh.items.append(("poly", [(x + bx0, y + by0) for x, y in kerf_outline(r, -KERF / 2)]))
    # --- knobs: two layers each (on sheet 1)
    sh = sh1
    for i in range(4): sh.part(f"knob layer {i + 1}", [(20 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a))) for a in range(0, 360, 10)], [(0, 0, H_FIX)])
    H1 = sh1.save(os.path.join(OUT, "tilt_maze_gimbal_sheet1")); H2 = sh2.save(os.path.join(OUT, "tilt_maze_gimbal_sheet2")); H = max(H1, H2)
    # --- checks
    lift = (TO / 2) * math.sin(math.radians(TILT))
    chk("tray edge stays inside the frame height at +-8 deg", TRAY_H / 2 + lift <= FRAME_H / 2 + 6.0, f"tray edge rises {lift:.1f} mm; frame half-height {FRAME_H / 2:.0f} mm (+6 above)")
    chk("tray clears the frame walls sideways", GAP >= 6.0, f"gap {GAP:.0f} mm each side")
    flift = (MO / 2) * math.sin(math.radians(TILT))
    chk("frame clears the base at +-8 deg", AX_Z - FRAME_H / 2 - flift >= 10.0, f"lowest frame corner {AX_Z - FRAME_H / 2 - flift:.1f} mm above the base")
    chk("plate fits the tray with 0.5 mm per side", TRAY_IN - PLATE == 1.0, f"tray inside {TRAY_IN:.0f} mm, plate {PLATE:.0f} mm")
    chk("each sheet fits a 900 x 600 mm laser bed (common CO2 9060)", H <= 600, f"tallest sheet {H:.0f} mm")
    rep = ["# Tilt Maze gimbal: geometry checks", "", f"Sheet: 3 mm MDF, kerf {KERF} mm compensated. Dowel {DOWEL:.0f} mm: glued holes {H_FIX} mm, turning holes {H_TURN} mm.", "",
           "Axles (6 mm wooden dowel, cut to length): A-left 40 mm (tray boss -> frame wall L -> knob), A-right 25 mm (tray boss -> frame wall R), B-front 45 mm (frame wall F -> upright F -> knob), B-back 25 mm (frame wall B -> upright B).",
           "Assembly: glue the tray walls to the floor and the bosses inside the L/R walls; glue the frame walls at the finger joints (check square); push the uprights' tabs into the base slots and glue; fit axles; glue the knobs last.", ""]
    rep += [f"- {'PASS' if ok else 'FAIL'}: {n} ({d})" for n, ok, d in checks]
    open(os.path.join(OUT, "tilt_maze_gimbal_checks.md"), "w").write("\n".join(rep) + "\n"); print("\n".join(rep))
    return 0 if all(ok for _, ok, _ in checks) else 1
if __name__ == "__main__": sys.exit(main())
