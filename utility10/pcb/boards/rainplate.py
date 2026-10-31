from .common import *
W, H = 36, 58
def comb(bd, nets, pcbnew, MM):
    def trk(a, b, net, w=0.4):
        t = pcbnew.PCB_TRACK(bd); t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); t.SetWidth(MM(w)); t.SetLayer(pcbnew.F_Cu); t.SetNet(nets[net]); bd.Add(t)
    xa, xb, top, n = 4.0, 32.0, 6.0, 44
    trk((18, 50), (xa, 50), "DRV"); trk((xa, 50), (xa, top), "DRV")                                  # spine A (left)
    trk((18, 52.54), (xb, 52.54), "SENSE"); trk((xb, 52.54), (xb, top), "SENSE")                     # spine B (right)
    for k in range(n):
        y = top + 0.8 * k
        if k % 2 == 0: trk((xa, y), (xb - 4.5, y), "DRV")
        else: trk((xb, y), (xa + 4.5, y), "SENSE")
BOARD = dict(name="rain_plate", title="Rain plate (ENIG, gold fingers)", rev="rev A", size=(W, H), custom=comb, parts=[
 dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", value="Cable", x=18, y=50, rot=0, nets={"1": "DRV", "2": "SENSE"}),
])
