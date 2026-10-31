import numpy as np, os, re, sys, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__)); import twin
from physics import *
OUT = os.path.join(os.path.dirname(__file__), "..", "out")
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
rng = np.random.default_rng(3); tof = 40.48e-6; t0 = tof - 4e-6; amp = 0.25
x = twin.capture(tof - t0, amp, amp / 10 ** (30 / 20), rng)[0]; t = np.arange(len(x)) / twin.FS * 1e6
ax[0].plot(t, x * 1000, ".-", lw=0.8); ax[0].set_title("one received shot at the ADC (30 dB SNR, 4 MS/s, 12 bit)"); ax[0].set_xlabel("time in capture window (us)"); ax[0].set_ylabel("mV")
rows = [l.split("|")[1:7] for l in open(os.path.join(OUT, "..", "docs", "twin_results.md")) if re.match(r"\| [0-9]", l)]
for snr, st in ((20, "o-"), (30, "s-"), (40, "^-")):
    ns = [int(r[2]) for r in rows if float(r[0]) == 5.0 and int(r[1]) == snr]; sd = [float(r[4]) for r in rows if float(r[0]) == 5.0 and int(r[1]) == snr]
    ax[1].loglog(ns, sd, st, label=f"SNR {snr} dB")
ax[1].set_xlabel("shot pairs averaged"); ax[1].set_ylabel("std of dt estimate (ps)"); ax[1].legend(); ax[1].grid(True, which="both", alpha=0.3); ax[1].set_title("transit-time difference resolution (Monte Carlo)")
s = Spool(); q = np.logspace(-2, 1.6, 60); T = 20; v = q / 60000 / s.A; dt = [s.dt(vi / kprofile(max(vi * s.d / nu_water(T), 1)), T) * 1e9 for vi in v]
ax[2].loglog(q * 60, dt); ax[2].axhline(0.075, color="r", ls="--", label="75 ps (30 dB, 1000 pairs)"); ax[2].set_xlabel("flow (L/h)"); ax[2].set_ylabel("dt (ns)"); ax[2].set_title("transit-time difference vs flow, 12 mm bore, 60 mm path"); ax[2].legend(); ax[2].grid(True, which="both", alpha=0.3)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "twin_overview.png"), dpi=110); print("ok")
