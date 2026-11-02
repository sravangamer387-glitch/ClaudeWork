"""Per-project ORDERING.md (what to order, where, in what steps) + the general ORDERING_GUIDE.md. Reads release folders, priced BOMs (costing/) and each project's manual."""
import os, re, csv, glob, json, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
src = open(os.path.join(ROOT, "manuals", "gen_index.py")).read()
rows_src = src[src.index("ROWS = ["):src.index("L = [")]
ns = {}; exec(rows_src, ns); ROWS = ns["ROWS"]
REL = os.path.join(ROOT, "utility10", "pcb", "release"); COST = os.path.join(ROOT, "costing")
INR = 88.0

def section(text, pats, maxlines=45):
    ls = text.splitlines()
    for i, l in enumerate(ls):
        if l.startswith("#") and any(re.search(p, l, re.I) for p in pats):
            lvl = len(l) - len(l.lstrip("#")); out = [l]
            for m in ls[i + 1:]:
                if m.startswith("#") and len(m) - len(m.lstrip("#")) <= lvl: break
                out.append(m)
            out = [x for x in out if x.strip()][:maxlines]
            return "\n".join(out)
    return None

def priced(board):
    f = os.path.join(COST, f"{board}_priced_BOM.csv")
    if not os.path.exists(f): return None
    rows = list(csv.reader(open(f))); head = rows[0]; body = [r for r in rows[1:] if r and r[0] and not r[0].startswith("TOTAL")]
    tot = [r for r in rows if r and r[0].startswith("TOTAL")]
    return head, body, tot[0] if tot else None

def board_block(board):
    d = os.path.join(REL, board); z = glob.glob(os.path.join(d, "1_fabrication", "*gerbers.zip")); bom = glob.glob(os.path.join(d, "2_assembly", "*JLC_BOM.csv")); cpl = glob.glob(os.path.join(d, "2_assembly", "*JLC_CPL.csv"))
    full = glob.glob(os.path.join(d, "2_assembly", "*BOM_full.csv"))
    if not (z and bom and cpl and full): return None
    rel = lambda p: os.path.relpath(p, ROOT)
    hand = [r for r in csv.DictReader(open(full[0])) if not r["Assembly"].startswith("SMT")]
    pr = priced(board); L = []
    L += ["## 2. Order the circuit boards (JLCPCB, PCB + assembly)", "",
          "Files (all in this repository):", "", f"- Gerbers: `{rel(z[0])}`", f"- Assembly BOM: `{rel(bom[0])}`", f"- Pick-and-place (CPL): `{rel(cpl[0])}`", f"- Full BOM with LCSC numbers and prices: `costing/{board}_priced_BOM.csv`", "",
          "Steps:", "",
          "1. Create an account at **jlcpcb.com** and click *Order now*. Upload the Gerber ZIP. The viewer must show the board outline, both copper layers, silkscreen and drill holes.",
          "2. Settings: **2 layers, 1.6 mm, FR-4**, lead-free HASL (use **ENIG** if the board has an LGA/QFN fine-pitch part, e.g. ADXL345, ESP32 module pad, BQ25570), green mask, white silk, quantity 5 (the minimum), *Remove order number: specify a location* if you want to avoid the order-number mark. Heavier copper (2 oz) only where the board notes say so.",
          "3. Switch on **PCB Assembly**: *Economic*, assembly side *Top*, and set tooling holes *Added by JLCPCB* unless the board already has them. Choose the number of boards to assemble (2 or 5).",
          "4. Upload the BOM and CPL. In the parts step, every line must match (LCSC numbers are in the BOM). Where a part is shown as *out of stock* or *no match*, use the alternative suggested by JLCPCB only after checking footprint and value against the list below; do not accept a different footprint.",
          "5. In the **component placement preview**, check pin 1 / polarity of every IC, diode, LED, electrolytic capacitor, USB-C and connector against `*_assembly_top.pdf` in the same folder. Wrong rotation is the most common assembly error: ask JLCPCB support to rotate before approving.",
          "6. Pay, then approve the assembly engineering review messages (they usually ask about a part or rotation). Delivery by DHL/FedEx/UPS takes about 1 to 2 weeks to India.", ""]
    if hand:
        L += ["Parts **not** assembled by JLCPCB (you buy and solder them yourself):", "", "| Refs | Value | Part | LCSC |", "|---|---|---|---|"]
        g = {}
        for r in hand: g.setdefault((r["Value"], r["Manufacturer part"], r["LCSC #"]), []).append(r["Ref"])
        for (v, m, c), rf in g.items(): L.append(f"| {', '.join(rf)} | {v} | {m} | {c} |")
        L += ["", "Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).", ""]
    if pr:
        head, body, tot = pr
        L += ["### Parts cost and stock (live LCSC prices on the run date)", "", f"Total parts per board: **US${float(tot[5].split(': ')[1]):.2f} for 1 board**, **US${float(tot[6].split(': ')[1]):.2f} each for 10 boards**, **US${float(tot[7].split(': ')[1]):.2f} each for 100 boards** (about INR {float(tot[5].split(': ')[1])*INR:.0f} / {float(tot[6].split(': ')[1])*INR:.0f} / {float(tot[7].split(': ')[1])*INR:.0f} at {INR:.0f} INR/USD). The per-line break-up is in `costing/{board}_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).", ""]
        low = [r for r in body if r[9]]
        if low: L += ["Stock warnings on the run date:", ""] + [f"- {r[4]} {r[2]} ({r[9].lower()}, stock {r[8]})" for r in low] + [""]
        L += ["| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |", "|---|---|---|---|---|---|---|"]
        for r in body: L.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} |")
        L.append("")
    return L

