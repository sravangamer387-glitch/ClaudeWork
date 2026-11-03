#!/usr/bin/env python3
"""TRISHNA mechanical CAD (parametric, manifold3d -> STL). Run with a Python that has manifold3d + trimesh + numpy:
    python3 trishna_cad.py            -> out/*.stl, out/cad_report.json (volumes, sizes, checks)

Coordinate convention for the two enclosure boxes (wall-mounted, back face on the wall):
    X = horizontal along the wall, Y = vertical (up), Z = away from the wall (the lid is at max Z, facing the user).
    Everything is printed back-face down on the bed (Z up while printing), so no part needs supports except where noted.
Sensor block: its own Z axis is VERTICAL in service (bore vertical, inlet at the bottom, outlet at the top).
All dimensions in millimetres."""
import json, math, os
from manifold3d import Manifold
import numpy as np, trimesh

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
SEG = 64

# ------------------------------------------------------------------ primitives
def box(x0, x1, y0, y1, z0, z1): return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
def cylz(r, z0, z1, x=0.0, y=0.0, r2=None):
    return Manifold.cylinder(z1 - z0, r, r if r2 is None else r2, SEG).translate([x, y, z0])
def cylx(r, x0, x1, y, z):   # axis along +X from x0 to x1
    return Manifold.cylinder(x1 - x0, r, r, SEG).rotate([0, 90, 0]).translate([x0, y, z])
def cyly(r, y0, y1, x, z):   # axis along +Y from y0 to y1
    return Manifold.cylinder(y1 - y0, r, r, SEG).rotate([-90, 0, 0]).translate([x, y0, z])
def union(parts):
    m = parts[0]
    for p in parts[1:]: m = m + p
    return m
def save(m, name, report):
    mesh = m.to_mesh(); tm = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts), process=True)
    os.makedirs(OUT, exist_ok=True); tm.export(os.path.join(OUT, name + ".stl"))
    bb = tm.bounds
    report[name] = dict(size_mm=[round(float(v), 1) for v in (bb[1] - bb[0])], volume_cm3=round(m.volume() / 1000.0, 2),
                        watertight=bool(tm.is_watertight), est_mass_g_petg=round(m.volume() / 1000.0 * 1.27, 1))
    return tm

# ================================================================== 1. SENSOR BLOCK (2.0 mL flow cell)
SB = dict(W=36.0, H=38.0, R=6.0, z_bot=10.0, z_top=27.0, cone=2.0, ch_r=1.5, m5_pilot_r=2.1, m5_depth=7.0,
          port_r=2.55, cb_r=3.6, cb_from=13.0, probe_r=3.1, probe_cb_r=4.6, probe_cb_from=14.0, probe_tip_y=2.0,
          z_blue=13.0, z_ir=23.0, z_pdtx=18.0, z_pdsc=20.5, z_probe=11.5, z_elec=25.5, x_elec=3.5, elec_r=0.45, mount=14.0, mount_r=1.7)

def sensor_cavity(with_probe=True):
    s = SB; R, zb, zt, c = s["R"], s["z_bot"], s["z_top"], s["cone"]
    cav = union([cylz(R, zb, zt), cylz(s["ch_r"], zb - c, zb, r2=R), cylz(R, zt, zt + c, r2=s["ch_r"])])
    if with_probe:   # the DS18B20 sheath (6 mm) enters from +Y and stops 2 mm past the bore axis plane -> it displaces liquid
        cav = cav - cyly(3.0, s["probe_tip_y"], R + 1.0, 0.0, s["z_probe"])
    return cav

def tilted_port(xw, zw, xt, zt, r, rcb, t_cb, t_end):
    """Port whose axis runs from the target point (xt, 0, zt) through the bore-wall point (xw, 0, zw) and on out of the block:
    through-hole of radius r from 0.5 mm inside the wall to t_cb along the axis, then a counterbore of radius rcb to t_end."""
    dx, dz = xw - xt, zw - zt; L = math.hypot(dx, dz); ux, uz = dx / L, dz / L
    phi = math.degrees(math.atan2(uz, ux))
    def seg(rad, t0, t1):
        c = Manifold.cylinder(t1 - t0, rad, rad, SEG).rotate([0, 90, 0]).rotate([0, -phi, 0])
        return c.translate([xw + ux * t0, 0, zw + uz * t0])
    return [seg(r, -0.5, t_cb + 0.01), seg(rcb, t_cb, t_end)]

