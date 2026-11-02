"""Parametric prototype enclosure v2, generated from the finished PCB.
Base + lid STL with: M2.5 screw-fastened lid (four corner columns), standoffs at the PCB mounting holes, side openings for connectors,
captive button plungers and light pipes for lid holes (separate STL), a screw-closed battery bay under the floor sized for a named holder,
height overrides for plug-in modules, optional wall vents, or a flat mounting plate for a bought IP65 box. Collision check of simplified volumes.
All dimensions are first-pass: print one set and test-fit before a batch."""
import sys, os, json, math, importlib, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, trimesh
from trimesh.creation import box, cylinder
HEIGHTS = [("TQFP", 1.2), ("SOT-23", 1.2), ("R_0603", 0.6), ("C_0603", 0.9), ("C_0805", 1.5), ("R_0805", 0.6), ("LED_0603", 0.7), ("D_SOD-323", 1.1), ("D_SMA", 2.4), ("D_SMB", 2.6), ("Fuse_1206", 0.9), ("SW_SPST_B3U", 1.6),
           ("SW_SPDT_PCM12", 5.5), ("PinHeader_2x03", 8.5), ("PinHeader_1x0", 8.5), ("PinSocket_1x08", 8.5), ("JST_PH_B", 6.0), ("Buzzer_12x9.5", 9.5), ("USB_C", 3.3), ("TestPoint", 0.2), ("MountingHole", 0.0), ("Fiducial", 0.0),
           ("CP_Elec_6.3x7.7", 7.7), ("SOIC", 1.75), ("HSOP", 1.7), ("QFN", 1.0), ("LGA", 1.0), ("ESP32-S3", 3.1), ("BarrelJack", 11.0), ("TerminalBlock", 10.0), ("Crystal", 1.0), ("L_", 4.0)]
# bought-in battery holders (outside L x W x H, mm) and the part they refer to
HOLDERS = {"3xAAA": (52.7, 37.5, 13.0, "Keystone 2480 (3 x AAA, wire leads)"), "3xAA": (58.0, 48.3, 17.0, "Keystone 2465 (3 x AA, wire leads)"),
           "2xAAA": (53.0, 24.6, 13.0, "Keystone 2469 (2 x AAA, wire leads)"), "2xAA": (58.0, 33.0, 16.0, "Keystone 2463 (2 x AA, wire leads)")}
T, M, PCBT, LT = 2.0, 0.6, 1.6, 2.4            # wall, PCB-to-wall gap, PCB thickness, lid thickness
def height(name):
    for k, h in HEIGHTS:
        if k in name: return h
    return 2.0
def cyl(r, h, x, y, z0, n=32):
    c = cylinder(radius=r, height=h, sections=n); c.apply_translation([x, y, z0 + h / 2]); return c
def bx(sx, sy, sz, cx, cy, z0):
    b = box([sx, sy, sz]); b.apply_translation([cx, cy, z0 + sz / 2]); return b
def battery_of(B):
    for p in B["parts"]:
        m = re.search(r"(\d)\s*x\s*(AAA|AA)\b", str(p.get("value", "")), re.I)
        if m: return f"{m.group(1)}x{m.group(2).upper()}"
    return None
