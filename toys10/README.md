# Ten new toys (2026-10-31)

All ten are designed with the same discipline as the six products: engines and simulations verified on this machine, **prototype ≤ Rs 3,000 each**, designed production BOM, economics with +30 % BOM sensitivity, manufacturing and compliance notes. **Nothing is built or child-tested.**

| # | Toy | Ages | Type | Prototype Rs | BOM Rs | Price Rs | Contribution Rs | If BOM +30 % |
|---|---|---|---|---|---|---|---|---|
| 01 | [Reflex Raja](01-reflex-raja/README.md) | 6+ | electronic | 1090 | 310 | 999 | 263 (31%) | 155 (18%) |
| 02 | [Taal Memory](02-taal-memory/README.md) | 5+ | electronic | 1070 | 310 | 899 | 189 (25%) | 80 (11%) |
| 03 | [Aloo Bomb](03-aloo-bomb/README.md) | 6+ | electronic | 940 | 227 | 699 | 137 (23%) | 57 (10%) |
| 04 | [Beat Runner](04-beat-runner/README.md) | 7+ | electronic | 1140 | 326 | 1299 | 365 (33%) | 251 (23%) |
| 05 | [Rangoli Spiro Gears](05-rangoli-spiro/README.md) | 6+ | laser | 700 | 193 | 649 | 199 (32%) | 131 (21%) |
| 06 | [Paper Rocket Air Launcher](06-paper-rocket/README.md) | 8+ | physics | 1100 | 310 | 799 | 188 (25%) | 80 (10%) |
| 07 | [Tilt Maze Labyrinth](07-tilt-maze/README.md) | 7+ | laser | 950 | 260 | 799 | 246 (32%) | 155 (20%) |
| 08 | [Rubber-band Racer](08-band-racer/README.md) | 6+ | laser | 600 | 119 | 449 | 118 (27%) | 76 (18%) |
| 09 | [Marble Cricket](09-marble-cricket/README.md) | 6+ | laser | 1110 | 262 | 999 | 412 (43%) | 320 (34%) |
| 10 | [Katha Cubes](10-katha-cubes/README.md) | 5+ | print | 400 | 109 | 399 | 87 (23%) | 49 (13%) |

## What the numbers say
- **Best margins:** Marble Cricket (43 %), Tilt Maze, Rangoli Spiro Gears and Rubber-band Racer (all 27–32 %); these are laser-cut and share the laser shops used by the earlier gravity and automata toys.
- **Electronic toys:** the first-draft prices (Rs 499–799) lost money at the designed BOM; they are priced at Rs 699–1,299 above. Taal Memory and Aloo Bomb are still thin at +30 % BOM. **Recommendation (decision): sell the three party games (Reflex Raja, Taal Memory, Aloo Bomb) as one "Desi Arcade" box with one board and a game-select switch at Rs 1,499** (BOM about Rs 345 → contribution Rs 476 (37%), Rs 355 (28%) if BOM +30 %). The merged firmware is built: `electronic/release/desi_arcade.hex` (hold button 1/2/3 while switching on to pick Reflex Raja / Taal Memory / Aloo Bomb; 5.5 KB).
- **Paper Rocket Air Launcher is the risky one:** a projectile toy. Do not sell it without a standards review; the design already forces a low-pressure relief valve (a first draft was 5× over my placeholder energy limit).
- **Launch order I recommend:** Marble Cricket, Tilt Maze, Rangoli Spiro Gears (one laser-shop trip), then Katha Cubes (needs an illustrator and proofreading), then the Desi Arcade box.

## Layout
`electronic/` C engines + tests + Nano demo hex for toys 01–04 (`make test`, `make hex`) · `sims/` simulations and generators · `out/` SVG cut files, previews, CSV · `docs/` results, economics.csv, `toys.py` (data), `build_docs.py` (regenerates every README) · one folder per toy with its README.

## Verification summary
Electronic engines: 80,045 host checks, sanitizers on. Spiro Gears: 8 gear pairs verified to close with the predicted petal count (my first counting method was wrong and was replaced). Rocket: relief pressure derived from an energy limit. Maze: three BFS-verified mazes with trap holes on dead ends only. Racer: model constant corrected by 6×. Marble Cricket: pockets chosen by search, Monte Carlo of 100,000 overs. Katha Cubes: 36 distinct words, 46,656 stories.
