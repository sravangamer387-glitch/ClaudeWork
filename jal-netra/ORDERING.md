# Jal-Netra (engineering marvel): ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: **Gate 1 acoustic test first; not sellable**. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/jalnetra/1_fabrication/jal_netra_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/jalnetra/2_assembly/jal_netra_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/jalnetra/2_assembly/jal_netra_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/jalnetra_priced_BOM.csv`

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
| J6 | Transducer A (BTL) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J7 | Transducer B (BTL) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J4 | OLED I2C | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J5 | UART host / BLE | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J3 | SWD | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 |
| TP1, TP2, TP3, TP4, TP5, TP6 | TP |  |  |
| BZ1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$10.10 for 1 board**, **US$9.01 each for 10 boards**, **US$7.66 each for 100 boards** (about INR 889 / 793 / 674 at 88 INR/USD). The per-line break-up is in `costing/jalnetra_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | STM32G431CBT6 | STM32G431CBT6 (LQFP-48) | C529355 | 4.8168 | 4.817 |
| U4,U7 | 2 | TS5A3159 | TI TS5A3159DCKR | C46388 | 0.3784 | 0.757 |
| U5,U6 | 2 | OPA356 | TI OPA356AIDBVR | C183100 | 1.3886 | 2.777 |
| U3 | 1 | AP2112K-3.3 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | 0.1814 | 0.181 |
| FB1 | 1 | BLM18 600R | Murata BLM18AG601SN1D | C19330 | 0.0122 | 0.012 |
| Y1 | 1 | 8 MHz | YXC X32258MOB4SI 8 MHz 12 pF 3225 (matches the 15 pF load caps) | C2682775 | 0.1994 | 0.199 |
| D5,D6 | 2 | BAV99 | JSCJ BAV99 | C68983 | 0.0168 | 0.034 |
| J6 | 1 | Transducer A (BTL) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J7 | 1 | Transducer B (BTL) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| R30,R31,R32,R33 | 4 | 22 | UNI-ROYAL 0603WAF220JT5E | C23345 | 0.0017 | 0.007 |
| C20,C21,C28,C30 | 4 | 10n | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | 0.0075 | 0.030 |
| R35,R36,R17,R7,R5 | 5 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.008 |
| C22,C23,C24,C1,C2,C3,C4,C33,C37 | 9 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.068 |
| C25,C27,C29,C31,C38,C39 | 6 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.086 |
| R10,R11,R21,R22 | 4 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.010 |
| R12,R16 | 2 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.006 |
| R13 | 1 | 2.2k | 0603 2.2k 1% | C4190 | 0.0018 | 0.002 |
| R14 | 1 | 240 | UNI-ROYAL 0603WAF2400T5E (JLCPCB listing) | C23350 | 0.0024 | 0.002 |
| R15,R19 | 2 | 0 | UNI-ROYAL 0603WAF0000T5E | C21189 | 0.0022 | 0.004 |
| R18 | 1 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.002 |
| R20 | 1 | 33 | UNI-ROYAL 0603WAF330JT5E | C23140 | 0.0024 | 0.002 |
| C32 | 1 | 22p | Samsung CL10C220JB8NNNC C0G | C1653 | 0.0090 | 0.009 |
| C34 | 1 | 4.7u | Samsung CL10A475KP8NNNC X5R 10V | C1705 | 0.0128 | 0.013 |
| C35,C36 | 2 | 15p | Samsung CL10C150JB8NNNC C0G | C1644 | 0.0112 | 0.022 |
| J4 | 1 | OLED I2C | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| R23,R24 | 2 | 4.7k | 0603 4.7k 1% | C23162 | 0.0028 | 0.006 |
| J5 | 1 | UART host / BLE | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J3 | 1 | SWD | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| SW2 | 1 | Test / zero | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| TP1,TP2,TP3,TP4,TP5,TP6 | 6 | TP |  |  |  |  |
| J1 | 1 | USB-C 5V | TYPE-C-31-M-12 | C165948 | 0.1890 | 0.189 |
| F1 | 1 | PTC 500mA | Littelfuse 1206L050YR (6 V) | C163512 | 0.0742 | 0.074 |
| D3 | 1 | SMAJ5.0A | Littelfuse SMAJ5.0A | C83329 | 0.1153 | 0.115 |
| R1,R2 | 2 | 5.1k | 0603 5.1k 1% | C23186 | 0.0016 | 0.003 |
| C5 | 1 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.044 |
| BZ1 | 1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | 0.1513 | 0.151 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| D1 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |

## 3. Bought-in and mechanical items

See the parts and materials section of the manual.

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: BZ1 Buzzer (stock 140).
- **Works-as-intended confidence: Low-Medium**: Clamp-on ultrasonic transit-time measurement has a hard analog front end; the manual itself says Gate 1 acoustic test comes first and it is not sellable.
- **First thing to do:** Run the Gate 1 acoustic test with the evaluation setup before any more boards.
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
