"""Remove stitching vias that DRC reports as dangling (not connected on both layers), refill the pours, save. Repeat until stable."""
import sys, os, re, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew
from pcbnew import ToMM
def run(mod):
    B = importlib.import_module("boards." + mod).BOARD; path = os.path.join(HERE, "out", mod, B["name"] + ".kicad_pcb"); removed = 0
    for _ in range(4):
        bd = pcbnew.LoadBoard(path)
        for z in bd.Zones():
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
            if z.GetLayer() == pcbnew.F_Cu: z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)          # top pour: solid pad connection (no starved thermal spokes)
        pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(path); bd = pcbnew.LoadBoard(path); rpt = os.path.join(HERE, "out", mod, "_prune.rpt"); pcbnew.WriteDRCReport(bd, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
        txt = open(rpt).read(); pts = [(float(m.group(1)), float(m.group(2))) for m in re.finditer(r"\[via_dangling\][^\n]*\n[^\n]*\n\s+@\(([-\d.]+) mm, ([-\d.]+) mm\): Via \[GND\]", txt)]
        if not pts: break
        for t in list(bd.GetTracks()):
            if t.GetClass() == "PCB_VIA" and any(abs(ToMM(t.GetPosition().x) - x) < 0.02 and abs(ToMM(t.GetPosition().y) - y) < 0.02 for x, y in pts): bd.Remove(t); removed += 1
        pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(path)
    os.path.exists(os.path.join(HERE, "out", mod, "_prune.rpt")) and os.remove(os.path.join(HERE, "out", mod, "_prune.rpt"))
    return removed
if __name__ == "__main__": print(run(sys.argv[1]))
