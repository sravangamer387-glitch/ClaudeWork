"""PCB toolchain v2. usage: python3 build.py <board>            (build everything for one board spec in boards/)
Pipeline: ERC on spec -> readable schematic -> placement -> routing (own router + pre-routes) -> pours/stitching -> DRC -> fab outputs."""
import sys, os, json, math, subprocess, importlib, shutil, re, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import pcbnew
from pcbnew import FromMM as MM, ToMM
from sexp import FPDIR, pins, resolve
import route as R, erc, sch2
V = pcbnew.VECTOR2I
DATE = "2026-11-01"
def load_fp(spec):
    lib, name = spec.split(":"); fp = pcbnew.FootprintLoad(os.path.join(FPDIR, lib + ".pretty"), name)
    if fp is None: raise SystemExit(f"footprint not found: {spec}")
    fp.SetFPID(pcbnew.LIB_ID(lib, name)); return fp
def text_rect(x, y, s, size):                       # rough bounding box of reference text
    w = 0.62 * size * len(s); h = size; return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
def hit(a, b, m=0.0): return a[0] < b[2] + m and b[0] < a[2] + m and a[1] < b[3] + m and b[1] < a[3] + m
def build(modname, boost=(), seed=None, outdir=None):
    B = importlib.import_module("boards." + modname).BOARD
    out = outdir or os.path.join(HERE, "out", modname); os.makedirs(out, exist_ok=True); name = B["name"]; W, H = B["size"]; CR = B.get("corner", 2.0)
    for f in os.listdir(out):
        fp_ = os.path.join(out, f)
        if os.path.isfile(fp_): os.remove(fp_)
    report = {"board": name}
    # ---------- ERC on the spec ----------
    errs, warns, netinfo = erc.run(B)
    open(os.path.join(out, "erc.txt"), "w").write("ERRORS\n" + "\n".join(errs) + "\nWARNINGS\n" + "\n".join(warns) + "\n")
    report["erc_errors"] = errs; report["erc_warnings"] = warns
    if errs: print("ERC errors:", *errs, sep="\n  "); json.dump(report, open(os.path.join(out, "verification.json"), "w"), indent=1); return report
    # ---------- schematic ----------
    sch2.build(name, B["parts"], B["sch"], B["title"], B.get("rev", "A"), DATE, os.path.join(out, name + ".kicad_sch"))
    # project-local library tables so footprints/symbols resolve (no 'library not configured' warnings)
    libs = sorted({p["fp"].split(":")[0] for p in B["parts"]} | {"MountingHole", "Fiducial", "TestPoint"})
    open(os.path.join(out, "fp-lib-table"), "w").write("(fp_lib_table\n  (version 7)\n" + "".join(f'  (lib (name "{l}")(type "KiCad")(uri "{FPDIR}/{l}.pretty")(options "")(descr ""))\n' for l in libs) + ")\n")
    symlibs = sorted({p["sym"].split(":")[0] for p in B["parts"]} | {"power"})
    open(os.path.join(out, "sym-lib-table"), "w").write("(sym_lib_table\n  (version 7)\n" + "".join(f'  (lib (name "{l}")(type "KiCad")(uri "/usr/share/kicad/symbols/{l}.kicad_sym")(options "")(descr ""))\n' for l in symlibs) + ")\n")
    # ---------- pcb: outline ----------
    bd = pcbnew.BOARD(); nets = {}
    def net(n):
        if n not in nets: ni = pcbnew.NETINFO_ITEM(bd, n); bd.Add(ni); nets[n] = ni
        return nets[n]
    def edge_seg(a, b):
        s = pcbnew.PCB_SHAPE(bd); s.SetShape(pcbnew.SHAPE_T_SEGMENT); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); s.SetStart(V(MM(a[0]), MM(a[1]))); s.SetEnd(V(MM(b[0]), MM(b[1]))); bd.Add(s)
    def arc3(start, mid, end):
        s = pcbnew.PCB_SHAPE(bd); s.SetShape(pcbnew.SHAPE_T_ARC); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); s.SetArcGeometry(V(MM(start[0]), MM(start[1])), V(MM(mid[0]), MM(mid[1])), V(MM(end[0]), MM(end[1]))); bd.Add(s)
    r = CR; k = r * (1 - math.sqrt(0.5))
    edge_seg((r, 0), (W - r, 0)); edge_seg((W, r), (W, H - r)); edge_seg((W - r, H), (r, H)); edge_seg((0, H - r), (0, r))
    arc3((0, r), (k, k), (r, 0)); arc3((W - r, 0), (W - k, k), (W, r)); arc3((W, H - r), (W - k, H - k), (W - r, H)); arc3((r, H), (k, H - k), (0, H - r))
    # ---------- parts ----------
    parts = list(B["parts"]); fps = {}; auto = []
    for i, (hx, hy) in enumerate(B.get("holes", []), 1): auto.append(dict(ref=f"H{i}", fp="MountingHole:MountingHole_2.7mm_M2.5", value="M2.5", x=hx, y=hy, rot=0, nets={}))
    for i, (fx, fy) in enumerate(B.get("fids", []), 1): auto.append(dict(ref=f"FID{i}", fp="Fiducial:Fiducial_1mm_Mask2mm", value="Fiducial", x=fx, y=fy, rot=0, nets={}))
    mism = []
    for p in parts + auto:
        fp = load_fp(p["fp"])
        drop_ = [pad_ for pad_ in fp.Pads() if pad_.GetNumber() == "41" and pad_.GetAttribute() == pcbnew.PAD_ATTRIB_PTH and p["fp"].startswith("RF_Module:ESP32")]   # drop the footprint's 0.2 mm thermal-via pads (below the fab's 0.3 mm drill limit); board specs add their own 0.6/0.3 ground vias
        for pad_ in drop_: fp.Remove(pad_)
        fp.SetReference(p["ref"]); fp.SetValue(p["value"]); fp.SetPosition(V(MM(p["x"]), MM(p["y"])))
        if p.get("side", "F") == "B": fp.Flip(fp.GetPosition(), False)
        fp.SetOrientationDegrees(p.get("rot", 0)); bd.Add(fp); fps[p["ref"]] = fp
        padnums = {pad.GetNumber() for pad in list(fp.Pads())}
        for num, nn in p["nets"].items():
            if nn and num not in padnums: mism.append(f"{p['ref']}: symbol pin {num} has no pad in footprint {p['fp']}")
        for pad in fp.Pads():
            nn = p["nets"].get(pad.GetNumber())
            if nn: pad.SetNet(net(nn))
        fp.Value().SetVisible(False)
    report["pin_pad_mismatch"] = mism
    if mism: print(*mism, sep="\n")
    # ---------- routing ----------
    widths = B.get("widths", {}); WS = tuple(B.get("ws", (0.2, 0.4))); clr = B.get("clr", 0.2)
    rt = R.Router(W, H, widths=WS, clr=clr); rt.block_outside(0.45); rt.block_corner(CR, W, H)
    netid = {n: i for i, n in enumerate(sorted({n for p in parts for n in p["nets"].values() if n}))}
    pad_info = {}; occupied = []
    for ref, fp in fps.items():
        for pidx, pad in enumerate(fp.Pads()):
            bb = pad.GetBoundingBox(); x0, y0, x1, y1 = ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom())
            n = pad.GetNetname(); attr = pad.GetAttribute(); occupied.append((x0, y0, x1, y1))
            if attr == pcbnew.PAD_ATTRIB_NPTH: rt.block_rect(x0, y0, x1, y1, extra=0.4); continue
            layers = [0, 1] if attr == pcbnew.PAD_ATTRIB_PTH else ([1] if fp.GetLayer() == pcbnew.B_Cu else [0])
            if n and n in netid:
                rt.add_pad(layers, x0, y0, x1, y1, netid[n]); pad_info[(ref, pad.GetNumber(), pidx)] = (n, layers, (x0, y0, x1, y1), (ToMM(pad.GetPosition().x), ToMM(pad.GetPosition().y)), attr == pcbnew.PAD_ATTRIB_PTH, pad)
            else: rt.block_rect(x0, y0, x1, y1, layers)
    for (a, b, c_, d) in B.get("keepout", []): rt.block_rect(a, b, c_, d)
    for fp_ in fps.values():                                                                                 # footprint keepout rule areas (e.g. under the MPU-6050 body)
        for z_ in fp_.Zones():
            if z_.GetDoNotAllowTracks() or z_.GetDoNotAllowVias():
                bb_ = z_.GetBoundingBox(); rt.block_rect(ToMM(bb_.GetLeft()), ToMM(bb_.GetTop()), ToMM(bb_.GetRight()), ToMM(bb_.GetBottom()))

    tracks = []; failures = []
    def add_track(layer, a, b, nname, w):
        t = pcbnew.PCB_TRACK(bd); t.SetStart(V(MM(a[0]), MM(a[1]))); t.SetEnd(V(MM(b[0]), MM(b[1]))); t.SetWidth(MM(w)); t.SetLayer(pcbnew.F_Cu if layer == 0 else pcbnew.B_Cu); t.SetNet(nets[nname]); bd.Add(t)
    def add_via(x, y, nname):
        v = pcbnew.PCB_VIA(bd); v.SetPosition(V(MM(x), MM(y))); v.SetWidth(MM(0.6)); v.SetDrill(MM(0.3)); v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetNet(nets[nname]); bd.Add(v)
    done = collections.defaultdict(set)
    inv = {v: k for k, v in netid.items()}
    # pre-routes (hand-placed critical copper)
    for pr in B.get("pre", []):
        w = pr.get("w", widths.get(pr["net"], 0.2)); nid = netid[pr["net"]]
        rt.commit_trace(nid, pr["layer"], pr["pts"], w)
        for a, b in zip(pr["pts"], pr["pts"][1:]): add_track(pr["layer"], a, b, pr["net"], w)
        for (x, y) in pr["pts"]:
            c = rt.cell(x, y)
            if pr.get("goal", True): done[pr["net"]].add((pr["layer"], c[0], c[1]))      # goal=False: copper is committed but not a routing goal (a separate island the router must still link)
    for (n, x, y) in B.get("pre_vias", []):
        rt.commit_via(netid[n], x, y); add_via(x, y, n); c = rt.cell(x, y); done[n] |= {(0, c[0], c[1]), (1, c[0], c[1])}
    esc_cells = {}
    # escape stubs: every used pad of a fine-pitch part (>= 24 pads) gets a short outward track first, so later nets cannot wall it in
    for ref_, fp_ in fps.items():
        pads_ = list(fp_.Pads())
        if (len(pads_) < 24 and not (ref_.startswith("U") and len(pads_) >= 5)) or ref_.startswith("J"): continue
        cx_, cy_ = ToMM(fp_.GetPosition().x), ToMM(fp_.GetPosition().y)
        for pidx_, pad_ in enumerate(pads_):
            n_ = pad_.GetNetname()
            if not n_ or n_ == "GND" or n_ not in netid: continue
            px_, py_ = ToMM(pad_.GetPosition().x), ToMM(pad_.GetPosition().y); dx_, dy_ = px_ - cx_, py_ - cy_
            d_ = (1 if dx_ > 0 else -1, 0) if abs(dx_) > abs(dy_) else (0, 1 if dy_ > 0 else -1)
            k_ = rt.cls(widths.get(n_, 0.2)); nid_ = netid[n_]; pts_ = [(px_, py_)]
            for step_ in range(1, 25):                                                  # up to 1.2 mm in 0.05 mm steps while the cells are free
                x_, y_ = px_ + d_[0] * step_ * R.G, py_ + d_[1] * step_ * R.G; ix_, iy_ = rt.cell(x_, y_)
                if not (rt._free(k_, 0, ix_, iy_, nid_)): break
                pts_.append((x_, y_))
            if len(pts_) < 8: continue                                                    # not even 0.35 mm: skip
            end_ = pts_[-1]; rt.commit_trace(nid_, 0, [pts_[0], end_], widths.get(n_, 0.2)); add_track(0, pts_[0], end_, n_, widths.get(n_, 0.2)); ex_, ey_ = rt.cell(*end_)
            esc_cells[(ref_, pad_.GetNumber(), pidx_)] = (0, ex_, ey_)
    order = {}
    for kk, v in pad_info.items(): order.setdefault(v[0], []).append(kk)
    def cells_in(bbox, layer, padobj, ctr):
        x0, y0, x1, y1 = bbox; a = rt.cell(x0, y0); b = rt.cell(x1, y1); res = []
        for ix in range(a[0], b[0] + 1):
            for iy in range(a[1], b[1] + 1):
                x, y = rt.xy(ix, iy)
                if not (x0 - 1e-6 <= x <= x1 + 1e-6 and y0 - 1e-6 <= y <= y1 + 1e-6): continue
                if not padobj.HitTest(V(MM(x), MM(y)), MM(-0.05)): continue                       # cell centre must lie inside the real pad copper
                res.append((layer, ix, iy))
        return res
    gnd = "GND"; first_nets = [n for n in list(boost) + list(B.get("first", [])) if n in order]; first_nets = list(dict.fromkeys(first_nets))
    sig = [n for n in order if n != gnd and n not in first_nets]
    pw = [n for n in sig if widths.get(n, 0.2) > 0.2 or n.startswith("+") or n == "VBUS"]; sig = [n for n in sig if n not in pw]
    def tightness(n):                                    # fewest free cells around any pad of the net (2 mm square, top layer) = most constrained
        k = rt.cls(widths.get(n, 0.2)); best = 10 ** 9; nid_ = netid[n]
        for pk_ in order[n]:
            cx, cy = rt.cell(*pad_info[pk_][3]); r_ = int(2.0 / R.G); sub = rt.owner[k][0][max(cy - r_, 0):cy + r_ + 1, max(cx - r_, 0):cx + r_ + 1]
            best = min(best, int(((sub == -1) | (sub == nid_)).sum()))
        return best
    import random; rnd_ = random.Random(seed)
    jit = (lambda: 1.0 + 0.9 * rnd_.random()) if seed is not None else (lambda: 1.0)
    sig.sort(key=lambda n: (len(order[n]) > 3, tightness(n) * jit()))
    if seed is not None: pw.sort(key=lambda n: rnd_.random())
    skip_gnd_tht = True
    only = os.environ.get("ONLY_NETS")
    for n in first_nets + ([gnd] if gnd in order else []) + pw + sig:
        if only and n not in only.split(","): continue
        nid = netid[n]; w = widths.get(n, 0.2); first = not done[n]
        for pk in order[n]:
            _, layers, bbox, ctr, tht, circ = pad_info[pk]
            starts = [c for l in layers for c in cells_in(bbox, l, circ, ctr) if rt._free(rt.cls(w), l, c[1], c[2], nid)]
            if pk in esc_cells: starts = starts + [esc_cells[pk]]                          # the pad's own escape stub end is part of the pad
            if not starts: failures.append((n, pk, "no free start cell")); continue
            if n == gnd and (tht or B.get("gnd_pour_only")): continue                  # ground reaches SMD pads through the top pour / stitching vias
            if first and n != gnd and not done[n]: first = False; done[n] |= set(starts); continue
            if n == gnd and any(c in done[n] for c in starts): continue
            # window around the pad and the nearest goals
            gx = [c[1] for c in done[n]]; gy = [c[2] for c in done[n]]
            sx = [c[1] for c in starts]; sy = [c[2] for c in starts]
            pad_cells = int(5 / R.G)
            if gx: win = (min(min(gx), min(sx)) - pad_cells, min(min(gy), min(sy)) - pad_cells, max(max(gx), max(sx)) + pad_cells, max(max(gy), max(sy)) + pad_cells)
            else: win = (min(sx) - pad_cells, min(sy) - pad_cells, max(sx) + pad_cells, max(sy) + pad_cells)
            path = None; via_end = False
            if n == gnd:
                small = (min(sx) - int(3 / R.G), min(sy) - int(3 / R.G), max(sx) + int(3 / R.G), max(sy) + int(3 / R.G))
                path, via_end = rt.route(nid, w, starts, done[n], goal_via=True, window=small)
                if path is None: path, via_end = rt.route(nid, w, starts, done[n], goal_via=True, window=(min(sx) - int(7 / R.G), min(sy) - int(7 / R.G), max(sx) + int(7 / R.G), max(sy) + int(7 / R.G)))
            else:
                path, via_end = rt.route(nid, w, starts, done[n], window=win, eps=2.5, max_nodes=500000)
                if path is None: path, via_end = rt.route(nid, w, starts, done[n], window=(min(sx) - int(14 / R.G), min(sy) - int(14 / R.G), max(sx) + int(14 / R.G), max(sy) + int(14 / R.G)), eps=4.0, max_nodes=900000)
                if path is None: path, via_end = rt.route(nid, w, starts, done[n], eps=5.0, max_nodes=3000000)         # last resort: whole board, greedier
            if path is None: failures.append((n, pk, "no route")); (os.environ.get("ROUTE_DEBUG") and __import__('numpy').savez(os.path.join(out, "dbg_%s.npz" % n.replace('+','p')), o0=rt.owner[rt.cls(w)][0], o1=rt.owner[rt.cls(w)][1], starts=__import__('numpy').array(starts), goals=__import__('numpy').array(list(done[n])), nid=nid)); print("  no route:", n, pk[:2], "starts", len(starts), "free_layers", sorted({c[0] for c in starts}), flush=True); continue
            rt.commit(nid, path, w)
            if via_end:
                l, ix, iy = path[-1]; x, y = rt.xy(ix, iy); rt.commit_via(nid, x, y); add_via(x, y, n)
            done[n] |= set(path) | set(starts)
            segs = []; start = path[0]; d = None
            for a, b in zip(path, path[1:]):
                if a[0] != b[0]:
                    if start != a: segs.append((a[0], start, a))
                    x, y = rt.xy(a[1], a[2]); add_via(x, y, n); start = b; d = None; continue
                dd = (b[1] - a[1], b[2] - a[2])
                if d is not None and dd != d: segs.append((a[0], start, a)); start = a
                d = dd
            if start != path[-1]: segs.append((path[-1][0], start, path[-1]))
            for l, a, b in segs: add_track(l, rt.xy(a[1], a[2]), rt.xy(b[1], b[2]), n, w)
            l0, ix0, iy0 = path[0]; c0 = rt.xy(ix0, iy0)
            if math.hypot(ctr[0] - c0[0], ctr[1] - c0[1]) > 1e-3: add_track(l0, ctr, c0, n, w)
    if "custom" in B: B["custom"](bd, nets, pcbnew, MM)
    # ---------- stitching vias ----------
    gid = netid.get(gnd); stitched = 0
    if gnd in nets and B.get("stitch", 5.0):
        pitch = B.get("stitch", 5.0); k0 = rt.cls(0.2); rad = int(1.5 / R.G)
        def spot(ix, iy):
            for dx in range(-rad, rad + 1, 2):
                for dy in range(-rad, rad + 1, 2):
                    cx, cy = ix + dx, iy + dy
                    if cx < 0 or cy < 0 or cx >= rt.nx or cy >= rt.ny: continue
                    if rt._via_ok(k0, cx, cy, gid) and rt._no_via_near(cx, cy, 2.5) and all(rt.owner[k0][l][cy, cx] in (-1, gid) for l in (0, 1)):
                        xx, yy = rt.xy(cx, cy)
                        if all(not hit((xx - .5, yy - .5, xx + .5, yy + .5), o, 0.3) for o in occupied): return xx, yy
            return None
        y = 3.0
        while y < H - 2.5:
            x = 3.0
            while x < W - 2.5:
                ix, iy = rt.cell(x, y); sp_ = spot(ix, iy)
                if sp_: rt.commit_via(gid, *sp_); add_via(sp_[0], sp_[1], gnd); stitched += 1
                x += pitch
            y += pitch
    report["stitch_vias"] = stitched
    # ---------- pours ----------
    if gnd in nets:
        for lay in (pcbnew.F_Cu, pcbnew.B_Cu):
            z = pcbnew.ZONE(bd); z.SetLayer(lay); z.SetNet(nets[gnd]); z.SetMinThickness(MM(0.2)); z.SetLocalClearance(MM(0.25)); z.SetThermalReliefGap(MM(0.25)); z.SetThermalReliefSpokeWidth(MM(0.3))
            z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS); z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL if lay == pcbnew.F_Cu else pcbnew.ZONE_CONNECTION_THERMAL); ol = z.Outline(); ol.NewOutline()
            m = 0.4
            for (x, y) in ((m, m), (W - m, m), (W - m, H - m), (m, H - m)): ol.Append(MM(x), MM(y))
            bd.Add(z)
    # ---------- silkscreen: reference placement with collision avoidance ----------
    occ = list(occupied); sil = []
    for ref_, fp_ in fps.items():
        for g in fp_.GraphicalItems():
            if g.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                bb_ = g.GetBoundingBox(); occ.append((ToMM(bb_.GetLeft()), ToMM(bb_.GetTop()), ToMM(bb_.GetRight()), ToMM(bb_.GetBottom())))
    for ref, fp in fps.items():
        t = fp.Reference(); t.SetTextSize(V(MM(0.8), MM(0.8))); t.SetTextThickness(MM(0.16))
        if ref.startswith(("H", "FID")) and ref[1:].isdigit() or ref.startswith("FID"): t.SetVisible(False); continue
        bb = fp.GetBoundingBox(False, False); cx0, cy0, cx1, cy1 = [ToMM(v) for v in (bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom())]
        # use pad extents for the footprint's real size
        pads = [p_.GetBoundingBox() for p_ in fp.Pads()]
        if pads:
            cx0 = min(ToMM(b.GetLeft()) for b in pads); cy0 = min(ToMM(b.GetTop()) for b in pads); cx1 = max(ToMM(b.GetRight()) for b in pads); cy1 = max(ToMM(b.GetBottom()) for b in pads)
        s = 0.8; w = 0.62 * s * len(ref); mx, my = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        cands = [(mx, cy0 - 0.9), (mx, cy1 + 0.9), (cx0 - w / 2 - 0.5, my), (cx1 + w / 2 + 0.5, my), (mx, cy0 - 1.8), (mx, cy1 + 1.8), (cx1 + w / 2 + 0.5, cy0 - 0.9), (cx0 - w / 2 - 0.5, cy1 + 0.9)]
        for rr in (3.0, 4.5, 6.0, 8.0):
            for k_ in range(16):
                cands.append((mx + (rr + (cx1 - cx0) / 2) * math.cos(k_ * math.pi / 8), my + (rr + (cy1 - cy0) / 2) * math.sin(k_ * math.pi / 8)))
        cands.append((mx, my))
        placed = False
        for (tx, ty) in cands:
            rc = text_rect(tx, ty, ref, s)
            if rc[0] < 0.6 or rc[1] < 0.6 or rc[2] > W - 0.6 or rc[3] > H - 0.6: continue
            if any(hit(rc, o, 0.2) for o in occ): continue
            t.SetPosition(V(MM(tx), MM(ty))); t.SetTextAngleDegrees(0); occ.append(rc); placed = True; break
        if not placed: sil.append(ref)
    report["silk_unplaced"] = sil
    for (txt, x, y, size) in B.get("silk", []):
        t = pcbnew.PCB_TEXT(bd); t.SetText(txt); t.SetPosition(V(MM(x), MM(y))); t.SetLayer(pcbnew.F_SilkS); t.SetTextSize(V(MM(max(size, 0.8)), MM(max(size, 0.8)))); t.SetTextThickness(MM(0.16)); bd.Add(t)
    pcb_path = os.path.join(out, name + ".kicad_pcb"); bd.Save(pcb_path)
    open(os.path.join(out, name + ".kicad_pro"), "w").write(json.dumps({"meta": {"filename": name + ".kicad_pro", "version": 1}, "net_settings": {"classes": [{"name": "Default", "clearance": clr, "track_width": 0.2, "via_diameter": 0.6, "via_drill": 0.3}], "meta": {"version": 3}}, "board": {"design_settings": dict({"rules": {"min_clearance": clr, "min_track_width": 0.2, "min_via_diameter": 0.6, "min_through_hole_diameter": 0.3}}, **({"rule_severities": {"lib_footprint_mismatch": "ignore"}} if any(p["fp"].startswith("RF_Module:ESP32") for p in B["parts"]) else {}))}}, indent=1))
    bd = pcbnew.LoadBoard(pcb_path); filler = pcbnew.ZONE_FILLER(bd); filler.Fill(bd.Zones()); bd.Save(pcb_path)
    import silkfix; report["silk"] = silkfix.fix(pcb_path)
    report["route_failures"] = [list(map(str, f_)) for f_ in failures]; report["tracks"] = len(list(bd.GetTracks()))
    json.dump(report, open(os.path.join(out, "route_report.json"), "w"), indent=1); return report
if __name__ == "__main__" and len(sys.argv) >= 4 and sys.argv[2] == "seed":            # python3 build.py <board> seed <n> : one randomised-order attempt into out/<board>_s<n>
    r = build(sys.argv[1], tuple(x for x in os.environ.get("BOOST", "").split(",") if x), int(sys.argv[3]), os.path.join(HERE, "out", f"{sys.argv[1]}_s{sys.argv[3]}")); print("RESULT", len(r.get("route_failures", [])))
    sys.exit(0)
if __name__ == "__main__":
    boost = []
    for attempt in range(1 if os.environ.get("ROUTE_DEBUG") else 5):                                  # if some nets fail, route those first on the next attempt
        r = build(sys.argv[1], tuple(boost))
        fails = [f[0] for f in r.get("route_failures", [])]
        if not fails: break
        new = [n for n in dict.fromkeys(fails) if n not in boost]
        if not new: break
        boost = new + boost
    r["attempts"] = attempt + 1; json.dump(r, open(os.path.join(HERE, "out", sys.argv[1], "route_report.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in r.items() if k not in ("erc_warnings",)}, indent=1)[:1500])
