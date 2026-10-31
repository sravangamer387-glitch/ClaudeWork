"""Two-layer grid router v2: 0.05 mm grid, per-net trace widths (two classes), exact per-class obstacle inflation, windowed weighted A*, vias."""
import heapq, math, os
import numpy as np
G = 0.05
class Router:
    def __init__(self, w_mm, h_mm, widths=(0.2, 0.4), clr=0.2, via_d=0.6, margin=0.0):
        self.nx, self.ny = int(w_mm / G) + 1, int(h_mm / G) + 1
        self.widths = list(widths); self.clr = clr; self.via_d = via_d; self.m = margin
        self.owner = [[np.full((self.ny, self.nx), -1, dtype=np.int32) for _ in range(2)] for _ in self.widths]    # [class][layer]
        self.paths = {}; self.vias = []
    def cls(self, w): return self.widths.index(w)
    def cell(self, x, y): return int(round(x / G)), int(round(y / G))
    def xy(self, ix, iy): return round(ix * G, 4), round(iy * G, 4)
    def _mark(self, k, layer, x0, y0, x1, y1, net, infl):
        ax, ay = self.cell(x0 - infl, y0 - infl); bx, by = self.cell(x1 + infl, y1 + infl)
        ax, ay = max(ax, 0), max(ay, 0); bx, by = min(bx, self.nx - 1), min(by, self.ny - 1)
        if ax > bx or ay > by: return
        sub = self.owner[k][layer][ay:by + 1, ax:bx + 1]
        if net == -2: sub[:] = -2
        else:
            bad = ((sub >= 0) & (sub != net)) | (sub == -2)
            sub[sub == -1] = net; sub[bad] = -2
    def add_pad(self, layers, x0, y0, x1, y1, net):
        for k, w in enumerate(self.widths):
            for l in layers: self._mark(k, l, x0, y0, x1, y1, net, self.clr + w / 2 + self.m)
    def block_rect(self, x0, y0, x1, y1, layers=(0, 1), extra=0.0):
        for k, w in enumerate(self.widths):
            for l in layers: self._mark(k, l, x0, y0, x1, y1, -2, self.clr + w / 2 + self.m + extra)
    def block_outside(self, margin):
        m = int(round(margin / G))
        for k in range(len(self.widths)):
            for l in (0, 1):
                a = self.owner[k][l]; a[:m, :] = -2; a[-m:, :] = -2; a[:, :m] = -2; a[:, -m:] = -2
    def block_corner(self, r, W, H):
        """round-corner board edge: block cells outside the arcs"""
        for k in range(len(self.widths)):
            for l in (0, 1):
                a = self.owner[k][l]
                for (cx, cy, sx, sy) in ((r, r, -1, -1), (W - r, r, 1, -1), (r, H - r, -1, 1), (W - r, H - r, 1, 1)):
                    ix0, iy0 = self.cell(cx, cy); n = int(round(r / G)) + 2
                    for dx in range(0, n + 1):
                        for dy in range(0, n + 1):
                            x, y = cx + sx * dx * G, cy + sy * dy * G
                            if math.hypot(x - cx, y - cy) > r - 0.4:
                                ix, iy = self.cell(x, y)
                                if 0 <= ix < self.nx and 0 <= iy < self.ny: a[iy, ix] = -2
    def _free(self, k, layer, ix, iy, net):
        if ix < 0 or iy < 0 or ix >= self.nx or iy >= self.ny: return False
        o = self.owner[k][layer][iy, ix]; return o == -1 or o == net
    def _via_ok(self, k, ix, iy, net):
        r = int(math.ceil((self.via_d / 2 + self.clr + self.m) / G))
        for l in (0, 1):
            a = self.owner[k][l][max(iy - r, 0):iy + r + 1, max(ix - r, 0):ix + r + 1]
            if ((a != -1) & (a != net)).any(): return False
        return True
    def _no_via_near(self, ix, iy, d=1.0):
        x, y = self.xy(ix, iy); return all(math.hypot(x - vx, y - vy) >= d for _, vx, vy in self.vias)
    def via_map(self, k, net):
        """boolean array: a via of the router's size can be placed here (no foreign copper within via radius on either layer)"""
        r = int(math.ceil((self.via_d / 2 + self.clr + self.m) / G)); ok = None
        for l in (0, 1):
            a = self.owner[k][l]; foreign = ((a != -1) & (a != net)).astype(np.int32)
            ii = np.pad(foreign.cumsum(0).cumsum(1), ((1, 0), (1, 0))); ny, nx = foreign.shape
            y0 = np.clip(np.arange(ny) - r, 0, ny); y1 = np.clip(np.arange(ny) + r + 1, 0, ny); x0 = np.clip(np.arange(nx) - r, 0, nx); x1 = np.clip(np.arange(nx) + r + 1, 0, nx)
            tot = ii[y1][:, x1] - ii[y0][:, x1] - ii[y1][:, x0] + ii[y0][:, x0]
            ok = (tot == 0) if ok is None else (ok & (tot == 0))
        return ok
    def route(self, net, w, starts, goals, allow_via=True, via_cost=40, goal_via=False, window=None, eps=1.3, max_nodes=600000):
        k = self.cls(w); nx_ = self.nx; ny_ = self.ny
        own = [self.owner[k][l].ravel().tolist() for l in (0, 1)]
        vok = self.via_map(k, net).ravel().tolist() if allow_via or goal_via else None
        nv = {}
        for d_ in (0.8, 1.0):
            a_ = np.zeros((self.ny, self.nx), dtype=bool); r_ = int(d_ / G)
            for _, vx, vy in self.vias:
                cx, cy = self.cell(vx, vy); a_[max(cy - r_, 0):cy + r_ + 1, max(cx - r_, 0):cx + r_ + 1] = True
            nv[d_] = a_.ravel().tolist()
        def far(ix, iy, d): return not nv[d][iy * nx_ + ix]
        open_, best, prev, pdir = [], {}, {}, {}
        for s in starts: heapq.heappush(open_, (0.0, 0.0, s)); best[s] = 0.0
        dirs = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
        if goals:
            gxs = [g[1] for g in goals]; gys = [g[2] for g in goals]; bx0, bx1, by0, by1 = min(gxs), max(gxs), min(gys), max(gys)
        def h(c):
            if goal_via or not goals: return 0.0
            dx = max(bx0 - c[1], 0, c[1] - bx1); dy = max(by0 - c[2], 0, c[2] - by1)
            return eps * math.hypot(dx, dy)                      # distance to the bounding box of the goal cells: cheap lower bound
        x0, y0, x1, y1 = window if window else (0, 0, nx_, ny_)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, nx_ - 1), min(y1, ny_ - 1)
        def free(l, ix, iy):
            o = own[l][iy * nx_ + ix]; return o == -1 or o == net
        popped = 0
        while open_:
            popped += 1
            if popped > max_nodes:
                if os.environ.get("ROUTE_DEBUG"): print("   route: node limit", max_nodes, "eps", eps, "window", window, flush=True)
                return None, False
            _, g, cur = heapq.heappop(open_)
            if g > best.get(cur, 1e18) + 1e-9: continue
            l, ix, iy = cur
            if (cur in goals) or (goal_via and l == 0 and g > 0 and vok[iy * nx_ + ix] and far(ix, iy, 1.0)):
                path = [cur]
                while cur in prev: cur = prev[cur]; path.append(cur)
                return path[::-1], (goal_via and path[-1] not in goals and path[-1][0] == 0)
            for dx, dy, c in dirs:
                nx, ny = ix + dx, iy + dy
                if nx < x0 or nx > x1 or ny < y0 or ny > y1: continue
                if not free(l, nx, ny): continue
                if dx and dy and not (free(l, ix + dx, iy) and free(l, ix, iy + dy)): continue
                turn = 0.4 if pdir.get(cur) not in (None, (dx, dy)) else 0.0
                ng = g + c + turn; nc = (l, nx, ny)
                if ng < best.get(nc, 1e18): best[nc] = ng; prev[nc] = cur; pdir[nc] = (dx, dy); heapq.heappush(open_, (ng + h(nc), ng, nc))
            if allow_via and vok[iy * nx_ + ix] and free(1 - l, ix, iy) and far(ix, iy, 0.8):
                nc = (1 - l, ix, iy); ng = g + via_cost
                if ng < best.get(nc, 1e18): best[nc] = ng; prev[nc] = cur; pdir[nc] = None; heapq.heappush(open_, (ng + h(nc), ng, nc))
        if os.environ.get("ROUTE_DEBUG"): print("   route: exhausted after", popped, "pops; reached cells", len(best), "window", window, "goals", len(goals), flush=True)
        return None, False
    def commit_trace(self, net, layer, pts, w):
        """mark a polyline (list of (x,y) mm) as copper of the net"""
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            n = max(int(max(abs(xb - xa), abs(yb - ya)) / G), 1)
            for i in range(n + 1):
                x, y = xa + (xb - xa) * i / n, ya + (yb - ya) * i / n
                for k, wc in enumerate(self.widths): self._mark(k, layer, x, y, x, y, net, self.clr + wc / 2 + w / 2 + self.m)
    def commit_via(self, net, x, y):
        self.vias.append((net, x, y))
        for k, wc in enumerate(self.widths):
            for l in (0, 1): self._mark(k, l, x, y, x, y, net, self.clr + wc / 2 + self.via_d / 2 + self.m)
    def commit(self, net, path, w):
        for i, (l, ix, iy) in enumerate(path):
            x, y = self.xy(ix, iy)
            for k, wc in enumerate(self.widths): self._mark(k, l, x, y, x, y, net, self.clr + wc / 2 + w / 2 + self.m)
            if i and path[i - 1][0] != l: self.commit_via(net, x, y)
