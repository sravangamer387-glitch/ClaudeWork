#!/usr/bin/env python3
"""TRISHNA engineering drawings (matplotlib): plumbing schematic, wall elevation / installation layout, cable harness, sensor-block
dimension drawing. Writes PNG + SVG to ../docs/drawings/.  usage: python3 drawings.py"""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "drawings"); os.makedirs(D, exist_ok=True)
FWD, REV, WATER, ELEC = "#1f6fb4", "#c0392b", "#2e8b57", "#555555"

def save(fig, name):
    for ext in ("png", "svg"): fig.savefig(os.path.join(D, f"{name}.{ext}"), dpi=130, bbox_inches="tight")
    plt.close(fig)

def blk(ax, x, y, w, h, title, sub="", fc="#f4f6f8", ec="#333"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2 + (0.18 if sub else 0), title, ha="center", va="center", fontsize=9, weight="bold")
    if sub: ax.text(x + w / 2, y + h / 2 - 0.25, sub, ha="center", va="center", fontsize=7, color="#333")

def pipe(ax, pts, color, lw=2.6, arrow=True, label=None, lpos=0.5, ls="-", lxy=None):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", ls=ls)
    if arrow:
        i = max(0, int(len(pts) * lpos) - 1); (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        ax.add_patch(FancyArrowPatch((x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2), arrowstyle="-|>", mutation_scale=14, color=color, lw=0))
    if label:
        (x0, y0), (x1, y1) = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
        lx, ly = lxy if lxy else ((x0 + x1) / 2 + 0.08, (y0 + y1) / 2 + 0.12)
        ax.text(lx, ly, label, fontsize=7, color=color)

# ------------------------------------------------------------------ 1. plumbing schematic
def plumbing():
    fig, ax = plt.subplots(figsize=(13, 9.4)); ax.set_xlim(0, 13); ax.set_ylim(0, 9.4); ax.axis("off")
    ax.set_title("TRISHNA plumbing schematic (P&ID-style). Blue: SAMPLING (pump forward). Red: PURGE / backwash (pump reverse + valve open).", fontsize=10)
    blk(ax, 9.6, 6.3, 2.6, 1.3, "RESERVOIR", "1.5-2 L, tap water, open top\n(air gap: no link to mains)", fc="#e8f6ee")
    blk(ax, 0.4, 0.5, 2.6, 1.6, "URINAL SUMP INSERT", "30 mm cup, 11 mL to overflow\nTi stream-probe pins", fc="#fff4e0")
    blk(ax, 3.9, 0.4, 2.0, 0.7, "URINAL DRAIN", "below the trap inlet", fc="#eee")
    ax.add_patch(Rectangle((3.4, 2.6), 9.2, 3.3, fill=False, ls="--", lw=1.2, ec="#777")); ax.text(3.5, 5.7, "CHAMBER B (wet box, below chamber A)", fontsize=8, color="#555")
    blk(ax, 3.8, 3.4, 1.7, 1.2, "PUMP", "12 V peristaltic\nDRV8871 H-bridge", fc="#e9f0fb")
    blk(ax, 6.4, 3.0, 1.4, 2.0, "SENSOR\nBLOCK", "2.0 mL bore\nEC | T | optics", fc="#efe9fb")
    blk(ax, 9.3, 4.4, 1.3, 0.8, "SOLENOID", "12 V NC direct-acting", fc="#e8f6ee")
    ax.add_patch(Circle((8.7, 4.7), 0.16, fc="white", ec="#333", lw=1.4)); ax.text(8.7, 4.95, "TEE", ha="center", fontsize=7)
    ax.add_patch(Polygon([[8.55, 3.55], [8.85, 3.55], [8.7, 3.3]], fc="#333")); ax.text(8.95, 3.4, "CHECK VALVE\n(duckbill, flow down only)", fontsize=7)
    ax.add_patch(Circle((7.1, 2.85), 0.12, fc="#999")); ax.text(7.3, 2.78, "leak well + M3 probe pins -> P4 drain", fontsize=7)
    # sampling path (forward)
    pipe(ax, [(2.7, 1.3), (3.1, 1.3), (3.1, 3.8), (3.8, 3.8)], FWD, label="T1 3x5 silicone\nP1 gland", lxy=(3.18, 2.75))
    pipe(ax, [(5.5, 3.8), (6.0, 3.8), (6.0, 3.2), (6.4, 3.2)], FWD, label="T2 -> M5 inlet\n(block bottom)", lxy=(5.55, 2.72))
    pipe(ax, [(7.1, 5.0), (7.1, 5.4), (8.7, 5.4), (8.7, 4.86)], FWD, label="T3 M5 outlet (top)")
    pipe(ax, [(8.7, 4.54), (8.7, 3.6)], FWD, arrow=True)
    pipe(ax, [(8.7, 3.3), (8.7, 2.3), (4.9, 2.3), (4.9, 1.1)], FWD, label="T4 waste, P2 gland", lpos=0.6)
    # fresh water / purge path (reverse)
    pipe(ax, [(10.9, 6.3), (10.9, 5.6), (9.95, 5.6), (9.95, 5.2)], WATER, label="T5 4x6, P3 gland (gravity head 0.3-0.5 m)")
    pipe(ax, [(9.3, 4.8), (8.86, 4.7)], REV)
    pipe(ax, [(8.6, 4.86), (8.6, 5.3), (7.0, 5.3), (7.0, 5.0)], REV, lw=1.6, arrow=True, ls="--")
    pipe(ax, [(6.4, 3.4), (5.9, 3.4), (5.9, 3.6), (5.5, 3.6)], REV, lw=1.6, ls="--")
    pipe(ax, [(3.8, 3.6), (2.95, 3.6), (2.95, 1.6), (2.7, 1.6)], REV, lw=1.6, ls="--", label="backwash returns to the sump\n-> overflow -> drain", lpos=0.7, lxy=(1.2, 2.55))
    pipe(ax, [(1.7, 0.5), (1.7, 0.25), (3.9, 0.25), (3.9, 0.6)], "#999", lw=1.6, label="sump overflow", lpos=0.5)
    pipe(ax, [(7.1, 2.7), (7.1, 2.1), (5.6, 2.1), (5.6, 1.1)], "#999", lw=1.2, arrow=True, label="P4", lpos=0.5)
    notes = ["SEQUENCE: stream detected -> 2 s delay -> pump FORWARD 6 mL (3 chamber volumes, 6 s at 1 mL/s) -> pump stops -> settle + measure (2-9 s)",
             "-> PURGE x2: valve OPEN + pump REVERSE 8 mL, 0.5 s pause -> chamber left full of rinse water (blank for the next event) -> 30 s lockout.",
             "The check valve stops the reversed pump from pulling waste back; the reservoir is open to air above its outlet: no cross-connection to drinking water.",
             "Tubing: 3 mm ID / 5 mm OD food-grade silicone (pump size) stretched onto 4 mm aquarium barbs; 4/6 mm silicone for the reservoir line. Keep T2+T3 under 15 cm each."]
    for i, n in enumerate(notes): ax.text(0.3, 9.05 - i * 0.3, n, fontsize=7.6)
    save(fig, "plumbing_schematic")

# ------------------------------------------------------------------ 2. wall elevation / installation
def elevation():
    fig, ax = plt.subplots(figsize=(9, 10)); ax.set_xlim(-50, 900); ax.set_ylim(-50, 1650); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Wall elevation (front view, mm). Chamber A above chamber B; reservoir highest; all ports and glands face DOWN.", fontsize=10)
    ax.plot([-50, 900], [0, 0], "k-", lw=2); ax.text(0, -40, "floor", fontsize=8)
    ax.add_patch(Rectangle((60, 380), 360, 420, fc="#f2f2f2", ec="#333")); ax.text(240, 600, "URINAL\n(bowl)", ha="center", fontsize=9)
    ax.add_patch(Rectangle((210, 380), 60, 40, fc="#fff4e0", ec="#333")); ax.text(240, 345, "sump insert on the drain strainer", ha="center", fontsize=7)
    bx = 560
    ax.add_patch(Rectangle((bx, 560), 175, 155, fc="#efe9fb", ec="#333", lw=1.3)); ax.text(bx + 87, 637, "CHAMBER B\n175 x 155 x 78\n(fluidics)", ha="center", fontsize=8)
    ax.add_patch(Rectangle((bx + 35, 755), 105, 141, fc="#e9f0fb", ec="#333", lw=1.3)); ax.text(bx + 87, 825, "CHAMBER A\n105 x 141 x 39\n(electronics)", ha="center", fontsize=8)
    ax.add_patch(Rectangle((bx + 20, 1150), 140, 260, fc="#e8f6ee", ec="#333")); ax.text(bx + 90, 1280, "RESERVOIR\n1.5-2 L\nopen top", ha="center", fontsize=8)
    ax.annotate("", (bx + 87, 715), (bx + 87, 755), arrowprops=dict(arrowstyle="<->")); ax.text(bx + 150, 730, "40 mm gap (drip break)", fontsize=7)
    ax.annotate("", (bx + 760 - bx, 560), (bx + 760 - bx, 0), arrowprops=dict(arrowstyle="<->")); ax.text(770, 280, "B bottom 560 mm\nabove floor\n(>= 150 mm above\nthe sump)", fontsize=7)
    ax.annotate("", (bx - 30, 1150), (bx - 30, 715), arrowprops=dict(arrowstyle="<->")); ax.text(bx - 25, 930, "reservoir outlet\n>= 300 mm above\nchamber B", fontsize=7, ha="left")
    ax.plot([240, 240, 500, 500, bx + 40, bx + 40], [400, 470, 470, 520, 520, 560], color=FWD, lw=2); ax.text(330, 480, "T1 sample (sump -> P1)", fontsize=7, color=FWD)
    ax.plot([bx + 62, bx + 62, 300, 300], [560, 500, 500, 420], color="#999", lw=2); ax.text(310, 505, "T4 waste (P2) -> into the bowl at the drain", fontsize=7, color="#666", va="bottom")
    ax.plot([bx + 140, bx + 140, bx + 205, bx + 205, bx + 128, bx + 128], [1150, 1100, 1100, 530, 530, 560], color=WATER, lw=2); ax.text(bx + 210, 1000, "T5 fresh water\n(into P3 from below)", fontsize=7, color=WATER)
    ax.add_patch(Rectangle((40, 1120), 180, 110, fc="#fafafa", ec="#333")); ax.text(130, 1175, "12 V 2 A adapter\n(socket >= 1.2 m high,\nRCD-protected circuit)", ha="center", va="center", fontsize=7)
    ax.add_patch(Rectangle((300, 950), 50, 30, fc="#ddd", ec="#333")); ax.text(325, 990, "VL53L1X ToF\n1.0-1.2 m high,\naimed at the user zone", ha="center", fontsize=7)
    save(fig, "wall_elevation")

# ------------------------------------------------------------------ 3. cable harness
def harness():
    fig, ax = plt.subplots(figsize=(13, 6.8)); ax.set_xlim(0, 13); ax.set_ylim(0, 6.8); ax.axis("off")
    ax.set_title("Cable harness: chamber A (controller PCB) <-> chamber B and field devices. Glands: A bottom wall G1-G3, A left wall G4-G7; B top wall G1-G4.", fontsize=10)
    blk(ax, 0.3, 0.4, 3.4, 5.8, "CHAMBER A - PCB", "", fc="#e9f0fb")
    rows = [("J6 PUMP (2)", "H1 4-core 0.5 mm2 (G1)", "pump: red = PUMP_O1, black = PUMP_O2"), ("J7 VALVE (2)", "H1 (same cable)", "valve coil: VM, VALVE_D (no polarity)"),
            ("J8 LEDS (4)", "H2 8-core 0.22 mm2 (G2)", "LEDB_A/K -> 450 nm LED, LEDI_A/K -> 850 nm LED"), ("J10 EC (2)", "H2 (same cable)", "E1, E2 -> titanium pins (crimp ferrules)"),
            ("J12 LEAK (2)", "H2 (same cable)", "LEAK_P, GND -> 2 x M3 SS screws in B's well"), ("J9 PD (3)", "H3 2-core + shield (G3)", "PD_TX, PD_SC cathodes; anodes GND; shield to GND at PCB only"),
            ("J13 TEMP (3)", "DS18B20 own cable (G4)", "red 3V3, yellow DATA, black GND"), ("J11 SUMP (2)", "2-core 0.22 mm2 (G5), 3 m", "Ti pins in the sump cup"),
            ("J14 ToF (4)", "4-core 0.22 mm2 (G6), up to 2 m", "VL53L1X breakout: VIN 3V3, SDA, SCL, GND"), ("J15 UART (3)", "USB-serial lead (G7)", "GND, TX(out) -> adapter RX, RX(in) <- adapter TX")]
    for i, (j, cab, dev) in enumerate(rows):
        y = 5.75 - i * 0.55
        ax.text(0.45, y, j, fontsize=8, family="monospace"); ax.plot([2.4, 5.3], [y + 0.07, y + 0.07], color=ELEC, lw=1.6)
        ax.text(5.4, y, cab, fontsize=8, color="#1a4d80"); ax.plot([8.1, 8.5], [y + 0.07, y + 0.07], color=ELEC, lw=1.6); ax.text(8.6, y, dev, fontsize=8)
    ax.text(0.4, 0.15, "Wire colours are a suggestion; record yours in the build log. Strip 5 mm, crimp JST PH SPH-002T-P0.5S contacts (AWG 24-30); 0.5 mm2 pump wires: AWG 20 in a ferrule to an inline crimp, then AWG 24 to the JST.", fontsize=7.4)
    save(fig, "cable_harness")

# ------------------------------------------------------------------ 4. sensor block dimension drawing
def block_drawing():
    fig, axs = plt.subplots(1, 3, figsize=(14, 5.6))
    titles = ["FRONT (+X face): LED ports, tilted 22.6 deg toward the PD", "SIDE (+Y face): scatter PD, DS18B20, Ti electrodes", "TOP: outlet M5, 4 x M3 mounting holes"]
    for ax, t in zip(axs, titles):
        ax.set_aspect("equal"); ax.set_title(t, fontsize=9); ax.set_xlim(-26, 26); ax.set_ylim(-6, 46); ax.axis("off")
    a = axs[0]; a.add_patch(Rectangle((-18, 0), 36, 38, fill=False, lw=1.5))
    for z, lab in ((13 - 4.97, "blue 450 nm, exit centre z 8.0 (port axis passes z 13.0 at the bore wall)"), (23 + 4.97, "IR 850 nm, exit centre z 28.0 (axis z 23.0 at the bore wall)")):
        a.add_patch(Circle((0, z), 3.6, fill=False, lw=1)); a.add_patch(Circle((0, z), 2.55, fill=False, lw=1, ls="--"))
    a.text(-25, -4.5, "Ports: 5.1 mm through, 7.2 mm counterbore for O-ring 5 x 1 + LED flange. Bore (hidden): 12.0 dia, z 10-27, 2 mm cones, wetted 2.02 mL.", fontsize=6.5)
    a.annotate("", (-18, 40), (18, 40), arrowprops=dict(arrowstyle="<->")); a.text(0, 41, "36", ha="center", fontsize=8)
    a.annotate("", (21, 0), (21, 38), arrowprops=dict(arrowstyle="<->")); a.text(22, 19, "38", fontsize=8)
    b = axs[1]; b.add_patch(Rectangle((-18, 0), 36, 38, fill=False, lw=1.5))
    b.add_patch(Circle((0, 20.5), 3.6, fill=False)); b.text(4.2, 20.2, "scatter PD z 20.5", fontsize=7)
    b.add_patch(Circle((0, 11.5), 4.6, fill=False)); b.add_patch(Circle((0, 11.5), 3.1, fill=False, ls="--")); b.text(5.2, 11.2, "DS18B20 z 11.5\n(6.2 / 9.2 cbore,\nO-ring 6 x 1.5)", fontsize=7)
    for x in (-3.5, 3.5): b.add_patch(Circle((x, 25.5), 0.5, fc="k"))
    b.text(-17, 28, "Ti electrodes 1.0 mm\nx = +-3.5, z 25.5,\nprotrude 4 mm into bore", fontsize=7)
    c = axs[2]; c.set_ylim(-26, 26); c.add_patch(Rectangle((-18, -18), 36, 36, fill=False, lw=1.5)); c.add_patch(Circle((0, 0), 2.1, fill=False)); c.text(2.6, 0.5, "M5 x 0.8 outlet\n(4.2 drill, tap 6 deep)", fontsize=7)
    for x in (-14, 14):
        for y in (-14, 14): c.add_patch(Circle((x, y), 1.7, fill=False))
    c.text(-17, -23.5, "4 x 3.4 mm through on a 28 x 28 mm square (M3 x 45 + nuts to the shelf). Bottom: M5 inlet, same as the top.", fontsize=7)
    save(fig, "sensor_block_drawing")

if __name__ == "__main__":
    plumbing(); elevation(); harness(); block_drawing()
    print("drawings ->", os.path.relpath(D))
