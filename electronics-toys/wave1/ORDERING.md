# Wave 1 electronics toys: ordering guide (what to buy, where, in what order)

> Companion to [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). Main caveat for this project: AP1 board order-ready; MP3 module and 4-digit display module are bought-in. Prices and stock are from LCSC on the run date; vendors, shipping and customs rules change: verify before paying. General rules and vendor list: [`manuals/ORDERING_GUIDE.md`](../../manuals/ORDERING_GUIDE.md).

## 1. Order of work

1. Read the manual and the caveat above.
2. Order the circuit boards and SMD assembly (section 2).
3. While the boards travel, order the other items (sections 3 and 5) and make the printed or laser-cut parts.
4. Assemble, program and test only after everything has arrived; follow the manual.

## 2. Order the circuit boards (JLCPCB, PCB + assembly)

Files (all in this repository):

- Gerbers: `utility10/pcb/release/ap1/1_fabrication/ap1_audio_gerbers.zip`
- Assembly BOM: `utility10/pcb/release/ap1/2_assembly/ap1_audio_JLC_BOM.csv`
- Pick-and-place (CPL): `utility10/pcb/release/ap1/2_assembly/ap1_audio_JLC_CPL.csv`
- Full BOM with LCSC numbers and prices: `costing/ap1_priced_BOM.csv`

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
| J1 | BATT 3xAA | JST B2B-PH-K-S(LF)(SN) | C131337 |
| BZ1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 |
| J8 | MP3 module left row (VCC RX TX DACR DACL SPK1 GND SPK2) | hanxia HX PM2.54-1x8P ZC-Y | C22438158 |
| J9 | MP3 module right row (BUSY .. GND IO1) | hanxia HX PM2.54-1x8P ZC-Y | C22438158 |
| J10 | Speaker 3 W 4-8 ohm | JST B2B-PH-K-S(LF)(SN) | C131337 |
| J11 | Display module (VCC SCLK RCLK DIO GND) | JST S5B-PH-K-S(LF)(SN) | C157923 |
| J13 | RGB LED (common anode) / lamp | JST B4B-PH-K-S(LF)(SN) | C131334 |
| J14 | Projector motor | JST B2B-PH-K-S(LF)(SN) | C131337 |
| TP1, TP2, TP4 | TP |  |  |

Order these with the same LCSC order (add them to the cart so one shipment arrives) or buy locally in India (section 5).

### Parts cost and stock (live LCSC prices on the run date)

Total parts per board: **US$6.61 for 1 board**, **US$6.08 each for 10 boards**, **US$5.03 each for 100 boards** (about INR 582 / 535 / 443 at 88 INR/USD). The per-line break-up is in `costing/ap1_priced_BOM.csv`. This is parts only: PCB fabrication, assembly fees, shipping, customs and GST come on top (see `manuals/ORDERING_GUIDE.md`, section 6).

Stock warnings on the run date:

-  TP (no lcsc price (hand-fit or not priced), stock )

