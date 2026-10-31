#!/usr/bin/env python3
"""Top-down unit economics for the proposed next products (same fee model as the toy files).
Usage: python3 -I economics.py > economics.md.  BOM lines are rough guesses; the +30 % column reflects the lesson from
the toy work that designed costs came out 20-50 % above guesses.  Channel: marketplace unless noted."""
CLOSE, ADS, RET = 30, 0.12, 0.08

def marketplace(price, bom, ship, gst):
    landed = bom * 1.08
    net = price / (1 + gst)
    ref = 0 if price < 1000 else 0.08
    fees = price * ref + CLOSE + ship
    cont = net - landed - fees - net * ADS - RET * landed
    return net, cont, cont / net

def b2b(price, bom, ship, gst, commission=0.15, warranty=0.05):
    landed = bom * 1.08
    net = price / (1 + gst)
    cont = net - landed - net * commission - ship - net * warranty
    return net, cont, cont / net

ROWS = [
 # name, channel, price, bom, ship, gst, note
 ("1 Desi card & board games (printed, no electronics)", "mkt", 599, 120, 60, 0.05, "GST 5 % assumed for non-electric games; verify"),
 ("2 Kalakriti automata kits (laser-cut, cam-driven)", "mkt", 899, 220, 90, 0.05, "non-electric; verify GST and toy-QCO scope"),
 ("3 School STEM lab kit (20 experiments, per kit)", "b2b", 7999, 3200, 300, 0.18, "15 % channel commission, 5 % warranty reserve"),
 ("4 Jal-Rakshak tank controller (alarm + pump control)", "mkt", 1299, 395, 90, 0.18, "mains relay: certification cost is extra"),
 ("5 Kheti-Mitra irrigation controller (sensor + 12 V valve driver)", "mkt", 1799, 520, 90, 0.18, "valve sold separately"),
]
print("| Product | Channel | Price Rs | BOM guess Rs | Contribution Rs | Margin | Margin if BOM +30 % |")
print("|---|---|---|---|---|---|---|")
for n, ch, price, bom, ship, gst, note in ROWS:
    f = marketplace if ch == "mkt" else b2b
    net, c, m = f(price, bom, ship, gst)
    _, c2, m2 = f(price, bom * 1.3, ship, gst)
    print(f"| {n} | {'marketplace' if ch == 'mkt' else 'B2B'} | {price:,} | {bom:,} | {c:,.0f} | {m:.0%} | {m2:.0%} |")
print()
print("Notes: " + "; ".join(f"{r[0].split(' ')[0]}: {r[6]}" for r in ROWS))
