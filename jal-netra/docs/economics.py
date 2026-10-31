"""Designed BOM estimate and marketplace economics for Jal-Netra (estimates; same fee model as the other products)."""
BOM = [("STM32G431CBT6 MCU", 250), ("2 x OPA356 amplifiers", 580), ("2 x TS5A3159 analog switches", 180), ("BAV99, MMBT3904, regulator, crystal, ferrite, misc ICs", 120), ("USB-C connector, PTC, TVS", 40), ("passives (about 55 parts)", 90), ("PCB 2-layer 86 x 66 mm (4-layer in production: +60)", 150), ("PCB assembly", 180),
       ("2 x 10 mm 1 MHz PZT discs, potted (custom: uncertain sourcing)", 300), ("spool body (injection-moulded PPSU or brass-insert PA, amortised tooling)", 280), ("2 x G1/2 brass fittings + O-rings", 160), ("enclosure + OLED module", 230), ("cable, potting epoxy, hardware", 100), ("packaging + manual", 60), ("calibration on a flow rig + test (about 15 min/unit)", 250)]
bom = sum(v for _, v in BOM)
def mk(price, b, gst=0.18, ship=120):
    landed = b * 1.08; net = price / (1 + gst); fees = price * (0 if price < 1000 else 0.08) + 30 + ship
    c = net - landed - fees - net * 0.12 - 0.08 * landed; return c, c / net
if __name__ == "__main__":
    print(f"Designed BOM Rs {bom}")
    for price in (4499, 5499, 6999):
        for mult, lab in ((1.0, "as designed"), (1.3, "BOM +30 %")):
            c, m = mk(price, bom * mult); print(f"  price Rs {price}: {lab}: contribution Rs {c:,.0f} ({m:.0%})")
    print("Not included: certification, fixed development (about Rs 8-15 lakh incl. rig, tooling, tests), warranty, returns from mis-installation.")
