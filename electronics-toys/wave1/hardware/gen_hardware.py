#!/usr/bin/env python3
"""Generate AP1 hardware artefacts: pin map, netlist, BOM + design-to-cost report, power budget,
and schematic drawings.  Usage: python gen_hardware.py <out_dir>   (needs schemdraw + matplotlib)

All part numbers are CANDIDATES from general knowledge and all prices are planning estimates (INR at ~1k units).
Nothing here has been built or bench-tested."""
import csv
import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ pin map (abstract MCU-32, >=24 GPIO)
# product columns: P1 rhymes player, P3 star lamp, P4 cricket game
PINS = [
    ("PA0", "UART_TX -> MP3 module RX (1k series)", "UART_TX", "UART_TX", "-"),
    ("PA1", "UART_RX <- MP3 module TX", "UART_RX", "UART_RX", "-"),
    ("PA2", "MP3 BUSY (low = playing)", "MP3_BUSY", "MP3_BUSY", "-"),
    ("PA3", "BTN0", "BTN_PLAY", "BTN_MODE", "BTN_BAT"),
    ("PA4", "BTN1", "BTN_NEXT", "BTN_TIMER", "BTN_START"),
    ("PA5", "BTN2", "BTN_PREV", "BTN_SONG", "-"),
    ("PA6", "BTN3", "BTN_VOLUP", "-", "-"),
    ("PA7", "BTN4", "BTN_VOLDN", "-", "-"),
    ("PB0", "BTN5", "BTN_LANG", "-", "-"),
    ("PB1", "BTN6", "BTN_SLEEP", "-", "-"),
    ("PB2", "LED/PWM0", "LED_PLAY", "PWM_R (via NPN)", "-"),
    ("PB3", "LED/PWM1", "LED_SLEEP", "PWM_G (via NPN)", "-"),
    ("PB4", "LED/PWM2", "-", "PWM_B (via NPN)", "-"),
    ("PB5", "MOTOR", "-", "PROJECTOR_MOTOR (via NPN)", "-"),
    ("PB6", "BUZZER", "-", "-", "PIEZO (via NPN)"),
    ("PB7", "74HC595 SER", "-", "-", "SEG_SER"),
    ("PC0", "74HC595 SRCLK", "-", "-", "SEG_SRCLK"),
    ("PC1", "74HC595 RCLK", "-", "-", "SEG_RCLK"),
    ("PC2", "DIGIT0 select (NPN)", "-", "-", "DIG0"),
    ("PC3", "DIGIT1 select (NPN)", "-", "-", "DIG1"),
    ("PC4", "DIGIT2 select (NPN)", "-", "-", "DIG2"),
    ("PC5", "DIGIT3 select (NPN)", "-", "-", "DIG3"),
    ("PC6", "ADC: battery divider", "VBAT_SENSE", "VBAT_SENSE", "VBAT_SENSE"),
    ("PC7", "SWD / factory test", "TEST_MODE", "TEST_MODE", "TEST_MODE"),
]
with open(OUT / "pinmap.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["MCU pin (abstract)", "Role", "P1 rhymes player", "P3 star lamp", "P4 cricket game"])
    w.writerows(PINS)

NETS = [  # net, nodes (power and shared)
    ("VBAT", "Battery+ -> slide switch -> Q1 (P-FET, reverse-polarity) -> VBAT_SW"),
    ("VBAT_SW", "U2 LDO in, MP3 module VCC, amp rail, divider R1/R2 top"),
    ("3V3", "U2 LDO out, MCU VDD, pull-ups, 74HC595 VCC"),
    ("GND", "Battery-, all grounds, speaker return"),
    ("SPK+/SPK-", "MP3 module speaker out -> speaker (P1, P3)"),
    ("UART", "MCU PA0/PA1 <-> MP3 module RX/TX, 1k series each"),
    ("VBAT_SENSE", "R1 100k / R2 100k divider -> PC6 (ADC); ratio 0.5"),
]
with open(OUT / "netlist_power_and_shared.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Net", "Connections"]); w.writerows(NETS)

