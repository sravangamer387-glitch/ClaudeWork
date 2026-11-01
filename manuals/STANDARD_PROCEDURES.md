# Standard manufacturing procedures (apply to every project in this repository)

Each product has its own `MANUFACTURING_MANUAL.md` that lists *what* to make and the product-specific settings. This file holds the *how* that is shared by all of them. Read it once, then follow the product manual.

**Honest status of everything below:** none of these products has been built, assembled or tested as hardware. The procedures are standard industry practice written for these designs; the numbers (temperatures, settings, sample sizes) are common recommendations that you must confirm against the datasheet or your vendor's current rules. Mark every first batch as a **prototype run** (5 to 10 units) and expect to change something.

---
## A. Ordering bare PCBs (JLCPCB or any fab)

Upload `1_fabrication/<board>_gerbers.zip` from the product's `pcb/release/<board>/` folder. Settings that match what the design was checked against:

| Setting | Value | Why |
|---|---|---|
| Layers | 2 | all boards are two-layer |
| Dimensions | read from the board README (the zip's outline layer defines it) | |
| PCB thickness | 1.6 mm | |
| Copper weight | 1 oz | |
| Surface finish | **HASL lead-free** for the electronics; **ENIG** for the Rain Plate (bare copper electrodes) | ENIG keeps the sensing comb from oxidising |
| Solder mask | any colour (green is cheapest); keep silkscreen white | |
| Min track / spacing | designs use 0.2 mm track and 0.15 mm (some 0.2 mm) clearance: inside standard capability | |
| Min via / hole | 0.6 mm pad, 0.3 mm drill | standard |
| Castellation, impedance, edge plating, gold fingers | none | |
| Remove order number | choose "specify a location" only if you add the marker yourself; otherwise accept the default | |
| Quantity | **5 boards** for the first run | |

After upload, check the fab's own Gerber viewer: outline present, four mounting holes, two fiducials, silkscreen readable. Compare with `3_design/<board>_top.png`.

## B. Ordering SMT assembly (JLCPCB assembly or an Indian EMS)

1. Tick **Assemble top side**. Upload `2_assembly/<board>_JLC_BOM.csv` and `<board>_JLC_CPL.csv`.
2. The BOM already carries LCSC part numbers. Every number was confirmed against an LCSC/JLCPCB listing on 2026-11-01, but **stock changes**: the assembly tool will flag out-of-stock lines, and you must pick a substitute with the same value, package and voltage rating (never a different pinout).
3. **Check the placement preview line by line.** The CPL rotations are generated from the KiCad footprints and have **not** been verified against a real assembly. Pay attention to: ICs (pin 1 dot), diodes, LEDs, tantalum/electrolytic parts, SOT-23 transistors/MOSFETs. Fix rotation in the tool, not by editing the board.
4. Through-hole parts (connectors, headers, buzzer, switches, barrel jack, terminal blocks) are **not** in the JLC BOM: they are listed in `2_assembly/<board>_BOM_full.csv` with a `hand/THT` flag and an LCSC number, so order them from the same cart and hand-solder (section D).
5. Order 5 assembled boards and, in the same cart, 10 extra of each IC so you can rework.

## C. Components: receiving inspection

- Check each reel/bag against the BOM line (value, package, marking).
- Keep ICs in anti-static bags; ATmega328P, STM32, CH340C, OPA356, HX711, TS5A3159 are ESD-sensitive.
- Moisture-sensitive parts (MSL 3 or worse): if the bag is opened for more than the time on the label, bake at 125 C for 8-24 h (check the datasheet) before reflow.
- Keep a **lot log** (template in `templates/lot_log.csv`).

## D. Hand assembly and rework

Tools: temperature-controlled iron (conical or small chisel tip), 0.5 mm solder (60/40 leaded or SAC305), flux pen, tweezers, side cutters, magnifier or microscope, ESD mat and wrist strap, isopropyl alcohol and brush, multimeter.

Order of work (lowest profile first):
1. SMD resistors/capacitors/diodes (if not assembled by the fab): tin one pad, place, reflow the first joint, solder the second.
2. SOT-23 parts, SOIC and QFP/LQFP ICs: align pin 1, tack two opposite corners, then flux and drag-solder the rest. Lead-free: iron about 330-350 C; leaded: about 300-320 C. Never hold the iron on a pad for more than 3-4 s.
3. Crystals, ferrites, polyfuse, TVS diode.
4. Through-hole parts: JST headers, pin headers, USB-C is SMD (the shield tabs are through-hole: solder them), switches, buzzer (mind the + mark), barrel jack or terminal block.
5. Clean flux with IPA. Inspect every joint under magnification: shiny, concave fillets, no bridges.

Rework: for a bridge, add flux and wick. For a lifted pad, stop: scrap the board. For a wrong polarity part, remove it with two irons or hot air at 350 C and replace.

## E. Power-on and electrical tests (do these in this order for every board)

1. **Visual** inspection against the assembly drawing (`2_assembly/<board>_assembly_top.pdf`).
2. **Short test (power off):** multimeter in continuity/resistance across the main supply and ground: not zero ohm. Typical: more than 1 kohm on battery boards.
3. **First power-up with a current-limited bench supply** (set 5 V or the battery voltage, current limit 50 mA; for Kheti-Mitra 12 V at 100 mA). If the current rises quickly, stop and look for a short or a reversed part.
4. Measure the voltages listed in the product's *Bring-up* table (`pcb/release/<board>/README.md`).
5. Flash the firmware (section F) and run the end-of-line test of the product manual.
6. Record every value in the test sheet (`templates/eol_test_sheet.md`). A board with any failed line is tagged and set aside, not reworked more than twice.

## F. Programming (flashing) the firmware

**ATmega328P boards (all utility tools, toys, Prayog, Gas Taraju, Kheti-Mitra, Jal-Rakshak, Arcade, Beat Runner)** use the 6-pin ISP header J2 and a USBasp or Arduino-as-ISP programmer. Pin 1 is marked on the silkscreen (square pad).

```
avrdude -p m328p -c usbasp -U lfuse:w:<LFUSE>:m -U hfuse:w:<HFUSE>:m -U efuse:w:<EFUSE>:m
avrdude -p m328p -c usbasp -U flash:w:<firmware>.hex:i
avrdude -p m328p -c usbasp -U flash:v:<firmware>.hex:i      # verify
```

Fuse values and the correct `.hex` file for each product are in the product manual (battery boards run the internal 8 MHz RC oscillator with a software 4 MHz prescale; USB/5 V boards run 8 MHz internal, Prayog uses the 16 MHz crystal). **Never change the fuses of a board that has a crystal to an internal-oscillator setting while a 3 V supply is applied beyond the speed grade**: the 2 x AAA boards must stay at 4 MHz.

Procedure: power the board (battery in or USB), connect the programmer, run the commands, remove the programmer, power-cycle, confirm the start-up beep or LED pattern described in the product manual.

**STM32G431 (Jal-Netra):** connect an ST-Link V2 to SWD header J3 (SWDIO, SWCLK, GND, 3V3, NRST) and flash the build in `jal-netra/firmware` with `st-flash write <file>.bin 0x08000000` or OpenOCD (`interface/stlink.cfg`, `target/stm32g4x.cfg`). The firmware in this repository is a tested core and a target skeleton: the transmit/receive timing code has **not** been run on hardware.

**Prayog hub:** the ATmega is first given an Arduino-style bootloader over ISP (or flashed directly with the hex); afterwards firmware is uploaded over USB (CH340C enumerates as a serial port, 115200 baud).

## G. 3D-printed enclosures

Files: `4_enclosure/<board>_enclosure_base.stl` and `..._lid.stl` (printed shells sized from the board outline, with standoffs and connector cut-outs generated from the layout).

| Setting | Value |
|---|---|
| Material | PETG (outdoor or kitchen/bathroom use: Rain Alert, Tap Meter, Fridge Guard, Gas Taraju) or PLA for indoor desk items |
| Nozzle / layer | 0.4 mm / 0.2 mm |
| Walls / infill | 3 perimeters / 20 % |
| Supports | none (print base cavity-up and lid flat) |
| Orientation | base open side up; lid outer face down |
| Tolerance check | print one, test-fit the real PCB; adjust the printer's horizontal-expansion setting by up to 0.2 mm if tight |
| Fasteners | M2.5 or M3 self-tapping screws into the standoffs (screw size is in the product manual); 4 mm standoff height |

These shells are prototypes. For production volumes see section I.

## H. Laser-cut parts (MDF / plywood)

Files: `.svg`/`.dxf` in the product's `out/` or `cad/` folder; layers: CUT (through) and ENGRAVE (surface). Units are millimetres, 1:1.

1. Confirm sheet size and thickness with the supplier; **measure the real thickness** with calipers (MDF varies by 0.2-0.5 mm) and adjust slot widths if the manual says so.
2. Kerf allowance: typical CO2 laser kerf is 0.1-0.2 mm; the files already include the kerf stated in the product manual. Cut one test piece and check the fit before the batch.
3. Order of cutting: engrave first, then inner cuts, then outer contour.
4. Clean the char with a damp cloth and fine sandpaper; seal with a water-based lacquer if a finish is required (not food-contact).
5. Mixed batches: keep lots of material together; thickness differences between lots change the fit.

## I. Scaling beyond the prototype

| Step | When | Notes |
|---|---|---|
| Hand assembly with JLC boards | up to ~100 units | what the manuals describe |
| Indian EMS for SMT | ~500+ units per product | send the full `release/<board>/` folder, ask for DFM review, test-jig quote, MOQ, price at 500/1000/2000 |
| Injection-moulded housing | only after ~500 units sell | tool cost typically Rs 1.5-5 lakh per housing (assumption: get quotes) |
| Printed manuals, boxes | any time | Hindi/Telugu/English quick-start card |

## J. Quality assurance

- **100 % tests** on every unit: visual, power-on current, voltage table, firmware flash + verify, product functional test (end-of-line sheet).
- **Sampling:** 1 unit in 50 gets a 24 h burn-in (powered, running, current logged) and a 1 m drop test of the housing; a failure in the sample means holding the lot.
- **Traceability:** write a serial number (batch code + running number) on the board's white label area or on a sticker; keep the lot log and test sheets for 3 years.
- **Calibration** (sensors that need it): follow the product manual; store the result in the test sheet, not only in the unit.

## K. Packaging, labelling and compliance checklist (India)

These are reminders, not legal advice: **verify each item with a certified lab or consultant before selling**.

- Legal Metrology (Packaged Commodities) Rules: pack must show product name, manufacturer's/importer's name and address, net quantity, MRP (incl. taxes), month/year of manufacture, consumer-care contact.
- Toys for children under 14: the Toys (Quality Control) Order and IS 9873 (safety of toys) may apply; electronic toys also need electrical safety testing. Label an age grade and choking-hazard warning for small parts.
- Battery products: state battery type and polarity; keep battery compartments screw-closed on children's toys.
- Electronics sold in India: BIS registration (CRS) applies to some product categories; products powered from an external USB charger should use a BIS-registered adapter. E-waste (Management) Rules: producers have EPR obligations; check thresholds.
- Wireless parts (none in these designs except the optional BLE/UART header on Jal-Netra): WPC equipment type approval if radios are added.
- Gas detector (Gas Taraju) and any safety function: **this repository does not claim a certified safety device**. See that product's manual for the restriction on how it may be described.
- Include a printed quick-start card, a warranty statement and a returns procedure (templates: `templates/quick_start_card.md`).

## L. Troubleshooting (all boards)

| Symptom | Likely cause | Action |
|---|---|---|
| Supply voltage collapses at power-on | short on the board, reversed polarised part, solder bridge | power off, current-limited supply, thermal camera or IPA-evaporation test to find the hot part |
| No programmer response | ISP header rotated, no target power, wrong fuses (e.g. external clock selected without a clock) | check pin 1, check VCC, reflash fuses with a clock applied to XTAL1 |
| Programs but does not run at 3 V | clock set to 8 MHz on a 2 x AAA board | use the 4 MHz hex and fuse values from the product manual |
| Intermittent resets | missing decoupling capacitor, weak battery, brown-out fuse set too high | check C1/C2 next to the MCU, battery voltage under load |
| Display/sensor gives no reading | connector wired the wrong way, pull-up missing | compare connector pin order with the board README |
| USB board not detected | no data lines connected (power-only cable), CH340C driver | try another cable; install the WCH driver on Windows |

---
Templates: `templates/eol_test_sheet.md`, `templates/lot_log.csv`, `templates/quick_start_card.md`.