def sensor_block(report):
    s = SB; W, H, R = s["W"], s["H"], s["R"]; h = W / 2
    body = box(-h, h, -h, h, 0, H)
    cuts = [cylz(R, s["z_bot"], s["z_top"]), cylz(s["ch_r"], s["z_bot"] - s["cone"], s["z_bot"], r2=R), cylz(R, s["z_top"], s["z_top"] + s["cone"], r2=s["ch_r"]),
            cylz(s["ch_r"], 0, s["z_bot"] - s["cone"] + 0.01), cylz(s["m5_pilot_r"], -0.01, s["m5_depth"]),                        # inlet: M5 tapped port + 3 mm channel
            cylz(s["ch_r"], s["z_top"] + s["cone"] - 0.01, H + 0.01), cylz(s["m5_pilot_r"], H - s["m5_depth"], H + 0.01)]          # outlet
    for z in (s["z_blue"], s["z_ir"]):            # +X: blue and IR LEDs (5 mm), each port tilted to aim at the transmission PD (-R, 0, z_pdtx)
        cuts += tilted_port(R, z, -R, s["z_pdtx"], s["port_r"], s["cb_r"], s["cb_from"] - R, 20.0)
    cuts += [cylx(s["port_r"], -s["cb_from"] - 0.01, -R + 0.5, 0, s["z_pdtx"]), cylx(s["cb_r"], -h - 0.01, -s["cb_from"], 0, s["z_pdtx"])]   # -X: transmission PD
    cuts += [cyly(s["port_r"], R - 0.5, s["cb_from"] + 0.01, 0, s["z_pdsc"]), cyly(s["cb_r"], s["cb_from"], h + 0.01, 0, s["z_pdsc"])]      # +Y: 90-degree scatter PD
    # (the scatter PD shares the +Y wall with the probe and the electrodes, so it looks at the plain black -Y wall, not at metal)
    cuts += [cyly(s["probe_r"], R - 0.5, s["probe_cb_from"] + 0.01, 0, s["z_probe"]), cyly(s["probe_cb_r"], s["probe_cb_from"], h + 0.01, 0, s["z_probe"])]  # +Y: DS18B20
    for x in (-s["x_elec"], s["x_elec"]):        # +Y: titanium electrodes (drill 1.0 mm after printing)
        cuts.append(cyly(s["elec_r"], R - 0.5, h + 0.01, x, s["z_elec"]))
    for x in (-s["mount"], s["mount"]):
        for y in (-s["mount"], s["mount"]): cuts.append(cylz(s["mount_r"], -0.01, H + 0.01, x, y))
    blk = body - union(cuts)
    tm = save(blk, "trishna_sensor_block", report)
    v_geom = sensor_cavity(False).volume() / 1000.0; v_wet = sensor_cavity(True).volume() / 1000.0
    report["trishna_sensor_block"].update(chamber_geometric_ml=round(v_geom, 3), chamber_wetted_ml_with_probe=round(v_wet, 3),
        bore="12.0 mm dia x 17.0 mm + 2 mm cones top and bottom", optical_path_mm=12.0,
        ports={"+X z13 (tilted 22.6 deg down-out)": "LED 450 nm aimed at the transmission PD", "+X z23 (tilted 22.6 deg up-out)": "LED 850 nm aimed at the transmission PD",
               "-X z18": "PD transmission (SFH 203, wide angle)", "+Y z20.5": "PD 90-degree scatter (looks at the plain -Y wall; the IR beam crosses the axis at z 20.5)",
               "+Y z11.5": "DS18B20 6 mm probe (tip 2 mm past axis)", "+Y z25.5 x+-3.5": "Ti electrodes 1.0 mm", "bottom": "M5 inlet", "top": "M5 outlet"})
    return v_wet