# ------------------------------------------------------------------ BOM + design-to-cost
# (item, qty, unit INR, note)
COMMON = [
    ("2-layer PCB ~90x60 mm", 1, 30, "India fab at ~1k: unverified"),
    ("LDO 3.3 V low-Iq (HT7533-class)", 1, 4, "alt: any 3.3 V 250 mA LDO"),
    ("P-MOSFET reverse protection (AO3401-class)", 1, 3, ""),
    ("Passives (caps, resistors, divider)", 1, 12, "lot price"),
    ("Slide switch", 1, 5, ""),
    ("Battery holder 3xAA/AAA with leads", 1, 18, ""),
    ("Screws, bosses, battery-door hardware", 1, 5, "captive M3 screw"),
]
PRODUCTS = {
    "P1 Rhymes player (SD card, 100 rhymes/lang)": dict(price=999, phase2_bom=330, parts=COMMON + [
        ("MCU Cortex-M0+ 32-pin", 1, 45, "e.g. STM32G0 / PY32 class"),
        ("MP3 module (YX5200 / DFPlayer-style)", 1, 70, "alt: bare YX5200 chip at volume"),
        ("microSD 4 GB, preloaded", 1, 130, "dominant cost - see variant B"),
        ("Speaker 3 W 4 ohm 40 mm", 1, 28, ""),
        ("Tactile buttons x7 + caps", 1, 14, ""),
        ("LEDs x2 + resistors", 1, 3, ""),
        ("Enclosure ABS, 3 parts (150 g resin + moulding)", 1, 48, "from enclosure/checks.md mass"),
        ("Tooling amortisation (Rs 3 lakh / 5,000 units)", 1, 60, "assumption"),
        ("Packaging (window box, insert, manual)", 1, 40, ""),
        ("Assembly + functional test labour", 1, 35, ""),
    ]),
    "P1b Rhymes player (SPI flash, 30 rhymes @32 kbps)": dict(price=999, phase2_bom=330, parts=COMMON + [
        ("MCU Cortex-M0+ 32-pin", 1, 45, ""),
        ("MP3 chip module with SPI-flash support (WT2003-class)", 1, 85, "needs verification"),
        ("SPI NOR flash 128 Mbit, programmed", 1, 45, "~16 MB: ~30 rhymes at 32 kbps"),
        ("Speaker 3 W 4 ohm 40 mm", 1, 28, ""),
        ("Tactile buttons x7 + caps", 1, 14, ""),
        ("LEDs x2 + resistors", 1, 3, ""),
        ("Enclosure ABS, 3 parts (150 g resin + moulding)", 1, 48, ""),
        ("Tooling amortisation (Rs 3 lakh / 5,000 units)", 1, 60, ""),
        ("Packaging (window box, insert, manual)", 1, 40, ""),
        ("Assembly + functional test labour", 1, 35, ""),
    ]),
    "P3 Star projector lamp": dict(price=799, phase2_bom=260, parts=COMMON + [
        ("MCU Cortex-M0+ 20-pin", 1, 35, ""),
        ("MP3 module (YX5200-style)", 1, 70, ""),
        ("microSD 1 GB (8 lullabies)", 1, 70, ""),
        ("Speaker 2 W 36 mm", 1, 20, ""),
        ("RGB LEDs 3 x 0.5 W + driver NPN x3", 1, 22, ""),
        ("Projection lens + star film", 1, 25, ""),
        ("Rotor motor + gear", 1, 14, ""),
        ("Buttons x3", 1, 5, ""),
        ("Enclosure ABS + silicone shell", 1, 55, ""),
        ("Tooling amortisation (Rs 4 lakh / 5,000 units)", 1, 80, ""),
        ("Packaging", 1, 40, ""),
        ("Assembly + functional test labour", 1, 35, ""),
    ]),
    "P3b Star lamp, low-cost (OTP voice chip, 3 lullabies, no SD)": dict(price=799, phase2_bom=260, parts=COMMON + [
        ("MCU Cortex-M0+ 20-pin", 1, 35, "firmware: GPIO-triggered voice chip instead of UART"),
        ("OTP voice IC with 3 lullabies (60 s class) + small amp", 1, 22, "needs verification; content fixed at factory"),
        ("Speaker 2 W 36 mm", 1, 20, ""),
        ("RGB LEDs 3 x 0.5 W + driver NPN x3", 1, 22, ""),
        ("Projection lens + star film", 1, 25, ""),
        ("Rotor motor + gear", 1, 14, ""),
        ("Buttons x3", 1, 5, ""),
        ("Enclosure ABS + silicone shell", 1, 55, ""),
        ("Tooling amortisation (Rs 4 lakh / 5,000 units)", 1, 80, ""),
        ("Packaging", 1, 40, ""),
        ("Assembly + functional test labour", 1, 35, ""),
    ]),
    "P4 Cricket game": dict(price=699, phase2_bom=220, parts=[
        ("2-layer PCB ~90x60 mm", 1, 30, ""),
        ("LDO 3.3 V low-Iq", 1, 4, ""),
        ("P-MOSFET reverse protection", 1, 3, ""),
        ("Passives lot", 1, 12, ""),
        ("Slide switch", 1, 5, ""),
        ("Battery holder 3xAAA", 1, 14, ""),
        ("MCU Cortex-M0+ 32-pin", 1, 45, ""),
        ("74HC595 x2", 1, 10, ""),
        ("4-digit 7-segment display", 1, 30, ""),
        ("LEDs x7 + resistors", 1, 8, ""),
        ("Piezo buzzer + NPN", 1, 8, ""),
        ("Buttons x2", 1, 4, ""),
        ("Enclosure ABS 2-part (87 g resin + moulding)", 1, 32, ""),
        ("Tooling amortisation (Rs 2.5 lakh / 5,000 units)", 1, 50, ""),
        ("Packaging + rules card", 1, 35, ""),
        ("Assembly + functional test labour", 1, 25, ""),
    ]),
}

