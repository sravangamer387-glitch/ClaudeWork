# Phase 6 Findings – what designing the products changed

## 1. Problems the build process caught
1. **Lamp could jump colour after a stalled main loop** (caught by a test): the old code caught up several 20 ms steps in one update (a 100 ms stall gave a 5-level jump). Fixed: at most one step per tick, then resynchronise. A test now enforces "never more than 1 level per update", also during the rainbow mode.
2. **Enclosure cut-outs missed the closed face** (caught because two STL files were tiny and the mass equalled an uncut shell). The watertight check could not see this. Fixed, and every cut now asserts that it removed material.
3. **Resume-after-sleep ambiguity** in the rhymes player (a resume after a STOP would not know the track): replaced a fragile frame-count check with an explicit `started` flag; after sleep the player restarts the track.
4. **Drawing quality:** two generated diagrams were wrong or overlapping and were redrawn by hand before being kept.

## 2. The economics are worse than Phase 2 assumed
Phase 2 used a guessed BOM x1.3. Designing the three products and costing every part gives (marketplace model, 5,000-unit tooling amortisation, all costs estimates):

| Product | Phase 2 landed guess | Designed landed | Price | Contribution | Margin |
|---|---|---|---|---|---|
| P1 Rhymes player, SD card, 100 rhymes/language | 429 | 594 | ₹999 | –₹7 | –1 % |
| **P1b Rhymes player, SPI flash, ~30 rhymes** | 429 | 518 | ₹999 | ₹75 | 9 % |
| P3 Star lamp with MP3 module + SD | 338 | 592 | ₹799 | –₹153 | –23 % |
| P3b Star lamp, OTP voice chip, 3 lullabies | 338 | 464 | ₹799 | –₹16 | –2 % |
| P4 Cricket game | 286 | 340 | ₹699 | ₹44 | 7 % |

Price needed for ≥ 20 % marketplace contribution: P1b about ₹1,360, P4 about ₹830, P3b about ₹1,240, P1 (SD) about ₹1,520.

**Why:** (a) a microSD card and MP3 module cost more than the chip alone; (b) injection tooling spread over 5,000 units adds ₹50–80 per unit; (c) the rhymes player's three parts weigh about 150 g of ABS (≈ ₹30 of resin, mass computed from the CAD); (d) packaging and assembly were too low in the guess.

**Volume helps:** at 20,000 units (tooling amortised over 4x as many) margins improve by about 6–12 points: P1b 15 %, P4 15 %, P3b 8 %.

## 3. Consequences for the plan
1. The Phase 3 launch gate (≥ 25 % contribution) is **not met by any of the three at the Phase 5 prices**. Do not start tooling yet.
2. **Reprice or redesign before launch:**
   - Rhymes player: use the **flash-based (P1b) design**, price ₹1,299–1,399, sell regional language editions with ~30 curated rhymes; or keep SD for a premium ₹1,499+ version with 100+ items.
   - Cricket game: price ₹799–899 (still cheap for the segment); keep the 2-part enclosure.
   - Star lamp: this category is price-competitive; only proceed with the OTP-voice design at ₹1,199+ or at 20,000+ units. It should drop below the cricket game and rhymes player in Wave 1 priority.
3. **Validate cheaper electronics first**: get real quotes for MP3 module vs bare chip, flash vs SD, and 3 quotes for the enclosure; cost can fall 10–20 % with volume commitments.
4. **De-risk before tooling:** build 3D-printed prototypes (STL files provided) and 10–20 hand-assembled units on a development PCB; run play tests; only then order moulds.
5. **Ranking caveat:** Phase 2 scores used optimistic margins for these items. Rhymes player and cricket game still lead on demand and India fit; the star lamp's rank is probably too high.
6. **Cost model transparency:** `hardware/bom.csv` and `hardware/design_to_cost.md` contain every line; change one number and rerun `gen_hardware.py`.

## 4. Next engineering steps
1. Choose the real MCU and write the HAL port (timers, GPIO, UART, ADC, watchdog); add battery-low behaviour.
2. KiCad schematic from the pin map; PCB layout (2-layer, 90 x 60 mm); EMS quote.
3. Bench: current draw per mode, SPL at 25 cm for volume cap, battery life, button feel.
4. Print enclosures (STL) and fit-check; then tool-maker review.
5. Record content (Hindi, Telugu first) and build the card/flash image pipeline.
6. Pre-compliance test at a lab.
