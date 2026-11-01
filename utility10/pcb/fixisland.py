"""Give every F.Cu ground-pour island that holds an SMD GND pad but no via a stitching via (0.6/0.3), keeping the DRC at least as clean. usage: fixisland.py <board>"""
import sys, glob, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
import pcbnew
from pcbnew import ToMM as T, FromMM as MM
def drc(bd, path):
    pcbnew.WriteDRCReport(bd, path, pcbnew.EDA_UNITS_MILLIMETRES, True); t = open(path).read()
    return len(re.findall(r"^\[(?!unconnected)\w+\]", t, re.M)), len(re.findall(r"^\[unconnected", t, re.M))
def islands(bd):
    vias = [v for v in bd.GetTracks() if v.GetClass() == "PCB_VIA" and v.GetNetname() == "GND"]
    z = [z for z in bd.Zones() if z.GetNetname() == "GND" and z.GetFirstLayer() == pcbnew.F_Cu][0]; ps = z.GetFilledPolysList(pcbnew.F_Cu); out = []
    for i in range(ps.OutlineCount()):
        o = ps.Outline(i); pads = [pd for f in bd.GetFootprints() for pd in f.Pads() if pd.GetNetname() == "GND" and pd.GetAttribute() == pcbnew.PAD_ATTRIB_SMD and o.PointInside(pd.GetPosition())]
        if pads and not any(o.PointInside(v.GetPosition()) for v in vias): out.append((o, pads))
    return z, out
def main(mod):
    p = glob.glob(os.path.join(HERE, "out", mod, "*.kicad_pcb"))[0]; fixed = 0
    for rnd in range(8):
        bd = pcbnew.LoadBoard(p); z, isl = islands(bd)
        if not isl: break
        o, pads = isl[0]; base = drc(bd, "/tmp/fi.rpt"); pc = pads[0].GetPosition(); px, py = T(pc.x), T(pc.y); bb = o.BBox()
        items = [t for t in bd.GetTracks() if t.GetNetname() != "GND"] + [pd for f in bd.GetFootprints() for pd in f.Pads() if pd.GetNetname() != "GND"]
        cands = []; x = T(bb.GetX())
        while x <= T(bb.GetX() + bb.GetWidth()):
            y = T(bb.GetY())
            while y <= T(bb.GetY() + bb.GetHeight()):
                pt = pcbnew.VECTOR2I(MM(x), MM(y))
                if z.HitTestFilledArea(pcbnew.F_Cu, pt, 0) and o.PointInside(pt) and not any(i.HitTest(pt, MM(0.45)) for i in items): cands.append(((x - px) ** 2 + (y - py) ** 2, round(x, 2), round(y, 2)))
                y += 0.05
            x += 0.05
        cands.sort(); ok = False
        for _, x, y in cands[:40]:
            bd = pcbnew.LoadBoard(p); v = pcbnew.PCB_VIA(bd); v.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y))); v.SetWidth(MM(0.6)); v.SetDrill(MM(0.3)); v.SetNet(bd.GetNetsByName()["GND"]); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); bd.Add(v)
            pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); r = drc(bd, "/tmp/fi.rpt")
            if r[0] <= base[0] and r[1] <= base[1]: bd.Save(p); print("via", x, y, base, "->", r); fixed += 1; ok = True; break
        if not ok: print("no spot for island at", round(px, 1), round(py, 1)); break
    print(mod, "islands fixed:", fixed)
if __name__ == "__main__": main(sys.argv[1])