def build(modname):
    B = importlib.import_module("boards." + modname).BOARD; E = B.get("enc"); name = B["name"]
    if not E: return None
    out = os.path.join(HERE, "out", modname); W, H = B["size"]; STAND = E.get("standoff", 4.0)
    raw = json.load(open(os.path.join(out, "components.json"))); comps = {}
    mods = E.get("modules", {})
    for ref, c in raw.items():
        x0, y0, x1, y1 = c["box"]; comps[ref] = dict(box=(x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 0.3), h=mods.get(ref, height(c["fp"])), cx=c["cx"], cy=c["cy"], fp=c["fp"])
    hmax = max(c["h"] for r, c in comps.items() if not r.startswith(("H", "FID")))
    Hin = E.get("inner_height", math.ceil(hmax + 2.0))
    if E.get("plate"): return plate(B, E, comps, out, name, W, H, STAND)
    bat = E.get("battery", battery_of(B)) if E.get("battery", True) is not False else None
    hold = HOLDERS.get(bat) if bat else None
    # cavity footprint: the board plus margin, enlarged if the battery bay needs more room
    cx0, cy0, cx1, cy1 = -M, -M, W + M, H + M
    if hold:
        bl, bw = hold[0] + 2.0, hold[1] + 2.0
        if bl > (cx1 - cx0) - 2 or bw > (cy1 - cy0) - 2:            # rotate if it fits better
            if bw <= (cx1 - cx0) - 2 and bl <= (cy1 - cy0) - 2: bl, bw = bw, bl
        grow_x = max(0.0, (bl + 10.0) - (cx1 - cx0)) / 2; grow_y = max(0.0, (bw + 10.0) - (cy1 - cy0)) / 2
        cx0 -= grow_x; cx1 += grow_x; cy0 -= grow_y; cy1 += grow_y
    el, et, er, eb = E.get("extend", (0, 0, 0, 0)); cx0 -= el; cy0 -= et; cx1 += er; cy1 += eb        # extra room, e.g. for panel-mounted arcade buttons
    ccx, ccy = (cx0 + cx1) / 2, (cy0 + cy1) / 2; Lx, Ly = cx1 - cx0, cy1 - cy0
    Db = (hold[2] + 0.8) if hold else 0.0
    F = (Db + 2.0) if hold else 2.0                                         # floor block thickness (bay + 2 mm ceiling)
    zpcb = F + STAND; zlid = zpcb + PCBT + Hin                              # z of the PCB underside and of the lid underside
    # outer shell with four corner columns (lid screw bosses, also round the corners)
    ox0, oy0, ox1, oy1 = cx0 - T, cy0 - T, cx1 + T, cy1 + T
    shell = bx(ox1 - ox0, oy1 - oy0, zlid, ccx, ccy, 0.0)
    corners = [(ox0 - 1.0, oy0 - 1.0), (ox1 + 1.0, oy0 - 1.0), (ox0 - 1.0, oy1 + 1.0), (ox1 + 1.0, oy1 + 1.0)]   # outside the cavity: they never touch the PCB
    for (x, y) in corners: shell = shell.union(cyl(4.0, zlid, x, y, 0.0))
    shell = shell.difference(bx(Lx, Ly, zlid, ccx, ccy, F))                 # cavity above the floor
    for (x, y) in corners: shell = shell.difference(cyl(1.05, 12.0, x, y, zlid - 11.9, 24))          # M2.5 self-tapping pilots for the lid screws
    for (hx, hy) in B.get("holes", []):                                       # PCB standoffs with pilots
        shell = shell.union(cyl(2.75, STAND, hx, hy, F)); shell = shell.difference(cyl(1.05, STAND + 1.5, hx, hy, F + 0.5, 24))
    info = dict()
    if hold:                                                                  # battery bay opening on the bottom, screw-closed door
        shell = shell.difference(bx(bl, bw, Db, ccx, ccy, -0.01))
        dl, dw = bl + 8.0, bw + 8.0
        shell = shell.difference(bx(dl, dw, 1.6, ccx, ccy, -0.01))           # door recess
        along_x = bl >= bw; sx = (bl / 2 + 2.0) if along_x else 0.0; sy = 0.0 if along_x else (bw / 2 + 2.0)
        screws = [(ccx - sx, ccy - sy), (ccx + sx, ccy + sy)]
        for (x, y) in screws: shell = shell.difference(cyl(1.05, F - 2.0, x, y, 1.0, 24))
        wx, wy = (ccx + (bl / 2 - 6.0), ccy) if along_x else (ccx, ccy + (bw / 2 - 6.0))
        shell = shell.difference(cyl(2.5, 3.0, wx, wy, Db - 0.5))           # wire pass-through from the bay into the electronics cavity
        door = bx(dl - 0.4, dw - 0.4, 1.5, ccx, ccy, 0.0)
        for (x, y) in screws: door = door.difference(cyl(1.45, 3.0, x, y, -1.0, 24)).difference(cyl(2.7, 0.8, x, y, -0.01, 24))
        door = door.union(bx(bl - 1.0, bw - 1.0, 0.8, ccx, ccy, 1.5).difference(bx(bl - 3.4, bw - 3.4, 0.9, ccx, ccy, 1.45)))   # locating rim inside the opening
        door.export(os.path.join(out, name + "_enclosure_battery_door.stl"))
        info.update(battery=bat, holder=hold[3], bay=[round(bl, 1), round(bw, 1), round(Db, 1)], door_screws="2 x M2.5 x 6 mm self-tapping (tool needed to open)")
    zb = zpcb + PCBT; sliders = []                                            # side openings (z relative to the PCB top)
    for c in E.get("side", []):
        ref, side, w, h, zc = c; pc = comps[ref]
        if side in ("top", "bottom"):
            y = cy0 - T / 2 if side == "top" else cy1 + T / 2; cut = bx(w, T + 3.0, h, pc["cx"], y, zb + zc - h / 2)
        else:
            x = cx0 - T / 2 if side == "left" else cx1 + T / 2; cut = bx(T + 3.0, w, h, x, pc["cy"], zb + zc - h / 2)
        shell = shell.difference(cut)
        x0, y0, x1, y1 = pc["box"]
        gap = {"top": y0 - cy0, "bottom": cy1 - y1, "left": x0 - cx0, "right": cx1 - x1}[side]
        if ref.startswith("SW") and gap > 0.5: sliders.append((ref, side, w, h, gap))
    if E.get("vent"):                                                         # vent slots high on both long walls
        n = int((Lx - 20) // 6)
        for i in range(n):
            x = cx0 + 10 + i * 6 + 1
            for y in (cy0 - T / 2, cy1 + T / 2): shell = shell.difference(bx(2.0, T + 2.0, 10.0, x, y, zlid - 13.0))
    # lid: plate + locating lip, screw holes with counterbores, cut-outs; plungers and light pipes are separate parts
    lid = bx(ox1 - ox0, oy1 - oy0, LT, ccx, ccy, 0.0)
    for (x, y) in corners: lid = lid.union(cyl(4.0, LT, x, y, 0.0))
    lid = lid.union(bx(Lx - 0.4, Ly - 0.4, 1.6, ccx, ccy, -1.6).difference(bx(Lx - 3.6, Ly - 3.6, 1.8, ccx, ccy, -1.7)))
    for (hx, hy) in B.get("holes", []):                                       # keep the lip clear of the standoff screws
        pass
    for (x, y) in corners: lid = lid.difference(cyl(1.45, LT + 4, x, y, -2.0, 24)).difference(cyl(2.7, 1.2, x, y, LT - 1.2, 24))
    parts = []
    for c in E.get("lid", []):
        kind = c[0]
        if kind == "abs_round":                                               # panel hole at board coordinates (e.g. 30 mm arcade button)
            lid = lid.difference(cyl(c[3] / 2, LT + 4, c[1], c[2], -2.0)); continue
        if kind == "abs_rect":                                                # window (cover with a translucent sheet from inside)
            lid = lid.difference(bx(c[3], c[4], LT + 4, c[1], c[2], -2.0)); continue
        ref = c[1]; pc = comps[ref]; px = pc["cx"] + (c[3] if len(c) > 3 else 0); py = pc["cy"] + (c[4] if len(c) > 4 else 0)
        if kind == "round":
            is_btn = ref.startswith("SW"); d = c[2] if is_btn else max(c[2], 3.0)
            lid = lid.difference(cyl(d / 2, LT + 4, px, py, -2.0))
            gap_top = zlid - (zb + pc["h"])                                   # from the part top to the lid underside
            if is_btn: parts.append(("plunger", ref, d - 0.5, d + 3.0, gap_top - 1.2 - 0.3, LT + 1.5))
            else: parts.append(("light pipe", ref, d - 0.3, d + 2.5, gap_top - 1.2 - 0.5, LT + 0.3))
        elif kind == "grille":
            n, sw, sl = c[2], c[3], c[4]
            for i in range(n): lid = lid.difference(bx(sw, sl, LT + 4, px + (i - (n - 1) / 2) * (sw + 1.2), py, -2.0))
        elif kind == "rect":
            lid = lid.difference(bx(c[2], c[3], LT + 4, px, py, -2.0))
    for (ref, sw_, sl_) in E.get("stalk", []):                                # top-access switch stalk: lid slot above the part, vertical bar with a fork at the knob
        pc = comps[ref]; lid = lid.difference(bx(sw_, sl_, LT + 4, pc["cx"], pc["cy"], -2.0))
        parts.append(("stalk", ref, min(sw_, sl_) - 0.8, 0.0, zlid - (zb + pc["h"] / 2) + LT + 3.0, max(sw_, sl_) - 3.5))
    for (ref, side, w, h, gap) in sliders:                                    # slide-switch extension: a bar running in the wall slot with a fork that grips the knob
        parts.append(("slider", ref, min(w, h) - 0.8, 0.0, gap + T + 2.0, max(w, h) - 0.8))
    if parts:                                                                 # captive parts: flange under the lid, shaft down to the part, cap through the lid
        acc = None; x = 0.0
        for (kind, ref, ds, df, below, above) in parts:
            if kind in ("slider", "stalk"):                                              # ds = bar thickness, below = bar length, above = bar width; fork 2.4 mm gap at one end
                p = bx(below, above, ds, x + below / 2, 0.0, 0.0).union(bx(2.5, 1.0, ds, x - 1.25, (2.4 + 1.0) / 2, 0.0)).union(bx(2.5, 1.0, ds, x - 1.25, -(2.4 + 1.0) / 2, 0.0))
                p = p.difference(bx(2.6, 2.4, ds + 1, x - 1.2, 0.0, -0.5)); acc = p if acc is None else acc.union(p); x += below + 8.0; continue
            p = cyl(df / 2, 1.2, x, 0.0, 0.0).union(cyl(ds / 2, above, x, 0.0, 1.2)).union(cyl(ds / 2, max(below, 0.4), x, 0.0, -max(below, 0.4)))
            acc = p if acc is None else acc.union(p); x += df + 4.0
        acc.export(os.path.join(out, name + "_enclosure_caps.stl"))
        info["caps"] = [dict(kind=k, ref=r, shaft=round(ds, 2), flange=round(df, 2), below_flange=round(b, 1), above_flange=round(a, 1)) for (k, r, ds, df, b, a) in parts]
    # collision check
    issues = []
    for r, c in comps.items():
        if r.startswith(("H", "FID")): continue
        x0, y0, x1, y1 = c["box"]
        if c["h"] > Hin + 0.01: issues.append(f"{r} height {c['h']} mm exceeds inner height {Hin}")
        if x0 < cx0 + 0.05 or y0 < cy0 + 0.05 or x1 > cx1 - 0.05 or y1 > cy1 - 0.05:
            if r not in [s[0] for s in E.get("side", [])]: issues.append(f"{r} extends into the wall without a declared opening")
        for (x, y) in corners:
            if x0 - 4.0 < x < x1 + 4.0 and y0 - 4.0 < y < y1 + 4.0 and c["h"] > 0: issues.append(f"{r} near lid-screw column at ({x:.0f},{y:.0f})")
    lid.apply_translation([0, 0, zlid])
    shell.export(os.path.join(out, name + "_enclosure_base.stl")); lid.export(os.path.join(out, name + "_enclosure_lid.stl"))
    info.update(version=2, inner_height=Hin, outer=[round(ox1 - ox0 + 10.0, 1), round(oy1 - oy0 + 10.0, 1), round(zlid + LT, 1)], tallest=hmax, lid_fastening="4 x M2.5 x 10 mm self-tapping, corner columns",
                base_watertight=bool(shell.is_watertight), lid_watertight=bool(lid.is_watertight), issues=issues, note=E.get("note", "indoor, dry use; print in PETG or ABS, 3 perimeters, 25 % infill"))
    json.dump(info, open(os.path.join(out, "enclosure.json"), "w"), indent=1); return info
def plate(B, E, comps, out, name, W, H, STAND):
    """Flat mounting plate for a bought IP-rated box: board standoffs plus four slotted mounting holes."""
    m = 8.0; p = bx(W + 2 * m, H + 2 * m, 3.0, W / 2, H / 2, 0.0)
    for (hx, hy) in B.get("holes", []): p = p.union(cyl(2.75, STAND, hx, hy, 3.0)).difference(cyl(1.05, STAND + 3.0, hx, hy, 0.5, 24))
    for (x, y) in [(-m / 2, -m / 2), (W + m / 2, -m / 2), (-m / 2, H + m / 2), (W + m / 2, H + m / 2)]: p = p.difference(cyl(2.2, 5.0, x, y, -1.0, 24))
    p.export(os.path.join(out, name + "_enclosure_plate.stl"))
    hmax = max(c["h"] for r, c in comps.items() if not r.startswith(("H", "FID")))
    info = dict(version=2, mode="mounting plate for a bought IP65 box", plate=[W + 2 * m, H + 2 * m, 3.0], min_box_inside=[round(W + 2 * m + 4, 0), round(H + 2 * m + 4, 0), round(3.0 + STAND + 1.6 + hmax + 10, 0)],
                tallest=hmax, plate_watertight=bool(p.is_watertight), issues=[], note=E.get("note", ""))
    json.dump(info, open(os.path.join(out, "enclosure.json"), "w"), indent=1); return info
if __name__ == "__main__": print(build(sys.argv[1]))
