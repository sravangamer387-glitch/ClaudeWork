# Product 1 · Desi Games Studio

Four print-and-box games for ages 7+ in **English, Hindi and Telugu**. Status: **designed, balance-simulated and print-ready PDFs generated; not yet play-tested with children, and the Hindi/Telugu text and all quiz facts must be reviewed before printing.** Prototype cost about Rs 1,300 (see §5).

## 1. The games
| Game | Players | Mechanic | Balance verified by |
|---|---|---|---|
| **Cricket Dhamaka** | 2 | Secret shot (Defend/Drive/Slog) vs secret delivery (Yorker/Bouncer/Spin), roll a d6 on a 3×3 result table; 12-ball innings, 2 wickets | search + game-theory solve + Monte Carlo |
| **Ganit Ladder** | 2–4 | Snakes and ladders with 24 "?" squares: answer a multiplication-table card; correct = roll again, wrong = back 4 | 20,000-game simulations |
| **India Yatra** | 2–6 | 24 multiple-choice GK cards in 3 language decks; first to 10 cards | answer positions balanced A/B/C |
| **Sabzi Mandi** | 2–4 | Shopkeeper makes change from a till; customers buy vegetables (prices Rs 3–25) | 20,000-sale simulation |

## 2. Verification results (`sim_results.md`, `src/sim_*.py`)
- **Cricket Dhamaka:** the result table was **found by search** under rules: Defend = small scores and fewest wickets, Slog = big scores and most wickets, no strategy dominated. At equilibrium the batter mixes shots about 34/34/32 % and the bowler deliveries 46/22/32 %, so **every card is useful**. A two-over innings averages **16.8 runs**; all-out in **32 %** of innings.
- **Ganit Ladder:** first-player advantage under 1.5 points; 24–35 turns per player in a 2-player game. **First version failed its purpose:** the maths hardly changed who won (55.6 % for a 90 %-accurate player against a 50 % one). After adding more "?" squares and a back-4 penalty the **better mathematician wins 58.8 %**: skill matters but luck keeps weaker players in the game.
- **Sabzi Mandi:** the long-run simulation failed (6.8 % of sales could not be made), so a house rule was added: **once per sale the shopkeeper may break one note at the bank ("chhutta")**, and the model was corrected to a real game length (12 sales per shift). Result: **2.7 %** of sales cannot be made exactly (needs the bank rule in 1.1 %).
- Not verified: fun, rules clarity for children, real play length: **play-test with 10 children**.

## 3. Print files (`out/`, regenerate with `src/render.py`)
`cricket_dhamaka_print.pdf` (12 cards, result table, score sheet) · `ganit_ladder_board.pdf` (594 mm board) · `ganit_ladder_cards.pdf` (60 cards) · `india_yatra_cards_{en,hi,te}.pdf` (24 cards each) · `sabzi_mandi_items.pdf` (24 cards) · `sabzi_mandi_money.pdf` (108 cards) · `rules_*.pdf` (3 languages each). Cards are 63 × 88 mm, 3 × 3 per A4 page at 200 dpi with crop marks. The renderer uses Pillow with RAQM shaping and Noto fonts so Hindi and Telugu conjuncts render correctly (two rendering faults were found and fixed while building: Latin letters inside Hindi/Telugu lines showed empty boxes, and a title collided with the table).

## 4. Economics (`src/econ.py`, marketplace, GST 5 % assumed – verify)
| Game | Price Rs | BOM guess Rs | Contribution Rs | Margin | Margin if BOM +30 % |
|---|---|---|---|---|---|
| Cricket Dhamaka | 499 | 90 | 228 | 48 % | 41 % |
| Ganit Ladder | 799 | 150 | 375 | 49 % | 42 % |
| India Yatra | 599 | 110 | 284 | 50 % | 43 % |
| Sabzi Mandi | 799 | 180 | 340 | 45 % | 36 % |

BOM covers printing, die-cut/box and packing at about 1,000 sets (assumption). Fixed launch costs: artwork review, native-language proofreading, printer set-up, testing (about Rs 1–2 lakh, assumption).

## 5. Prototype (about Rs 1,300, well under Rs 3,000)
| Item | Rs |
|---|---|
| Cricket: 4 A4 pages colour on 250 gsm | 80 |
| Ganit: 594 mm poster print + 7 card pages | 490 |
| India Yatra: 2 languages x 3 pages | 120 |
| Sabzi Mandi: 12 pages | 240 |
| Rules (mono, 12 pages) | 60 |
| Dice, tokens, till tray (box), pouches | 100 |
| Cutter, glue, lamination pouches | 200 |
| **Total** | **1,290** |

Prices are estimates for a local print shop. **Playtest plan:** 10 children aged 7–12, 3 sessions per game; record rule confusions, session length and which cards are never chosen.

## 6. Compliance and content checklist
1. **Toys QCO:** confirm with BIS or a lab whether board/card games for children under 14 need IS 9873 testing (inks and paper may fall under chemical requirements). Use food-grade or low-migration inks; ask the printer for a heavy-metal report.
2. **Age grade and warnings:** small parts (dice, tokens) need a small-parts warning for under-3s; label 7+.
3. **Legal Metrology:** MRP, contents ("108 money cards"), maker, month/year.
4. **Content review:** native speakers must proofread Hindi and Telugu (written by me, unreviewed); fact-check every quiz answer against two sources before printing; avoid licensed names/logos (no team or player names).
5. **IP:** original mechanics and art; run a trademark search for the game names.

## 7. Manufacturing / RFQ essentials
Ask 3 Hyderabad print/packaging houses for: 300 gsm art card + 350 gsm box board, aqueous varnish, die-cut cards (63 × 88 mm, 3 mm radius), tuck box (about 70 × 95 × 28 mm for card games; 300 × 300 × 45 mm for the board game), shrink-wrap, MOQ 500 and 1,000 sets, lead time, price per set, Pantone tolerance, proof approval. Own the print files.

## 8. Listing copy (drafts)
- **Cricket Dhamaka – 2-Player Cricket Strategy Card Game | Hindi English Telugu | Ages 8+.** Bullets: secret shot vs delivery; every card useful (balanced by 20,000 simulated games); 15-minute games; bilingual rules; travel-friendly.
- **Ganit Ladder – Multiplication Tables Snakes & Ladders.** Practice tables while you play; 60 table cards; for 2–4 players.
- **India Yatra – 72-Card Quiz Game (3 language decks).** Verified-fact GK cards.
- **Sabzi Mandi – Learn Change & Money Game.** Shopkeeper and customers, Rs 1–50 money cards.
Do not claim "educational outcomes" or curriculum alignment until verified.

## 9. Risks
Copycats (games are easy to copy: series, language and art are the defence); quiz-fact errors (reputational); language quality; marketplace discovery; printing colour variation.

## 10. Next steps
Native-speaker proofreading → 10-child playtest → print 20 prototype sets → printer RFQ → listing.
