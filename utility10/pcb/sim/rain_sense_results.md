| plate resistance | V(SENSE) at 2 ms | at 5 ms (final) | ADC counts at 4.5 V ref | reads as |
|---|---|---|---|---|
| 1 kΩ (heavy rain, shorted) | 4.369 V | 4.369 V | 994 | WET (>=400) |
| 10 kΩ (wet) | 4.018 V | 4.018 V | 914 | WET (>=400) |
| 50 kΩ (wet) | 2.961 V | 2.961 V | 674 | WET (>=400) |
| 150 kΩ (damp) | 1.786 V | 1.786 V | 406 | WET (>=400) |
| 500 kΩ (dew/humid) | 0.747 V | 0.748 V | 170 | dry (<250) |
| 2 MΩ (dry-ish) | 0.214 V | 0.214 V | 49 | dry (<250) |
| open (dry) | 0.000 V | 0.000 V | 0 | dry (<250) |

Pulse 4.5 V for 5 ms through 1 kΩ; time constant (plate+2k)||100k x 2.2 nF is at most 0.22 ms, so the reading has settled long before 2 ms. Firmware must wait >= 2 ms (demo waits 2 ms).
