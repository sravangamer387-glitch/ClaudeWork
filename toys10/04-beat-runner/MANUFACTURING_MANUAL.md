# Beat Runner: manufacturing manual

> **Status: design only; nothing built.**

## 1. What is built

1. Notes spawn at the far end and scroll toward LED 0, getting faster every 40 steps (400 ms → 150 ms).
2. Press when a note is on LED 0 (perfect, 3 points) or LED 1 (good, 1 point). Combos multiply score; 5 misses end the game.
3. Two players alternate; highest score wins.

## 2. Deliverables

| Item | Where |
|---|---|
| PCB (150 x 46 mm, 2 x 74HC595, 16 LEDs) | `utility10/pcb/release/beatrunner/` (**not yet released**: routing/verification unfinished) |
| Firmware for the board | `toys10/electronic/release/pcb/beat_runner_rev_b.hex` (buzzer on D9, build `make pcb`) |
| Engine + tests | `toycore.c` (`br_*`) |

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
