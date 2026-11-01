"""ASTRADAND laser/print files: display stand (6 mm MDF), carton dieline (350 gsm board), spell cards (63 x 88 mm). SVG + DXF. Units mm, red = cut, blue = fold/engrave."""
import os, math, sys
import ezdxf
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
class Sheet:
    def __init__(s, w, h): s.w, s.h, s.cut, s.fold, s.txt = w, h, [], [], []
    def poly(s, pts, close=True, kind="cut"): (s.cut if kind == "cut" else s.fold).append((list(pts), close))
    def rect(s, x, y, w, h, kind="cut"): s.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], True, kind)
    def circle(s, cx, cy, r, kind="cut"): n = 48; s.poly([(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)], True, kind)
    def text(s, x, y, t, size=3): s.txt.append((x, y, t, size))
    def save(s, base):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}mm" height="{s.h}mm" viewBox="0 0 {s.w} {s.h}">']
        svg.append('<g fill="none" stroke="red" stroke-width="0.2">'); doc = ezdxf.new("R2010"); doc.layers.add("CUT", color=1); doc.layers.add("FOLD", color=5); msp = doc.modelspace()
        for pts, cl in s.cut: svg.append(('<polygon' if cl else '<polyline') + ' points="' + " ".join(f"{x:.3f},{y:.3f}" for x, y in pts) + '"/>'); msp.add_lwpolyline([(x, s.h - y) for x, y in pts], close=cl, dxfattribs={"layer": "CUT"})
        svg.append('</g><g fill="none" stroke="blue" stroke-width="0.2" stroke-dasharray="2,1">')
        for pts, cl in s.fold: svg.append(('<polygon' if cl else '<polyline') + ' points="' + " ".join(f"{x:.3f},{y:.3f}" for x, y in pts) + '"/>'); msp.add_lwpolyline([(x, s.h - y) for x, y in pts], close=cl, dxfattribs={"layer": "FOLD"})
        svg.append('</g>')
        for x, y, t, sz in s.txt: svg.append(f'<text x="{x}" y="{y}" font-size="{sz}" fill="blue" stroke="none">{t}</text>')
        svg.append("</svg>"); open(base + ".svg", "w").write("\n".join(svg)); doc.saveas(base + ".dxf")
# ---------------- display stand: base + two cradle uprights (6 mm MDF, finger-joint tabs) ----------------
T = 6.0; KERF = 0.1; BL, BW = 280.0, 100.0; UP_W, UP_H = 76.0, 70.0; R_NOTCH = 18.4; XS = (55.0, 225.0)
s = Sheet(420, 300)
bx, by = 5, 5; pts = [(bx, by), (bx + BL, by), (bx + BL, by + BW), (bx, by + BW)]; s.poly(pts)
for xc in XS:                                                                     # slots for the upright tabs (width T, length 40)
    s.rect(bx + xc - 20, by + BW / 2 - (T + KERF) / 2, 40, T + KERF)
for i, xc in enumerate(XS):
    ox, oy = 5 + i * (UP_W + 6), 125
    p = [(ox, oy + UP_H), (ox, oy + 6)]                                           # upright: tab at bottom, semicircular notch at top (wand cradle)
    outline = [(ox + 18, oy + UP_H), (ox, oy + UP_H), (ox, oy + 6)]
    outline += [(ox + (UP_W - 40) / 2, oy + 6), (ox + (UP_W - 40) / 2, oy), (ox + (UP_W + 40) / 2, oy), (ox + (UP_W + 40) / 2, oy + 6), (ox + UP_W, oy + 6), (ox + UP_W, oy + UP_H)]
    arc = [(ox + UP_W / 2 + R_NOTCH * math.cos(math.pi * k / 24), oy + UP_H - 0.0 - R_NOTCH * math.sin(math.pi * k / 24)) for k in range(25)]
    s.poly(outline[:-1] + [(ox + UP_W, oy + UP_H)] + arc[::-1][:0] + [(ox + UP_W / 2 + R_NOTCH, oy + UP_H)] + arc + [(ox + UP_W / 2 - R_NOTCH, oy + UP_H)], True)
s.text(8, 118, "ASTRADAND display stand: 6 mm MDF, cradles hold the 34 mm hilt (notch r 18.4). Cut layer red.", 3)
s.save(os.path.join(OUT, "stand_laser"))
# ---------------- straight-tuck carton dieline: inside 250 x 64 x 54 mm, 350 gsm ----------------
L, Wd, Hd, G, TK, DUST, CH = 250.0, 64.0, 54.0, 14.0, 16.0, 22.0, 4.0
widths = [("glue", G), ("front", Wd), ("side1", Hd), ("back", Wd), ("side2", Hd)]
y0 = 10 + TK + CH; c = Sheet(G + 2 * Wd + 2 * Hd + 20, L + 2 * (TK + CH) + 20)
xs = [10.0]
for _, w in widths: xs.append(xs[-1] + w)
depth_top = {"glue": 0, "front": 0, "side1": DUST, "back": TK + CH, "side2": DUST}           # tuck flap on the back panel, dust flaps on the sides
top = []; bot = []
for k, (nm, w) in enumerate(widths):
    a, b = xs[k], xs[k + 1]; d = depth_top[nm]
    if nm == "glue": top += [(a, y0 + 6), (b, y0)]; bot += [(a, y0 + L - 6), (b, y0 + L)]
    elif d == 0: top += [(a, y0), (b, y0)]; bot += [(a, y0 + L), (b, y0 + L)]
    else:
        top += [(a, y0), (a, y0 - d + CH), (a + CH, y0 - d), (b - CH, y0 - d), (b, y0 - d + CH), (b, y0)]
        bot += [(a, y0 + L), (a, y0 + L + d - CH), (a + CH, y0 + L + d), (b - CH, y0 + L + d), (b, y0 + L + d - CH), (b, y0 + L)]
c.poly(top + [(xs[5], y0 + L)] + bot[::-1], True)
for k in range(1, 5): c.poly([(xs[k], y0), (xs[k], y0 + L)], False, "fold")
c.poly([(xs[1], y0), (xs[5], y0)], False, "fold"); c.poly([(xs[1], y0 + L), (xs[5], y0 + L)], False, "fold")
c.text(xs[1] + 3, y0 + L / 2, "ASTRADAND carton, inside 250 x 64 x 54 mm, 350 gsm board; red = cut, blue = fold; glue flap 14 mm", 3)
c.text(xs[1] + 3, y0 + L / 2 + 6, "panels: front | side | back (tuck flaps) | side. Print artwork on the outside face.", 3)
c.save(os.path.join(OUT, "carton_dieline"))
print("stand_laser and carton_dieline written")
