#!/usr/bin/env python3
"""Kalakriti automata: kinematic design + verification + laser-cut SVG generator (standard library only).
Usage: python3 -I automata.py <out_dir>  -> SVG parts sheets + design_report.md.  Exit code 1 if any check fails.
Units mm / degrees.  Idealised kinematics (rigid parts, no friction in the geometry checks)."""
import math, sys
from pathlib import Path

G = 9.81
KERF = 0.2                       # laser kerf (mm): every outline is offset OUTWARD and every hole INWARD by half the kerf in part_poly(), so cut parts keep nominal size
CUT, ENG = "#ff0000", "#0000ff"
report, fails = [], []
def note(s=""): report.append(s)
def check(name, ok, detail=""):
    note(f"- {'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not ok: fails.append(name)

# ------------------------------------------------------------------ cam-follower
def cycloidal(u):                # rise fraction and its derivatives for u in [0,1]
    s = u - math.sin(2 * math.pi * u) / (2 * math.pi)
    v = 1 - math.cos(2 * math.pi * u)
    a = 2 * math.pi * math.sin(2 * math.pi * u)
    return s, v, a

def motion(theta_deg, lift, rise, dwell1, fall, dwell2):
    """Follower displacement s, ds/dtheta (mm/rad) and d2s/dtheta2 for a rise-dwell-fall-dwell cycle (cycloidal laws)."""
    t = theta_deg % 360.0
    if t < rise:
        s, v, a = cycloidal(t / rise); k = math.radians(rise); return lift * s, lift * v / k, lift * a / k ** 2
    t -= rise
    if t < dwell1: return lift, 0.0, 0.0
    t -= dwell1
    if t < fall:
        s, v, a = cycloidal(t / fall); k = math.radians(fall); return lift * (1 - s), -lift * v / k, -lift * a / k ** 2
    return 0.0, 0.0, 0.0

def cam_analysis(Rb, Rr, lift, rise, d1, fall, d2, n=720):
    Rp = Rb + Rr; pts, phi_max, rho_min, a_max = [], 0.0, 1e9, 0.0
    for i in range(n):
        th = 360.0 * i / n; s, v, a = motion(th, lift, rise, d1, fall, d2)
        R = Rp + s; ang = -math.radians(th)                         # cam turns clockwise relative to the follower
        pts.append((R * math.cos(ang), R * math.sin(ang)))
        phi_max = max(phi_max, math.degrees(math.atan2(abs(v), R))); a_max = max(a_max, abs(a))
    for i in range(n):                                               # curvature of the pitch curve (convex parts only)
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        dx, dy = (x2 - x0) / 2, (y2 - y0) / 2; ddx, ddy = x2 - 2 * x1 + x0, y2 - 2 * y1 + y0
        cross = dx * ddy - dy * ddx
        if cross != 0:
            rho = (dx * dx + dy * dy) ** 1.5 / abs(cross)
            if cross < 0: rho_min = min(rho_min, rho)                # sign chosen for clockwise travel: convex when negative
    return pts, phi_max, rho_min, a_max

def solve_cam(name, lift, rise, d1, fall, d2, Rr=4.0, phi_lim=30.0, rpm=120):
    for Rb10 in range(100, 600, 5):                                  # base circle 10..60 mm
        Rb = Rb10 / 10
        pts, phi, rho, a = cam_analysis(Rb, Rr, lift, rise, d1, fall, d2)
        if phi <= phi_lim and rho >= Rr * 1.5: break
    w = rpm * 2 * math.pi / 60; acc = a * w * w / 1000                # follower acceleration m/s2 at `rpm`
    rpm_safe = 60 / (2 * math.pi) * math.sqrt(G * 0.5 / (a / 1000))   # gravity return stays in contact up to 0.5 g
    note(f"**{name}**: lift {lift} mm, rise {rise} deg, dwell {d1} deg, fall {fall} deg, dwell {d2} deg, roller O{2 * Rr:.0f} mm -> base circle {Rb:.1f} mm, "
         f"max pressure angle {phi:.1f} deg, min pitch-curve radius {rho:.1f} mm, peak follower acceleration {acc:.2f} m/s2 at {rpm} rpm; gravity return holds contact to about {rpm_safe:.0f} rpm.")
    check(f"{name}: pressure angle <= {phi_lim} deg", phi <= phi_lim, f"{phi:.1f} deg")
    check(f"{name}: no undercut (pitch radius of curvature >= 1.5 x roller radius)", rho >= Rr * 1.5, f"{rho:.1f} mm")
    check(f"{name}: follower stays on the cam at 120 rpm (acceleration < 0.5 g)", acc < 0.5 * G, f"{acc:.2f} m/s2")
    return Rb, Rr, pts

def working_profile(pts, Rr):
    """Inward offset of the pitch curve by the roller radius: the nominal cam surface (kerf compensation happens in part_poly)."""
    out, n = [], len(pts)
    for i in range(n):
        x0, y0 = pts[i - 1]; x2, y2 = pts[(i + 1) % n]; tx, ty = x2 - x0, y2 - y0; L = math.hypot(tx, ty)
        nx, ny = ty / L, -tx / L                                      # for clockwise travel the inward normal is (ty, -tx)/L
        off = Rr                                                      # nominal cam surface; kerf is added once, outward, in part_poly()
        px, py = pts[i]
        if px * nx + py * ny > 0: nx, ny = -nx, -ny                   # make sure it points toward the centre
        out.append((px + nx * off, py + ny * off))
    return out

# ------------------------------------------------------------------ gears
def involute_gear(z, m, alpha=20.0, backlash=0.15, steps=8):
    """Closed polygon of a spur gear, nominal size with the tooth thinned by the backlash only."""
    r = m * z / 2; rb = r * math.cos(math.radians(alpha)); ra = r + m; rf = r - 1.25 * m
    def inv(t): return math.tan(t) - t
    def pt(rad, ang): return rad * math.cos(ang), rad * math.sin(ang)
    half_pitch_angle = math.pi / (2 * z) - backlash / (2 * r)                  # half tooth angle at the pitch circle: nominal tooth minus backlash (kerf handled in part_poly)
    a_pitch = math.acos(rb / r); inv_pitch = inv(a_pitch)
    out = []
    for k in range(z):
        c = 2 * math.pi * k / z
        left, right = [], []
        for j in range(steps + 1):
            rad = max(rb, rf) + (ra - max(rb, rf)) * j / steps
            ta = math.acos(min(1.0, rb / rad)); ang = inv(ta) - inv_pitch
            right.append(pt(rad, c - half_pitch_angle + ang)); left.append(pt(rad, c + half_pitch_angle - ang))   # tooth narrows toward the tip
        out += right + left[::-1]
        c2 = c + math.pi / z                                           # root between teeth
        out.append(pt(rf, c2))
    return out

def gear_check(name, z1, z2, m, alpha=20.0):
    a = m * (z1 + z2) / 2
    ra1, ra2 = m * z1 / 2 + m, m * z2 / 2 + m; rb1, rb2 = m * z1 / 2 * math.cos(math.radians(alpha)), m * z2 / 2 * math.cos(math.radians(alpha))
    eps = (math.sqrt(ra1 ** 2 - rb1 ** 2) + math.sqrt(ra2 ** 2 - rb2 ** 2) - a * math.sin(math.radians(alpha))) / (math.pi * m * math.cos(math.radians(alpha)))
    note(f"**{name}**: module {m}, {z1}:{z2} teeth (ratio {z2 / z1:.1f}:1), centre distance {a:.1f} mm, contact ratio {eps:.2f}.")
    check(f"{name}: no undercut (z >= 17 for 20 deg pressure angle)", min(z1, z2) >= 17, f"z={min(z1, z2)}")
    check(f"{name}: contact ratio >= 1.2", eps >= 1.2, f"{eps:.2f}")
    return a

# ------------------------------------------------------------------ crank-slider (bullock head)
def crank_slider(name, r, L):
    worst = max(math.degrees(math.asin(r / L * abs(math.sin(math.radians(t))))) for t in range(360))
    note(f"**{name}**: crank {r} mm, connecting rod {L} mm -> stroke {2 * r} mm, maximum rod angle {worst:.1f} deg.")
    check(f"{name}: rod angle <= 25 deg (no jamming)", worst <= 25.0, f"{worst:.1f} deg")

# ------------------------------------------------------------------ SVG helpers
def path(pts, c=CUT): return '<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pts) + f'" fill="none" stroke="{c}" stroke-width="0.1"/>'
def circ(x, y, r, c=CUT): return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="{c}" stroke-width="0.1"/>'
def rect(x, y, w, h, c=CUT, r=0): return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" fill="none" stroke="{c}" stroke-width="0.1"/>'
def text(x, y, s): return f'<text x="{x:.1f}" y="{y:.1f}" font-size="3" fill="{ENG}">{s}</text>'

def bbox(pts): xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; return min(xs), min(ys), max(xs), max(ys)
def shift(pts, dx, dy): return [(x + dx, y + dy) for x, y in pts]
def perimeter(pts): return sum(math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) for i in range(len(pts)))

