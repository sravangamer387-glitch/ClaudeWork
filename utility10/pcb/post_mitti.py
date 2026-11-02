"""MITTI-NETRA finishing step after finalize/dangle: restore the hand-routed SCL escape (dangle.py can remove it) and refill zones.
usage: python3 post_mitti.py   (then package.py mitti)"""
import pcbnew, glob
from pcbnew import FromMM as MM
f = glob.glob("out/mitti/*.kicad_pcb")[0]; b = pcbnew.LoadBoard(f); net = b.FindNet("SCL")
have = {(round(t.GetStart().x / 1e6, 2), round(t.GetStart().y / 1e6, 2), round(t.GetEnd().x / 1e6, 2), round(t.GetEnd().y / 1e6, 2)) for t in b.GetTracks() if t.GetClass() != "PCB_VIA" and t.GetNetname() == "SCL"}
for seg in [(62, 48, 62, 44.4), (62, 44.4, 71, 44.4)]:
    if seg in have or (seg[2], seg[3], seg[0], seg[1]) in have: continue
    t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(MM(seg[0]), MM(seg[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(seg[2]), MM(seg[3]))); t.SetWidth(MM(0.2)); t.SetLayer(pcbnew.F_Cu); t.SetNet(net); b.Add(t); print("restored", seg)
pcbnew.ZONE_FILLER(b).Fill(b.Zones()); b.Save(f)
import subprocess, sys; subprocess.run([sys.executable, "fixisland.py", "mitti"])   # the restored SCL trace can isolate the C9 ground pad: re-stitch
b = pcbnew.LoadBoard(f)
b = pcbnew.LoadBoard(f); pcbnew.WriteDRCReport(b, "/tmp/mitti_drc.rpt", pcbnew.EDA_UNITS_MILLIMETRES, True)
t = open("/tmp/mitti_drc.rpt").read(); import re; print(re.findall(r"Found (\d+) (DRC violations|unconnected pads)", t))
