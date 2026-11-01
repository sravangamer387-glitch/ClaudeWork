# Beat Runner: manufacturing manual

> **Status: design only; nothing built.**

## 1. What is built

1. Notes spawn at the far end and scroll toward LED 0, getting faster every 40 steps (400 ms → 150 ms).
2. Press when a note is on LED 0 (perfect, 3 points) or LED 1 (good, 1 point). Combos multiply score; 5 misses end the game.
3. Two players alternate; highest score wins.

## 2. Deliverables

| Item | Where |
|---|---|
| PCB (150 x 46 mm, 2 x 74HC595, 16 LEDs) | `utility10/pcb/release/beatrunner/` (released) |
| Firmware for the board | `toys10/electronic/release/pcb/beat_runner_rev_b.hex` (buzzer on D9, build `make pcb`) |
| Engine + tests | `toycore.c` (`br_*`) |

## 3. Bill of materials

### 3a. Board parts

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | BATT 3xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| U2 | 74HC595 | SOIC-16_3.9x9.9mm_P1.27mm | 74HC595D | C5947 | SMT (JLC) |
| U3 | 74HC595 | SOIC-16_3.9x9.9mm_P1.27mm | 74HC595D | C5947 | SMT (JLC) |
| C5 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C6 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| J3 | Arcade button | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| D10 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R20 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D11 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R21 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D12 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R22 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D13 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R23 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D14 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R24 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D15 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R25 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D16 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R26 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D17 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R27 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D18 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R28 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D19 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R29 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D20 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R30 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D21 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R31 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D22 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R32 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D23 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R33 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D24 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R34 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| D25 | Red | LED_0603_1608Metric | Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check) | C72044 | SMT (JLC) |
| R35 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |

### 3b. Bought-in items

| Item | Rs |
|---|---|
| MCU + crystal | 55 |
| PCB | 35 |
| 2 × 74HC595 | 14 |
| 16 LEDs + resistor arrays | 30 |
| Arcade button | 15 |
| Buzzer | 12 |
| Battery/USB power | 30 |
| Enclosure | 60 |
| Packaging + manual | 30 |
| Assembly + test | 45 |

- One 30 mm arcade button (J3), 3 x AAA holder + switch, enclosure, 16 x red 0603 LEDs are on the board.

## 4. Make, program, test

1. Order PCB and SMT assembly per STANDARD_PROCEDURES A/B; solder THT parts (battery JST, switch, buzzer, button socket, ISP).
2. Fuses and flash: `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m` then `-U flash:w:toys10/electronic/release/pcb/beat_runner_rev_b.hex:i`.
3. Pin map: data D11, shift clock D12, latch D13 (shared with the ISP header: the LEDs flicker while programming), button D2, buzzer D9.
4. Test: LEDs light in sequence as notes scroll; press when a note reaches LED 0: perfect = 3 points (high beep), good at LED 1; 5 misses end the game (all LEDs light); speed rises every 40 steps (400 ms to 150 ms).
5. Current: at most a few LEDs lit at once (74HC595 allows 70 mA total); idle current under 15 mA.

## 5. Packaging, compliance

Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

## 6. Known limits

Host tests: scoring windows, a perfect player never loses over 500+ notes, an idle player loses after 5 misses, speed-up bounded to 150 ms.

Perceived value vs mobile games; keep price ≤ Rs 799.