def doc_for(name, path, board, cav):
    mp = os.path.join(ROOT, path, "MANUFACTURING_MANUAL.md"); txt = open(mp).read() if os.path.exists(mp) else ""
    L = [f"# {name}: ordering guide (what to buy, where, in what order)", "",
         f"> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). {("Main caveat for this project: " + cav + ". ") if cav else ""}Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../{'../' * (path.count('/'))}manuals/ORDERING_GUIDE.md).", "",
         "## 1. Order of work", ""]
    steps = ["Read the manual and the caveat above.", "Order the circuit boards and SMD assembly (section 2)." if board else "No custom circuit board: nothing to order from JLCPCB for this project.",
             "While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.", "Assemble, program and test only after everything has arrived; follow the manual."]
    L += [f"{i + 1}. {s}" for i, s in enumerate(steps)] + [""]
    bl = board_block(board) if board else None
    if bl: L += bl
    elif board: L += ["## 2. Circuit board", "", f"Board `{board}` has no release folder yet; see the manual for status.", ""]
    if board:
        ej = os.path.join(REL, board, "4_enclosure", "enclosure.json")
        if os.path.exists(ej):
            e = json.load(open(ej)); L += ["## 2b. Enclosure: printed parts and fasteners (generated from the board)", ""]
            if e.get("mode", "").startswith("mounting plate"):
                L += [f"- Print `4_enclosure/*_enclosure_plate.stl` ({e['plate'][0]:.0f} x {e['plate'][1]:.0f} x 3 mm, PETG or ABS). Buy an **IP65 ABS junction box** with at least {e['min_box_inside'][0]:.0f} x {e['min_box_inside'][1]:.0f} x {e['min_box_inside'][2]:.0f} mm inside, cable glands and a breather/vent membrane; fix the plate with 4 x M4 screws.", f"- Board to plate: 4 x M2.5 x 6 mm self-tapping screws. {e.get('note', '')}", ""]
            else:
                L += [f"- Print `4_enclosure/` base and lid (outer about {e['outer'][0]:.0f} x {e['outer'][1]:.0f} x {e['outer'][2]:.0f} mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws."]
                if e.get("battery"): L += [f"- Battery: **{e['holder']}** in the floor bay ({e['bay'][0]} x {e['bay'][1]} x {e['bay'][2]} mm); print `*_enclosure_battery_door.stl`; the door closes with {e['door_screws']}. Route the holder lead through the hole in the bay ceiling to the battery connector."]
                if e.get("caps"):
                    kinds = sorted({c["kind"] for c in e["caps"]})
                    L += [f"- Print `*_enclosure_caps.stl` ({', '.join(kinds)}): " + "; ".join(f"{c['kind']} for {c['ref']}" for c in e["caps"]) + ". Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid."]
                if e.get("note"): L += [f"- {e['note']}"]
                L += ["- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.", ""]
    L += ["## 3. Bought-in and mechanical items", ""]
    b = section(txt, [r"bought"]) or section(txt, [r"bill of materials", r"materials", r"parts list", r"what you need", r"^#+ *\d*\.? *parts"])
    L += [b if b else "See the parts and materials section of the manual.", ""]
    cj = os.path.join(COST, "confidence.json")
    if os.path.exists(cj):
        c = {r["path"]: r for r in json.load(open(cj))}.get(path)
        if c: L += ["## 4. Confidence (read before you order)", "", f"- **Order confidence: {c['order']}**: {c['order_why']}.", f"- **Works-as-intended confidence: {c['works']}**: {c['works_why']}", f"- **First thing to do:** {c['first']}", "- Rubric and the reasons for every project: `costing/CONFIDENCE.md`. These are judgements, not measurements: nothing here has been built.", ""]
    L += ["## 5. Where to buy and whom to approach", "", "| Item type | India (fast, GST invoice) | Overseas (cheaper, 1 to 3 weeks, customs) |", "|---|---|---|",
          "| Printed circuit board and SMD assembly | JLCPCB is the practical choice for 5 to 100 boards; local PCB shops quote per project (ask for the Gerber ZIP price) | **JLCPCB** (jlcpcb.com), PCBWay (pcbway.com) |",
          "| Connectors, headers, passives, ICs by LCSC number | element14 India, Mouser India, DigiKey India (genuine, GST invoice, higher price); local electronics markets for common parts | **LCSC** (lcsc.com) with the same cart as JLCPCB |",
          "| Modules: ESP32 dev boards, SIM7080G, LoRa (RA-08 / RAK3172), pH / EC / DO modules, relay modules, load cells, ultrasonic sensors | Robu.in, Robocraze, ThinkRobotics, Sunrom Electronics, Amazon.in | AliExpress, Seeed Studio, Waveshare |",
          "| Motors, stepper drivers, wheels | Robu.in, Robocraze, local robotics shops | StepperOnline (omc-stepperonline.com) |",
          "| Li-ion / LiFePO4 cells and packs, solar panels, MPPT controllers | Authorised battery and solar dealers, Amazon.in (buy protected cells with an invoice) | not recommended by post (shipping rules for batteries) |",
          "| Laser-cut and 3D-printed parts | Local laser-cutting and 3D-printing shops (search IndiaMART, Justdial or maker spaces): send the SVG/DXF/STL from the repository and ask for a quote per piece | JLC3DP (jlc3dp.com), PCBWay 3D printing |",
          "| Fasteners, tubing, hardware, enclosures | Local hardware, Robu.in, Amazon.in | n/a |", "",
          "How to approach a vendor: send the project name, the exact file (BOM, CPL, Gerber ZIP, STL or SVG), the quantity, and ask for the price, the lead time, the GST invoice and the warranty or return terms. Keep the reply for your records.", ""]
    return "\n".join(L)

done = set()
for grp, rows in ROWS:
    for name, path, board, cav in rows:
        if not os.path.exists(os.path.join(ROOT, path, "MANUFACTURING_MANUAL.md")): continue
        open(os.path.join(ROOT, path, "ORDERING.md"), "w").write(doc_for(name, path, board, cav)); done.add(path)
print("wrote", len(done), "ORDERING.md files")
