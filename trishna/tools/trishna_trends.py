#!/usr/bin/env python3
"""Daily hydration / electrolyte trend report from the bridge CSV (no third-party packages).

  python3 trishna_trends.py trishna.csv [--baseline-days 14]

For each day: number of good events, median SG estimate, median EC25, first-morning SG, share of events in each hydration class,
and an electrolyte-shift z-score: (day median EC25 - personal baseline median) / baseline robust spread (1.4826 x MAD over the
previous N days). |z| >= 2 on several consecutive days is a trend worth noting - it is NOT a diagnosis; see the manual's limits section."""
import argparse, csv, statistics as st, time
from collections import defaultdict


def mad(xs):
    m = st.median(xs); return st.median([abs(x - m) for x in xs]) * 1.4826


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--baseline-days", type=int, default=14); a = ap.parse_args()
    days = defaultdict(list)
    for r in csv.DictReader(open(a.csv)):
        if r["type"] != "result" or float(r["quality"] or 0) < 50 or not r["sg"]:
            continue
        ts = int(r["unix_s"]) if r["unix_s"] not in ("", "0") else None
        if ts is None:
            continue                                   # no clock (Wi-Fi/SNTP not set): cannot place the event in a day
        lt = time.localtime(ts)
        days[time.strftime("%Y-%m-%d", lt)].append((lt.tm_hour, float(r["sg"]), float(r["ec25_mscm"]), r["hydration"]))
    order = sorted(days)
    print(f"{'day':10} {'n':>3} {'SG med':>7} {'SG am':>7} {'EC25 med':>8} {'z(EC)':>6}  hydration mix")
    for i, d in enumerate(order):
        ev = sorted(days[d]); sgs = [e[1] for e in ev]; ecs = [e[2] for e in ev]
        am = [e[1] for e in ev if 4 <= e[0] < 10]
        prev = [x for dd in order[max(0, i - a.baseline_days):i] for x in [e[2] for e in days[dd]]]
        z = ""
        if len(prev) >= 10 and mad(prev) > 1e-6:
            z = f"{(st.median(ecs) - st.median(prev)) / mad(prev):+.1f}"
        mix = defaultdict(int)
        for e in ev:
            mix[e[3]] += 1
        print(f"{d:10} {len(ev):3d} {st.median(sgs):7.4f} {(f'{am[0]:.4f}' if am else '   -'):>7} {st.median(ecs):8.2f} {z:>6}  " + ", ".join(f"{k} {v}" for k, v in sorted(mix.items())))


if __name__ == "__main__":
    main()
