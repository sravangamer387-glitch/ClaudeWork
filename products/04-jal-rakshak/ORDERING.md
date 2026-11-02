# 4 Jal-Rakshak tank controller: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: **mains version cannot be made**: low-voltage prototype only. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/jalrakshak/1_fabrication/jal_rakshak_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/jalrakshak/2_assembly/jal_rakshak_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/jalrakshak/2_assembly/jal_rakshak_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/jalrakshak_priced_BOM.csv`

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
| J2 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 |
| BZ1 | Buzzer active 3V | S&S SUN-1275Y-0327-50P7.6 | C3015483 |
| J1 | 12 V DC in | CUI/Same Sky PJ-063AH | C22434582 |
| J5 | Pump 12V DC, max 1 A (LOW VOLTAGE ONLY) | Cixi Kefa KF128-5.08-2P-AA | C474952 |
| J6 | Probes: COM, SUMP, TANK LOW, TANK FULL | JST B4B-PH-K-S(LF)(SN) | C131334 |
| TP1, TP2, TP3, TP4 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$6.73 for 1 board**, **US$6.01 each for 10 boards**, **US$4.94 each for 100 boards** (about INR 592 / 529 / 435 at 88 INR/USD). The per-line break-up is in `costing/jalrakshak_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| C1,C2,C3,C8 | 4 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.030 |
| R7,R21,R23,R25 | 4 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.010 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| BZ1 | 1 | Buzzer active 3V | S&S SUN-1275Y-0327-50P7.6 | C3015483 | 0.2368 | 0.237 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| R6,R5,R20 | 3 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.005 |
| D1 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| J1 | 1 | 12 V DC in | CUI/Same Sky PJ-063AH | C22434582 | 2.7602 | 2.760 |
| F1 | 1 | PTC 1A 16V | Littelfuse 1812L110/16DR (1.1 A hold, 16 V) | C142746 | 0.1050 | 0.105 |
| D3 | 1 | SMBJ15A | Littelfuse SMBJ15A | C83846 | 0.1300 | 0.130 |
| Q3 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| R17,R18,R22,R24,R26 | 5 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.015 |
| U3 | 1 | AMS1117-5.0 | AMS AMS1117-5.0 SOT-223 | C6187 | 0.2602 | 0.260 |
| C6,C7 | 2 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.088 |
| Q4 | 1 | AO3400A | AOS AO3400A | C20917 | 0.0899 | 0.090 |
| R16 | 1 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.002 |
| D7 | 1 | SS14 | Starsea SS14 SMA | C84343 | 0.0252 | 0.025 |
| J5 | 1 | Pump 12V DC, max 1 A (LOW VOLTAGE ONLY) | Cixi Kefa KF128-5.08-2P-AA | C474952 | 0.1948 | 0.195 |
| R30 | 1 | 68 | UNI-ROYAL 0603WAF680JT5E | C27592 | 0.0013 | 0.001 |
| J6 | 1 | Probes: COM, SUMP, TANK LOW, TANK FULL | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| SW2 | 1 | Reset fault | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 101 x 75 x 23 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Print `*_enclosure_caps.stl` (light pipe, plunger): plunger for SW2; light pipe for D1. Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid.
- indoor, dry use near the pump controller; probe and pump cables through the side openings; low voltage only
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

See the parts and materials section of the manual.

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: J1 12 V DC in (stock 321).
- **Works-as-intended confidence: Medium**: Low-voltage board reuses the Kheti-Mitra 12 V front end and pump driver; the firmware rules pass 20 simulated checks and an 8 MHz PCB build exists (3.2 kB); real probes, water, pump currents untested; the mains version is still out of scope.
- **First thing to do:** Bench test with a 12 V pump and probes in a bucket; never connect mains.
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
