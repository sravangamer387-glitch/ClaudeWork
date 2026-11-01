# ASTRADAND: a gesture-casting fantasy / sci-fi wand

*Hold the trigger, draw a rune in the air, release: the crystal answers.* A 232 mm hilt with a 6-axis motion sensor, a light-bar crystal, piezo and haptics. Six spells (Agni fire, Vajra lightning, Jala water, Raksha shield, Prakash light, Vayu wind), mana, cooldowns and the Agni+Vajra combo Mahastra.

**Status: designed, simulated, unit-tested in software; the board and shell are generated and checked by software; nothing has been built or tested on hardware or with human hands.** Read `docs/CONCEPT.md` section 7 for the full list of what is unproven.

| What | Where | Result |
|---|---|---|
| Ideation (3 candidates scored), lore, spells, market, risks | `docs/CONCEPT.md` | selected over a dragon-egg hatchery and an NFC rune oracle |
| Gesture recogniser (reference, synthetic traces) | `sim/gesture_sim.py`, `docs/gesture_results.md` | 100 % at nominal noise, 98.3 % at 1.6x; scribbles cast a spell 8 % of the time |
| Firmware core (C99) + host tests | `firmware/lib/ad_core.c`, `firmware/test/test_ad.c` (`make test`) | 83 checks pass with sanitizers; C matches the Python reference on 46/46 traces |
| Board firmware (ATmega328P) | `firmware/src/main_astradand.cpp`, `make hex` | compiles: 19.7 KB flash, 1.1 KB RAM; hardware-untested |
| PCB (146 x 26 mm, 2 layers) | `hardware/` (copy of `utility10/pcb/release/astradand/` when released) | see `MANUFACTURING_MANUAL.md` |
| Shell (FDM), crystal, caps | `cad/out/*.stl`, `cad/hilt.py` | watertight; unprototyped |
| Display stand (laser), carton dieline | `cad/out/stand_laser.*`, `carton_dieline.*` | DXF + SVG |
| Spell cards (print) | `spellbook/out/spell_cards_A4.pdf` | 9 cards; Hindi names unreviewed |
| Economics | `docs/economics.md` | BOM about Rs 1,216; Rs 2,999 target |
| Test plan, design notes, manual | `docs/TEST_PLAN.md`, `docs/DESIGN.md`, `MANUFACTURING_MANUAL.md` | gates 0-4 |

Run the software: `cd firmware && make test`; `cd sim && python3 gesture_sim.py` (needs numpy); `cd cad && python3 hilt.py` (needs trimesh, manifold3d).
