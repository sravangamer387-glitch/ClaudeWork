"""Priced BOM for every released board from live LCSC data (wmsc.lcsc.com product detail API).
usage: python3 costing.py [--refresh]   -> costing/prices_lcsc.json, costing/<board>_priced_BOM.csv, costing/BOM_COSTS.md
Assumptions are explicit constants below. Prices are LCSC list ladder prices (USD) at the time of the run, parts only."""
import csv, glob, json, os, sys, time, subprocess, datetime, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "costing"); os.makedirs(OUT, exist_ok=True)
INR_PER_USD = 88.0                       # ASSUMPTION: change to today's rate
QTYS = (1, 10, 100)                      # number of boards per order for the break-up
PCB_FAB_USD = {"small": 2.0, "large": 8.0}   # ASSUMPTION: JLC standard 2-layer 5 pcs, <=100x100 mm / larger; per ORDER, not per board
ASSY_SETUP_USD = 8.0                     # ASSUMPTION: JLC economic assembly setup, per order
CACHE = os.path.join(OUT, "prices_lcsc.json")
boards = sorted(os.path.basename(p) for p in glob.glob(os.path.join(HERE, "release", "*")) if os.path.isdir(p))
lines = {}                                # board -> list of dict
for b in boards:
    f = glob.glob(os.path.join(HERE, "release", b, "2_assembly", "*_BOM_full.csv"))
    if not f: continue
    rows = list(csv.DictReader(open(f[0])))
    g = collections.OrderedDict()
    for r in rows:
        k = (r["LCSC #"], r["Value"], r["Manufacturer part"], r["Assembly"]); g.setdefault(k, []).append(r["Ref"])
    lines[b] = [dict(lcsc=k[0], value=k[1], mpn=k[2], assembly=k[3], refs=v) for k, v in g.items()]
codes = sorted({l["lcsc"] for v in lines.values() for l in v if l["lcsc"].startswith("C")})
cache = json.load(open(CACHE)) if os.path.exists(CACHE) and "--refresh" not in sys.argv else {}
for c in codes:
    if c in cache: continue
    out = subprocess.run(["curl", "-s", "-m", "30", f"https://wmsc.lcsc.com/ftps/wm/product/detail?productCode={c}"], capture_output=True, text=True).stdout
    try:
        r = json.loads(out)["result"]
        cache[c] = dict(model=r.get("productModel"), brand=r.get("brandNameEn"), pkg=r.get("encapStandard"), stock=r.get("stockNumber"), minbuy=r.get("minBuyNumber"),
                        ladder=[(p["ladder"], p["usdPrice"]) for p in r.get("productPriceList") or []], fetched=datetime.date.today().isoformat())
    except Exception as e:
        cache[c] = dict(error=str(e)[:80], fetched=datetime.date.today().isoformat())
    time.sleep(0.25)
json.dump(cache, open(CACHE, "w"), indent=1)
def unit(c, qty):
    d = cache.get(c) or {}; lad = d.get("ladder") or []
    if not lad: return None
    q = max(qty, d.get("minbuy") or 1); p = lad[0][1]
    for (l, pr) in lad:
        if q >= l: p = pr
    return p
size = {}
for b in boards:
    pcb = glob.glob(os.path.join(HERE, "release", b, "3_design", "*.kicad_pcb"))
    area = 0
    if pcb:
        import re; t = open(pcb[0]).read(); m = re.search(r'\(general[^)]*\)', t)
    size[b] = "large" if b in ("kinetic_ctl", "biotray", "mitti", "jalnetra", "arcade", "prayog", "kheti", "beatrunner") else "small"
md = ["# Priced bills of materials (parts, live LCSC list prices)", "", f"Generated {datetime.date.today().isoformat()} by `utility10/pcb/costing.py` from each board's `2_assembly/*_BOM_full.csv` and the LCSC product API. USD list prices, ladder price for the quantity bought; INR at an assumed **{INR_PER_USD:.0f} INR/USD**.", "",
      "**What is and is not in the numbers:** parts only. Not included: bare PCB fabrication, assembly fees (setup, extended-part fees, placement), stencil, shipping, import duty and GST, cell/battery, enclosure, bought-in modules and cables. Planning figures for PCB and assembly are shown separately and are assumptions, not quotes: get a JLC quote before you order. Stock is as returned by LCSC on the run date and changes daily.", ""]
