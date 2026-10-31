#!/usr/bin/env python3
"""Designed production BOM (~2,000 units, estimates) and marketplace economics for Jal-Rakshak (mains-switching version)."""
BOM = [("MCU (Cortex-M0+ / ATmega class)", 45), ("2-layer PCB (mains + low-voltage zones, slots)", 40), ("Relay 16 A, 12 V coil (pump contactor drive)", 60),
       ("Isolated 230 V to 12 V supply module (certified)", 130), ("Low-voltage probe isolation + AC excitation parts", 35), ("3 probe sets, 15 m cable", 80),
       ("Enclosure IP54 + tooling amortisation", 90), ("Terminals, fuse, MOV surge protector", 50), ("LED, buzzer, button, passives", 25),
       ("Packaging + manual (Hindi/Telugu/English)", 45), ("Assembly, test, burn-in", 60)]
bom = sum(v for _, v in BOM)
def mk(price, b, ship=90):
    landed = b * 1.08; net = price / 1.18; fees = price * (0 if price < 1000 else 0.08) + 30 + ship
    c = net - landed - fees - net * 0.12 - 0.08 * landed; return c, c / net
print(f"Designed BOM: Rs {bom}  (earlier top-down guess: Rs 395)")
for price in (1299, 1799, 2199):
    for mult, lab in ((1.0, "as designed"), (1.3, "BOM +30 %")):
        c, m = mk(price, bom * mult); print(f"  price Rs {price}: {lab}: contribution Rs {c:,.0f} ({m:.0%})")