GST, LAND, CLOSE, SHIP, ADS, RET = 0.18, 1.0, 30, 80, 0.12, 0.08   # BOM above already includes assembly/packaging


def contribution(price, bom, ref_rate=None):
    """Amazon.in marketplace contribution; same model as electronics-toys/top50.csv except that
    the BOM here already includes packaging, tooling and assembly (so landed = BOM * 1.08 for scrap/freight)."""
    landed = bom * 1.08
    net = price / (1 + GST)
    referral = 0 if price < 1000 else 0.08
    fees = price * referral + CLOSE + SHIP
    cont = net - landed - fees - net * ADS - RET * landed
    return net, landed, cont, cont / net


rows = []
with open(OUT / "bom.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Product", "Item", "Qty", "Unit INR @1k (estimate)", "Line INR", "Note"])
    for name, p in PRODUCTS.items():
        total = 0
        for item, q, u, note in p["parts"]:
            w.writerow([name, item, q, u, q * u, note]); total += q * u
        w.writerow([name, "TOTAL BOM (incl. tooling amortisation, packaging, assembly)", "", "", total, ""])
        rows.append((name, p["price"], p["phase2_bom"], total))

report = ["| Product | Phase 2 landed guess (BOM x1.3) | Designed landed (BOM x1.08) | Designed BOM | Price | Net rev | Contribution | Margin |", "|---|---|---|---|---|---|---|---|"]
for name, price, ph2, bom in rows:
    net, landed, cont, pct = contribution(price, bom)
    report.append(f"| {name} | {ph2 * 1.3:.0f} | {landed:.0f} | {bom} | {price} | {net:.0f} | {cont:.0f} | {pct:.0%} |")
# break-even / target prices for >=20% margin
report.append("")
report.append("Price needed for >=20% contribution on the marketplace (assumed fee model):")
report.append("")
for name, price, ph2, bom in rows:
    p = price
    while True:
        _, _, c, pct = contribution(p, bom)
        if pct >= 0.20 or p > 5000: break
        p += 10
    report.append(f"- {name}: about Rs {p}")
(OUT / "design_to_cost.md").write_text("\n".join(report) + "\n")
print("\n".join(report))

# volume sensitivity: tooling amortised over 20,000 instead of 5,000 units
sens = ["", "Volume sensitivity (tooling amortised over 20,000 units instead of 5,000):", "",
        "| Product | BOM @5k | BOM @20k | Margin @20k at listed price |", "|---|---|---|---|"]
for name, p_ in PRODUCTS.items():
    b5 = sum(q * u for _, q, u, _ in p_["parts"])
    b20 = sum(q * (u / 4 if "Tooling" in i else u) for i, q, u, _ in p_["parts"])
    _, _, c, pct = contribution(p_["price"], b20)
    sens.append(f"| {name} | {b5:.0f} | {b20:.0f} | {pct:.0%} |")
(OUT / "design_to_cost.md").write_text((OUT / "design_to_cost.md").read_text() + "\n".join(sens) + "\n")
print("\n".join(sens))

