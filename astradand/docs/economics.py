"""ASTRADAND unit economics (same marketplace fee model as the toy/utility files). Every number is an ESTIMATE; the +30 % column reflects that designed costs came out 20-50 % above guesses elsewhere in this repository."""
CLOSE, ADS, RET = 30, 0.12, 0.08
BOM = [("ATmega328P-AU", 170), ("MPU-6050 IMU (LCSC listing about USD 2.7 at volume; price varies a lot between listings)", 230), ("AP2112K LDO + Schottky + MOSFET/NPN switch + passives (about 30 parts)", 85), ("6 x WS2812B-Mini LEDs", 30), ("Murata piezo 12x12 mm", 60),
       ("Haptic coin motor", 25), ("Button, slide switch, JST connectors", 45), ("PCB 146 x 26 mm 2-layer (about 2,000 pcs)", 38), ("SMT assembly (EMS)", 85), ("3 x AAA in-line holder with leads", 30),
       ("Hilt: injection-moulded halves, tip, pommel, crystal (tooling amortised over 2,000 units about Rs 150 + resin)", 180), ("Screws, springs, label", 8), ("Carton (350 gsm) + insert", 45), ("Spell cards + rules (9 cards)", 25), ("Display stand (6 mm MDF, laser cut)", 70), ("Assembly, programming and test labour", 90)]
def marketplace(price, bom, ship=90, gst=0.18):
    landed = bom * 1.08; net = price / (1 + gst); ref = 0 if price < 1000 else 0.08; fees = price * ref + CLOSE + ship
    cont = net - landed - fees - net * ADS - RET * landed; return net, cont, cont / net
total = sum(v for _, v in BOM); lines = ["# ASTRADAND economics (estimates)", "", "| Item | Rs |", "|---|---|"] + [f"| {k} | {v} |" for k, v in BOM] + [f"| **Total designed BOM (about 2,000 units)** | **{total}** |", "",
         "Prices exclude batteries (sold separately or a pack of 3 AAA included at about Rs 25).", "", "| Price Rs | Net of GST (18 %) | Contribution Rs | Margin | Contribution if BOM +30 % | Margin |", "|---|---|---|---|---|---|"]
for p in (1799, 2299, 2499, 2999, 3499):
    n, c, m = marketplace(p, total); n2, c2, m2 = marketplace(p, total * 1.3); lines.append(f"| {p} | {n:.0f} | {c:.0f} | {m*100:.0f} % | {c2:.0f} | {m2*100:.0f} % |")
lines += ["", "Fixed launch costs (assumptions, not quotes): injection tooling for the hilt about Rs 3-5 lakh (amortised above), lab testing (toy standard, battery, EMC) Rs 1-2 lakh, artwork/illustration Rs 0.5-1 lakh, certification and insurance not included.",
          "Comparison: the Kymera universal remote wand lists at about USD 60-70 outside India (no Indian price found); simple LED 'wands' sell for a few hundred rupees. This product competes on play, not on price.",
          "Reading: at Rs 2,499 the unit is roughly break-even-to-thin once the BOM overruns; Rs 2,999 or a convention/direct-sales channel (no marketplace fees) is the realistic target. Do not launch below Rs 2,499."]
open("economics.md", "w").write("\n".join(lines)); print("\n".join(lines[-16:]))
