"""Silkscreen audit + re-placement on a finished board (post-route, geometry from the real pcbnew objects).
Reference texts go to the nearest spot (0/90 deg) that touches no top-side pad, via, hole, other silk, board edge,
and (preferred) no top-layer track. Reports anything it cannot place. usage: silkfix.py <outdir> [...]"""
import sys, os, glob, math, json
import numpy as np
import pcbnew
from pcbnew import FromMM as MM, ToMM
V = pcbnew.VECTOR2I
RES = 0.1
def rect(bb): return (ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom()))
class Grid:
    def __init__(s, W, H): s.n = (int(W / RES) + 2, int(H / RES) + 2); s.a = np.zeros(s.n, np.uint8)
    def mark(s, r, m=0.0):
        x0, y0, x1, y1 = r; i0 = max(0, int((x0 - m) / RES)); j0 = max(0, int((y0 - m) / RES)); i1 = min(s.n[0] - 1, int((x1 + m) / RES) + 1); j1 = min(s.n[1] - 1, int((y1 + m) / RES) + 1)
        s.a[i0:i1 + 1, j0:j1 + 1] = 1
    def free(s, r):
        x0, y0, x1, y1 = r
        if x0 < 0.5 or y0 < 0.5 or x1 > (s.n[0] - 2) * RES - 0.5 or y1 > (s.n[1] - 2) * RES - 0.5: return False
        return not s.a[int(x0 / RES):int(x1 / RES) + 2, int(y0 / RES):int(y1 / RES) + 2].any()
