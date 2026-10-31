"""Rebuild only the schematic from the board spec (no re-routing)."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sch2
for m in sys.argv[1:]:
    B = importlib.import_module("boards." + m).BOARD; sch2.build(B["name"], B["parts"], B["sch"], B["title"], B.get("rev", "A"), "2026-11-01", os.path.join(HERE, "out", m, B["name"] + ".kicad_sch"))
