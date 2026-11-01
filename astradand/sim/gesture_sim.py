"""ASTRADAND gesture recognition: synthetic wand traces + reference recogniser (same algorithm as firmware/lib/ad_core.c).
Wand axes: x along the wand (tip direction), y left, z up. Drawing in the air = tip direction (yaw, pitch) changing: path = integral of the world-frame
pitch/yaw rates. Gyro +-1000 dps (32.8 LSB/dps), accelerometer +-2 g (16384 LSB/g), 50 Hz sampling. ALL TRACES ARE SYNTHETIC: real hands differ (see docs)."""
import math, json, sys, os
import numpy as np
FS = 50; DT = 1.0 / FS; GLSB = 32.8; ALSB = 16384.0; M = 16
NAMES = ["agni", "vajra", "jala", "raksha", "prakash", "vayu"]
def circle(n=200):
    t = np.linspace(0, 2 * math.pi, n); return np.c_[0.9 * np.sin(t), 0.9 * np.cos(t)]            # start at top, clockwise
def poly(pts, n=60):
    pts = np.array(pts, float); out = []
    for a, b in zip(pts[:-1], pts[1:]): out += [a + (b - a) * k / n for k in range(n)]
    out.append(pts[-1]); return np.array(out)
SHAPES = {
 "agni": circle(),
 "vajra": poly([(-0.5, 0.8), (0.5, 0.8), (-0.5, -0.8), (0.5, -0.8)]),
 "jala": np.c_[np.linspace(-1, 1, 200), 0.6 * np.sin(np.linspace(0, 4 * math.pi, 200))],
 "raksha": poly([(0, 0.8), (0.8, -0.6), (-0.8, -0.6), (0, 0.8)]),
 "prakash": poly([(0, -0.9), (0, 0.9)]),
 "vayu": poly([(-0.8, 0.2), (-0.3, -0.6), (0.9, 0.9)]),
}
def resample(P, m=M):
    P = np.asarray(P, float); d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; L = d[-1]
    if L < 1e-9: return None, 0.0
    s = np.linspace(0, L, m); return np.c_[np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], L
def normalise(Q):
    Q = Q - Q.mean(axis=0); w = np.ptp(Q[:, 0]); h = np.ptp(Q[:, 1]); sc = max(w, h)
    return Q / sc if sc > 1e-9 else Q
TEMPL = {k: normalise(resample(v)[0]) for k, v in SHAPES.items()}
def rot(Q, a): c, s = math.cos(a), math.sin(a); return Q @ np.array([[c, s], [-s, c]])
ROTS = [math.radians(r) for r in (-20, -10, 0, 10, 20)]
D_MAX = 0.14; MARGIN = 0.10; MIN_EXTENT_DEG = 12.0
def classify_path(P):
    Q, L = resample(P)
    if Q is None or max(np.ptp(P[:, 0]), np.ptp(P[:, 1])) < MIN_EXTENT_DEG: return None, 9.0, 0.0       # extent (not path length): hand tremor has length but no size
    Q = normalise(Q); best = []
    for name in NAMES:
        d = min(float(np.mean(np.hypot(*(rot(Q, a) - TEMPL[name]).T))) for a in ROTS); best.append((d, name))
    best.sort(); d1, n1 = best[0]; d2 = best[1][0]; conf = (d2 - d1) / d2
    if d1 > D_MAX or conf < MARGIN: return None, d1, conf
    return n1, d1, conf
def synth(name, rng, hard=1.0, roll_max=35.0, raw=False):
    """gyro/accel trace (50 Hz) for one cast; returns raw int16-like arrays and the true class"""
    S = 1.0 if raw else rng.uniform(15, 40); T = rng.uniform(0.7, 1.7); rho = math.radians(np.clip(rng.normal(0, 8 * hard), -20, 20))
    base = SHAPES[name] if isinstance(name, str) else name
    P = rot(np.asarray(base) * S, rho)                                              # degrees
    n = int(T * FS); u = np.linspace(0, 1, n); u = 10 * u ** 3 - 15 * u ** 4 + 6 * u ** 5                  # minimum-jerk timing
    idx = u * (len(P) - 1); x = np.interp(idx, np.arange(len(P)), P[:, 0]); y = np.interp(idx, np.arange(len(P)), P[:, 1])
    pre = int(rng.uniform(0.3, 0.7) * FS); post = int(rng.uniform(0.15, 0.4) * FS)
    x = np.r_[np.full(pre, x[0]), x, np.full(post, x[-1])]; y = np.r_[np.full(pre, y[0]), y, np.full(post, y[-1])]
    N = len(x); t = np.arange(N) * DT
    for arr in (x, y):                                                              # hand tremor 5-9 Hz, 0.3-0.7 deg
        arr += rng.uniform(0.3, 0.7) * hard * np.sin(2 * math.pi * rng.uniform(5, 9) * t + rng.uniform(0, 6.28))
    wz = np.gradient(x, DT); wy = np.gradient(y, DT)                                # deg/s: yaw rate, pitch rate (world)
    phi = math.radians(rng.uniform(-roll_max, roll_max)); c, s = math.cos(phi), math.sin(phi)
    gy = c * wy + s * wz; gz = -s * wy + c * wz; gx = rng.normal(0, 4, N) * hard                         # body-frame rates (roll rate = noise)
    bias = rng.normal(0, 1.5, 3); noise = 0.15 * hard
    g = np.c_[gx + bias[0], gy + bias[1], gz + bias[2]] + rng.normal(0, noise, (N, 3))
    a = np.c_[rng.normal(0, 0.01, N), np.full(N, math.sin(phi)), np.full(N, math.cos(phi))] + rng.normal(0, 0.01, (N, 3))
    trig = np.zeros(N, bool); trig[max(pre - int(0.15 * FS), 0):N - max(post - int(0.1 * FS), 0)] = True            # button held around the stroke
    return (np.clip(np.round(g * GLSB), -32768, 32767).astype(np.int16), np.clip(np.round(a * ALSB), -32768, 32767).astype(np.int16), trig)
