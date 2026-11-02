# AP1 shared audio platform (rhymes player, star lamp, cricket game) (rev A)

AP1 shared audio platform (128 x 92 mm) for the rhymes player, star lamp and cricket game: ATmega328P at 8 MHz from 3 x AA, DFPlayer-type MP3 module socket and speaker, a bought-in 4-digit 74HC595 LED display module on a 5-way lead, a 74HC595 driving a 7-LED ball lane, seven buttons on one ADC ladder, lamp and motor drivers, buzzer.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 128 x 92 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 287 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 79 parts, 60 nets.

## Circuit description
- **MP3:** module in two 1x8 sockets, 1 k series on RX and TX, BUSY on D2, 100 uF bulk; speaker on J10.
- **Display and lane:** U5 74HC595 drives the 7 lane LEDs; its QH' feeds DIO of the bought 4-digit 74HC595 display module on J11 (JST PH side-entry: VCC SCLK RCLK DIO GND). Each 2 ms refresh shifts 24 bits (segment byte, digit byte, lane byte) and latches; SER/SRCLK/RCLK on D11/D13/D12 (shared with ISP). Segment/digit polarity flags `DISP_SEG_ACTIVE_LOW` / `DISP_DIGIT_ACTIVE_HIGH` in `main_ap1.cpp` cover module variants.
- **Buttons:** 10 k pull-up on A6, buttons to GND through 1k, 2.2k, 3.9k, 6.8k, 12k, 22k, 47k: one press decoded at a time.
- **Lamp/motor:** AO3400A on D3/D5/D6 (RGB, common anode) and D10 (motor, SS14 flyback). **Firmware:** `electronics-toys/wave1/firmware`, `make avr` builds one hex per product.

## Power
Idle about 20 mA (MP3 module), playing 100-700 mA peaks into a 3 W speaker; 3 x AA give a few hours of play.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [128.1, 92.1] mm, match |

Enclosure (prototype shell for 3D printing, screwed lid, 3xAA bay with screwed door): outer 143.2 x 107.2 x 49.8 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | verified |
| J1 | BATT 3xAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | verified |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | verified |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D1 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D4 | Amber | LED_0603_1608Metric | Hubei KENTO KT-0603Y yellow (Everlight 19-213 was out of stock) | C2287 | verified |
| R8 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J8 | MP3 module left row (VCC RX TX DACR DACL SPK1 GND SPK2) | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P ZC-Y | C22438158 | verified |
| J9 | MP3 module right row (BUSY .. GND IO1) | PinSocket_1x08_P2.54mm_Vertical | hanxia HX PM2.54-1x8P ZC-Y | C22438158 | verified |
| R10 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R11 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C21 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C20 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VZH101M1VTR-0607 | C176683 | verified |
| J10 | Speaker 3 W 4-8 ohm | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| J11 | Display module (VCC SCLK RCLK DIO GND) | JST_PH_S5B-PH-K_1x05_P2.00mm_Horizontal | JST S5B-PH-K-S(LF)(SN) | C157923 | verified |
| U5 | 74HC595 | SOIC-16_3.9x9.9mm_P1.27mm | 74HC595D | C5947 | verified |
| C25 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| R60 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R61 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R62 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R63 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R64 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R65 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R66 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D10 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D11 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D12 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D13 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D14 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D15 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| D16 | Red | LED_0603_1608Metric | Hubei KENTO KT-0603R red (Everlight 19-217 was out of stock) | C2286 | verified |
| SW2 | Button 1 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW3 | Button 2 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW4 | Button 3 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW5 | Button 4 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW6 | Button 5 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW7 | Button 6 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW8 | Button 7 | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| R40 | 1k | R_0603_1608Metric | UNI-ROYAL 0603WAF1001T5E | C21190 | verified |
| R41 | 2.2k | R_0603_1608Metric | UNI-ROYAL 0603WAF2201T5E | C4190 | verified |
| R42 | 3.9k | R_0603_1608Metric | UNI-ROYAL 0603WAF3901T5E | C23018 | verified |
| R43 | 6.8k | R_0603_1608Metric | UNI-ROYAL 0603WAF6801T5E | C23212 | verified |
| R44 | 12k | R_0603_1608Metric | UNI-ROYAL 0603WAF1202T5E | C22790 | verified |
| R45 | 22k | R_0603_1608Metric | UNI-ROYAL 0603WAF2202T5E | C31850 | verified |
| R46 | 47k | R_0603_1608Metric | UNI-ROYAL 0603WAF4702T5E | C25819 | verified |
| R47 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C24 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| Q9 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| Q10 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| Q11 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| Q12 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R50 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R51 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R52 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R53 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R54 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R55 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R56 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R57 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J13 | RGB LED (common anode) / lamp | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| J14 | Projector motor | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| D8 | SS14 | D_SMA | SS14 | C84343 | verified |
| R58 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R59 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| C22 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Bench 4.5 V, current-limited 300 mA, no module: about 5 mA.
2. Flash the product hex; press each button and read the ladder value on the serial monitor (debug build) against the thresholds.
3. Plug the display module lead into J11: all segments and the 7 lane LEDs light in the self-test (if the digits show inverted or ghosted, flip the polarity flags and rebuild); then the MP3 module with an SD card.

## Files
`1_fabrication/` Gerber + drill zip (upload to JLCPCB/any fab), fab notes, copper plot
`2_assembly/` JLC BOM + CPL (SMD parts JLC assembles), full BOM with LCSC numbers for every part, pick-and-place, assembly drawing
`3_design/` KiCad 7 project (pcb, schematic, libs), netlist, STEP model, schematic PDF, renders
`4_enclosure/` printable enclosure (base, screwed lid, battery door, plungers / light pipes / switch extensions) or a mounting plate for a bought IP65 box; dimensions and notes in enclosure.json
`5_verification/` DRC, ERC, verification and readiness reports

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.

## Manufacturing readiness (automatic check)

| Check | Result |
|---|---|
| gerber layers and drill present | PASS |
| drc errors 0 | PASS |
| unconnected 0 | PASS |
| netlist matches schematic | PASS |
| erc errors 0 | PASS |
| independent gerber check clean | PASS |
| every part has lcsc number | PASS |
| every lcsc number verified | PASS |
| cpl rows equal jlc bom parts | PASS |
| step model | PASS |
| KiCad DRC warnings | 0 |
| **Order ready** | **YES** |

Order steps: (1) upload `1_fabrication/*_gerbers.zip`; (2) for assembly upload `2_assembly/*_JLC_BOM.csv` and `*_JLC_CPL.csv`, check the 3D/rotation preview for every polarised part (diodes, ICs, LEDs, electrolytics) because CPL rotations are generated, not hand-checked; (3) buy the through-hole parts listed in `*_BOM_full.csv` marked hand/THT and solder them; (4) re-check stock and the exact LCSC listing for every line before paying.

Limits: the layout is software-generated and has not been reviewed by a PCB engineer; no prototype has been built; the first batch should be treated as a prototype run (order 5 boards).
