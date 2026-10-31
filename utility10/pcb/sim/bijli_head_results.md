| condition (phototransistor collector current) | SIG voltage | ADC counts (5 V ref) | note |
|---|---|---|---|
| dark / meter LED off, dim room (1 uA) | 4.99 V | 1021 |  |
| indoor ambient light on the head (20 uA) | 4.80 V | 982 |  |
| bright window light (150 uA) | 3.49 V | 713 |  |
| meter LED lit, weak coupling (200 uA) | 2.98 V | 610 |  |
| meter LED lit, typical close clip (1 mA) | 0.20 V | 41 | saturated (collector near 0.2 V) |
| meter LED lit, strong (3 mA) | 0.20 V | 41 | saturated (collector near 0.2 V) |

SIG = 5 V - Ic x (10 k pull-up + 100 ohm), clamped at 0.2 V (saturation). The firmware looks for a swing of more than 40 counts (0.2 V) between its running minimum and maximum, so a lit LED (>= 0.2 mA) against indoor ambient (<= 20 uA) gives a swing of more than 1.5 V. Direct sunlight on the head (> 1 mA) would hide the pulses: use the black clip. Edge speed: 10 k x 100 nF = 1 ms time constant, meter LED pulses are tens of ms.
These phototransistor currents are typical-datasheet assumptions, not measurements of a real meter.
