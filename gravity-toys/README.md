# Gravity Toys for Kids – Research, Top 5 Designs & Sourcing (Hyderabad + Global)

Prepared 2026-10-31. Start with **[00-research-and-sourcing.md](00-research-and-sourcing.md)** (market,
materials, vendor leads, BIS/EN71/ASTM compliance), then the five toy packages. Each toy file has:
**Plan → Design (with numbers) → Deliverables → Manufacturing vendors → Cost → Safety.**

| # | Toy | Age | Gravity concept | Build route | Tooling risk | Indicative retail |
|---|---|---|---|---|---|---|
| 1 | [Timber Tower Marble Run](toys/01-timber-tower-marble-run.md) | 4+ | Energy, incline | Laser + CNC + lathe (wood) | Low | ₹1,499 |
| 2 | [Drop Quest logic puzzle](toys/02-gravity-maze-puzzle.md) | 8+ | Routing by height | Laser v1 → injection v2 | Med-high | ₹1,099 |
| 3 | [Galton Board Plinko Lab](toys/03-galton-board-plinko-lab.md) | 6+ | Probability/random walk | Laser acrylic + MDF | Lowest | ₹799 |
| 4 | [Santulan balance set](toys/04-balancing-bird-cog-set.md) | 3+ | Centre of gravity | Turned wood, hand-painted | Lowest | ₹599 |
| 5 | [Ramp Racers Physics Lab](toys/05-ramp-racers-physics-lab.md) | 5+ | Inclined plane, mass vs. acceleration | Ply + turned parts | Low-med | ₹1,299 |

## Why these five (selection logic)
Scored from 10 candidates on: demand evidence, play/learning value, Hyderabad manufacturability,
capex, compliance risk, margin. Rejected: loose-magnet tile runs (magnet-ingestion risk, China commodity
price war), Newton's cradle (momentum rather than gravity), water/sand timers (low repeat value),
motorised lift runs (electrical scope, IS 15644).
Mix is intentional: two craft-led low-capex toys (3, 4), two wood/lab toys (1, 5), one scalable
IP-led puzzle (2) that earns the injection-mould investment only after validation.

## Recommended launch order
1. **Galton Board + Balance Set** (cheapest, fastest, 8–10 weeks) → cash and learnings
2. **Timber Tower** (hero product, expansion packs)
3. **Ramp Racers** (school lab channel)
4. **Drop Quest** (injection v2 once v1 sells)

## Business launch pack (`business/`)
- `01-business-plan.md` – recommendation, unit economics, compliance, 12-week plan, budget
- `02-manufacturer-rfq-pack.md` – RFQ email, vendor scorecard, product spec annexes, QC checklist
- `03-listing-copy-pack.md` – Amazon/Etsy listing copy and compliance fields
- `05-unit-economics.csv` – marketplace margin model (formulas)
- **Note:** the unit economics show the original retail prices lose money on Amazon; use the prices in the business plan.

## Verification (new)
- `sim/verify_designs.py` (+ `sim/verification.md`) – physics checks for all toys; **found three design corrections**: marble-run ramps must be 6–8° not 8–12°; the balancing bird's weights must sit ~95 mm forward of the beak; felt wheels need ≥ 10° ramps. Run: `python3 -I sim/verify_designs.py`.

## Files
- `cad/generate_laser_svgs.py` – parametric laser-cut files (`python3 -I cad/generate_laser_svgs.py cad/out`);
  outputs in `cad/out/` (Galton front/back, tower plate, racer ramp). Includes asserts that guard
  ball-clearance rules.

## Honest limitations
- Vendor names come from directory/marketplace listings or background knowledge; **none are verified**.
  Do RFQs, factory visits and sample tests before committing. No Hyderabad 3D-print bureau or
  toy-test lab was found in research.
- Costs and mould prices are planning assumptions, not quotes.
- Standards figures (e.g. 31.7 mm small-part cylinder, ball-size exemption, magnet limits) come from
  secondary sources; confirm in IS 9873 (Part 1):2025 / EN 71 / ASTM F963 before freezing dimensions.
- `Drop Quest` is intentionally an original mechanism; get an IP/patent review before launch.
- Products in the CAD folder are 2D starting files, not production-validated drawings.

## Mirroring rule
Every file in this folder is kept in two places: this repo and the Google Drive folder "Gravity Toys"
(owner sravank387@gmail.com). Docs in Drive are Google Docs converted from these markdown files; SVGs and
the script are stored as-is. Task checklists live in GitHub issues #1–#7 and in `TASKS.md` (and its Drive twin).
When one side changes, update the other in the same working session.
