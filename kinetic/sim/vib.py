"""KINETIC vibration model: synthetic bearing-fault vibration generator, order-tracked envelope features, tiny MLP, int8 export.

NOTHING HERE IS TRAINED ON REAL MACHINES. The data are synthetic, built from the textbook bearing-fault physics (impulse trains at BPFO/BPFI
exciting a structural resonance, amplitude-modulated for inner-race faults, plus 1x/2x unbalance and motor-ripple nuisance and non-periodic knocks).
The point of this file is the *pipeline* (features that use the known shaft speed, int8 inference that is bit-exact in C); retrain on real
recordings (e.g. the public CWRU/Paderborn sets or your own rig) before trusting any number it prints.
usage: python3 vib.py            -> trains, evaluates, writes ../firmware/lib/kn_vib_model.h and ../firmware/test/vib_vectors.h and ../docs/vib_results.md"""
import numpy as np, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
FS = 3200.0; N = 1024; DEC = 8; NE = N // DEC; FSE = FS / DEC           # raw window 1024 @3200 Hz (0.32 s), envelope 128 @400 Hz
BPFO, BPFI = 3.58, 5.42                                                    # order multiples of shaft speed (typical 6205-class deep-groove ball bearing, 9 balls)
CLASSES = ["healthy", "outer-race", "inner-race", "unbalance"]
FR_MIN, FR_MAX = 8.0, 25.0                                                 # operating window 480..1500 rpm
LP_HP = 1.0 - math.exp(-2 * math.pi * 300.0 / FS)                          # 1-pole low-pass used to build the high-pass (fc 300 Hz)
LP_EN = 1.0 - math.exp(-2 * math.pi * 150.0 / FS)                          # envelope smoothing (fc 150 Hz)
# ----------------------------------------------------------------- synthesis
def synth(cls, fr, rng, sev=None):
    t = np.arange(N) / FS; x = np.zeros(N)
    fr_t = fr * (1 + 0.01 * rng.standard_normal() )                         # speed ripple / measurement error of the commanded speed
    a1 = rng.uniform(0.01, 0.05) if cls != 3 else rng.uniform(0.1, 0.5)
    ph = rng.uniform(0, 2 * np.pi, 6)
    x += a1 * np.sin(2 * np.pi * fr_t * t + ph[0]) + a1 * rng.uniform(0.1, 0.5 if cls == 3 else 0.35) * np.sin(2 * np.pi * 2 * fr_t * t + ph[1])
    x += rng.uniform(0.0, 0.03) * np.sin(2 * np.pi * 4 * fr_t * t + ph[2]) + rng.uniform(0, 0.02) * np.sin(2 * np.pi * 8 * fr_t * t + ph[3])   # stepper torque ripple harmonics
    x += rng.uniform(0.01, 0.045) * rng.standard_normal(N)                  # sensor + structure noise
    for _ in range(rng.poisson(rng.uniform(0, 2.0) * N / FS)):               # non-periodic knocks (nuisance for every class)
        x = add_impulse(x, rng.uniform(0, N / FS), rng.uniform(0.05, 0.3), rng.uniform(700, 1100), t)
    if cls in (1, 2):
        A = np.exp(rng.uniform(np.log(0.04), np.log(0.5))) if sev is None else sev
        f_res = rng.uniform(700, 1100); order = BPFO if cls == 1 else BPFI; period = 1.0 / (order * fr_t); tk = rng.uniform(0, period)
        while tk < N / FS:
            amp = A * (1 + 0.8 * math.cos(2 * math.pi * fr_t * tk + ph[4]) if cls == 2 else 1.0) * rng.uniform(0.7, 1.3)
            x = add_impulse(x, tk, amp, f_res, t); tk += period * (1 + 0.015 * rng.standard_normal())   # roller slip: 1.5 % period jitter
    return x
def add_impulse(x, t0, amp, fres, t, tau=0.003):
    m = t >= t0; d = t[m] - t0; x[m] += amp * np.exp(-d / tau) * np.sin(2 * np.pi * fres * d); return x