# ------------------------------------------------------------------ power budget (assumptions)
def hours(capacity_mah, avg_ma): return capacity_mah / avg_ma
budget = [
    ("P1 rhymes @ moderate volume", 2500, 5 + 90, "MCU 5 mA + module/amp ~90 mA average (assumed)"),
    ("P1 rhymes @ max cap volume", 2500, 5 + 220, "module/amp peaks; assumed"),
    ("P3 lamp warm-white only, no song", 1000, 60, "3 x AAA alkaline ~1000 mAh"),
    ("P3 lamp rainbow + lullaby", 1000, 140, "assumed"),
    ("P4 cricket game", 1000, 25, "display multiplex + LEDs, assumed"),
]
pb = ["| Case | Battery mAh (alkaline) | Avg mA (assumed) | Hours |", "|---|---|---|---|"]
for n, cap, ma, note in budget:
    pb.append(f"| {n} | {cap} | {ma} | {hours(cap, ma):.0f} |")
(OUT / "power_budget.md").write_text("\n".join(pb) + "\n\nAll currents are assumptions to be replaced by bench measurements.\n")

# ------------------------------------------------------------------ schematic drawings
import matplotlib
matplotlib.use("Agg")
import schemdraw
import schemdraw.elements as elm
from schemdraw import flow

schemdraw.use("matplotlib")

# 1. block diagram of the AP1 platform (plain matplotlib: reliable layout)
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(13, 4.2))
ax.set_xlim(0, 26); ax.set_ylim(0, 8.4); ax.axis("off")


def box(x, y, w, h, text, fc="#eef3fb"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec="#223", lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.5, color="#223"))


box(0.3, 3.2, 3.0, 2.0, "3 x AA / AAA\nbattery\n(4.5 V)")
box(4.3, 3.2, 2.4, 2.0, "Slide\nswitch")
box(7.7, 3.2, 3.0, 2.0, "P-FET\nreverse-polarity\nprotection")
box(11.7, 3.2, 2.6, 2.0, "LDO\n3.3 V")
box(15.3, 2.7, 3.2, 3.0, "MCU\nCortex-M0+\n(32 pin)", fc="#fdf1d6")
box(19.5, 3.2, 3.2, 2.0, "MP3 module\n+ SD / SPI flash")
box(23.5, 3.2, 2.3, 2.0, "Speaker\n3 W")
for x1, x2 in [(3.3, 4.3), (6.7, 7.7), (10.7, 11.7), (14.3, 15.3), (18.5, 19.5), (22.7, 23.5)]:
    arrow(x1, 4.2, x2, 4.2)
box(13.8, 6.4, 6.2, 1.2, "8 buttons (debounced in firmware)")
box(13.4, 0.3, 7.0, 1.4, "LEDs / RGB PWM / 7-seg via 74HC595")
arrow(16.9, 6.4, 16.9, 5.7); arrow(16.9, 2.7, 16.9, 1.7)
ax.text(0.3, 7.4, "AP1 audio / toy platform - block diagram", fontsize=11, ha="left", weight="bold")
fig.savefig(OUT / "block_diagram.png", dpi=140, bbox_inches="tight")
plt.close(fig)

