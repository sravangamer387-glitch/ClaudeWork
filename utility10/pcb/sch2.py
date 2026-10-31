"""Readable schematic generator v2: placed symbols (rotatable), power symbols on supply pins, explicit wires for local connections,
net labels elsewhere, dashed block frames with titles, notes, title block. Output: KiCad 7 .kicad_sch"""
import sys, os, math; sys.path.insert(0, os.path.dirname(__file__))
from sexp import *
def f(v): return ("%.3f" % v).rstrip("0").rstrip(".")
POWER_SYM = {"GND": ("power:GND", "down"), "+3V0": ("power:+3V3", "up"), "+5V": ("power:+5V", "up"), "+4V5": ("power:+5V", "up"), "VBUS": ("power:VBUS", "up"), "BAT_P": ("power:+BATT", "up"), "+BATT": ("power:+BATT", "up")}
def rot_pin(px, py, a, rot):
    r = math.radians(rot); rx = px * math.cos(r) - py * math.sin(r); ry = px * math.sin(r) + py * math.cos(r)
    return rx, ry
def out_dir(pin_angle, rot):
    a = math.radians(pin_angle + 180 + rot); return round(math.cos(a)), round(-math.sin(a))      # schematic coordinates (y down)
def build(name, parts, S, title, rev, date, out_path):
    root = uid(); libsyms = {}; body = []; endpoints = {}
    def need(key):
        if key not in libsyms:
            l, n = key.split(":"); cp = parse(dump(resolve(l, n))); cp[1] = Q(key)
            cp[:] = [e for e in cp if not (isinstance(e, list) and e and e[0] == "extends")]; libsyms[key] = cp
        return pins(resolve(*key.split(":")))
    def symbol_inst(key, ref, value, fp, x, y, rot, unit, pinlist, hide_ref=False, props_at=None):
        s = f'(symbol (lib_id "{key}") (at {f(x)} {f(y)} {int(rot)}) (unit {unit}) (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})'
        px, py = props_at or (x + 3.0, y - 4.0)
        s += f' (property "Reference" "{ref}" (at {f(px)} {f(py)} 0) (effects (font (size 1.27 1.27)) (justify left){" hide" if hide_ref else ""}))'
        s += f' (property "Value" "{value}" (at {f(px)} {f(py + 2.54)} 0) (effects (font (size 1.27 1.27)) (justify left)))'
        s += f' (property "Footprint" "{fp}" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))'
        s += f' (property "Datasheet" "~" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))'
        for num in pinlist: s += f' (pin "{num}" (uuid {uid()}))'
        s += f' (instances (project "{name}" (path "/{root}" (reference "{ref}") (unit {unit}))))'
        return s + ")"
    def wire(a, b): body.append(f'(wire (pts (xy {f(a[0])} {f(a[1])}) (xy {f(b[0])} {f(b[1])})) (stroke (width 0) (type default)) (uuid {uid()}))')
    def label(net, p, d, glob=False):
        ang = 0 if d[0] > 0 else 180 if d[0] < 0 else 90 if d[1] < 0 else 270
        just = "left" if d[0] > 0 or (d[0] == 0 and d[1] < 0) else "right"
        body.append(f'(label "{net}" (at {f(p[0])} {f(p[1])} {ang}) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid {uid()}))')
    pwr_count = 0; pinpos = {}
    for p in parts:
        pn = need(p["sym"]); x, y, rot = S["place"][p["ref"]]
        units = sorted({v[0] for v in pn.values() if v[0] != 0}) or [1]
        for ui, u in enumerate(units):
            ox, oy = (x, y) if ui == 0 else S["place"].get(p["ref"] + f"#{u}", (x + 40, y, rot))[:2]
            urot = rot if ui == 0 else S["place"].get(p["ref"] + f"#{u}", (0, 0, rot))[2]
            body.append(symbol_inst(p["sym"], p["ref"], p["value"], p["fp"], ox, oy, urot, u, [n for n, v in pn.items() if v[0] in (0, u)], False, p.get("ref_at") and (ox + p["ref_at"][0], oy + p["ref_at"][1])))
            for num, (pu, qx, qy, qa, ln, pname, ptype) in pn.items():
                if pu not in (0, u): continue
                rx, ry = rot_pin(qx, qy, qa, urot); ex, ey = ox + rx, oy - ry
                d = out_dir(qa, urot); net = p["nets"].get(num); pinpos[(p["ref"], num)] = ((ex, ey), d, net)
                if net is None:
                    body.append(f'(no_connect (at {f(ex)} {f(ey)}) (uuid {uid()}))'); continue
    wired = set()
    auto = {}
    for (ref, num), (pt, d, net) in pinpos.items():
        if net and net not in POWER_SYM: auto.setdefault(net, []).append((ref, num))
    def seg_hit(s1, s2, tol=0.4):
        """axis-aligned segments closer than tol (touching/crossing)"""
        (ax0, ay0), (ax1, ay1) = s1; (bx0, by0), (bx1, by1) = s2
        return min(max(ax0, ax1), max(bx0, bx1)) - max(min(ax0, ax1), min(bx0, bx1)) > -tol and min(max(ay0, ay1), max(by0, by1)) - max(min(ay0, ay1), min(by0, by1)) > -tol
    stub = {k: (v[0], (v[0][0] + v[1][0] * 3.81, v[0][1] + v[1][1] * 3.81)) for k, v in pinpos.items() if v[2]}
    accepted = []; S["_wires_auto"] = []
    seen_ = set()
    for (ref, num), (pt, d, net) in pinpos.items():                       # keep auto-wires away from the PWR_FLAG symbols that are placed later
        if net in POWER_SYM and net not in seen_ and net not in S.get("no_flag", ()):
            seen_.add(net); fx, fy = pt[0] + d[0] * 5.08, pt[1] + d[1] * 5.08 + (3.81 if d[1] == 0 else 0)
            accepted += [((fx - 3.0, fy - 4.0), (fx + 3.0, fy - 4.0)), ((fx - 3.0, fy + 5.0), (fx + 3.0, fy + 5.0)), ((fx, fy - 4.0), (fx, fy + 5.0)), ((fx - 3.0, fy - 4.0), (fx - 3.0, fy + 5.0)), ((fx + 3.0, fy - 4.0), (fx + 3.0, fy + 5.0))]
    for net, pl in auto.items():
        if len(pl) != 2 or not S.get("auto_wire", True) or pl[0][0] == pl[1][0]: continue
        (a, da, _), (b, db, _) = pinpos[pl[0]], pinpos[pl[1]]
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) > S.get("auto_wire_max", 70): continue
        a2 = (a[0] + da[0] * 2.54, a[1] + da[1] * 2.54); b2 = (b[0] + db[0] * 2.54, b[1] + db[1] * 2.54)
        for mid in ((b2[0], a2[1]), (a2[0], b2[1])):
            segs = [(a2, mid), (mid, b2)]
            if any(seg_hit(sg, st) for sg in segs for k, st in stub.items() if k not in pl) : continue
            if any(seg_hit(sg, (pp[0], pp[0])) for sg in segs for k, pp in pinpos.items() if k not in pl): continue
            if any(seg_hit(sg, ac) for sg in segs for ac in accepted): continue
            accepted += segs + [(a, a2), (b, b2)]; S["_wires_auto"].append((pl[0][0], pl[0][1], pl[1][0], pl[1][1], mid)); break
    S["wires"] = list(S.get("wires", [])) + [w[:4] for w in S["_wires_auto"]]
    S["_mid"] = {w[:4]: w[4] for w in S["_wires_auto"]}
    for (r1, p1, r2, p2) in S.get("wires", []):
        (a, da, na), (b, db, nb) = pinpos[(r1, p1)], pinpos[(r2, p2)]
        assert na == nb, f"wire between different nets {r1}.{p1} {na} / {r2}.{p2} {nb}"
        L = 2.54; a2 = (a[0] + da[0] * L, a[1] + da[1] * L); b2 = (b[0] + db[0] * L, b[1] + db[1] * L)
        wire(a, a2); wire(b, b2)
        mid = S.get("_mid", {}).get((r1, p1, r2, p2)) or ((b2[0], a2[1]) if S.get("wire_hfirst", True) else (a2[0], b2[1]))
        if a2 != mid: wire(a2, mid)
        if mid != b2: wire(mid, b2)
        label(na, mid, (1, 0)); wired.add((r1, p1)); wired.add((r2, p2))
    for (ref, num), (pt, d, net) in pinpos.items():
        if net is None or (ref, num) in wired: continue
        if net in POWER_SYM:
            key, body_dir = POWER_SYM[net]; need(key); L = 2.54
            end = (pt[0] + d[0] * L, pt[1] + d[1] * L); wire(pt, end)
            want = d                                                       # the symbol body should extend away from the pin
            if body_dir == "down": rot = {(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270}[want]
            else: rot = {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270}[want]
            pwr_count += 1
            sp = parse(dump(symbol(*key.split(":")))); pin0 = list(pins(resolve(*key.split(":"))).values())[0]
            rx, ry = rot_pin(pin0[1], pin0[2], pin0[3], rot)
            ox, oy = end[0] - rx, end[1] + ry
            body.append(symbol_inst(key, f"#PWR0{pwr_count}", net, "", ox, oy, rot, 1, ["1"], hide_ref=True, props_at=(end[0] + 1, end[1] - 1)))
            continue
        L = 3.81; end = (pt[0] + d[0] * L, pt[1] + d[1] * L); wire(pt, end); label(net, end, d)
    # PWR_FLAG on supply nets (once each, near the first pin of the net)
    need("power:PWR_FLAG"); flagged = set(); fl = 0
    for (ref, num), (pt, d, net) in pinpos.items():
        if net in POWER_SYM and net not in flagged and net not in S.get("no_flag", ()):
            flagged.add(net); fl += 1
            L = 5.08; fx, fy = pt[0] + d[0] * L, pt[1] + d[1] * L + (3.81 if d[1] == 0 else 0)
            fp0 = list(pins(resolve("power", "PWR_FLAG")).values())[0]
            pw = (fx, fy)
            body.append(symbol_inst("power:PWR_FLAG", f"#FLG0{fl}", "PWR_FLAG", "", fx, fy, 0, 1, ["1"], hide_ref=True, props_at=(fx + 1, fy - 3)))
            wire(pw, (fx, fy + 3.81)); label(net, (fx, fy + 3.81), (0, 1))
    for b in S.get("blocks", []):
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        body.append(f'(rectangle (start {f(x)} {f(y)}) (end {f(x + w)} {f(y + h)}) (stroke (width 0.2) (type dash)) (fill (type none)) (uuid {uid()}))')
        body.append(f'(text "{b["title"]}" (at {f(x + 1.5)} {f(y + 3.0)} 0) (effects (font (size 2 2) bold) (justify left)) (uuid {uid()}))')
    for (t, x, y) in S.get("notes", []):
        body.append(f'(text "{t}" (at {f(x)} {f(y)} 0) (effects (font (size 1.5 1.5)) (justify left)) (uuid {uid()}))')
    tb = f'(title_block (title "{title}") (date "{date}") (rev "{rev}") (company "ClaudeWork") (comment 1 "First engineering release; see pcb/README.md for status and limits"))'
    text = f'(kicad_sch (version 20230121) (generator sch2) (uuid {root}) (paper "{S.get("paper", "A3")}") {tb} (lib_symbols ' + " ".join(dump(v) for v in libsyms.values()) + ") " + " ".join(body) + f' (sheet_instances (path "/" (page "1"))))'
    open(out_path, "w").write(text)
