# Seeti Counter: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: firmware compiled, not run on hardware. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/seeti/1_fabrication/seeti_counter_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/seeti/2_assembly/seeti_counter_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/seeti/2_assembly/seeti_counter_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/seeti_priced_BOM.csv`

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
| J1 | BATT 2xAAA | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J2 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 |
| J3 | MIC electret | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J4 | UART | ZHOURI 2.54-1*4 | C5116483 |
| BZ1 | Buzzer 3V | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 |
| TP1, TP2, TP3, TP4 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$4.75 for 1 board**, **US$4.22 each for 10 boards**, **US$3.56 each for 100 boards** (about INR 418 / 371 / 313 at 88 INR/USD). The per-line break-up is in `costing/seeti_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| U2 | 1 | MCP6001 | MCP6001T-I/OT | C116490 | 0.3212 | 0.321 |
| J1 | 1 | BATT 2xAAA | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| SW1 | 1 | Power | C&K PCM12SMTR | C221841 | 1.2754 | 1.275 |
| Q2 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| J3 | 1 | MIC electret | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J4 | 1 | UART | ZHOURI 2.54-1*4 | C5116483 | 0.0223 | 0.022 |
| BZ1 | 1 | Buzzer 3V | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | 0.1513 | 0.151 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| SW2 | 1 | Target | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| D1 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| R1 | 1 | 2.2k | 0603 2.2k 1% | C4190 | 0.0018 | 0.002 |
| R2,R3,R4 | 3 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.009 |
| R5,R6,R9,R10 | 4 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.007 |
| R7 | 1 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.002 |
| R8 | 1 | 33k | UNI-ROYAL 0603WAF3302T5E | C4216 | 0.0021 | 0.002 |
| C1,C2,C3,C8 | 4 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.030 |
| C4,C7 | 2 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.088 |
| C5 | 1 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.014 |
| C6 | 1 | 220n | Samsung CL10B224KB8NNNC X7R 50V | C64705 | 0.0171 | 0.017 |
| C9 | 1 | 22n | Samsung CL10B223KB8NNNC X7R | C21122 | 0.0058 | 0.006 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 79 x 59 x 36 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Battery: **Keystone 2469 (2 x AAA, wire leads)** in the floor bay (55.0 x 26.6 x 13.8 mm); print `*_enclosure_battery_door.stl`; the door closes with 2 x M2.5 x 6 mm self-tapping (tool needed to open). Route the holder lead through the hole in the bay ceiling to the battery connector.
- Print `*_enclosure_caps.stl` (light pipe, plunger, slider): plunger for SW2; light pipe for D1; slider for SW1. Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid.
- indoor, dry use; print in PETG or ABS, 3 perimeters, 25 % infill
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)
| Item | Rs |
|---|---|
| MCU + crystal | 45 |
| Electret mic amp module | 40 |
| Buzzer | 12 |
| PCB | 30 |
| 2×AAA holder + switch | 18 |
| Heat-resistant clip/magnet mount | 40 |
| Enclosure | 50 |
| Packaging + Hindi/Telugu manual | 30 |
| Assembly + test | 40 |

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: BZ1 Buzzer 3V (stock 140).
- **Works-as-intended confidence: Medium**: Mic front end and clap/whistle detector are analog and tuned on synthetic audio; the firmware itself passes 115 host checks; the documented limit is that quiet whistles are missed.
- **First thing to do:** Bench-test the microphone gain with real claps before ordering more than 5 boards.
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
