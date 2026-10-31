#!/usr/bin/env python3
"""Cricket Dhamaka balance search + verification (standard library only).
Each ball the batter secretly picks a shot (Defend/Drive/Slog) and the bowler a delivery (Yorker/Bouncer/Spin); a d6 is
rolled and read on the 3x3 table. We search for a table where: no pure strategy dominates, the equilibrium mixes all three
options for both players, average 2-over innings score is in a target band, and a wicket is neither rare nor constant.
Usage: python3 -I sim_cricket.py [search]   -> prints the chosen table + checks."""
import itertools, json, random, sys

OUTC = ["0", "1", "2", "4", "6", "W"]
RUNS = {"0": 0, "1": 1, "2": 2, "4": 4, "6": 6, "W": 0}
SHOTS = ["Defend", "Drive", "Slog"]
DELIV = ["Yorker", "Bouncer", "Spin"]
WICKET_COST = 5.0          # a wicket is worth about 5 runs of lost batting time (2 wickets per innings)

def cell_stats(faces):
    runs = sum(RUNS[f] for f in faces) / 6.0
    pw = sum(1 for f in faces if f == "W") / 6.0
    return runs, pw

def payoff(table):         # payoff to the batter, matrix[shot][deliv]
    return [[(lambda r, w: r - WICKET_COST * w)(*cell_stats(table[s][d])) for d in range(3)] for s in range(3)]

def solve(P, step=0.02):   # batter maximin over mixed strategies by grid search; bowler minimax likewise
    best = (-1e9, None)
    n = int(1 / step)
    for i in range(n + 1):
        for j in range(n + 1 - i):
            p = (i * step, j * step, 1 - i * step - j * step)
            worst = min(sum(p[s] * P[s][d] for s in range(3)) for d in range(3))
            if worst > best[0]: best = (worst, p)
    v, p = best
    bestq = (1e9, None)
    for i in range(n + 1):
        for j in range(n + 1 - i):
            q = (i * step, j * step, 1 - i * step - j * step)
            worst = max(sum(q[d] * P[s][d] for d in range(3)) for s in range(3))
            if worst < bestq[0]: bestq = (worst, q)
    return v, p, bestq[1]

def dominated(P):
    for a, b in itertools.permutations(range(3), 2):                      # batter: row a dominated by row b
        if all(P[b][d] >= P[a][d] for d in range(3)) and any(P[b][d] > P[a][d] for d in range(3)): return True
    for a, b in itertools.permutations(range(3), 2):                      # bowler: column a dominated by b (bowler minimises)
        if all(P[s][b] <= P[s][a] for s in range(3)) and any(P[s][b] < P[s][a] for s in range(3)): return True
    return False

def play_innings(table, p, q, rng, balls=12, wickets=2):
    runs = w = 0
    for _ in range(balls):
        s = rng.choices(range(3), p)[0]; d = rng.choices(range(3), q)[0]
        f = rng.choice(table[s][d])
        if f == "W":
            w += 1
            if w >= wickets: break
        else: runs += RUNS[f]
    return runs, w

def evaluate(table, n=4000, seed=1):
    P = payoff(table)
    v, p, q = solve(P)
    rng = random.Random(seed)
    scores = [play_innings(table, p, q, rng) for _ in range(n)]
    mean = sum(r for r, _ in scores) / n
    all_out = sum(1 for _, w in scores if w >= 2) / n
    return dict(value=v, p=p, q=q, mean=mean, all_out=all_out, dom=dominated(P), P=P)

ALLOWED = {  # what each shot can produce: sensible for a children's game
    0: (["0", "1", "2", "W"], [6, 5, 3, 2]),            # Defend: small scores, rarely out
    1: (["0", "1", "2", "4", "W"], [3, 4, 3, 3, 2]),    # Drive: up to a four
    2: (["0", "1", "4", "6", "W"], [3, 2, 3, 3, 3]),    # Slog: big or out
}

def wicket_rate(table, s):
    return sum(f == "W" for d in range(3) for f in table[s][d]) / 18.0

def search(iters=60000, seed=7):
    rng = random.Random(seed); best = None
    for _ in range(iters):
        t = [[sorted(rng.choices(ALLOWED[s][0], ALLOWED[s][1], k=6)) for _ in range(3)] for s in range(3)]
        if not (wicket_rate(t, 0) < wicket_rate(t, 1) < wicket_rate(t, 2)): continue   # riskier shot = more wickets
        P = payoff(t)
        if dominated(P): continue
        v, p, q = solve(P, 0.05)
        if min(p) < 0.15 or min(q) < 0.15: continue                      # every option must be used at equilibrium
        r = evaluate(t, 600)
        score = abs(r["mean"] - 17) + 20 * abs(r["all_out"] - 0.35)
        if best is None or score < best[0]: best = (score, t)
    return best[1]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        t = search(); print(json.dumps(t))
    else:
        FROZEN = json.load(open(__file__.replace("sim_cricket.py", "cricket_table.json")))
        r = evaluate(FROZEN, 20000)
        print(json.dumps(FROZEN))
        print("equilibrium batter mix", [round(x, 2) for x in r["p"]], "bowler mix", [round(x, 2) for x in r["q"]])
        print(f"mean 2-over score {r['mean']:.1f}, all-out rate {r['all_out']:.0%}, dominated strategy: {r['dom']}")
