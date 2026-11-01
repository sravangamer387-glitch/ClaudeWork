"""Interference check: PCB + component envelope, battery, crystal vs the printed shell halves (boolean intersection volumes, mm3). Expect ~0 for every pair that must not touch."""
import os, trimesh
import hilt as H
def load(n): return trimesh.load(os.path.join(H.OUT, n + ".stl"))
up, lo, cr = load("hilt_upper"), load("hilt_lower"), load("crystal")
def inter(a, b): 
    r = trimesh.boolean.intersection([a, b], engine="manifold"); return 0.0 if r.is_empty else abs(float(r.volume))
board = H.box(H.BX0, H.BX0 + H.BOARD_L, -H.BOARD_W / 2, H.BOARD_W / 2, H.BZ, H.BZ + H.BOARD_T)
TOP = H.BZ + H.BOARD_T
def part(bx, by, w, d, h): return H.box(H.BX0 + bx - w / 2, H.BX0 + bx + w / 2, by - H.BOARD_W / 2 - d / 2, by - H.BOARD_W / 2 + d / 2, TOP, TOP + h)
tall = {"BZ1 piezo 12x12x3": part(24, 18, 12, 12, 3.0), "MCU + 4 corner parts 16x16x1.4": part(100, 12.5, 16, 16, 1.4), "J1 battery JST 6x5x6": part(112, 4.5, 6, 5, 6.0), "SW1 slide switch 10x6x3.5": part(123, 5.5, 10, 6, 3.5),
        "J2 ISP header 5.1x7.6x2.5": part(46, 19, 7.6, 5.1, 2.5), "SW2 trigger 3x2.5x2": part(58, 20.5, 3, 2.5, 2.0), "D20 SMA 5x2.7x2.2": part(132, 12, 5, 2.7, 2.2), "U2 IMU 4x4x1": part(70, 9, 4, 4, 1.0)}
cell = H.cyl_x(5.4, H.BX0 + 12, H.BX0 + 12 + 134); cell.apply_translation([0, 0, -8.0])
led_zone = H.box(H.HEAD_X0 + 2, H.HEAD_X1 - 2, H.LED_Y - 1.8, H.LED_Y + 1.8, H.BZ + H.BOARD_T, H.BZ + H.BOARD_T + 1.2)
rows = []
for nm, obj in [("board", board), ("3xAAA cells", cell), ("LED tops", led_zone)] + list(tall.items()):
    rows.append((nm, round(inter(obj, up), 2), round(inter(obj, lo), 2), round(inter(obj, cr), 2)))
for r in rows: print(r)
bad = [r for r in rows if max(r[1:]) > 1.0]
open(os.path.join(H.OUT, "fitcheck.txt"), "w").write("Interference volumes (mm3) of the PCB/components/cells/LEDs against upper shell, lower shell, crystal:\n" + "\n".join(str(r) for r in rows) + ("\nFAIL: " + str([r[0] for r in bad]) if bad else "\nPASS: no interference above 1 mm3") + "\n")
print("FAIL" if bad else "PASS")
