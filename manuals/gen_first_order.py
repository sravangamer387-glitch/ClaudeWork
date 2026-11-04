#!/usr/bin/env python3
"""Consolidated FIRST ORDER across a chosen set of projects: one JLCPCB order (PCB + SMT assembly), one LCSC cart for the
hand-soldered parts of every board, and one India buying list for the bought-in modules, mechanics, consumables and tools.
Prices come from the live-priced BOMs in costing/<board>_priced_BOM.csv (run utility10/pcb/costing.py first).
Writes costing/FIRST_ORDER.md and costing/FIRST_ORDER_lcsc_cart.csv (LCSC "BOM upload" format).   usage: python3 manuals/gen_first_order.py"""
import csv, glob, math, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REL = os.path.join(ROOT, "utility10", "pcb", "release"); COST = os.path.join(ROOT, "costing"); INR = 88.0

# ---------------------------------------------------------------- the chosen first batch
# (board, project, folder, PCBs ordered, boards assembled by JLCPCB, why it is in the first batch)
BATCH = [
    ("trishna", "TRISHNA urinal hydration monitor", "trishna", 5, 2, "your priority project; the most complex - start bring-up early"),
    ("arcade", "Desi Arcade (toys 01 Reflex Raja, 02 Taal Memory, 03 Aloo Bomb)", "toys10/01-reflex-raja", 5, 2, "one board runs three games; fun, quick to validate"),
    ("chulha", "Chulha Timers", "utility10/06-chulha-timers", 5, 2, "simple utility, high confidence"),
    ("fridge", "Fridge Door Guard", "utility10/03-fridge-door-guard", 5, 2, "simplest board in the portfolio; first soldering practice"),
    ("prayog", "Prayog STEM lab kit (hub)", "products/03-prayog", 5, 2, "USB bench instrument; doubles as a test tool for the others"),
]
BUILD_SETS = 2          # hand-solder parts are bought for every assembled board (2 per design)
SPARE = 0.2             # + 20 % spares, at least 1, on every hand-solder line

