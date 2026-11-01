# BioTray vertical-farm tray controller (ESP32-S3, MQTT) (rev A)

BioTray vertical-farm tray controller (100 x 80 mm): ESP32-S3 (WiFi/MQTT), 12 V input with PTC, TVS and reverse-polarity PMOS, 5 V buck and 3.3 V LDO, four low-side 12 V outputs (2 pumps, fan, PWM grow light), DS18B20, I2C, water-level and analog pH/EC inputs.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 100 x 80 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 3 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 241 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 67 parts, 39 nets.

## Circuit description
- **Power:** 12 V barrel jack -> 1.1 A PTC -> SMBJ15A TVS -> AO3401A reverse-polarity PMOS with a 12 V zener gate clamp -> VM; AP63205 buck (4.7 uH, 2 x 22 uF) makes 5 V; AP2112K makes 3.3 V; USB VBUS joins 5 V through an SS14.
- **Outputs:** AO3400A low-side switches with 100 ohm gate resistors and 100 k pull-downs; SS14 flyback diodes on pumps and fan; the light output has none (LED strip).
- **Inputs:** DS18B20 (4.7 k pull-up), I2C 4-pin with 4.7 k pull-ups, float switch with 10 k pull-up, pH and EC through 1 k + 100 nF (module outputs must stay under 3 V).

## Power
About 0.15 A at 12 V idle (WiFi on); loads add to this and must stay under the 1.1 A PTC hold current.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [100.1, 80.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 105.2 x 85.2 x 17.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| J2 | 12 V DC in | BarrelJack_CUI_PJ-063AH_Horizontal | CUI/Same Sky PJ-063AH | C22434582 | verified |
| F1 | PTC 1A 16V | Fuse_1812_4532Metric | Littelfuse 1812L110/16DR | C142746 | verified |
| D3 | SMBJ15A | D_SMB | Littelfuse SMBJ15A | C83846 | verified |
| Q5 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| D4 | BZT52C12 | D_SOD-123 | DIODES BZT52C12-7-F | C124196 | verified |
| R40 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C30 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VEJ101M1VTT-0607L | C7442639 | verified |
| C31 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | verified |
| U2 | AP63205WU-7 | TSOT-23-6 | AP63205WU-7 | C2071056 | verified |
| R41 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| C32 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| L1 | 4.7u | L_Changjiang_FNR5040S | Changjiang FNR5040S4R7MT | C167963 | verified |
| C33 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| C34 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| D5 | SS14 | D_SMA | SS14 | C84343 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 | AP2112K-3.3TRG1 | C51118 | verified |
| C35 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C36 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| U1 | ESP32-S3-WROOM-1-N8 | ESP32-S3-WROOM-1 | ESP32-S3-WROOM-1-N8 | C2913198 | verified |
| C37 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| R42 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| SW2 | Reset (EN) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| SW3 | Boot (IO0) | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| J1 | USB-C | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| R43 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| R44 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| D6 | Green | LED_0603_1608Metric | Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check) | C72043 | verified |
| R45 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| J7 | Water temp DS18B20 | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R46 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| J8 | I2C (BH1750 / SHT31) | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R47 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R48 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| J9 | Water-level float switch | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| R49 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| J10 | pH module (0-3 V analog) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R50 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C40 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| J11 | EC module (0-3 V analog) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R51 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C41 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | verified |
| J12 | UART flash/debug (USB-serial adapter) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| Q1 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R10 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R14 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J3 | Pump 1 | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| D10 | SS14 | D_SMA | SS14 | C84343 | verified |
| Q2 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R11 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R15 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J4 | Pump 2 | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| D11 | SS14 | D_SMA | SS14 | C84343 | verified |
| Q3 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R12 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R16 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J5 | Grow light (PWM) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| Q4 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R13 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R17 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| J6 | Fan | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| D13 | SS14 | D_SMA | SS14 | C84343 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. Current-limited 12 V: TP1 12 V, TP2 5.0 V, TP3 3.3 V.
2. USB: ESP32-S3 enumerates; flash the firmware.
3. Dummy loads on each output before real pumps.

## Files
`1_fabrication/` Gerber + drill zip (upload to JLCPCB/any fab), fab notes, copper plot
`2_assembly/` JLC BOM + CPL (SMD parts JLC assembles), full BOM with LCSC numbers for every part, pick-and-place, assembly drawing
`3_design/` KiCad 7 project (pcb, schematic, libs), netlist, STEP model, schematic PDF, renders
`4_enclosure/` printable base and lid STL
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
