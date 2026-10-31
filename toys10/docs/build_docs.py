import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__)); from toys import TOYS, contribution
ROOT = os.path.join(os.path.dirname(__file__), ".."); idx = []; rows = []
for t in TOYS:
    b = sum(v for _, v in t["bom"]); p = sum(v for _, v in t["proto"]); assert p <= 3000
    c, m = contribution(t["price"], b, t["gst"]); c3, m3 = contribution(t["price"], b * 1.3, t["gst"])
    d = os.path.join(ROOT, f"{t['id']}-{t['slug']}"); os.makedirs(d, exist_ok=True)
    kind = {"electronic": "Electronic (low voltage, battery)", "laser": "Laser-cut MDF/acrylic", "physics": "Plumbing/pneumatic (pressure-tested)", "print": "Printed + wooden cubes"}[t["kind"]]
    first = f"\nFirst-draft price Rs {t['price_first']} lost or barely made money, so it was raised." if "price_first" in t else ""
    r = [f"# {t['id']} · {t['name']}", "", f"*{t['tag']}*", "", f"**Ages {t['ages']} · Players {t['players']} · {kind}.** Status: designed, verified as far as a computer can; **no prototype built; nothing tested with children.**", "", "## How it plays"] + [f"{i}. {s}" for i, s in enumerate(t["play"], 1)]
    r += ["", "## Design", t["design"], "", "## What I verified (and what I did not)", t["verified"], "", "## Prototype budget (Rs %d, limit Rs 3,000)" % p, "| Item | Rs |", "|---|---|"] + [f"| {n} | {v} |" for n, v in t["proto"]] + [f"| **Total** | **{p}** |", "", "(Local-market estimates; verify with quotes.)", "", "## Designed production BOM (~2,000 units, estimate: Rs %d)" % b, "| Item | Rs |", "|---|---|"] + [f"| {n} | {v} |" for n, v in t["bom"]]
    r += ["", f"## Economics (marketplace; GST {int(t['gst']*100)} % assumed)", f"Price **Rs {t['price']}** → contribution **Rs {c:,.0f} ({m:.0%})**; with BOM +30 %: Rs {c3:,.0f} ({m3:.0%}). Same fee model as the earlier products (ads 12 %, returns 8 %, shipping Rs 90, closing Rs 30, referral 8 % at or above Rs 1,000).{first}", "", "## Manufacturing", t["mfg"], "RFQ: ask 3 vendors for price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.", "", "## Compliance (to verify)", "Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; " + ("battery safety, BIS toy-electrics, e-waste EPR, noise level; " if t["kind"] == "electronic" else "") + ("paint/ink heavy-metal report; " if t["kind"] != "electronic" else "") + "no licensed names or logos.", "", "## Listing title (draft)", t["listing"], "", "## Risks", t["risk"], "", "## Next steps", "Build the prototype from the budget above → test with 5 children → adjust → RFQ.", ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(r))
    idx.append(f"| {t['id']} | [{t['name']}]({t['id']}-{t['slug']}/README.md) | {t['ages']} | {t['kind']} | {p} | {b} | {t['price']} | {c:,.0f} ({m:.0%}) | {c3:,.0f} ({m3:.0%}) |")
    rows.append([t["id"], t["name"], t["kind"], p, b, t["price"], round(c), round(m, 3), round(c3), round(m3, 3)])
with open(os.path.join(ROOT, "docs", "economics.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "name", "kind", "prototype_rs", "designed_bom_rs", "price_rs", "contribution_rs", "margin", "contribution_bom_plus30", "margin_bom_plus30"]); w.writerows(rows)
bc, bm = contribution(1499, 345, 0.18); bc3, bm3 = contribution(1499, 345 * 1.3, 0.18)
open(os.path.join(ROOT, "README.md"), "w").write(f"""# Ten new toys (2026-10-31)

All ten are designed with the same discipline as the six products: engines and simulations verified on this machine, **prototype ≤ Rs 3,000 each**, designed production BOM, economics with +30 % BOM sensitivity, manufacturing and compliance notes. **Nothing is built or child-tested.**

| # | Toy | Ages | Type | Prototype Rs | BOM Rs | Price Rs | Contribution Rs | If BOM +30 % |
|---|---|---|---|---|---|---|---|---|
""" + "\n".join(idx) + f"""

## What the numbers say
- **Best margins:** Marble Cricket (43 %), Tilt Maze, Rangoli Spiro Gears and Rubber-band Racer (all 27–32 %); these are laser-cut and share the laser shops used by the earlier gravity and automata toys.
- **Electronic toys:** the first-draft prices (Rs 499–799) lost money at the designed BOM; they are priced at Rs 699–1,299 above. Taal Memory and Aloo Bomb are still thin at +30 % BOM. **Recommendation (decision): sell the three party games (Reflex Raja, Taal Memory, Aloo Bomb) as one "Desi Arcade" box with one board and a game-select switch at Rs 1,499** (BOM about Rs 345 → contribution Rs {bc:,.0f} ({bm:.0%}), Rs {bc3:,.0f} ({bm3:.0%}) if BOM +30 %). The merged firmware is built: `electronic/release/desi_arcade.hex` (hold button 1/2/3 while switching on to pick Reflex Raja / Taal Memory / Aloo Bomb; 5.5 KB).
- **Paper Rocket Air Launcher is the risky one:** a projectile toy. Do not sell it without a standards review; the design already forces a low-pressure relief valve (a first draft was 5× over my placeholder energy limit).
- **Launch order I recommend:** Marble Cricket, Tilt Maze, Rangoli Spiro Gears (one laser-shop trip), then Katha Cubes (needs an illustrator and proofreading), then the Desi Arcade box.

## Layout
`electronic/` C engines + tests + Nano demo hex for toys 01–04 (`make test`, `make hex`) · `sims/` simulations and generators · `out/` SVG cut files, previews, CSV · `docs/` results, economics.csv, `toys.py` (data), `build_docs.py` (regenerates every README) · one folder per toy with its README.

## Verification summary
Electronic engines: 80,045 host checks, sanitizers on. Spiro Gears: 8 gear pairs verified to close with the predicted petal count (my first counting method was wrong and was replaced). Rocket: relief pressure derived from an energy limit. Maze: three BFS-verified mazes with trap holes on dead ends only. Racer: model constant corrected by 6×. Marble Cricket: pockets chosen by search, Monte Carlo of 100,000 overs. Katha Cubes: 36 distinct words, 46,656 stories.
""")
print("\n".join(idx))
