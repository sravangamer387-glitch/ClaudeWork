"""Readable schematic generator v2: placed symbols (rotatable), power symbols on supply pins, explicit wires for local connections,
net labels elsewhere, dashed block frames with titles, notes, title block. Output: KiCad 7 .kicad_sch"""
import sys, os, math, re; sys.path.insert(0, os.path.dirname(__file__))
from sexp import *
def f(v): return ("%.3f" % v).rstrip("0").rstrip(".")
POWER_SYM = {"GND": ("power:GND", "down"), "+3V3": ("power:+3V3", "up"), "+3V0": ("power:+3V3", "up"), "+5V": ("power:+5V", "up"), "+4V5": ("power:+5V", "up"), "VBUS": ("power:VBUS", "up"), "BAT_P": ("power:+BATT", "up"), "+BATT": ("power:+BATT", "up")}
def rot_pin(px, py, a, rot):
    r = math.radians(rot); rx = px * math.cos(r) - py * math.sin(r); ry = px * math.sin(r) + py * math.cos(r)
    return rx, ry
def out_dir(pin_angle, rot):
    a = math.radians(pin_angle + 180 + rot); return round(math.cos(a)), round(-math.sin(a))      # schematic coordinates (y down)
def build(name, parts, S, title, rev, date, out_path):
    root = uid(); libsyms = {}; body = []; endpoints = {}
    W = []; BOD = []; FIX = []; FLD = []
    def need(key):
        if key not in libsyms:
            l, n = key.split(":"); cp = parse(dump(resolve(l, n))); cp[1] = Q(key)
            cp[:] = [e for e in cp if not (isinstance(e, list) and e and e[0] == "extends")]; libsyms[key] = cp
        return pins(resolve(*key.split(":")))
    def symbol_inst(key, ref, value, fp, x, y, rot, unit, pinlist, hide_ref=False, props_at=None):
        s = f'(symbol (lib_id "{key}") (at {f(x)} {f(y)} {int(rot)}) (unit {unit}) (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})'
        tk = len(FLD); FLD.append(dict(ref=ref, value=value, hide_ref=hide_ref, hide_val=(key == "power:PWR_FLAG"), fixed=props_at, pos=(x, y), key=key, n=tk, owner=(ref, unit), rot=int(rot) % 360))
        s += f' (property "Reference" "{ref}" @@R{tk}@@)'
        s += f' (property "Value" "{value}" @@V{tk}@@)'
        s += f' (property "Footprint" "{fp}" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))'
        s += f' (property "Datasheet" "~" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))'
        for num in pinlist: s += f' (pin "{num}" (uuid {uid()}))'
        s += f' (instances (project "{name}" (path "/{root}" (reference "{ref}") (unit {unit}))))'
        return s + ")"
    def wire(a, b): W.append((a, b)); body.append(f'(wire (pts (xy {f(a[0])} {f(a[1])}) (xy {f(b[0])} {f(b[1])})) (stroke (width 0) (type default)) (uuid {uid()}))')
    def label(net, p, d, glob=False):
        ang = 0 if d[0] > 0 else 180 if d[0] < 0 else 90 if d[1] < 0 else 270
        just = "left" if d[0] > 0 or (d[0] == 0 and d[1] < 0) else "right"
        FIX.append(tbox(net, p, d))
        body.append(f'(label "{net}" (at {f(p[0])} {f(p[1])} {ang}) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid {uid()}))')
    CW = 1.2
    def inter0(a, b, m=0.12): return a[0] < b[2] - m and b[0] < a[2] - m and a[1] < b[3] - m and b[1] < a[3] - m
    def tbox(txt, p, d):
        w = len(txt) * CW + 0.3
        if d[0] > 0: return (p[0], p[1] - 1.9, p[0] + w, p[1] + 0.25)
        if d[0] < 0: return (p[0] - w, p[1] - 1.9, p[0], p[1] + 0.25)
        if d[1] < 0: return (p[0] - 1.7, p[1] - w, p[0] + 0.1, p[1])
        return (p[0] - 0.1, p[1], p[0] + 1.7, p[1] + w)
    pwr_count = 0; pinpos = {}
    for p in parts:
        pn = need(p["sym"]); x, y, rot = S["place"][p["ref"]]
        units = sorted({v[0] for v in pn.values() if v[0] != 0}) or [1]
        for ui, u in enumerate(units):
            ox, oy = (x, y) if ui == 0 else S["place"].get(p["ref"] + f"#{u}", (x + 40, y, rot))[:2]
            urot = rot if ui == 0 else S["place"].get(p["ref"] + f"#{u}", (0, 0, rot))[2]
            body.append(symbol_inst(p["sym"], p["ref"], p["value"], p["fp"], ox, oy, urot, u, [n for n, v in pn.items() if v[0] in (0, u)], False, p.get("ref_at") and (ox + p["ref_at"][0], oy + p["ref_at"][1])))
            ends_ = []
            for num, (pu, qx, qy, qa, ln, pname, ptype) in pn.items():
                if pu not in (0, u): continue
                rx, ry = rot_pin(qx, qy, qa, urot); ex, ey = ox + rx, oy - ry; ends_.append((ex, ey)); dd_ = out_dir(qa, urot); ends_.append((ex - dd_[0] * (ln + 1.0), ey - dd_[1] * (ln + 1.0)))
                d = out_dir(qa, urot); net = p["nets"].get(num); pinpos[(p["ref"], num)] = ((ex, ey), d, net)
                if net is None:
                    body.append(f'(no_connect (at {f(ex)} {f(ey)}) (uuid {uid()}))'); continue
            if ends_:
                xs_ = [e[0] for e in ends_]; ys_ = [e[1] for e in ends_]; cx_, cy_ = (min(xs_) + max(xs_)) / 2, (min(ys_) + max(ys_)) / 2
                hw_ = max((max(xs_) - min(xs_)) / 2, 2.1) + 1.2; hh_ = max((max(ys_) - min(ys_)) / 2, 2.1) + 0.8; BOD.append(((p["ref"], u), (cx_ - hw_, cy_ - hh_, cx_ + hw_, cy_ + hh_)))
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
        if len(pl) != 2 or not S.get("auto_wire", True) or pl[0][0] == pl[1][0] or net in S.get("no_auto", ()): continue
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
        segs_ = [(a2, mid), (mid, b2)]; segs_ = [sg for sg in segs_ if sg[0] != sg[1]] or [(a, a2)]; sg = max(segs_, key=lambda q: abs(q[0][0] - q[1][0]) + abs(q[0][1] - q[1][1]))
        anc = ((sg[0][0] + sg[1][0]) / 2, (sg[0][1] + sg[1][1]) / 2)
        label(na, anc, (1, 0) if sg[0][1] == sg[1][1] else (0, -1)); wired.add((r1, p1)); wired.add((r2, p2))
    clus = {}                                                              # adjacent pins on the same power net in one row share one power symbol
    groups_ = {}
    for (ref, num), (pt, d, net) in pinpos.items():
        if net in POWER_SYM and (ref, num) not in wired:
            groups_.setdefault((net, d, round(pt[1], 2) if d[0] == 0 else round(pt[0], 2)), []).append(((ref, num), pt))
    for (net, d, _), lst in groups_.items():
        lst.sort(key=lambda t: t[1][0] if d[0] == 0 else t[1][1]); run = [lst[0]]
        for it in lst[1:] + [None]:
            if it is not None and abs((it[1][0] - run[-1][1][0]) if d[0] == 0 else (it[1][1] - run[-1][1][1])) <= 5.1: run.append(it); continue
            lead = run[len(run) // 2]
            for k_, _pt in run: clus[k_] = (lead[0], run)
            if it is not None: run = [it]
    for (ref, num), (pt, d, net) in pinpos.items():
        if net is None or (ref, num) in wired: continue
        if net in POWER_SYM:
            key, body_dir = POWER_SYM[net]; need(key); L = 2.54
            end = (pt[0] + d[0] * L, pt[1] + d[1] * L); wire(pt, end)
            if (ref, num) in clus and len(clus[(ref, num)][1]) > 1:
                lead_k, run_ = clus[(ref, num)]
                if (ref, num) != lead_k:
                    lp = pinpos[lead_k][0]; lend = (lp[0] + d[0] * L, lp[1] + d[1] * L)
                    nb = [q for q in run_ if q[0] != (ref, num)]; 
                    idx = [q[0] for q in run_].index((ref, num)); lidx = [q[0] for q in run_].index(lead_k)
                    nxt = run_[idx + (1 if lidx > idx else -1)][1]; nend = (nxt[0] + d[0] * L, nxt[1] + d[1] * L)
                    wire(end, nend); body.append(f'(junction (at {f(end[0])} {f(end[1])}) (diameter 0) (color 0 0 0 0) (uuid {uid()}))')
                    continue
            want = d                                                       # the symbol body should extend away from the pin
            if body_dir == "down": rot = {(0, 1): 0, (1, 0): 90, (0, -1): 180, (-1, 0): 270}[want]
            else: rot = {(0, -1): 0, (-1, 0): 90, (0, 1): 180, (1, 0): 270}[want]
            pwr_count += 1
            sp = parse(dump(symbol(*key.split(":")))); pin0 = list(pins(resolve(*key.split(":"))).values())[0]
            rx, ry = rot_pin(pin0[1], pin0[2], pin0[3], rot)
            ox, oy = end[0] - rx, end[1] + ry
            bx0, bx1 = min(end[0], end[0] + d[0] * 3.2) - 1.3, max(end[0], end[0] + d[0] * 3.2) + 1.3; by0, by1 = min(end[1], end[1] + d[1] * 3.2) - 1.3, max(end[1], end[1] + d[1] * 3.2) + 1.3
            BOD.append((("#PWR", pwr_count), (bx0, by0, bx1, by1)))
            body.append(symbol_inst(key, f"#PWR0{pwr_count}", net, "", ox, oy, rot, 1, ["1"], hide_ref=True, props_at=("PW", end, d)))
            continue
        L = 3.81; end = (pt[0] + d[0] * L, pt[1] + d[1] * L); wire(pt, end); label(net, end, d)
    # PWR_FLAG on supply nets (once each, near the first pin of the net)
    need("power:PWR_FLAG"); flagged = set(); fl = 0
    for (ref, num), (pt, d, net) in pinpos.items():
        if net in POWER_SYM and net not in flagged and net not in S.get("no_flag", ()):
            flagged.add(net); fl += 1
            def flag_cost(fx, fy):
                bx = (fx - 1.8, fy - 0.3, fx + 1.8, fy + 3.2); lb = tbox(net, (fx, fy + 3.81), (0, 1)); wb = (fx - 0.1, fy, fx + 0.1, fy + 3.81); c = 0
                for q in (bx, lb, wb):
                    for a_, b_ in W:
                        if inter0(q, (min(a_[0], b_[0]) - 0.1, min(a_[1], b_[1]) - 0.1, max(a_[0], b_[0]) + 0.1, max(a_[1], b_[1]) + 0.1)): c += 3
                    for ow, bb_ in BOD:
                        if inter0(q, bb_): c += 5
                    for fb in FIX:
                        if inter0(q, fb): c += 4
                return c
            cand = []
            for dist in (5.08, 7.62, 10.16, 12.7):
                for off in (0, 5.08, -5.08, 7.62, -7.62):
                    cand.append((pt[0] + d[0] * dist + (off if d[0] == 0 else 0), pt[1] + d[1] * dist + (off if d[0] != 0 else 0) + (3.81 if d[1] == 0 and off == 0 else 0)))
            fx, fy = min(cand, key=lambda c_: flag_cost(*c_))
            if (fx, fy) != (pt[0] + d[0] * 5.08, pt[1] + d[1] * 5.08 + (3.81 if d[1] == 0 else 0)): wire(pt, (pt[0] + d[0] * 2.54, pt[1] + d[1] * 2.54)) if False else None
            fp0 = list(pins(resolve("power", "PWR_FLAG")).values())[0]
            pw = (fx, fy)
            BOD.append((("#FLG", fl), (fx - 1.8, fy - 0.3, fx + 1.8, fy + 3.2)))
            body.append(symbol_inst("power:PWR_FLAG", f"#FLG0{fl}", "PWR_FLAG", "", fx, fy, 0, 1, ["1"], hide_ref=True, props_at=(fx + 1, fy - 3)))
            wire(pw, (fx, fy + 3.81)); label(net, (fx, fy + 3.81), (0, 1))
    for b in S.get("blocks", []):
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        body.append(f'(rectangle (start {f(x)} {f(y)}) (end {f(x + w)} {f(y + h)}) (stroke (width 0.2) (type dash)) (fill (type none)) (uuid {uid()}))')
        FIX.append((x + 1.5, y + 1.5, x + 1.5 + len(b["title"]) * 2.2, y + 4.5))
        body.append(f'(text "{b["title"]}" (at {f(x + 1.5)} {f(y + 3.0)} 0) (effects (font (size 2 2) bold) (justify left)) (uuid {uid()}))')
    import textwrap
    PWH = {"A3": (420, 297), "A2": (594, 420), "A1": (841, 594), "A4": (297, 210)}[S.get("paper", "A3")]
    ny = max([b["y"] + b["h"] for b in S.get("blocks", [])] + [0]) + 8
    for (t, x0_, y0_) in S.get("notes", []):                              # notes: wrapped under the lowest block (the position given by the board spec is ignored so they cannot land on circuitry)
        for ln_ in textwrap.wrap(t, 110):
            FIX.append((20, ny - 1.0, 20 + len(ln_) * 1.5, ny + 1.0))
            body.append(f'(text "{ln_}" (at 20 {f(ny)} 0) (effects (font (size 1.5 1.5)) (justify left)) (uuid {uid()}))'); ny += 3.4
        ny += 2.0
    # ---- text placement: choose a free spot for every reference/value/power-label so nothing overlaps wires, symbols or other text
    def inter(a, b, m=0.12): return a[0] < b[2] - m and b[0] < a[2] - m and a[1] < b[3] - m and b[1] < a[3] - m
    wbox = [(min(a[0], b[0]) - 0.1, min(a[1], b[1]) - 0.1, max(a[0], b[0]) + 0.1, max(a[1], b[1]) + 0.1) for a, b in W]
    placed = []; tokens = {}
    def cost(box, own):
        c = 0
        for wb in wbox:
            if inter(box, wb): c += 3
        for ow, bb in BOD:
            if ow != own and inter(box, bb, 0.05): c += 5
        for fb in FIX:
            if inter(box, fb): c += 4
        for pb in placed:
            if inter(box, pb): c += 4
        return c
    def fld_box(txt, x, y, just):
        w = len(txt) * CW + 0.3
        return (x, y - 1.05, x + w, y + 1.05) if just == "left" else (x - w, y - 1.05, x, y + 1.05)
    def fmt(x, y, just, hide=False, rot=0):
        ang = 0 if rot == 180 else (-rot) % 360
        if rot == 180: just = "right" if just == "left" else "left"
        return f"(at {f(x)} {f(y)} {ang}) (effects (font (size 1.27 1.27)) (justify {just}){' hide' if hide else ''})"
    for fl in FLD:                                                                 # power symbols first (they sit on pin ends and are the least flexible)
        k = fl["fixed"]
        if not (isinstance(k, tuple) and k and k[0] == "PW"): continue
        end, d = k[1], k[2]; txt = fl["value"]; cands = []
        if d[0] == 0:
            yy = end[1] + d[1] * 2.2
            cands = [(end[0] + 1.6, yy, "left"), (end[0] - 1.6, yy, "right"), (end[0] + 1.6, yy + d[1] * 1.6, "left"), (end[0] - 1.6, yy + d[1] * 1.6, "right"), (end[0] + 1.6, yy + d[1] * 3.4, "left"), (end[0] - 1.6, yy + d[1] * 3.4, "right"), (end[0] + 1.6, yy - d[1] * 1.6, "left"), (end[0] - 1.6, yy - d[1] * 1.6, "right")]
        else:
            jj = "left" if d[0] > 0 else "right"
            cands = [(end[0] + d[0] * 3.9, end[1], jj), (end[0] + d[0] * 0.5, end[1] - 2.0, jj), (end[0] + d[0] * 0.5, end[1] + 2.4, jj), (end[0] + d[0] * 3.9, end[1] - 1.8, jj), (end[0] + d[0] * 3.9, end[1] + 2.0, jj)]
        best = min(cands, key=lambda c: cost(fld_box(txt, c[0], c[1], c[2]), ("#PWR", -1)))
        placed.append(fld_box(txt, *best)); tokens[f"@@V{fl['n']}@@"] = fmt(best[0], best[1], best[2], False, fl["rot"]); tokens[f"@@R{fl['n']}@@"] = fmt(best[0], best[1], "left", True, fl["rot"])
    for fl in FLD:
        if f"@@V{fl['n']}@@" in tokens: continue
        if fl["key"] == "power:PWR_FLAG":
            tokens[f"@@R{fl['n']}@@"] = fmt(fl["pos"][0], fl["pos"][1], "left", True); tokens[f"@@V{fl['n']}@@"] = fmt(fl["pos"][0], fl["pos"][1], "left", True); continue
        own = fl["owner"]; bb = [b for o, b in BOD if o == own]
        if not bb:
            px, py = fl["fixed"] or (fl["pos"][0] + 3, fl["pos"][1] - 4); tokens[f"@@R{fl['n']}@@"] = fmt(px, py, "left"); tokens[f"@@V{fl['n']}@@"] = fmt(px, py + 2.54, "left"); continue
        bb = bb[0]; txt1, txt2 = fl["ref"], fl["value"]; w = max(len(txt1), len(txt2)) * CW + 0.3; cy = (bb[1] + bb[3]) / 2; cx = (bb[0] + bb[2]) / 2; cands = []
        if fl["fixed"] and not (isinstance(fl["fixed"], tuple) and fl["fixed"][0] == "PW"): cands.append((fl["fixed"][0], fl["fixed"][1], "left"))
        for extra in (0.8, 3.5, 6.5):
            cands += [(bb[2] + extra, cy - 1.27, "left"), (bb[0] - extra, cy - 1.27, "right"), (bb[2] + extra, cy - 3.0, "left"), (bb[0] - extra, cy - 3.0, "right"), (bb[2] + extra, cy + 2.2, "left"), (bb[0] - extra, cy + 2.2, "right")]
        for up in (1.8, 4.0):
            cands += [(bb[0], bb[1] - up - 2.54, "left"), (bb[2], bb[1] - up - 2.54, "right"), (bb[0], bb[3] + up, "left"), (bb[2], bb[3] + up, "right")]
        def blk(c): 
            x0, y0, j = c; a = fld_box("x" * max(len(txt1), len(txt2)), x0, y0, j); b = fld_box("x" * max(len(txt1), len(txt2)), x0, y0 + 2.54, j); return (min(a[0], b[0]), a[1], max(a[2], b[2]), b[3])
        best = None; bc = 1e9
        for c in cands:
            cc = cost(blk(c), own)
            if cc < bc: best, bc = c, cc
            if cc == 0: break
        x0, y0, j = best; placed.append(blk(best)); tokens[f"@@R{fl['n']}@@"] = fmt(x0, y0, j, fl["hide_ref"], fl["rot"]); tokens[f"@@V{fl['n']}@@"] = fmt(x0, y0 + 2.54, j, False, fl["rot"])
        fl["cost"] = bc
    S["_text_cost"] = sum(1 for fl in FLD if fl.get("cost", 0) > 0)
    body = [re.sub(r"@@[RV]\d+@@", lambda m: tokens[m.group(0)], b) for b in body]
    tb = f'(title_block (title "{title}") (date "{date}") (rev "{rev}") (company "ClaudeWork") (comment 1 "First engineering release; see pcb/README.md for status and limits"))'
    text = f'(kicad_sch (version 20230121) (generator sch2) (uuid {root}) (paper "{S.get("paper", "A3")}") {tb} (lib_symbols ' + " ".join(dump(v) for v in libsyms.values()) + ") " + " ".join(body) + f' (sheet_instances (path "/" (page "1"))))'
    open(out_path, "w").write(text)
