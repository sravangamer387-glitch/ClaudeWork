#!/usr/bin/env python3
"""Prototype budget model: every prototype must cost <= Rs 3,000 (tiers: Rs 1k / 2k / 3k).
Usage: python3 -I prototype_budget.py <out_dir>   -> prototype_budgets.md + prototype_budgets.csv
Prices are typical Indian online/hobby-store prices from my general knowledge ([K], clone boards and generic modules)
unless tagged [S]. They are estimates: check current listings (Robu.in, Robocraze, Amazon.in etc.) before ordering.
[S] anchors from my research: official Arduino Nano ESP32 Rs 1,741-2,249; 3D printing Rs 2-10 per gram (PLA)."""
import csv
import sys
from pathlib import Path

CAP = 3000
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT.mkdir(parents=True, exist_ok=True)

P = {}
def add(code, name, items): P[code] = (name, items)

# ------------------------------------------------------------------ gravity toys (no electronics)
add("G1", "Timber Tower Marble Run (MDF laser-cut prototype)", [
    ("MDF 6 mm sheet 2x2 ft", 250), ("Laser cutting job work (~40 min)", 240), ("Pine strip 20x20, 6 posts", 120),
    ("Glass marbles 25 mm x4 (or wood balls)", 100), ("Sandpaper, wax, PVA glue", 160), ("Brass tube for chime + string", 80), ("Cork sheet", 50)])
add("G2", "Drop Quest v0 (foam-board + MDF puzzle)", [
    ("MDF 3 mm + foam board", 220), ("Laser cutting", 200), ("Glass marbles 14 mm x6", 60), ("Printed challenge cards (A4 colour x4)", 150), ("Glue, tape", 60)])
add("G3", "Galton Board (acrylic front, MDF back)", [
    ("Acrylic 5 mm A3 sheet", 450), ("MDF 6 mm", 200), ("Laser cutting (acrylic + MDF)", 300), ("Stainless rod O4 mm cut to 55 pegs (or steel dowel pins)", 160),
    ("Steel balls O12 mm x30", 200), ("Screws, glue, rubber feet", 120)])
add("G4", "Santulan balance set (bird, roly-poly, tumbler)", [
    ("Rubber-wood blanks", 150), ("Turning by local artisan (3 pieces)", 450), ("Birch ply 3 mm + laser (wings x2)", 180),
    ("Zinc/brass weights + steel slug (lead-free)", 200), ("Water-based paint + brushes", 200), ("Lacquer + screws", 100)])
add("G5", "Ramp Racers (ramp + 4 cars)", [
    ("Plywood 12 mm (ramp + stand)", 450), ("Cutting job work", 200), ("Wood blocks for 4 car bodies", 150), ("Wheels O30 x16 (4 types)", 320),
    ("Steel axle rod 3 mm + brass bushes", 140), ("Steel weights 20/40/60 g", 150), ("Cork, hinge, lock pin", 160)])

# ------------------------------------------------------------------ electronics toys on Arduino Nano clone
BASE_E = [("Arduino Nano clone (CH340, ATmega328P)", 400), ("Prototype board / breadboard", 150), ("Jumper wires + resistor kit", 170)]
add("E1", "Rhymes player (Nano + MP3 module)", BASE_E + [
    ("DFPlayer-Mini-style MP3 module", 180), ("microSD 8 GB (preloaded with rhymes)", 250), ("Speaker 3 W 4 ohm 40 mm", 80),
    ("7 tactile buttons + 2 LEDs", 80), ("3xAA holder + 3 cells", 250), ("Enclosure: laser MDF box", 350)])
add("E2", "Star projector lamp (Nano + MP3 + RGB)", BASE_E + [
    ("DFPlayer-style MP3 module", 180), ("microSD 2 GB with lullabies", 150), ("Speaker 2 W 36 mm", 70), ("3 x 1 W LEDs + heatsinks", 100),
    ("Logic-level MOSFETs IRLZ44N x4", 120), ("N20 gear motor (rotor)", 120), ("Star-projection film + lens", 100), ("3 buttons", 30),
    ("3xAAA holder + cells", 130), ("3D-printed dome 59 g at Rs 5/g [S] + courier", 400)])
add("E3", "Cricket game (Nano + TM1637 display)", BASE_E + [
    ("TM1637 4-digit display module", 120), ("7 LEDs + resistors", 40), ("Piezo buzzer", 30), ("2 buttons", 30),
    ("3xAAA holder + cells", 130), ("Enclosure: laser MDF box", 300)])

# ------------------------------------------------------------------ DJ prototypes
add("D1", "Beat-synced light controller (Nano + mic + 12 V RGB strip)", BASE_E + [
    ("Analog microphone module (MAX9814-class)", 250), ("Logic-level MOSFETs IRLZ44N x3 + gate resistors", 110), ("12 V RGB strip 5050, 2 m", 250),
    ("12 V 2 A adapter", 250), ("Terminal blocks, fuse, heat-shrink", 120)])
add("D2", "DJ MIDI controller (Nano + pots + buttons + encoder)", BASE_E + [
    ("Rotary pots 10k x6", 150), ("Slide pots 60 mm x2 (crossfader, pitch)", 200), ("Tactile/arcade buttons x8", 160), ("Rotary encoder KY-040", 60),
    ("Knobs x8", 100), ("Laser-cut MDF enclosure", 400), ("USB cable", 80)])

SHARED_TOOLS = ("One-time tools for the electronics builds (soldering iron, solder, multimeter, wire cutters)", 1500)

rows = []
for code, (name, items) in P.items():
    total = sum(v for _, v in items)
    tier = 1000 if total <= 1000 else 2000 if total <= 2000 else 3000
    assert total <= CAP, f"{code} {name} costs Rs {total} > cap Rs {CAP}"
    rows.append((code, name, total, tier, items))

lines = ["| Code | Prototype | Cost Rs | Tier | Fits your cap? |", "|---|---|---|---|---|"]
for code, name, total, tier, _ in rows:
    lines.append(f"| {code} | {name} | {total:,} | up to Rs {tier:,} | yes |")
tot = sum(r[2] for r in rows)
lines += ["", f"**All ten prototypes: Rs {tot:,}** (plus one-time tools Rs {SHARED_TOOLS[1]:,} if you have none). Cheapest {min(rows, key=lambda r: r[2])[1]} Rs {min(r[2] for r in rows):,}; dearest {max(rows, key=lambda r: r[2])[1]} Rs {max(r[2] for r in rows):,}."]
lines += ["", "## Line items", ""]
for code, name, total, tier, items in rows:
    lines += [f"### {code} {name} - Rs {total:,}", "", "| Item | Rs |", "|---|---|"] + [f"| {i} | {v:,} |" for i, v in items] + [f"| **Total** | **{total:,}** |", ""]
(OUT / "prototype_budgets.md").write_text("# Prototype budgets (all <= Rs 3,000)\n\n" + "\n".join(lines) + "\n")
with open(OUT / "prototype_budgets.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Code", "Prototype", "Item", "Rs"])
    for code, name, total, tier, items in rows:
        for i, v in items: w.writerow([code, name, i, v])
        w.writerow([code, name, "TOTAL", total])
print("\n".join(lines[:16]))
