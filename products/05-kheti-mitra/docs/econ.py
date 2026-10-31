#!/usr/bin/env python3
"""Designed production BOM (~2,000 units, estimates) and marketplace economics for Kheti-Mitra (controller + 2 sensors, valve sold separately)."""
BOM = [("MCU", 45), ("2-layer PCB", 30), ("2 capacitive soil sensors (coated, with 2 m cable)", 140), ("Rain sensor module", 40), ("MOSFET valve driver + flyback diode + terminals", 25),
       ("12 V adapter (certified)", 110), ("Enclosure IP65 + tooling amortisation, cable glands", 125), ("Packaging + quick-start card (Hindi/Telugu/English)", 45), ("Assembly, test", 60)]
bom = sum(v for _, v in BOM)
def mk(price, b, ship=90):
    landed = b * 1.08; net = price / 1.18; fees = price * (0 if price < 1000 else 0.08) + 30 + ship
    c = net - landed - fees - net * 0.12 - 0.08 * landed; return c, c / net
print(f"Designed BOM: Rs {bom} (earlier top-down guess: Rs 520)")
for price in (1799, 2299, 2799):
    for mult, lab in ((1.0, "as designed"), (1.3, "BOM +30 %")):
        c, m = mk(price, bom * mult); print(f"  price Rs {price}: {lab}: contribution Rs {c:,.0f} ({m:.0%})")
