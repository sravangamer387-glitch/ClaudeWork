"""Edge camera analytics for the MITTI-NETRA companion (Raspberry Pi / Banana Pi): canopy cover and greenness from a field photo.
Pure numpy (+ Pillow to read files). Method: Excess Green index ExG = 2g - r - b on chromatic coordinates, threshold by Otsu, canopy cover = fraction of pixels above it.
This is a classical vision baseline; it is NOT a trained crop-disease model. A TFLite/ONNX classifier can be added behind the same `analyse()` interface.
usage: python3 crop_index.py photo.jpg     |     python3 crop_index.py --selftest"""
import sys, json
import numpy as np

def exg(rgb):
    """rgb: HxWx3 uint8 -> ExG per pixel (float, about -1..2), using chromatic coordinates r,g,b = R/(R+G+B)..."""
    a = rgb.astype(np.float64); s = a.sum(axis=2) + 1e-9
    r, g, b = a[..., 0] / s, a[..., 1] / s, a[..., 2] / s
    return 2 * g - r - b

def otsu(x, bins=256):
    h, edges = np.histogram(x, bins=bins); p = h / h.sum(); w = np.cumsum(p); mu = np.cumsum(p * (edges[:-1] + edges[1:]) / 2); mt = mu[-1]
    sb = (mt * w - mu) ** 2 / (w * (1 - w) + 1e-12); return float(edges[int(np.argmax(sb)) + 1])

def analyse(rgb):
    e = exg(rgb); t = otsu(e); mask = e > t
    # reject an Otsu split of an image with almost no variation (bare soil or all canopy): require a minimum contrast between the two classes
    if mask.any() and (~mask).any() and (e[mask].mean() - e[~mask].mean()) < 0.15:
        mask = np.zeros_like(mask) if e.mean() < 0.1 else np.ones_like(mask)
    cover = float(mask.mean()); green = float(e[mask].mean()) if mask.any() else 0.0
    return {"canopy_cover": round(cover, 4), "mean_exg_canopy": round(green, 4), "threshold": round(t, 4)}

def selftest():
    rng = np.random.default_rng(1); fails = 0
    def scene(frac, h=120, w=160):
        img = np.zeros((h, w, 3), np.uint8); img[:] = (120, 95, 70)                                   # brown soil
        n = int(frac * w); img[:, :n] = (50, 140, 45)                                                 # green plants
        return np.clip(img.astype(int) + rng.integers(-12, 13, img.shape), 0, 255).astype(np.uint8)
    for f in (0.0, 0.25, 0.5, 0.8, 1.0):
        r = analyse(scene(f)); ok = abs(r["canopy_cover"] - f) < 0.03
        print(f"true cover {f:.2f} -> {r['canopy_cover']:.3f} {'ok' if ok else 'FAIL'}"); fails += not ok
    dark = (scene(0.5) * 0.4).astype(np.uint8); r = analyse(dark); ok = abs(r["canopy_cover"] - 0.5) < 0.05; print(f"dim light (x0.4) -> {r['canopy_cover']:.3f} {'ok' if ok else 'FAIL'}"); fails += not ok
    print("selftest:", "FAILED" if fails else "ok"); return fails

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest": sys.exit(1 if selftest() else 0)
    from PIL import Image
    print(json.dumps(analyse(np.asarray(Image.open(sys.argv[1]).convert("RGB")))))
