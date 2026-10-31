#!/usr/bin/env python3
"""Prayog analysis tools + simulated-experiment validation (standard library only).
Each numeric experiment has: a simulator (true physics + noise), an analysis that recovers the constant, and a tolerance.
Run:  python3 -I prayog_tools.py        -> validates all analyses, writes ../docs/validation.md
Use:  analysis functions take lists of numbers (from the logger CSV)."""
import math, random, sys
from pathlib import Path

def linfit(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x); sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    slope = sxy / sxx; icpt = my - slope * mx
    ss_res = sum((b - (icpt + slope * a)) ** 2 for a, b in zip(x, y)); ss_tot = sum((b - my) ** 2 for b in y)
    return slope, icpt, 1 - ss_res / ss_tot if ss_tot else 1.0

# ---------------- analyses
def newton_cooling_k(t_s, temp_c, ambient_c):  return -linfit(t_s, [math.log(T - ambient_c) for T in temp_c])[0]      # 1/s
def power_law_exponent(x, y):                  return linfit([math.log(a) for a in x], [math.log(b) for b in y])[0]      # log-log slope
def speed_of_sound(dist_m, echo_s):            return 2.0 * linfit(echo_s, dist_m)[0]      # d = c t / 2, so c = 2 x slope of d against t
def g_from_pendulum(length_m, period_s):       return 4 * math.pi ** 2 / linfit(length_m, [T * T for T in period_s])[0]
def g_from_fall(height_m, t_s):                return 2.0 * linfit([t * t for t in t_s], height_m)[0]               # h = g t^2 / 2
def resistance_from_iv(v, i):                  return linfit(i, v)[0]
def rc_time_constant(t_s, v, v_final):         return -1.0 / linfit(t_s, [math.log(abs(v_final - a)) for a in v])[0]
def conductivity_slope(conc, reading):         return linfit(conc, reading)[0:3:2]
def gate_events_period(events):
    """events = [(t_us, level)] from the logger 'G' lines; mean time between successive beam interruptions (level 1)."""
    ts = [t for t, lv in events if lv == 1]
    return (ts[-1] - ts[0]) / 1e6 / (len(ts) - 1)
def mean_sd(x):
    m = sum(x) / len(x); return m, math.sqrt(sum((a - m) ** 2 for a in x) / (len(x) - 1))

# ---------------- simulations (true constants chosen by us) and validation
rng = random.Random(2026)
def noise(sd): return rng.gauss(0, sd)

def v_newton():
    k, Ta = 0.0021, 28.0; t = [i * 30 for i in range(0, 60)]; T = [Ta + (85 - Ta) * math.exp(-k * s) + noise(0.15) for s in t]
    return newton_cooling_k(t, T, Ta), k, 0.05 * k          # 5 % of the true value
def v_inverse_square():
    d = [0.2 + 0.1 * i for i in range(10)]; lux = [800 / x ** 2 * (1 + noise(0.03)) for x in d]
    return power_law_exponent(d, lux), -2.0, 0.08
def v_speed_of_sound():
    c = 343.4; d = [0.3 + 0.2 * i for i in range(10)]; t = [2 * x / c + noise(15e-6) for x in d]
    return speed_of_sound(d, t), c, 0.02 * c
def v_pendulum():
    L = [0.3 + 0.1 * i for i in range(8)]; T = [2 * math.pi * math.sqrt(x / 9.78) * (1 + noise(0.003)) for x in L]
    return g_from_pendulum(L, T), 9.78, 0.2
def v_freefall():
    h = [0.2 + 0.1 * i for i in range(8)]; t = [math.sqrt(2 * x / 9.78) + noise(0.0008) for x in h]
    return g_from_fall(h, t), 9.78, 0.35
def v_gate_pipeline():
    T = 2.006; ev = []
    for k in range(12):
        t0 = int(1e5 + k * T * 1e6 + noise(40)); ev += [(t0, 1), (t0 + 15000, 0)]
    return gate_events_period(ev), T, 0.001
def v_ohm():
    R = 47.0; i = [0.01 * k for k in range(1, 11)]; v = [R * a + noise(0.02) for a in i]
    return resistance_from_iv(v, i), R, 1.5
def v_rc():
    tau = 4.7; t = [0.5 * k for k in range(30)]; v = [5.0 * (1 - math.exp(-s / tau)) + noise(0.01) for s in t]
    return rc_time_constant(t, v, 5.0), tau, 0.2
def v_hall():
    d = [0.01 + 0.005 * i for i in range(8)]; B = [1e-6 / x ** 3 * (1 + noise(0.04)) for x in d]
    return power_law_exponent(d, B), -3.0, 0.2
def v_conductivity():
    conc = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]; r = [20 + 85 * c + noise(3) for c in conc]
    return linfit(conc, r)[0], 85.0, 6.0
def v_reaction():
    x = [max(0.12, 0.21 + noise(0.035)) for _ in range(40)]; m, s = mean_sd(x)
    return m, 0.21, 0.02

VALID = [("Newton cooling constant k (1/s)", v_newton), ("Light intensity exponent (inverse square: -2)", v_inverse_square),
         ("Speed of sound from echoes (m/s)", v_speed_of_sound), ("g from pendulum (m/s2)", v_pendulum), ("g from free fall (m/s2)", v_freefall),
         ("Photogate event stream -> pendulum period (s)", v_gate_pipeline), ("Resistance from V-I slope (ohm)", v_ohm), ("RC time constant (s)", v_rc), ("Magnet field exponent on axis (dipole: -3)", v_hall),
         ("Conductivity vs concentration slope", v_conductivity), ("Human reaction time (s)", v_reaction)]

def main():
    rows, bad = ["| Analysis | True value | Recovered | Tolerance | Result |", "|---|---|---|---|---|"], 0
    for name, f in VALID:
        got, true, tol = f(); ok = abs(got - true) <= tol; bad += (not ok)
        rows.append(f"| {name} | {true:g} | {got:.4g} | ±{tol:.3g} | {'PASS' if ok else 'FAIL'} |")
    # honesty test: the analyses must also fail when the data are wrong (a power law fitted to linear data gives the wrong exponent)
    wrong = power_law_exponent([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    rows.append(f"| Sanity: linear data does not look like inverse square | exponent ≠ -2 | {wrong:.2f} | – | {'PASS' if abs(wrong + 2) > 1 else 'FAIL'} |")
    text = "# Validation of the Prayog analysis tools (simulated experiments with noise)\n\n" + "\n".join(rows) + "\n\nSimulated data use the stated true constants plus sensor-like noise; they validate the *method*, not the hardware.\n"
    Path(__file__).resolve().parent.parent.joinpath("docs", "validation.md").write_text(text)
    print(text); return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