def fix(path, size=0.8, verbose=True):
    bd = pcbnew.LoadBoard(path); eb = bd.GetBoardEdgesBoundingBox(); W, H = ToMM(eb.GetRight()), ToMM(eb.GetBottom())
    hard = Grid(W, H); soft = Grid(W, H); fps = {f.GetReference(): f for f in bd.GetFootprints()}
    for ref, f in fps.items():
        for p in f.Pads():
            if p.IsOnLayer(pcbnew.F_Cu) or p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH: hard.mark(rect(p.GetBoundingBox()), 0.15)
            if p.GetDrillSize().x > 0: hard.mark(rect(p.GetBoundingBox()), 0.3)
    for t in bd.GetTracks():
        if t.GetClass() == "PCB_VIA": hard.mark(rect(t.GetBoundingBox()), 0.2)
        elif t.IsOnLayer(pcbnew.F_Cu):
            a, b = t.GetStart(), t.GetEnd(); L = max(1, int(math.hypot(b.x - a.x, b.y - a.y) / MM(0.1)))
            for k in range(L + 1):
                x = ToMM(a.x + (b.x - a.x) * k / L); y = ToMM(a.y + (b.y - a.y) * k / L); w = ToMM(t.GetWidth()) / 2
                soft.mark((x - w, y - w, x + w, y + w), 0.1)
    texts = [d for d in bd.GetDrawings() if d.GetLayer() == pcbnew.F_SilkS and d.GetClass() == "PCB_TEXT"]
    for d in bd.GetDrawings():
        if d.GetLayer() == pcbnew.F_SilkS and d not in texts: hard.mark(rect(d.GetBoundingBox()), 0.1)
    own = {}
    for ref, f in fps.items():
        own[ref] = []
        for g in f.GraphicalItems():
            if g.GetLayer() == pcbnew.F_SilkS and g.GetClass() != "FP_TEXT" and g.GetClass() != "PCB_TEXT": own[ref].append(rect(g.GetBoundingBox()))
    # mark every footprint silk graphic as hard obstacle (text must not sit on outlines)
    for ref, rs in own.items():
        for r in rs: hard.mark(r, 0.1)
    order = sorted(fps, key=lambda r: -len(list(fps[r].Pads())))
    unplaced = []; moved = 0
    for ref in order:
        f = fps[ref]; t = f.Reference()
        if ref.startswith(("H", "FID")) and (ref[1:].isdigit() or ref.startswith("FID")): t.SetVisible(False); continue
        t.SetVisible(True); t.SetTextSize(V(MM(size), MM(size))); t.SetTextThickness(MM(0.15)); t.SetLayer(pcbnew.F_SilkS if f.GetLayer() == pcbnew.F_Cu else pcbnew.B_SilkS)
        pads = [rect(p.GetBoundingBox()) for p in f.Pads()]
        fx0 = min(r[0] for r in pads); fy0 = min(r[1] for r in pads); fx1 = max(r[2] for r in pads); fy1 = max(r[3] for r in pads)
        for r in own[ref]: fx0 = min(fx0, r[0]); fy0 = min(fy0, r[1]); fx1 = max(fx1, r[2]); fy1 = max(fy1, r[3])
        cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
        # unmark own silk outline while testing (text may sit adjacent to it but not on it): keep marked, outlines are inside fp bbox
        best = None
        for ang in (0, 90):
            t.SetTextAngleDegrees(ang); t.SetPosition(V(MM(cx), MM(cy))); bb = rect(t.GetBoundingBox()); hw = (bb[2] - bb[0]) / 2; hh = (bb[3] - bb[1]) / 2; ox = (bb[0] + bb[2]) / 2 - cx; oy = (bb[1] + bb[3]) / 2 - cy
            R = int(7 / 0.25)
            for ix in range(-R, R + 1):
                for iy in range(-R, R + 1):
                    px, py = cx + ix * 0.25, cy + iy * 0.25; r = (px + ox - hw, py + oy - hh, px + ox + hw, py + oy + hh)
                    # must not overlap own footprint body box (pads+outline)
                    if r[0] < fx1 + 0.05 and r[2] > fx0 - 0.05 and r[1] < fy1 + 0.05 and r[3] > fy0 - 0.05: continue
                    if not hard.free(r): continue
                    gap = max(fx0 - r[2], r[0] - fx1, fy0 - r[3], r[1] - fy1, 0)
                    cost = gap + (0 if soft.free(r) else 3.0) + (0.15 if ang else 0)
                    if best is None or cost < best[0]: best = (cost, px, py, ang, r)
        if best is None or best[0] > 4.5:
            t.SetTextAngleDegrees(0); t.SetPosition(V(MM(cx), MM(cy))); bb = rect(t.GetBoundingBox())
            if len(pads) <= 3 and (fx1 - fx0) > 8 and not any(bb[0] < r[2] + .3 and bb[2] > r[0] - .3 and bb[1] < r[3] + .3 and bb[3] > r[1] - .3 for r in pads): hard.mark(bb, 0.1); moved += 1; continue
            unplaced.append(ref); t.SetTextAngleDegrees(0); t.SetPosition(V(MM(cx), MM(fy0 - 1.0))); continue
        _, px, py, ang, r = best; t.SetTextAngleDegrees(ang); t.SetPosition(V(MM(px), MM(py))); hard.mark(r, 0.1); moved += 1
    for d in texts:                                         # board-level labels (title, connector names): nearest clear spot, keep inside the board
        bb = rect(d.GetBoundingBox()); hw = (bb[2] - bb[0]) / 2; hh = (bb[3] - bb[1]) / 2; px0, py0 = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2; ox, oy = ToMM(d.GetPosition().x) - px0, ToMM(d.GetPosition().y) - py0
        best = None
        for ix in range(-80, 81):
            for iy in range(-80, 81):
                px, py = px0 + ix * 0.25, py0 + iy * 0.25; r = (px - hw, py - hh, px + hw, py + hh)
                if not hard.free(r): continue
                cost = math.hypot(ix, iy) + (0 if soft.free(r) else 6)
                if best is None or cost < best[0]: best = (cost, px, py, r)
        if best: d.SetPosition(V(MM(best[1] + ox), MM(best[2] + oy))); hard.mark(best[3], 0.1)
        else: unplaced.append(d.GetText())
    bd.Save(path)
    return {"placed": moved, "unplaced": unplaced}
if __name__ == "__main__":
    for d in sys.argv[1:]:
        p = glob.glob(os.path.join(d, "*.kicad_pcb"))[0]; r = fix(p); print(os.path.basename(d), r)
