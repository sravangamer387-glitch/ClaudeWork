# MITTI-NETRA soil + structure node: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: modem is a plug-in breakout. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/mitti/1_fabrication/mitti_netra_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/mitti/2_assembly/mitti_netra_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/mitti/2_assembly/mitti_netra_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/mitti_priced_BOM.csv`

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
| J2 | Solar panel 5-6 V | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J3 | Li-ion cell (protected!) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J6 | Cellular modem (SIM7080G breakout) | HCTL PZ254-2-03-Z-8.5 | C2894964 |
| J4 | Strain-gauge bridge E+ E- A+ A- | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J5 | Soil probe (capacitive, 3.3 V) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J7 | DS18B20 temp | JST B3B-PH-K-S | C131339 |
| J8 | UART flash/debug (USB-serial adapter) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| TP1, TP2, TP3 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$12.97 for 1 board**, **US$11.48 each for 10 boards**, **US$9.29 each for 100 boards** (about INR 1141 / 1010 / 818 at 88 INR/USD). The per-line break-up is in `costing/mitti_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1-N8 | C2913198 | 4.9100 | 4.910 |
| C37,C5,C8,C9,C10,C11,C12,C14,C15,C16 | 10 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.075 |
| C38,C1,C2,C4,C13 | 5 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.221 |
| R42 | 1 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.002 |
| C39,C3 | 2 | 1u | 0603 1uF X7R | C15849 | 0.0144 | 0.029 |
| SW2 | 1 | Reset (EN) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW3 | 1 | Boot (IO0) | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| J1 | 1 | USB-C (charge + program) | TYPE-C-31-M-12 | C165948 | 0.1890 | 0.189 |
| R43,R44 | 2 | 5.1k | 0603 5.1k 1% | C23186 | 0.0016 | 0.003 |
| J2 | 1 | Solar panel 5-6 V | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| D1,D2 | 2 | SS14 | SS14 | C84343 | 0.0252 | 0.050 |
| U4 | 1 | TP4056 | TPOWER TP4056 | C382139 | 0.1208 | 0.121 |
| R1 | 1 | 2.2k | 0603 2.2k 1% | C4190 | 0.0018 | 0.002 |
| R16 | 1 | 6.2k | UNI-ROYAL 0603WAF6201T5E | C4260 | 0.0023 | 0.002 |
| TH1 | 1 | NTC 10k B3950 | FH CMFB103F3950FANT | C51597 | 0.0785 | 0.079 |
| D3 | 1 | Red | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | 0.0077 | 0.008 |
| R2,R3,R15,R14 | 4 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.007 |
| D4,D5 | 2 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.021 |
| J3 | 1 | Li-ion cell (protected!) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| U3 | 1 | AP2112K-3.3 | AP2112K-3.3TRG1 | C51118 | 0.1814 | 0.181 |
| R4,R5 | 2 | 330k | UNI-ROYAL 0603WAF3303T5E | C23137 | 0.0016 | 0.003 |
| Q1 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| R6,R8 | 2 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.006 |
| Q2 | 1 | AO3400A | AO3400A | C20917 | 0.0899 | 0.090 |
| R7,R11,R12 | 3 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.007 |
| C6 | 1 | 100u/35V | Lelon VZH101M1VTR-0607 | C176683 | 0.0881 | 0.088 |
| C7 | 1 | 22u/10V | Samsung CL21A226MPQNNNE | C29277 | 0.0377 | 0.038 |
| J6 | 1 | Cellular modem (SIM7080G breakout) | HCTL PZ254-2-03-Z-8.5 | C2894964 | 0.0766 | 0.077 |
| U5 | 1 | ADXL345 | ADXL345BCCZ-RL7 | C9667 | 5.4131 | 5.413 |
| R9,R10,R13 | 3 | 4.7k | 0603 4.7k 1% | C23162 | 0.0028 | 0.008 |
| U2 | 1 | HX711 | HX711 | C43656 | 0.6211 | 0.621 |
| J4 | 1 | Strain-gauge bridge E+ E- A+ A- | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J5 | 1 | Soil probe (capacitive, 3.3 V) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J7 | 1 | DS18B20 temp | JST B3B-PH-K-S | C131339 | 0.0420 | 0.042 |
| J8 | 1 | UART flash/debug (USB-serial adapter) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| TP1,TP2,TP3 | 3 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/*_enclosure_plate.stl` (106 x 96 x 3 mm, PETG or ABS). Buy an **IP65 ABS junction box** with at least 110 x 100 x 38 mm inside, cable glands and a breather/vent membrane; fix the plate with 4 x M4 screws.
- Board to plate: 4 x M2.5 x 6 mm self-tapping screws. field node: mount on this plate inside an IP65 ABS junction box with cable glands and a vent membrane; place the 18650 holder and the modem breakout in the same box; keep the NTC TH1 side of the board next to the cell; shade the box from direct sun

## 3. Bought-in and mechanical items

### Bought-in
SIM7080G (LTE-M/NB-IoT) breakout board with nano-SIM holder and antenna; protected 18650 cell (or protected pouch cell) with JST-PH 2 lead; 5-6 V solar panel (2 W) with JST-PH 2 lead; capacitive soil moisture probe (3.3 V, analog) with JST-PH 3 lead; DS18B20 waterproof probe; strain gauges (350 ohm, GF about 2) with bridge completion; IP65 enclosure with cable glands; a SIM and data plan.

## 4. Confidence (read before you order)

- **Order confidence: High**: all parts live-checked, none flagged.
- **Works-as-intended confidence: Medium**: Charger thermal pad now grounded with thermal vias; NTC window stops Li-ion charging outside about 6 to 44 C; power diodes corrected; IP65 box with a printed mounting plate; firmware core 23 checks and the pin map match; the cellular modem is a plug-in breakout and the ESP32 skeleton has never been compiled.
- **First thing to do:** Bring up power and charging first (check TEMP voltage at room temperature), then the modem last.
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
