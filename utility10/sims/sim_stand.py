"""Fold-flat Laptop/Tablet Stand (laser-cut 6 mm MDF/plywood or 5 mm acrylic): hinged top plate + back strut with 3 notches (angles ~12, 18, 25 deg).
Verifies: strut length per angle, tipping margin and sliding with typing force, strut buckling (Euler) and plate bending, nesting."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from cadlib import *
OUT = os.path.join(os.path.dirname(__file__), "..", "out"); DOC = os.path.join(os.path.dirname(__file__), "..", "docs")
PW, PD, T = 300.0, 250.0, 6.0          # plate width, depth(length along the slope), thickness
BASE_D = 230.0                         # base depth
M_LAP, G, MU = 2.5, 9.81, 0.4
PUSH = 6.0                             # design push (typing / touch) in N: assumption; a deliberate 15 N shove is reported separately
REAR = 40.0                            # base extends this far behind the plate's back edge          # laptop kg (heavy case), rubber feet friction (assumption)
E = 2500.0; lines = []
# geometry: plate hinged at the front edge at height h0 above the table; back edge held by a strut resting in a notch
H0 = 12.0
lines.append(f"| tilt deg | back-edge height mm | strut length mm | horizontal run of plate mm | tipping margin, push {PUSH:.0f} N | slide: friction needed | margin with a hard 15 N shove |")
lines.append("|---|---|---|---|---|---|---|")
ok = True
for ang in (12, 18, 25):
    a = math.radians(ang); hb = H0 + PD * math.sin(a); run = PD * math.cos(a)
    strut = hb - T                                   # vertical-ish prop from base to underside of plate (simplified, strut vertical)
    Wt = M_LAP * G; x_com = run / 2
    def margin(F):
        h = H0 + PD * math.sin(a) / 2 + 150; m_over = F * h
        return min(Wt * (run + REAR - x_com) / m_over, Wt * x_com / m_over)       # about the rear foot edge / about the front foot
    mu_need = PUSH / Wt; mg = margin(PUSH); mg15 = margin(15.0)
    ok &= mg > 1.5 and mu_need < MU
    lines.append(f"| {ang} | {hb:.0f} | {strut:.0f} | {run:.0f} | x{mg:.1f} | {mu_need:.2f} (rubber feet {MU}) | x{mg15:.1f} {'(slides: needs mu 0.61)' if 15/Wt > MU else ''} |")
# strut buckling and plate bending
w_strut, t_strut = 25.0, T
I = w_strut * t_strut ** 3 / 12; L = H0 + PD * math.sin(math.radians(25)) - T
Pcr = math.pi ** 2 * E * I / (1.0 * L) ** 2          # pinned-pinned about the weak axis (thickness direction)
load_on_strut = M_LAP * G * 0.5
lines.append(f"\nStrut {w_strut:.0f}x{t_strut:.0f} mm, longest {L:.0f} mm: Euler buckling load {Pcr:.0f} N vs working load {load_on_strut:.0f} N (factor {Pcr/load_on_strut:.0f}).")
I_pl = PW * T ** 3 / 12; w = M_LAP * G / PW; d = 5 * w * PW ** 4 / (384 * E * I_pl)
lines.append(f"Plate bending under a {M_LAP} kg laptop (UDL over {PW:.0f} mm, simply supported, strut + hinge): deflection {d:.2f} mm (span/{PW/d:.0f}); needs a centre strut ({'OK' if PW/d >= 300 else 'sag risk without it'}).")
ok &= Pcr / load_on_strut > 5
# parts
def notch(x, y, w=T + 0.1, h=8): return rect(x, y, w, h)
plate = dict(poly=[rect(0, 0, PW, PD)], circles=[(20, 20, 3), (PW - 20, 20, 3)])
lip = dict(poly=[rect(0, 0, PW, 22)])
base = dict(poly=[rect(0, 0, PW, BASE_D + REAR)] , engrave=[[(PW / 2 - 5, 20), (PW / 2 + 5, 20)]])
strut_p = dict(poly=[[(0, 0), (155, 0), (155, 25), (0, 25)]] + [notch(30 + i * 40, 25 - 8) for i in range(3)][:0])
# a strut with three notches along its length: stepped teeth on its top edge
teeth = [(0, 0), (160, 0), (160, 25)]
for i in (2, 1, 0): teeth += [(30 + i * 40 + 12, 25), (30 + i * 40 + 12, 17), (30 + i * 40, 17), (30 + i * 40, 25)]
teeth += [(0, 25)]
strut_p = dict(poly=[teeth])
parts = {"top_plate": plate, "front_lip": lip, "base": base, "strut_a": strut_p, "strut_b": strut_p, "hinge_rail": dict(poly=[rect(0, 0, PW, 20)])}
placed = nest(parts, 600, 600); bad = overlap(placed)
write(placed, 600, 600, os.path.join(OUT, "laptop_stand.svg"), os.path.join(OUT, "laptop_stand.dxf"))
lines.append(f"Parts nest on one 600x600 mm sheet, {'no overlaps' if not bad else 'OVERLAPS '+str(bad)}. Not verified: hinge strength (use a 2 mm piano hinge or cloth tape prototype), comfort, heat (stand is open for airflow), real friction.")
open(os.path.join(DOC, "results_stand.md"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines)); sys.exit(0 if ok and not bad else 1)
