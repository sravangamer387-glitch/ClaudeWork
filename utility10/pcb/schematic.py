"""Netlist-style schematic writer: every pin gets a short wire stub and a net label (valid, ERC-checkable, not hand-drawn)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from sexp import *
def fmt(v): return ("%.4f" % v).rstrip("0").rstrip(".")
def build_schematic(name, parts, title, out_path, cols=3, dx=60.0, dy=50.0):
    root = uid(); libsyms = {}; body = []; grid = {}
    # place parts on a grid; big parts (more than 12 pins) get a whole cell row of their own
    x0, y0 = 40.0, 40.0; col = 0; row = 0; rowh = 0.0
    for p in parts:
        libname, symname = p["sym"].split(":")
        key = p["sym"]
        sym = resolve(libname, symname)
        if key not in libsyms:
            cp = parse(dump(sym)); cp[1] = Q(key)
            for e in cp:
                if isinstance(e, list) and e and e[0] == "extends": cp.remove(e)
            libsyms[key] = cp
        pn = pins(sym); npin = len(pn)
        # bounding box of pins
        xs = [v[1] for v in pn.values()]; ys = [v[2] for v in pn.values()]
        w = (max(xs) - min(xs)) + 30; h = (max(ys) - min(ys)) + 14
        if col and col >= cols or (col and x0 + col * dx + w > (380 if len(parts) <= 16 else 560)): col = 0; row += 1; y0 += rowh; rowh = 0
        cx = x0 + col * dx + (-min(xs) if min(xs) < 0 else 0) + 12; cy = y0 + (max(ys)) + 10
        rowh = max(rowh, h + 16)
        p["_pos"] = (cx, cy); col += 1 if w < dx else int(w // dx) + 1
        units = sorted({v[0] for v in pn.values() if v[0] != 0}) or [1]
        for u in units:
            ox, oy = (cx, cy + (u - 1) * 0)
            if u != units[0]: ox += 0; oy = cy + (max(ys) - min(ys)) + 14 + (u - 2) * 20
            props = [("Reference", p["ref"], 0, -2), ("Value", p["value"], 0, 2), ("Footprint", p.get("fp", ""), 0, 0), ("Datasheet", "~", 0, 0)]
            s = f'(symbol (lib_id "{key}") (at {fmt(ox)} {fmt(oy)} 0) (unit {u}) (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})'
            for k, v, a, b in props:
                hide = "" if k in ("Reference", "Value") else " hide"
                s += f' (property "{k}" "{v}" (at {fmt(ox + 8)} {fmt(oy + (-8 if k=="Reference" else -5.5))} 0) (effects (font (size 1.27 1.27)){hide}))'
            for num, v in pn.items():
                if v[0] in (0, u): s += f' (pin "{num}" (uuid {uid()}))'
            s += f' (instances (project "{name}" (path "/{root}" (reference "{p["ref"]}") (unit {u}))))'
            s += ")"
            body.append(s)
            for num, (pu, px, py, pa, ln, pname, ptype) in pn.items():
                if pu not in (0, u): continue
                net = p["nets"].get(num)
                ex, ey = ox + px, oy - py                       # connection point in schematic coordinates (y flipped)
                import math
                outx = round(-math.cos(math.radians(pa)))      # outward = opposite of the pin's stored direction
                outy = round(math.sin(math.radians(pa)))
                if net is None:
                    body.append(f'(no_connect (at {fmt(ex)} {fmt(ey)}) (uuid {uid()}))'); continue
                L = 3.81; lx, ly = ex + outx * L, ey + outy * L
                body.append(f'(wire (pts (xy {fmt(ex)} {fmt(ey)}) (xy {fmt(lx)} {fmt(ly)})) (stroke (width 0) (type default)) (uuid {uid()}))')
                ang = 0 if outx > 0 else 180 if outx < 0 else 90 if outy < 0 else 270
                just = "left" if outx > 0 or (outx == 0 and outy < 0) else "right"
                body.append(f'(label "{net}" (at {fmt(lx)} {fmt(ly)} {ang}) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid {uid()}))')
    # power flags on the supply nets named in the first part list
    pf = parse(dump(symbol("power", "PWR_FLAG"))); pf[1] = Q("power:PWR_FLAG"); libsyms["power:PWR_FLAG"] = pf
    ppins = pins(pf)
    flags = sorted({n for p in parts for n in p["nets"].values() if n and (n.startswith("+") or n in ("GND", "VBUS", "VBAT"))})
    for i, net in enumerate(flags):
        fx, fy = 40.0 + 20 * i, 270.0
        body.append(f'(symbol (lib_id "power:PWR_FLAG") (at {fmt(fx)} {fmt(fy)} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid {uid()}) (property "Reference" "#FLG0{i+1}" (at {fmt(fx)} {fmt(fy-3)} 0) (effects (font (size 1.27 1.27)) hide)) (property "Value" "PWR_FLAG" (at {fmt(fx)} {fmt(fy+3)} 0) (effects (font (size 1.27 1.27)) hide)) (property "Footprint" "" (at {fmt(fx)} {fmt(fy)} 0) (effects (font (size 1.27 1.27)) hide)) (property "Datasheet" "~" (at {fmt(fx)} {fmt(fy)} 0) (effects (font (size 1.27 1.27)) hide)) (pin "1" (uuid {uid()})) (instances (project "{name}" (path "/{root}" (reference "#FLG0{i+1}") (unit 1)))))')
        pyy = [v for v in ppins.values()][0]
        body.append(f'(wire (pts (xy {fmt(fx)} {fmt(fy)}) (xy {fmt(fx)} {fmt(fy+3.81)})) (stroke (width 0) (type default)) (uuid {uid()}))')
        body.append(f'(label "{net}" (at {fmt(fx)} {fmt(fy+3.81)} 270) (effects (font (size 1.27 1.27)) (justify right bottom)) (uuid {uid()}))')
    paper = 'A3' if len(parts) <= 16 else 'A2'
    text = f'(kicad_sch (version 20230121) (generator netlist_sch) (uuid {root}) (paper "{paper}") (title_block (title "{title}") (company "ClaudeWork")) (lib_symbols ' + " ".join(dump(v) for v in libsyms.values()) + ") " + " ".join(body) + f' (sheet_instances (path "/" (page "1"))))'
    open(out_path, "w").write(text)
