"""Jal-Netra spool (Z-body) for 3D printing (SLS PA12 / SLA resin prototype; production: injection-moulded PPSU or brass-insert body).
Axis along X. Measuring bore D=12 mm over L=60 mm; end chambers D=16 mm hold the piezo face and receive the side ports (inlet +Y at the left head, outlet -Y at the right head)."""
import trimesh, numpy as np, json, math, os
from trimesh.creation import cylinder, box
D, L = 12.0, 60.0; DC, LC = 16.0, 9.0; OD_T, OD_H, LH = 20.0, 32.0, 20.0; PORT_D, BOSS_OD, BOSS_L = 12.0, 26.0, 16.0; PZT_D, PZT_T, POCKET_D, POCKET_L = 10.0, 2.0, 12.0, 6.0
def cyl_x(r, h, x): c = cylinder(radius=r, height=h, sections=64); c.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0])); c.apply_translation([x, 0, 0]); return c
def cyl_y(r, h, y, x): c = cylinder(radius=r, height=h, sections=64); c.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0])); c.apply_translation([x, y, 0]); return c
xl, xr = -L / 2, L / 2                                       # inner faces of the measuring bore
outer = cyl_x(OD_T / 2, L + 2 * LC, 0)
for sgn in (-1, 1): outer = outer.union(cyl_x(OD_H / 2, LH, sgn * (L / 2 + LC - LH / 2 + 4)))        # heads overlap the bore ends
outer = outer.union(cyl_y(BOSS_OD / 2, BOSS_L + OD_H / 2, (BOSS_L + OD_H / 2) / 2, xl - LC / 2 - 2))       # inlet boss +Y
outer = outer.union(cyl_y(BOSS_OD / 2, BOSS_L + OD_H / 2, -(BOSS_L + OD_H / 2) / 2, xr + LC / 2 + 2))     # outlet boss -Y
fluid = cyl_x(D / 2, L + 0.2, 0)
for sgn in (-1, 1): fluid = fluid.union(cyl_x(DC / 2, LC, sgn * (L / 2 + LC / 2)))                       # end chambers
fluid = fluid.union(cyl_y(PORT_D / 2, BOSS_L + OD_H, (BOSS_L + OD_H) / 2, xl - LC / 2 - 2)).union(cyl_y(PORT_D / 2, BOSS_L + OD_H, -(BOSS_L + OD_H) / 2, xr + LC / 2 + 2))
pockets = None
for sgn in (-1, 1):
    p = cyl_x(POCKET_D / 2, POCKET_L, sgn * (L / 2 + LC + POCKET_L / 2 - 0.0)); pockets = p if pockets is None else pockets.union(p)         # transducer pockets behind the chamber
body = outer.difference(fluid).difference(pockets)
xmax = L / 2 + LC + POCKET_L
cap = lambda s: cyl_x(OD_H / 2 - 1.0, 2.0, s * (xmax + 1.0))
body = body.union(cap(1).difference(cyl_x(2.0, 3, 1 * (xmax + 1.0)))).union(cap(-1).difference(cyl_x(2.0, 3, -(xmax + 1.0))))      # rear caps with a 4 mm cable hole
body.export(os.path.join(os.path.dirname(__file__), "spool_body.stl")); fluid.export(os.path.join(os.path.dirname(__file__), "spool_fluid_volume.stl"))
pz = cyl_x(PZT_D / 2, PZT_T, 0); pz.export(os.path.join(os.path.dirname(__file__), "piezo_disc_reference.stl"))
vol_ml = fluid.volume / 1000; v12 = lambda q: q / 60000 / (math.pi * (D / 2000) ** 2)
def dp_kpa(q_lpm, K=2.6):
    v = v12(q_lpm); return K * 1000 * v * v / 2 / 1000
t_wall = (OD_T - D) / 2; sigma = 1.0 * (OD_T / 2) / t_wall                                       # thin-wall hoop stress at 10 bar (1 MPa) in MPa
info = dict(body_watertight=bool(body.is_watertight), fluid_volume_ml=round(vol_ml, 2), overall_length_mm=round(body.bounds[1][0] - body.bounds[0][0], 1), overall_height_mm=round(body.bounds[1][1] - body.bounds[0][1], 1), min_wall_mm=t_wall,
            hoop_stress_mpa_at_10bar=round(sigma, 2), dp_kpa={q: round(dp_kpa(q), 2) for q in (1, 5, 10, 20, 30)}, velocity_m_s={q: round(v12(q), 2) for q in (1, 5, 10, 20, 30)})
json.dump(info, open(os.path.join(os.path.dirname(__file__), "spool_info.json"), "w"), indent=1); print(info)
