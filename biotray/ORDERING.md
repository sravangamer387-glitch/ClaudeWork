# BioTray vertical-farm controller: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: calibration values are placeholders. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/biotray/1_fabrication/biotray_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/biotray/2_assembly/biotray_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/biotray/2_assembly/biotray_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/biotray_priced_BOM.csv`

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
| J2 | 12 V DC in | CUI/Same Sky PJ-063AH | C22434582 |
| J7 | Water temp DS18B20 | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J8 | I2C (BH1750 / SHT31) | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J9 | Water-level float switch | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J10 | pH module (0-3 V analog) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J11 | EC module (0-3 V analog) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J12 | UART flash/debug (USB-serial adapter) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| TP1, TP2, TP3, TP4 | TP |  |  |
| J3 | Pump 1 | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J4 | Pump 2 | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J5 | Grow light (PWM) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J6 | Fan | JST B2B-PH-K-S(LF)(SN) | C131337 |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$10.82 for 1 board**, **US$9.64 each for 10 boards**, **US$7.69 each for 100 boards** (about INR 952 / 848 / 677 at 88 INR/USD). The per-line break-up is in `costing/biotray_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| J2 | 1 | 12 V DC in | CUI/Same Sky PJ-063AH | C22434582 | 2.7602 | 2.760 |
| F1 | 1 | PTC 1A 16V | Littelfuse 1812L110/16DR | C142746 | 0.1050 | 0.105 |
| D3 | 1 | SMBJ15A | Littelfuse SMBJ15A | C83846 | 0.1300 | 0.130 |
| Q5 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| D4 | 1 | BZT52C12 | DIODES BZT52C12-7-F | C124196 | 0.0775 | 0.077 |
| R40,R42,R49 | 3 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.007 |
| C30 | 1 | 100u/35V | Lelon VZH101M1VTR-0607 | C176683 | 0.0881 | 0.088 |
| C31 | 1 | 10u/50V | Samsung CL32A106KBJNNNE | C380537 | 0.2086 | 0.209 |
| U2 | 1 | AP63205WU-7 | AP63205WU-7 | C2071056 | 0.4665 | 0.467 |
| R41,R14,R15,R16,R17 | 5 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.015 |
| C32,C37,C40,C41 | 4 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.030 |
| L1 | 1 | 4.7u | Changjiang FNR5040S4R7MT | C167963 | 0.0933 | 0.093 |
| C33,C34 | 2 | 22u/10V | Samsung CL21A226MPQNNNE | C29277 | 0.0377 | 0.075 |
| D5,D10,D11,D13 | 4 | SS14 | SS14 | C84343 | 0.0252 | 0.101 |
| U3 | 1 | AP2112K-3.3 | AP2112K-3.3TRG1 | C51118 | 0.1814 | 0.181 |
| C35,C39 | 2 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.029 |
| C36,C38 | 2 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.088 |
| U1 | 1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1-N8 | C2913198 | 4.9100 | 4.910 |
| SW2 | 1 | Reset (EN) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW3 | 1 | Boot (IO0) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| J1 | 1 | USB-C | TYPE-C-31-M-12 | C165948 | 0.1890 | 0.189 |
| R43,R44 | 2 | 5.1k | 0603 5.1k 1% | C23186 | 0.0016 | 0.003 |
| D6 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| R45,R50,R51 | 3 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.005 |
| J7 | 1 | Water temp DS18B20 | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| R46,R47,R48 | 3 | 4.7k | 0603 4.7k 1% | C23162 | 0.0028 | 0.008 |
| J8 | 1 | I2C (BH1750 / SHT31) | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J9 | 1 | Water-level float switch | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J10 | 1 | pH module (0-3 V analog) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J11 | 1 | EC module (0-3 V analog) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J12 | 1 | UART flash/debug (USB-serial adapter) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |
| Q1,Q2,Q3,Q4 | 4 | AO3400A | AO3400A | C20917 | 0.0899 | 0.360 |
| R10,R11,R12,R13 | 4 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.010 |
| J3 | 1 | Pump 1 | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J4 | 1 | Pump 2 | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J5 | 1 | Grow light (PWM) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J6 | 1 | Fan | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/*_enclosure_plate.stl` (116 x 96 x 3 mm, PETG or ABS). Buy an **IP65 ABS junction box** with at least 120 x 100 x 31 mm inside, cable glands and a breather/vent membrane; fix the plate with 4 x M4 screws.
- Board to plate: 4 x M2.5 x 6 mm self-tapping screws. wet environment: mount on this plate inside an IP65 ABS junction box with cable glands; keep the box above the water line; use a GFCI-protected 12 V adapter

## 3. Bought-in and mechanical items

### Bought-in
12 V 3 A adapter (barrel 5.5/2.1, centre positive), 12 V peristaltic or submersible pumps, 12 V fan, 12 V LED grow strip (total under 1.1 A or replace the PTC), DS18B20 probe, BH1750 module, float switch, pH module and probe, EC module and probe, tubing, tray.

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: J2 12 V DC in (stock 321).
- **Works-as-intended confidence: Medium**: 12 V low-side drivers, ESP32 and sensors; 22 host checks; calibration constants are placeholders; wet environment.
- **First thing to do:** Dummy loads on all outputs first; seal the enclosure before any water.
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
