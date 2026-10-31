"""Tiny CAD helper: parts = dict name -> dict(poly=[closed polylines], circles=[(x,y,r)], engrave=[polylines]); nests on a sheet and writes SVG (mm) + DXF."""
import ezdxf
def bbox(part):
    xs = [p[0] for pl in part["poly"] for p in pl]; ys = [p[1] for pl in part["poly"] for p in pl]
    return min(xs), min(ys), max(xs), max(ys)
def move(part, dx, dy):
    f = lambda pl: [(x + dx, y + dy) for x, y in pl]
    return dict(poly=[f(p) for p in part["poly"]], circles=[(x + dx, y + dy, r) for x, y, r in part.get("circles", [])], engrave=[f(p) for p in part.get("engrave", [])])
def nest(parts, sheet_w, sheet_h, gap=5.0):
    """shelf nesting by decreasing height; returns placed parts and utilisation; raises if it does not fit"""
    items = sorted(parts.items(), key=lambda kv: -(bbox(kv[1])[3] - bbox(kv[1])[1]))
    x = y = gap; row_h = 0; placed = {}
    for name, p in items:
        x0, y0, x1, y1 = bbox(p); w, h = x1 - x0, y1 - y0
        if x + w + gap > sheet_w: x = gap; y += row_h + gap; row_h = 0
        if y + h + gap > sheet_h: raise ValueError(f"does not fit on {sheet_w}x{sheet_h}: {name}")
        placed[name] = move(p, x - x0, y - y0); x += w + gap; row_h = max(row_h, h)
    return placed
def overlap(placed):
    bs = [(n, bbox(p)) for n, p in placed.items()]; bad = []
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i][1], bs[j][1]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]: bad.append((bs[i][0], bs[j][0]))
    return bad
def write(placed, w, h, path_svg, path_dxf):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}"><g fill="none" stroke="red" stroke-width="0.2">']
    doc = ezdxf.new("R2010"); doc.units = 4; msp = doc.modelspace(); doc.layers.add("CUT", color=1); doc.layers.add("ENGRAVE", color=5)
    for n, p in placed.items():
        for pl in p["poly"]:
            s.append('<polygon points="%s"/>' % " ".join(f"{x:.3f},{y:.3f}" for x, y in pl)); msp.add_lwpolyline([(x, h - y) for x, y in pl], close=True, dxfattribs={"layer": "CUT"})
        for x, y, r in p.get("circles", []): s.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}"/>'); msp.add_circle((x, h - y), r, dxfattribs={"layer": "CUT"})
        for pl in p.get("engrave", []): s.append('<polyline stroke="blue" points="%s"/>' % " ".join(f"{x:.3f},{y:.3f}" for x, y in pl)); msp.add_lwpolyline([(x, h - y) for x, y in pl], dxfattribs={"layer": "ENGRAVE"})
        x0, y0, _, _ = bbox(p); s.append(f'<text x="{x0+1:.1f}" y="{y0+4:.1f}" font-size="3" fill="blue" stroke="none">{n}</text>')
    s.append("</g></svg>"); open(path_svg, "w").write("\n".join(s)); doc.saveas(path_dxf)
def rect(x, y, w, h): return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
