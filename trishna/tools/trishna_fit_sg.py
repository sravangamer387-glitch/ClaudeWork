#!/usr/bin/env python3
"""Fit the device's specific-gravity model to your own refractometer readings, then print the console command that stores it.

Model (firmware trishna_sense.c):  SG = 1 + c_ec * EC25[mS/cm] + c_a450 * A450 + c0

1. Run the bridge with --csv trishna.csv for a few days.
2. For each event you also measure with a handheld urine refractometer (catch a few mL from the same stream in a clean cup),
   write a line in refractometer.csv:   event_id,sg        e.g.   57,1.018
   Aim for at least 10 events spread over morning (concentrated) and after-drinking (dilute) samples.
3. python3 trishna_fit_sg.py trishna.csv refractometer.csv
   -> prints the fit, its error, and   cal sg <c_ec> <c_a450> <c0>   to type into the device console (then 'save').
No numpy needed (3x3 normal equations solved directly)."""
import csv, sys


def solve3(A, b):
    import copy
    M = [row[:] + [b[i]] for i, row in enumerate(copy.deepcopy(A))]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-15:
            raise ValueError("singular: need more varied samples")
        M[c], M[p] = M[p], M[c]
        for r in range(3):
            if r != c:
                k = M[r][c] / M[c][c]
                M[r] = [M[r][j] - k * M[c][j] for j in range(4)]
    return [M[i][3] / M[i][i] for i in range(3)]


def main(frames_csv, ref_csv):
    res = {}
    for r in csv.DictReader(open(frames_csv)):
        if r["type"] == "result" and float(r["quality"] or 0) >= 50:
            res[int(r["event_id"])] = (float(r["ec25_mscm"]), float(r["a450"]))
    pts = []
    for r in csv.reader(open(ref_csv)):
        if not r or r[0].startswith("#") or not r[0].strip().isdigit():
            continue
        e, sg = int(r[0]), float(r[1])
        if e in res:
            pts.append((res[e][0], res[e][1], sg))
    if len(pts) < 5:
        sys.exit(f"only {len(pts)} matched events with quality >= 50: collect at least 5 (10+ recommended)")
    # least squares on y = SG - 1 = c_ec*x1 + c_a450*x2 + c0
    X = [(x1, x2, 1.0) for x1, x2, _ in pts]; y = [sg - 1.0 for _, _, sg in pts]
    A = [[sum(X[k][i] * X[k][j] for k in range(len(X))) for j in range(3)] for i in range(3)]
    b = [sum(X[k][i] * y[k] for k in range(len(X))) for i in range(3)]
    c_ec, c_a, c0 = solve3(A, b)
    err = [(1 + c_ec * x1 + c_a * x2 + c0) - sg for x1, x2, sg in pts]
    rmse = (sum(e * e for e in err) / len(err)) ** 0.5
    print(f"{len(pts)} paired events. Fit: SG = 1 + {c_ec:.6f}*EC25 + {c_a:.5f}*A450 + {c0:.5f}")
    print(f"RMS error {rmse:.4f} SG units, worst {max(abs(e) for e in err):.4f}")
    if rmse > 0.004:
        print("WARNING: RMS error above 0.004 - conductivity alone is not tracking your SG well (e.g. high urea/glucose fraction); treat SG as a trend only.")
    print(f"\nDevice console:\n  cal sg {c_ec:.6f} {c_a:.5f} {c0:.5f}\n  save")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
