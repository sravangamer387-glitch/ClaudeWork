"""Arrange release/<board>/ into a clean, order-ready folder layout and write the manufacturing-readiness checklist into its README.
Returns the readiness dict (also saved as 5_verification/readiness.json)."""
import os, re, csv, json, shutil, zipfile
FOLDERS = {"1_fabrication": ("_gerbers.zip", "_fab_notes.pdf", "_copper.pdf"), "2_assembly": ("_JLC_BOM.csv", "_JLC_CPL.csv", "_BOM_full.csv", "_pos.csv", "_assembly_top.pdf"),
           "3_design": (".kicad_pcb", ".kicad_sch", ".kicad_pro", ".net", ".step", "_schematic.pdf", "_top.png", "_bottom.png", "fp-lib-table", "sym-lib-table"),
           "4_enclosure": ("_enclosure_base.stl", "_enclosure_lid.stl", "enclosure.json"), "5_verification": ("drc.rpt", "erc.txt", "verification.json")}
NEED = ["F_Cu", "B_Cu", "F_Mask", "B_Mask", "F_Silkscreen", "Edge_Cuts"]
def tidy(rel, name):
    for d, pats in FOLDERS.items():
        os.makedirs(os.path.join(rel, d), exist_ok=True)
        for f in sorted(os.listdir(rel)):
            p = os.path.join(rel, f)
            if os.path.isfile(p) and f != "README.md" and any(f.endswith(x) or f == x for x in pats): shutil.move(p, os.path.join(rel, d, f))
    for f in sorted(os.listdir(rel)):                                   # anything unclassified: do not leave stray files
        p = os.path.join(rel, f)
        if os.path.isfile(p) and f != "README.md": shutil.move(p, os.path.join(rel, "3_design", f))
    ver = json.load(open(os.path.join(rel, "5_verification", "verification.json")))
    z = zipfile.ZipFile(os.path.join(rel, "1_fabrication", name + "_gerbers.zip")); names = z.namelist()
    layers_ok = all(any(n_ in n for n in names) for n_ in NEED) and any(n.endswith(".drl") for n in names)
    bom = list(csv.DictReader(open(os.path.join(rel, "2_assembly", name + "_BOM_full.csv"))))
    real = [r for r in bom if r["Value"] != "TP"]; nolcsc = [r["Ref"] for r in real if not r["LCSC #"].strip()]; unver = [r["Ref"] for r in real if r["LCSC #"].strip() and r["LCSC status"] != "verified"]
    jb = list(csv.DictReader(open(os.path.join(rel, "2_assembly", name + "_JLC_BOM.csv")))); cpl = list(csv.DictReader(open(os.path.join(rel, "2_assembly", name + "_JLC_CPL.csv"))))
    nj = sum(len(r["Designator"].split(",")) for r in jb)
    rd = {"gerber_layers_and_drill_present": layers_ok, "drc_errors_0": ver["drc_errors"] == 0, "unconnected_0": ver["unconnected"] == 0, "netlist_matches_schematic": bool(ver["netlist_match"]),
          "erc_errors_0": not ver["erc_errors"], "independent_gerber_check_clean": not ver.get("gerber_independent_check", {}).get("errors", ["x"]), "every_part_has_lcsc_number": not nolcsc,
          "every_lcsc_number_verified": not unver, "cpl_rows_equal_jlc_bom_parts": nj == len(cpl), "step_model": os.path.exists(os.path.join(rel, "3_design", name + ".step")) and os.path.getsize(os.path.join(rel, "3_design", name + ".step")) > 20000, "drc_warnings": ver["drc_warnings"],
          "parts_without_lcsc": nolcsc, "parts_with_unverified_lcsc": unver}
    rd["order_ready"] = all(v for k, v in rd.items() if isinstance(v, bool))
    json.dump(rd, open(os.path.join(rel, "5_verification", "readiness.json"), "w"), indent=1)
    rp = os.path.join(rel, "README.md"); t = open(rp).read()
    t = re.sub(r"## Files\n.*?(?=\n## |\Z)", "## Files\n" + "\n".join(["`1_fabrication/` Gerber + drill zip (upload to JLCPCB/any fab), fab notes, copper plot", "`2_assembly/` JLC BOM + CPL (SMD parts JLC assembles), full BOM with LCSC numbers for every part, pick-and-place, assembly drawing",
          "`3_design/` KiCad 7 project (pcb, schematic, libs), netlist, STEP model, schematic PDF, renders", "`4_enclosure/` printable base and lid STL", "`5_verification/` DRC, ERC, verification and readiness reports"]) + "\n", t, flags=re.S)
    chk = ["", "## Manufacturing readiness (automatic check)", "", "| Check | Result |", "|---|---|"] + [f"| {k.replace('_', ' ')} | {'PASS' if v else 'FAIL'} |" for k, v in rd.items() if isinstance(v, bool) and k != "order_ready"] + \
          [f"| KiCad DRC warnings | {rd['drc_warnings']} |", f"| **Order ready** | **{'YES' if rd['order_ready'] else 'NO - see lists below'}** |"]
    if nolcsc: chk += ["", f"Parts with no LCSC number: {', '.join(nolcsc)}"]
    if unver: chk += ["", f"Parts whose LCSC number is not verified: {', '.join(unver)}"]
    chk += ["", "Order steps: (1) upload `1_fabrication/*_gerbers.zip`; (2) for assembly upload `2_assembly/*_JLC_BOM.csv` and `*_JLC_CPL.csv`, check the 3D/rotation preview for every polarised part (diodes, ICs, LEDs, electrolytics) because CPL rotations are generated, not hand-checked; (3) buy the through-hole parts listed in `*_BOM_full.csv` marked hand/THT and solder them; (4) re-check stock and the exact LCSC listing for every line before paying.", "",
            "Limits: the layout is software-generated and has not been reviewed by a PCB engineer; no prototype has been built; the first batch should be treated as a prototype run (order 5 boards)."]
    open(rp, "w").write(t.rstrip() + "\n" + "\n".join(chk) + "\n")
    return rd