# ------------------------------------------------------------------ generic split-lid box
WALL, FLOOR, LID = 2.5, 3.0, 3.0
GROOVE_W, GROOVE_D = 2.7, 1.9            # for 2.5 mm solid silicone cord (about 25 % squeeze)
INSERT_R, INSERT_D = 2.0, 6.0            # M3 heat-set insert, 4.0 mm hole x 6 deep
def screw_points(ix, iy, nx, ny):
    pts = []
    for i in range(nx):
        x = -WALL / 2 + (ix + WALL) * i / (nx - 1)
        pts += [(x, -WALL / 2 - 3.5), (x, iy + WALL / 2 + 3.5)]
    for j in range(1, ny - 1):
        y = -WALL / 2 + (iy + WALL) * j / (ny - 1)
        pts += [(-WALL / 2 - 3.5, y), (ix + WALL / 2 + 3.5, y)]
    return pts

def make_box(ix, iy, iz, nx, ny, wall_cuts, inside_add, inside_cut, name, report):
    """Inner cavity [0,ix] x [0,iy] x [FLOOR, FLOOR+iz]. Screw lugs outside the walls (the gasket never crosses a screw hole).
    Returns (base, lid). The lid has a gasket groove over the wall centre line and a 1.5 mm locating skirt."""
    ox0, ox1, oy0, oy1 = -WALL, ix + WALL, -WALL, iy + WALL; zt = FLOOR + iz
    base = box(ox0, ox1, oy0, oy1, 0, zt) - box(0, ix, 0, iy, FLOOR, zt + 1)
    lugs = screw_points(ix, iy, nx, ny)
    for (x, y) in lugs:
        base = base + cylz(4.5, 0, zt, x, y) - cylz(INSERT_R, zt - INSERT_D, zt + 0.1, x, y)
    # wall-mount ears (back plane) with 4.5 mm holes and 8 mm counterbores for M4 / No.8 wall screws
    ears = [(ox0 - 9, oy0 + 15), (ox1 + 9, oy0 + 15), (ox0 - 9, oy1 - 15), (ox1 + 9, oy1 - 15)]
    for (x, y) in ears:
        tab = box(ox0 - 16, ox0 + 0.01, y - 7, y + 7, 0, 5) if x < ox0 else box(ox1 - 0.01, ox1 + 16, y - 7, y + 7, 0, 5)
        base = base + tab - cylz(2.25, -0.1, 5.1, x, y) - cylz(4.0, 3.0, 5.1, x, y)
    if inside_add: base = base + union(inside_add)
    if wall_cuts: base = base - union(wall_cuts)
    if inside_cut: base = base - union(inside_cut)
    # lid
    lid = box(ox0 - 9.5, ox1 + 9.5, oy0 - 9.5, oy1 + 9.5, 0, LID)
    for (x, y) in lugs: lid = lid - cylz(1.7, -0.1, LID + 0.1, x, y) - cylz(3.2, LID - 1.6, LID + 0.1, x, y)   # M3 clearance + head recess
    gx0, gx1, gy0, gy1 = -WALL / 2 - GROOVE_W / 2, ix + WALL / 2 + GROOVE_W / 2, -WALL / 2 - GROOVE_W / 2, iy + WALL / 2 + GROOVE_W / 2
    ring = box(gx0, gx1, gy0, gy1, -0.1, GROOVE_D) - box(gx0 + GROOVE_W, gx1 - GROOVE_W, gy0 + GROOVE_W, gy1 - GROOVE_W, -0.2, GROOVE_D + 0.1)
    lid = lid - ring                                                     # groove on the lid underside (z = 0 face)
    skirt = box(0.25, ix - 0.25, 0.25, iy - 0.25, -1.5, 0.01) - box(1.85, ix - 1.85, 1.85, iy - 1.85, -1.6, 0.1)
    lid = lid + skirt
    # rounded corner relief is cosmetic; corners of the lid stay square for simple printing
    save(base, name + "_base", report); save(lid.rotate([180, 0, 0]), name + "_lid", report)   # lid exported groove-up for printing
    report[name + "_base"].update(inner_mm=[ix, iy, iz], outer_mm=[round(ix + 2 * WALL, 1), round(iy + 2 * WALL, 1), round(zt, 1)], lid_screws=len(lugs))
    return base, lid

