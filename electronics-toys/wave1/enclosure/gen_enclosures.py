#!/usr/bin/env python3
"""Parametric enclosure generator (trimesh + manifold3d booleans) for the three Wave-1 toys.
Usage: python gen_enclosures.py <out_dir>.  Units: mm.  Output: binary STL per part + checks.md.

These are first-article CAD solids for 3D-printed prototypes and for the tooling vendor to start from.
NOT done here (needs the tool-maker): draft angles, fillets, ribs, snap fits, gating, venting."""
import sys
from pathlib import Path

import numpy as np
import trimesh

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
OUT.mkdir(parents=True, exist_ok=True)

WALL = 2.4          # ABS wall (injection-mouldable range 2.0-3.0 mm)
BOSS_OD, BOSS_ID = 7.0, 2.6          # M3 self-tapping screw boss
ABS_DENSITY = 1.05  # g/cm3
checks = []


def box(x, y, z, cx=0, cy=0, cz=0):
    m = trimesh.creation.box(extents=(x, y, z))
    m.apply_translation((cx, cy, cz + z / 2))
    return m


def cyl(r, h, cx, cy, cz, sections=48):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=sections)
    m.apply_translation((cx, cy, cz + h / 2))
    return m


def diff(a, *bs):
    for b in bs:
        a = trimesh.boolean.difference([a, b], engine="manifold")
    return a


def union(*ms):
    return trimesh.boolean.union(list(ms), engine="manifold")


def tcyl(r, x, y, h_top, sections=48):
    """Cylinder that drills through the closed top face of a shell of height h_top."""
    return cyl(r, WALL + 2.0, x, y, h_top - WALL - 1.0, sections)


def tbox(sx, sy, cx, cy, h_top):
    return box(sx, sy, WALL + 2.0, cx=cx, cy=cy, cz=h_top - WALL - 1.0)


def cut(part, *tools, label="cut"):
    """Boolean difference that FAILS if nothing was removed (guards against mis-placed tools)."""
    before = part.volume
    out = diff(part, *tools)
    removed = before - out.volume
    assert removed > 1.0, f"{label}: tools removed no material (placed on the wrong face?)"
    return out


def save(name, mesh, note=""):
    mesh.export(OUT / f"{name}.stl")
    bb = mesh.bounds[1] - mesh.bounds[0]
    mass = mesh.volume / 1000 * ABS_DENSITY
    checks.append((name, bb, mass, mesh.is_watertight, note))


def shell_pair(name, L, W, H_top, H_bot, boss_inset=8.0):
    """Two-part clamshell with 4 screw bosses in the bottom half; returns (top, bottom) un-cut shells."""
    outer_t = box(L, W, H_top)
    inner_t = box(L - 2 * WALL, W - 2 * WALL, H_top - WALL, cz=0)
    top = diff(outer_t, inner_t)
    outer_b = box(L, W, H_bot)
    inner_b = box(L - 2 * WALL, W - 2 * WALL, H_bot - WALL, cz=WALL)
    bottom = diff(outer_b, inner_b)
    posts, holes = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (L / 2 - boss_inset), sy * (W / 2 - boss_inset)
            posts.append(cyl(BOSS_OD / 2, H_bot - WALL, x, y, WALL))
            holes.append(cyl(BOSS_ID / 2, H_bot - WALL - 1, x, y, WALL + 1))
    bottom = diff(union(bottom, *posts), *holes)
    return top, bottom


# ------------------------------------------------------------ P1 rhymes player 160 x 110
L, W = 160.0, 110.0
top, bottom = shell_pair("p1", L, W, 24.0, 26.0)
HT1 = 24.0
cuts = []
for i in range(4):                                  # 7 control buttons: row of 4 + row of 3, 11 mm holes
    cuts.append(tcyl(5.5, -48 + i * 32, -28, HT1))
for i in range(3):
    cuts.append(tcyl(5.5, -32 + i * 32, -44, HT1))
for x in (-60, 60):                                 # 2 LED windows
    cuts.append(tcyl(1.6, x, 36, HT1))
for gx in np.arange(-16, 16.1, 4.0):                # speaker grille: O2.2 holes on a 4 mm grid inside O31
    for gy in np.arange(-16, 16.1, 4.0):
        if gx * gx + gy * gy <= 15.5 ** 2:
            cuts.append(tcyl(1.1, 38 + gx, 22 + gy, HT1, sections=16))
p1_top = cut(top, *cuts, label="p1 top")
save("p1_rhymes_top", p1_top, "7 button holes, 2 LED holes, speaker grille")
# battery door window on the bottom: 3xAA tray 60 x 18
p1_bot = cut(bottom, box(62, 20, WALL * 3, cx=-30, cy=-20, cz=-1), label="p1 battery door")
save("p1_rhymes_bottom", p1_bot, "battery door opening 62 x 20")
door = box(64, 22, 1.8, cx=0, cy=0, cz=0)
door = union(door, cyl(3.5, 3.0, 0, 0, 1.8))     # simple finger pip
save("p1_battery_door", door, "door plate 64 x 22 (screw fixing to be added by tool-maker)")

