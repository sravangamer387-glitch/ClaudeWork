"""ASTRADAND mechanical parts (FDM): two-half hilt shell, diffuser crystal, trigger cap, tip cap, pommel. Units mm, wand axis = X, split plane z = 0.
Board: 146 x 26 mm, 1.6 mm, centred on y = 0, top face (components) at z = +BZ, board x = 0 sits at hilt x = BX0.
All dimensions are first-pass and UNPROTOTYPED: print one shell, test-fit the real PCB and 3xAAA holder, then adjust PCB_CLEAR / WALL."""
import os, json, math
import numpy as np, trimesh
from trimesh import creation, transformations as T
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
L = 232.0; R_OUT = 17.0; WALL = 2.4; R_IN = R_OUT - WALL            # outer diameter 34 mm
BX0 = 24.0; BZ = 2.0; BOARD_L, BOARD_W, BOARD_T = 146.0, 26.0, 1.6
HEAD_X0, HEAD_X1 = BX0 + 8, BX0 + 60                                   # LEDs sit at board x 10..55
BOSS_Y = BOARD_W / 2 + 2.9                                              # screw bosses sit outside the board edge (inside the wall thickness): no collision with the PCB
LED_Y = -(BOARD_W / 2 - 5.0)                                            # board y=5 from the LED edge -> offset slit
def cyl_x(r, x0, x1, sections=96):
    m = creation.cylinder(radius=r, height=x1 - x0, sections=sections); m.apply_transform(T.rotation_matrix(math.pi / 2, [0, 1, 0])); m.apply_translation([(x0 + x1) / 2, 0, 0]); return m
def box(x0, x1, y0, y1, z0, z1):
    m = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0]); m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return m
def cyl_z(r, x, y, z0, z1, sections=48):
    m = creation.cylinder(radius=r, height=z1 - z0, sections=sections); m.apply_translation([x, y, (z0 + z1) / 2]); return m
def union(ms): 
    out = ms[0]
    for m in ms[1:]: out = trimesh.boolean.union([out, m], engine="manifold")
    return out
def diff(a, bs):
    for b in bs: a = trimesh.boolean.difference([a, b], engine="manifold")
    return a
