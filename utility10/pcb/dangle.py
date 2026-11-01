"""Remove dead-end copper stubs using KiCad's own DRC 'track_dangling' report (never guesses connectivity). usage: dangle.py <outdir>..."""
import sys, glob, os, re
import pcbnew
from pcbnew import FromMM as MM, ToMM
def fix(path, rounds=6):
    total = 0
    for _ in range(rounds):
        bd = pcbnew.LoadBoard(path); rpt = path + ".dangle.rpt"; pcbnew.WriteDRCReport(bd, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
        pts = [(float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)) for m in re.finditer(r"\[track_dangling\][^\n]*\n[^\n]*\n\s+@\(([-\d.]+) mm, ([-\d.]+) mm\): Track \[([^\]]*)\] on ([A-Za-z.]+)", open(rpt).read())]
        os.remove(rpt)
        if not pts: break
        victims = []
        for (x, y, net, lay) in pts:
            for t in bd.GetTracks():
                if t.GetClass() == "PCB_VIA" or t.GetNetname() != net or t.GetLayerName() != lay: continue
                if any(abs(ToMM(e.x) - x) < 0.02 and abs(ToMM(e.y) - y) < 0.02 for e in (t.GetStart(), t.GetEnd())): victims.append(t); break
        if not victims: break
        for t in victims: bd.Remove(t)
        total += len(victims); bd.Save(path)
    bd = pcbnew.LoadBoard(path); pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(path); return total
if __name__ == "__main__":
    for d in sys.argv[1:]: print(d, fix(glob.glob(os.path.join(d, "*.kicad_pcb"))[0]))