# 2. power section: hand-drawn connection diagram (not CAD output)
fig, ax = plt.subplots(figsize=(12, 5.6))
ax.set_xlim(-1, 17); ax.set_ylim(-0.5, 8); ax.axis("off")
LW = dict(color="#223", lw=1.8)
def ln(*pts): ax.plot([p[0] for p in pts], [p[1] for p in pts], **LW)
def part(x, y, w, h, text, fc="#eef3fb"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04", fc=fc, ec="#223", lw=1.5)); ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)
def dot(x, y): ax.plot([x], [y], "o", color="#223", ms=6)
def gnd(x, y):
    ln((x, y), (x, y - 0.3)); ln((x - 0.35, y - 0.3), (x + 0.35, y - 0.3)); ln((x - 0.2, y - 0.45), (x + 0.2, y - 0.45)); ln((x - 0.08, y - 0.6), (x + 0.08, y - 0.6))
Y, G = 5.5, 1.0                                          # supply rail y, ground rail y
part(-0.8, 2.4, 2.0, 2.6, "3 x AA\n4.5 V\n(+ top)")
ln((0.2, 5.0), (0.2, Y), (2.2, Y)); part(2.2, Y - 0.5, 1.6, 1.0, "S1\nswitch"); ln((3.8, Y), (5.4, Y)); dot(5.4, Y)
ax.text(5.4, Y + 0.45, "VBAT", ha="center", fontsize=9)
part(5.9, Y - 0.6, 2.8, 1.2, "Q1 P-FET\nDRAIN -> SOURCE", fc="#fdf1d6"); ln((5.4, Y), (5.9, Y)); ln((8.7, Y), (10.2, Y)); dot(10.2, Y)
ax.text(10.2, Y + 0.45, "VBAT_SW", ha="center", fontsize=9)
ln((7.3, Y - 0.6), (7.3, G + 0.0)); dot(7.3, G); ax.text(7.55, 3.0, "gate to GND\n(turns on when battery is\nconnected the right way)", fontsize=8, va="center")
ln((10.2, Y), (11.2, Y)); part(11.2, Y - 0.7, 2.4, 1.4, "U2 LDO\n3.3 V"); ln((13.6, Y), (15.6, Y)); dot(15.6, Y); ax.text(15.6, Y + 0.45, "3V3", ha="center", fontsize=9)
ln((12.4, Y - 0.7), (12.4, G)); dot(12.4, G)
ln((10.2, Y), (10.2, 4.3)); part(9.6, 3.2, 1.2, 1.1, "R1\n100k"); ln((10.2, 3.2), (10.2, 2.7)); dot(10.2, 2.7)
ax.text(10.5, 2.7, "VBAT_SENSE -> MCU ADC (PC6)", fontsize=9, va="center")
ln((10.2, 2.7), (10.2, 2.4)); part(9.6, 1.3, 1.2, 1.1, "R2\n100k"); ln((10.2, 1.3), (10.2, G)); dot(10.2, G)
ln((-0.2, 2.4), (-0.2, G), (15.6, G)); ln((-0.2, G), (-0.2, G)); gnd(15.6, G)
ax.text(-0.9, 7.4, "AP1 power section - connection diagram (draw in KiCad for the PCB)", fontsize=11, weight="bold")
ax.text(-0.9, 0.0, "P-FET reverse protection: battery+ to DRAIN, load to SOURCE, GATE to GND. Wrong-way battery = FET stays off.", fontsize=8.5)
fig.savefig(OUT / "power_section.png", dpi=140, bbox_inches="tight"); plt.close(fig)

# 3. MP3 + speaker section
with schemdraw.Drawing(show=False) as d:
    d.config(unit=3, fontsize=9)
    ic = elm.Ic(pins=[elm.IcPin(name="VCC", side="left", pin="1"), elm.IcPin(name="RX", side="left", pin="2"),
                       elm.IcPin(name="TX", side="left", pin="3"), elm.IcPin(name="BUSY", side="left", pin="16"),
                       elm.IcPin(name="GND", side="left", pin="7"),
                       elm.IcPin(name="SPK1", side="right", pin="6"), elm.IcPin(name="SPK2", side="right", pin="8")],
                 edgepadH=0.5, pinspacing=1.0, size=(3.2, 5.2)).label("MP3 module\n(YX5200 class)\n+ microSD", loc="top")
    d += ic
    d += elm.Line().at(ic.SPK1).right(1.0)
    d += elm.Speaker().right().label("LS1\n3 W 4 ohm")
    d += elm.Line().at(ic.SPK2).right(1.0).tox(d.here) if False else elm.Line().at(ic.SPK2).right(1.0)
    d += elm.Resistor().at(ic.RX).left(1.6).label("R3 1k", loc="top")
    d += elm.Dot().label("MCU PA0 (TX)", loc="left")
    d += elm.Line().at(ic.TX).left(0.8)
    d += elm.Dot().label("MCU PA1 (RX)", loc="left")
    d += elm.Line().at(ic.BUSY).left(0.8)
    d += elm.Dot().label("MCU PA2", loc="left")
    d += elm.Line().at(ic.VCC).left(0.8)
    d += elm.Dot().label("VBAT_SW", loc="left")
    d += elm.Line().at(ic.GND).left(0.8)
    d += elm.Ground()
    d.save(str(OUT / "mp3_speaker_section.png"), dpi=140)

print("wrote", sorted(p.name for p in OUT.iterdir()))
