# KINETIC motion controller + vibration puck: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: never run on a motor; AI on synthetic data. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/kinetic_ctl/1_fabrication/kinetic_ctl_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/kinetic_ctl/2_assembly/kinetic_ctl_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/kinetic_ctl/2_assembly/kinetic_ctl_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/kinetic_ctl_priced_BOM.csv`

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
| J5 | 24 V in | KF128-5.08-2P-AA | C474952 |
| J7 | Host UART (Pi/PC) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J3 | Vibration sensor SPI | HCTL PZ254-2-03-Z-8.5 | C2894964 |
| J8 | Endstop X | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J9 | Endstop Y | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J10 | Endstop Z | JST B3B-PH-K-S(LF)(SN) | C131339 |
| TP1, TP2, TP3, TP4 | TP |  |  |
| J11 | X driver logic | hanxia HX PM2.54-1x8P | C22438158 |
| J12 | X driver power/motor | hanxia HX PM2.54-1x8P | C22438158 |
| J20 | Motor X | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J13 | Y driver logic | hanxia HX PM2.54-1x8P | C22438158 |
| J14 | Y driver power/motor | hanxia HX PM2.54-1x8P | C22438158 |
| J21 | Motor Y | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J15 | Z driver logic | hanxia HX PM2.54-1x8P | C22438158 |
| J16 | Z driver power/motor | hanxia HX PM2.54-1x8P | C22438158 |
| J22 | Motor Z | JST B4B-PH-K-S(LF)(SN) | C131334 |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$8.49 for 1 board**, **US$7.72 each for 10 boards**, **US$6.21 each for 100 boards** (about INR 747 / 679 / 546 at 88 INR/USD). The per-line break-up is in `costing/kinetic_ctl_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| J5 | 1 | 24 V in | KF128-5.08-2P-AA | C474952 | 0.1948 | 0.195 |
| D3 | 1 | SMBJ28A | Littelfuse SMBJ28A | C178227 | 0.1091 | 0.109 |
| Q5 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| D4 | 1 | BZT52C12 | DIODES BZT52C12-7-F | C124196 | 0.0775 | 0.077 |
| R40,R42,R47,R51,R52,R53 | 6 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.014 |
| C30 | 1 | 100u/35V | Lelon VZH101M1VTR-0607 | C176683 | 0.0881 | 0.088 |
| C31 | 1 | 10u/50V | Samsung CL32A106KBJNNNE | C380537 | 0.2086 | 0.209 |
| U2 | 1 | AP63205WU-7 | AP63205WU-7 | C2071056 | 0.4665 | 0.467 |
| R41,R46 | 2 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.006 |
| C32,C37,C40,C41,C42,C43 | 6 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.045 |
| L1 | 1 | 4.7u | Changjiang FNR5040S4R7MT | C167963 | 0.0933 | 0.093 |
| C33,C34 | 2 | 22u/10V | Samsung CL21A226MPQNNNE | C29277 | 0.0377 | 0.075 |
| D5 | 1 | SS14 | SS14 | C84343 | 0.0252 | 0.025 |
| U3 | 1 | AP2112K-3.3 | AP2112K-3.3TRG1 | C51118 | 0.1814 | 0.181 |
| C35,C39 | 2 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.029 |
| C36,C38 | 2 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.088 |
| U1 | 1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1-N8 | C2913198 | 4.9100 | 4.910 |
| SW2 | 1 | Reset (EN) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW3 | 1 | Boot (IO0) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| J1 | 1 | USB-C | TYPE-C-31-M-12 | C165948 | 0.1890 | 0.189 |
| R43,R44 | 2 | 5.1k | 0603 5.1k 1% | C23186 | 0.0016 | 0.003 |
| D6 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| R45,R48,R49,R50 | 4 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.007 |
| J7 | 1 | Host UART (Pi/PC) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J3 | 1 | Vibration sensor SPI | HCTL PZ254-2-03-Z-8.5 | C2894964 | 0.0766 | 0.077 |
| J8 | 1 | Endstop X | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J9 | 1 | Endstop Y | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J10 | 1 | Endstop Z | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |
| J11 | 1 | X driver logic | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J12 | 1 | X driver power/motor | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J20 | 1 | Motor X | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J13 | 1 | Y driver logic | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J14 | 1 | Y driver power/motor | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J21 | 1 | Motor Y | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J15 | 1 | Z driver logic | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J16 | 1 | Z driver power/motor | hanxia HX PM2.54-1x8P | C22438158 | 0.1359 | 0.136 |
| J22 | 1 | Motor Z | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 127 x 95 x 39 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- driver modules with heatsinks are about 26 mm tall above the board; vents on both long walls; add a 40 mm fan on the lid if a driver runs above 1 A
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

### Bought-in
StepStick driver modules (1-3), NEMA17 motors, 12-28 V supply (24 V recommended) with current limit capability for bring-up, 1x8 female socket strips are on the BOM, endstop switches, 6-wire cable for the puck (under 30 cm), M2.5 screws.

## 4. Confidence (read before you order)

- **Order confidence: High**: all parts live-checked, none flagged.
- **Works-as-intended confidence: Medium**: ESP32-S3 controller with three StepStick sockets and a 24 V to 5 V buck. Motion library (370 checks) and protocol are host-tested; the ESP32 firmware has never been compiled; drivers and motors are bought in. The vibration model is trained on synthetic data only.
- **First thing to do:** Power with a current-limited supply and no drivers; then one driver and one motor at low current.
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
