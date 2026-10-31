"""Parametric prototype enclosure (base + lid STL) generated from the finished PCB: standoffs at the mounting holes, lid cut-outs at real
part positions, side openings for connectors, plus a collision check of simplified component volumes against the walls and lid."""
import sys, os, json, importlib, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, trimesh
from trimesh.creation import box, cylinder
HEIGHTS = [("TQFP", 1.2), ("SOT-23", 1.2), ("R_0603", 0.6), ("C_0603", 0.9), ("C_0805", 1.5), ("LED_0603", 0.7), ("D_SOD-323", 1.1), ("D_SMA", 2.4), ("Fuse_1206", 0.9), ("SW_SPST_B3U", 2.6), ("SW_SPDT_PCM12", 5.5),
           ("PinHeader_2x03", 8.5), ("PinHeader_1x0", 8.5), ("JST_PH_B", 6.0), ("Buzzer_12x9.5", 9.5), ("USB_C", 3.3), ("TestPoint", 0.2), ("MountingHole", 0.0), ("Fiducial", 0.0)]
def height(name):
    for k, h in HEIGHTS:
        if k in name: return h
    return 2.0
def build(modname):
    B = importlib.import_module("boards." + modname).BOARD; E = B.get("enc"); name = B["name"]
    if not E: return None
    out = os.path.join(HERE, "out", modname); W, H = B["size"]
    T, M, STAND, PCBT = 2.0, 0.6, E.get("standoff", 4.0), 1.6
    raw = json.load(open(os.path.join(out, "components.json"))); comps = {}
    for ref, c in raw.items():
        x0, y0, x1, y1 = c["box"]; comps[ref] = dict(box=(x0 - 0.3, y0 - 0.3, x1 + 0.3, y1 + 0.3), h=height(c["fp"]), cx=c["cx"], cy=c["cy"], fp=c["fp"])
    ztop_pcb = STAND + PCBT; hmax = max(c["h"] for r, c in comps.items() if not r.startswith(("H", "FID")))
    Hin = E.get("inner_height", math.ceil(hmax + 2.0))                                   # clearance above the tallest part
    Wx, Wy = W + 2 * M, H + 2 * M; ox, oy = -M - T, -M - T
    # enclosure frame: board origin at (0,0); z = 0 at outside floor
    base = box([Wx + 2 * T, Wy + 2 * T, STAND + PCBT + Hin - 1.0]); base.apply_translation([W / 2, H / 2, (STAND + PCBT + Hin - 1.0) / 2 - 1.0])
    cav = box([Wx, Wy, STAND + PCBT + Hin]); cav.apply_translation([W / 2, H / 2, (STAND + PCBT + Hin) / 2 + 1.0 - 1.0 + 0.0])
    cav.apply_translation([0, 0, 0])
    floor_top = 0.0
    shell = base.difference(cav)
    # keep a 2 mm floor
    floor = box([Wx + 2 * T, Wy + 2 * T, 2.0]); floor.apply_translation([W / 2, H / 2, -1.0]); shell = shell.union(floor)
    # standoffs at the mounting holes (M2.5 self-tapping pilot 2.1 mm)
    for (hx, hy) in B.get("holes", []):
        post = cylinder(radius=2.75, height=STAND, sections=32); post.apply_translation([hx, hy, STAND / 2]); shell = shell.union(post)
    for (hx, hy) in B.get("holes", []):
        pilot = cylinder(radius=1.05, height=STAND + 2.0, sections=24); pilot.apply_translation([hx, hy, STAND / 2 + 0.5]); shell = shell.difference(pilot)
    # side openings
    zb = ztop_pcb
    for c in E.get("side", []):
        ref, side, w, h, zc = c; pc = comps[ref]; cut = None
        if side in ("top", "bottom"):
            cut = box([w, T + M + 3.0, h]); y = -M - T / 2 - 0.5 if side == "top" else H + M + T / 2 + 0.5; cut.apply_translation([pc["cx"], y, zb + zc])
        else:
            cut = box([T + M + 3.0, w, h]); x = -M - T / 2 - 0.5 if side == "left" else W + M + T / 2 + 0.5; cut.apply_translation([x, pc["cy"], zb + zc])
        shell = shell.difference(cut)
    # lid
    lt = 2.0; lid = box([Wx + 2 * T, Wy + 2 * T, lt]); lid.apply_translation([W / 2, H / 2, lt / 2])
    lip = box([Wx - 0.4, Wy - 0.4, 1.6]); lip.apply_translation([W / 2, H / 2, -0.8]); lid = lid.union(lip)                  # lip enters the base walls
    lid_top_z = lt
    for c in E.get("lid", []):
        kind, ref = c[0], c[1]; pc = comps[ref]
        if kind == "round":
            d = c[2]; cut = cylinder(radius=d / 2, height=lt + 4, sections=32); cut.apply_translation([pc["cx"] + (c[3] if len(c) > 3 else 0), pc["cy"] + (c[4] if len(c) > 4 else 0), 0]); lid = lid.difference(cut)
        elif kind == "grille":
            n, sw, sl = c[2], c[3], c[4]
            for i in range(n):
                s = box([sw, sl, lt + 4]); s.apply_translation([pc["cx"] + (i - (n - 1) / 2) * (sw + 1.2), pc["cy"], 0]); lid = lid.difference(s)
        elif kind == "rect":
            cut = box([c[2], c[3], lt + 4]); cut.apply_translation([pc["cx"], pc["cy"], 0]); lid = lid.difference(cut)
    # collision check: component volumes vs lid underside and walls
    issues = []; z_lid_under = STAND + PCBT + Hin
    for r, c in comps.items():
        if r.startswith(("H", "FID")): continue
        x0, y0, x1, y1 = c["box"]
        if c["h"] > Hin + 0.01: issues.append(f"{r} height {c['h']} mm exceeds inner height {Hin}")
        if x0 < -M + 0.05 or y0 < -M + 0.05 or x1 > W + M - 0.05 or y1 > H + M - 0.05:
            sides = [s[0] for s in E.get("side", []) if s[0] == r]
            if r not in sides: issues.append(f"{r} extends into the wall ({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f}) without a declared opening")
    lid.apply_translation([0, 0, z_lid_under + 1.0 - 0.0])
    shell.export(os.path.join(out, name + "_enclosure_base.stl")); lid.export(os.path.join(out, name + "_enclosure_lid.stl"))
    info = dict(inner_height=Hin, outer=[round(Wx + 2 * T, 1), round(Wy + 2 * T, 1), round(STAND + PCBT + Hin + 1.0 + lt, 1)], tallest=hmax, base_watertight=bool(shell.is_watertight), lid_watertight=bool(lid.is_watertight), issues=issues)
    json.dump(info, open(os.path.join(out, "enclosure.json"), "w"), indent=1); return info
if __name__ == "__main__": print(build(sys.argv[1]))