def kerf_outline(pts, d=None):
    """Offset a closed outline outward by d (default half the kerf): the laser path that leaves a part of nominal size."""
    d = KERF / 2 if d is None else d; n = len(pts)
    area = sum(pts[i - 1][0] * pts[i][1] - pts[i][0] * pts[i - 1][1] for i in range(n)) / 2; sgn = 1.0 if area > 0 else -1.0
    out = []
    for i in range(n):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[(i + 1) % n]
        e1 = (x1 - x0, y1 - y0); e2 = (x2 - x1, y2 - y1); l1 = math.hypot(*e1) or 1e-9; l2 = math.hypot(*e2) or 1e-9
        n1 = (sgn * e1[1] / l1, -sgn * e1[0] / l1); n2 = (sgn * e2[1] / l2, -sgn * e2[0] / l2)      # outward normals
        bx_, by_ = n1[0] + n2[0], n1[1] + n2[1]; lb = math.hypot(bx_, by_)
        if lb < 1e-9: bx_, by_, lb = n1[0], n1[1], 1.0
        bx_, by_ = bx_ / lb, by_ / lb; c = max(bx_ * n1[0] + by_ * n1[1], 0.5)                     # miter limited to 2 x d
        out.append((x1 + bx_ * d / c, y1 + by_ * d / c))
    return out
