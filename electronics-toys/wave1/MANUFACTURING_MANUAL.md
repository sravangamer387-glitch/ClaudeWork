# Wave 1 electronics toys (rhymes player P1, star lamp P3, handheld cricket P4): manufacturing manual

> **Status: prototype-ready on one shared board (AP1).** One circuit board, the AP1 audio platform, serves all three toys. Each toy is a different firmware build plus a different set of parts fitted. The board release (Gerbers, BOM, pick-and-place, schematic, enclosure) is in `utility10/pcb/release/ap1/` and copied to `hardware/ap1_audio/`. The firmware builds for the board (`make avr`, about 6 kB per product) and passes 76 host checks. **Nothing has been built yet.** Toy-safety certification (IS 9873 / BIS) is a separate step before selling.

## What exists
| Item | Where |
|---|---|
| AP1 board release: Gerbers, JLC BOM + CPL, schematic PDF, assembly drawing, 3D model, enclosure STL | `utility10/pcb/release/ap1/` (copy in `hardware/ap1_audio/`) |
| Firmware: portable core + three apps, ATmega328P HAL | `firmware/` (`make test`: 76 checks; `make avr`: `release/ap1_rhymes_8MHz.hex`, `ap1_lamp_8MHz.hex`, `ap1_cricket_8MHz.hex`) |
| Concept-stage pin map, power budget, design-to-cost (before AP1) | `hardware/out/` (kept for history; the AP1 schematic overrides it) |
| Product shells (rhymes, lamp, cricket) | `enclosure/out/*.stl` + `checks.md`; the AP1 release adds a generic platform box |
| Factory test spec (draft) | `docs/factory-test-spec.md` |
| Breadboard prototypes | `prototypes/` (E1 rhymes player, E2 star lamp, E3 cricket) |

## The AP1 board in one paragraph
ATmega328P-AU at 8 MHz internal oscillator, powered from 3 x AA through a slide switch and a reverse-polarity P-MOSFET. A DFPlayer-Mini-type MP3 module plugs into two 1x8 sockets (1 k series resistors on its UART, BUSY to D2, 100 uF bulk) and drives a 3 W speaker on J10. Seven buttons share one ADC input through a resistor ladder. A 74HC595 drives the seven ball-lane LEDs for the cricket game; its serial output continues to a **bought-in 4-digit 74HC595 LED display module** on J11 (5-way JST PH side-entry: VCC, SCLK, RCLK, DIO, GND). Three AO3400A MOSFETs drive an RGB common-anode lamp (J13) and one drives the projector motor (J14, SS14 flyback). Buzzer, two status LEDs, battery divider, 6-pin ISP header and test points complete it. Board 128 x 92 mm, 2 layers.

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

## Fitting options per toy
| Toy | Firmware | Fit | Leave empty |
|---|---|---|---|
| P1 rhymes player | `ap1_rhymes_8MHz.hex` | MP3 module, speaker, buttons, status LEDs | display module, lamp/motor leads |
| P3 star lamp | `ap1_lamp_8MHz.hex` | RGB lamp lead, motor lead, buttons | display module (MP3 optional for lullabies) |
| P4 cricket | `ap1_cricket_8MHz.hex` | display module, lane LEDs (on board), MP3 + speaker, buttons | lamp/motor leads |

## Build and programme
1. Order 5 boards with assembly from JLCPCB using `ORDERING.md` (Gerbers, BOM, CPL in the release folder). Through-hole parts (sockets, JST connectors, buttons, switch, buzzer, ISP header) are listed as hand-solder parts in the ordering guide.
2. Visual check against `*_assembly_top.pdf`; then bench power at 4.5 V, current-limited to 300 mA, with no modules fitted: expect about 5 mA.
3. Programme the ATmega328P through the 6-pin ISP header (USBasp or an Arduino as ISP): set fuses for 8 MHz internal (`lfuse 0xE2, hfuse 0xD9, efuse 0xFE` (brown-out at 1.8 V); e.g. `avrdude -c usbasp -p m328p -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m -U flash:w:release/ap1_cricket_8MHz.hex`), then flash the product hex.
4. Fit the bought-in items for the toy, insert the SD card, and run the self-test: every LED and display segment lights, each button is reported, the MP3 module plays track 1.
5. Close the enclosure (printed base and lid from the release, or the product shells in `enclosure/out/`).

## What must still be done before selling (not before prototyping)
1. Bench tests on the built prototypes: current draw, sound level (keep within the toy standard), battery life, drop test, EMC pre-scan.
2. Tooling-grade CAD for the product shells: draft angles, fillets, snap fits, ribs, gating.
3. Content: recorded rhymes, stories and lullabies with talent releases (copyright).
4. Compliance: IS 9873 (toy safety) and IS 15644 testing, BIS licence, labels and user manual.

MP3 module command codes were written from recollection and must be checked on the real module. The button ladder thresholds are calculated, not measured. The lamp's colour change limit (one level per 20 ms, no flashing) is enforced by tests and must be re-verified on hardware.

## Prototype build (breadboard route, before the board arrives)
Follow `prototypes/guides/electronics-prototypes.md` (wiring, SD-card layout, flashing, acceptance tests) and the manual in `prototypes/MANUFACTURING_MANUAL.md`.
