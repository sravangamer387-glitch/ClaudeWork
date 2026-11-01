"""Fin-Ray style compliant gripper finger for delicate produce (print in TPU 95A / flexible resin). Units mm. UNPROTOTYPED first-pass geometry.
The finger is two thin side walls joined by diagonal ribs; the tip wraps around an object under load. Built from overlapping boxes (multi-body STL: slicers union overlapping bodies).
usage: python3 gripper.py   -> out/finger.stl, out/finger_info.json"""
import numpy as np, json, os, struct, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"); os.makedirs(OUT, exist_ok=True)
H, W_BASE, W_TIP, T_WALL, T_RIB, DEPTH, N_RIB = 70.0, 24.0, 4.0, 1.6, 1.2, 20.0, 7        # finger height, widths, wall and rib thickness, depth (z), ribs

def box(c, size, rot=0.0):
    sx, sy, sz = size; v = np.array([[x, y, z] for x in (-sx / 2, sx / 2) for y in (-sy / 2, sy / 2) for z in (-sz / 2, sz / 2)])
    cr, sr = math.cos(rot), math.sin(rot); R = np.array([[cr, -sr, 0], [sr, cr, 0], [0, 0, 1]]); v = v @ R.T + np.array(c)
    f = [(0, 1, 3), (0, 3, 2), (4, 6, 7), (4, 7, 5), (0, 4, 5), (0, 5, 1), (2, 3, 7), (2, 7, 6), (0, 2, 6), (0, 6, 4), (1, 5, 7), (1, 7, 3)]; return v, np.array(f)

def width_at(y): return W_BASE + (W_TIP - W_BASE) * (y / H)                              # tapers from base (y=0) to tip (y=H)
parts = []
for side in (-1, 1):                                                                       # two side walls following the taper (segmented)
    for i in range(20):
        y0, y1 = H * i / 20, H * (i + 1) / 20; ym = 0.5 * (y0 + y1); xm = side * width_at(ym) / 2; ang = math.atan2(side * (width_at(y1) - width_at(y0)) / 2, y1 - y0)
        parts.append(box((xm, ym, 0), (T_WALL, (y1 - y0) * 1.08, DEPTH), rot=-ang))
parts.append(box((0, 1.5, 0), (W_BASE, 3.0, DEPTH)))                                       # base plate (bolt to the gripper jaw)
for k in range(1, N_RIB + 1):                                                              # diagonal ribs, alternating lean: the Fin-Ray effect
    y = H * k / (N_RIB + 1); w = width_at(y) - T_WALL; length = math.hypot(w, 6.0) * 1.02; ang = math.atan2(6.0, w) * (1 if k % 2 else -1)
    parts.append(box((0, y, 0), (length, T_RIB, DEPTH), rot=ang))
V = []; F = []; off = 0
for v, f in parts: V.append(v); F.append(f + off); off += len(v)
V = np.vstack(V); F = np.vstack(F); tri = V[F]; n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)
with open(os.path.join(OUT, "finger.stl"), "wb") as fh:
    fh.write(b"fin-ray finger, mm".ljust(80, b" ")); fh.write(struct.pack("<I", len(F)))
    for i in range(len(F)): fh.write(struct.pack("<12fH", *n[i], *tri[i].reshape(-1), 0))
info = dict(height_mm=H, base_width_mm=W_BASE, tip_width_mm=W_TIP, depth_mm=DEPTH, ribs=N_RIB, triangles=int(len(F)), bbox_mm=[round(float(x), 1) for x in (V.max(0) - V.min(0))],
            contact_note="grip force per finger must be limited by the actuator: pressure = F / (contact length x depth); keep below about 20 kPa for soft fruit (assumption)", material="TPU 95A, 100% wall, 3 perimeters, print upright")
json.dump(info, open(os.path.join(OUT, "finger_info.json"), "w"), indent=1); print(info)
