#!/usr/bin/env python3
"""Independent geometric checks for the automata parts (needs pillow): cam offset distance, gear mesh interference."""
import math, sys
import numpy as np
from PIL import Image, ImageDraw
import automata as A

def dist_to_poly(p, poly):
    best = 1e9
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i - 1], poly[i]
        dx, dy = x2 - x1, y2 - y1; L2 = dx * dx + dy * dy
        t = 0 if L2 == 0 else max(0, min(1, ((p[0] - x1) * dx + (p[1] - y1) * dy) / L2))
        best = min(best, math.hypot(p[0] - (x1 + t * dx), p[1] - (y1 + t * dy)))
    return best

def test_cam(name, lift, rise, d1, fall, d2):
    Rb, Rr, pts = A.solve_cam(name, lift, rise, d1, fall, d2)
    prof = A.working_profile(pts, Rr)
    ds = [dist_to_poly(p, prof) for p in pts[::6]]
    err = max(abs(d - Rr) for d in ds)
    # follower roller centre stays on the pitch curve: distance to the nominal cam surface = roller radius
    ok = err < 0.15
    print(f"{name}: worst deviation of roller-to-profile distance from roller radius = {err:.3f} mm ->", "PASS" if ok else "FAIL")
    # profile area positive and simple (winding)
    area = sum(prof[i - 1][0] * prof[i][1] - prof[i][0] * prof[i - 1][1] for i in range(len(prof))) / 2
    print(f"  cam outline area {abs(area):.0f} mm2, size {max(p[0] for p in prof) - min(p[0] for p in prof):.1f} x {max(p[1] for p in prof) - min(p[1] for p in prof):.1f} mm")
    return ok

def raster(poly, rot, cx, cy, scale, size):
    im = Image.new("1", size, 0); d = ImageDraw.Draw(im)
    c, s = math.cos(rot), math.sin(rot)
    d.polygon([((cx + x * c - y * s) * scale, (cy + x * s + y * c) * scale) for x, y in poly], fill=1)
    return im

def test_gears(z1=18, z2=54, m=2.0):
    g1 = A.involute_gear(z1, m); g2 = A.involute_gear(z2, m); a = m * (z1 + z2) / 2
    scale = 6; size = (int((a + m * z2 / 2 + 15) * scale), int((m * z2 + 20) * scale)); worst = 0
    for k in range(0, 360, 4):
        r1 = math.radians(k); r2 = -r1 * z1 / z2 + math.pi / z2 * 1.0       # gear 2 turns opposite, phased to interdigitate
        im1 = raster(g1, r1, m * z1 / 2 + 8, m * z2 / 2 + 10, scale, size)
        im2 = raster(g2, r2, m * z1 / 2 + 8 + a, m * z2 / 2 + 10, scale, size)
        overlap = int((np.array(im1) & np.array(im2)).sum())
        worst = max(worst, overlap / (scale * scale))
    print(f"gear pair {z1}:{z2}: worst overlap over a full turn of the small gear = {worst:.2f} mm2 ->", "PASS" if worst < 1.5 else "FAIL (teeth interfere)")
    return worst < 1.5

if __name__ == "__main__":
    ok = test_cam("Peacock cam", 12, 120, 60, 120, 60) & test_cam("Ganesh cam", 25, 150, 30, 150, 30) & test_gears()
    sys.exit(0 if ok else 1)
