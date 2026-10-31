# Portable DJ / Party System – Project Plan (home and parties, with lights)

Prepared 2026-10-31. Status: **research and planning done; no hardware or firmware built yet.** This is the "bigger project": 12–18 months, ₹60 lakh–1.5 crore if designed in full.

| File | Contents |
|---|---|
| `01-market-and-positioning.md` | Market bands in India, gaps, positioning options, segments |
| `02-concept-and-architecture.md` | Product family (controller, light kit, speaker, bundle), sizing, architecture, economics |
| `03-compliance-and-safety.md` | BIS CRS, battery, WPC/ETA, e-waste, safety rules, IP and content |
| `04-project-plan-and-deliverables.md` | Phases with go/no-go gates, workstreams, who does what, budget, risks, next steps |
| `calcs/acoustics_power.py` + `sizing.md` | Amplifier power, battery and weight needed for three party sizes |
| `calcs/cost_model.py` + `cost_model.md` | Top-down margin model for speaker, controller, light kit and bundle |

## Headline findings
1. **Home and terrace parties are portable (about 100–600 W, 150–390 Wh); banquet halls are not** (about 3 kW, 1.5 kWh).
2. **A standalone party speaker is the weakest product** (about 7 % modelled margin at ₹14,999; the market is crowded from ₹2k to ₹30k).
3. **The DJ controller (~27 %) and sync-light kit (~22 %) are the differentiated, better-margin pieces**; the bundle models at ~26 % of ₹59,999.
4. **Recommended start:** controller + light kit, speakers from an ODM, works with any speaker; own speaker later.
5. **Approvals are the long pole:** BIS CRS, battery (IS 16046), WPC ETA for radio, e-waste EPR. None of it is verified against official text yet.
6. The toy work showed real design costing raises BOM guesses by 20–50 %; treat these margins as optimistic until Phase 1 produces a designed BOM.

## Open questions
Market size (not found); import duty on speakers/controllers; exact BIS CRS coverage; WPC import licence rules; battery certification route; whether to bundle software.

## Mirroring rule
Kept in the repo (`dj-setup/`) and in the Google Drive folder "DJ Setup". Update both in the same session.