GLAND_HOLE = {"M12": 12.3, "M16": 16.3, "M20": 20.3}

# ================================================================== 2. CHAMBER A: controller box (dry, mounted ABOVE chamber B)
A = dict(ix=100.0, iy=136.0, iz=36.0, pcb_off=(8.0, 8.0), standoff=6.0)
def pcb_to_box(px, py):  # PCB x (0..120) runs up the wall (box Y), PCB y (0..84) runs along X; PCB origin at the cavity offset
    return A["pcb_off"][0] + py, A["pcb_off"][1] + px
def chamber_a(report):
    ix, iy, iz = A["ix"], A["iy"], A["iz"]; zf = FLOOR
    add, cut = [], []
    for (px, py) in [(3.5, 3.5), (116.5, 3.5), (3.5, 80.5), (116.5, 80.5)]:
        x, y = pcb_to_box(px, py)
        add.append(cylz(3.5, zf - 0.01, zf + A["standoff"], x, y)); cut.append(cylz(INSERT_R, zf + A["standoff"] - INSERT_D, zf + A["standoff"] + 0.1, x, y))
    zpcb_top = zf + A["standoff"] + 1.6
    wc = []
    jx, _ = pcb_to_box(8, 14)                                   # barrel jack J1 faces down through the bottom wall (drip-safe)
    wc.append(cyly(5.2, -WALL - 0.1, 0.1, jx, zpcb_top + 6.5))
    glands = {"G1 (M16) pump+valve 4-core from chamber B": (46.0, "M16"), "G2 (M16) sensor 8-core from chamber B": (70.0, "M16"), "G3 (M12) optics shielded cable": (91.0, "M12")}
    for k, (x, g) in glands.items(): wc.append(cyly(GLAND_HOLE[g] / 2, -WALL - 0.1, 0.1, x, zf + 20.0))
    side = {"G4 (M12) DS18B20 cable": 30.0, "G5 (M12) sump probe cable": 55.0, "G6 (M12) ToF sensor cable": 80.0, "G7 (M12) telemetry USB-serial": 105.0}
    for k, y in side.items(): wc.append(cylx(GLAND_HOLE["M12"] / 2, -WALL - 0.1, 0.1, y, zf + 20.0))
    make_box(ix, iy, iz, 3, 4, wc, add, cut, "trishna_chamberA", report)
    report["trishna_chamberA_base"].update(bottom_wall=dict({"J1 barrel jack hole 10.4 mm": round(jx, 1)}, **{k: v[0] for k, v in glands.items()}), left_wall_heights=side,
                                           pcb_standoffs="6 mm, M3 heat-set inserts; PCB x axis vertical, barrel jack down")

