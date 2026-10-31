"""Build schematic + routed 2-layer PCB + Gerbers + reports from a board spec (python module in boards/).
usage: python3 build.py seeti   (uses system python for pcbnew)"""
import sys, os, json, math, subprocess, importlib, shutil
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from pcbnew import FromMM as MM, ToMM
from sexp import FPDIR
from schematic import build_schematic
import route as R

def load_fp(spec):
    lib, name = spec.split(":"); fp = pcbnew.FootprintLoad(os.path.join(FPDIR, lib + ".pretty"), name)
    if fp is None: raise SystemExit(f"footprint not found: {spec}")
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    return fp
def build(modname, outdir):
    B = importlib.import_module("boards." + modname).BOARD
    os.makedirs(outdir, exist_ok=True); name = B["name"]; W, H = B["size"]
    parts = B["parts"]
    # ---------- schematic ----------
    build_schematic(name, parts, B["title"], os.path.join(outdir, name + ".kicad_sch"))
    # ---------- pcb ----------
    bd = pcbnew.BOARD(); nets = {}
    def net(n):
        if n not in nets: ni = pcbnew.NETINFO_ITEM(bd, n); bd.Add(ni); nets[n] = ni
        return nets[n]
    fps = {}
    for p in parts:
        fp = load_fp(p["fp"]); fp.SetReference(p["ref"]); fp.SetValue(p["value"]); fp.SetPosition(pcbnew.VECTOR2I(MM(p["x"]), MM(p["y"])))
        if p.get("side", "F") == "B": fp.Flip(fp.GetPosition(), False)
        fp.SetOrientationDegrees(p.get("rot", 0)); bd.Add(fp); fps[p["ref"]] = fp
        for pad in fp.Pads():
            n = p["nets"].get(pad.GetNumber())
            if n: pad.SetNet(net(n))
    # edge cuts (rounded rectangle approximated by a plain rectangle with 1 mm corner arcs omitted)
    def seg(a, b):
        s = pcbnew.PCB_SHAPE(bd); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); s.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); bd.Add(s)
    pts = [(0, 0), (W, 0), (W, H), (0, H)]
    for i in range(4): seg(pts[i], pts[(i + 1) % 4])
    # ---------- routing ----------
    rt = R.Router(W, H, width=B.get("trace", 0.25), clr=B.get("clr", 0.2), via_d=0.6, via_hole=0.3)
    rt.block_outside(0.3 + rt.w / 2)
    netid = {n: i for i, n in enumerate(sorted({n for p in parts for n in p["nets"].values() if n}))}
    pad_info = {}
    for ref, fp in fps.items():
        for pidx, pad in enumerate(fp.Pads()):
            bb = pad.GetBoundingBox(); x0, y0, x1, y1 = ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom())
            n = pad.GetNetname()
            attr = pad.GetAttribute()
            if attr == pcbnew.PAD_ATTRIB_NPTH:
                rt.block_rect(x0, y0, x1, y1, infl=0.5); continue
            layers = [0, 1] if attr == pcbnew.PAD_ATTRIB_PTH else ([1] if fp.GetLayer() == pcbnew.B_Cu else [0])
            if n:
                rt.add_pad(layers, x0, y0, x1, y1, netid[n]); pad_info[(ref, pad.GetNumber(), pidx)] = (n, layers, (x0, y0, x1, y1), (ToMM(pad.GetPosition().x), ToMM(pad.GetPosition().y)), attr == pcbnew.PAD_ATTRIB_PTH, pad.GetShape() == pcbnew.PAD_SHAPE_CIRCLE)
            else: rt.block_rect(x0, y0, x1, y1, layers)
    for (rx0, ry0, rx1, ry1) in B.get("keepout", []): rt.block_rect(rx0, ry0, rx1, ry1)
    order = {}
    for k, v in pad_info.items(): order.setdefault(v[0], []).append(k)
    def cells_in(bbox, layer, circle=False, ctr=None):
        x0, y0, x1, y1 = bbox; a = rt.cell(x0, y0); b = rt.cell(x1, y1); out = []
        for ix in range(a[0], b[0] + 1):
            for iy in range(a[1], b[1] + 1):
                x, y = rt.xy(ix, iy)
                if not (x0 <= x <= x1 and y0 <= y <= y1): continue
                if circle and math.hypot(x - ctr[0], y - ctr[1]) > (x1 - x0) / 2 - 0.1: continue
                out.append((layer, ix, iy))
        return out
    tracks = []; vias = []; failures = []
    def add_track(layer, a, b, nname):
        t = pcbnew.PCB_TRACK(bd); t.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); t.SetEnd(pcbnew.VECTOR2I(MM(b[0]), MM(b[1]))); t.SetWidth(MM(rt.w)); t.SetLayer(pcbnew.F_Cu if layer == 0 else pcbnew.B_Cu); t.SetNet(nets[nname]); bd.Add(t)
    def add_via(x, y, nname):
        v = pcbnew.PCB_VIA(bd); v.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y))); v.SetWidth(MM(0.6)); v.SetDrill(MM(0.3)); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(nets[nname]); bd.Add(v)
    gnd = "GND"
    sig = [n for n in order if n != gnd]; sig.sort(key=lambda n: (len(order[n]) > 3, B.get("route_order", {}).get(n, 0), len(order[n])))
    routed_cells = {}
    pw = [n for n in sig if n.startswith('+') or n in ('VBUS',)]; sig = [n for n in sig if n not in pw]
    first_nets = [n for n in B.get('first', []) if n in order]; pw = [n for n in pw if n not in first_nets]; sig = [n for n in sig if n not in first_nets]
    for n in first_nets + ([gnd] if gnd in order else []) + pw + sig:
        nid = netid[n]; pads = order[n]; done_cells = set()
        first = True
        for pk in pads:
            _, layers, bbox, ctr, tht, circ = pad_info[pk]
            starts = [c for l in layers for c in cells_in(bbox, l, circ, ctr) if rt._free(l, c[1], c[2], nid)]
            if not starts:
                failures.append((n, pk, "no free start cell")); continue
            if n == gnd and tht: continue                       # through-hole ground pads connect straight to the bottom pour
            if first and n != gnd:
                first = False; done_cells |= set(starts); continue
            first = False
            if n == gnd:
                path, via_end = rt.route(nid, starts, done_cells, goal_via=True)
            else:
                path, via_end = rt.route(nid, starts, done_cells)
            if path is None: failures.append((n, pk, "no route")); continue
            rt.commit(nid, path)
            if via_end:
                l, ix, iy = path[-1]; x, y = rt.xy(ix, iy); rt.vias.append((nid, x, y)); [rt._mark_rect(ll, x, y, x, y, nid, rt.r_via) for ll in (0, 1)]
            done_cells |= set(path) | set(starts)
            # emit copper: merge collinear moves
            segs = []; cur = path[0]; start = path[0]; d = None
            for a, b in zip(path, path[1:]):
                if a[0] != b[0]:
                    if start != a: segs.append((a[0], start, a))
                    vias.append((*rt.xy(a[1], a[2]), n)); start = b; d = None; continue
                dd = (b[1] - a[1], b[2] - a[2])
                if d is not None and dd != d:
                    segs.append((a[0], start, a)); start = a
                d = dd
            if start != path[-1]: segs.append((path[-1][0], start, path[-1]))
            for l, a, b in segs: add_track(l, rt.xy(a[1], a[2]), rt.xy(b[1], b[2]), n)
            # stub from pad centre to the first cell
            l0, ix0, iy0 = path[0]; add_track(l0, ctr, rt.xy(ix0, iy0), n)
            if via_end: vias.append((rt.xy(path[-1][1], path[-1][2])[0], rt.xy(path[-1][1], path[-1][2])[1], n)); 
            # NOTE: for goal-via nets the final cell becomes a via; for signal nets the path ends on an existing net cell
    for x, y, n in {(round(v[0], 3), round(v[1], 3), v[2]) for v in vias}: add_via(x, y, n)
    # a tie from non-first pads of a multi-pad signal net is only valid if the goal cell belongs to routed copper; connectivity is verified by DRC below.
    if "custom" in B: B["custom"](bd, nets, pcbnew, MM)
    # ---------- ground pour on the bottom layer ----------
    if gnd in nets:
        z = pcbnew.ZONE(bd); z.SetLayer(pcbnew.B_Cu); z.SetNet(nets[gnd]); z.SetMinThickness(MM(0.2)); z.SetLocalClearance(MM(0.25))
        ol = z.Outline(); ol.NewOutline()
        for x, y in ((0.3, 0.3), (W - 0.3, 0.3), (W - 0.3, H - 0.3), (0.3, H - 0.3)): ol.Append(MM(x), MM(y))
        bd.Add(z)
    # title text on silkscreen
    t = pcbnew.PCB_TEXT(bd); t.SetText(B["title"] + "  " + B.get("rev", "rev A")); t.SetPosition(pcbnew.VECTOR2I(MM(2), MM(H - 1.8))); t.SetLayer(pcbnew.F_SilkS); t.SetTextSize(pcbnew.VECTOR2I(MM(0.9), MM(0.9))); bd.Add(t)
    pcb_path = os.path.join(outdir, name + ".kicad_pcb"); bd.Save(pcb_path)
    bd = pcbnew.LoadBoard(pcb_path)                           # reload so the zone filler has a fully initialised board
    filler = pcbnew.ZONE_FILLER(bd); filler.Fill(bd.Zones()); bd.Save(pcb_path)
    json.dump({"failures": failures, "tracks": len([1 for _ in bd.GetTracks()])}, open(os.path.join(outdir, "route_report.json"), "w"), indent=1)
    return pcb_path, failures
