"""Gateway-side anomaly detector for buried geotechnical / foundation nodes.
A node streams short acceleration windows (here 2 s at 200 Hz) and slow strain/tilt readings. The gateway must tell apart:
  AMBIENT  - broadband low-level noise (wind, distant traffic, electronics)
  VEHICLE  - a heavy vehicle passing: energy concentrated in 3-20 Hz, smooth envelope, 3-15 s long, no sharp impulses
  CRACK    - concrete cracking / shifting: short broadband impulses (stick-slip, microcracks) with energy well above 20 Hz, often repeated
The detector is a transparent feature + threshold design (not a trained black box), calibrated on SYNTHETIC data produced by `synth()` below.
Real structures differ strongly (coupling, soil, sensor mounting): thresholds MUST be re-derived from a baseline recording at the installation.
"""
import numpy as np
FS = 200.0; WIN = int(2 * FS)

def synth(kind, rng, n=WIN):
    t = np.arange(n) / FS; x = rng.normal(0, 0.004, n)                                  # sensor + ambient noise floor (g)
    if kind == "vehicle":
        f0 = rng.uniform(5, 14); env = np.hanning(n) ** 1.5; a = rng.uniform(0.02, 0.08)
        x += a * env * (np.sin(2 * np.pi * f0 * t + rng.uniform(0, 6.28)) + 0.5 * np.sin(2 * np.pi * 2 * f0 * t + rng.uniform(0, 6.28)))
    elif kind == "crack":
        for _ in range(rng.integers(1, 5)):
            t0 = rng.uniform(0.1, 1.7); a = rng.uniform(0.03, 0.12); fr = rng.uniform(40, 90); d = t - t0; m = d >= 0
            x[m] += a * np.exp(-d[m] / 0.012) * np.sin(2 * np.pi * fr * d[m])
    elif kind == "ambient_gust":
        x += rng.normal(0, 0.01, n) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.2, 1) * t) ** 2)
    return x

def features(x):
    x = x - x.mean(); r = np.sqrt((x ** 2).mean()) + 1e-12
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2; f = np.fft.rfftfreq(len(x), 1 / FS); tot = X.sum() + 1e-18
    low = X[(f >= 3) & (f < 20)].sum() / tot; high = X[(f >= 30)].sum() / tot
    k = (x ** 4).mean() / (r ** 4); crest = np.abs(x).max() / r
    return dict(rms=r, low_frac=low, high_frac=high, kurtosis=k, crest=crest, peak=float(np.abs(x).max()))

class Detector:
    """thresholds: peak_event + kurtosis_impulse + high_frac_crack decide crack; rms_event separates ambient from vehicles (all calibrated on the install-time baseline)."""
    def __init__(self, rms_event=0.012, kurt_impulse=6.0, high_crack=0.25, peak_event=0.03):
        self.rms_event, self.kurt, self.high, self.peak_event = rms_event, kurt_impulse, high_crack, peak_event
    def classify(self, x):
        f = features(x)
        if f["kurtosis"] > self.kurt and f["high_frac"] > self.high and f["peak"] > self.peak_event: return "crack", f      # impulses are tested first: a weak crack barely raises the RMS
        if f["rms"] < self.rms_event: return "ambient", f
        if f["low_frac"] > 0.6: return "vehicle", f
        return "ambient", f
    @staticmethod
    def calibrate(baseline_windows, k=6.0):
        """rms_event = mean + k * std of the baseline window rms values (install-time ambient recording)"""
        fs = [features(w) for w in baseline_windows]; r = np.array([f["rms"] for f in fs]); p = np.array([f["peak"] for f in fs])
        return Detector(rms_event=float(r.mean() + k * r.std()), peak_event=float(p.mean() + 6 * p.std()))

class CrackTracker:
    """A single crack-class window may be noise; the structural alarm needs repeated cracks: >= n in the last `horizon` windows."""
    def __init__(self, n=3, horizon=30): self.n, self.h, self.hist = n, horizon, []
    def update(self, label):
        self.hist.append(label == "crack"); self.hist = self.hist[-self.h:]; return sum(self.hist) >= self.n

def evaluate(seed=3, n=300):
    rng = np.random.default_rng(seed); base = [synth("ambient", rng) for _ in range(80)]; det = Detector.calibrate(base)
    kinds = ["ambient", "ambient_gust", "vehicle", "crack"]; conf = {k: {} for k in kinds}
    for k in kinds:
        for _ in range(n):
            lab, _ = det.classify(synth(k, rng)); lab = "ambient" if k == "ambient_gust" and lab == "ambient" else lab
            conf[k][lab] = conf[k].get(lab, 0) + 1
    return det, conf

if __name__ == "__main__":
    det, conf = evaluate(); print("calibrated rms_event = %.4f g" % det.rms_event)
    for k, v in conf.items(): print(f"{k:14s}", v)