def recognise(g, a, trig, bias_deg=None):
    """firmware algorithm: bias from the samples before the trigger, roll from gravity at trigger, integrate to a path, classify"""
    first = int(np.argmax(trig)); rest = g[max(first - 12, 0):first].astype(float) / GLSB
    b = rest.mean(axis=0) if len(rest) >= 6 else np.zeros(3) if bias_deg is None else bias_deg
    a0 = a[first:first + 5].astype(float).mean(axis=0) / ALSB; phi = math.atan2(a0[1], a0[2]); c, s = math.cos(phi), math.sin(phi)
    x = y = 0.0; P = []
    for k in range(first, len(g)):
        if not trig[k]: break
        wy = (g[k, 1] / GLSB - b[1]); wz = (g[k, 2] / GLSB - b[2]); wyw = c * wy - s * wz; wzw = s * wy + c * wz            # undo roll
        x += wzw * DT; y += wyw * DT; P.append((x, y))
    return classify_path(np.array(P)) if len(P) > 4 else (None, 9.0, 0.0)
def scribble(rng):
    pts = np.cumsum(rng.normal(0, 1, (rng.integers(5, 9), 2)), axis=0) * rng.uniform(8, 20); return poly(pts, 20)
def run(trials=300, seed=7, hard=1.0):
    rng = np.random.default_rng(seed); conf = np.zeros((len(NAMES), len(NAMES) + 1), int)                 # last column = rejected (fizzle)
    for i, nm in enumerate(NAMES):
        for _ in range(trials):
            res, d, c = recognise(*synth(nm, rng, hard)); conf[i, NAMES.index(res) if res else len(NAMES)] += 1
    fa = {"random scribble": 0, "tiny shake (<5 deg)": 0, "horizontal sweep (60 deg)": 0}; N = trials
    for _ in range(N):
        if recognise(*synth(scribble(rng), rng, hard, raw=True))[0]: fa["random scribble"] += 1
        small = poly([(0, 0), (rng.uniform(-1, 1), rng.uniform(-1, 1))], 10) * 3.0
        if recognise(*synth(small, rng, hard, raw=True))[0]: fa["tiny shake (<5 deg)"] += 1
        sweep = poly([(-1, rng.uniform(-.1, .1)), (1, rng.uniform(-.1, .1))], 30) * 30
        if recognise(*synth(sweep, rng, hard, raw=True))[0]: fa["horizontal sweep (60 deg)"] += 1
    return conf, fa, N
if __name__ == "__main__":
    out = []
    for hard in (1.0, 1.6):
        conf, fa, N = run(300, 7, hard); acc = np.trace(conf[:, :6]) / conf.sum()
        rej = conf[:, 6].sum() / conf.sum(); wrong = (conf[:, :6].sum() - np.trace(conf[:, :6])) / conf.sum()
        out.append(f"### Noise/variation level x{hard}  (300 casts per spell)\n\naccuracy {acc*100:.1f} %, fizzled (rejected) {rej*100:.1f} %, wrong spell {wrong*100:.1f} %\n\n| true \\ result | " + " | ".join(NAMES) + " | fizzle |\n|---|" + "---|" * 7)
        for i, nm in enumerate(NAMES): out.append(f"| {nm} | " + " | ".join(str(v) for v in conf[i]) + " |")
        out.append(f"\nFalse casts from non-spells ({N} each): " + ", ".join(f"{k} {v} ({100*v/N:.1f} %)" for k, v in fa.items()) + "\n")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "gesture_results.md"), "w").write("# Gesture recognition on synthetic traces\n\nSynthetic only: minimum-jerk strokes, 15-40 deg size, 0.7-1.7 s, tilt of drawing +-20 deg, wand roll +-35 deg, gyro bias +-1.5 deg/s, 0.15 deg/s noise, 5-9 Hz tremor. Real hands will do worse until tuned on recorded data.\n\n" + "\n".join(out))
    print("\n".join(out))