| Refs | Qty | Value | Part | LCSC | Unit USD (1 board) | Line USD |
|---|---|---|---|---|---|---|
| U1 | 1 | ATmega328P-AU | ATMEGA328P-AU | C14877 | 2.3308 | 2.331 |
| C1,C2,C3,C21,C25,C24,C22 | 7 | 100n | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | 0.0075 | 0.052 |
| R7,R47 | 2 | 10k | 0603 10k 1% | C25804 | 0.0024 | 0.005 |
| J2 | 1 | ISP | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | 0.0766 | 0.077 |
| J1 | 1 | BATT 3xAA | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| SW1 | 1 | Power | C&K PCM12SMTR | C221841 | 1.2754 | 1.275 |
| Q2 | 1 | AO3401A | AO3401A | C15127 | 0.0969 | 0.097 |
| C4 | 1 | 10u | 0805 10uF X5R | C15850 | 0.0441 | 0.044 |
| BZ1 | 1 | Buzzer | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | 0.1513 | 0.151 |
| Q1 | 1 | MMBT3904 | MMBT3904 | C20526 | 0.0118 | 0.012 |
| D2 | 1 | 1N4148WS | 1N4148WS | C2128 | 0.0120 | 0.012 |
| R6,R5,R8,R10,R11,R60,R61,R62,R63,R64,R65,R66 | 12 | 1k | 0603 1k 1% | C21190 | 0.0017 | 0.020 |
| D1 | 1 | Green | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | 0.0105 | 0.011 |
| D4 | 1 | Amber | Hubei KENTO KT-0603Y yellow (Everlight 19-213 was out of stock) | C2287 | 0.0105 | 0.011 |
| J8 | 1 | MP3 module left row (VCC RX TX DACR DACL SPK1 GND SPK2) | hanxia HX PM2.54-1x8P ZC-Y | C22438158 | 0.1359 | 0.136 |
| J9 | 1 | MP3 module right row (BUSY .. GND IO1) | hanxia HX PM2.54-1x8P ZC-Y | C22438158 | 0.1359 | 0.136 |
| C20 | 1 | 100u/35V | Lelon VZH101M1VTR-0607 | C176683 | 0.0881 | 0.088 |
| J10 | 1 | Speaker 3 W 4-8 ohm | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| J11 | 1 | Display module (VCC SCLK RCLK DIO GND) | JST S5B-PH-K-S(LF)(SN) | C157923 | 0.0777 | 0.078 |
| U5 | 1 | 74HC595 | 74HC595D | C5947 | 0.1079 | 0.108 |
| D10,D11,D12,D13,D14,D15,D16 | 7 | Red | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | 0.0077 | 0.054 |
| SW2 | 1 | Button 1 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW3 | 1 | Button 2 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW4 | 1 | Button 3 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW5 | 1 | Button 4 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW6 | 1 | Button 5 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW7 | 1 | Button 6 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| SW8 | 1 | Button 7 | Omron B3U-1000P | C231329 | 0.1894 | 0.189 |
| R40 | 1 | 1k | UNI-ROYAL 0603WAF1001T5E | C21190 | 0.0017 | 0.002 |
| R41 | 1 | 2.2k | UNI-ROYAL 0603WAF2201T5E | C4190 | 0.0018 | 0.002 |
| R42 | 1 | 3.9k | UNI-ROYAL 0603WAF3901T5E | C23018 | 0.0021 | 0.002 |
| R43 | 1 | 6.8k | UNI-ROYAL 0603WAF6801T5E | C23212 | 0.0024 | 0.002 |
| R44 | 1 | 12k | UNI-ROYAL 0603WAF1202T5E | C22790 | 0.0031 | 0.003 |
| R45 | 1 | 22k | UNI-ROYAL 0603WAF2202T5E | C31850 | 0.0042 | 0.004 |
| R46 | 1 | 47k | UNI-ROYAL 0603WAF4702T5E | C25819 | 0.0020 | 0.002 |
| Q9,Q10,Q11,Q12 | 4 | AO3400A | AO3400A | C20917 | 0.0899 | 0.360 |
| R50,R51,R52,R53 | 4 | 100 | UNI-ROYAL 0603WAF1000T5E | C22775 | 0.0024 | 0.010 |
| R54,R55,R56,R57,R58,R59 | 6 | 100k | 0603 100k 1% | C25803 | 0.0030 | 0.018 |
| J13 | 1 | RGB LED (common anode) / lamp | JST B4B-PH-K-S(LF)(SN) | C131334 | 0.0458 | 0.046 |
| J14 | 1 | Projector motor | JST B2B-PH-K-S(LF)(SN) | C131337 | 0.0359 | 0.036 |
| D8 | 1 | SS14 | SS14 | C84343 | 0.0252 | 0.025 |
| TP1,TP2,TP4 | 3 | TP |  |  |  |  |

## 2b. Enclosure: printed parts and fasteners (generated from the board)

