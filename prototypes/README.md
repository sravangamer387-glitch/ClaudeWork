# Prototypes under Rs 1k / 2k / 3k – build packs for all ten

Prepared 2026-10-31. **Every prototype below costs at most Rs 3,000** (cheapest Rs 690, dearest Rs 2,120; all ten together Rs 14,940, plus Rs 1,500 one-time tools if you own none). Prices are my estimates from typical Indian online/hobby stores – check current listings before ordering. **None of these has been physically built by me**; I produced everything needed to build them and verified what a computer can verify.

| Code | Prototype | Cost Rs | Verified here |
|---|---|---|---|
| G1 | Timber Tower Marble Run (MDF) | 1,000 | physics: run time, groove clearance, slopes |
| G2 | Drop Quest v0 | 690 | – (solver not written yet) |
| G3 | Galton Board | 1,430 | simulation matches the bell curve; jam guard |
| G4 | Santulan balance set | 1,280 | centre-of-gravity model |
| G5 | Ramp Racers | 1,570 | run times per wheel type and angle |
| E1 | Rhymes player (Nano + MP3 module) | 1,910 | firmware: 76 host tests + compiled for ATmega328P |
| E2 | Star projector lamp | 2,120 | same; no-flash rule enforced by tests |
| E3 | Cricket game | 1,370 | same |
| D1 | Beat-synced light controller | 1,700 | beat/BPM detector tested on synthetic music; compiled |
| D2 | DJ MIDI controller | 1,870 | filters/encoder tested; compiled; Mixxx map written (untested) |

## Where things are
| Path | What |
|---|---|
| `budget/` | `prototype_budget.py`, `prototype_budgets.md/.csv` – every line item; the script **fails if any prototype exceeds Rs 3,000** |
| `firmware/` | Five Arduino-Nano firmwares + DJ core library + host tests. `make` builds all five (**compiles clean for the ATmega328P: 3.7–6.1 KB flash, up to 855 B of 2,048 B RAM**); `make test` runs 26 DJ-core tests (the shared toy core has 76 more in `electronics-toys/wave1/firmware`) |
| `guides/` | Wiring tables, SD-card layout, flashing, per-prototype acceptance tests (electronics and gravity toys) |
| `mixxx/` | Mapping file for the DJ controller prototype (untested in Mixxx) |
| `../gravity-toys/sim/` | Physics verification of the five gravity toys |

## Results worth knowing
- **Beat detector:** on synthetic music at 90–150 BPM it reports BPM within ±1 and flags 24 of 24 kick beats within ±60 ms; it ignores soft hi-hats, silence, and steady noise. Real music is messier: expect tuning.
- **Light safety:** even if the detector misfires on every frame, the lights pulse at most 3 times per second and never go dark while music plays.
- **Three design corrections found by simulation** (applied to the toy docs): marble-run ramps 6–8° not 8–12°; the balancing bird's weights must sit about 95 mm in front of the beak; felt wheels need ≥ 10° ramps.
- **Bugs caught by testing:** lamp could jump colour after a stalled loop; beat detector reported a tempo after silence; encoder test sequence wrong; all fixed.

## Prototype cost is not unit profit (important)
A Rs 1–3k prototype is easy; **profit comes from the cost of each unit at volume and the fixed launch costs**, and those are very different numbers (contribution per unit from the earlier models; fixed launch costs are my assumptions):

| Product | Prototype Rs | Contribution per unit Rs | Units to repay the prototype | Fixed launch cost (assumption) | Units to repay that |
|---|---|---|---|---|---|
| Timber Tower | 1,000 | 513 | 2 | Rs 3 lakh | 585 |
| Ramp Racers | 1,570 | 354 | 5 | Rs 3 lakh | 848 |
| Galton Board | 1,430 | 156 | 10 | Rs 3 lakh | 1,924 |
| Santulan set | 1,280 | 127 | 11 | Rs 3 lakh | 2,363 |
| Rhymes player (flash design) | 1,910 | 75 | 26 | Rs 6 lakh | 8,000 |
| Cricket game | 1,370 | 44 | 32 | Rs 6 lakh | 13,637 |
| Star lamp (low-cost design) | 2,120 | –16 | never | Rs 6 lakh | never |
| DJ controller (top-down guess) | 1,870 | 3,407 | 1 | Rs 25 lakh | 734 |
| Light kit (top-down guess) | 1,700 | 2,442 | 1 | Rs 25 lakh | 1,024 |

**Reading it plainly:** the wooden/lab toys (Tower, Racers) and the DJ products are where the per-unit money is; the cheap electronic toys earn tens of rupees per unit and need thousands of sales to pay back testing and tooling; the star lamp loses money as designed. DJ figures are top-down guesses and the toy work showed such guesses run 20–50 % optimistic.

## Not done (needs hardware, people or decisions)
1. Physical assembly and bench testing of all ten prototypes.
2. Drop Quest puzzle solver and 60 levels (rules need a decision after kid play-tests).
3. Production PCB layout, EMC/safety/BIS/WPC testing, tooling.
4. Verifying MP3-module command codes, Mixxx mapping and every price on the real parts.
5. Music/rhyme content recording and licences.