def build():
    body = cyl_x(R_OUT, 0, L); cavity = cyl_x(R_IN, WALL, L - WALL)
    rings = [cyl_x(R_OUT + 0.8, x, x + 3.0) for x in (96, 106, 116, 140, 150)]                          # decorative rune bands on the grip
    grooves = []
    for k in range(10): ang = k * 2 * math.pi / 10; g = box(160, 185, -0.8, 0.8, R_OUT - 0.7, R_OUT + 1.5); g.apply_transform(T.rotation_matrix(ang, [1, 0, 0])); grooves.append(g)   # grip flutes
    shell = diff(union([body] + rings), [cavity] + grooves)
    # internal features (added back after the cavity cut): board support rails, battery saddle, screw bosses on the split plane
    inner = []
    for x in (BX0 + 6, BX0 + 40, BX0 + 74, BX0 + 108, BX0 + 140):                                    # board rails: ledge under the board edge on both sides
        inner += [box(x - 3, x + 3, -BOARD_W / 2 - 1.0, -BOARD_W / 2 + 1.5, BZ - 2.6, BZ - 0.0), box(x - 3, x + 3, BOARD_W / 2 - 1.5, BOARD_W / 2 + 1.0, BZ - 2.6, BZ - 0.0)]
    for x in (BX0 + 10, BX0 + 60, BX0 + 110, BX0 + 136): inner.append(box(x - 4, x + 4, -R_IN + 0.5, R_IN - 0.5, -R_IN + 3.0, -9.0)) if False else None
    saddle = diff(cyl_x(8.2, BX0 + 12, BX0 + 12 + 140), [cyl_x(6.3, BX0 + 12 - 1, BX0 + 12 + 141)])      # 3 x AAA in line (about 134 mm) rests in a tube under the board
    saddle.apply_translation([0, 0, -8.0]); inner.append(saddle)
    # trim: boolean with the inner cylinder so nothing pokes through the outer wall
    keep = cyl_x(R_OUT - 0.4, 0, L); inner_u = [trimesh.boolean.intersection([m, keep], engine="manifold") for m in inner if m is not None]
    bosses = []
    for x in (22, 62, 102, 142, 182, 214):
        for sy in (-1, 1): bosses.append(cyl_z(2.7, x, sy * BOSS_Y, -6.0, 6.0))
    bosses = [trimesh.boolean.intersection([b, keep], engine="manifold") for b in bosses]
    shell = union([shell] + inner_u + bosses)
    holes = []
    for x in (22, 62, 102, 142, 182, 214):
        for sy in (-1, 1): holes.append(cyl_z(1.15, x, sy * BOSS_Y, -8.0, 8.0))                  # 2.3 mm pilot for M2.5 self-tapping screws (upper) / clearance below
    shell = diff(shell, holes)
    window = box(HEAD_X0, HEAD_X1, LED_Y - 3.7, LED_Y + 3.7, 4.0, R_OUT + 2.0)                         # light slit over the six LEDs (diffuser crystal sits in it)
    trig = cyl_z(3.1, BX0 + 58, 6.0 - 4.0, 2.0, R_OUT + 2.0)                                              # trigger button hole over SW2 (board x 58, y 20.5 -> y = +7.5)
    trig = cyl_z(3.1, BX0 + 58, 20.5 - BOARD_W / 2, 2.0, R_OUT + 2.0)
    grille = [cyl_z(0.8, BX0 + 24 + dx, 18 - BOARD_W / 2 + dy, 2.0, R_OUT + 2.0, 16) for dx in (-3, 0, 3) for dy in (-3, 0, 3)]   # buzzer sound holes
    usb_none = []
    upper_cut = diff(box(-1, L + 1, -R_OUT - 3, R_OUT + 3, 0.0, R_OUT + 3), [window, trig] + grille)
    upper = trimesh.boolean.intersection([shell, box(-1, L + 1, -R_OUT - 3, R_OUT + 3, 0.0, R_OUT + 3)], engine="manifold"); upper = diff(upper, [window, trig] + grille)
    lower = trimesh.boolean.intersection([shell, box(-1, L + 1, -R_OUT - 3, R_OUT + 3, -R_OUT - 3, 0.0)], engine="manifold")
    # lower screw heads: counterbore 5 mm on the underside
    cb = [cyl_z(2.6, x, sy * BOSS_Y, -9.0, -5.2) for x in (22, 62, 102, 142, 182, 214) for sy in (-1, 1)]
    lower = diff(lower, cb)
    # crystal diffuser (translucent natural PETG / clear resin): slides into the slit from below the upper shell rim
    crystal = box(HEAD_X0 + 0.3, HEAD_X1 - 0.3, LED_Y - 3.4, LED_Y + 3.4, 5.4, R_OUT + 0.8)
    crystal = trimesh.boolean.intersection([crystal, creation.cylinder(radius=1, height=1)], engine="manifold") if False else crystal
    chamfer = trimesh.boolean.difference([crystal, box(HEAD_X0 - 1, HEAD_X1 + 1, LED_Y - 5, LED_Y - 2.4, R_OUT, R_OUT + 3)], engine="manifold")
    trigger_cap = union([cyl_z(2.9, 0, 0, 0.0, 6.5), cyl_z(4.2, 0, 0, -1.2, 0.0)])                       # push button cap with a retaining flange
    tip = trimesh.creation.cone(radius=R_OUT, height=22.0, sections=96); tip.apply_transform(T.rotation_matrix(-math.pi / 2, [0, 1, 0])); tip.apply_translation([-0.0, 0, 0])
    pom = trimesh.creation.icosphere(subdivisions=3, radius=R_OUT - 0.5); pom.apply_scale([0.6, 1, 1])
    return dict(hilt_upper=upper, hilt_lower=lower, crystal=chamfer, trigger_cap=trigger_cap, tip_cap=tip, pommel=pom)
if __name__ == "__main__":
    info = {}
    for k, m in build().items():
        m.export(os.path.join(OUT, k + ".stl")); b = m.bounds
        info[k] = dict(watertight=bool(m.is_watertight), volume_cm3=round(float(abs(m.volume)) / 1000, 2), size_mm=[round(float(v), 1) for v in (b[1] - b[0])]); print(k, info[k])
    info["wand_overall_mm"] = L; info["board_in_hilt_x0_mm"] = BX0
    json.dump(info, open(os.path.join(OUT, "hilt_info.json"), "w"), indent=1)