summary = []
for b in boards:
    if b not in lines: continue
    rows = []; tot = {q: 0.0 for q in QTYS}; flags = []
    for l in lines[b]:
        c = l["lcsc"]; n = len(l["refs"]); d = cache.get(c, {})
        if not c.startswith("C") or not d.get("ladder"):
            rows.append([",".join(l["refs"]), n, l["value"], l["mpn"], c, "", "", "", "", "no LCSC price (hand-fit or not priced)"]); continue
        pq = {q: unit(c, n * q) for q in QTYS}
        for q in QTYS: tot[q] += pq[q] * n * q
        stock = d.get("stock") or 0; note = ""
        if stock < n * 100: note = "LOW STOCK" if stock > 0 else "OUT OF STOCK"; flags.append(f"{c} {l['value']} ({note.lower()}, stock {stock})")
        rows.append([",".join(l["refs"]), n, l["value"], l["mpn"], c, f"{pq[1]:.4f}", f"{pq[1]*n:.3f}", f"{pq[100]:.4f}", stock, note])
    with open(os.path.join(OUT, f"{b}_priced_BOM.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Refs", "Qty/board", "Value", "Manufacturer part", "LCSC #", "Unit USD (1 board)", "Line USD (1 board)", "Unit USD (100 boards)", "LCSC stock", "Note"]); w.writerows(rows)
        w.writerow([]); w.writerow(["TOTAL parts per board, USD", "", "", "", "", "1 board: %.2f" % tot[1], "10 boards: %.2f" % (tot[10] / 10), "100 boards: %.2f" % (tot[100] / 100)])
    fab = PCB_FAB_USD[size[b]]
    per = {q: tot[q] / q for q in QTYS}
    summary.append((b, len(lines[b]), sum(len(l["refs"]) for l in lines[b]), per, fab, flags))
md += ["## Summary: parts cost per assembled board", "", "| Board | Lines | Parts | 1 board USD | 1 board INR | 10 boards (each) USD | 100 boards (each) USD | 100 boards (each) INR | PCB fab planning (per order of 5) | Stock flags |", "|---|---|---|---|---|---|---|---|---|---|"]
for (b, nl, npart, per, fab, flags) in summary:
    md.append(f"| {b} | {nl} | {npart} | {per[1]:.2f} | {per[1]*INR_PER_USD:.0f} | {per[10]:.2f} | {per[100]:.2f} | {per[100]*INR_PER_USD:.0f} | US${fab:.0f} | {len(flags) or 'none'} |")
md += ["", "Per-board file: `costing/<board>_priced_BOM.csv` (every line with LCSC number, unit price, stock).", "", "## Stock flags (fewer than 100 boards' worth in stock, or zero)", ""]
for (b, nl, npart, per, fab, flags) in summary:
    for fl in flags: md.append(f"- **{b}**: {fl}")
md += ["", "## Planning assumptions (not quotes)", "", f"- PCB fabrication: about US${PCB_FAB_USD['small']:.0f} (small) to US${PCB_FAB_USD['large']:.0f} (large) per order of 5 boards at a standard 2-layer, 1.6 mm spec; ENIG, 2 oz copper or other options cost more.", f"- JLC assembly: about US${ASSY_SETUP_USD:.0f} setup per order plus per-part placement and a per-unique-part fee for extended parts; with many unique parts this can exceed the parts cost for 1 to 10 boards.", "- Through-hole connectors listed as hand-soldered are in the parts total but not in the assembly fee.", ""]
open(os.path.join(OUT, "BOM_COSTS.md"), "w").write("\n".join(md)); print("done", len(codes), "parts", len(summary), "boards")
