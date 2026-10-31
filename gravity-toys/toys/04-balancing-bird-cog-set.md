# Toy 4 · "Santulan" Centre-of-Gravity Set (Balancing Bird + Roly-Poly + Tipsy Tumbler)

**One line:** Turned-wood animals that defy tipping: a bird that balances on its beak, a roly-poly
that always rights itself, a tumbler that rocks. The ideal Channapatna / Nirmal craft product.

| | |
|---|---|
| Age | 3+ (no small parts if designed ≥ 45 mm) |
| Principle | Centre of gravity below pivot = stable equilibrium |
| Price | ₹ 599 (3-piece) |
| Tooling risk | **Lowest** – lathe + hand-paint |

## 1. Plan
Weeks 1–2 CoG calculations & balsa/MDF mock-ups; weeks 3–6 turned prototypes with artisan; 6–10
pilot 300 sets; paint test + IS 9873 P3. GI/craft story (artisan names on box) drives gifting and
export.

## 2. Design
### Balancing bird
- Body: turned rubber wood, 160 mm long, beak a 6 mm cone (tip rounded R1.5 – not sharp).
- Wings: 3 mm birch ply laser-cut, 220 mm span, curved down 25°.
- Wing-tip weights: 2 × 20 g **lead-free** (zinc/brass/steel), hanging **90 mm below the beak line and swept about 95 mm FORWARD of the beak tip**. *Found by simulation (`sim/verify_designs.py`): with the weights any further back the centre of gravity falls behind the pivot and the bird tips backward.* Resulting CoG is about 43 mm below the beak tip; rocking period about 1 s. Use adjustable weight screws to trim each bird (5 mm of weight error tilts it about 3°).
- Balance rule: total CoG must lie **≥ 25 mm below** the beak contact point. Verify by computing:
  Σ m·y / Σ m with beak tip as origin (positive = down). Tune with weight screws.
- Stand: wooden perch with shallow dimple (R 3 mm) for the beak.

### Roly-poly (weeble)
- Hemisphere base Ø70 mm + body Ø60, weight 60 g steel slug in the base.
- Righting condition: CoG lower than centre of curvature of the base → R_base (35) > h_cog (<35 mm above
  floor contact). The CoG calculates to about 24 mm with a 60 g slug 8 mm above the floor (lever arm 11 mm at 90° tilt): works; a heavier or lower slug gives a livelier return.

### Tipsy tumbler (rocking duck)
- Curved rocker R 90 mm, two dowel legs, counterbalance weight in tail.

Finish: natural/water-based lacquer, 3 colours per animal, hand-brushed motif (peacock, parrot, owl).
Weights fully captive (screwed + epoxy plug) – inaccessible.

## 3. Deliverables
CoG worksheet (Excel) · lathe drawings · wing DXF · paint-pattern guide · artisan training sheet ·
packaging with craft story · experiment card ("find the balance") · test reports.

## 4. Manufacturing & vendors
| Step | Lead |
|---|---|
| Turning & lacquer (premium, GI craft) | Bharat Art & Crafts, Vin Global Export (Channapatna/Bengaluru) [S] |
| Telangana-origin option | Nirmal Toys & Arts Industrial Co-operative Society (poniki) [S] |
| Wing cutting | Hyderabad laser shop [S] |
| Weights | Local zinc/brass casting [K] |
| Export channels | Craft exporters/D2C platforms (e.g. iTokri) [S] |
| Testing | Bharat Test House / Krishna Met Lab [S] |

## 5. Cost
Wood ₹ 45 · turning ₹ 110 · paint ₹ 60 · weights ₹ 30 · wings/laser ₹ 15 · pack ₹ 60 → **≈ ₹ 320**;
retail ₹ 599–799; export ₹ 1,800+ (craft premium).

## 6. Social impact angle
Pay artisan above prevailing piece rate, name them on pack — addresses the middleman and cheap-import
pressure reported in Channapatna.
