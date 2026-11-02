# BioWatt MFC energy harvester (BQ25570) (rev A)

BioWatt microbial-fuel-cell energy harvester (44 x 40 mm): TI BQ25570 boost charger with MPPT, buck output, VBAT_OK, megohm setting dividers; one protected Li-ion cell as storage.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 44 x 40 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.0 mm, 2 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 30 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 29 parts, 20 nets.

## Circuit description
- **Harvester:** BQ25570 (SLUSBH2G). VIN_DC from the fuel cell through L1 = 22 uH, CIN 4.7 uF; VOC_SAMP tied to GND = MPPT at 50 % of Voc (the maximum-power point of a source with a linear polarisation curve); VREF_SAMP 10 nF; EN tied to GND (enabled); VOUT_EN tied to VSTOR; NC pins tied to the PowerPAD.
- **Settings (equations from the datasheet, VBIAS 1.21 V):** VBAT_OV 3.95 V (ROV1 5.6 M, ROV2 5.6 M + 1 M); VBAT_OK 3.35 V falling and 3.63 V rising (ROK1 4.3 M, ROK2 5.6 M + 1 M + 1 M, ROK3 1 M); VOUT 3.35 V (ROUT1 4.3 M, ROUT2 5.6 M + 1 M + 1 M). Dividers go from VRDIV to GND.
- **Output:** buck L2 = 10 uH, COUT 22 uF; header with VOUT, GND and the VBAT_OK flag for the sensor tag. Storage: a protected single Li-ion/LiPo cell on VBAT (22 uF) with CSTOR 4.7 uF + CBYP 0.1 uF at VSTOR.

## Power
Harvester quiescent about 0.5 uA (datasheet); output limited by what the fuel cell delivers (see biowatt/docs/budget.md).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [44.1, 40.1] mm, match |

Enclosure (prototype shell for 3D printing, screwed lid): outer 59.2 x 55.2 x 17.0 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | BQ25570RGRR | QFN-20-1EP_3.5x3.5mm_P0.5mm_EP2x2mm | BQ25570RGRR | C506250 | verified |
| J1 | MFC in (+ / -) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S | C131337 | verified |
| J2 | Storage cell (+ / -), protected | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S | C131337 | verified |
| J3 | Tag out (VOUT, GND, VBAT_OK) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S | C131339 | verified |
| L1 | 22u | L_Coilcraft_LPS4018 | Coilcraft LPS4018-223MRC | C5278935 | verified |
| L2 | 10u | L_Changjiang_FNR3015S | ZE ZENR3015T100M | C42427989 | verified |
| C1 | 4.7u | C_0603_1608Metric | Samsung CL10A475KP8NNNC X5R 10V | C1705 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 4.7u | C_0603_1608Metric | Samsung CL10A475KP8NNNC X5R 10V | C1705 | verified |
| C4 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| C5 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| C6 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R3 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | verified |
| R2 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R1 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | verified |
| R4 | 4.3M | R_0603_1608Metric | FH RS-03L4304FT | C136595 | verified |
| R5 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | verified |
| R6 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R7 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R8 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R9 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R10 | 4.3M | R_0603_1608Metric | FH RS-03L4304FT | C136595 | verified |
| R11 | 5.6M | R_0603_1608Metric | FOJAN FRC0603F5604TS | C2933237 | verified |
| R12 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| R13 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. With no cell and no source: nothing to measure; check no shorts VSTOR-GND, VOUT-GND.
2. Fit the protected cell: VSTOR follows the cell, VBAT_OK goes high above about 3.63 V.
3. Feed 0.6-1.0 V from a bench supply through 1 kohm: VSTOR rises (cold start needs VIN of at least 0.6 V).
4. Connect the fuel cell, measure VIN_DC under load: it should settle near half of the open-circuit voltage.
5. Measure VOUT = 3.35 V +-3 %.

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
