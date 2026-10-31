"""Rangoli Spiro Gears: hypotrochoid pen curves from a fixed ring gear (R teeth) and a rolling wheel (r teeth), pen hole d mm from wheel centre.
Verifies: the curve closes after r/gcd wheel turns, lobes = R/gcd, pen stays inside ring, and writes SVG gear parts (trapezoid teeth, module 2 mm)."""
import math, os, sys
import numpy as np
OUT = os.path.join(os.path.dirname(__file__), "..", "out"); M = 2.0
COMBOS = [(96, 40, 0.8), (96, 32, 0.7), (96, 45, 0.75), (84, 35, 0.7), (96, 56, 0.8), (105, 63, 0.7), (96, 24, 0.9), (72, 30, 0.8)]
def curve(R, r, pen, n=6000):
    Rm, rm = R * M / 2, r * M / 2; d = pen * rm
    turns = r // math.gcd(R, r); t = np.linspace(0, 2 * math.pi * turns, n * turns + 1)
    k = (Rm - rm) / rm
    return (Rm - rm) * np.cos(t) + d * np.cos(k * t), (Rm - rm) * np.sin(t) - d * np.sin(k * t), turns, Rm, d
def lobes(x, y):
    """lobes = upward crossings of the mid radius (robust: peak-picking fails on flat float plateaus near maxima)"""
    rad = np.hypot(x, y); mid = (rad.max() + rad.min()) / 2; above = rad > mid
    return int((above & ~np.roll(above, 1)).sum())
lines = ["| ring/wheel teeth | pen hole (fraction of wheel radius) | wheel turns to close | lobes counted | lobes expected R/gcd | closes? | max radius vs ring pitch radius |", "|---|---|---|---|---|---|---|"]
ok = True
for R, r, pen in COMBOS:
    x, y, turns, Rm, d = curve(R, r, pen); g = math.gcd(R, r)
    gap = math.hypot(x[-1] - x[0], y[-1] - y[0]); n = lobes(x[:-1], y[:-1]); exp = R // g if R // g != 1 else 1
    closes = gap < 1e-6; inside = np.hypot(x, y).max() < Rm
    ok &= closes and inside and (n == exp)
    lines.append(f"| {R}/{r} | {pen} | {turns} | {n} | {exp} | {'yes' if closes else 'NO'} | {np.hypot(x,y).max():.1f} < {Rm:.1f} mm |")
# gear cut parts
def gear(teeth, ring=False, cx=0, cy=0):
    rp = teeth * M / 2; add, ded = M, 1.25 * M; pts = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth; pitch = 2 * math.pi / teeth
        for frac, rad in ((0.0, rp - ded if not ring else rp + ded), (0.25, rp - ded if not ring else rp + ded), (0.40, rp + add if not ring else rp - add), (0.60, rp + add if not ring else rp - add), (0.75, rp - ded if not ring else rp + ded)):
            a = a0 + frac * pitch; pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="620mm" height="420mm" viewBox="0 0 620 420"><g fill="none" stroke="red" stroke-width="0.2">']
svg.append(f'<path d="{gear(96, True, 110, 110)}"/><circle cx="110" cy="110" r="{96*M/2+8}"/>')
cx = 250
for r in (24, 32, 40, 45, 56, 63):
    svg.append(f'<path d="{gear(r, False, cx, 120)}"/>')
    for k in range(1, 9):
        svg.append(f'<circle cx="{cx + k*(r*M/2*0.9)/8:.2f}" cy="120" r="1.6"/>')    # pen holes along a radius, 1.6 mm for a 0.7 mm pen tip? see README: use 3 mm hole for pens
    cx += r * M + 10
svg.append("</g></svg>")
open(os.path.join(OUT, "spiro_parts.svg"), "w").write("\n".join(svg))
# preview PNG
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 4, figsize=(12, 6))
for a, (R, r, pen) in zip(ax.flat, COMBOS):
    x, y, *_ = curve(R, r, pen, 800); a.plot(x, y, lw=0.6); a.set_aspect("equal"); a.axis("off"); a.set_title(f"{R}/{r}", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "spiro_previews.png"), dpi=110)
res = "\n".join(lines) + f"\n\nAll curves verified closed, inside the ring and with the expected lobe count: {ok}.\nGear pitch radius = teeth x 2 mm / 2; ring inner diameter for 96 teeth = {96*M:.0f} mm pitch (cut area about {96*M+10:.0f} mm). Tooth shape is a simple trapezoid (not involute): good enough for a hand-driven toy; clearance 0.25 mm per flank to be tuned for the laser kerf."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_spiro.md"), "w").write(res + "\n"); print(res); sys.exit(0 if ok else 1)
