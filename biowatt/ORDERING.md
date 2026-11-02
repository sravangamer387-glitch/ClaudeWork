# BioWatt MFC harvester: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: cold start needs 600 mV; marginal on one MFC. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/biowatt/1_fabrication/biowatt_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/biowatt/2_assembly/biowatt_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/biowatt/2_assembly/biowatt_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/biowatt_priced_BOM.csv`

Steps:

1. Create an account at **jlcpcb.com** and click *Order now*. Upload the Gerber ZIP. The viewer must show the board outline, both copper layers, silkscreen and drill holes.
2. Settings: **2 layers, 1.6 mm, FR-4**, lead-free HASL (use **ENIG** if the board has an LGA/QFN fine-pitch part, e.g. ADXL345, ESP32 module pad, BQ25570), green mask, white silk, quantity 5 (the minimum), *Remove order number: specify a location* if you want to avoid the order-number mark. Heavier copper (2 oz) only where the board notes say so.
3. Switch on **PCB Assembly**: *Economic*, assembly side *Top*, and set tooling holes *Added by JLCPCB* unless the board already has them. Choose the number of boards to assemble (2 or 5).
4. Upload the BOM and CPL. In the parts step, every line must match (LCSC numbers are in the BOM). Where a part is shown as *out of stock* or *no match*, use the alternative suggested by JLCPCB only after checking footprint and value against the list below; do not accept a different footprint.
5. In the **component placement preview**, check pin 1 / polarity of every IC, diode, LED, electrolytic capacitor, USB-C and connector against `*_assembly_top.pdf` in the same folder. Wrong rotation is the most common assembly error: ask JLCPCB support to rotate before approving.
6. Pay, then approve the assembly engineering review messages (they usually ask about a part or rotation). Delivery by DHL/FedEx/UPS takes about 1 to 2 weeks to India.

Parts **not** assembled by JLCPCB (you buy and solder them yourself):

| Refs | Value | Part | LCSC |
|---|---|---|---|
| J1 | MFC in (+ / -) | JST B2B-PH-K-S | C131337 |
| J2 | Storage cell (+ / -), protected | JST B2B-PH-K-S | C131337 |
| J3 | Tag out (VOUT, GND, VBAT_OK) | JST B3B-PH-K-S | C131339 |
| TP1, TP2, TP3, TP4 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$5.96 for 1 board**, **US$5.10 each for 10 boards**, **US$4.17 each for 100 boards** (about INR 524 / 449 / 367 at 88 INR/USD). The per-line break-up is in `costing/biowatt_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | BQ25570RGRR | BQ25570RGRR | C506250 | 4.4879 | 4.488 |
| J1 | 1 | MFC in (+ / -) | JST B2B-PH-K-S | C131337 | 0.0359 | 0.036 |
| J2 | 1 | Storage cell (+ / -), protected | JST B2B-PH-K-S | C131337 | 0.0359 | 0.036 |
| J3 | 1 | Tag out (VOUT, GND, VBAT_OK) | JST B3B-PH-K-S | C131339 | 0.0420 | 0.042 |
| L1 | 1 | 22u | Coilcraft LPS4018-223MRC | C5278935 | 1.1736 | 1.174 |
| L2 | 1 | 10u | ZE ZENR3015T100M | C42427989 | 0.0410 | 0.041 |
| C1,C3 | 2 | 4.7u | Samsung CL10A475KP8NNNC X5R 10V | C1705 | 0.0128 | 0.026 |
| C2 | 1 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.007 |
| C4,C5 | 2 | 22u/10V | Samsung CL21A226MPQNNNE | C29277 | 0.0377 | 0.075 |
| C6 | 1 | 10n | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | 0.0075 | 0.007 |
| R3,R1,R5,R11 | 4 | 5.6M | FOJAN FRC0603F5604TS | C2933237 | 0.0023 | 0.009 |
| R2,R6,R7,R8,R9,R12,R13 | 7 | 1M | UNI-ROYAL 0603WAF1004T5E | C22935 | 0.0018 | 0.013 |
| R4,R10 | 2 | 4.3M | FH RS-03L4304FT | C136595 | 0.0036 | 0.007 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 59 x 55 x 17 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- indoor, dry use; print in PETG or ABS, 3 perimeters, 25 % infill
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

### Bought-in
Protected single Li-ion/LiPo cell (3.7 V) with JST-PH 2 lead; MFC with JST-PH 2 lead; load tag on J3 (BLE/LoRa class: average current well under 1 mA).

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: all parts verified; the BQ25570 stock is limited (about 400) and the hold capacitor is a substitute grade.
- **Works-as-intended confidence: Low-Medium**: BQ25570 with megohm setting dividers computed from datasheet equations; cold start needs at least 600 mV (marginal for one microbial fuel cell); the hold capacitor is X7R where the datasheet asks for low leakage; leakage on a dirty board shifts the thresholds.
- **First thing to do:** Test with a bench supply at 0.8 V first, clean flux thoroughly, then try the fuel cell.
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
