# Toy 2 · "Drop Quest" – Gravity Logic Puzzle

**One line:** A solo logic game: place coloured towers and tubes on a grid so a dropped marble
travels start → target. Challenge-card driven, 60 levels. This is the category's best-seller type,
so we build an **original mechanism** rather than clone ThinkFun's *Gravity Maze* (check patents/trade dress before launch).

| | |
|---|---|
| Age | 8+ (marble Ø14 mm → small-part warning) |
| Principle | Height → direction; gravity-guided routing; planning/sequencing |
| Price | ₹ 899–1,199 |
| Tooling risk | **Medium-high** – injection mould for towers/tubes (or MDF-laser version for v1) |

## 1. Plan
1. **v0 (wk 1–3)** – 5×5 cardboard & laser MDF prototype, write 12 puzzles, user-test 10 kids.
2. **Puzzle engine (wk 2–6)** – Python solver generates & verifies 60 levels with unique solutions
   (write once; reuse for expansion packs/app).
3. **v1 launch version – laser MDF/acrylic** (no mould) – 500-unit pilot.
4. **v2 injection version** – amortise mould after validating 3,000+ sales.
5. BIS licence for v2 plastic parts (ABS, heavy metals, colourants).

## 2. Design
- **Board:** 5 × 5 grid of 38 mm cells, base 230 × 230 × 8 mm, 4 rubber feet, start-socket on left
  edge, target cup on right.
- **Towers (cell parts):** heights 1, 2, 3 units (1 unit = 20 mm) with Ø16 mm vertical bore; a marble
  dropped on a tower exits at its base and rolls into any adjacent opening.
- **Tubes (tiles):** straight (2 cells), elbow, "bridge" (passes over another tube – requires height
  stacking, makes puzzles deep).
- **Rule:** marble falls only downward or horizontally through tubes; the exit side of a tower is
  indicated by a notch (orientation rotatable 4 ways).
- **Marble:** Ø14 mm glass or steel; tube bore Ø17 mm (3 mm clearance, avoids jams).
- **Challenge cards:** 60 puzzles, 4 difficulty bands (green/blue/red/black); card back shows solution.
- Colour-blind-safe palette + shape cues.

Solver spec: state = placement of ≤ 8 pieces on grid; BFS over placements with pruning by height
monotonicity; accept only levels with exactly 1 minimal solution.

## 3. Deliverables
Rulebook · puzzle generator + 60 verified levels · board/tower CAD (STEP) · laser DXF (v1) · mould
design pack (v2: 8-cavity tower family, 4-cavity tubes) · tolerance study · packaging · BIS test reports.

## 4. Manufacturing & vendors
| Step | Lead |
|---|---|
| v1 laser parts | Doozy Creatives / SA Creative Store (Balanagar) [S] |
| v2 mould design | CITD Balanagar [K] for design review; Efficient Technocrafts [S] / Ashok Brand [S] for tool build |
| v2 moulding | DSC Plastic Industries (existing plastic toys) [S], Device Generation [S] |
| Resin | Virgin ABS (Indian producer, e.g. LG Polymers Vizag) [K] |
| Marbles | Firozabad glass [K]; steel balls via bearing distributors [K] |
| Cards/box | Hyderabad print cluster [K] |
| China benchmark | Shenzhen/Dongguan ABS marble-run OEMs via Alibaba/HKTDC [S] |

## 5. Cost
v1 landed ≈ ₹ 380 (laser) · v2 ≈ ₹ 210 at 5k/yr + mould ₹ 12–20 lakh (assumption). Retail ₹ 1,099.

## 6. Risks
IP resemblance to existing products (mitigate: unique tower-bore mechanic, legal review); tube jamming
(tolerance ladder test 16.5/17/17.5 mm); marble loss (spare marbles + pouch).
