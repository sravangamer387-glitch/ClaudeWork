# Prototype packs (10 prototypes under Rs 3,000): build manual

> **These are bench prototypes, not products.** Every prototype was costed to stay under Rs 3,000 (cheapest Rs 690, dearest Rs 2,120; all ten Rs 14,940 plus Rs 1,500 for tools if you own none). The build recipes, wiring tables, SD layout, flashing and acceptance tests are already written; use them in this order.

## 1. Where the instructions are
| Prototype | Instructions | Files |
|---|---|---|
| G1-G5 gravity toys (tower Rs 1,000, Drop Quest v0 Rs 690, Galton Rs 1,430, Santulan Rs 1,280, Ramp Racers Rs 1,570) | `prototypes/guides/gravity-prototypes.md` (cut lists, MDF groove trick, tests) | `gravity-toys/cad/out/*.svg`; budget `prototypes/budget/prototype_budgets.md` |
| E1 rhymes player, E2 star lamp, E3 cricket game (Nano + modules) | `prototypes/guides/electronics-prototypes.md` | hex files in `prototypes/firmware/release/` (`rhymes.hex`, `lamp.hex`, `cricket.hex`), source in `prototypes/firmware/` |
| D1 beat-synced light controller, D2 DJ MIDI controller | same guide; Mixxx map `prototypes/mixxx/PartyPod-Proto.midi.xml` (untested in Mixxx) | `beatlight.hex`, `midi.hex` |

## 2. Common procedure
1. Buy parts from `prototypes/budget/prototype_budgets.csv` (prices are estimates; the budget script fails if a prototype goes over Rs 3,000).
2. Build per the guide; for Nano-based prototypes flash with `avrdude -p m328p -c arduino -P <port> -b 57600 -U flash:w:<file>.hex:i` (use `-b 115200` for new-bootloader clones).
3. Run the acceptance test listed in the guide and record it on `manuals/templates/eol_test_sheet.md`.
4. Safety: low voltage only (USB power bank or batteries); never connect mains; keep the lamp's colour changes gentle (tested rule: at most 1 level per 20 ms).

## 3. Known limits
Drop Quest v0 has no solver yet; Mixxx map untested; MP3-module command codes unverified; all figures are estimates or simulations. Real manufacturing manuals for the products these prototypes lead to: see each product's `MANUFACTURING_MANUAL.md`.
