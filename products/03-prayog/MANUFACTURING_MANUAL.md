# Prayog STEM lab kit: manufacturing manual

> **Status: firmware and analysis tools tested on the host; the hub board is **order-ready (all automatic checks pass)**; no hardware built; sensors uncalibrated; syllabus mapping and school procurement route unverified.**

## 1. What is made

A hub board (ATmega328P at 16 MHz, CH340C USB-serial with auto-reset, USB-C, eight 3-pin sensor sockets A0-A7, photogate port on D2, ultrasonic port on D4/D5, reaction pad button D8 + LED D7) plus **12 plug-in sensor modules** and 20 experiments with worksheets and a teacher guide. Firmware streams CSV at 115200 baud; Python tools analyse data offline.

| Deliverable | Where |
|---|---|
| Hub PCB | `utility10/pcb/release/prayog/` |
| Firmware | `products/03-prayog/release/prayog.hex` (9.6 KB flash, 434 B RAM), source `products/03-prayog/firmware/`, 40 sensor-library checks |
| Analysis tools | `products/03-prayog/tools/prayog_tools.py` (11 of 11 pass on simulated data) |
| Experiments | `products/03-prayog/docs/experiments.md` (20) |
| Cost model | `products/03-prayog/docs/kit_cost.txt` (BOM Rs 2,580 at about 1,000 kits) |

## 2. Hub board bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | SMT (JLC) |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | SMT (JLC) |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | hand/THT |
| J1 | USB-C data + 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | SMT (JLC) |
| F1 | PTC 500mA | Fuse_1206_3216Metric | Littelfuse 1206L050YR (6 V) | C163512 | SMT (JLC) |
| D3 | SMAJ5.0A | D_SMA | Littelfuse SMAJ5.0A | C83329 | SMT (JLC) |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | SMT (JLC) |
| C5 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | SMT (JLC) |
| U2 | CH340C | SOIC-16_3.9x9.9mm_P1.27mm | CH340C | C84681 | SMT (JLC) |
| C6 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C7 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C8 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| Y1 | 16 MHz | Crystal_SMD_3225-4Pin_3.2x2.5mm | YXC X322516MOB4SI 16 MHz 12 pF 3225 (LCSC listing seen in search results; matches the 22 pF load caps) | C12668 | SMT (JLC) |
| C9 | 22p | C_0603_1608Metric | Samsung CL10C220JB8NNNC C0G | C1653 | SMT (JLC) |
| C10 | 22p | C_0603_1608Metric | Samsung CL10C220JB8NNNC C0G | C1653 | SMT (JLC) |
| J3 | Analog socket A0 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J4 | Analog socket A1 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J5 | Analog socket A2 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J6 | Analog socket A3 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J7 | Analog socket A4 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J8 | Analog socket A5 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J9 | Analog socket A6 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J10 | Analog socket A7 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J11 | Photogate | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | hand/THT |
| J12 | Ultrasonic HC-SR04 | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | hand/THT |
| SW2 | Reaction pad | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | SMT (JLC) |
| D1 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | SMT (JLC) |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | SMT (JLC) |

## 3. The 12 modules (bought-in or built in-house)

Temperature (10k NTC with 10k divider), light (LDR with divider), sound level (electret microphone module), magnetic field (linear Hall sensor), soil moisture (capacitive), voltage probe x2 (resistor divider with input protection, low voltage only), IR reflective, water conductivity (AC-driven pair), ultrasonic distance (HC-SR04 class), photogate x2 (U-slot optical sensors, output LOW when the beam is interrupted), button + LED reaction pad. Each module plugs into a 3-pin JST-PH socket: +5 V, signal, GND.

Procure from a module supplier with lot test data, or build them on small boards using the same procedure (STANDARD_PROCEDURES A-F).

## 4. Make the hub

1. Order PCBs and SMT assembly per STANDARD_PROCEDURES A and B (the CH340C, ATmega328P, crystal and 22 pF caps are on the JLC BOM when released); solder the hand/THT parts (USB-C tabs, JST sockets, ISP header, button).
2. **Bootloader/firmware:** fuses for a 16 MHz external crystal: `avrdude -p m328p -c usbasp -U lfuse:w:0xFF:m -U hfuse:w:0xDE:m -U efuse:w:0xFD:m` (Arduino Uno values: full-swing 16 MHz crystal, 2.7 V brown-out, reset vector at the Optiboot bootloader; use hfuse 0xD9 if you flash the hex directly with no bootloader; confirm all values against the ATmega328P datasheet). Burn an Arduino-Uno-class (Optiboot) bootloader over ISP, then upload `prayog.hex` over USB at 115200 baud (`avrdude -p m328p -c arduino -P <port> -b 115200 -U flash:w:prayog.hex:i`), or flash the hex directly over ISP without a bootloader (then the auto-reset capacitor is unused).
3. Plug the USB-C cable: +5 V = 5.0 V, the CH340C enumerates as a serial port (install the WCH driver on Windows if needed). Open a serial terminal at 115200: CSV lines appear 10 times a second (`ms,A0..A7,echo_cm,gate_count`).
4. Commands: `SET <0-7> <NTC|LDR|MIC|HALL|SOIL|VOLT|IR|COND>` assigns a sensor type to a socket.

## 5. Calibration (per module type, before shipping a kit)

NTC: check 0 and 100 C reference (ice and boiling water: within the 0.6 C limit set by the 10-bit ADC); LDR: record a lux table with a reference lux meter; Hall: sensitivity with a known magnet; soil: dry/wet counts (typical 520/260: measure); ultrasonic: speed of sound correction with temperature (library does it) checked at 100 cm; photogate: timing check with a falling-object rig. **Sensor constants in the library are typical datasheet values: the experiments must be validated with real sensors (the analysis validation used simulated data only).**

## 6. End-of-line test per hub (and per kit)

1. Supply current from USB under 100 mA with no modules.
2. Serial output appears; each socket reads a pot or fixed divider correctly (A0-A7 within +-1 %).
3. Photogate: interrupt the beam: a `G,<us>,1` line is printed, release: `G,<us>,0`.
4. Ultrasonic: 100 cm target reads 100 +-2 cm at 20 C.
5. Reaction pad: button and LED respond.
6. Run one analysis (`prayog_tools.py`) on a recorded file.
Record on `manuals/templates/eol_test_sheet.md`.

## 7. Kit assembly and packaging

Tray with the hub, 12 modules, cables (3-pin leads), magnets, steel ball and string for the pendulum/photogate experiments, printed student worksheets (20) and a teacher guide (to be written from `experiments.md`). Label 12+, low-voltage only, small-parts warning. Compliance to verify: BIS/lab view on whether kits for under-14s fall under the toys QCO, e-waste EPR.

## 8. Procurement and pilot (not done)

Ask five schools and one lab-kit dealer how kits are bought (GeM, dealers, direct) before building stock; teacher review of the syllabus mapping; pilot in two schools; price list; EMS RFQ.

## 9. Known limits

Simulated validation only; 10 of 20 experiments have a validated analysis; hardware unbuilt; sensor constants typical; USB bootloader flow untested.
