#!/usr/bin/env python3
"""Physics checks for the five gravity-toy designs (standard library only).
Usage: python3 -I verify_designs.py > verification.md
These are idealised models (point masses, rolling resistance coefficients, ideal random walk).
They catch design errors early; they do NOT replace testing a physical prototype."""
import math
import random

G = 9.81
out = []
def p(s=""): out.append(s)
fails = []
def check(name, ok, detail=""):
    p(f"- {'PASS' if ok else 'FAIL'}: {name}" + (f" ({detail})" if detail else ""))
    if not ok: fails.append(name)

# ---------------------------------------------------------------- 1. Galton board (toy 3)
p("## 1. Galton board (Toy 3)")
random.seed(11)
rows, balls = 10, 5000
bins = [0] * (rows + 1)
for _ in range(balls):
    bins[sum(random.random() < 0.5 for _ in range(rows))] += 1
theory = [math.comb(rows, k) / 2 ** rows for k in range(rows + 1)]
chi2 = sum((bins[k] - balls * theory[k]) ** 2 / (balls * theory[k]) for k in range(rows + 1))
p(f"Ideal random walk, {balls} balls, {rows} rows. Bin fractions: " + ", ".join(f"{b / balls:.3f}" for b in bins))
p(f"Theory: " + ", ".join(f"{t:.3f}" for t in theory))
check("simulation matches binomial (chi-square < 18.3 for 10 dof at 5 %)", chi2 < 18.3, f"chi2={chi2:.1f}")
pitch, peg, ball = 24.0, 4.0, 12.0
gap = pitch - peg
check("peg gap >= 1.5 x ball diameter (jam guard)", gap >= 1.5 * ball, f"gap {gap:.0f} mm vs {1.5 * ball:.0f} mm")
check("bin width 24 mm holds a 12 mm ball with 3 mm walls", pitch - 3 >= ball + 4, f"clear {pitch - 3:.0f} mm")
sigma = math.sqrt(rows * 0.25)
p(f"Expected spread: standard deviation {sigma:.2f} bins; centre bin {theory[5]:.1%}; edge bins {theory[0]:.2%} (rarely visited with 30 balls: expect a 30-ball run to look ragged, 300+ balls to look smooth).")
p()

# ---------------------------------------------------------------- 2. Timber tower marble run (toy 1)
p("## 2. Timber tower marble run (Toy 1)")
ball_d, groove_w, ramp_len = 25.0, 28.0, 100.0
check("groove clears the ball by >= 1 mm each side", (groove_w - ball_d) / 2 >= 1.0, f"{(groove_w - ball_d) / 2:.1f} mm")
crr = 0.015                                  # rolling resistance, wood ball on lacquered/waxed wood (assumption)
def accel(theta_deg, crr_):                  # solid sphere rolling: a = (5/7) g (sin t - crr cos t) (approx.)
    t = math.radians(theta_deg)
    return (5.0 / 7.0) * G * (math.sin(t) - crr_ * math.cos(t))
p("| Slope | Acceleration m/s2 | Time for one 100 mm ramp from rest s | Exit speed m/s |")
p("|---|---|---|---|")
for th in (3, 5, 8, 10, 12, 15):
    a = accel(th, crr)
    if a <= 0:
        p(f"| {th} deg | {a:.2f} | will not roll | - |"); continue
    t = math.sqrt(2 * ramp_len / 1000 / a); v = a * t
    p(f"| {th} deg | {a:.2f} | {t:.2f} | {v:.2f} |")
check("8-12 degree slopes roll reliably (a > 0.5 m/s2 even with crr 0.03)", all(accel(th, 0.03) > 0.5 for th in (8, 10, 12)))
# full starter-set route: 6 ramps (100 mm), 2 curves (~80 mm), 2 spirals (1 turn, 314 mm centreline), funnel (~50 mm)
STARTER = [100] * 6 + [80] * 2 + [314] * 2 + [50]
def route_time(slope, delays_s=0.0, loss=0.2):
    v, total, a = 0.0, 0.0, accel(slope, crr)
    for d_mm in STARTER:
        d = d_mm / 1000
        t = (-v + math.sqrt(v * v + 2 * a * d)) / a
        total += t; v = (v + a * t) * (1 - loss)     # 20 % of the speed is lost at every junction/curve
    return total + delays_s
p("Full starter-set route (6 ramps, 2 curves, 2 spirals, funnel), 20 % speed lost at each junction, +1.2 s for see-saw / funnel / bell delays:")
p()
p("| Ramp slope | Track only s | With delays s |")
p("|---|---|---|")
for sl in (4, 5, 6, 8, 10, 12):
    p(f"| {sl} deg | {route_time(sl):.1f} | {route_time(sl, 1.2):.1f} |")
check("design slope 6 deg gives a watchable run of 3.5-6 s with delays", 3.5 <= route_time(6, 1.2) <= 6.0, f"{route_time(6, 1.2):.1f} s")
check("design slope 10 deg would be too quick (< 3.5 s) - the original 8-12 degree range was wrong", route_time(10, 1.2) < 3.5, f"{route_time(10, 1.2):.1f} s")
p("**Design change:** ramps at 6-8 degrees (not 8-12). At 10 degrees the whole starter route lasts only about 3.5 s.")
p()