def part_poly(name, pts, holes=()):
    """Nominal outline and holes in; laser path out: outline offset outward, holes reduced, by half the kerf each."""
    return dict(name=name, outline=kerf_outline(pts), holes=[(x, y, r - KERF / 2) for (x, y, r) in holes], nominal=pts)
def part_rect(name, w, h, holes=(), r=2):
    p = part_poly(name, [(0, 0), (w, 0), (w, h), (0, h)], holes); p["rounded"] = r; return p

def sheet(kit, parts, W=400.0, gap=6.0):
    """Shelf-pack parts into a W-wide sheet; returns svg text, height, cut length."""
    x = y = rowh = 0.0; items = []; cutlen = 0.0
    for p in parts:
        x0, y0, x1, y1 = bbox(p["outline"]); w, h = x1 - x0, y1 - y0
        if x + w > W: x = 0; y += rowh + gap; rowh = 0
        items.append((p, x - x0, y - y0, x, y, w, h)); x += w + gap; rowh = max(rowh, h)
    H = y + rowh + gap
    body = []
    for p, dx, dy, px, py, w, h in items:
        out = shift(p["outline"], dx, dy); body.append(path(out)); cutlen += perimeter(out)
        for hx, hy, hr in p["holes"]:
            body.append(circ(hx - bbox(p["outline"])[0] + px, hy - bbox(p["outline"])[1] + py, hr)); cutlen += 2 * math.pi * hr
        body.append(text(px, py + h + 3.5, p["name"]))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H + 6:.0f}mm" viewBox="0 0 {W} {H + 6:.0f}">\n' + "\n".join(body) + "\n</svg>\n"
    return svg, H, cutlen

def cam_part(name, Rb, Rr, pts):
    prof = working_profile(pts, Rr)
    return part_poly(name, prof, holes=[(0, 0, 2.1)])

