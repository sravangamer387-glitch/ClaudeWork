# 1 Desi Games Studio (print): ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: language + fact review before print. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. No custom circuit board: nothing to order from JLCPCB for this project.
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 3. Bought-in and mechanical items

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

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: no electronic parts to source: local laser-cutting or printing.
- **Works-as-intended confidence: Medium**: Printed game; needs language and fact review before print.
- **First thing to do:** Proofread with native speakers.
- Rubric and the reasons for every project: `costing/CONFIDENCE.md`. These are judgements, not measurements: nothing here has been built.

## 5. Where to buy and whom to approach

| Item type | India (fast, GST invoice) | Overseas (cheaper, 1 to 3 weeks, customs) |
|---|---|---|
| Printed circuit board and SMD assembly | JLCPCB is the practical choice for 5 to 100 boards; local PCB shops quote per project (ask for the Gerber ZIP price) | **JLCPCB** (jlcpcb.com), PCBWay (pcbway.com) |
| Connectors, headers, passives, ICs by LCSC number | element14 India, Mouser India, DigiKey India (genuine, GST invoice, higher price); local electronics markets for common parts | **LCSC** (lcsc.com) with the same cart as JLCPCB |
| Modules: ESP32 dev boards, SIM7080G, LoRa (RA-08 / RAK3172), pH / EC / DO modules, relay modules, load cells, ultrasonic sensors | Robu.in, Robocraze, ThinkRobotics, Sunrom Electronics, Amazon.in | AliExpress, Seeed Studio, Waveshare |
| Motors, stepper drivers, wheels | Robu.in, Robocraze, local robotics shops | StepperOnline (omc-stepperonline.com) |
| Li-ion / LiFePO4 cells and packs, solar panels, MPPT controllers | Authorised battery and solar dealers, Amazon.in (buy protected cells with an invoice) | not recommended by post (shipping rules for batteries) |
| Laser-cut and 3D-printed parts | Local laser-cutting and 3D-printing shops (search IndiaMART, Justdial or maker spaces): send the SVG/DXF/STL from the repository and ask for a quote per piece | JLC3DP (jlc3dp.com), PCBWay 3D printing |
| Fasteners, tubing, hardware, enclosures | Local hardware, Robu.in, Amazon.in | n/a |

How to approach a vendor: send the project name, the exact file (BOM, CPL, Gerber ZIP, STL or SVG), the quantity, and ask for the price, the lead time, the GST invoice and the warranty or return terms. Keep the reply for your records.