# ----------------------------------------------------------------- features (the C code in kn_vib.c does exactly this in float32)
def goertzel_power(y, f, fs):
    n = len(y); w = 2 * np.pi * f / fs; c = 2 * np.cos(w); s1 = s2 = 0.0
    for v in y: s0 = v + c * s1 - s2; s2 = s1; s1 = s0
    return (s1 * s1 + s2 * s2 - c * s1 * s2) * 4.0 / (n * n)               # amplitude^2 of the sinusoid at f
def envelope(x):
    lp = 0.0; en = 0.0; out = np.zeros(N)
    for i, v in enumerate(x):
        lp += LP_HP * (v - lp); h = v - lp; en += LP_EN * (abs(h) - en); out[i] = en
    e = out[DEC // 2::DEC][:NE]; return e - e.mean()
def peak3(y, f, fs):
    d = fs / len(y); return max(goertzel_power(y, f + k * d, fs) for k in (-1, 0, 1))
def features(x, fr):
    x = x - x.mean(); r = math.sqrt((x * x).mean()) + 1e-9; k = (x ** 4).mean() / (r ** 4); cr = np.abs(x).max() / r
    e = envelope(x); ev = (e * e).mean() * 1.0 + 1e-12                      # envelope power (variance), for normalisation
    ep = lambda f: min(peak3(e, f, FSE) / ev, 4.0)
    rp = lambda f: min(peak3(x, f, FS) / (r * r), 4.0)
    return np.array([math.log10(r), k, cr, ep(fr), ep(BPFO * fr), ep(2 * BPFO * fr), ep(BPFI * fr), 0.5 * (ep(BPFI * fr + fr) + ep(BPFI * fr - fr)), rp(fr), rp(2 * fr)], np.float64)
NF = 10; FNAMES = ["log10 rms[g]", "kurtosis", "crest", "env@1x", "env@BPFO", "env@2BPFO", "env@BPFI", "env@BPFI+-1x", "raw@1x", "raw@2x"]
def make_set(n, rng, **kw):
    X = np.zeros((n, NF)); y = rng.integers(0, 4, n); fr = rng.uniform(FR_MIN, FR_MAX, n); W = np.zeros((n, N)); 
    for i in range(n):
        W[i] = synth(int(y[i]), fr[i], rng, **kw); X[i] = features(W[i], fr[i])
    return X, y, fr, W
# ----------------------------------------------------------------- tiny MLP (numpy Adam)
H1, H2 = 16, 8
def train(X, y, rng, epochs=60, lr=0.01):
    mu, sd = X.mean(0), X.std(0) + 1e-9; Z = (X - mu) / sd; n = len(Z)
    P = dict(W1=rng.standard_normal((NF, H1)) * math.sqrt(2 / NF), b1=np.zeros(H1), W2=rng.standard_normal((H1, H2)) * math.sqrt(2 / H1), b2=np.zeros(H2), W3=rng.standard_normal((H2, 4)) * math.sqrt(2 / H2), b3=np.zeros(4))
    m = {k: np.zeros_like(v) for k, v in P.items()}; v2 = {k: np.zeros_like(v) for k, v in P.items()}; step = 0
    for ep in range(epochs):
        idx = rng.permutation(n)
        for s in range(0, n, 64):
            b = idx[s:s + 64]; zb = Z[b]; yb = y[b]
            a1 = np.maximum(zb @ P["W1"] + P["b1"], 0); a2 = np.maximum(a1 @ P["W2"] + P["b2"], 0); lo = a2 @ P["W3"] + P["b3"]
            p = np.exp(lo - lo.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); d = p; d[np.arange(len(b)), yb] -= 1; d /= len(b)
            g = {"W3": a2.T @ d, "b3": d.sum(0)}; d2 = (d @ P["W3"].T) * (a2 > 0); g["W2"] = a1.T @ d2; g["b2"] = d2.sum(0); d1 = (d2 @ P["W2"].T) * (a1 > 0); g["W1"] = zb.T @ d1; g["b1"] = d1.sum(0)
            step += 1
            for k in P:
                m[k] = 0.9 * m[k] + 0.1 * g[k]; v2[k] = 0.999 * v2[k] + 0.001 * g[k] ** 2; P[k] -= lr * (m[k] / (1 - 0.9 ** step)) / (np.sqrt(v2[k] / (1 - 0.999 ** step)) + 1e-8)
        lr *= 0.95
    return P, mu, sd
def fwd_float(P, mu, sd, X):
    z = (X - mu) / sd; a = np.maximum(z @ P["W1"] + P["b1"], 0); a = np.maximum(a @ P["W2"] + P["b2"], 0); return a @ P["W3"] + P["b3"]
# ----------------------------------------------------------------- int8 quantisation (symmetric weights, int32 bias, float requant -- identical in C)
def quantise(P, mu, sd, Xcal):
    Z = (Xcal - mu) / sd; sx = max(np.abs(Z).max() / 127.0, 1e-6); s_in = np.float32(sx); layers = []; a = Z; s_prev = s_in
    ws = [("W1", "b1", True), ("W2", "b2", True), ("W3", "b3", False)]
    for W, b, relu in ws:
        sw = np.float32(np.abs(P[W]).max() / 127.0); Wq = np.clip(np.round(P[W] / sw), -127, 127).astype(np.int8); bq = np.round(P[b] / (sw * s_prev)).astype(np.int32)
        a_f = a @ P[W] + P[b]; a_f = np.maximum(a_f, 0) if relu else a_f
        s_out = np.float32(max(np.abs(a_f).max() / 127.0, 1e-6)); M = np.float32(sw * s_prev / s_out) if relu else np.float32(1.0)
        layers.append(dict(Wq=Wq.T.copy(), bq=bq, M=M, relu=relu)); a = a_f; s_prev = s_out      # Wq stored [out][in]
    return dict(s_in=s_in, layers=layers)
def infer_q(Q, mu, sd, x):
    z = (np.float32(x) - np.float32(mu)) / np.float32(sd); a = np.clip(np.floor(z / Q["s_in"] + np.float32(0.5)), -127, 127).astype(np.int32)
    for L in Q["layers"]:
        acc = L["Wq"].astype(np.int32) @ a + L["bq"]
        if L["relu"]: a = np.clip(np.floor(acc.astype(np.float32) * L["M"] + np.float32(0.5)), 0, 127).astype(np.int32)
        else: return acc
def export_header(Q, mu, sd, path):
    o = ["/* generated by sim/vib.py -- do not edit. Synthetic-data model; retrain on real recordings. */", "#ifndef KN_VIB_MODEL_H", "#define KN_VIB_MODEL_H", "#include <stdint.h>",
         f"#define KV_NF {NF}", f"#define KV_H1 {H1}", f"#define KV_H2 {H2}", "#define KV_NC 4", f"static const float kv_mu[KV_NF] = {{{', '.join('%.9gf' % v for v in mu)}}};", f"static const float kv_sd[KV_NF] = {{{', '.join('%.9gf' % v for v in sd)}}};", "static const float kv_sin = %.9gf;" % float(Q['s_in'])]
    for i, L in enumerate(Q["layers"], 1):
        o.append(f"static const int8_t kv_w{i}[{L['Wq'].shape[0]}][{L['Wq'].shape[1]}] = {{" + ", ".join("{" + ", ".join(str(int(v)) for v in r) + "}" for r in L["Wq"]) + "};")
        o.append(f"static const int32_t kv_b{i}[{len(L['bq'])}] = {{{', '.join(str(int(v)) for v in L['bq'])}}};"); mm = '%.9g' % float(L['M']); mm += '' if any(c in mm for c in '.e') else '.0'; o.append(f"static const float kv_m{i} = {mm}f;")
    o.append("#endif"); open(path, "w").write("\n".join(o) + "\n")
def main():
    rng = np.random.default_rng(7); print("generating..."); Xtr, ytr, _, _ = make_set(9000, rng); Xte, yte, frte, Wte = make_set(3000, np.random.default_rng(99)); print("training...")
    P, mu, sd = train(Xtr, ytr, rng); Q = quantise(P, mu, sd, Xtr)
    pf = fwd_float(P, mu, sd, Xte).argmax(1); pq = np.array([infer_q(Q, mu, sd, x).argmax() for x in Xte]); accf = (pf == yte).mean(); accq = (pq == yte).mean()
    cm = np.zeros((4, 4), int)
    for a, b in zip(yte, pq): cm[a, b] += 1
    def sweep(label, **kw):
        X2, y2, _, _ = make_set(600, np.random.default_rng(5), **kw); p = np.array([infer_q(Q, mu, sd, x).argmax() for x in X2]); return (p == y2).mean()
    # per-severity recall for faulty classes
    sev_rows = []
    for sev in (0.04, 0.08, 0.15, 0.3, 0.5):
        r = np.random.default_rng(11); ok = 0; tot = 0
        for cls in (1, 2):
            for _ in range(150):
                fr = r.uniform(FR_MIN, FR_MAX); x = synth(cls, fr, r, sev=sev); ok += infer_q(Q, mu, sd, features(x, fr)).argmax() == cls; tot += 1
        sev_rows.append((sev, ok / tot))
    healthy_fa = 1 - cm[0, 0] / cm[0].sum()
    ram_w = sum(L["Wq"].size for L in Q["layers"]); print(f"float acc {accf:.3f}  int8 acc {accq:.3f}  weights {ram_w} B"); 
    export_header(Q, mu, sd, os.path.join(HERE, "..", "firmware", "lib", "kn_vib_model.h"))
    # test vectors: 40 raw windows as int16 counts at 1 mg/LSB-ish scale (4 mg/LSB, ADXL345 full-res typical 3.9 mg/LSB) + shaft speed + python features + python int8 class
    LSB = 0.0039; V = []; r = np.random.default_rng(2024)
    with open(os.path.join(HERE, "..", "firmware", "test", "vib_vectors.h"), "w") as f:
        f.write("/* generated by sim/vib.py */\n#define VV_N 24\n#define VV_LSB 0.0039f\nstatic const float vv_fr[VV_N] = {"); sel = []
        for c in range(4):
            for k in range(6):
                fr = r.uniform(FR_MIN, FR_MAX); x = synth(c, fr, r); q = np.clip(np.round(x / LSB), -2048, 2047).astype(np.int16); xq = q.astype(np.float64) * LSB; sel.append((c, fr, q, features(xq, fr), infer_q(Q, mu, sd, features(xq, fr)).argmax()))
        f.write(", ".join("%.6ff" % s[1] for s in sel) + "};\nstatic const int vv_label[VV_N] = {" + ", ".join(str(s[0]) for s in sel) + "};\nstatic const int vv_pred[VV_N] = {" + ", ".join(str(int(s[4])) for s in sel) + "};\n")
        f.write("static const float vv_feat[VV_N][%d] = {" % NF + ", ".join("{" + ", ".join("%.7gf" % v for v in s[3]) + "}" for s in sel) + "};\nstatic const int16_t vv_win[VV_N][%d] = {" % N + ", ".join("{" + ", ".join(str(int(v)) for v in s[2]) + "}" for s in sel) + "};\n")
    md = ["# KINETIC vibration model results (SYNTHETIC data only)\n", f"Model: {NF} order-tracked features -> MLP {NF}-{H1}-{H2}-4, int8 weights ({ram_w} bytes), float requantisation. Window {N} samples at {FS:.0f} Hz ({N/FS:.2f} s). Shaft-speed window {FR_MIN*60:.0f}-{FR_MAX*60:.0f} rpm.\n",
          f"Held-out synthetic test set (3000 windows, different seed): **float {accf*100:.1f} %, int8 {accq*100:.1f} %**. Healthy windows flagged as faulty: **{healthy_fa*100:.1f} %**.\n", "\nConfusion matrix (rows true, columns predicted, int8):\n", "| true \\ pred | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * 4]
    for i in range(4): md.append(f"| {CLASSES[i]} | " + " | ".join(str(v) for v in cm[i]) + " |")
    md += ["\nRace-fault recall by impulse amplitude (synthetic, g at the resonance; 300 windows each):\n", "| impulse amplitude | recall |", "|---|---|"] + [f"| {s:.2f} g | {v*100:.0f} % |" for s, v in sev_rows]
    md += ["\n**What this does and does not show.** The pipeline is internally consistent and the C implementation reproduces the Python features and classes (see test). The accuracy is for *this simulator*, whose faults are cleaner than real ones: real rigs add looseness, gear mesh, resonance shifts, load-dependent amplitudes and sensor-mounting effects. Expect a real-data accuracy well below these numbers until the model is retrained on recordings from the real machine. No claim of field performance is made.\n"]
    open(os.path.join(HERE, "..", "docs", "vib_results.md"), "w").write("\n".join(md)); print("\n".join(md[:6]))
if __name__ == "__main__": main()
