# Decisions and closure (taken by Claude on the owner's instruction, 2026-10-31)

Basis: per-unit economics from each product's `docs/econ`, verification status, and certification burden. These are recommendations the owner delegated to me; every one can be reversed. I cannot verify market demand, so each "go" has an exit test.

| # | Product | Decision | Why | Closure / exit criterion |
|---|---|---|---|---|
| 1 | Desi Games | **GO – launch first** | 45–50 % margin, no electronics, only toys-QCO check | Close when: proofreading sheets returned, 10-child playtest passes (≥ 7/10 "play again"), printer quote ≤ BOM guess +30 %. If playtest fails, rewrite the failing game only. |
| 2 | Automata | **GO – second** | 35–44 % margin, same laser shops | Close when: cardboard mock-up and one laser-cut set assemble in ≤ 60 min by an 8-year-old with a parent, and the cam turns with one finger. |
| 3 | Prayog | **PILOT ONLY** (no stock) | route to schools unknown; 22 % margin if BOM +30 % | Close when: 2 schools run 5 experiments and one placed a purchase order or quoted a procurement route. If none in 3 months: shelve. |
| 4 | Jal-Rakshak | **PARK** (do not build mains version; do not build a low-voltage "Lite") | Rs 4–8 lakh certification against Rs 308 contribution at the incumbent-aligned Rs 1,799; a Rs 199–400 alarm price war for the Lite variant | Reopen only with an electronics partner who already holds the safety approvals (white-label route) or a B2B order for ≥ 500 units. Firmware and sim stay as reusable assets. |
| 5 | Kheti-Mitra | **GO to field trial, then decide** | best margin of the electronics (35 % at Rs 2,299) and low voltage | Close when: 60-day trial with 10 users shows ≥ 25 % water saving vs timer and ≤ 1 sensor failure per 10 units. |
| 6 | Gas-Suraksha | **STOP – design study closed** | safety-critical; loses money below Rs 1,300; liability risk is unbounded for a hobby-class sensor | Reopen only with a certified-sensor-module partner, a lab quote and a liability policy. Never sell the demo hex as a safety device. |

## Other decisions
- **Pricing:** use each README's recommended price (games Rs 499–799, automata Rs 899 / set Rs 2,999, Prayog Rs 7,999, Kheti-Mitra Rs 2,299).
- **Names:** Desi Games, Kalakriti, Prayog, Kheti-Mitra are working names; run trademark search (class 9/28/16) before printing. Do not use "Suraksha"/"Rakshak" claims anywhere on unsold product.
- **GST/fees:** keep my assumptions (games 5 %, electronics 18 %); the owner's accountant confirms before pricing goes live.
- **Sequence for the owner:** (1) games + automata prototypes this month, (2) Kheti-Mitra trial in parallel, (3) Prayog pilot conversations, (4) the 10 new toys in `toys/` only after games/automata show sell-through.
- **What is closed on my side:** all firmware, simulations, print files and documents; nothing else can be advanced without people, hardware or a lab (see HANDOFF.md).
