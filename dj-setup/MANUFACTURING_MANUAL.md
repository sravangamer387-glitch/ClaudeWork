# Portable DJ / party system: manufacturing status

> **Not manufacturable: this is a plan, not a design.** There is no schematic, PCB, firmware or CAD; only market research, a concept architecture, sizing and cost models. A manufacturing manual cannot exist until the phases below are done, and writing one now would invent data.

## What exists
`01-market-and-positioning.md`, `02-concept-and-architecture.md`, `03-compliance-and-safety.md`, `04-project-plan-and-deliverables.md`, `calcs/acoustics_power.py`, `calcs/cost_model.py`. Findings: portable party systems are 100-600 W and 150-390 Wh; a standalone speaker models at about 7 % margin (weak); the DJ controller (about 27 %) and sync-light kit (about 22 %) are the differentiated products; approvals (BIS CRS, battery IS 16046, WPC/ETA, e-waste EPR) are the long pole and none is verified.

## What manufacturing would need (the project plan's gates, in order)
1. **Phase 1:** designed BOM and prototypes of the controller and light kit (the repository's `prototypes/` has Rs 1,700-1,870 breadboard prototypes: D1 beat-synced light controller, D2 MIDI controller with a Mixxx map: see `prototypes/MANUFACTURING_MANUAL.md`).
2. Schematic, PCB layout, firmware and enclosure for the controller and the light kit, using the repository's PCB toolchain and manual templates as the pattern.
3. Compliance route and lab quotes (BIS CRS, battery certification, WPC for radios).
4. ODM selection for the speaker; samples, golden unit, factory test spec, EMS RFQ.
Budget in the plan: Rs 60 lakh to 1.5 crore over 12-18 months. Follow `04-project-plan-and-deliverables.md`.
