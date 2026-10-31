"""Fast placement check (seconds): courtyard overlaps, parts too near the board edge or mounting holes."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew
from pcbnew import FromMM as MM, ToMM
from build import load_fp
V = pcbnew.VECTOR2I
def check(modname, verbose=True):
    B = importlib.import_module("boards." + modname).BOARD; W, H = B["size"]; boxes = {}; tmp = pcbnew.BOARD()
    items = list(B["parts"]) + [dict(ref=f"H{i}", fp="MountingHole:MountingHole_2.7mm_M2.5", x=x, y=y, rot=0) for i, (x, y) in enumerate(B.get("holes", []), 1)] + [dict(ref=f"FID{i}", fp="Fiducial:Fiducial_1mm_Mask2mm", x=x, y=y, rot=0) for i, (x, y) in enumerate(B.get("fids", []), 1)]
    for p in items:
        fp = load_fp(p["fp"]); fp.SetPosition(V(MM(p["x"]), MM(p["y"])))
        if p.get("side", "F") == "B": fp.Flip(fp.GetPosition(), False)
        fp.SetOrientationDegrees(p.get("rot", 0)); tmp.Add(fp); fp.BuildCourtyardCaches()
        cy = fp.GetCourtyard(pcbnew.F_CrtYd) if p.get("side", "F") == "F" else fp.GetCourtyard(pcbnew.B_CrtYd); bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False, False)
        r = (ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom()))
        if p["ref"].startswith("H"): r = (p["x"] - 3.2, p["y"] - 3.2, p["x"] + 3.2, p["y"] + 3.2)          # screw-head keep-out
        boxes[p["ref"]] = r
    issues = []
    refs = list(boxes)
    for i, a in enumerate(refs):
        x0, y0, x1, y1 = boxes[a]
        if not a.startswith(("H", "FID")) and (x0 < 0.8 or y0 < 0.8 or x1 > W - 0.8 or y1 > H - 0.8) and a not in B.get("edge_ok", ()): issues.append(f"{a} courtyard ({x0:.1f},{y0:.1f},{x1:.1f},{y1:.1f}) closer than 0.8 mm to the board edge")
        for b in refs[i + 1:]:
            u0, v0, u1, v1 = boxes[b]
            if x0 < u1 and u0 < x1 and y0 < v1 and v0 < y1: issues.append(f"{a} overlaps {b}")
    if verbose:
        if "--boxes" in sys.argv: [print(f"  {k:5s} x {v[0]:5.1f}..{v[2]:5.1f}  y {v[1]:5.1f}..{v[3]:5.1f}") for k, v in boxes.items()]
        print("placement issues:", len(issues)); print(*issues, sep="\n")
    return issues
if __name__ == "__main__": check(sys.argv[1])
