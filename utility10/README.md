# Ten utility tools (2026-10-31)

Smart, simple tools for Indian homes. Eight are low-voltage electronics (one C library of tested engines, `firmware/`), two are laser-cut (`sims/`, `out/`). Prototype ≤ Rs 3,000 each. **Nothing is built or field-tested.** Engineering-release PCBs (rev B: KiCad schematic and layout, Gerbers, JLCPCB BOM/CPL, 3D STEP, fab notes, enclosure shell, SPICE results) exist for the three electronic Tier A tools in `pcb/` — software-verified (0 DRC errors), engineer sign-off still required (`pcb/REVIEW_CHECKLIST.md`).

| # | Tool | Tier | Prototype Rs | BOM Rs | Price Rs | Contribution Rs | If BOM +30 % |
|---|---|---|---|---|---|---|---|
| 01 | [Seeti Counter](01-seeti-counter/README.md) | A | 1080 | 305 | 999 | 269 (32%) | 163 (19%) |
| 02 | [Gas Taraju (LPG cylinder scale)](02-gas-taraju/README.md) | B | 1730 | 757 | 2499 | 661 (31%) | 396 (19%) |
| 03 | [Fridge Door Guard](03-fridge-door-guard/README.md) | B | 610 | 162 | 599 | 138 (27%) | 81 (16%) |
| 04 | [Bijli Meter Reader](04-bijli-meter-reader/README.md) | A | 900 | 325 | 1299 | 366 (33%) | 252 (23%) |
| 05 | [Bijli Log (power-cut logger)](05-bijli-log/README.md) | B | 1220 | 475 | 1499 | 324 (26%) | 158 (12%) |
| 06 | [Chulha Timers (4 kitchen timers)](06-chulha-timers/README.md) | B | 970 | 362 | 1199 | 256 (25%) | 129 (13%) |
| 07 | [Rain Alert Bell (terrace/clothesline)](07-rain-alert/README.md) | A | 780 | 240 | 899 | 271 (36%) | 187 (24%) |
| 08 | [Tap Litre Meter](08-tap-litre-meter/README.md) | B | 1200 | 380 | 1199 | 235 (23%) | 102 (10%) |
| 09 | [Masala Rack (3-step spice rack)](09-masala-rack/README.md) | A | 850 | 380 | 1299 | 422 (34%) | 289 (23%) |
| 10 | [Fold-flat Laptop Stand](10-laptop-stand/README.md) | A | 700 | 270 | 799 | 235 (31%) | 140 (18%) |

**Tier A = launch first** (margin holds at +30 % BOM): Masala Rack, Laptop Stand, Seeti Counter, Bijli Meter Reader, Rain Alert Bell. **Tier B = conditional** (thin margin or price risk against cheap rivals): Tap Litre Meter, Bijli Log, Chulha Timers, Gas Taraju, Fridge Door Guard — build only after Tier A sells, or redesign to cost.

## Research notes (web search, 2026-10-31; sources are blogs/listings, treat as directional)
- Induction cooktops with automatic whistle counters exist (Prestige PIC series) — the retrofit gap for ordinary cookers is open; I found no standalone counter listed.
- LPG: magnetic strip level gauges are the cheap option and approximate; dealer weighing scales are about Rs 1,300 (IndiaMART) and B2B.
- Inverters from V-Guard/Luminous already include battery top-up reminders, so I dropped an inverter-battery monitor from the list.
- Meter pulse LEDs: constants vary by meter (1000/1600/3200 imp/kWh seen); BSES spec leaves the constant to the maker — the product asks the user to enter it from the label.
- Electricity tariffs rising and "home upgrade" demand growth reported for the 2026 festival season; no reliable category sales data was available for utility gadgets, so demand is unproven.

## Verification
110 automated checks across the eight engines with sanitizers on (`make test` in `firmware/`), eight Nano builds (`make hex`, 3–7 kB each). Real bugs found: the gas scale's sample history froze after 255 samples (fixed); the first test harness detected a tone at the generated frequency instead of the whistle frequency (test bug, fixed); first prices of five tools lost money or were thin, and were raised. Honest limits are in each README: whistle detection fails when the mic is far from the whistle, the stand slides under a hard 15 N shove, bill slab rates are placeholders.