- Print `4_enclosure/` base and lid (outer about 143 x 107 x 50 mm) in PETG or ABS, 3 perimeters, 25 % infill; the lid closes with **4 x M2.5 x 10 mm self-tapping screws** into the corner columns; the board sits on its standoffs with 4 x M2.5 x 6 mm self-tapping screws.
- Battery: **Keystone 2465 (3 x AA, wire leads)** in the floor bay (60.0 x 50.3 x 17.8 mm); print `*_enclosure_battery_door.stl`; the door closes with 2 x M2.5 x 6 mm self-tapping (tool needed to open). Route the holder lead through the hole in the bay ceiling to the battery connector.
- Print `*_enclosure_caps.stl` (light pipe, plunger, slider): plunger for SW2; plunger for SW3; plunger for SW4; plunger for SW5; plunger for SW6; plunger for SW7; plunger for SW8; light pipe for D1; light pipe for D4; slider for SW1. Light pipes in clear PETG or resin; fit plungers and pipes from inside before closing the lid.
- shared platform box: display window for the bought 4-digit module (fix the module to the lid behind tinted acrylic with M3 screws/standoffs; lead to J11), seven button plungers, speaker grille to add for the chosen speaker; 3 x AA bay with a screwed door
- Print one set first and test-fit the board, the holder and every cap; the dimensions are first-pass.

## 3. Bought-in and mechanical items

## Bought-in items (not on the JLCPCB assembly)
| Item | Qty per toy | Used in | Where (India) | Notes |
|---|---|---|---|---|
| DFPlayer Mini MP3 module (or clone with the same pinout) | 1 | P1 rhymes, P4 cricket (P3 optional) | Robu.in, Robocraze, Amazon.in (about Rs 120-180) | Check the command codes on the real module (see firmware README). |
| microSD card 1-8 GB, FAT32 | 1 | with the MP3 module | any shop | Files `/mp3/0001.mp3`... as in the prototype guide. |
| Speaker 3 W, 4-8 ohm, 40-57 mm, with 2-pin JST PH lead | 1 | P1, P4 | Robu.in, Amazon.in | |
| 4-digit 0.36 in LED display module with two 74HC595 (pins VCC SCLK RCLK DIO GND) | 1 | P4 cricket | Robu.in, Robocraze, Amazon.in, AliExpress (about Rs 60-120) | Common-anode version expected; if digits look inverted or ghosted, change `DISP_SEG_ACTIVE_LOW` / `DISP_DIGIT_ACTIVE_HIGH` in `firmware/src_avr/main_ap1.cpp` and rebuild. |
| JST PH 2.0 mm 5-pin to Dupont female lead, 15-20 cm | 1 | P4 cricket | Robu.in, Amazon.in, AliExpress | Plugs J11 to the display module header. Check the pin order end to end before power-up. |
| Keystone 2465 (or equivalent) 3 x AA holder with lead and 2-pin JST PH plug | 1 | all | element14 India, Amazon.in | |
| RGB common-anode LED (or LED strip segment, 5 V) with 4-pin JST PH lead | 1 | P3 lamp | Robu.in | |
| Small 3-6 V DC motor for the projector disc, 2-pin JST PH lead | 1 | P3 lamp (optional) | Robu.in | |
| Tinted acrylic window, M3 x 8 screws + 4 mm standoffs for the display module | 1 set | P4 cricket | local laser cutter, hardware shop | |
| AA cells | 3 | all | any shop | |

## 4. Confidence (read before you order)

- **Order confidence: Medium-High**: limited stock on: BZ1 Buzzer (stock 140).
- **Works-as-intended confidence: Low-Medium**: AP1 board added (ATmega328P, MP3 module socket, bought-in 4-digit 74HC595 display module on a 5-way lead, 7-LED ball lane on a 74HC595, 7-button resistor ladder, lamp and motor drivers); all three apps now build for the board (about 6 kB each) and pass 76 host checks. The MP3 command codes are from memory and must be checked on the real module; the ladder thresholds are calculated, not measured.
- **First thing to do:** Bench-test one board per product: ladder readings, MP3 commands, display module polarity (one compile flag each).
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