if __name__ == "__main__" and len(sys.argv) == 2:
    mod = sys.argv[1]; out = os.path.join(os.path.dirname(__file__), "out", mod)
    p, f = build(mod, out); print("pcb:", p, "route failures:", f)

def post(modname):
    import re, xml.etree.ElementTree as ET
    B = importlib.import_module("boards." + modname).BOARD; name = B["name"]; out = os.path.join(os.path.dirname(__file__), "out", modname)
    pcb = os.path.join(out, name + ".kicad_pcb"); sch = os.path.join(out, name + ".kicad_sch"); rep = {}
    bd = pcbnew.LoadBoard(pcb)
    pcbnew.WriteDRCReport(bd, os.path.join(out, "drc.rpt"), pcbnew.EDA_UNITS_MILLIMETRES, True)
    txt = open(os.path.join(out, "drc.rpt")).read()
    m = re.search(r"\*\* Found (\d+) DRC violations \*\*", txt); u = re.search(r"\*\* Found (\d+) unconnected pads \*\*", txt); f = re.search(r"\*\* Found (\d+) Footprint errors \*\*", txt)
    rep["drc_violations"] = int(m.group(1)) if m else -1; rep["unconnected"] = int(u.group(1)) if u else -1; rep["footprint_errors"] = int(f.group(1)) if f else -1
    gdir = os.path.join(out, "gerbers"); os.makedirs(gdir, exist_ok=True)
    layers = "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts"
    subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "--layers", layers, "--output", gdir, pcb], capture_output=True)
    subprocess.run(["kicad-cli", "pcb", "export", "drill", "--output", gdir + "/", pcb], capture_output=True)
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "--output", os.path.join(out, name + "_cpl.csv"), "--format", "csv", "--units", "mm", pcb], capture_output=True)
    subprocess.run(["kicad-cli", "pcb", "export", "svg", "--layers", "F.Cu,B.Cu,F.SilkS,Edge.Cuts", "--output", os.path.join(out, name + "_board.svg"), "--page-size-mode", "2", pcb], capture_output=True)
    subprocess.run(["kicad-cli", "sch", "export", "pdf", "--output", os.path.join(out, name + "_schematic.pdf"), sch], capture_output=True)
    nl = os.path.join(out, name + ".net"); subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "kicadxml", "--output", nl, sch], capture_output=True)
    # netlist cross-check: schematic netlist vs. the spec used for the PCB
    spec = {}
    for p in B["parts"]:
        for pin, n in p["nets"].items():
            if n: spec.setdefault(n, set()).add((p["ref"], pin))
    got = {}
    if os.path.exists(nl):
        for netel in ET.parse(nl).getroot().iter("net"):
            nm = netel.get("name").lstrip("/")
            for node in netel.iter("node"): got.setdefault(nm, set()).add((node.get("ref"), node.get("pin")))
    got = {k: {x for x in v if not x[0].startswith("#")} for k, v in got.items()}
    got = {k: v for k, v in got.items() if not k.startswith('unconnected-')}
    mism = {n: (sorted(spec.get(n, set()) ^ got.get(n, set()))) for n in set(spec) | set(got) if spec.get(n, set()) != got.get(n, set())}
    rep["netlist_match"] = not mism; rep["netlist_mismatch"] = {k: v for k, v in list(mism.items())[:10]}
    rep["nets"] = len(spec); rep["parts"] = len(B["parts"]); rep["gerber_files"] = len(os.listdir(gdir))
    # BOM
    import csv
    with open(os.path.join(out, name + "_bom.csv"), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["Ref", "Value", "Footprint", "Symbol"]); [w.writerow([p["ref"], p["value"], p["fp"], p["sym"]]) for p in B["parts"]]
    json.dump(rep, open(os.path.join(out, "verification.json"), "w"), indent=1); return rep
if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "post":
    print(post(sys.argv[1]))
