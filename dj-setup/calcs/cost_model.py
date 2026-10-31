#!/usr/bin/env python3
"""Top-down cost and margin model for candidate DJ-system products (Amazon.in-style marketplace fees, same model as the
toy files). Usage: python3 -I cost_model.py > cost_model.md
EVERY BOM line is a rough planning guess (INR, ~5,000 units) - the purpose is to find which pieces can earn money, not to quote."""
GST, CLOSE, ADS, RET = 0.18, 30, 0.12, 0.08

def margin(price, bom, ship, referral=0.08):
    landed = bom * 1.08
    net = price / (1 + GST)
    fees = price * (0 if price < 1000 else referral) + CLOSE + ship
    cont = net - landed - fees - net * ADS - RET * landed
    return net, landed, cont, cont / net

PRODUCTS = {
 "A  Home party speaker, 100 W peak, 150 Wh, mic input, light ring": dict(price=14999, ship=300, parts=[
    ("Drivers (woofer + tweeter) + passive radiator", 700), ("Class-D amp + DSP + Bluetooth module", 800),
    ("LiFePO4 150 Wh pack + BMS", 2000), ("Cabinet, grille, handle (incl. tooling amortisation)", 1500),
    ("Main PCB, connectors, mic input", 800), ("RGB pixel light ring + driver", 450), ("Charger / adapter (BIS)", 500),
    ("Packaging + manual", 300), ("Assembly + test + burn-in", 450)]),
 "B  DJ controller, 2-deck, USB-C + USB-stick standalone, mic, effects": dict(price=14999, ship=250, parts=[
    ("Audio SoC/MCU board + DSP + USB audio", 1300), ("Jog wheels x2 (touch + motion)", 700), ("Faders, knobs, encoders", 900),
    ("RGB pads x16 + display", 500), ("Case + tooling amortisation", 900), ("PCBs", 400), ("Power / USB-C", 150),
    ("Packaging + manual", 250), ("Assembly + test", 300)]),
 "C  Light kit: 4 battery RGBW pars + sync hub + carry bag": dict(price=12999, ship=350, parts=[
    ("4 x battery RGBW par (LEDs, driver, 2-3 h cell, housing)", 3200), ("Sync hub (MCU, 2.4 GHz radio, DMX out)", 700),
    ("Charger + cables", 300), ("Carry bag + packaging", 450), ("Assembly + test", 350)]),
 "D  Party System bundle: 2 x speaker (300 W) + controller + 4 lights": dict(price=59999, ship=900, parts=[
    ("2 x 300 W speaker, 390 Wh total battery", 9500), ("DJ controller (B)", 5300), ("Light kit (C)", 5000),
    ("Stands, cables, bag", 1200), ("Packaging", 600), ("Assembly + test", 700)]),
}
print("| Product | Price Rs | BOM Rs | Net revenue | Contribution Rs | Margin |")
print("|---|---|---|---|---|---|")
for name, p in PRODUCTS.items():
    bom = sum(v for _, v in p["parts"])
    net, landed, cont, pct = margin(p["price"], bom, p["ship"])
    print(f"| {name} | {p['price']:,} | {bom:,} | {net:,.0f} | {cont:,.0f} | {pct:.0%} |")
print()
print("Price needed for 25% marketplace contribution:")
for name, p in PRODUCTS.items():
    bom = sum(v for _, v in p["parts"]); pr = p["price"]
    while margin(pr, bom, p["ship"])[3] < 0.25 and pr < 200000: pr += 100
    print(f"- {name}: about Rs {pr:,}")
