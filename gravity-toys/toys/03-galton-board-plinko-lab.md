# Toy 3 · Galton Board "Plinko Probability Lab"

**One line:** Drop balls through a triangle of pegs; they pile into a bell curve. Gravity + chance
makes statistics visible. Desk toy, classroom kit and gift.

| | |
|---|---|
| Age | 6+ (Ø12 mm steel balls ⇒ small-part warning) |
| Principle | Gravity + random walk → binomial / normal distribution |
| Price | Desk model ₹ 799 · Class kit (5 boards) ₹ 3,499 |
| Tooling risk | **Lowest** – laser acrylic + MDF, no mould |

## 1. Plan
Prototype in 2 weeks; test 3 peg pitches; run 500-ball experiment to verify the bell curve; pilot of
300 units; schools' pilot (CBSE statistics class IX–XII tie-in) in 2 cities.

## 2. Design (parametric – see `../cad/generate_laser_svgs.py`)
| Parameter | Value | Why |
|---|---|---|
| Panel | 300 × 420 mm, 5 mm cast acrylic front, 6 mm MDF back | See-through, rigid |
| Ball | Ø12 mm chrome steel | Heavy, repeatable bounces |
| Peg | Ø4 mm stainless pin, 6 mm protrusion | |
| Rows | 10, hex pattern | 11 bins |
| Horizontal pitch | 24 mm | Clear gap = 20 mm = 1.67 × ball (prevents jamming, keeps randomness) |
| Row spacing | 20.8 mm (= 24·√3/2) | Equilateral grid |
| Bins | 11 × 24 mm, walls 3 mm | |
| Funnel | Entry 30 mm → 15 mm throat | Centre-feed |
| Back-gate | Slide cover to reset | Rotate board to recycle balls |
| Cavity depth | 16 mm (ball Ø12 + 4 mm) | Prevents ball stacking |

Expected distribution with N rows: bin k probability = C(10,k)/1024; centre bin 24.6 %, edges 0.1 %.
Print a theory overlay on the front for the "predict vs measure" activity.

Add-ons: tilt-adjust foot (skew the curve), 3 peg-pitch overlays, tally-sheet pad, 500-ball tube.

## 3. Deliverables
SVG/DXF cut files (generated) · BOM · assembly guide · teacher guide (6 experiments) · 500-ball
experiment data sheet · packaging · test reports.

## 4. Manufacturing & vendors
| Step | Lead |
|---|---|
| Acrylic/MDF laser | Doozy Creatives, SA Creative Store, Mekuva Technologies (Balanagar) [S] |
| Peg pins & steel balls | Bearing/fastener suppliers in Hyderabad/Bengaluru [K] |
| Assembly | In-house or SHG women's group (Telangana) [K] |
| Box | Hyderabad carton cluster [K] |
| Testing | Bharat Test House, Krishna Met Lab [S] |
| Global benchmark | Many Galton boards sold via Alibaba/Etsy [K]; premium = lab-grade (Germany/US) |

## 5. Cost
Acrylic ₹ 160 · MDF ₹ 70 · pins/balls ₹ 90 · laser time ₹ 60 · assembly ₹ 45 · box ₹ 55 → **≈ ₹ 480**.
Retail ₹ 799–999; school kit with bulk discount.

## 6. Safety
Steel balls: warning + captive design (back-gate closes, balls cannot fall out in use). Sand/polish
acrylic edges. Sealed screw-heads.
