# 6 Gas-Suraksha leak alarm: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: **not certified, not for sale**. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/gassuraksha/1_fabrication/gas_suraksha_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/gassuraksha/2_assembly/gas_suraksha_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/gassuraksha/2_assembly/gas_suraksha_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/gassuraksha_priced_BOM.csv`

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
| J5 | BATT 3xAA | JST B2B-PH-K-S(LF)(SN) | C131337 |
| BZ1 | Buzzer active 3V | S&S SUN-1275Y-0327-50P7.6 | C3015483 |
| J2 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 |
| J3 | MQ-6 module: VCC GND DO AO | ZHOURI 2.54-1*4 | C5116483 |
| J4 | UART log (adapter RX, TX) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| TP1, TP2, TP3 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$5.28 for 1 board**, **US$4.76 each for 10 boards**, **US$3.98 each for 100 boards** (about INR 465 / 419 / 350 at 88 INR/USD). The per-line break-up is in `costing/gassuraksha_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| J1 | 1 | USB-C 5V | TYPE-C-31-M-12 | C165948 | 0.1890 | 0.189 |
| F1 | 1 | PTC 500mA | Littelfuse 1206L050YR (6 V) | C163512 | 0.0742 | 0.074 |
| D3 | 1 | SMAJ5.0A | Littelfuse SMAJ5.0A | C83329 | 0.1153 | 0.115 |
| R1,R2 | 2 | 5.1k | 0603 5.1k 1% | C23186 | 0.0016 | 0.003 |
| C5,C4,C20 | 3 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.132 |
| J5 | 1 | BATT 3xAA | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| SW1 | 1 | Power | C&K PCM12SMTR | C221841 | 1.2754 | 1.275 |
| Q2 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| BZ1 | 1 | Buzzer active 3V | S&S SUN-1275Y-0327-50P7.6 | C3015483 | 0.2368 | 0.237 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| R6,R10,R5,R8,R9 | 5 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.008 |
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| C1,C2,C3,C11,C12 | 5 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.037 |
| R7 | 1 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.002 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| R20 | 1 | 47 | UNI-ROYAL 0603WAF470JT5E | C23182 | 0.0020 | 0.002 |
| D6,D7 | 2 | SS14 | SS14 | C84343 | 0.0252 | 0.050 |
| Y1 | 1 | 16 MHz | YXC X322516MOB4SI 16 MHz 12 pF 3225 (LCSC listing seen in search results; matches the 22 pF load caps) | C12668 | 0.0982 | 0.098 |
| C9,C10 | 2 | 22p | Samsung CL10C220JB8NNNC C0G | C1653 | 0.0090 | 0.018 |
| J3 | 1 | MQ-6 module: VCC GND DO AO | ZHOURI 2.54-1*4 | C5116483 | 0.0223 | 0.022 |
| R11,R12 | 2 | 220k | UNI-ROYAL 0603WAF2203T5E | C22961 | 0.0015 | 0.003 |
| J4 | 1 | UART log (adapter RX, TX) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| SW2 | 1 | Silence | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW3 | 1 | Test | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| TP1,TP2,TP3 | 3 | TP |  |  |  |  |
| D1 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| D4 | 1 | Amber | Hubei KENTO KT-0603Y yellow (Everlight 19-213 was out of stock) | C2287 | 0.0105 | 0.011 |
| D5 | 1 | Red | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | 0.0077 | 0.008 |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 99 x 75 x 40 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Battery: **Keystone 2465 (3 x AA, wire leads)** in the floor bay (60.0 x 50.3 x 17.8 mm); print `*_enclosure_battery_door.stl`; the door closes with 2 x M2.5 x 6 mm self-tapping (tool needed to open). Route the holder lead through the hole in the bay ceiling to the battery connector.
- Print `*_enclosure_caps.stl` (light pipe, plunger): plunger for SW2; light pipe for D1; light pipe for D4; light pipe for D5. Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid.
- indoor, dry use; print in PETG or ABS, 3 perimeters, 25 % infill
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

## 2. Parts (about Rs 1,270)
Arduino Nano clone, MQ-6 module (analog out AO), active buzzer, 3 LEDs (green, amber, red) with resistors, 2 buttons, breadboard/jumpers, 3 x AA holder + USB power, 3D-printed puck (or cardboard), a lighter-gas test bag.
Wiring (from `firmware/src/main_gas.cpp`): MQ-6 AO to **A0**; buzzer **D8**; green LED **D9**, amber **D10**, red **D11**; silence button **D2** and test button **D3** (to GND).

## 4. Confidence (read before you order)

- **Order confidence: High**: all parts live-checked, none flagged.
- **Works-as-intended confidence: Low-Medium**: Prototype/logging board carries the tested alarm engine (34 checks) with an active buzzer and a UART log header; MQ-6 thresholds are placeholders and it is not a certified detector.
- **First thing to do:** Log real sensor data for a week; never use or sell as a safety device.
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
