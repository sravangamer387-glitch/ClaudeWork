# Desi Games Studio: manufacturing manual (4 print-and-box games)

> **Status: print files exist; nothing has been printed, cut or play-tested.** Hindi/Telugu text and all quiz facts are unreviewed and **must not go to print** before a native-speaker proofread and a two-source fact check (see section 9).

## 1. What is made

| Game | Contents per set | Files (`products/01-desi-games/out/`) |
|---|---|---|
| Cricket Dhamaka (2 players) | 12 cards, result-table sheet, score sheet, rules | `cricket_dhamaka_print.pdf`, `rules_cricket.pdf` |
| Ganit Ladder (2-4) | 594 mm board, 60 table cards, tokens, die | `ganit_ladder_board.pdf`, `ganit_ladder_cards.pdf`, `rules_ganit.pdf` |
| India Yatra (2-6) | 72 cards in 3 language decks (24 each), rules | `india_yatra_cards_en.pdf`, `_hi.pdf`, `_te.pdf`, `rules_yatra.pdf` |
| Sabzi Mandi (2-4) | 24 item cards, 108 money cards, till tray, rules | `sabzi_mandi_items.pdf`, `sabzi_mandi_money.pdf`, `rules_mandi.pdf` |

Cards are 63 x 88 mm, 3 x 3 per A4 page at 200 dpi with crop marks. Regenerate any file with `python3 products/01-desi-games/src/render.py` (Pillow with RAQM shaping + Noto fonts; needed so Hindi and Telugu conjuncts render).

## 2. Materials and bought-in items (per set, about 1,000 sets, estimates)

| Item | Spec |
|---|---|
| Cards | 300 gsm art card, aqueous varnish, die-cut 63 x 88 mm, 3 mm corner radius |
| Board (Ganit Ladder) | 594 mm print on 350 gsm board, folded or two-piece, laminate |
| Boxes | tuck box 70 x 95 x 28 mm (card games); 300 x 300 x 45 mm (board game), 350 gsm box board |
| Dice (6-sided, 16 mm) and tokens | check small-parts warning; use low-migration paint |
| Rules | mono print, one booklet per language |
| Packaging | shrink-wrap, MRP label |

Costs per set from the product README: Cricket Rs 90, Ganit Rs 150, Yatra Rs 110, Sabzi Rs 180 (guesses to replace with quotes).

## 3. Before any printing (gates, in this order)
1. **Native-speaker review** of Hindi and Telugu rules and cards (the texts were machine-written and are unreviewed).
2. **Fact check** every quiz answer in India Yatra against two independent sources; remove any card you cannot confirm. Avoid logos, team or player names.
3. **Play-test** with 10 children aged 7-12, 3 sessions per game (plan in the product README): record rule confusions, session length, cards never chosen. Correct the rules and regenerate the PDFs.
4. **Name check:** run a trademark search for the four game names.
5. **Materials safety:** ask the printer for a heavy-metal/low-migration ink statement.

## 4. Making the prototype (20 sets) at a local print shop
1. Print the PDFs on 250-300 gsm card at 100 % scale (no "fit to page"). Check that a card measures 63 x 88 mm.
2. Cut with a guillotine along the crop marks, round corners with a 3 mm corner punch.
3. Laminate the board and optionally the cards (matte pouch, 125 micron).
4. Assemble: count cards into the box (the contents list is in the table above), add dice/tokens in a bag, rules booklet on top.
5. Quality check against the contents table (section 7).

## 5. Production run (after the gates)
Send three Hyderabad printers: the PDFs, the specifications in section 2, MOQ 500 and 1,000 sets, request: proof approval with Pantone tolerance, die-line drawing, price per set, lead time. **Keep ownership of the print files.** Approve a physical proof (not a PDF proof) of each game before the run.

## 6. Packaging, labelling, compliance
- Label 7+ (or 8+ for Cricket Dhamaka); small-parts warning for dice and tokens ("not for children under 3").
- Legal Metrology: MRP, contents ("108 money cards"), maker, month/year, consumer-care contact.
- Toys: confirm with BIS or a lab whether card/board games for under-14s fall under the Toys QCO and IS 9873 (inks and paper chemical requirements).
- Do not claim educational outcomes or curriculum alignment until verified.

## 7. Quality inspection (sample per batch)
- Contents complete against the table; no card missing, no duplicate card.
- Cards cut to 63 x 88 mm +-1 mm, corners rounded, no cut into the print.
- Colour: compare with the approved proof under daylight; Hindi/Telugu characters not clipped.
- Box closes, flaps hold, shrink-wrap clean.
- Record on `manuals/templates/eol_test_sheet.md` (use the contents table as the test lines).

## 8. Costs and prices
Plan prices Rs 499 / 799 / 599 / 799 with contribution margins of 45-50 %; if costs rise 30 % the margin falls to 36-43 % (see the product README table). Fixed launch cost Rs 1-2 lakh (assumption).

## 9. Known limits
Not play-tested with children; language and facts unreviewed; copycat risk; colour variation between print runs.