# ================================================================== 3. CHAMBER B: fluidics box (wet, mounted BELOW chamber A)
B = dict(ix=170.0, iy=150.0, iz=75.0, blk_x=85.0, blk_z=36.0)   # block: its +Y (probe side) points along +X, its +X (LEDs) toward the lid
def chamber_b(report):
    ix, iy, iz = B["ix"], B["iy"], B["iz"]; zf = FLOOR
    add, cut = [], []
    # V-floor (on the bottom wall, the lowest surface in service): 4 mm high at the ends, 0 at the drain in the middle
    xs = np.linspace(0, ix, 41)
    for i in range(40):
        xm = (xs[i] + xs[i + 1]) / 2; hgt = 4.0 * abs(xm - ix / 2) / (ix / 2)
        if hgt > 0.2: add.append(box(xs[i], xs[i + 1], 0, hgt, zf - 0.01, zf + iz))
    # leak probe: two M3 stainless screws through the bottom wall, 12 mm either side of the drain (tips 3 mm into the well)
    for x in (ix / 2 - 12, ix / 2 + 12): cut.append(cyly(1.25, -WALL - 0.1, 3.0, x, zf + 12.0))      # tap M3 (2.5 mm pilot)
    # sensor-block shelf: plate perpendicular to the back, 5 mm thick, top face at y = 32
    sx, sz = B["blk_x"], B["blk_z"]
    add.append(box(sx - 26, sx + 26, 27.0, 32.0, zf - 0.01, sz + 24.0))
    add.append(box(sx - 26, sx - 21, 0.01, 27.0, zf - 0.01, sz + 24.0)); add.append(box(sx + 21, sx + 26, 0.01, 27.0, zf - 0.01, sz + 24.0))   # shelf legs
    cut.append(cyly(8.0, 26.9, 32.1, sx, sz))                                                        # inlet fitting + tube through the shelf
    for dx in (-14, 14):
        for dz in (-14, 14): cut.append(cyly(1.7, 26.9, 32.1, sx + dx, sz + dz))
    # pump bracket bosses (universal bracket screws down with 4 x M3 into heat-set inserts) and valve saddle bosses
    for (x, y) in [(20, 75), (70, 75), (20, 125), (70, 125), (125, 100), (155, 100), (125, 135), (155, 135)]:
        add.append(cylz(4.0, zf - 0.01, zf + 6.0, x, y)); cut.append(cylz(INSERT_R, zf + 0.5, zf + 6.1, x, y))
    # cable-tie anchors for the tubing (bridges printed flat)
    for (x, y) in [(40, 45), (130, 45), (100, 75), (100, 120), (40, 140)]:
        add.append(box(x - 6, x + 6, y - 2, y + 2, zf - 0.01, zf + 5.0)); cut.append(box(x - 3.5, x + 3.5, y - 2.1, y + 2.1, zf + 0.9, zf + 3.6))
    wc = []
    bottom = {"P1 sample in (M12 gland on 5 mm tube)": (40.0, "M12"), "P2 waste out (M12 gland)": (62.0, "M12"), "P4 leak drain (4 mm barb, glue)": (ix / 2, "drain"),
              "P3 fresh water in (M12 gland)": (128.0, "M12")}
    for k, (x, g) in bottom.items():
        wc.append(cyly(GLAND_HOLE[g] / 2 if g != "drain" else 3.1, -WALL - 0.1, 0.1 if g != "drain" else 1.0, x, zf + (20.0 if g != "drain" else 3.5)))
    top = {"G1 (M16) to chamber A: pump+valve": (55.0, "M16"), "G2 (M16) to chamber A: sensors": (80.0, "M16"), "G3 (M12) optics": (102.0, "M12"), "G4 (M12) DS18B20": (122.0, "M12")}
    for k, (x, g) in top.items(): wc.append(cyly(GLAND_HOLE[g] / 2, iy - 0.1, iy + WALL + 0.1, x, zf + 25.0))
    make_box(ix, iy, iz, 4, 4, wc, add, cut, "trishna_chamberB", report)
    report["trishna_chamberB_base"].update(bottom_wall={k: v[0] for k, v in bottom.items()}, top_wall={k: v[0] for k, v in top.items()},
                                           sensor_shelf="top face y=32, block centre x=85, z=36 from the back face; block probe side (+Y) toward +X, LED side (+X) toward the lid; 4 x M3 x 45 screws + nuts through the block corners",
                                           leak_probe="2 x M3 x 10 A2 stainless screws at x=73 and x=97 through the bottom wall")

