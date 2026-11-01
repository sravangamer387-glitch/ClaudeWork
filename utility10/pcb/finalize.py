"""Post-route finishing on out/<board>: pour clearances, island stitching, dead-end stubs, silkscreen, DRC. usage: finalize.py <board>"""
import sys, os, glob, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew, islandfix, dangle, silkfix
from pcbnew import FromMM as MM
def run(mod):
    B = importlib.import_module("boards." + mod).BOARD; clr = B.get("clr", 0.2); d = os.path.join(HERE, "out", mod); p = glob.glob(d + "/*.kicad_pcb")[0]
    bd = pcbnew.LoadBoard(p); ds = bd.GetDesignSettings(); ds.m_NetSettings.m_DefaultNetClass.SetClearance(MM(clr)); ds.m_MinClearance = MM(clr)
    for z in bd.Zones():
        z.SetLocalClearance(MM(max(clr + 0.03, 0.18))); z.SetMinThickness(MM(0.15)); z.SetThermalReliefGap(MM(0.2)); z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(p)
    r = {"island_vias": islandfix.fix(p), "stubs_removed": dangle.fix(p)}; r["silk"] = silkfix.fix(p)
    bd = pcbnew.LoadBoard(p); rpt = os.path.join(d, "drc_final.rpt"); pcbnew.WriteDRCReport(bd, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
    import re, collections; c = collections.Counter(re.findall(r"^\[(\w+)\]", open(rpt).read(), re.M)); r["drc"] = dict(c); return r
if __name__ == "__main__":
    for m in sys.argv[1:]: print(m, run(m))
