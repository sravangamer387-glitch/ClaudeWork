#!/usr/bin/env python3
"""Production BOM, prototype budget and B2B economics for the Prayog kit. Prices are estimates (INR)."""
PROD = [("Mother board (PCB, MCU, sockets, USB)", 250), ("NTC temperature module", 55), ("LDR light module", 45), ("Microphone module", 120),
        ("Hall magnetic module", 70), ("Soil-moisture module", 150), ("Voltage probe module x2", 120), ("IR reflective module", 70),
        ("Conductivity probe module", 50), ("Ultrasonic distance module", 110), ("Photogate module x2", 200), ("Button + LED reaction pad", 40),
        ("Leads, magnets, steel ball, string, resistors, capacitor pack", 200), ("Carry tray / box", 300), ("Printed teacher guide + 20 worksheets", 250),
        ("Packaging", 200), ("Assembly, test, burn-in", 350)]
PROTO = [("Arduino Nano clone", 400), ("Breadboard + jumper wires", 250), ("NTC 10k + LDR + resistors/caps", 120), ("Microphone module", 120), ("Hall sensor 49E + 2 magnets", 90),
         ("Capacitive soil sensor", 120), ("Ultrasonic HC-SR04-type", 100), ("IR reflective TCRT5000 module", 40), ("Slot-type photogate module x2", 120),
         ("Voltage divider resistors, 4.7 mF cap, 47 ohm resistor", 100), ("Steel ball, string, wooden stand parts", 150), ("USB cable", 80), ("Salt, cups, beakers (household)", 100)]
def b2b(price, bom, ship=300, gst=0.18, commission=0.15, warranty=0.05):
    landed = bom * 1.08; net = price / (1 + gst); c = net - landed - net * commission - ship - net * warranty; return c, c / net
bom = sum(v for _, v in PROD); proto = sum(v for _, v in PROTO)
print(f"Production BOM (designed, ~1,000 kits): Rs {bom:,}")
for price in (7999, 5999):
    for mult, label in ((1.0, "as designed"), (1.3, "BOM +30 %")):
        c, m = b2b(price, bom * mult); print(f"  price Rs {price:,}, {label}: contribution Rs {c:,.0f} ({m:.0%})")
c, m = b2b(7999, 3200); print(f"  earlier proposal guess BOM Rs 3,200 at Rs 7,999: contribution Rs {c:,.0f} ({m:.0%})")
print(f"Prototype budget: Rs {proto:,} (cap Rs 3,000) -> {'OK' if proto <= 3000 else 'OVER'}")
assert proto <= 3000
