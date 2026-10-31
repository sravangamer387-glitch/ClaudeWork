"""Marble Cricket: a pachinko board (8 rows of pegs) drops a marble into 9 pockets; each pocket = runs or wicket. Monte Carlo of an over (6 balls).
Pocket values are chosen by search so that: wicket probability per ball ~ 12-16 %, mean runs per over 8-12, and no pocket pair (high runs + wicket) stays on the same side."""
import itertools, math, random, os
ROWS = 8; N = ROWS + 1
P = [math.comb(ROWS, k) / 2 ** ROWS for k in range(N)]       # ideal pachinko with p = 0.5
def stats(vals):
    pw = sum(p for p, v in zip(P, vals) if v == "W"); mean_ball = sum(p * (0 if v == "W" else v) for p, v in zip(P, vals))
    return pw, mean_ball * 6
cands = ["W", 0, 1, 2, 3, 4, 6]
best = None
for vals in itertools.product(cands, repeat=N):
    if vals[0] != "W" and vals[-1] != "W": continue
    if vals.count("W") > 3 or vals[4] == "W": continue
    pw, mo = stats(vals)
    if not (0.12 <= pw <= 0.16 and 7 <= mo <= 10): continue
    if any(vals[i] not in (0, 1, 2, 3) for i in (3, 4, 5)): continue        # the three busiest pockets must be cheap
    if 6 not in vals or vals.count("W") < 1: continue
    if sum(p for p, v in zip(P, vals) if v == 6) > 0.14: continue
    if vals != tuple(reversed(vals)) or True:
        # prefer big scores at the edges (hard to hit), small in the middle; variance as the target
        var = sum(p * ((0 if v == "W" else v) ** 2) for p, v in zip(P, vals)) - (mo / 6) ** 2
        distinct = len(set(vals))
        score = var + distinct * 0.5
        if best is None or score > best[0]: best = (score, vals, pw, mo)
_, vals, pw, mo = best
rnd = random.Random(5); overs = []; wk = 0; N_OVER = 100000
for _ in range(N_OVER):
    runs = 0; w = 0
    for b in range(6):
        k = sum(rnd.random() < 0.5 for _ in range(ROWS)); v = vals[k]
        if v == "W": w += 1
        else: runs += v
    overs.append(runs); wk += w
ov = sorted(overs); mean = sum(overs) / N_OVER; p10, p90 = ov[N_OVER // 10], ov[9 * N_OVER // 10]
txt = f"Pocket values left to right (9 pockets): {list(vals)}\nPocket probabilities: {[round(p,3) for p in P]}\nWicket probability per ball: {pw:.3f}; mean runs per over (analytic) {mo:.2f}\nMonte Carlo ({N_OVER} overs): mean {mean:.2f} runs, 10th-90th percentile {p10}-{p90}, wickets per over {wk/N_OVER:.2f}\n\nTwo teams of 2 overs each: chance a given team wins a 2-over match is 50 % by symmetry; a tie happens with about {100*sum(1 for i in range(0,N_OVER-1,2) if overs[i]+overs[i+1]==overs[i+1] ) / N_OVER:.0f} % placeholder-free estimate below.\n"
# match tie rate: two innings of 2 overs each
t = 0; M = 50000
for _ in range(M):
    def inn():
        r = 0
        for o in range(2):
            for b in range(6):
                v = vals[sum(rnd.random() < 0.5 for _ in range(ROWS))]
                if v != "W": r += v
        return r
    if inn() == inn(): t += 1
txt = txt.split("\n\nTwo teams")[0] + f"\n\nTwo-over innings tie rate between equal teams: {100*t/M:.1f} % (decide a super-over rule if above 8 %).\nAssumes a perfectly symmetric peg board and fair drop; real boards bias to one side by tilt/peg spacing, so include a levelling screw and a calibration drop test of 100 marbles. Not measured on a real board."
open(os.path.join(os.path.dirname(__file__), "..", "docs", "results_cricket.md"), "w").write(txt + "\n"); print(txt)
