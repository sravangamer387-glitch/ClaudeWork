# TRISHNA urinal hydration monitor: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: reagentless SG estimate needs per-user refractometer calibration; wellness trend only, not a medical device. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/trishna/1_fabrication/trishna_ctrl_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/trishna/2_assembly/trishna_ctrl_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/trishna/2_assembly/trishna_ctrl_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/trishna_priced_BOM.csv`

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
| J1 | 12 V DC in (2 A) | CUI/Same Sky PJ-063AH | C22434582 |
| TP1, TP2, TP3, TP4 | TP |  |  |
| J4 | DevKitC left: 3V3 EN 36 39 34 35 32 33 25 26 27 14 12 GND 13 D2 D3 CMD 5V | BOOMELE 2.54-1*19P female header | C319202 |
| J5 | DevKitC right: GND 23 22 TX RX 21 GND 19 18 5 17 16 4 0 2 15 D1 D0 CLK | BOOMELE 2.54-1*19P female header | C319202 |
| JP1 | 3V3 link (remove for USB-only power) | XFCN PZ254V-11-02P + jumper | C492401 |
| J6 | Peristaltic pump 12 V (red = PUMP_O1) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J7 | Solenoid valve 12 V NC | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J8 | Sensor-block LEDs (450 nm blue, 850 nm IR) | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J9 | Photodiodes BPW34: transmission, 90-degree scatter (anodes to GND) | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J10 | EC electrodes (titanium pins E1, E2) | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J11 | Sump stream-detect probe | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J12 | Chamber-B floor leak probe | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J13 | DS18B20 temperature probe | JST B3B-PH-K-S(LF)(SN) | C131339 |
| J14 | VL53L1X ToF presence sensor (I2C) | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J15 | Telemetry UART (ESP32 TX out, RX in) to USB-serial | JST B3B-PH-K-S(LF)(SN) | C131339 |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$9.16 for 1 board**, **US$8.23 each for 10 boards**, **US$6.45 each for 100 boards** (about INR 806 / 724 / 568 at 88 INR/USD). The per-line break-up is in `costing/trishna_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| J1 | 1 | 12 V DC in (2 A) | CUI/Same Sky PJ-063AH | C22434582 | 2.7602 | 2.760 |
| F1 | 1 | PTC 2A 16V | R+O SMD1812-200-16 (2 A hold) | C46641167 | 0.0771 | 0.077 |
| D3 | 1 | SMBJ15A | Littelfuse SMBJ15A | C83846 | 0.1300 | 0.130 |
| Q5 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| D4 | 1 | BZT52C12 | DIODES BZT52C12-7-F | C124196 | 0.0775 | 0.077 |
| R40,R61,R71,R86,R87,R88,R89 | 7 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.017 |
| C30,C40 | 2 | 100u/35V | Lelon VZH101M1VTR-0607 | C176683 | 0.0881 | 0.176 |
| C31,C41 | 2 | 10u/50V | Samsung CL32A106KBJNNNE | C380537 | 0.2086 | 0.417 |
| U2 | 1 | AP63203WU-7 | AP63203WU-7 (3.3 V fixed) | C780769 | 1.2058 | 1.206 |
| R41,R60,R64,R66,R69 | 5 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.015 |
| C32,C37,C60,C39,C42,C65,C70 | 7 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.052 |
| L1 | 1 | 4.7u | Changjiang FNR5040S4R7MT | C167963 | 0.0933 | 0.093 |
| C33,C34 | 2 | 22u/10V | Samsung CL21A226MPQNNNE | C29277 | 0.0377 | 0.075 |
| FB1 | 1 | BLM18 600R | Murata BLM18AG601SN1D | C19330 | 0.0122 | 0.012 |
| C36,C38,C69 | 3 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.132 |
| D6 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| R45,R73,R74,R79,R81 | 5 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.008 |
| TP1,TP2,TP3,TP4 | 4 | TP |  |  |  |  |
| J4 | 1 | DevKitC left: 3V3 EN 36 39 34 35 32 33 25 26 27 14 12 GND 13 D2 D3 CMD 5V | BOOMELE 2.54-1*19P female header | C319202 | 0.1509 | 0.151 |
| J5 | 1 | DevKitC right: GND 23 22 TX RX 21 GND 19 18 5 17 16 4 0 2 15 D1 D0 CLK | BOOMELE 2.54-1*19P female header | C319202 | 0.1509 | 0.151 |
| JP1 | 1 | 3V3 link (remove for USB-only power) | XFCN PZ254V-11-02P + jumper | C492401 | 0.0189 | 0.019 |
| U3 | 1 | DRV8871DDAR | TI DRV8871DDAR | C75864 | 1.6982 | 1.698 |
| R62,R80 | 2 | 47k | UNI-ROYAL 0603WAF4702T5E | C25819 | 0.0020 | 0.004 |
| J6 | 1 | Peristaltic pump 12 V (red = PUMP_O1) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| Q1,Q2,Q3 | 3 | AO3400A | AO3400A | C20917 | 0.0899 | 0.270 |
| R63,R65,R68,R76,R77 | 5 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.012 |
| D10 | 1 | M7 (1N4007) | MDD M7 (1N4007, 1 A 1000 V) | C95872 | 0.0104 | 0.010 |
| J7 | 1 | Solenoid valve 12 V NC | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| R67,R70 | 2 | 1k 1/4W | UNI-ROYAL 1206W4F1001T5E | C4410 | 0.0086 | 0.017 |
| J8 | 1 | Sensor-block LEDs (450 nm blue, 850 nm IR) | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| U4 | 1 | MCP6002T-I/SN | Microchip MCP6002T-I/SN | C7377 | 0.3121 | 0.312 |
| C61,C63,C64 | 3 | 10n | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | 0.0075 | 0.022 |
| R72 | 1 | 1M | UNI-ROYAL 0603WAF1004T5E | C22935 | 0.0018 | 0.002 |
| C62,C66,C67,C68 | 4 | 1n | Samsung CL10B102KB8NNNC X7R 50V | C1588 | 0.0099 | 0.040 |
| J9 | 1 | Photodiodes BPW34: transmission, 90-degree scatter (anodes to GND) | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| R75 | 1 | 330 | UNI-ROYAL 0603WAF3300T5E | C23138 | 0.0021 | 0.002 |
| J10 | 1 | EC electrodes (titanium pins E1, E2) | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| R78,R82,R83,R84 | 4 | 4.7k | 0603 4.7k 1% | C23162 | 0.0028 | 0.011 |
| J11 | 1 | Sump stream-detect probe | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J12 | 1 | Chamber-B floor leak probe | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J13 | 1 | DS18B20 temperature probe | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J14 | 1 | VL53L1X ToF presence sensor (I2C) | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J15 | 1 | Telemetry UART (ESP32 TX out, RX in) to USB-serial | JST B3B-PH-K-S(LF)(SN) | C131339 | 0.0420 | 0.042 |
| J16 | 1 | microSD (SPI log) | Molex 104031-0811 | C585350 | 0.6848 | 0.685 |

## 3. Bought-in and mechanical items

### 5.2 Bought-in items (India sources; prices are rough guides, check before ordering)
| Item | Qty | Spec / example | Where | Approx. INR |
|---|---|---|---|---|
| ESP32-DevKitC-32E | 1 | **38-pin, 1.0 in (25.4 mm) row spacing**, WROOM-32E or 32D (not WROVER: GPIO16/17 are used). 30-pin DOIT boards do not fit | element14 India, Robu.in | 900-1,100 (clones 450) |
| 12 V DC adapter | 1 | 12 V 2 A, 5.5 x 2.1 mm, centre positive, BIS-marked | local, Amazon.in | 300-450 |
| Peristaltic pump | 1 | 12 V DC, about 0.2-0.4 A, 3 x 5 mm tube, 40-100 mL/min (e.g. Kamoer NKP-DC-S10B, or generic "12V DC dosing pump") | Robu.in, Amazon.in | 450-2,500 |
| Solenoid valve | 1 | 12 V DC **normally closed, direct-acting, 0 MPa minimum**, <= 6 W, 1/8 in or 6-8 mm barbs, food-grade body (water-dispenser / coffee-machine type). **Not** an RO pilot valve | Amazon.in, Robu.in | 250-600 |
| VL53L1X ToF breakout | 1 | 3.3 V, I2C (Pololu #3415 or CJMCU-531) | Robu.in, Robocraze | 600-900 |
| DS18B20 waterproof probe | 1 | 6 x 50 mm stainless sheath, 1 m 3-wire cable | Robu.in | 120-200 |
| Photodiodes | 2 (+1) | **OSRAM SFH 203** (5 mm clear, 400-1100 nm, +/- 75 deg); SFH 203 P also fits | element14 India, Mouser India | 60-90 each |
| LED 450 nm | 1 (+1) | 5 mm water-clear blue, 30 deg or wider | local, Robu.in | 10 |
| LED 850 nm | 1 (+1) | 5 mm IR, 850 nm, 30 deg or wider (e.g. Vishay TSHG6200, or generic 850 nm) | element14, Robu.in | 15-60 |
| Titanium wire | 30 cm | Grade 2, 1.0 mm | Amazon.in (anodising / jewellery wire) | 300-500 |
| Silicone tubing | 2 m + 2 m | food-grade 3 x 5 mm and 4 x 6 mm | Amazon.in, aquarium shops | 150 each |
| M5 to 4 mm hose-barb fittings | 6 | **PP or nylon** (no plain brass in urine), M5 x 0.8 male | Amazon.in, pneumatics shops | 40 each |
| Check valve | 2 | 4 mm aquarium duckbill (one spare) | aquarium shops | 30 each |
| Tee 4 mm | 2 | aquarium PP tee | aquarium shops | 20 each |
| Reducers | 2 | 6-8 mm to 4 mm barb (valve to tubing) | aquarium / Amazon.in | 30 each |
| Cable glands | 4 x M16 + 10 x M12 | nylon, IP68, M16 x 1.5 (4-8 mm) / M12 x 1.5 (3-6.5 mm) | Robu.in, local electrical | kit 300 |
| O-rings | 4 x 5 x 1, 1 x 6 x 1.5 | NBR or silicone | metric O-ring kit (Amazon.in) | 250 |
| Silicone cord | 1.5 m | 2.5 mm solid | Amazon.in | 200 |
| Heat-set inserts | 40 | M3 x 5.7 for 4.0 mm holes | Robu.in | 250 |
| Screws | - | 22 x M3 x 8 (lids), 4 x M3 x 6 (PCB), 8 x M3 x 8 (brackets), 4 x M3 x 45 + nuts (block), 2 x M3 x 10 A2 stainless + 2 ring terminals (leak probe), 10 x M2 x 6 self-tapping (retainers), 8 wall screws + plugs | hardware shop | 300 |
| Cables | - | 1 m 4-core 0.5 mm2; 1 m 8-core 0.22 mm2 alarm cable; 1 m 2-core shielded; 3 m 2-core 0.22 mm2; 2 m 4-core 0.22 mm2 | local electrical | 300 |
| JST PH kit | 1 | PH 2.0 housings 2/3/4-pin + SPH-002T-P0.5S crimps | Robu.in | 250 |
| USB-serial adapter | 1 | CP2102 or CH340, 3.3 V logic | Robu.in | 150 |
| microSD | 1 | 8-32 GB, FAT32 | any | 300 |
| Reservoir | 1 | 1.5-2 L food container + 4 mm aquarium bulkhead | local | 200 |
| Sealants | - | black RTV silicone (neutral cure), 2-part epoxy (Araldite Standard), PTFE tape | hardware shop | 400 |
| Calibration | - | KCl standards 1413 uS/cm and 12.88 mS/cm (Hanna HI7031 / HI7030 sachets) or self-made (section 9.2); handheld **urine-SG refractometer** with ATC (1.000-1.050) | lab suppliers, Amazon.in | 600 + 900-1,500 |
| Bench fluids | - | NaCl, KCl, urea (lab grade or 46 % N fertiliser urea for bench tests), riboflavin tablet or yellow food colour, citric acid | chemist, grocery | 200 |
| Filament | 1 kg | black PETG | Robu.in, local | 1,200 |
---

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: J1 12 V DC in (2 A) (stock 321); U2 AP63203WU-7 (stock 195).
- **Works-as-intended confidence: Low-Medium**: Controller is a standard ESP32 carrier (buck, H-bridge, MOSFET + flyback, TIAs); firmware compiles for the ESP32 and 19 host tests cover the frame, filters, EC maths and every state-machine path; CAD solids give a 2.02 mL chamber. Unproven until built: the printed flow cell must be leak-free, the bipolar GPIO EC drive and the photodiode gains need tuning on the bench, and the SG estimate from conductivity + colour is only as good as the per-user refractometer fit.
- **First thing to do:** Print and pressure-test the sensor block, then run validation V1-V4 with the synthetic-urine fluids before any real use.
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
