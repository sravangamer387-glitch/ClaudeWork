# KINETIC vibration model results (SYNTHETIC data only)

Model: 10 order-tracked features -> MLP 10-16-8-4, int8 weights (320 bytes), float requantisation. Window 1024 samples at 3200 Hz (0.32 s). Shaft-speed window 480-1500 rpm.

Held-out synthetic test set (3000 windows, different seed): **float 94.6 %, int8 94.5 %**. Healthy windows flagged as faulty: **6.8 %**.


Confusion matrix (rows true, columns predicted, int8):

| true \ pred | healthy | outer-race | inner-race | unbalance |
|---|---|---|---|---|
| healthy | 656 | 27 | 21 | 0 |
| outer-race | 72 | 677 | 9 | 0 |
| inner-race | 33 | 3 | 745 | 0 |
| unbalance | 0 | 0 | 0 | 757 |

Race-fault recall by impulse amplitude (synthetic, g at the resonance; 300 windows each):

| impulse amplitude | recall |
|---|---|
| 0.04 g | 38 % |
| 0.08 g | 93 % |
| 0.15 g | 100 % |
| 0.30 g | 100 % |
| 0.50 g | 100 % |

**What this does and does not show.** The pipeline is internally consistent and the C implementation reproduces the Python features and classes (see test). The accuracy is for *this simulator*, whose faults are cleaner than real ones: real rigs add looseness, gear mesh, resonance shifts, load-dependent amplitudes and sensor-mounting effects. Expect a real-data accuracy well below these numbers until the model is retrained on recordings from the real machine. No claim of field performance is made.
