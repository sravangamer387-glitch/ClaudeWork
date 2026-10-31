# Handoff – what is finished on my side and what needs people or hardware

Everything below needs a human, a physical object or a lab. Nothing here can be done from a computer. Order = my suggested priority.

## A. Do first (cheap, quick)
1. **Games – proofreading.** Give `01-desi-games/review/yatra_proofreading.csv` and `mandi_items_proofreading.csv` to a Hindi and a Telugu speaker; verify every quiz fact against two sources (columns provided). I wrote the Hindi/Telugu myself and it is unreviewed. Then regenerate PDFs with `src/render.py` (edit `src/content.py`).
2. **Games – playtest.** Print the PDFs from `out/` (about Rs 1,300), use `review/playtest_sheet.md` with 10 children.
3. **Automata – cardboard mock-up** of each kit from `02-automata/out/*_parts_sheet.svg`; frame layouts are provisional, so expect to adjust shaft heights.
4. **Electronics prototypes** (Prayog Rs 1,790, Jal-Rakshak Rs 1,820 low-voltage only, Kheti-Mitra Rs 1,990, Gas demo Rs 1,270): buy parts, flash the `release/*.hex` (avrdude -p m328p -c arduino -P <port> -b 57600 -U flash:w:file.hex:i; old-bootloader Nanos may need 57600, new 115200), follow wiring in each `main_*.cpp` header comment. Enclosure STLs: `06-gas-suraksha/enclosure/`, `04-jal-rakshak/enclosure_*.stl`, `05-kheti-mitra/enclosure_*.stl` (simple prototype boxes: print and check fit, not production tooling).

## B. Needs measurement before any claim
- Soil sensor dry/wet counts (Kheti), probe/tank thresholds and run-time limit (Jal), LDR/Hall/NTC constants (Prayog), **gas sensor clean-air and test-gas counts (Gas)**. Constants in code are placeholders.
- Field trial for Kheti-Mitra (plan in its README). The 43% saving is simulated.

## C. Needs money, a lab or a lawyer
- Jal-Rakshak mains version: electrical-safety engineer + BIS/CRS applicability from a lab. Gas-Suraksha: gas-detector performance lab, product-liability opinion. Games/automata/Prayog: confirm toys-QCO (IS 9873) applicability.
- PCB layout (none done for any product), production tooling, EMS and printer/laser RFQs (templates in each README; vendor leads in `electronics-toys/phase1-market-and-rules.md`).
- School procurement route for Prayog (ask 5 schools and a dealer).

## D. Decisions I did not make for you
Gas product: continue or stop; Jal low-voltage-only variant; pricing (see each README's recommended price, margins quoted at +30% BOM); brand names and trademark search; GST rates and marketplace fees are assumptions to confirm with your accountant.

## E. Earlier open items (from previous phases)
Drop Quest puzzle solver (decide rules after kids try it), physical gravity-toy builds, electronic-toy PCBs, DJ-system prototype purchases (see `dj-setup/`).

## F. If you want me to continue later
Useful follow-ups I can do on request: automata assembly manuals and exploded drawings, teacher guide/worksheet PDFs for Prayog, PCB schematics (KiCad netlists) for products 3–5, listing images, update content after the proofreaders return their sheets.
