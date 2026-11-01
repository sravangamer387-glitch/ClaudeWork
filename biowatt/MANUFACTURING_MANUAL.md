# BioWatt MFC energy-harvester board: manufacturing manual

> **Status: design only; nothing built or tested with a real fuel cell.** PCB: **order-ready: every automatic check passes**. Setting resistors derived from the TI BQ25570 datasheet equations (SLUSBH2G).

## 1. What is made

A 44 x 40 mm board: BQ25570 harvester (boost charger with MPPT at 50 % of Voc, nano-power buck) from a microbial fuel cell input (J1) into a protected single Li-ion/LiPo cell (J2), with a regulated 3.35 V output and a VBAT_OK flag on J3. Thirteen 1 % megohm resistors set VBAT_OV 3.95 V, VBAT_OK 3.35 V falling / 3.63 V rising and VOUT 3.35 V; the region around them has no ground pour.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB | `utility10/pcb/release/biowatt/` and `biowatt/hardware/biowatt/` | **order-ready: every automatic check passes** |
| Energy budget model | `biowatt/sim/budget.py`, `biowatt/docs/budget.md` | assumption-based |

## 3. Bill of materials

| Ref | Value | Package | Part (manufacturer) | LCSC | Assembly |
|---|---|---|---|---|---|
| U1 | BQ25570RGRR | QFN-20-1EP_3.5x3.5mm_P0.5mm_EP2x2mm | BQ25570RGRR | C506250 | SMT (JLC) |
| J1 | MFC in (+ / -) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S | C131337 | hand/THT |
| J2 | Storage cell (+ / -), protected | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S | C131337 | hand/THT |
| J3 | Tag out (VOUT, GND, VBAT_OK) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S | C131339 | hand/THT |
| L1 | 22u | L_Coilcraft_LPS4018 | Coilcraft LPS4018-223MRC | C5278935 | SMT (JLC) |
| L2 | 10u | L_Changjiang_FNR3015S | ZE ZENR3015T100M | C42427989 | SMT (JLC) |
| C1 | 4.7u | C_0603_1608Metric | Samsung CL10A475KP8NNNC X5R 10V | C1705 | SMT (JLC) |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | SMT (JLC) |
| C3 | 4.7u | C_0603_1608Metric | Samsung CL10A475KP8NNNC X5R 10V | C1705 | SMT (JLC) |
| C4 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| C5 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | SMT (JLC) |
| C6 | 10n | C_0603_1608Metric | 0603 10nF X7R | C57112 | SMT (JLC) |
| R3 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | SMT (JLC) |
| R2 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R1 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | SMT (JLC) |
| R4 | 4.3M | R_0603_1608Metric | FH RS-03L4304FT | C136595 | SMT (JLC) |
| R5 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | SMT (JLC) |
| R6 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R7 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R8 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R9 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R10 | 4.3M | R_0603_1608Metric | FH RS-03L4304FT | C136595 | SMT (JLC) |
| R11 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | SMT (JLC) |
| R12 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |
| R13 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | SMT (JLC) |

### Bought-in

Protected single Li-ion/LiPo cell (3.7 V) with JST-PH 2 lead; MFC with JST-PH 2 lead; load tag on J3 (BLE/LoRa class: average current well under 1 mA).

## 4. Make the board

1. Upload `utility10/pcb/release/biowatt/1_fabrication/biowatt_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; 1 oz is fine). 2. For assembly upload `2_assembly/biowatt_JLC_BOM.csv` and `biowatt_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.
The megohm resistors are 0603 1 % parts (5.6 M, 4.3 M, 1 M): check the CPL preview and clean flux residue thoroughly afterwards, then keep the board dry.

## 5. Commissioning

1. Bench supply 0.8 V, current-limited 5 mA, on J1: with no cell fitted VSTOR (TP2) rises. 2. Fit a protected cell: VBAT_OK goes high above about 3.63 V and drops below 3.35 V. 3. VOUT (TP3) reads 3.35 V. 4. Then connect the MFC.

## 6. Limits

Cold start needs VIN of at least 600 mV: a single MFC (0.5-0.7 V) is marginal, use two in series or a start-up source. C6 is a stocked X7R 10 nF where the datasheet asks for a low-leakage part. MFC power (about 20 uW) supports only a BLE/LoRa tag. Not tested on hardware.
