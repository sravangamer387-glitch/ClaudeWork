"""Drop Quest v1 laser parts (kit sized from the 60 verified levels): board, tower layers, deflector caps, start ramp, target gate.
Unit height = 18 mm = three 6 mm MDF squares; towers 36 x 36 mm on 38 mm cells (1 mm play each side); deflector = 3 mm acrylic cap with a 45-degree slot for a 12 mm wall strip.
Outputs dropquest_sheet_6mm.svg/.dxf (board + tower layers), dropquest_sheet_3mm.svg/.dxf (acrylic caps, walls, start ramp parts). Kerf-compensated."""
import os, sys, math, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "toys10", "sims"))
from gen_gimbal import Sheet, kerf_outline, KERF
HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "levels.json")))
need = collections.Counter(); caps = 0
for l in L:
    c = collections.Counter(); k = 0
    for v in list(l["fixed"].values()) + [tuple(x) for x in l["loose"]]: c[v[0]] += 1; k += 1 if v[1] else 0
    for h in c: need[h] = max(need[h], c[h])
    caps = max(caps, k)
layers = sum(h * 3 * n for h, n in need.items())
CELL, TOWER, BOARD = 38.0, 36.0, 230.0
s6 = Sheet(); s6.W = 600.0
grid_off = (BOARD - 5 * CELL) / 2
s6.part("board 230 x 230 (engrave the 5 x 5 grid and the card coordinates)", [(0, 0), (BOARD, 0), (BOARD, BOARD), (0, BOARD)], [(10, 10, 4), (BOARD - 10, 10, 4), (10, BOARD - 10, 4), (BOARD - 10, BOARD - 10, 4)])
for i in range(layers): s6.part("" if i else f"tower layer 36 x 36 x {layers}", [(0, 0), (TOWER, 0), (TOWER, TOWER), (0, TOWER)])
H6 = s6.save(os.path.join(HERE, "dropquest_sheet_6mm"))
s3 = Sheet(); s3.W = 600.0
for i in range(caps):
    s3.part("deflector cap" if i == 0 else "", [(0, 0), (TOWER, 0), (TOWER, TOWER), (0, TOWER)])
    # 45-degree slot 3.2 x 46 mm along the diagonal for the wall strip (cut as a thin polygon, kerf inward)
    dx, dy = s3.items[-1][1][0]; d = 3.2 / 2 / math.sqrt(2); L2 = 46 / 2 / math.sqrt(2); cx, cy = dx + TOWER / 2 + KERF / 2, dy + TOWER / 2 + KERF / 2
    slot = [(cx - L2 - d, cy + L2 - d), (cx - L2 + d, cy + L2 + d), (cx + L2 + d, cy - L2 + d), (cx + L2 - d, cy - L2 - d)]
    s3.items.append(("poly", kerf_outline(slot, -KERF / 2)))
for i in range(caps): s3.part("deflector wall 48 x 12 (glue into the slot)" if i == 0 else "", [(0, 0), (48, 0), (48, 15), (0, 15)])
s3.part("start ramp side x2", [(0, 0), (60, 0), (60, 4), (0, 3 * 18 + 6)]); s3.part("", [(0, 0), (60, 0), (60, 4), (0, 3 * 18 + 6)])
s3.part("start ramp floor", [(0, 0), (64, 0), (64, 20), (0, 20)]); s3.part("target cup front", [(0, 0), (40, 0), (40, 25), (0, 25)])
H3 = s3.save(os.path.join(HERE, "dropquest_sheet_3mm"))
assert TOWER + 2 <= CELL and 14 + 3 <= 18, "marble 14 mm must fit the 18 mm unit step and towers fit the cells"
print(f"kit: towers h1 x {need[1]}, h2 x {need[2]}, h3 x {need[3]} -> {layers} MDF layers; deflector caps x {caps}; sheets 600 x {H6:.0f} (6 mm) and 600 x {H3:.0f} (3 mm)")
