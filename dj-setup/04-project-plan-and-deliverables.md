# 04 · Project Plan, Workstreams and Deliverables

**Size:** this is a 12–18 month, ₹60 lakh – ₹1.5 crore project (assumption) if you design speaker, controller and lights. The plan therefore has **go/no-go gates** so you never commit large money before key risks are retired.

## 1. Who does what
| I (Claude) can do | Needs people, labs or vendors |
|---|---|
| Market and compliance research updates, requirement specs, architecture | Customer interviews, field trials |
| Firmware: portable C core, DSP algorithms (filters, echo, beat tracker), MIDI/USB descriptors, light-sync protocol, host tests | Running firmware on real MCU/SoC boards, debugging hardware |
| Simulations: acoustics sizing, thermal, battery runtime, power-supply budgets, tolerance stack-ups | Anechoic/acoustic measurement, thermal chamber, battery abuse tests |
| Schematics (block, power, interfaces), pin maps, netlists, BOM + costing models, cost-down options | PCB layout sign-off by an experienced hardware engineer, EMC |
| Parametric enclosure CAD (STL/STEP-style), mass and cost checks | Tooling design review, mould making, sampling |
| Test specs, factory test jigs' requirements, RFQ packs, listing copy, manuals, project tracking in GitHub/Drive | Manufacturing, certification, certification testing, legal opinion |

## 2. Phases and gates
| Phase | Weeks | What happens | Gate (go/no-go) |
|---|---|---|---|
| **0 Discovery** | 1–4 | Verify rules (BIS/WPC/battery), talk to 20 target users and 5 DJs/event operators, quote ODM speakers, get 3 EMS quotes, shortlist radio and battery modules, decide product scope | **G0:** confirmed approval path and cost; at least 10 users would pay; scope fixed (recommend B + C first) |
| **1 Concept and architecture** | 5–10 | Detailed specs, designed BOM (not guessed), firmware architecture, risk list, industrial design sketches, cost model v2 | **G1:** designed BOM gives ≥ 25 % marketplace contribution at target price, or price/scope changed |
| **2 Prototype v1 (modules)** | 11–24 | Controller dev board + firmware; light node + hub prototypes; ODM speaker samples; 3D-printed enclosures | **G2:** each module works on the bench; play-test with 10 users |
| **3 Integration and field trials** | 25–32 | Synced system, outdoor tests (heat, dust, splash), battery tests, SPL tests, app v1 | **G3:** meets spec; no safety failures |
| **4 Pre-compliance and DFM** | 33–40 | Pre-scan EMC, safety, battery; tooling design; EMS pilot; supplier audits | **G4:** pre-compliance passed; tooling approved |
| **5 Pilot batch** | 41–48 | 100–300 units; QC process; reviews from beta customers | **G5:** field failure < 2 %, certifications filed |
| **6 Certification and launch** | parallel from week 20 | BIS/WPC/battery certification; marketplace and D2C setup; launch | **G6:** certificates in hand |

## 3. Workstreams and deliverables
| Workstream | Key deliverables |
|---|---|
| Product & UX | Requirements, personas, user manuals, preset library (Bollywood/regional BPM ranges, dhol/tabla loops), app wireframes |
| DJ audio and firmware | Core library (decks, mixer, effects, beat tracking), USB MIDI/audio, file-system playback, host tests, factory test mode |
| Lighting | Light node firmware, sync protocol, DMX512 driver, safe-flash rules, scene library |
| Hardware | Block/schematic set, pin maps, BOMs, power budget, PCB layout (by a hardware engineer), test jig requirements |
| Battery and power | Pack spec, BMS spec, charger selection, runtime model, safety test plan |
| Acoustics | Driver/cabinet simulation, tuning targets, limiter curves, measurement plan |
| Mechanical/ID | Parametric CAD, 3D-printed prototypes, tooling drawings for vendor, IP rating plan |
| Compliance | Standards matrix, test plan, lab quotes, BIS/WPC applications, label content |
| Supply chain | RFQs, vendor scorecards, price tables, second-source plan |
| Commercial | Pricing model, channel plan, listing assets, support and warranty policy |

## 4. Budget by phase (rough, assumption)
| Phase | Cost ₹ lakh |
|---|---|
| 0 Discovery | 1–2 |
| 1 Concept | 2–4 |
| 2 Prototype | 8–15 |
| 3 Field trials | 4–8 |
| 4 Pre-compliance and DFM (including tooling deposits) | 15–35 |
| 5 Pilot batch | 15–35 |
| 6 Certification and launch | 15–30 |
| **Total** | **60–130 +** |

## 5. Top risks
| Risk | Mitigation |
|---|---|
| Approvals take longer or cost more (BIS/WPC/battery) | Phase 0 clarification; use pre-approved radio and battery modules |
| Speaker economics poor (modelled ~7 % margin) | Source speaker from ODM; lead with controller + lights |
| Battery safety incident | LiFePO4, certified cells, BMS design review, abuse testing |
| Firmware complexity (DJ audio quality, latency) | Prototype algorithms on a laptop first; pick a capable SoC; allow 3-month firmware contingency |
| Heat and dust failures in Indian summer/monsoon | Thermal derating, ingress testing, field trials in May and monsoon |
| Counterfeit/copycat lights | Own the sync protocol and firmware; design registration |
| Demand uncertain | Pre-orders and beta programme before tooling |

## 6. Immediate next steps (this week)
1. Decide scope for Phase 0: recommend **PP-C controller + PP-L light kit**, speakers via ODM.
2. I draft: requirement specs, the user interview guide, ODM/EMS RFQ packs, designed BOM v1, firmware architecture and a beat-tracker prototype tested on sample audio.
3. You: arrange 5–10 interviews (DJs, wedding/event operators, house-party hosts), contact a BIS/WPC consultant, and pick 2–3 ODM/EMS vendors to approach.
4. Create a GitHub project board with these phases; mirror documents in Drive.

## 7. Decisions I need from you
1. Budget ceiling and who funds each phase.
2. Scope: controller + lights first, or also speakers from the start?
3. ODM white-label speaker (fast) vs own speaker design (slow, differentiated)?
4. Target launch window and the priority channel (Amazon, own site, event-rental partners).
