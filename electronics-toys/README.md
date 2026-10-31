# Electronic Toys for the Indian Market – Top 50, Phase by Phase

Prepared 2026-10-31. Evidence tags: [S] found in web research, [K] background knowledge, (assumption) my estimate. Scores are my judgement, not market data.

| Phase | File | Status |
|---|---|---|
| 1. Market, rules, manufacturing base | `phase1-market-and-rules.md` | Done |
| 2. Top 50 ranked list (scoring model) | `phase2-top50.md`, `top50.csv`, `build_top50.py` | Done |
| 3. Commercial strategy | `phase3-commercial-strategy.md` | Done |
| 4. Build, test, compliance plan | `phase4-build-and-compliance.md` | Done (plan) |
| 5. Wave 1 design briefs (top 10) | `phase5-wave1-design-briefs.md` | Done (briefs) |
| 6. Design & development for Wave 1 (firmware, hardware, enclosures, tests) | `wave1/` (see `wave1/README.md`, `wave1/docs/findings.md`) | Done to prototype level – not built or bench-tested |
| 7. Real MCU port, PCB layout, prototypes, RFQs, listing copy | – | Next |

## Headline findings
1. India's electronic-toy opportunity is **Indian-language and curriculum-linked toys**: rhymes/stories player, keyboard with Indian instruments, learning tablet, tabla pads, cricket game.
2. **Marketplace margins are thin (about 6–22 %)** at 1,000-unit costs; fixing this needs shared platform boards, volume, content ownership, bundles and B2B/school sales.
3. **Keep radio, lithium and under-3 designs out of Wave 1** until WPC/ETA, battery and safety rules are confirmed.
4. **Start with three products on one audio board**: rhymes player, star projector lamp, cricket game.
5. Rough Wave 1 capital for 3 products: ₹20–30 lakh (assumption).

## Correction from Phase 6 (important)
Designing and costing the first three products showed the Phase 2 cost guesses were too low: at the Phase 5 prices **none of them meets the 25 % contribution gate** (rhymes player about 9 % with a flash-based design, cricket game about 7 %, star lamp negative). Reprice or redesign before any tooling: see `wave1/docs/findings.md`. Phase 2 margin scores for these three are optimistic.

## Open items to verify before spending
WPC/ETA rules for Bluetooth and 2.4 GHz; battery certification; e-waste EPR thresholds; 2026 import duty; real Amazon.in bestseller data; GST on electronic toys (18 % assumed); every vendor named.

## Mirroring rule
Everything here is kept in two places: this repo (folder `electronics-toys/`) and the Google Drive folder "Electronics Toys". Update both in the same session.
