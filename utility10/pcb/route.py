"""Small two-layer grid router for tiny boards. Grid in mm units of G. Not a general autorouter: sequential A*, 8-direction moves, vias."""
import heapq, math
import numpy as np
G = 0.1
class Router:
    def __init__(self, w_mm, h_mm, width=0.25, clr=0.2, via_d=0.6, via_hole=0.3, origin=(0, 0)):
        self.ox, self.oy = origin; self.nx, self.ny = int(w_mm / G) + 1, int(h_mm / G) + 1
        self.w, self.clr, self.via_d = width, clr, via_d; self.via_hole = via_hole
        self.owner = [np.full((self.ny, self.nx), -1, dtype=np.int32) for _ in range(2)]     # per layer: -1 free, -2 blocked, >=0 net id
        self.r_trace = clr + width / 2 + 0.06; self.r_via = clr + via_d / 2 + width / 2 + 0.06   # +0.06: grid-rounding margin
        self.paths = {}; self.vias = []
    def cell(self, x, y): return int(round((x - self.ox) / G)), int(round((y - self.oy) / G))
    def xy(self, ix, iy): return self.ox + ix * G, self.oy + iy * G
    def _mark_rect(self, layer, x0, y0, x1, y1, net, infl):
        ax, ay = self.cell(x0 - infl, y0 - infl); bx, by = self.cell(x1 + infl, y1 + infl)
        ax, ay = max(ax, 0), max(ay, 0); bx, by = min(bx, self.nx - 1), min(by, self.ny - 1)
        if ax > bx or ay > by: return
        sub = self.owner[layer][ay:by + 1, ax:bx + 1]
        if net == -2: sub[:] = -2
        else:
            bad = (sub >= 0) & (sub != net) | (sub == -2)
            sub[sub == -1] = net; sub[bad] = -2
    def add_pad(self, layers, x0, y0, x1, y1, net):
        for l in layers: self._mark_rect(l, x0, y0, x1, y1, net, self.r_trace)
    def block_rect(self, x0, y0, x1, y1, layers=(0, 1), infl=None):
        for l in layers: self._mark_rect(l, x0, y0, x1, y1, -2, self.r_trace if infl is None else infl)
    def block_outside(self, margin):
        """keep copper margin mm away from the board edge"""
        m = int(round(margin / G))
        for l in (0, 1):
            self.owner[l][:m, :] = -2; self.owner[l][-m:, :] = -2; self.owner[l][:, :m] = -2; self.owner[l][:, -m:] = -2
    def _free(self, layer, ix, iy, net):
        if ix < 0 or iy < 0 or ix >= self.nx or iy >= self.ny: return False
        o = self.owner[layer][iy, ix]; return o == -1 or o == net
    def _via_ok(self, ix, iy, net):
        r = int(math.ceil((self.via_d / 2 + self.clr) / G))
        for l in (0, 1):
            a = self.owner[l][max(iy - r, 0):iy + r + 1, max(ix - r, 0):ix + r + 1]
            if ((a != -1) & (a != net)).any(): return False
        return True
    def _no_via_near(self, ix, iy, d=0.9):
        x, y = self.xy(ix, iy)
        return all(math.hypot(x - vx, y - vy) >= d for _, vx, vy in self.vias)
    def route(self, net, starts, goals, allow_via=True, via_cost=30, goal_via=False):
        """starts: list of (layer, ix, iy); goals: set of (layer, ix, iy). goal_via: any via-able cell is a goal (used for GND to the pour)."""
        open_, best, prev = [], {}, {}
        for s in starts:
            heapq.heappush(open_, (0.0, 0.0, s)); best[s] = 0.0
        dirs = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
        gl = list(goals)[:80]
        def h(c):
            if goal_via or not gl: return 0.0
            return min(math.hypot(c[1] - g[1], c[2] - g[2]) for g in gl)
        pdir = {}
        while open_:
            _, g, cur = heapq.heappop(open_)
            if g > best.get(cur, 1e18) + 1e-9: continue
            l, ix, iy = cur
            if (cur in goals) or (goal_via and l == 0 and self._via_ok(ix, iy, net) and g > 0 and self._no_via_near(ix, iy)):
                path = [cur]
                while cur in prev: cur = prev[cur]; path.append(cur)
                return path[::-1], (goal_via and l == 0 and path[-1] not in goals)
            for dx, dy, c in dirs:
                nx, ny = ix + dx, iy + dy
                if not self._free(l, nx, ny, net): continue
                if dx and dy and not (self._free(l, ix + dx, iy, net) and self._free(l, ix, iy + dy, net)): continue
                turn = 0.3 if pdir.get(cur) not in (None, (dx, dy)) else 0.0
                ng = g + c + turn; nc = (l, nx, ny)
                if ng < best.get(nc, 1e18): best[nc] = ng; prev[nc] = cur; pdir[nc] = (dx, dy); heapq.heappush(open_, (ng + h(nc), ng, nc))
            if allow_via and self._via_ok(ix, iy, net) and self._free(1 - l, ix, iy, net):
                nc = (1 - l, ix, iy); ng = g + via_cost
                if ng < best.get(nc, 1e18): best[nc] = ng; prev[nc] = cur; pdir[nc] = None; heapq.heappush(open_, (ng + h(nc), ng, nc))
        return None, False
    def commit(self, net, path):
        """mark the routed path as occupied by the net"""
        for i, (l, ix, iy) in enumerate(path):
            x, y = self.xy(ix, iy); self._mark_rect(l, x, y, x, y, net, self.r_trace)
            if i and path[i - 1][0] != l:
                self.vias.append((net, x, y))
                for ll in (0, 1): self._mark_rect(ll, x, y, x, y, net, self.r_via)
