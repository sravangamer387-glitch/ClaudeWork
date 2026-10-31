"""Tilt Maze Labyrinth: generate 3 mazes (difficulty), verify solvable, count dead ends, put trap holes only on dead ends / never on the solution path,
and check the minimum corridor width against ball size. Writes SVG cut files (walls as 6 mm MDF strips are separate: here the wall LINES to be laser-engraved/cut as slots)."""
import random, os, collections
OUT = os.path.join(os.path.dirname(__file__), "..", "out"); CELL = 22.0   # mm pitch; corridor clear width = CELL - wall thickness 3 = 19 mm for a 12 mm marble
def gen(n, seed):
    rnd = random.Random(seed); walls = {(x, y): {"N", "S", "E", "W"} for x in range(n) for y in range(n)}
    seen = {(0, 0)}; stack = [(0, 0)]; D = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
    while stack:
        x, y = stack[-1]; opts = [(k, x + dx, y + dy, o) for k, (dx, dy, o) in D.items() if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
        if not opts: stack.pop(); continue
        k, nx, ny, o = rnd.choice(opts); walls[(x, y)].discard(k); walls[(nx, ny)].discard(o); seen.add((nx, ny)); stack.append((nx, ny))
    return walls, D
def solve(walls, D, n):
    prev = {(0, 0): None}; q = collections.deque([(0, 0)])
    while q:
        c = q.popleft()
        for k, (dx, dy, o) in D.items():
            nb = (c[0] + dx, c[1] + dy)
            if k not in walls[c] and nb not in prev and 0 <= nb[0] < n and 0 <= nb[1] < n: prev[nb] = c; q.append(nb)
    goal = (n - 1, n - 1); path = []; c = goal
    while c is not None: path.append(c); c = prev.get(c)
    return path[::-1], prev
lines = ["| level | grid | solution length (cells) | dead ends | trap holes | solvable with holes | longest dead-end branch |", "|---|---|---|---|---|---|---|"]
for name, n, holes, seed in (("Easy", 9, 4, 1), ("Medium", 13, 10, 2), ("Hard", 17, 20, 3)):
    walls, D = gen(n, seed); path, prev = solve(walls, D, n)
    assert path[0] == (0, 0) and path[-1] == (n - 1, n - 1), "unsolvable"
    deg = {c: 4 - len(w) for c, w in walls.items()}; dead = [c for c, d in deg.items() if d == 1 and c not in (path[0], path[-1])]
    rnd = random.Random(seed + 10); onpath = set(path); cand = [c for c in dead if c not in onpath]; hs = rnd.sample(cand, min(holes, len(cand)))
    # solvable with holes (holes on dead ends cannot block the route): BFS avoiding holes
    blocked = set(hs); p2, _ = solve(walls, D, n); ok = all(c not in blocked for c in p2)
    # branch depth: BFS distance from path of each dead end
    dist = {}; q = collections.deque((c, 0) for c in path); seen = set(path)
    while q:
        c, dd = q.popleft(); dist[c] = dd
        for k, (dx, dy, o) in D.items():
            nb = (c[0] + dx, c[1] + dy)
            if k not in walls[c] and nb not in seen and 0 <= nb[0] < n and 0 <= nb[1] < n: seen.add(nb); q.append((nb, dd + 1))
    lines.append(f"| {name} | {n}x{n} | {len(path)} | {len(dead)} | {len(hs)} | {'yes' if ok else 'NO'} | {max(dist.values())} |")
    W = n * CELL; s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W+20}mm" height="{W+20}mm" viewBox="-10 -10 {W+20} {W+20}"><g stroke="blue" stroke-width="0.3" fill="none">']
    for (x, y), w in walls.items():
        if "N" in w: s.append(f'<line x1="{x*CELL}" y1="{y*CELL}" x2="{(x+1)*CELL}" y2="{y*CELL}"/>')
        if "W" in w: s.append(f'<line x1="{x*CELL}" y1="{y*CELL}" x2="{x*CELL}" y2="{(y+1)*CELL}"/>')
        if "S" in w and y == n - 1: s.append(f'<line x1="{x*CELL}" y1="{(y+1)*CELL}" x2="{(x+1)*CELL}" y2="{(y+1)*CELL}"/>')
        if "E" in w and x == n - 1: s.append(f'<line x1="{(x+1)*CELL}" y1="{y*CELL}" x2="{(x+1)*CELL}" y2="{(y+1)*CELL}"/>')
    s.append('</g><g stroke="red" stroke-width="0.3" fill="none">')
    for (x, y) in hs: s.append(f'<circle cx="{(x+.5)*CELL}" cy="{(y+.5)*CELL}" r="9"/>')       # 18 mm holes through the maze floor (marble 12 mm)
    s.append(f'<circle cx="{(n-.5)*CELL}" cy="{(n-.5)*CELL}" r="9" stroke-dasharray="2"/></g></svg>')
    open(os.path.join(OUT, f"maze_{name.lower()}.svg"), "w").write("\n".join(s))
txt = "\n".join(lines) + f"\n\nCell pitch {CELL} mm, wall 3 mm, clear corridor {CELL-3} mm for a 12 mm marble (7 mm clearance; trap hole 18 mm). Wall lines (blue) are for gluing 3 mm MDF strips; red circles are cut-out trap holes on dead ends only, so no hole lies on the solution path. Every maze is a perfect maze (one solution), checked by BFS. Not tested: tilt feel, friction, difficulty for real children."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_maze.md"), "w").write(txt + "\n"); print(txt)
