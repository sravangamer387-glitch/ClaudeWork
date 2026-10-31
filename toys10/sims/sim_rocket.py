"""Paper Rocket Air Launcher: hand-pumped air chamber fires a paper rocket (rolled paper tube, foam nose) from a barrel.
Model: adiabatic expansion of the chamber while the rocket travels the barrel, then ballistic flight with quadratic drag.
ASSUMPTIONS (unverified): rocket 4 g, tube diameter 19 mm, nose Cd 0.75, chamber 0.3 L gauge pressure set by a 1.0 bar relief valve, barrel 0.2 m,
friction/leak losses 35 % of the ideal energy. Toy safety: a design limit of 0.5 J launch kinetic energy is used (the applicable limit in the toy
standard must be looked up and verified: this value is MY placeholder)."""
import math, os
G = 9.81; RHO = 1.2; m = 0.004; d = 0.019; A = math.pi * d * d / 4; Cd = 0.75; gamma = 1.4; Patm = 101325.0
def muzzle(p_gauge_bar, V0=0.3e-3, L=0.2, loss=0.35):
    p0 = Patm + p_gauge_bar * 1e5; V1 = V0 + A * L
    work = (p0 * V0 - p0 * V0 ** gamma / V1 ** (gamma - 1)) / (gamma - 1) - Patm * A * L      # adiabatic work minus work against atmosphere
    return math.sqrt(max(0, 2 * work * (1 - loss) / m)), work * (1 - loss)
def fly(v0, ang_deg, dt=0.001):
    a = math.radians(ang_deg); x = y = 0.0; vx, vy = v0 * math.cos(a), v0 * math.sin(a); t = 0
    while y >= 0 and t < 20:
        v = math.hypot(vx, vy); k = 0.5 * RHO * Cd * A / m * v
        vx -= k * vx * dt; vy -= (G + k * vy) * dt; x += vx * dt; y += vy * dt; t += dt
    return x, t
rows = ["| gauge pressure bar | muzzle speed m/s | launch energy J | range at 45 deg m | range at 30 deg m | flight time at 45 deg s |", "|---|---|---|---|---|---|"]
res = {}
lo, hi = 0.0, 2.0
for _ in range(40):
    mid = (lo + hi) / 2
    if muzzle(mid)[1] <= 0.5: lo = mid
    else: hi = mid
P_SAFE = lo
for p in (0.15, 0.2, round(P_SAFE, 2), 0.5, 1.0):
    v, E = muzzle(p); r45, t45 = fly(v, 45); r30, _ = fly(v, 30); res[p] = (v, E, r45)
    rows.append(f"| {p} | {v:.1f} | {E:.2f} | {r45:.1f} | {r30:.1f} | {t45:.1f} |")
v, E = muzzle(P_SAFE)
best = max(range(5, 86), key=lambda a: fly(v, a)[0])
r_safe = fly(v, best)[0]
txt = "\n".join(rows) + f"\n\nRelief valve setting chosen so launch energy <= 0.5 J (placeholder limit): {P_SAFE:.2f} bar gauge -> muzzle {v:.1f} m/s, {E:.2f} J, best angle {best} deg, range {r_safe:.1f} m. A first draft with a 1.0 bar valve gave 2.8 J, 5x over the placeholder limit, so the design uses a ~{P_SAFE:.2f} bar relief valve (a calibrated spring valve or a bleed hole) and the 0.5 bar+ rows are for reference only. Range is an estimate (friction/leak guesses): measure with a tape; never aim at people or animals; foam nose; adult supervision. The real limit comes from the toy standard and must be looked up."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_rocket.md"), "w").write(txt + "\n"); print(txt)
