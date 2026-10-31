# Products – six approved builds (2026-10-31)

| # | Product | Verified on this machine | Economics verdict | Status |
|---|---|---|---|---|
| 1 | [Desi Games Studio](01-desi-games/README.md) | game-balance simulations, print PDFs | 45–50 % margin (BOM guess) | needs proofreading + playtest |
| 2 | [Kalakriti Automata](02-automata/README.md) | cam/gear geometry checks, parts sheets | about 35–44 % | needs a laser-cut prototype |
| 3 | [Prayog STEM kit](03-prayog/README.md) | 40 firmware checks, 20 experiments validated numerically | designed BOM Rs 2,580 (below guess) | needs hardware + sales route |
| 4 | [Jal-Rakshak](04-jal-rakshak/README.md) | 20 checks + tank/pump simulation | designed BOM Rs 660 vs guess 395: thin margin | mains certification needed |
| 5 | [Kheti-Mitra](05-kheti-mitra/README.md) | 22 checks + 90-day water-balance simulation (saving 43 %, simulated only) | designed BOM Rs 620 vs guess 520 | needs field trial |
| 6 | [Gas-Suraksha](06-gas-suraksha/README.md) | 34 checks, leak-time model | **loses money below about Rs 1,300**; safety-critical | design study; do not sell without certification |

Run any firmware test with `make test` in the product's `firmware/` folder; `make hex` needs gcc-avr, avr-libc, arduino-core-avr. Everything is a prototype design: no physical hardware has been built or tested.
