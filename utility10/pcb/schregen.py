"""Regenerate only the schematic of a board (no re-routing): python3 schregen.py <board> [outdir]; renders PNG to /tmp/sch/<board>.png"""
import sys, os, importlib, subprocess, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sch2
mod = sys.argv[1]; B = importlib.import_module("boards." + mod).BOARD; out = os.path.join(HERE, "out", mod); os.makedirs("/tmp/sch", exist_ok=True)
S = copy.deepcopy(B["sch"]); sch2.build(B["name"], B["parts"], S, B["title"], B.get("rev", "A"), "2026-11-01", os.path.join(out, B["name"] + ".kicad_sch"))
print(mod, "fields still colliding:", S.get("_text_cost"))
if len(sys.argv) > 2:
    subprocess.run(["kicad-cli", "sch", "export", "svg", "-n", "-o", "/tmp/sch/" + mod, os.path.join(out, B["name"] + ".kicad_sch")], capture_output=True)
    f = [x for x in os.listdir("/tmp/sch/" + mod) if x.endswith(".svg")][0]; subprocess.run(["rsvg-convert", "-w", "3000", "-b", "white", f"/tmp/sch/{mod}/{f}", "-o", f"/tmp/sch/{mod}.png"])
