"""Re-add any hand pre-route segment (board spec B['pre']) that the stub clean-up removed, refill the pours. usage: prerestore.py <board>"""
import sys, os, glob, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew
from pcbnew import FromMM as MM, ToMM
def main(mod):
    B = importlib.import_module("boards." + mod).BOARD; pre = B.get("pre", [])
    if not pre: return 0
    p = glob.glob(os.path.join(HERE, "out", mod, "*.kicad_pcb"))[0]; bd = pcbnew.LoadBoard(p); nets = bd.GetNetsByName(); tracks = [t for t in bd.GetTracks() if t.GetClass() != "PCB_VIA"]; added = 0
    for pr in pre:
        layer = pcbnew.F_Cu if pr["layer"] == 0 else pcbnew.B_Cu
        for a, b in zip(pr["pts"], pr["pts"][1:]):
            have = any(t.GetLayer() == layer and t.GetNetname() == pr["net"] and ((abs(ToMM(t.GetStart().x) - a[0]) < 0.03 and abs(ToMM(t.GetStart().y) - a[1]) < 0.03 and abs(ToMM(t.GetEnd().x) - b[0]) < 0.03 and abs(ToMM(t.GetEnd().y) - b[1]) < 0.03) or (abs(ToMM(t.GetEnd().x) - a[0]) < 0.03 and abs(ToMM(t.GetEnd().y) - a[1]) < 0.03 and abs(ToMM(t.GetStart().x) - b[0]) < 0.03 and abs(ToMM(t.GetStart().y) - b[1]) < 0.03)) for t in tracks)
            if not have:
                t = pcbnew.PCB_TRACK(bd); t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); t.SetWidth(MM(pr.get("w", 0.2))); t.SetLayer(layer); t.SetNet(nets[pr["net"]]); bd.Add(t); added += 1
    bd.Save(p); print("pre-route segments restored:", added); return added
if __name__ == "__main__":
    n = main(sys.argv[1])
    if n:
        p = glob.glob(os.path.join(HERE, "out", sys.argv[1], "*.kicad_pcb"))[0]; bd = pcbnew.LoadBoard(p); pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(p)
