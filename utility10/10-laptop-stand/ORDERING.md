# Laptop Stand (laser-cut): ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: stability limit stated. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. No custom circuit board: nothing to order from JLCPCB for this project.
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 3. Bought-in and mechanical items

## 2. Materials, tools and bought-in items
- Sheet: **6 mm** plywood (BWP) or bamboo for stiffness; MDF is acceptable only for prototypes; cutting area **600 x 600 mm**.
- Tools: caliper, try square, clamps, sandpaper (120/240), brush, PVA glue (D3), water-based polyurethane or paint, rubber/felt feet.
- Cost per unit (about 2,000 units, estimate; replace with quotes):
| Item | Rs |
|---|---|
| MDF/ply 6 mm | 90 |
| Laser cutting | 70 |
| Rubber feet ×4 | 15 |
| Hinge/tape | 30 |
| Packaging | 40 |
| Assembly | 25 |

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: no electronic parts to source: local laser-cutting or printing.
- **Works-as-intended confidence: Medium-High**: Laser-cut stand: fit depends on kerf; stability limit stated.
- **First thing to do:** Cut a kerf coupon and load-test.
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
