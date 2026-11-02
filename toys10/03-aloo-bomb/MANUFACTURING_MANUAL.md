# Aloo Bomb: manufacturing manual

> **Status: design only.** The three arcade games share one board (**Desi Arcade rev B**) and one firmware image; nothing has been built or tested with children.

## 1. What is built

1. Press start; the fuse is hidden and random (20–60 s). Beeps every 1 s, then 0.6, 0.3 and 0.12 s in the last 5 s.
2. Pass the potato round the circle. Whoever holds it at the explosion loses a life / does a silly task from the card.

One board runs three games: hold a button while switching on to choose (none/button 1 = Reflex Raja, button 2 = Taal Memory, button 3 = Aloo Bomb). The blink count at power-on equals the game number.

## 2. Deliverables

| Item | Where |
|---|---|
| PCB: Gerbers, BOM, CPL, KiCad project | `utility10/pcb/release/arcade/` (order-ready: all automatic checks pass) |
| Firmware for the board (8 MHz, rev B pin map) | `toys10/electronic/release/pcb/desi_arcade_rev_b.hex` (build: `make pcb` in `toys10/electronic`) |
| Engine + tests | `toys10/electronic/lib/toycore.c`, 80,045 host checks pass |
| Nano bench demo | `toys10/electronic/release/<game>.hex` |

## 3. Bill of materials

### 3a. Board parts

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | HCTL PZ254-2-03-Z-8.5 (ZHOURI C5116479 had only 340 in stock) | C2894964 | hand/THT |
| J1 | BATT 3xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | hand/THT |
| SW1 | Power | SW_SPDT_PCM12 | C&K PCM12SMTR | C221841 | SMT (JLC) |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | SMT (JLC) |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | hand/THT |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | SMT (JLC) |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | SMT (JLC) |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |
| J5 | Arcade button 1 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J6 | Arcade button 2 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J7 | Arcade button 3 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J8 | Arcade button 4 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| R10 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| R11 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| R12 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| R13 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | SMT (JLC) |
| R14 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |
| R15 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | SMT (JLC) |

### 3b. Bought-in and mechanical (estimates, ~2,000 units)

| Item | Rs |
|---|---|
| MCU (smaller, ATmega-class) | 45 |
| PCB | 25 |
| Button | 8 |
| LEDs + resistors | 8 |
| Buzzer | 12 |
| 2×AAA holder + switch | 14 |
| Silicone shell or ABS potato (amortised) | 50 |
| Packaging + task cards | 30 |
| Assembly + test | 35 |

- 4 arcade push buttons, 30 mm, with 5 V LED lamp (3-wire leads to the JST-PH 3-pin sockets J5-J8: button, lamp, GND), housing (ABS, or 3D-printed/laser-cut MDF for the first 500), 3 x AAA holder, button caps/labels.

## 4. Make the board

Order bare PCBs and SMT assembly per `manuals/STANDARD_PROCEDURES.md` A and B using the files in `utility10/pcb/release/arcade/`; solder the hand/THT parts (JST sockets J5-J8, battery JST J1, slide switch, buzzer BZ1, ISP header).

## 5. Program

```
avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m
avrdude -p m328p -c usbasp -U flash:w:toys10/electronic/release/pcb/desi_arcade_rev_b.hex:i
```
(8 MHz internal, brown-out 2.7 V: 3 x AAA runs from 4.5 V down to about 2.7 V.)

Pin map of the rev B board (generated from the PCB spec): buttons D0, D1, D2, A5; lamp LEDs A1-A4 (330 ohm); buzzer D9; random-seed noise on A0.

## 6. Bring-up

1. Batteries in, switch on: +4V5 at TP1 = 4.2-4.6 V; current under 20 mA idle.
2. Power-on blink count = selected game; hold each button in turn to select each game.
3. Each button lights its own lamp; the buzzer sounds.

## 7. Assemble the toy

Mount four arcade buttons in the lid, wire to J5-J8, fit the board on standoffs, screw-closed battery door, label the game-select instruction on the base.

## 8. Functional test: Aloo Bomb (every unit)

1. Press start: beeps every 1 s, faster (0.6/0.3/0.12 s) in the last 5 s; the explosion sound ends the round (fuse 20-60 s hidden).
2. Run 5 rounds: fuse lengths vary; the explosion always follows the fast beeps.
3. Battery door must be screw-closed on the production housing.

Game select for this game: Hold button 3 while switching on = Aloo Bomb.

Record on `manuals/templates/eol_test_sheet.md`.

## 9. Packaging, compliance

Toys QCO / IS 9873 applicability and testing; age grade and small-parts warnings; Legal Metrology labelling; battery safety, BIS toy-electrics, e-waste EPR, noise level; no licensed names or logos.

Add: age grade label, small-parts warning, battery warning, Legal Metrology marks; buzzer level not above 85 dB at 25 cm (verify).

## 10. Known limits

Host tests: fuse always within the set range with mean 40.0 s, beep tempo bands, explosion exactly at the fuse, millis() wrap-around safe.

Choking/battery-compartment safety (screw-closed battery door is mandatory), noise level of the buzzer (keep ≤ 85 dB at 25 cm; verify).
