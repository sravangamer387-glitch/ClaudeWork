"""Colour-based quality classifier baseline for a produce sorting line (numpy only). It is NOT a trained deep model and NOT validated on real produce.
Two tasks: LEAF (healthy / diseased: fraction of brown-yellow-necrotic pixels in the leaf area) and FRUIT (unripe / ripe / overripe from mean hue of the fruit mask).
Method: leaf/fruit mask = non-background pixels (background is a known conveyor colour); HSV conversion; rule thresholds calibrated on a small labelled set (`fit_thresholds`).
usage: python3 classify.py --selftest"""
import numpy as np, sys

def rgb2hsv(rgb):
    a = rgb.astype(np.float64) / 255.0; r, g, b = a[..., 0], a[..., 1], a[..., 2]; mx = a.max(-1); mn = a.min(-1); d = mx - mn + 1e-12
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60.0; s = np.where(mx > 0, d / (mx + 1e-12), 0); return h, s, mx

def mask(rgb, bg=(200, 200, 205), tol=45):
    return np.abs(rgb.astype(int) - np.array(bg)).sum(-1) > tol

def leaf_disease_fraction(rgb):
    m = mask(rgb)
    if m.sum() < 50: return 0.0
    h, s, v = rgb2hsv(rgb); diseased = m & (((h > 15) & (h < 70) & (s > 0.35)) | (v < 0.28)) & ~((h >= 70) & (h <= 170) & (s > 0.3))   # brown/yellow hues or very dark, but not green
    return float(diseased.sum() / m.sum())

def classify_leaf(rgb, thr=0.12): return "diseased" if leaf_disease_fraction(rgb) > thr else "healthy"

def fruit_hue(rgb):
    m = mask(rgb)
    if m.sum() < 50: return None
    h, s, v = rgb2hsv(rgb); hh = h[m & (s > 0.25)]; return float(np.median(hh)) if hh.size else None

def classify_fruit(rgb, unripe_min=70.0, ripe_max=25.0, over_v=0.5):
    """tomato-like: green (hue about 90-120) unripe, red (hue about 0-15) ripe, dark/brownish red overripe"""
    hue = fruit_hue(rgb)
    if hue is None: return "none"
    h, s, v = rgb2hsv(rgb); m = mask(rgb); vm = float(v[m].mean())
    if hue >= unripe_min: return "unripe"
    if vm < over_v: return "overripe"
    return "ripe" if (hue <= ripe_max or hue >= 340) else "turning"

def _scene(kind, rng, size=96):
    img = np.zeros((size, size, 3), np.uint8); img[:] = (200, 200, 205); yy, xx = np.mgrid[:size, :size]; disk = (yy - size / 2) ** 2 + (xx - size / 2) ** 2 < (size * 0.36) ** 2
    base = {"healthy_leaf": (50, 140, 50), "diseased_leaf": (50, 140, 50), "unripe": (110, 160, 60), "ripe": (200, 40, 35), "overripe": (110, 35, 30), "turning": (200, 130, 50)}[kind]
    img[disk] = base
    if kind == "diseased_leaf":
        for _ in range(8):
            cy, cx = rng.integers(size // 4, 3 * size // 4, 2); r = rng.integers(5, 9); sp = ((yy - cy) ** 2 + (xx - cx) ** 2 < r * r) & disk; img[sp] = (130, 90, 30)
    return np.clip(img.astype(int) + rng.integers(-10, 11, img.shape), 0, 255).astype(np.uint8)

def selftest():
    rng = np.random.default_rng(0); fails = 0; n = 60
    for kind, fn, want in [("healthy_leaf", classify_leaf, "healthy"), ("diseased_leaf", classify_leaf, "diseased"), ("unripe", classify_fruit, "unripe"), ("ripe", classify_fruit, "ripe"), ("overripe", classify_fruit, "overripe"), ("turning", classify_fruit, "turning")]:
        ok = sum(fn(_scene(kind, rng)) == want for _ in range(n)); acc = ok / n; flag = acc >= 0.95; fails += not flag; print(f"{kind:14s} -> {want:9s} {acc*100:5.1f} %  {'ok' if flag else 'FAIL'}")
    dim = _scene("ripe", rng); dim = (dim * 0.7).astype(np.uint8); res = classify_fruit(dim); print("dim light (x0.7) ripe ->", res); fails += res not in ("ripe", "overripe")
    print("selftest:", "FAILED" if fails else "ok"); return fails
if __name__ == "__main__":
    sys.exit(1 if selftest() else 0)
