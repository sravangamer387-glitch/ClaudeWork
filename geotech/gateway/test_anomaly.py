import numpy as np, sys
import anomaly as A
fails = 0
def check(c, msg):
    global fails
    print(("ok   " if c else "FAIL ") + msg); fails += not c
det, conf = A.evaluate(seed=3, n=300)
rec = lambda k, lab: conf[k].get(lab, 0) / sum(conf[k].values())
check(rec("ambient", "ambient") > 0.97, f"ambient recall {rec('ambient','ambient'):.3f}")
check(rec("ambient_gust", "ambient") > 0.9, f"gusty ambient not flagged {rec('ambient_gust','ambient'):.3f}")
check(rec("vehicle", "vehicle") > 0.9, f"vehicle recall {rec('vehicle','vehicle'):.3f}")
check(rec("vehicle", "crack") < 0.02, f"vehicle never called crack ({rec('vehicle','crack'):.3f})")
check(rec("crack", "crack") > 0.85, f"crack recall {rec('crack','crack'):.3f}")
check(rec("crack", "vehicle") < 0.02, f"crack not called vehicle ({rec('crack','vehicle'):.3f})")
# robustness: different seed, thresholds from a fresh baseline
d2, c2 = A.evaluate(seed=11, n=200); r2 = lambda k, l: c2[k].get(l, 0) / sum(c2[k].values())
check(r2("crack", "crack") > 0.8 and r2("vehicle", "vehicle") > 0.85 and r2("ambient", "ambient") > 0.95, "held-out seed holds")
# tracker: isolated crack window does not alarm, repeated ones do
t = A.CrackTracker(3, 30); out = [t.update(l) for l in ["crack"] + ["ambient"] * 10 + ["crack", "crack", "crack"]]
check(not any(out[:12]) and out[-1], "tracker needs repeated cracks")
# a vehicle train (many vehicle windows) never raises the structural alarm
t = A.CrackTracker(3, 30); rng = np.random.default_rng(5); al = False
for _ in range(100): al |= t.update(det.classify(A.synth("vehicle", rng))[0])
check(not al, "vehicle traffic alone never alarms")
print("FAILED" if fails else "geotech anomaly: OK"); sys.exit(1 if fails else 0)
