"""Build all boards, run checks, and assemble release/<board>/ plus pcb/README.md. Run with system python3 (needs pcbnew); PNG renders use /tmp/venv cairosvg."""
import os, sys, json, shutil, subprocess, zipfile, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build
BOARDS = [("seeti", "Seeti Counter", "01-seeti-counter"), ("bijli", "Bijli Meter Reader", "04-bijli-meter-reader"), ("rain", "Rain Alert Bell (indoor unit)", "07-rain-alert"), ("rainplate", "Rain Alert Bell (rain plate)", "07-rain-alert")]
MPN = {"ATmega328P-AU": "Microchip ATmega328P-AU (TQFP-32)", "MCP6001": "Microchip MCP6001T-I/OT", "MMBT3904": "any SOT-23 NPN (MMBT3904)", "1N4148WS": "1N4148WS (SOD-323)", "100n": "0603 X7R 16 V", "10u": "0805 X5R 10 V", "1u": "0603 X7R 10 V", "10n": "0603 X7R 50 V",
       "Power": "slide switch SPDT (C&K PCM12-class)", "Target": "SMD tact switch (B3U-1000P-class)", "Mute": "SMD tact switch (B3U-1000P-class)", "Reset bill": "SMD tact switch (B3U-1000P-class)", "500mA PTC": "0805 PTC 0.5 A 6 V", "Micro-USB 5V": "Micro-USB B SMD receptacle (Amphenol 10118194-class)"}
summ = []
for mod, label, tool in BOARDS:
    out = os.path.join(HERE, "out", mod); build.build(mod, out); rep = build.post(mod)
    B = importlib.import_module("boards." + mod).BOARD; name = B["name"]
    rel = os.path.join(HERE, "release", mod); os.makedirs(rel, exist_ok=True)
    with zipfile.ZipFile(os.path.join(rel, name + "_gerbers.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(os.path.join(out, "gerbers"))): z.write(os.path.join(out, "gerbers", f), f)
    for ext in (".kicad_pcb", ".kicad_sch", "_schematic.pdf", "_cpl.csv", ".net"): shutil.copy(os.path.join(out, name + ext), rel)
    import csv
    with open(os.path.join(rel, name + "_bom.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Ref", "Value", "Footprint", "Suggested part (VERIFY availability/price)"])
        for p in B["parts"]: w.writerow([p["ref"], p["value"], p["fp"], MPN.get(p["value"], {"Device:R": "0603 1 % resistor", "Device:C": "0603 capacitor"}.get(p["sym"], p["value"]))])
    subprocess.run(["/tmp/venv/bin/python", "-c", f"import cairosvg; cairosvg.svg2png(url={os.path.join(out, name + '_board.svg')!r}, write_to={os.path.join(rel, name + '_board.png')!r}, output_width=1400)"])
    drc = open(os.path.join(out, "drc.rpt")).read(); import re, collections
    c = collections.Counter(m.group(2) for m in re.finditer(r"\[(\w+)\]: [^\n]*\n[^\n]*Severity: (\w+)", drc))
    summ.append((label, tool, B["size"], len(B["parts"]), rep["nets"], c.get("error", 0), rep["unconnected"], rep["netlist_match"], c.get("warning", 0)))
json.dump(summ, open(os.path.join(HERE, "release", "summary.json"), "w"), indent=1); print(summ)
