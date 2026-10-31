"""Jal-Netra digital twin of the measurement chain: transducer burst -> water path -> LNA noise -> 12-bit ADC at 4 MS/s -> I/Q phase estimator.
Monte Carlo of the transit-time difference estimate versus signal-to-noise ratio and averaging; results go to ../docs/twin_results.md and ../out/*.png."""
import numpy as np, math, os, sys
sys.path.insert(0, os.path.dirname(__file__)); from physics import *
F0, FS, NCYC = 1.0e6, 4.0e6, 6                          # carrier, ADC rate, burst cycles
TAU_R = 4 / (math.pi * F0)                               # transducer (Q=4) rise/fall time constant
WIN_US, T_START_US = 16.0, None                          # capture window; start chosen 4 us before the expected arrival
def pulse(t, tau, amp):
    """received waveform: burst of NCYC cycles shaped by the transducer pair response (rise/fall exponential), arriving at tau"""
    x = t - tau; burst = NCYC / F0; env = np.zeros_like(x)
    r = (x > 0) & (x <= burst); env[r] = 1 - np.exp(-x[r] / TAU_R)
    peak = 1 - math.exp(-burst / TAU_R); f = x > burst; env[f] = peak * np.exp(-(x[f] - burst) / TAU_R)
    return amp * env * np.sin(2 * np.pi * F0 * x)
def capture(tau, amp, sigma, rng, adc_bits=12, vref=3.3, shots=1):
    """returns array (shots, nsamp) of ADC codes around mid-scale; tau in seconds from the start of the window"""
    n = int(WIN_US * 1e-6 * FS); t = np.arange(n) / FS
    clean = pulse(t, tau, amp)[None, :] + rng.normal(0, sigma, (shots, n))
    lsb = vref / 2 ** adc_bits; return np.round(clean / lsb) * lsb
def iq_phase(x, f0=F0, fs=FS):
    """complex demodulation over the whole window with a Hann taper; returns phase (rad) and amplitude"""
    n = x.shape[-1]; k = np.arange(n); w = np.hanning(n); ref = np.exp(-2j * np.pi * f0 * k / fs)
    z = (x * (w * ref)).sum(-1); return np.angle(z), np.abs(z)
def estimate_dt(up, down, f0=F0):
    """phase difference -> time difference (positive when the upstream path is slower); valid for |dt| < 1/(2 f0)"""
    pu, au = iq_phase(up); pd, ad = iq_phase(down); dphi = np.angle(np.exp(1j * (pu - pd)))        # wrap to (-pi, pi]
    return dphi / (2 * np.pi * f0) * -1.0                                                             # later arrival = more negative phase
def monte_carlo(dt_true, snr_db, nshots, trials=300, seed=1, amp=0.25):
    rng = np.random.default_rng(seed); sigma = amp / 10 ** (snr_db / 20)
    tof = 40.48e-6; t0 = tof - 4e-6; res = []
    for _ in range(trials):
        up = capture(tof - t0 + dt_true / 2, amp, sigma, rng, shots=nshots); down = capture(tof - t0 - dt_true / 2, amp, sigma, rng, shots=nshots)
        res.append(estimate_dt(up, down).mean())
    res = np.array(res); return res.mean() - dt_true, res.std()
if __name__ == "__main__":
    out = []; rows = ["| true dt (ns) | SNR per shot (dB) | shots averaged | bias (ps) | std dev (ps) | equivalent flow resolution (L/h, 12 mm bore) |", "|---|---|---|---|---|---|"]
    s = Spool(); lph_per_ns = None
    for dt_ns in (0.5, 5.0):
        for snr in (20, 30, 40):
            for n in (1, 100, 1000):
                b, sd = monte_carlo(dt_ns * 1e-9, snr, n, trials=150 if n >= 1000 else 300)
                # flow resolution: dQ/ddt at this operating point
                v1 = s.v_from_dt(sd, 20); q = 60000 * s.A * v1 * 60 * 0.75 / 60 * 60 / 60                       # L/h = v[m/s] * A[m2] * 3.6e6 * k
                q = v1 * s.A * 3.6e6 * 0.75
                rows.append(f"| {dt_ns} | {snr} | {n} | {b*1e12:+.0f} | {sd*1e12:.0f} | {q:.2f} |"); print(rows[-1], flush=True)
    open(os.path.join(os.path.dirname(__file__), "..", "docs", "twin_results.md"), "w").write("\n".join(rows) + "\n")
