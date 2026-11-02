# 02 Taal Memory: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: shares the Desi Arcade board. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/arcade/1_fabrication/desi_arcade_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/arcade/2_assembly/desi_arcade_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/arcade/2_assembly/desi_arcade_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/arcade_priced_BOM.csv`

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
| J1 | BATT 3xAAA | JST B2B-PH-K-S(LF)(SN) | C131337 |
| BZ1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 |
| J5 | Arcade button 1 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J6 | Arcade button 2 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J7 | Arcade button 3 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J8 | Arcade button 4 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| TP1, TP2, TP3 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$4.24 for 1 board**, **US$3.72 each for 10 boards**, **US$3.15 each for 100 boards** (about INR 373 / 327 / 277 at 88 INR/USD). The per-line break-up is in `costing/arcade_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| C1,C2,C3 | 3 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.022 |
| R7 | 1 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.002 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| J1 | 1 | BATT 3xAAA | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| SW1 | 1 | Power | C&K PCM12SMTR | C221841 | 1.2754 | 1.275 |
| Q2 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| C4 | 1 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.044 |
| BZ1 | 1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | 0.1513 | 0.151 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| R6 | 1 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.002 |
| J5 | 1 | Arcade button 1 | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J6 | 1 | Arcade button 2 | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J7 | 1 | Arcade button 3 | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J8 | 1 | Arcade button 4 | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| R10,R11,R12,R13 | 4 | 330 | UNI-ROYAL 0603WAF3300T5E | C23138 | 0.0021 | 0.008 |
| R14,R15 | 2 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.006 |
| TP1,TP2,TP3 | 3 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 157 x 125 x 60 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Battery: **Keystone 2480 (3 x AAA, wire leads)** in the floor bay (54.7 x 39.5 x 13.8 mm); print `*_enclosure_battery_door.stl`; the door closes with 2 x M2.5 x 6 mm self-tapping (tool needed to open). Route the holder lead through the hole in the bay ceiling to the battery connector.
- Print `*_enclosure_caps.stl` (slider): slider for SW1. Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid.
- arcade console: four 30 mm arcade buttons in the lid (28.5 mm holes: check your button and open up if needed), 3 x AAA bay under the floor with a screwed door; print in PETG or ABS
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

### 3b. Bought-in and mechanical (estimates, ~2,000 units)
| Item | Rs |
|---|---|
| MCU + crystal | 55 |
| PCB | 30 |
| 4 coloured pads (dome buttons) | 60 |
| 4 LEDs + resistors | 10 |
| Piezo buzzer | 12 |
| Battery holder + switch | 18 |
| Enclosure | 55 |
| Packaging + manual | 30 |
| Assembly + test | 40 |
- 4 arcade push buttons, 30 mm, with 5 V LED lamp (3-wire leads to the JST-PH 3-pin sockets J5-J8: button, lamp, GND), housing (ABS, or 3D-printed/laser-cut MDF for the first 500), 3 x AAA holder, button caps/labels.

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: BZ1 Buzzer (stock 140).
- **Works-as-intended confidence: Medium-High**: Same board and test base as Reflex Raja.
- **First thing to do:** Play-test the buttons and the buzzer.
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
