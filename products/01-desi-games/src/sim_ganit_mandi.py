#!/usr/bin/env python3
"""Balance simulations for Ganit Ladder (maths snakes & ladders) and Sabzi Mandi (change-making market game).
Usage: python3 -I sim_ganit_mandi.py"""
import random, statistics

# ------------------------------------------------------------------ Ganit Ladder
LADDERS = {4: 25, 13: 46, 33: 49, 42: 63, 50: 69, 62: 81, 74: 92}
SNAKES = {27: 5, 40: 3, 43: 18, 54: 31, 66: 45, 76: 58, 89: 53, 99: 41}
QUESTION_SQUARES = {6, 9, 11, 15, 17, 22, 24, 28, 32, 35, 39, 44, 47, 52, 56, 58, 61, 64, 71, 75, 78, 85, 91, 96}
PENALTY = 4                    # wrong answer on a question square: move back 4; correct answer: roll again

def move(pos, d):
    if pos + d > 100: return pos                     # exact finish required
    pos += d
    return LADDERS.get(pos, SNAKES.get(pos, pos))

def turn(pos, rng, accuracy):
    pos = move(pos, rng.randint(1, 6))
    while pos in QUESTION_SQUARES and pos != 100:
        if rng.random() < accuracy:                  # correct: roll again (may land on another question square)
            pos = move(pos, rng.randint(1, 6))
        else:                                        # wrong: back 3
            pos = max(1, pos - PENALTY); break
    return pos

def game(players, rng, accuracy):
    accs = accuracy if isinstance(accuracy, (list, tuple)) else [accuracy] * players
    pos = [0] * players; turns = 0
    while True:
        turns += 1
        for i in range(players):
            pos[i] = turn(pos[i], rng, accs[i])
            if pos[i] == 100: return i, turns

def ganit(n=20000, seed=3):
    rng = random.Random(seed); out = []
    out.append("| Players | Answer accuracy | Mean turns per player | 90th percentile | First-player win rate (fair = 1/players) |")
    out.append("|---|---|---|---|---|")
    ok = True
    for players in (2, 3, 4):
        for acc in (0.5, 0.8, 1.0):
            res = [game(players, rng, acc) for _ in range(n)]
            turns = [t for _, t in res]
            first = sum(1 for w, _ in res if w == 0) / n
            out.append(f"| {players} | {acc:.0%} | {statistics.mean(turns):.1f} | {sorted(turns)[int(n * 0.9)]} | {first:.1%} (fair {1 / players:.1%}) |")
            if acc == 0.8:
                ok &= 18 <= statistics.mean(turns) <= 45 and first - 1 / players < 0.06
    # head to head: does knowing the tables matter? (accuracy 90 % vs 50 %, 2 players, alternate who goes first)
    wins = 0
    for k in range(n):
        accs = [0.9, 0.5] if k % 2 == 0 else [0.5, 0.9]
        w, _ = game(2, rng, accs)
        wins += (w == 0) if k % 2 == 0 else (w == 1)
    share = wins / n
    out.append("")
    out.append(f"Head to head, 90 % accurate vs 50 % accurate player (first move alternated): the better mathematician wins {share:.1%} of games.")
    ok &= 0.58 <= share <= 0.78
    return out, ok

# ------------------------------------------------------------------ Sabzi Mandi
SWAPS = {20: {10: 1, 5: 2}, 10: {5: 2}, 5: {2: 2, 1: 1}, 2: {1: 2}}     # "chhutta": the bank breaks one note into smaller ones

def change_with_bank(till, amount):
    """Try exact change; if impossible, the shopkeeper may break ONE note at the bank (house rule). Returns (till, swapped)."""
    t = change(till, amount)
    if t is not None: return t, False
    for note in (20, 10, 5, 2):
        if till.get(note, 0) == 0: continue
        t2 = dict(till); t2[note] -= 1
        for d, k in SWAPS[note].items(): t2[d] = t2.get(d, 0) + k
        r = change(t2, amount)
        if r is not None: return r, True
    return None, False

def change(till, amount):
    """Greedy change from a till dict {denomination: count}; returns new till or None if impossible."""
    t = dict(till); rest = amount
    for d in (50, 20, 10, 5, 2, 1):
        k = min(rest // d, t.get(d, 0)); rest -= k * d; t[d] = t.get(d, 0) - k
    return t if rest == 0 else None

PRICES = [3, 4, 6, 7, 8, 9, 12, 14, 15, 18, 22, 25]          # price cards (rupees)
SALES_PER_SHIFT = 12                                           # one shopkeeper serves about 12 customers per game
START_TILL = {20: 1, 10: 3, 5: 6, 2: 10, 1: 12}                # shopkeeper's starting money cards
def mandi(n=20000, seed=5):
    rng = random.Random(seed)
    start = dict(START_TILL)
    fails = total = swaps = 0
    till = dict(start)
    for k in range(n):
        if k % SALES_PER_SHIFT == 0: till = dict(start)                # a new shopkeeper shift starts with the standard till
        items = rng.randint(1, 3); cost = sum(rng.choice(PRICES) for _ in range(items))
        while cost > 45: cost -= rng.choice(PRICES) if cost - 3 > 3 else 0; cost = max(cost, 3)   # a customer buys at most Rs 45 of goods
        pay = min(d for d in (5, 10, 20, 50, 100) if d >= cost)
        total += 1
        t2, swapped = change_with_bank(till, pay - cost)
        swaps += swapped
        if t2 is None:
            fails += 1; till = dict(start); continue            # shopkeeper must borrow: reset till, count the failure
        t2[pay] = t2.get(pay, 0) + 1                            # customer's note goes into the till
        till = t2
        for d in (100, 50):                                     # large notes are banked immediately (not usable as change)
            till[d] = 0
    return fails / total, swaps / total

if __name__ == "__main__":
    lines, ok = ganit()
    print("## Ganit Ladder"); print(); print("\n".join(lines)); print()
    print("PASS" if ok else "FAIL", ": game length 18-45 turns, first-player advantage < 6 points, and the better mathematician wins 58-78 %")
    rate, swaprate = mandi()
    print(); print("## Sabzi Mandi"); print()
    print(f"House rule: once per sale the shopkeeper may break one note at the bank. With it, change could not be made in {rate:.1%} of 20,000 simulated sales in shifts of 12 (the bank rule was needed in {swaprate:.1%} of sales) with the starting till (Rs 20 x1, 10 x3, 5 x6, 2 x10, 1 x12); purchases are capped at Rs 45 and customers pay with the smallest note of 5/10/20/50 that covers the bill.")
    print("PASS" if rate < 0.05 else "FAIL", ": change failure rate < 5 %")
