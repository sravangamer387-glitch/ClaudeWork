"""Rubber-band Racer: twisted rubber band drives the rear axle. Energy model E = k * turns^2 (torsional), efficiency eta, rolling resistance Crr.
ASSUMPTIONS (unverified, must be measured with a spring scale / test run): k = 0.00015 J/turn^2 per band, eta 0.45 into the wheels,
Crr 0.04 (hard wheel on tiles), car mass 120 g, 2 bands. Distance = eta*E/(Crr*m*g)."""
import os
g = 9.81
def dist(turns, m=0.12, k=0.00015, bands=2, eta=0.45, crr=0.04): return eta * bands * k * turns ** 2 / (crr * m * g)
rows = ["| winding turns | stored energy J | distance m (mass 120 g) | distance with 60 g driver figurine | distance if Crr 0.08 (carpet) |", "|---|---|---|---|---|"]
for t in (20, 40, 60, 80, 100):
    rows.append(f"| {t} | {2*0.00015*t*t:.2f} | {dist(t):.1f} | {dist(t, m=0.18):.1f} | {dist(t, crr=0.08):.1f} |")
txt = "\n".join(rows) + "\n\nGearing note: a 1:2 axle step-up halves the turns needed but not the energy. A first version of this model used k = 0.0009 and predicted 60 m, which was physically absurd (a rubber band stores well under 1 J); the constant was cut to 0.00015 and the target is 5-12 m on tiles at 60 turns. If the first prototype gives under 3 m raise bands to 3 or reduce wheel friction. Everything here is an estimate from assumed constants, not measured."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_racer.md"), "w").write(txt + "\n"); print(txt)
