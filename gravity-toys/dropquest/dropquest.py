"""Drop Quest v1: rules, simulator, exact solver and level generator (60 levels, each with exactly one solution).
Rules (v1, laser-cut version):
- 5 x 5 board. Every cell is floor (height 0) or holds one TOWER of height 1, 2 or 3 units. A tower may carry a DEFLECTOR cap: a 45-degree wall, "/" or "\\" (rotate the cap 90 deg to swap), that reflects the marble by 90 deg.
- The marble is released from the START socket on the left edge (row rs) at height 3, rolling right (east).
- It rolls straight from cell to cell. Entering a cell that is LOWER or EQUAL: it drops onto it and keeps rolling. Entering a HIGHER cell: blocked -> fail.
- On a deflector it turns 90 deg (L or R) and keeps rolling. Rolling off the board -> fail, except through the TARGET gate on the right edge (row rt) at floor height 0... the marble must leave the last column rolling east at height 0 at row rt.
- A level fixes some pieces on the board and hands the player a set of loose pieces; the player places ALL loose pieces on empty cells so that the marble reaches the target AND touches every placed loose piece.
- Levels are accepted only if exactly one placement solves them (verified by exhaustive search)."""
import itertools, json, random, sys, os
N = 5; DIRS = {"E": (0, 1), "S": (1, 0), "W": (0, -1), "N": (-1, 0)}
MIRROR = {"/": {"E": "N", "N": "E", "W": "S", "S": "W"}, "\\": {"E": "S", "S": "E", "W": "N", "N": "W"}}   # 45-degree deflector walls (a cap rotated 90 deg swaps / and \\)
def simulate(board, rs, rt):
    """board: dict (r, c) -> (height, deflector or None). Returns (success, path list of cells)."""
    r, c, d, h = rs, -1, "E", 3; path = []; seen = set()
    for _ in range(60):
        dr, dc = DIRS[d]; nr, nc = r + dr, c + dc
        if not (0 <= nr < N and 0 <= nc < N):
            return (d == "E" and nc == N and nr == rt and h == 0), path
        nh, defl = board.get((nr, nc), (0, None))
        if nh > h: return False, path
        r, c, h = nr, nc, nh; path.append((r, c))
        if defl: d = MIRROR[defl][d]
        st = (r, c, d, h)
        if st in seen: return False, path
        seen.add(st)
    return False, path
def solutions(fixed, loose, rs, rt, limit=2):
    """Count placements of the loose pieces (list of (h, defl)) on empty cells that solve the level; stop at `limit`."""
    empty = [(r, c) for r in range(N) for c in range(N) if (r, c) not in fixed]
    found = []
    pieces = list(loose); k = len(pieces)
    def rec(i, board, used):
        if len(found) >= limit: return
        if i == k:
            ok, path = simulate(board, rs, rt)
            if ok and all(cell in path for cell in used): found.append(dict(used))
            return
        h, df = pieces[i]
        for cell in empty:
            if cell in used: continue
            if i > 0 and pieces[i - 1] == pieces[i] and any(used[cc] == pieces[i] and cell <= cc for cc in used): continue   # identical pieces: ordered placement
            board[cell] = (h, df); used[cell] = (h, df); rec(i + 1, board, used); del board[cell]; del used[cell]
    rec(0, dict(fixed), {})
    return found