# ---------------------------------------------------------------- 3. Ramp racers (toy 5)
p("## 3. Ramp racers (Toy 5)")
L = 1.2
p("Run time over 1.2 m (s). Sliding/rolling resistance coefficients are assumptions: hard wood 0.02, rubber tyre 0.04, felt 0.08. '-' = does not move.")
p()
p("| Angle | Rise mm | hard wood | rubber | felt |")
p("|---|---|---|---|---|")
times = {}
for th in (5, 10, 15, 20, 25):
    row = []
    for name, c in (("wood", 0.02), ("rubber", 0.04), ("felt", 0.08)):
        t = math.radians(th); a = G * (math.sin(t) - c * math.cos(t))
        if a <= 0.05: row.append("-"); times[(th, name)] = None
        else: tt = math.sqrt(2 * L / a); row.append(f"{tt:.2f}"); times[(th, name)] = tt
    p(f"| {th} deg | {L * 1000 * math.sin(math.radians(th)):.0f} | " + " | ".join(row) + " |")
check("felt wheels are impractically slow at 5 degrees (> 3 s): use >= 10 degrees for felt", times[(5, 'felt')] is None or times[(5, 'felt')] > 3.0, f"{times[(5, 'felt')]:.1f} s")
check("every wheel type moves at 10 degrees and the run is measurable (0.8-3 s)", all(times[(10, w)] and 0.8 <= times[(10, w)] <= 3.0 for w in ('wood', 'rubber', 'felt')),
      ", ".join(f"{w} {times[(10, w)]:.2f}s" for w in ('wood', 'rubber', 'felt')))
check("at 25 degrees fastest run is >= 0.5 s (phone stopwatch resolution)", times[(25, 'wood')] >= 0.5, f"{times[(25, 'wood')]:.2f} s")
p("Mass independence: acceleration has no mass term when resistance is proportional to weight, so 20/40/60 g inserts should NOT change the time (that is the lesson). Real cars will differ slightly because axle friction is not purely proportional to load: expect a few percent.")
p()

# ---------------------------------------------------------------- 4. Santulan balancing bird (toy 4)
p("## 4. Balancing bird (Toy 4): centre-of-gravity check")
# coordinates: origin at the beak tip (pivot), x towards the tail (mm), y DOWN (mm). Masses in grams.
body_m, body_x, body_y = 37.0, 80.0, 0.0       # turned rubber wood, 160 mm long, centre at pivot height
wing_m, wing_x, wing_y = 13.0, 60.0, 20.0      # 3 mm birch ply, both wings, slight droop
w_m = 40.0                                     # two 20 g lead-free weights
y_w = 90.0                                     # weights hang 90 mm below the beak line (from the design doc)
# horizontal balance: sum(m x) = 0  => weight position x_w
x_w = -(body_m * body_x + wing_m * wing_x) / w_m
m_tot = body_m + wing_m + w_m
y_cog = (body_m * body_y + wing_m * wing_y + w_m * y_w) / m_tot
x_cog = (body_m * body_x + wing_m * wing_x + w_m * x_w) / m_tot
p(f"Masses: body {body_m:.0f} g, wings {wing_m:.0f} g, weights {w_m:.0f} g (total {m_tot:.0f} g). Weights hang {y_w:.0f} mm below the beak line.")
p(f"**Result: the weights must sit {abs(x_w):.0f} mm FORWARD of the beak tip** (wings swept forward) for the centre of gravity to be under the pivot (x_cog = {x_cog:.1f} mm). The original design text did not say this; without it the bird tips backward.")
p(f"Centre of gravity {y_cog:.0f} mm below the beak tip (target >= 25 mm).")
check("CoG at least 25 mm below pivot", y_cog >= 25.0, f"{y_cog:.0f} mm")
check("horizontal CoG within 1 mm of the pivot", abs(x_cog) <= 1.0)
# small-oscillation period about the pivot: T = 2 pi sqrt(I / (m g y))
pts = [(body_m, body_x, body_y), (wing_m, wing_x, wing_y), (w_m, x_w, y_w)]
I = sum(m * (x * x + y * y) for m, x, y in pts) / 1000 * 1e-6      # g mm^2 -> kg m^2
T = 2 * math.pi * math.sqrt(I / (m_tot / 1000 * G * y_cog / 1000))
p(f"Rocking period about {T:.2f} s after a nudge (point-mass estimate).")
check("rocking period 0.6-2 s (lively but calm)", 0.6 <= T <= 2.0, f"{T:.2f} s")
# tolerance: how far can the real weight position be off before the bird tips? Restoring if |x_cog| small relative to y_cog.
tilt = math.degrees(math.atan2(abs((body_m * body_x + wing_m * wing_x + w_m * (x_w + 5)) / m_tot), y_cog))
p(f"If the weights are placed 5 mm further back than designed, the bird rests tilted about {tilt:.0f} degrees. Use adjustable weight screws so each bird can be trimmed.")
p()
p("### Roly-poly (self-righting)")
R = 35.0
slug_m, slug_h = 60.0, 8.0          # steel slug, centre 8 mm above floor contact
shell_m, shell_h = 30.0, 55.0
h = (slug_m * slug_h + shell_m * shell_h) / (slug_m + shell_m)
check("CoG height below the radius of the base (self-righting)", h < R, f"h={h:.1f} mm, R={R:.0f} mm")
p(f"Restoring lever arm at 90 degree tilt = (R - h) = {R - h:.1f} mm. Design target said 18 mm; with these masses the CoG is {h:.1f} mm: acceptable, but a heavier/lower slug gives a livelier return.")
p()

# ---------------------------------------------------------------- summary
p("## Summary")
p(f"{'ALL CHECKS PASSED' if not fails else 'FAILED: ' + ', '.join(fails)}")
print("# Design verification (physics models)\n\nGenerated by `sim/verify_designs.py`. Idealised models only.\n")
print("\n".join(out))
raise SystemExit(1 if fails else 0)
