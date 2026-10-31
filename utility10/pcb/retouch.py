"""Silkscreen-only touch-up without re-routing: replaces the custom silk texts from the board spec in the existing .kicad_pcb, refills zones."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew
from pcbnew import FromMM as MM
def run(mod):
    B = importlib.import_module("boards." + mod).BOARD; path = os.path.join(HERE, "out", mod, B["name"] + ".kicad_pcb"); bd = pcbnew.LoadBoard(path)
    for d in list(bd.GetDrawings()):
        if d.GetClass() == "PCB_TEXT" and d.GetLayer() == pcbnew.F_SilkS: bd.Remove(d)
    for (txt, x, y, size) in B.get("silk", []):
        t = pcbnew.PCB_TEXT(bd); t.SetText(txt); t.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y))); t.SetLayer(pcbnew.F_SilkS); t.SetTextSize(pcbnew.VECTOR2I(MM(max(size, 0.8)), MM(max(size, 0.8)))); t.SetTextThickness(MM(0.16)); bd.Add(t)
    pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(path)
if __name__ == "__main__":
    for m in sys.argv[1:]: run(m)
