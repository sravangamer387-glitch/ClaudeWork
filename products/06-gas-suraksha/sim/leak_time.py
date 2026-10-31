"""Well-mixed kitchen leak model: time for LPG concentration to reach 10 % LEL, plus the alarm delay of the firmware.
Assumptions (all unverified): LPG LEL 1.8 % by volume, vapour density 2.0 kg/m3 (propane/butane mix, near 1 atm 25 C),
room 20 m3 (kitchen), air change rates 0.5 / 2 / 5 per hour. Real gas pools low (heavier than air) so floor concentration
at the sensor is HIGHER than the mixed value near a leak and lower far from it: this model is an order-of-magnitude guide only."""
import math
LEL = 0.018; RHO = 2.0; V = 20.0
def t_to(frac_lel, leak_g_per_min, ach):
    target = frac_lel * LEL                       # volume fraction
    q = leak_g_per_min / 1000 / RHO / 60          # m3 gas per second
    lam = ach / 3600.0
    ss = q / (lam * V) if lam > 0 else float("inf")      # steady-state fraction (small-fraction approx)
    if ss <= target: return None
    if lam == 0: return target * V / q
    return -math.log(1 - target / ss) / lam
SENSOR_DELAY = 8    # s confirm (fast); response of an MQ sensor adds roughly 10-30 s (assumption)
rows = ["| leak g/min | ventilation 0.5 ACH | 2 ACH | 5 ACH |", "|---|---|---|---|"]
for leak in (0.2, 1.0, 2.0, 5.0, 20.0):
    cells = []
    for ach in (0.5, 2, 5):
        t = t_to(0.10, leak, ach)
        cells.append("never reaches 10 % LEL" if t is None else f"{(t+SENSOR_DELAY+20)/60:.1f} min")
    rows.append(f"| {leak} | " + " | ".join(cells) + " |")
out = "\n".join(rows)
# reference: how long to reach 25 % LEL, the level where it becomes serious, for the same leaks
print(out)
open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "docs", "leak_time_table.md"), "w").write("# Time until a 10 % LEL alarm (model)\n\n" + out + "\n\nIncludes 8 s confirm + 20 s sensor response (assumption). Well-mixed 20 m3 room; real leaks pool at floor level. Order-of-magnitude only; NOT validated with real gas.\n")
