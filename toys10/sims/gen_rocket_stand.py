"""Paper Rocket v1 (stomp launcher): laser-cut tilt stand (3 mm MDF) for an 18 mm launch tube, plus the spec sheet.
No pump, no valve, no stored pressure: a foot stomp on a 2 L PET bottle (or a stomp bag) pushes air through a 1 m hose into the launch tube.
Outputs ../out/rocket_stand.svg/.dxf and ../out/rocket_v1_spec.md. Kerf-compensated. First-pass: test-fit the tube and hose before a batch."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ezdxf
from gen_gimbal import kerf_outline, Sheet, KERF
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
TUBE_OD = 18.0; ANGLES = (30, 45, 60); PIVOT_H = 40.0; R_STOP = 60.0
def main():
    sh = Sheet(); sh.W = 600.0
    sh.part("base plate 200 x 120", [(0, 0), (200, 0), (200, 120), (0, 120)], [(20, 20, 5), (180, 20, 5), (20, 100, 5), (180, 100, 5)])
    cheek = [(0, 0), (110, 0), (110, PIVOT_H + 20), (60, PIVOT_H + R_STOP + 15), (0, PIVOT_H + 20)]
    holes = [(30, PIVOT_H, 6.2)] + [(30 + R_STOP * math.cos(math.radians(a)), PIVOT_H + R_STOP * math.sin(math.radians(a)) * 0 + 0, 0) for a in ()]
    stops = [(30 + R_STOP * math.cos(math.radians(a)), PIVOT_H + R_STOP * math.sin(math.radians(a)), 6.2) for a in ANGLES]
    cheek_f = [(x, PIVOT_H + R_STOP + 15 - y) for x, y in cheek]                                   # draw with y up
    holes_f = [(x, PIVOT_H + R_STOP + 15 - y, d) for x, y, d in [(30, PIVOT_H, 6.2)] + stops]
    for k in range(2): sh.part(f"cheek {k + 1} (pivot + angle stops 30/45/60)", cheek_f, holes_f)
    arm = [(0, 0), (140, 0), (140, 24), (0, 24)]
    for k in range(2): sh.part(f"tilt arm {k + 1}", arm, [(10, 12, 6.2), (10 + R_STOP, 12, 6.2), (120, 12, TUBE_OD + 0.4)])
    sh.part("tube saddle", [(0, 0), (40, 0), (40, 30), (0, 30)], [(20, 12, TUBE_OD + 0.4)])
    H = sh.save(os.path.join(OUT, "rocket_stand"))
    assert H <= 400, H
    spec = f"""# Paper Rocket v1: stomp launcher specification (replaces the pumped chamber and relief valve)

Why: the pumped design needed a 0.29 bar relief valve and a pressure chamber; that valve is hard to source and stored pressure is the main hazard. The stomp launcher has **no pump, no valve and no stored pressure**: each launch is one foot stomp, so the energy cannot build up.

Parts (all bought in India, about Rs 250 for a prototype):
- 2 L PET bottle (or a 3 L PVC stomp bag) as the air bladder.
- 1.0 m clear PVC or silicone hose, 12 mm ID; two hose clamps.
- Launch tube: 18 mm OD rigid PVC electrical conduit, 300 mm long, end chamfered and sanded (no sharp edge).
- Reducer/joint: 12 mm barb to 18 mm conduit (or a 20 mm conduit coupler with a hose barb glued in), PVC solvent cement.
- Laser-cut stand: `toys10/out/rocket_stand.svg` / `.dxf` (3 mm MDF): base, two cheeks with pivot and angle-stop holes (30/45/60 deg), two tilt arms with an {TUBE_OD + 0.4:.1f} mm tube hole, saddle; 6 mm dowels for the pivot and the stop pin; 4 x M4 screws or glue.
- Rockets: rolled on the 18 mm tube from 80 gsm paper (templates in the manual), **foam nose mandatory**, 4 g target mass.

Energy check: a child's stomp gives a short pulse of about 0.2-0.4 bar; with the 4 g rocket the model in `docs/results_rocket.md` gives 0.2-0.5 J and 9-16 m range. Measure range with three users before any sale; if a rocket lands farther than 20 m, shorten the tube to 200 mm.

Build and test:
1. Cut the stand; glue the cheeks to the base; fit the tilt arms on the pivot dowel; choose an angle with the stop dowel.
2. Push the hose onto the barb and clamp; glue the barb into the tube; push the tube through both arms and the saddle.
3. Leak test: stomp with the tube end closed by a finger: no air from the joints.
4. Fire 20 rockets at 45 deg in an open area, nobody in front; record range; inspect the tube end and joints.

Warnings (keep): never aim at people or animals; foam nose only; adult supervision; 6+.
"""
    open(os.path.join(OUT, "rocket_v1_spec.md"), "w").write(spec); print("rocket_stand + spec written, sheet height", round(H))
if __name__ == "__main__": main()
