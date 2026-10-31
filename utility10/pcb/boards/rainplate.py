from .common import *
W, H = 38, 60
def comb(bd, nets, pcbnew, MM):
    def trk(a, b, net, w=0.4):
        t = pcbnew.PCB_TRACK(bd); t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); t.SetWidth(MM(w)); t.SetLayer(pcbnew.F_Cu); t.SetNet(nets[net]); bd.Add(t)
    xa, xb, top, n = 5.0, 33.0, 7.0, 44
    trk((19, 52), (xa, 52), "DRV", 0.6); trk((xa, 52), (xa, top), "DRV", 0.6)                       # spine A (left)
    trk((19, 54.54), (xb, 54.54), "SENSE", 0.6); trk((xb, 54.54), (xb, top), "SENSE", 0.6)          # spine B (right)
    for k in range(n):
        y = top + 0.8 * k
        if k % 2 == 0: trk((xa, y), (xb - 4.5, y), "DRV")
        else: trk((xb, y), (xa + 4.5, y), "SENSE")
    m = pcbnew.PCB_SHAPE(bd); m.SetShape(pcbnew.SHAPE_T_RECT); m.SetLayer(pcbnew.F_Mask); m.SetFilled(True); m.SetWidth(0); m.SetStart(pcbnew.VECTOR2I(MM(xa - 1.0), MM(top - 1.0))); m.SetEnd(pcbnew.VECTOR2I(MM(xb + 1.0), MM(top + 0.8 * n + 0.5))); bd.Add(m)      # mask opening over the whole comb (bare ENIG gold)
parts = [dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", value="Cable", x=19, y=52, rot=0, nets={"1": "DRV", "2": "SENSE"})]
S = dict(paper="A4", place={"J1": (100, 100, 0)}, blocks=[dict(title="RAIN PLATE: two interleaved comb electrodes (layout-only, ENIG)", x=40, y=60, w=140, h=90)],
 notes=[("Comb: 44 fingers, 0.4 mm trace / 0.4 mm gap on the top layer; spines 0.6 mm. Order ENIG; never cover the fingers with solder mask (mask opening over the whole comb).", 40, 170)])
BOARD = dict(name="rain_plate", title="Rain plate", rev="B", size=(W, H), corner=2.0, custom=comb, parts=parts, sch=S, supply={}, single_ok=("DRV", "SENSE"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[], widths={}, stitch=0, silk=[("RAIN PLATE rev B  ENIG", 5, 58.2, 0.9), ("DRV", 15.5, 49.5, 0.7), ("SENSE", 20.5, 49.5, 0.7)])
