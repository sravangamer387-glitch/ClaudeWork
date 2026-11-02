"""Post-process built boards: verification, fab outputs, enclosure, docs; assemble release/<board>/ (run build.py <board> first)."""
import os, sys, shutil, subprocess, zipfile, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import outputs, docgen
BOARDS = sys.argv[1:] or ["seeti", "bijli", "rain", "rainplate", "fridge", "chulha", "tap", "bijlilog", "gastaraju", "arcade", "kheti", "jalnetra", "prayog", "beatrunner", "astradand", "kinetic_ctl", "kinetic_vib", "biotray", "mitti", "biowatt", "gassuraksha", "jalrakshak", "ap1"]
summary = []
for mod in BOARDS:
    if mod != "rainplate": subprocess.run([sys.executable, os.path.join(HERE, "prune.py"), mod], capture_output=True, text=True)
    rep = outputs.post(mod)
    subprocess.run(["/tmp/venv/bin/python", os.path.join(HERE, "enclosure.py"), mod], capture_output=True, text=True)
    subprocess.run(["/tmp/venv/bin/python", os.path.join(HERE, "fabdoc.py"), mod], capture_output=True, text=True)
    gc = subprocess.run(["/tmp/venv/bin/python", "-W", "ignore", os.path.join(HERE, "gerbercheck.py"), mod], capture_output=True, text=True).stdout.strip()
    try: rep["gerber_independent_check"] = eval(gc.split(" ", 1)[1])
    except Exception: rep["gerber_independent_check"] = {"errors": [gc[:200]]}
    json.dump(rep, open(os.path.join(HERE, "out", mod, "verification.json"), "w"), indent=1)
    docgen.gen(mod)
    out = os.path.join(HERE, "out", mod); rel = os.path.join(HERE, "release", mod)
    if os.path.exists(rel): shutil.rmtree(rel)
    os.makedirs(rel)
    import importlib; name = importlib.import_module("boards." + mod).BOARD["name"]
    with zipfile.ZipFile(os.path.join(rel, name + "_gerbers.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(os.path.join(out, "gerbers"))): z.write(os.path.join(out, "gerbers", f), f)
    for f in os.listdir(out):
        p = os.path.join(out, f)
        if os.path.isfile(p) and f.split(".")[-1] in ("kicad_pcb", "kicad_sch", "kicad_pro", "pdf", "csv", "step", "stl", "md", "net", "txt", "rpt", "json") and f not in ("route_report.json", "components.json", "view.svg"): shutil.copy(p, rel)
    for f in ("fp-lib-table", "sym-lib-table"): shutil.copy(os.path.join(out, f), rel)
    subprocess.run(["/tmp/venv/bin/python", "-c", f"import cairosvg; cairosvg.svg2png(url={os.path.join(out, name + '_top.svg')!r}, write_to={os.path.join(rel, name + '_top.png')!r}, output_width=1600); cairosvg.svg2png(url={os.path.join(out, name + '_bottom.svg')!r}, write_to={os.path.join(rel, name + '_bottom.png')!r}, output_width=1600)"])
    import release_tidy; rd = release_tidy.tidy(rel, name)
    summary.append(dict(board=name, mod=mod, drc_errors=rep["drc_errors"], drc_warnings=rep["drc_warnings"], unconnected=rep["unconnected"], netlist=rep["netlist_match"], erc_errors=len(rep["erc_errors"]), failures=len(rep["route_failures"]), parts=rep["parts"], nets=rep["nets"], order_ready=rd["order_ready"]))
old = {}
sp = os.path.join(HERE, "release", "summary.json")
if os.path.exists(sp):
    for x in json.load(open(sp)): old[x["mod"]] = x
for x in summary: old[x["mod"]] = x
order = ["seeti", "bijli", "rain", "rainplate", "fridge", "chulha", "tap", "bijlilog", "gastaraju", "arcade", "kheti", "jalnetra", "prayog", "beatrunner", "astradand", "kinetic_ctl", "kinetic_vib", "biotray", "mitti", "biowatt", "gassuraksha", "jalrakshak", "ap1"]
summary = [old[m] for m in order if m in old]
json.dump(summary, open(sp, "w"), indent=1); print(json.dumps(summary, indent=1))