# ---------------------------------------------------------------- bought-in items (India), prototype quantities for ONE complete unit
# (project, item, qty, spec, where, INR each approx)
BOUGHT = [
 ("TRISHNA", "ESP32-DevKitC-32E", 1, "38-pin, 25.4 mm row spacing, WROOM-32E/32D (not WROVER, not 30-pin DOIT)", "element14 India, Robu.in", 1000),
 ("TRISHNA", "12 V 2 A adapter", 1, "5.5 x 2.1 mm, centre positive, BIS-marked", "local / Amazon.in", 380),
 ("TRISHNA", "Peristaltic pump 12 V", 1, "DC, 0.2-0.4 A, 3 x 5 mm tube, 40-100 mL/min", "Robu.in / Amazon.in", 700),
 ("TRISHNA", "Solenoid valve 12 V NC", 1, "DIRECT-ACTING, 0 MPa minimum (not an RO pilot valve), <= 6 W", "Amazon.in / Robu.in", 450),
 ("TRISHNA", "VL53L1X ToF breakout", 1, "3.3 V I2C (Pololu 3415 / CJMCU-531)", "Robu.in / Robocraze", 750),
 ("TRISHNA", "DS18B20 waterproof probe", 1, "6 x 50 mm SS sheath, 1 m", "Robu.in", 160),
 ("TRISHNA", "Photodiode OSRAM SFH 203", 3, "5 mm clear, wide angle (1 spare)", "element14 India / Mouser India", 80),
 ("TRISHNA", "LED 5 mm 450 nm + LED 5 mm 850 nm", 2, "one of each (+1 spare each)", "Robu.in / element14", 30),
 ("TRISHNA", "Titanium wire Gr2 1.0 mm", 1, "30 cm", "Amazon.in", 400),
 ("TRISHNA", "Silicone tube food-grade 3x5 mm + 4x6 mm", 2, "2 m each", "Amazon.in / aquarium shop", 150),
 ("TRISHNA", "Fittings set", 1, "6 x M5-to-4 mm barb (PP/nylon), 2 check valves, 2 tees, 2 reducers", "Amazon.in / aquarium shop", 450),
 ("TRISHNA", "Cable glands kit", 1, "4 x M16 + 10 x M12 nylon IP68", "Robu.in / electrical shop", 300),
 ("TRISHNA", "O-ring kit + 2.5 mm silicone cord 1.5 m", 1, "metric NBR kit (5x1, 6x1.5)", "Amazon.in", 450),
 ("TRISHNA", "USB-serial adapter CP2102 / CH340 (3.3 V)", 1, "for the telemetry header J15", "Robu.in", 150),
 ("TRISHNA", "microSD 8-32 GB", 1, "FAT32", "any", 300),
 ("TRISHNA", "Reservoir 1.5-2 L + 4 mm bulkhead", 1, "food container, open top", "local", 200),
 ("TRISHNA", "Calibration: KCl standards 1413 uS + 12.88 mS", 1, "Hanna HI7031 / HI7030 sachets (or weigh KCl)", "lab supplier / Amazon.in", 600),
 ("TRISHNA", "Urine-SG refractometer (ATC, 1.000-1.050)", 1, "for the SG model fit", "Amazon.in / lab supplier", 1200),
 ("TRISHNA", "Bench chemicals", 1, "NaCl, KCl, urea, riboflavin tablet, citric acid", "chemist / grocery", 250),
 ("Desi Arcade", "Arcade push button 30 mm with 5 V LED", 4, "3-wire leads to J5-J8 (button, lamp, GND)", "Robu.in / Amazon.in", 80),
 ("Desi Arcade", "3 x AAA holder with leads", 1, "Keystone 2480 or generic, 2-pin JST-PH plug", "Amazon.in / element14", 40),
 ("Chulha Timers", "TM1637 4-digit display module", 1, "0.56 in, 4-pin (VCC GND DIO CLK) to J4", "Robu.in", 90),
 ("Chulha Timers", "3 x AAA holder with leads", 1, "Keystone 2480 or generic", "Amazon.in", 40),
 ("Chulha Timers", "Flat magnet about 30 x 20 x 3 mm", 1, "ferrite or neodymium, epoxy to the back plate", "Amazon.in / hardware", 60),
 ("Fridge Door Guard", "Reed switch + magnet (MC-38 type, wired)", 1, "normally-open, leads to J3", "Robu.in / Amazon.in", 80),
 ("Fridge Door Guard", "2 x AAA holder with leads", 1, "Keystone 2469 or generic", "Amazon.in", 30),
 ("Prayog hub", "Starter sensor set", 1, "10k NTC module, LDR module, sound module, linear Hall (49E) module, capacitive soil v1.2, HC-SR04, 2 x TCRT5000 IR, 2 x U-slot photogate, push button + LED", "Robu.in / Robocraze", 950),
 ("Prayog hub", "JST-PH 3-pin leads 20 cm", 12, "pre-crimped, one per module", "Robu.in / Amazon.in", 15),
 ("Prayog hub", "USB-C data cable", 1, "for the CH340C USB-serial", "any", 150),
 ("All AVR boards", "USBasp programmer + 10-to-6-pin ISP adapter", 1, "fuses + firmware for Arcade, Chulha, Fridge; bootloader for Prayog", "Robu.in", 300),
 ("All", "AAA cells", 8, "3 Arcade + 3 Chulha + 2 Fridge", "any", 20),
 ("All", "Black PETG 1 kg", 2, "TRISHNA (about 600 g) + four v2 enclosures (about 400 g) + reprints", "Robu.in / local", 1200),
 ("All", "Clear PETG 250 g (light pipes) or resin", 1, "only the light-pipe caps", "local", 400),
 ("All", "M2.5 self-tapping screw kit", 1, "x 6 and x 10 mm (v2 enclosure lids, standoffs, battery doors)", "hardware / Amazon.in", 250),
 ("All", "M3 heat-set inserts (40) + M3/M2 screw assortment", 1, "TRISHNA lids, brackets, port retainers", "Robu.in", 450),
 ("All", "JST-PH 2.0 crimp kit + crimper (SN-28B / PA-09)", 1, "housings 2/3/4-pin + contacts", "Robu.in", 900),
 ("All", "Sealants and consumables", 1, "black neutral RTV, 2-part epoxy, PTFE tape, flux, solder 0.6 mm, heat-shrink", "hardware / electronics shop", 900),
]

def rows(path):
    return list(csv.DictReader(open(path)))

def board_data(b):
    full = rows(glob.glob(os.path.join(REL, b, "2_assembly", "*BOM_full.csv"))[0])
    pb = [r for r in csv.reader(open(os.path.join(COST, f"{b}_priced_BOM.csv")))]
    head = pb[0]; price = {}; stock = {}
    for r in pb[1:]:
        if r and r[0] and not r[0].startswith("TOTAL"):
            d = dict(zip(head, r))
            if d.get("LCSC #"): price[d["LCSC #"]] = float(d["Unit USD (1 board)"] or 0); stock[d["LCSC #"]] = d["LCSC stock"]
    tot = [r for r in pb if r and r[0].startswith("TOTAL")][0]
    smt_usd = sum(price.get(r["LCSC #"], 0) for r in full if r["Assembly"].startswith("SMT"))
    hand = [r for r in full if not r["Assembly"].startswith("SMT") and r["LCSC #"]]
    smt_unique = sorted({r["LCSC #"] for r in full if r["Assembly"].startswith("SMT")})
    # JLC "basic" library (no 3 USD feeder fee): the common UNI-ROYAL 0603 resistors, Samsung CL10/CL21 MLCCs and a few jellybean parts
    BASIC = ("0603WAF", "CL10B", "CL10A", "CL10C", "CL21A", "CL21B", "AO3400A", "AO3401A", "MMBT3904", "KT-0603", "1N4148WS")
    ext = {r["LCSC #"] for r in full if r["Assembly"].startswith("SMT") and not any(k in (r["Manufacturer part"] + " " + r["LCSC #"]) for k in BASIC)}
    return dict(full=full, price=price, stock=stock, smt_usd=smt_usd, hand=hand, smt_unique=smt_unique, ext=sorted(ext), total1=float(tot[5].split(": ")[1]))

