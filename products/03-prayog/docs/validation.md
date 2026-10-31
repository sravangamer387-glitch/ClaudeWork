# Validation of the Prayog analysis tools (simulated experiments with noise)

| Analysis | True value | Recovered | Tolerance | Result |
|---|---|---|---|---|
| Newton cooling constant k (1/s) | 0.0021 | 0.00209 | ±0.000105 | PASS |
| Light intensity exponent (inverse square: -2) | -2 | -2.003 | ±0.08 | PASS |
| Speed of sound from echoes (m/s) | 343.4 | 344.1 | ±6.87 | PASS |
| g from pendulum (m/s2) | 9.78 | 9.818 | ±0.2 | PASS |
| g from free fall (m/s2) | 9.78 | 9.786 | ±0.35 | PASS |
| Photogate event stream -> pendulum period (s) | 2.006 | 2.006 | ±0.001 | PASS |
| Resistance from V-I slope (ohm) | 47 | 47 | ±1.5 | PASS |
| RC time constant (s) | 4.7 | 4.719 | ±0.2 | PASS |
| Magnet field exponent on axis (dipole: -3) | -3 | -2.968 | ±0.2 | PASS |
| Conductivity vs concentration slope | 85 | 84.91 | ±6 | PASS |
| Human reaction time (s) | 0.21 | 0.2063 | ±0.02 | PASS |
| Sanity: linear data does not look like inverse square | exponent ≠ -2 | 1.00 | – | PASS |

Simulated data use the stated true constants plus sensor-like noise; they validate the *method*, not the hardware.
