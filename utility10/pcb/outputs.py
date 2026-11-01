"""Verification and manufacturing outputs for a built board."""
import sys, os, json, re, csv, subprocess, importlib, collections, zipfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew, xml.etree.ElementTree as ET
def run(*a, env=None):
    e = dict(os.environ); e.update(env or {}); return subprocess.run(list(a), capture_output=True, text=True, env=e)
def post(modname):
    B = importlib.import_module("boards." + modname).BOARD; name = B["name"]; out = os.path.join(HERE, "out", modname)
    pcb = os.path.join(out, name + ".kicad_pcb"); sch = os.path.join(out, name + ".kicad_sch"); rep = json.load(open(os.path.join(out, "route_report.json")))
    bd = pcbnew.LoadBoard(pcb)
    pcbnew.WriteDRCReport(bd, os.path.join(out, "drc.rpt"), pcbnew.EDA_UNITS_MILLIMETRES, True)
    txt = open(os.path.join(out, "drc.rpt")).read()
    c = collections.Counter((m.group(1), m.group(2)) for m in re.finditer(r"\[(\w+)\]: [^\n]*\n[^\n]*Severity: (\w+)", txt))
    rep["drc"] = {f"{k[0]}:{k[1]}": v for k, v in c.items()}; rep["drc_errors"] = sum(v for k, v in c.items() if k[1] == "error"); rep["drc_warnings"] = sum(v for k, v in c.items() if k[1] == "warning")
    rep["drc_waived"] = {}
    if modname == "rainplate":                                   # intentional: the solder-mask opening spans both electrodes (bare gold comb); open finger ends are the design
        w1 = rep["drc"].pop("solder_mask_bridge:error", 0); w2 = rep["drc"].pop("track_dangling:warning", 0)
        rep["drc_errors"] -= w1; rep["drc_warnings"] -= w2; rep["drc_waived"] = {"solder_mask_bridge (intentional mask opening over the comb)": w1, "track_dangling (open comb finger ends)": w2}
    u = re.search(r"\*\* Found (\d+) unconnected pads \*\*", txt); rep["unconnected"] = int(u.group(1)) if u else -1
    gdir = os.path.join(out, "gerbers"); os.makedirs(gdir, exist_ok=True)
    run("kicad-cli", "pcb", "export", "gerbers", "--layers", "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts", "--output", gdir, pcb)
    run("kicad-cli", "pcb", "export", "drill", "--output", gdir + "/", "--drill-origin", "absolute", pcb)
    run("kicad-cli", "pcb", "export", "pos", "--output", os.path.join(out, name + "_pos.csv"), "--format", "csv", "--units", "mm", "--side", "both", pcb)
    run("kicad-cli", "pcb", "export", "svg", "--layers", "F.Cu,F.SilkS,Edge.Cuts", "--output", os.path.join(out, name + "_top.svg"), "--page-size-mode", "2", pcb)
    run("kicad-cli", "pcb", "export", "svg", "--layers", "B.Cu,B.SilkS,Edge.Cuts", "--mirror", "--output", os.path.join(out, name + "_bottom.svg"), "--page-size-mode", "2", pcb)
    run("kicad-cli", "pcb", "export", "pdf", "--layers", "F.Fab,F.SilkS,Edge.Cuts", "--output", os.path.join(out, name + "_assembly_top.pdf"), pcb)
    run("kicad-cli", "pcb", "export", "pdf", "--layers", "F.Cu,B.Cu,Edge.Cuts", "--output", os.path.join(out, name + "_copper.pdf"), pcb)
    run("kicad-cli", "sch", "export", "pdf", "--output", os.path.join(out, name + "_schematic.pdf"), sch)
    nl = os.path.join(out, name + ".net"); run("kicad-cli", "sch", "export", "netlist", "--format", "kicadxml", "--output", nl, sch)
    step = os.path.join(out, name + ".step"); run("kicad-cli", "pcb", "export", "step", "--subst-models", "--output", step, "--force", pcb, env={"KICAD7_3DMODEL_DIR": "/usr/share/kicad/3dmodels", "KICAD6_3DMODEL_DIR": "/usr/share/kicad/3dmodels"})
    rep["step"] = os.path.exists(step) and os.path.getsize(step) > 500000
    spec = {}
    for p in B["parts"]:
        for pin, n in p["nets"].items():
            if n: spec.setdefault(n, set()).add((p["ref"], pin))
    got = {}
    if os.path.exists(nl):
        for netel in ET.parse(nl).getroot().iter("net"):
            nm = netel.get("name").lstrip("/")
            if nm.startswith("unconnected-"): continue
            for node in netel.iter("node"):
                if not node.get("ref").startswith("#"): got.setdefault(nm, set()).add((node.get("ref"), node.get("pin")))
    spec_groups = {frozenset(v) for v in spec.values()}; got_groups = {frozenset(v) for v in got.values()}          # compare pin groups (power symbols create alias net names)
    mism = {str(sorted(g)[:3]) + "...": ("only in schematic" if g in got_groups else "only in PCB") for g in spec_groups ^ got_groups}
    names_missing = [n for n in spec if not any(spec[n] == v for v in got.values())]
    rep["netlist_match"] = not mism; rep["net_names_not_in_schematic"] = names_missing; rep["netlist_mismatch"] = dict(list(mism.items())[:8]); rep["nets"] = len(spec); rep["parts"] = len(B["parts"])
    import lcsc_fill; lcsc_fill.fill(B["parts"])
    # ---------- JLCPCB BOM / CPL ----------
    smd = {fp.GetReference(): bool(fp.GetAttributes() & pcbnew.FP_SMD) for fp in bd.GetFootprints()}
    groups = collections.OrderedDict()
    for p in B["parts"]:
        if not smd.get(p["ref"], False) or not p.get("lcsc"): continue
        groups.setdefault((p["value"], p["fp"].split(":")[1], p["lcsc"]), []).append(p["ref"])
    with open(os.path.join(out, name + "_JLC_BOM.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"]); [w.writerow([k[0], ",".join(v), k[1], k[2]]) for k, v in groups.items()]
    smd_refs = {r for v in groups.values() for r in v}
    with open(os.path.join(out, name + "_pos.csv")) as fh, open(os.path.join(out, name + "_JLC_CPL.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for row in csv.DictReader(fh):
            if row["Ref"] in smd_refs: w.writerow([row["Ref"], row["PosX"] + "mm", row["PosY"] + "mm", "Top" if row["Side"] == "top" else "Bottom", row["Rot"]])
    with open(os.path.join(out, name + "_BOM_full.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Ref", "Value", "Footprint", "Manufacturer part", "LCSC #", "LCSC status", "Assembly"]); 
        for p in B["parts"]: w.writerow([p["ref"], p["value"], p["fp"], p.get("mpn", ""), p.get("lcsc", ""), p.get("lcsc_status", "unverified" if p.get("lcsc") else ""), "SMT (JLC)" if smd.get(p["ref"]) and p.get("lcsc") else "hand/THT"])
    comps = {}
    for fp in bd.GetFootprints():
        pads = [p.GetBoundingBox() for p in fp.Pads()]
        if not pads: continue
        comps[fp.GetReference()] = dict(box=[min(pcbnew.ToMM(b.GetLeft()) for b in pads), min(pcbnew.ToMM(b.GetTop()) for b in pads), max(pcbnew.ToMM(b.GetRight()) for b in pads), max(pcbnew.ToMM(b.GetBottom()) for b in pads)],
                                         cx=pcbnew.ToMM(fp.GetPosition().x), cy=pcbnew.ToMM(fp.GetPosition().y), fp=str(fp.GetFPID().GetLibItemName()))
    json.dump(comps, open(os.path.join(out, "components.json"), "w"), indent=1)
    json.dump(rep, open(os.path.join(out, "verification.json"), "w"), indent=1); return rep
if __name__ == "__main__":
    r = post(sys.argv[1]); print(json.dumps({k: v for k, v in r.items() if k in ("drc_errors", "drc_warnings", "unconnected", "netlist_match", "step", "route_failures", "pin_pad_mismatch", "erc_errors", "stitch_vias", "silk_unplaced", "drc")}, indent=1))