def random_level(rng, n_loose, n_fixed):
    """Build a solved board by walking a path, then hide n_loose of the path pieces."""
    for _ in range(400):
        rs, rt = rng.randrange(N), rng.randrange(N)
        r, c, d, h = rs, -1, "E", 3; board = {}; path = []
        okay = False
        for step in range(14):
            dr, dc = DIRS[d]; nr, nc = r + dr, c + dc
            if not (0 <= nr < N and 0 <= nc < N) or (nr, nc) in board: break
            # choose a height <= h; floor allowed only late
            nh = rng.choice([x for x in range(0, h + 1)]) if step > 0 else rng.choice([2, 3])
            defl = None
            if nh > 0 and rng.random() < 0.45: defl = rng.choice("/\\")
            board[(nr, nc)] = (nh, defl); path.append((nr, nc)); r, c, h = nr, nc, nh
            if defl: d = MIRROR[defl][d]
            if d == "E" and c == N - 1 and r == rt and h == 0: okay = True; break
        if not okay: continue
        board = {k: v for k, v in board.items() if v != (0, None)}       # plain floor cells are not pieces
        ok, p = simulate(board, rs, rt)
        if not ok: continue
        cand = [k for k in board]
        if len(cand) < n_loose: continue
        hide = rng.sample(cand, n_loose); fixed = {k: v for k, v in board.items() if k not in hide}
        # distractor fixed pieces off the path
        free = [(rr, cc) for rr in range(N) for cc in range(N) if (rr, cc) not in board]
        for cell in rng.sample(free, min(n_fixed, len(free))): fixed[cell] = (rng.choice([1, 2, 3]), None)
        if not simulate({**fixed, **{k: board[k] for k in hide}}, rs, rt)[0]: continue
        loose = sorted((board[k] for k in hide), key=lambda p: (p[0], p[1] or ""))
        if len(solutions(fixed, loose, rs, rt, 2)) == 1: return dict(rs=rs, rt=rt, fixed={f"{k[0]},{k[1]}": v for k, v in fixed.items()}, loose=loose, solution={f"{k[0]},{k[1]}": board[k] for k in hide})
    return None
BANDS = [("green", 2, 2, 15), ("blue", 3, 3, 15), ("red", 4, 3, 15), ("black", 5, 4, 15)]
def generate(seed=2026):
    rng = random.Random(seed); levels = []
    for band, nl, nf, count in BANDS:
        made = 0
        while made < count:
            L = random_level(rng, nl, nf)
            if L and L not in levels: L["band"] = band; L["id"] = len(levels) + 1; levels.append(L); made += 1
    return levels
def verify(levels):
    bad = []
    for L in levels:
        fixed = {tuple(map(int, k.split(","))): tuple(v) for k, v in L["fixed"].items()}; loose = [tuple(x) for x in L["loose"]]
        s = solutions(fixed, loose, L["rs"], L["rt"], 3)
        sol = {tuple(map(int, k.split(","))): tuple(v) for k, v in L["solution"].items()}
        if len(s) != 1 or s[0] != sol: bad.append(L["id"])
    return bad
def card(L):
    g = [["." for _ in range(N)] for _ in range(N)]
    for k, (h, df) in L["fixed"].items(): r, c = map(int, k.split(",")); g[r][c] = f"{h}{df or ''}"
    rows = []
    for r in range(N): rows.append(("S> " if r == L["rs"] else "   ") + " ".join(f"{x:>3}" for x in g[r]) + (" >T" if r == L["rt"] else ""))
    return "\n".join(rows)
if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    levels = generate(); bad = verify(levels)
    json.dump(levels, open(os.path.join(out, "levels.json"), "w"), indent=0)
    md = ["# Drop Quest v1: 60 challenge cards (generated and verified: exactly one solution each)", "", "Legend: number = tower height in units, / or \\ = deflector wall direction as seen from above (north at the top), `.` = empty floor, `S>` start row (marble released at height 3 rolling right), `>T` target row. Place ALL loose pieces; the marble must touch each of them.", ""]
    for L in levels:
        md += [f"## Card {L['id']} ({L['band']})", "", "```", card(L), "```", "", "Loose pieces: " + ", ".join(f"tower {h}" + (f" + deflector {df}" if df else "") for h, df in L["loose"]), "",
               "<details><summary>Solution (card back)</summary>", "", ", ".join(f"row {int(k.split(',')[0]) + 1} col {int(k.split(',')[1]) + 1}: {v[0]}{v[1] or ''}" for k, v in L["solution"].items()), "", "</details>", ""]
    open(os.path.join(out, "CARDS.md"), "w").write("\n".join(md))
    print(f"{len(levels)} levels; bands", {b: sum(1 for L in levels if L['band'] == b) for b, *_ in BANDS}, "; non-unique or wrong:", bad)
    sys.exit(1 if bad or len(levels) != 60 else 0)