def size(b):
    import re
    s = open(os.path.join(ROOT, "utility10", "pcb", "boards", f"{b}.py")).read(); m = re.search(r"W, H = ([\d.]+), ([\d.]+)", s)
    return float(m.group(1)), float(m.group(2))

def main():
    L = ["# First order: consolidated shopping list", "",
         "Generated by `manuals/gen_first_order.py` from the live-priced BOMs (`costing/*_priced_BOM.csv`) and the project manuals. "
         f"Prices: LCSC unit price for small quantities on the run date, converted at {INR:.0f} INR/USD; bought-in items are approximate Indian street prices. "
         "**Re-check stock and prices on the day you order** (`python3 utility10/pcb/costing.py`).", "",
         "## 1. The first batch (and why)", "", "| Board | Project | PCBs | Assembled by JLCPCB | Why first |", "|---|---|---|---|---|"]
    data = {}
    for b, name, folder, npcb, nasm, why in BATCH:
        data[b] = board_data(b); L.append(f"| `{b}` | {name} | {npcb} | {nasm} | {why} |")
    L += ["", "Build plan: assemble 1 unit of each project first; the second assembled board of each design is the spare / second unit. "
          "The 3 bare PCBs per design wait for revision B.", "",
          "## 2. JLCPCB: one order, five designs (PCB + economic SMT assembly)", "",
          "Upload each design separately in the **same cart** (one shipment). Files: `utility10/pcb/release/<board>/1_fabrication/*_gerbers.zip`, "
          "`2_assembly/*_JLC_BOM.csv`, `2_assembly/*_JLC_CPL.csv`. Settings for all: 2 layers, 1.6 mm, HASL lead-free, green, PCBA economic, top side.", "",
          "| Board | Size (mm) | SMT parts / board (USD, LCSC price) | SMT lines (extended) | SMT parts for the assembled boards (USD) | PCB 5 pcs (USD, est.) | Assembly fees (USD, est.) |", "|---|---|---|---|---|---|---|"]
    jlc_parts = jlc_fees = jlc_pcb = 0.0
    for b, name, folder, npcb, nasm, why in BATCH:
        d = data[b]; w, h = size(b)
        pcb = 4.0 if w <= 100 and h <= 100 else 9.0                  # JLC 2-layer 5 pcs: about 2-4 USD up to 100 x 100 mm, about 8-10 USD above
        n_ext = len(d["ext"])                                          # lines that are not in JLC's basic library
        fees = 8.0 + 1.5 + 3.0 * n_ext                               # setup + stencil + 3 USD feeder fee per extended part
        parts = d["smt_usd"] * nasm * 1.1                             # + 10 % attrition
        jlc_parts += parts; jlc_fees += fees; jlc_pcb += pcb
        L.append(f"| `{b}` | {w:.0f} x {h:.0f} | {d['smt_usd']:.2f} | {len(d['smt_unique'])} ({n_ext}) | {parts:.2f} | {pcb:.0f} | {fees:.0f} |")
    ship = 30.0
    sub = jlc_parts + jlc_fees + jlc_pcb + ship
    L += [f"| **total** | | | | **{jlc_parts:.2f}** | **{jlc_pcb:.0f}** | **{jlc_fees:.0f}** |", "",
          f"Estimated JLCPCB order: parts {jlc_parts:.0f} + PCBs {jlc_pcb:.0f} + assembly fees {jlc_fees:.0f} + DHL/FedEx about {ship:.0f} = **about US${sub:.0f} (INR {sub * INR:,.0f})**, "
          f"plus Indian customs duty and IGST on arrival (budget about 30-40 % of the declared value: **about INR {sub * INR * 0.35:,.0f}**). "
          "Fees are estimates (8 USD setup + 1.5 USD stencil per design + 3 USD per *extended* part line; lines counted as basic: UNI-ROYAL 0603 resistors, Samsung CL10/CL21 capacitors, AO3400A/AO3401A, MMBT3904, KT-0603 LEDs, 1N4148WS - JLC's library decides): **the JLCPCB quote is authoritative**.", "",
          "## 3. LCSC cart: hand-soldered parts for all assembled boards", "",
          f"Quantities = per-board quantity x {BUILD_SETS} assembled boards + {int(SPARE * 100)} % spares (at least 1). Upload `costing/FIRST_ORDER_lcsc_cart.csv` with LCSC's **BOM tool** "
          "(columns: LCSC Part Number, Quantity, Manufacturer Part Number, Description) or add the lines by hand; put it in the **same order as the JLCPCB parts** if you use JLC's combined shipping.", "",
          "| LCSC # | Part | Used on | Qty to buy | Unit USD | Line USD | LCSC stock |", "|---|---|---|---|---|---|---|"]
    cart = collections.OrderedDict()
    for b, name, folder, npcb, nasm, why in BATCH:
        d = data[b]
        for r in d["hand"]:
            c = r["LCSC #"]; e = cart.setdefault(c, dict(mpn=r["Manufacturer part"], value=r["Value"], need=0, boards=set(), price=d["price"].get(c, 0), stock=d["stock"].get(c, "")))
            e["need"] += BUILD_SETS; e["boards"].add(b)
    lcsc_total = 0.0
    out = []
    for c, e in cart.items():
        q = e["need"] + max(1, math.ceil(e["need"] * SPARE)); line = q * e["price"]; lcsc_total += line
        L.append(f"| {c} | {e['mpn']} | {', '.join(sorted(e['boards']))} | {q} | {e['price']:.4f} | {line:.2f} | {e['stock']} |")
        out.append((c, q, e["mpn"], e["value"]))
    lcsc_ship = 15.0
    L += [f"| | **total** | | | | **{lcsc_total:.2f}** | |", "",
          f"LCSC cart about **US${lcsc_total:.0f}** + shipping about US${lcsc_ship:.0f} (cheaper if added to the JLCPCB shipment) = **about INR {(lcsc_total + lcsc_ship) * INR:,.0f}** before duty. "
          "The ESP32-DevKitC sockets, the barrel jacks and the JST connectors are in this cart; the DevKit itself is in section 4.", "",
          "## 4. Bought-in in India (one complete unit per project)", "", "| For | Item | Qty | Spec | Where | INR each (approx) | INR line |", "|---|---|---|---|---|---|---|"]
    india = 0
    for proj, item, q, spec, where, inr in BOUGHT:
        india += q * inr; L.append(f"| {proj} | {item} | {q} | {spec} | {where} | {inr:,} | {q * inr:,} |")
    L += [f"| | **total** | | | | | **{india:,}** |", "",
          "## 5. Budget summary", "", "| Block | INR (approx) |", "|---|---|",
          f"| JLCPCB (PCBs, SMT assembly, parts, shipping) | {sub * INR:,.0f} |", f"| Customs duty + IGST on the JLCPCB parcel (about 35 %) | {sub * INR * 0.35:,.0f} |",
          f"| LCSC cart (hand-solder parts) + shipping | {(lcsc_total + lcsc_ship) * INR:,.0f} |", f"| India bought-in, mechanics, consumables, tools | {india:,} |",
          f"| **Total for the first batch** | **{sub * INR * 1.35 + (lcsc_total + lcsc_ship) * INR + india:,.0f}** |", "",
          "Tools you need and may not have (not in the total): temperature-controlled soldering iron, multimeter, bench supply with current limit, 3D printer (or a print service), "
          "drill + 1.0/2.5/4.2/5.1 mm bits, M5 and M3 taps. See each manual's tool list.", "",
          "## 6. Order sequence", "",
          "1. Day 0: place the JLCPCB order (all five designs in one cart) and the LCSC cart; order the India items the same day (most arrive in 2-5 days).",
          "2. While the boards travel (7-12 days): print the enclosures and the TRISHNA parts; pressure-test the TRISHNA sensor block (manual 10.1 step 3); set up PlatformIO and avrdude.",
          "3. Boards arrive: solder the hand parts, then bring up in this order: Fridge Door Guard (simplest), Chulha Timers, Desi Arcade, Prayog hub, TRISHNA (dry bring-up, then plumbing).",
          "4. Record every result against the manual's acceptance tests before ordering more.", ""]
    os.makedirs(COST, exist_ok=True)
    open(os.path.join(COST, "FIRST_ORDER.md"), "w").write("\n".join(L))
    with open(os.path.join(COST, "FIRST_ORDER_lcsc_cart.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["LCSC Part Number", "Quantity", "Manufacturer Part Number", "Description"]); w.writerows(out)
    print(f"JLCPCB about US${sub:.0f}, LCSC about US${lcsc_total + lcsc_ship:.0f}, India about INR {india:,}; total about INR {sub * INR * 1.35 + (lcsc_total + lcsc_ship) * INR + india:,.0f}; {len(out)} cart lines")

if __name__ == "__main__":
    main()
