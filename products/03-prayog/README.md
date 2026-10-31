# Product 3 · "Prayog" School STEM Lab Kit

A sensor board with 12 plug-in modules and **20 experiments** with worksheets, plus a teacher guide, for schools and tuition labs (B2B). Status: **sensor library, analysis tools and firmware built and tested; hardware not built; syllabus mapping and procurement route unverified.**

## 1. What the kit contains
- **Mother board** (Nano-class MCU, 8 analog sockets, photogate and ultrasonic ports, USB).
- **12 modules:** temperature (NTC), light (LDR), sound level (microphone), magnetic field (Hall), soil moisture (capacitive), voltage probe x2, IR reflective, water conductivity, ultrasonic distance, photogate x2, button + LED reaction pad. Low voltage only (5 V; probes up to 15 V through dividers); no mains.
- **Software:** firmware streams CSV over USB at 115200 baud; Python tools analyse data offline (no cloud, no account).
- **Docs:** `docs/experiments.md` (20 experiments), `docs/validation.md`, `docs/kit_cost.txt`.

## 2. Verification
| What | Result |
|---|---|
| C sensor library (`firmware/lib`, `make test`) | **40 checks pass** with sanitizers: NTC within 0.6 °C over 0–80 °C (limited by the 10-bit ADC), ultrasonic 1 m at 20 °C = 100.0 cm and the temperature correction, photogate period/transit timing, ring-buffer overflow, spike rejection, command parser |
| Analysis tools (`tools/prayog_tools.py`) | **11 of 11 pass**: each analysis recovers the true constant from noisy simulated data (g to 2 %, speed of sound to 2 %, Newton cooling k to 5 %, inverse-square exponent to 4 %, RC time constant to 4 %, resistance to 3 %, dipole exponent to 7 %) and a sanity case correctly refuses to look like inverse-square. |
| Nano firmware | **compiles for ATmega328P: 9.6 KB flash (29 %), 434 B RAM (21 %)**; `release/prayog.hex` |
| Self-corrections during the build | a first Newton-cooling tolerance was ±0.03 on a value of 0.0021 (meaningless); fixed to 5 %. The firmware initially reported only a gate *count*; it now streams timestamped events and the event pipeline is validated. The first plan said 20 experiments but 19 existed; the 20th (ultrasonic tank calibration) was added. |

Limits: the validation uses simulated data (it tests the method, not real sensors); 10 of 20 experiments have a validated analysis, the rest are qualitative; sensor constants (LDR law, Hall sensitivity, soil dry/wet counts) are typical values that the experiments calibrate.

## 3. Economics (B2B price Rs 7,999 + GST, 15 % channel commission, 5 % warranty reserve, Rs 300 shipping)
Designed production BOM is **Rs 2,580** (`tools/kit_cost.py`, about 1,000 kits). At Rs 7,999 the contribution is **Rs 2,337 (34 %)**, **Rs 1,501 (22 %)** if the BOM runs 30 % over, and Rs 1,667 (25 %) on the earlier Rs 3,200 guess. **Do not drop to Rs 5,999** (3 % if costs run over). Fixed launch costs about Rs 4–6 lakh (board design, tooling for the tray, teacher guide, validation; assumption).

## 4. Prototype (Rs 1,790, under Rs 3,000)
Nano clone 400 · breadboard and wires 250 · NTC, LDR, resistors, caps 120 · microphone 120 · Hall sensor and magnets 90 · soil sensor 120 · ultrasonic 100 · IR module 40 · 2 photogates 120 · divider parts and capacitor 100 · steel ball, string, stand 150 · USB cable 80 · household items 100 = **Rs 1,790** (estimates). Build with `firmware/Makefile` (`make hex`), flash `release/prayog.hex`, run the experiments with a laptop.

## 5. Compliance and selling
- Low-voltage educational kit for school use: confirm with BIS/a lab whether kits for children under 14 fall under the toys QCO; label age 12+ and warnings; electronics e-waste/EPR check.
- **Procurement:** about 10,000 Atal Tinkering Labs exist and 50,000 more are planned [S] but I found **no information on how kits are bought**; before building stock, ask 5 schools and one existing lab-kit dealer how they buy (GeM, dealers, direct).
- Teacher guide and worksheets need review by a science teacher; **syllabus mapping is unverified**.

## 6. Not done / next
Board layout and enclosure/tray; teacher guide PDF; student worksheets (the 20 experiment sheets are the text source); real-sensor calibration; pilot in 2 schools; price list; RFQ for PCB assembly (Hyderabad EMS leads in `electronics-toys/phase1-market-and-rules.md`).

## 7. Risks
Long school sales cycle; margin sensitive to BOM; sensor quality variation; teachers' time; competition from existing lab-kit dealers.