# ------------------------------------------------------------ P4 cricket game 150 x 80
L4, W4 = 150.0, 80.0
t4, b4 = shell_pair("p4", L4, W4, 14.0, 18.0, boss_inset=7.0)
HT4 = 14.0
c4 = [tbox(64, 16, -24, 14, HT4)]                  # 4-digit display window
for i in range(6):                                  # 6 lane LED holes + 1 result LED
    c4.append(tcyl(2.2, -55 + i * 12, -10, HT4))
c4.append(tcyl(2.2, 38, -10, HT4))
c4.append(tcyl(8.0, 44, 14, HT4))                   # buzzer / sound opening
c4.append(tcyl(9.0, -40, -28, HT4))                 # BAT button
c4.append(tcyl(6.0, 20, -28, HT4))                  # START button
save("p4_cricket_top", cut(t4, *c4, label="p4 top"), "display window, 7 LED holes, 2 button holes, sound hole")
save("p4_cricket_bottom", cut(b4, box(52, 18, WALL * 3, cx=0, cy=-12, cz=-1), label="p4 door"), "3xAAA door opening")

# ------------------------------------------------------------ P3 star lamp: dome 90 mm on 90 mm base
R = 45.0
sphere = trimesh.creation.icosphere(subdivisions=4, radius=R)
dome = diff(sphere, box(2 * R + 10, 2 * R + 10, R + 10, cz=-(R + 10)))          # keep upper hemisphere
dome_hollow = trimesh.creation.icosphere(subdivisions=4, radius=R - 2.0)
dome_hollow = diff(dome_hollow, box(2 * R + 10, 2 * R + 10, R + 10, cz=-(R + 10)))
dome = diff(dome, dome_hollow)
rng = np.random.default_rng(7)
stars = []
for _ in range(60):                                         # 60 star holes Ø1.6 distributed over the dome
    th = rng.uniform(0, 2 * np.pi); ph = np.arccos(rng.uniform(0.15, 1.0))
    p = R * np.array([np.sin(ph) * np.cos(th), np.sin(ph) * np.sin(th), np.cos(ph)])
    c = trimesh.creation.cylinder(radius=0.8, height=10, sections=12)
    z_axis = np.array([0, 0, 1.0]); d = p / np.linalg.norm(p)
    T = trimesh.geometry.align_vectors(z_axis, d)
    c.apply_transform(T); c.apply_translation(p)
    stars.append(c)
save("p3_lamp_dome", cut(dome, *stars, label="p3 star holes"), "hemisphere dome R45, wall 2 mm, 60 star holes (random, seed 7)")
base = diff(cyl(R, 28, 0, 0, 0, 72), cyl(R - WALL, 28 - WALL, 0, 0, WALL, 72))
posts3 = [cyl(BOSS_OD / 2, 24, x, y, WALL) for x, y in [(30, 0), (-30, 0), (0, 30), (0, -30)]]
holes3 = [cyl(BOSS_ID / 2, 22, x, y, WALL + 2) for x, y in [(30, 0), (-30, 0), (0, 30), (0, -30)]]
base = diff(union(base, *posts3), *holes3)
base = cut(base, cyl(14, WALL * 3, 0, 0, -1), box(40, 16, WALL * 3, cx=0, cy=-30, cz=-1), label="p3 base openings")   # speaker grille hole + battery door
save("p3_lamp_base", base, "cylindrical base Ø90 x 28, 4 bosses, speaker + battery openings")

# ------------------------------------------------------------ design checks
lines = ["| Part | Bounding box mm | ABS mass g | Watertight | Note |", "|---|---|---|---|---|"]
for name, bb, mass, wt, note in checks:
    lines.append(f"| {name} | {bb[0]:.0f} x {bb[1]:.0f} x {bb[2]:.0f} | {mass:.0f} | {'yes' if wt else 'NO'} | {note} |")
lines += ["",
          f"Design rules used: wall {WALL} mm (mouldable ABS 2.0-3.0), boss OD {BOSS_OD} / ID {BOSS_ID} "
          f"(OD/ID = {BOSS_OD / BOSS_ID:.1f}, guideline >= 2.2 for self-tapping screws), button holes 11 mm, edges square (tool-maker adds R>=2 mm).",
          "Mass uses ABS 1.05 g/cm3; use it to sanity-check the Rs 22-28 enclosure piece-cost assumption in the BOM."]
# enclosure material cost per product (resin only; moulding/overhead extra)
RESIN_INR_PER_KG = 200   # assumption, verify with a supplier quote
by = {}
for name, bb, mass, wt, note in checks:
    by[name.split("_")[0]] = by.get(name.split("_")[0], 0) + mass
lines += ["", f"Resin cost at Rs {RESIN_INR_PER_KG}/kg (assumption): " + ", ".join(f"{k} {v:.0f} g = Rs {v * RESIN_INR_PER_KG / 1000:.0f}" for k, v in sorted(by.items())) +
          ". Moulding, regrind loss and finishing add roughly Rs 15-20 per part set."]
(OUT / "checks.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
assert BOSS_OD / BOSS_ID >= 2.2 and WALL >= 2.0
assert all(c[3] for c in checks), "a mesh is not watertight"
