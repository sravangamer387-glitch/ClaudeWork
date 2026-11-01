# Gesture recognition on synthetic traces

Synthetic only: minimum-jerk strokes, 15-40 deg size, 0.7-1.7 s, tilt of drawing +-20 deg, wand roll +-35 deg, gyro bias +-1.5 deg/s, 0.15 deg/s noise, 5-9 Hz tremor. Real hands will do worse until tuned on recorded data.

### Noise/variation level x1.0  (300 casts per spell)

accuracy 100.0 %, fizzled (rejected) 0.0 %, wrong spell 0.0 %

| true \ result | agni | vajra | jala | raksha | prakash | vayu | fizzle |
|---|---|---|---|---|---|---|---|
| agni | 300 | 0 | 0 | 0 | 0 | 0 | 0 |
| vajra | 0 | 300 | 0 | 0 | 0 | 0 | 0 |
| jala | 0 | 0 | 300 | 0 | 0 | 0 | 0 |
| raksha | 0 | 0 | 0 | 300 | 0 | 0 | 0 |
| prakash | 0 | 0 | 0 | 0 | 300 | 0 | 0 |
| vayu | 0 | 0 | 0 | 0 | 0 | 300 | 0 |

False casts from non-spells (300 each): random scribble 24 (8.0 %), tiny shake (<5 deg) 1 (0.3 %), horizontal sweep (60 deg) 0 (0.0 %)

### Noise/variation level x1.6  (300 casts per spell)

accuracy 98.3 %, fizzled (rejected) 1.7 %, wrong spell 0.0 %

| true \ result | agni | vajra | jala | raksha | prakash | vayu | fizzle |
|---|---|---|---|---|---|---|---|
| agni | 292 | 0 | 0 | 0 | 0 | 0 | 8 |
| vajra | 0 | 298 | 0 | 0 | 0 | 0 | 2 |
| jala | 0 | 0 | 299 | 0 | 0 | 0 | 1 |
| raksha | 0 | 0 | 0 | 286 | 0 | 0 | 14 |
| prakash | 0 | 0 | 0 | 0 | 296 | 0 | 4 |
| vayu | 0 | 0 | 0 | 0 | 0 | 298 | 2 |

False casts from non-spells (300 each): random scribble 25 (8.3 %), tiny shake (<5 deg) 11 (3.7 %), horizontal sweep (60 deg) 0 (0.0 %)
