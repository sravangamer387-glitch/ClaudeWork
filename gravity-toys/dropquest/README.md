# Drop Quest v1 (laser-cut): rules, 60 verified levels, parts

**Status: v1 rules fixed, 60 challenge cards generated and each verified by exhaustive search to have exactly one solution; laser parts generated; nothing built or play-tested.**

- Rules, simulator, solver, generator: `dropquest.py` (`python3 dropquest.py` regenerates `levels.json` and `CARDS.md` and exits non-zero if any level is not unique).
- Rules in short: 5 x 5 board; towers 1-3 units (1 unit = 18 mm = three 6 mm MDF squares); the marble (14 mm) starts at height 3 from the start row rolling right, rolls straight, drops onto lower or equal cells, is stopped by higher cells, and is reflected by 45-degree deflector caps (`/` or `\`, rotate the cap to swap). Win: leave the right edge at floor height on the target row. Place all loose pieces; the marble must touch each.
- Cards: `CARDS.md` (15 each green, blue, red, black; solution on the card back).
- Parts: `gen_parts.py` -> `dropquest_sheet_6mm.svg/.dxf` (board 230 x 230 and 120 tower layers: 8 x h1, 7 x h2, 6 x h3, enough for every card) and `dropquest_sheet_3mm.svg/.dxf` (6 acrylic deflector caps with 45-degree slots and walls, start ramp, target cup).
- Assembly: glue tower layers in stacks (use a square jig), sand edges R1; glue each wall strip into its cap slot; engrave grid coordinates on the board.
- Test before production: 10 children, cards 1-20; marble must never jump a cell when dropping 3 units (if it does, add a 2 mm lip to the tower tops); check 14 mm marble small-part labelling (8+).
