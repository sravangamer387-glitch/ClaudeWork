"""Stitch every isolated top-layer GND pour island to the bottom GND pour with a via (post-route, geometry from the filled zones).
usage: islandfix.py <out dir> ; returns number of vias added; run before the final fill is trusted (it refills itself)."""
import sys, glob, os, math
import pcbnew
from pcbnew import FromMM as MM, ToMM
V = pcbnew.VECTOR2I
def inside(poly, x, y, r):
    for k in range(8):
        a = k * math.pi / 4
        if not poly.Collide(V(MM(x + r * math.cos(a)), MM(y + r * math.sin(a))), 0): return False
    return poly.Collide(V(MM(x), MM(y)), 0)
def fix(path, gndname="GND", rounds=4):
    added = 0
    for rnd in range(rounds):
        relax = rnd >= 2                       # last rounds: smaller via (0.5/0.25, JLC minimum 0.45/0.2) and tighter fit
        vd, vr = (0.5, 0.42) if relax else (0.6, 0.55)
        bd = pcbnew.LoadBoard(path); pcbnew.ZONE_FILLER(bd).Fill(bd.Zones())
        zs = {z.GetLayer(): z for z in bd.Zones() if z.GetNetname() == gndname}
        if pcbnew.F_Cu not in zs or pcbnew.B_Cu not in zs: return added
        polys = {pcbnew.F_Cu: zs[pcbnew.F_Cu].GetFilledPolysList(pcbnew.F_Cu), pcbnew.B_Cu: zs[pcbnew.B_Cu].GetFilledPolysList(pcbnew.B_Cu)}
        # connectivity: island is OK if a GND via already lands inside it
        vias = [t for t in bd.GetTracks() if t.GetClass() == "PCB_VIA" and t.GetNetname() == gndname]
        n = 0; net = zs[pcbnew.F_Cu].GetNet()
        for lay, other in ((pcbnew.F_Cu, pcbnew.B_Cu), (pcbnew.B_Cu, pcbnew.F_Cu)):
          top = polys[lay]; bot = polys[other]
          for i in range(top.OutlineCount()):
            o = top.Outline(i); bb = o.BBox(); area = abs(o.Area()) / 1e12
            if area < (0.3 if relax else 1.0): continue
            single = pcbnew.SHAPE_POLY_SET(); single.AddOutline(o)
            if any(single.Collide(v.GetPosition(), 0) for v in vias): continue
            if i == 0 and area > 1500: continue
            x0, y0, x1, y1 = [ToMM(v) for v in (bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom())]
            cands = []; x = x0
            while x <= x1:
                y = y0
                while y <= y1:
                    cands.append((x, y)); y += 0.3
                x += 0.3
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; cands.sort(key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
            for (x, y) in cands:
                if inside(single, x, y, vr) and inside(bot, x, y, vr):
                    v = pcbnew.PCB_VIA(bd); v.SetPosition(V(MM(x), MM(y))); v.SetWidth(MM(vd)); v.SetDrill(MM(vd / 2)); v.SetNet(net); v.SetViaType(pcbnew.VIATYPE_THROUGH); bd.Add(v); n += 1; break
        if n == 0 and relax: break
        added += n; bd.Save(path)
    bd = pcbnew.LoadBoard(path); pcbnew.ZONE_FILLER(bd).Fill(bd.Zones()); bd.Save(path)
    return added
if __name__ == "__main__":
    for d in sys.argv[1:]: print(d, fix(glob.glob(os.path.join(d, "*.kicad_pcb"))[0]))