def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    note("# Automata design report (generated by automata.py)\n")
    note("## 1. Cam-follower mechanisms")
    peacock = solve_cam("Dancing peacock fan lift", 12, 120, 60, 120, 60)
    ganesh = solve_cam("Ganesh modak lift", 25, 150, 30, 150, 30)
    note("\n## 2. Gear train (rotating diya wheel)")
    a = gear_check("Diya wheel gear pair", 18, 54, 2.0)
    note("\n## 3. Crank-slider (bullock head and cart)")
    crank_slider("Bullock head bob", 10, 45)
    crank_slider("Bullock cart wheel-rocker", 12, 55)
    # ---------------- parts sheets
    sheets = {}
    # kit 1 peacock: frame, cam, follower guide, follower with fan, crank handle, shaft supports
    kit1 = [cam_part("peacock cam x1", *peacock), part_rect("base 150x100", 150, 100, [(20, 50, 2.1), (130, 50, 2.1)]),
            part_rect("side frame x2", 80, 70, [(40, 25, 2.1)]), part_rect("follower guide plate x2 (hole for O6 dowel follower)", 40, 60, [(20, 15, 3.1)]),
            part_poly("fan (peacock tail)", [(60 * math.cos(math.radians(t)), -60 * math.sin(math.radians(t))) for t in range(0, 181, 6)]),
            part_poly("crank handle", [(0, 0), (50, 0), (50, 12), (0, 12)], [(6, 6, 2.1), (44, 6, 2.1)]), part_rect("roller holder x1", 14, 14, [(7, 7, 2.1)])]
    kit2 = [cam_part("ganesh cam x1", *ganesh), part_rect("base 160x110", 160, 110, [(20, 55, 2.1), (140, 55, 2.1)]),
            part_rect("side frame x2", 90, 90, [(45, 30, 2.1)]), part_rect("follower arm 8x100", 8, 100, [(4, 8, 2.1)]),
            part_rect("hand-with-modak plate", 40, 30, [(10, 15, 2.1)]), part_rect("body plate (stylised Ganesh)", 80, 100, []),
            part_poly("crank handle", [(0, 0), (50, 0), (50, 12), (0, 12)], [(6, 6, 2.1), (44, 6, 2.1)])]
    g1 = involute_gear(18, 2.0); g2 = involute_gear(54, 2.0)
    kit3 = [part_poly("gear 18T drive", g1, [(0, 0, 2.1)]), part_poly("gear 54T platform gear", g2, [(0, 0, 2.1)]),
            part_poly("diya platform O110", [(55 * math.cos(math.radians(t)), 55 * math.sin(math.radians(t))) for t in range(0, 360, 5)], [(0, 0, 2.1)]),
            part_rect("base 200x120", 200, 120, [(60, 60, 2.1), (60 + a, 60, 2.1)]), part_rect("side frame x2", 60, 70, [(30, 20, 2.1)]),
            part_poly("crank handle", [(0, 0), (50, 0), (50, 12), (0, 12)], [(6, 6, 2.1), (44, 6, 2.1)])]
    kit4 = [part_rect("base 180x100", 180, 100, [(30, 50, 2.1), (150, 50, 2.1)]), part_rect("side frame x2", 90, 70, [(45, 25, 2.1)]),
            part_poly("crank disc O40", [(20 * math.cos(math.radians(t)), 20 * math.sin(math.radians(t))) for t in range(0, 360, 6)], [(10, 0, 2.1)]),
            part_rect("connecting rod 4x45 ", 55, 8, [(4, 4, 2.1), (51, 4, 2.1)]), part_rect("ox head slider 10x70", 70, 10, [(5, 5, 2.1)]),
            part_poly("ox body (stylised)", [(0, 0), (90, 0), (90, 45), (70, 60), (20, 60), (0, 40)]), part_poly("cart wheel O60 x2", [(30 * math.cos(math.radians(t)), 30 * math.sin(math.radians(t))) for t in range(0, 360, 6)], [(0, 0, 2.1)]),
            part_rect("cart bed 90x50", 90, 50, [(15, 25, 2.1), (75, 25, 2.1)])]
    note("\n## 4. Laser parts sheets (3 mm MDF, sheet width 400 mm)\n")
    note("| Kit | Sheet size mm | Parts | Cut length m | Estimated laser time min (15 mm/s + 0.5 s per pierce) |")
    note("|---|---|---|---|---|")
    for key, label, parts in (("peacock", "Dancing peacock", kit1), ("ganesh", "Modak Ganesh", kit2), ("diya", "Diya wheel", kit3), ("bullock", "Bullock cart", kit4)):
        svg, H, cl = sheet(key, parts); (out / f"{key}_parts_sheet.svg").write_text(svg)
        npierce = sum(1 + len(p["holes"]) for p in parts); mins = (cl / 15 + npierce * 0.5) / 60
        note(f"| {label} | 400 x {H + 6:.0f} | {len(parts)} | {cl / 1000:.2f} | {mins:.1f} |")
        check(f"{label}: sheet fits a 400 x 300 mm laser bed", H + 6 <= 300, f"{H + 6:.0f} mm")
    note("\nFigure silhouettes (peacock fan, Ganesh body, ox body) are simple placeholders: an illustrator should finish the artwork; mechanism geometry is final.")
    (out / "design_report.md").write_text("\n".join(report) + "\n")
    print("\n".join(report)); return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "out"))
