#!/usr/bin/env python3
"""Generate laser-cut SVGs (units: mm) for the gravity-toys designs.

Usage: python3 -I generate_laser_svgs.py <output_dir>

Outputs:
  galton_front_acrylic.svg   5 mm acrylic window + bin-wall slots
  galton_back_mdf.svg        6 mm MDF back panel with peg holes
  marble_tower_plate.svg     100x100 plate with 4 post holes and a 28 mm U-groove guide line
  ramp_racer_ramp.svg        1200 x 140 ply ramp with lane guides
Colour convention: red = cut, blue = score/engrave.
"""
import math
import sys
from pathlib import Path

CUT, SCORE = "#ff0000", "#0000ff"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" '
            f'viewBox="0 0 {w} {h}">\n{body}\n</svg>\n')


def rect(x, y, w, h, c=CUT, r=0):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r}" '
            f'fill="none" stroke="{c}" stroke-width="0.1"/>')


def circle(x, y, d, c=CUT):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{d / 2:.2f}" fill="none" stroke="{c}" stroke-width="0.1"/>'


def line(x1, y1, x2, y2, c=SCORE):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="0.1"/>'


def galton(rows=10, pitch=24.0, peg_d=4.0, ball_d=12.0, panel_w=300.0, panel_h=420.0):
    assert pitch - peg_d >= 1.5 * ball_d, "gap too small: balls will jam"
    row_h = pitch * math.sqrt(3) / 2
    bins = rows + 1
    x0 = (panel_w - bins * pitch) / 2
    top = 70.0  # space for funnel
    pegs = []
    for r in range(rows):
        n = r + 1
        y = top + r * row_h
        for k in range(n):
            x = panel_w / 2 + (k - (n - 1) / 2) * pitch
            pegs.append((x, y))
    bin_top = top + rows * row_h + 10
    bin_bot = panel_h - 25
    # back panel: outline + peg holes (slightly undersized 3.9 for press fit) + bin guide marks
    back = [rect(0, 0, panel_w, panel_h, r=4)]
    back += [circle(x, y, peg_d - 0.1) for x, y in pegs]
    back += [line(x0 + i * pitch, bin_top, x0 + i * pitch, bin_bot) for i in range(bins + 1)]
    # front window: outline + 3 mm slots for bin walls (3 mm acrylic dividers are cut separately)
    front = [rect(0, 0, panel_w, panel_h, r=4)]
    front += [rect(x0 + i * pitch - 1.5, bin_bot - 3, 3, 8) for i in range(bins + 1)]
    funnel_w = 30
    front += [circle(panel_w / 2, 40, 12, SCORE),
              rect(panel_w / 2 - funnel_w / 2, 30, funnel_w, 3, SCORE)]
    return (svg(panel_w, panel_h, "\n".join(back)), svg(panel_w, panel_h, "\n".join(front)),
            len(pegs))


def tower_plate(size=100.0, post=20.0, groove_w=28.0, ball_d=25.0):
    assert groove_w >= ball_d + 2, "groove must clear ball by >=1 mm"
    body = [rect(0, 0, size, size, r=3)]
    off = 12.0
    for cx in (off + post / 2, size - off - post / 2):
        for cy in (off + post / 2, size - off - post / 2):
            body.append(rect(cx - post / 2 - 0.15, cy - post / 2 - 0.15, post + 0.3, post + 0.3))
    # CNC groove centreline (engrave layer): diagonal-ish run across the plate
    body.append(line(size / 2, 5, size / 2, size - 5))
    body.append(f'<text x="2" y="{size - 2}" font-size="3" fill="{SCORE}">groove {groove_w} wide x 12 deep</text>')
    return svg(size, size, "\n".join(body))


def ramp(length=1200.0, width=140.0, lane=60.0, rail=6.0):
    body = [rect(0, 0, length, width, r=5)]
    body += [line(0, rail, length, rail), line(0, width - rail, length, width - rail),
             line(0, width / 2, length, width / 2)]
    return svg(length, width, "\n".join(body))


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    back, front, n = galton()
    (out / "galton_back_mdf.svg").write_text(back)
    (out / "galton_front_acrylic.svg").write_text(front)
    (out / "marble_tower_plate.svg").write_text(tower_plate())
    (out / "ramp_racer_ramp.svg").write_text(ramp())
    print(f"wrote 4 files to {out}; galton pegs={n} (expected 55)")
    print("ramp rises (mm):", {d: round(1200 * math.sin(math.radians(d))) for d in (5, 10, 15, 20, 25)})
    print("galton bin probs:", [round(math.comb(10, k) / 1024, 3) for k in range(11)])


if __name__ == "__main__":
    main()