# ================================================================== 4. SUMP INSERT (sits on the urinal drain strainer)
def sump_insert(report, d_drain=70.0):
    R = d_drain / 2; base = cylz(R, 0, 3.0) - union([cylz(4.0, -0.1, 3.1, (R - 8) * math.cos(a), (R - 8) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 10, endpoint=False)])
    cup = cylz(17.5, 0, 22.0) - cylz(15.0, 2.0, 22.1)                      # 30 mm inside, 20 mm deep above a 2 mm floor
    notch = box(-4, 4, 12, 20, 18.0, 22.1)                                  # overflow notch: level stays at 18 mm -> 30 mm dia x 16 mm = 11.3 mL
    port = cylx(2.1, 13.0, 17.6, 0, 5.0)                                    # M5 tapped side port low in the cup -> 4 mm barb fitting
    pin_holes = [cyly(0.45, -17.6, -13.0, x, 9.0) for x in (-5, 5)]        # Ti stream-probe pins, 10 mm apart, 9 mm above the floor
    feet = union([cylz(3.0, -6.0, 0.01, (R - 4) * math.cos(a), (R - 4) * math.sin(a)) for a in (0.3, 2.4, 4.5)])
    m = base + cup + feet - notch - port - union(pin_holes)
    save(m, "trishna_sump_insert", report)
    report["trishna_sump_insert"].update(cup_ml_to_overflow=round(math.pi * 15.0 ** 2 * 16.0 / 1000.0, 1), drain_diameter_param=d_drain)

# ================================================================== 5. small brackets
def pump_bracket(report):
    # universal plate for 12 V peristaltic pumps with a 2-hole front flange (M3, 30..42 mm hole spacing) and a motor up to 28 mm dia
    p = box(-30, 30, -30, 30, 0, 4.0) + box(-30, -26, -30, 30, 0, 40.0)            # base plate + upright flange plate (40 mm high)
    p = p - cylx(14.5, -30.1, -25.9, 0, 22.0)                                       # motor / shaft clearance through the upright
    for s in (-1, 1): p = p - box(-30.1, -25.9, s * 15 - 1.7 - 6 * (s > 0), s * 15 + 1.7 + 6 * (s < 0), 20.3, 23.7)   # slots for M3 at 30..42 mm spacing
    for (x, y) in [(-25, -25), (25, -25), (-25, 25), (25, 25)]: p = p - cylz(1.7, -0.1, 4.1, x, y)   # to the chamber-B bosses (50 x 50 mm)
    save(p, "trishna_pump_bracket", report)

def valve_saddle(report):
    s = box(-20, 20, -22, 22, 0, 4.0) + box(-20, 20, -14, 14, 0, 12.0) - cylx(15.0, -20.1, 20.1, 0, 27.0)   # cradle for 22..32 mm valve bodies
    for x in (-10, 10): s = s - box(x - 2.0, x + 2.0, -14.1, 14.1, 4.0, 6.5)                                # zip-tie slots (5 mm ties)
    for (x, y) in [(-15, -17.5), (15, -17.5), (-15, 17.5), (15, 17.5)]: s = s - cylz(1.7, -0.1, 4.1, x, y)
    save(s, "trishna_valve_saddle", report)

def probe_retainer(report):
    # clamps an LED / photodiode / DS18B20 into its counterbore (2 x M2 self-tapping into the block face) - light-tight cover
    r = box(-6, 6, -9, 9, 0, 3.0) - cylz(1.2, -0.1, 3.1, 0, -6.5) - cylz(1.2, -0.1, 3.1, 0, 6.5) - box(-1.6, 1.6, -3.5, 3.5, -0.1, 3.1)
    save(r, "trishna_port_retainer", report)

if __name__ == "__main__":
    rep = {}
    v = sensor_block(rep)
    chamber_a(rep); chamber_b(rep); sump_insert(rep); pump_bracket(rep); valve_saddle(rep); probe_retainer(rep)
    rep["checks"] = {"sensor chamber wetted volume within 2.0 +/- 0.1 mL": abs(v - 2.0) <= 0.1,
                     "all parts watertight meshes": all(r.get("watertight", True) for k, r in rep.items() if isinstance(r, dict) and "watertight" in r),
                     "every part fits a 220 x 220 mm bed": all(max(r["size_mm"][0], r["size_mm"][1]) <= 220 for k, r in rep.items() if isinstance(r, dict) and "size_mm" in r)}
    json.dump(rep, open(os.path.join(OUT, "cad_report.json"), "w"), indent=1)
    print(json.dumps(rep, indent=1))
