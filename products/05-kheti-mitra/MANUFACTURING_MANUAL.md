# Kheti-Mitra irrigation controller: manufacturing manual

> **Status: board files are order-ready (all automatic checks pass: DRC 0, netlist match, verified part numbers); the control logic is simulation-tested; nothing has been built or field-tested.** Savings claims (about 43 % less water in the simulation) must be proven in a 60-day field trial before any marketing.

## 1. What is made
A 12 V DC controller (barrel jack in, 5 V on board) that opens a 12 V solenoid valve only when soil is dry, holds after rain, limits each watering to 20 min and the day to 60 min, and falls back to a safe timer (5 min every 12 h) if both soil sensors fail. Low voltage only: **there is no mains wiring in this product; use a certified, BIS-registered 12 V adapter.**

| Deliverable | Where |
|---|---|
| Board (Gerbers, BOM, CPL, KiCad project, STEP, enclosure STL) | `utility10/pcb/release/kheti/` (folders 1_fabrication ... 5_verification) |
| Firmware for the board | `products/05-kheti-mitra/release/kheti_mitra_board_8MHz.hex` (build: `make board` in `products/05-kheti-mitra/firmware`); the Nano bench version is `release/kheti_mitra.hex` |
| Engine + tests | `firmware/lib/kheti_core.c`, `firmware/test/test_kheti.c` (22 checks pass) |
| Enclosure | `enclosure_body.stl`, `enclosure_lid.stl` (prototype shell; the release folder has a shell sized to the board) |

## 2. Bill of materials
- Board parts (37 parts incl. barrel jack, polyfuse, TVS, AMS1117-5.0, valve MOSFET AO3400A, Schottky flyback diode SS14): see the table in `utility10/pcb/release/kheti/README.md` and the machine-readable `2_assembly/kheti_mitra_BOM_full.csv`.
- Bought-in: 12 V DC adapter (BIS-registered, 1 A or more), 12 V normally-closed solenoid valve (1/2 in), 2 capacitive soil-moisture sensors (3-wire, 3.3-5 V), rain sensor module (digital output), tubing/fittings, IP65 box if used outdoors, cable glands.
- Designed production BOM is Rs 620 (earlier guess Rs 520); recommended price Rs 2,299 (see product README economics).

## 3. Make the board
1. Order PCBs per `manuals/STANDARD_PROCEDURES.md` A; ENIG recommended, HASL lead-free acceptable (finish noted in the board README).
2. Order SMT assembly per section B with `2_assembly/kheti_mitra_JLC_BOM.csv` and `..._JLC_CPL.csv`. Solder the hand/THT parts: barrel jack J1, JST sensors J6-J8 and valve terminal J5, ISP header J2.
3. Check polarity: the SS14 flyback diode D7 across the valve output (stripe toward +12 V), the TVS D3.

## 4. Program
- Fuses (5 V board, 8 MHz internal): `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFD:m`
- Flash: `avrdude -p m328p -c usbasp -U flash:w:products/05-kheti-mitra/release/kheti_mitra_board_8MHz.hex:i` (then verify with `flash:v`).
- Pin map (generated from the board): valve gate D6, soil sensors A0/A1, rain sensor D3 (LOW = wet), hold button D2, status LED D7.

## 5. Bring-up (from the board README)
1. 12 V adapter in: +12V = 11.9 V, +5V = 5.0 V (current under 40 mA without valve).
2. Force VALVE_G high from the ISP (or hold the button per firmware): the valve switches; check that the flyback diode D7 catches the turn-off spike (no resets).
3. Soil sensors: dry about 520 counts, wet about 260 counts (typical; calibrate).

## 6. Calibrate each sensor
The board has **no serial header**, so the dry/wet counts are changed in the firmware: measure each sensor in dry air and in water (use a bench ADC reading of the signal or a Nano with `release/kheti_mitra.hex` and the 115200 baud serial output), edit `cfg.dry_adc` / `cfg.wet_adc` in `src/main_kheti.cpp`, run `make test` and `make board`, flash. For production, write the calibrated values into EEPROM at the factory (to do).

## 7. End-of-line test (every unit)
1. Current at 12 V idle under 40 mA; valve off.
2. Dry sensors in air: valve opens within 10 s and the status LED blinks code 2; wet sensors in water: valve closes.
3. Rain sensor wet: valve stays closed, LED code 3 (rain hold 12 h).
4. Unplug both soil sensors: LED code 4 (fault); the fallback timer runs 5 min every 12 h.
5. Leave valve forced on: the 20 min limit closes it.
6. Record on `manuals/templates/eol_test_sheet.md`.

## 8. Enclosure, packaging, compliance
Print the shell (section G) or use an IP65 junction box with cable glands; **IP65 claims need a real test**. Pack: unit, adapter, quick start in Hindi/Telugu/English, valve sold separately or in a bundle (about Rs 2,999). Verify: BIS CRS for the adapter, e-waste EPR, Legal Metrology. No safety-critical claims.

## 9. Field trial (required before selling)
60 days, 10 users (terrace gardens, 2 nurseries, 3 small farms), plain timer on matched plots as control; log water, plant health, sensor drift, failures.

## 10. Known limits
Real sensor drift, fouling, rain-sensor false triggers and plant effects are unproven; the water-balance simulation uses one soil and synthetic weather; calibration constants are edited in firmware.
