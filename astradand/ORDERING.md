# ASTRADAND gesture wand (sci-fi project): ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: software-verified; never built; Hindi names unreviewed. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/astradand/1_fabrication/astradand_main_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/astradand/2_assembly/astradand_main_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/astradand/2_assembly/astradand_main_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/astradand_priced_BOM.csv`

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
| J4 | Haptic motor | JST B2B-PH-K-S(LF)(SN) | C131337 |
| TP1, TP2 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$27.69 for 1 board**, **US$24.66 each for 10 boards**, **US$21.36 each for 100 boards** (about INR 2437 / 2170 / 1880 at 88 INR/USD). The per-line break-up is in `costing/astradand_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| C1,C2,C3,C20,C21,C22,C23,C24,C25,C10,C12,C13 | 12 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.090 |
| R7 | 1 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.002 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| J1 | 1 | BATT 3xAAA | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| SW1 | 1 | Power | C&K PCM12SMTR | C221841 | 1.2754 | 1.275 |
| Q2,Q3 | 2 | AO3401A | AO3401A | C15127 | 0.0969 | 0.194 |
| C4,C7 | 2 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.088 |
| D11,D12,D13,D14,D15,D16 | 6 | WS2812B-Mini | OPSCO SK6812MINI-B-012 SMD3535-4P, same pin order and 800 kHz protocol as the WS2812B-Mini (Worldsemi parts were sold out) | C5183448 | 0.0953 | 0.572 |
| U2 | 1 | MPU-6050 | MPU-6050 | C24112 | 21.6984 | 21.698 |
| C11 | 1 | 2.2n | Samsung CL10B222KB8NNNC X7R | C16033 | 0.0100 | 0.010 |
| R20,R21 | 2 | 4.7k | 0603 4.7k 1% | C23162 | 0.0028 | 0.006 |
| U3 | 1 | AP2112K-3.3 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | 0.1814 | 0.181 |
| C5,C6 | 2 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.029 |
| D20 | 1 | SS14 | Starsea SS14 SMA | C84343 | 0.0252 | 0.025 |
| Q4,Q1 | 2 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.024 |
| R33,R32 | 2 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.006 |
| R34,R6 | 2 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.003 |
| R30 | 1 | 330 | UNI-ROYAL 0603WAF3300T5E | C23138 | 0.0021 | 0.002 |
| R31 | 1 | 330k | UNI-ROYAL 0603WAF3303T5E | C23137 | 0.0016 | 0.002 |
| BZ1 | 1 | PKLCS1212E4001 | PKLCS1212E4001-R1 | C113159 | 0.8028 | 0.803 |
| SW2 | 1 | Cast trigger | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| J4 | 1 | Haptic motor | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| TP1,TP2 | 2 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 151 x 31 x 20 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

### Bought-in and mechanical (estimates for 2,000 units)
3 x AAA in-line holder with leads (JST-PH 2-pin), coin vibration motor with JST-PH 2-pin lead (3 V, 8-10 mm, under 80 mA), M2.5 x 8 mm self-tapping screws x 12, rubber grommet for the battery lead, translucent natural PETG or clear resin for the crystal, PETG (opaque, any dark colour) for the shell, 350 gsm board for the carton, 6 mm MDF for the stand, 300 gsm card for the spell cards.

## 4. Confidence (read before you order)

- **Order confidence: Medium**: substitute addressable LED whose pad geometry is unproven; other parts verified.
- **Works-as-intended confidence: Medium**: IMU gesture recognition validated against a Python reference (46/46) and on synthetic gestures; hardware (haptics, six addressable LEDs) is new; the LED part was replaced with a pin-compatible one whose pads are unproven.
- **First thing to do:** Order 2 boards, check the LED footprint fit, then run the gesture self-test.
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
