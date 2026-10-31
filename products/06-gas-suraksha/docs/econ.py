#!/usr/bin/env python3
"""Designed production BOM (~2,000 units, estimates) and marketplace economics for Gas-Suraksha. Same fee model as the other products."""
BOM = [("MCU (ATmega-class)", 45), ("Catalytic/MOS LPG sensor, bare element + calibration-friendly socket", 110), ("2-layer PCB", 35),
       ("5 V USB adapter (BIS-registered, bought-in) + cable", 90), ("Backup 3 x AA holder + switch circuit", 30), ("Piezo buzzer 85 dB", 20),
       ("LEDs, button, passives, regulator", 25), ("Enclosure (injection amortised) + strap", 55), ("Packaging + manual (Hindi/Telugu/English)", 35),
       ("Assembly, 2-point gas calibration, burn-in", 70)]
bom = sum(v for _, v in BOM)
def mk(price, b, ship=90):
    landed = b * 1.08; net = price / 1.18; fees = price * (0 if price < 1000 else 0.08) + 30 + ship
    c = net - landed - fees - net * 0.12 - 0.08 * landed; return c, c / net
print(f"Designed BOM: Rs {bom}")
for price in (799, 1299, 1799, 2299):
    for mult, lab in ((1.0, "as designed"), (1.3, "BOM +30 %")):
        c, m = mk(price, bom * mult); print(f"  price Rs {price}: {lab}: contribution Rs {c:,.0f} ({m:.0%})")
print("Excludes: certification/testing (lab quote needed), product liability insurance, returns from false alarms, warranty.")
