# TRISHNA urinal hydration monitor - controller (ESP32-DevKitC carrier) (rev A)

TRISHNA controller (120 x 84 mm): carrier for an ESP32-DevKitC-32E that runs a reagentless urinal hydration monitor - 12 V input with PTC, TVS and reverse-polarity PMOS; AP63203 3.3 V buck; DRV8871 H-bridge for the reversible peristaltic pump; AO3400A + 1N4007 (M7) for the fresh-water solenoid; bipolar ratiometric EC cell drive; two photodiode TIAs (MCP6002) and two LED drivers; DS18B20, VL53L1X, microSD and UART telemetry.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 120 x 84 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 302 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 88 parts, 56 nets.

## Circuit description
- **Power:** J1 12 V -> F1 2 A PTC -> D3 SMBJ15A -> Q5 AO3401A (reverse polarity, D4 12 V gate clamp) -> VM (100 uF + 10 uF). U2 AP63203 -> +3V3 (4.7 uH, 2 x 22 uF); FB1 + 10 uF/100 nF -> +3V3A for the TIAs. JP1 links +3V3 to the DevKit 3V3 pin: remove it before plugging USB into the DevKit.
- **Actuators:** U3 DRV8871 (IN1 GPIO13 forward, IN2 GPIO12 reverse, ILIM 47 k about 1.4 A) -> J6 pump; Q1 AO3400A (GPIO2) -> J7 solenoid with D10 M7 flyback (cathode to VM).
- **EC:** GPIO25 -> 330 R -> E1 (J10.1); E2 (J10.2) -> 100 R -> GPIO26; node E1 -> 100 R/1 nF -> GPIO36. Balanced bipolar drive; ratio V_A/V_B is independent of the supply.
- **Optics:** Q2/Q3 AO3400A switch the 450 nm / 850 nm LEDs from VM through 1 k (1206); U4 MCP6002 TIAs: transmission 10 k || 10 nF, scatter 1 M || 1 nF -> 1 k/10 nF -> GPIO39 / GPIO34.
- **Probes and buses:** GPIO27 pulses 4.7 k (sump, GPIO32) and 47 k (leak, GPIO33); DS18B20 GPIO4; VL53L1X I2C GPIO21/22; microSD SPI 18/19/23, CS 5; telemetry UART2 GPIO17 TX / GPIO16 RX on J15. **Firmware:** `trishna/firmware` (PlatformIO).

## Power
Idle about 80-120 mA at 12 V with the DevKit (Wi-Fi off); sampling adds the pump (0.2-0.4 A); purge adds the valve (0.3-0.5 A). Use a 12 V 2 A adapter.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [120.1, 84.1] mm, match |

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| J1 | 12 V DC in (2 A) | BarrelJack_CUI_PJ-063AH_Horizontal | CUI/Same Sky PJ-063AH | C22434582 | verified |
| F1 | PTC 2A 16V | Fuse_1812_4532Metric | R+O SMD1812-200-16 (2 A hold) | C46641167 | verified |
| D3 | SMBJ15A | D_SMB | Littelfuse SMBJ15A | C83846 | verified |
| Q5 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| D4 | BZT52C12 | D_SOD-123 | DIODES BZT52C12-7-F | C124196 | verified |
| R40 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C30 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VZH101M1VTR-0607 | C176683 | verified |
| C31 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | verified |
| U2 | AP63203WU-7 | TSOT-23-6 | AP63203WU-7 (3.3 V fixed) | C780769 | verified |
| R41 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| C32 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| L1 | 4.7u | L_Changjiang_FNR5040S | Changjiang FNR5040S4R7MT | C167963 | verified |
| C33 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| C34 | 22u/10V | C_0805_2012Metric | Samsung CL21A226MPQNNNE | C29277 | verified |
| FB1 | BLM18 600R | L_0603_1608Metric | Murata BLM18AG601SN1D | C19330 | verified |
| C36 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| C37 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| D6 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R45 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R60 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R61 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C60 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| J4 | DevKitC left: 3V3 EN 36 39 34 35 32 33 25 26 27 14 12 GND 13 D2 D3 CMD 5V | PinSocket_1x19_P2.54mm_Vertical | BOOMELE 2.54-1*19P female header | C319202 | verified |
| J5 | DevKitC right: GND 23 22 TX RX 21 GND 19 18 5 17 16 4 0 2 15 D1 D0 CLK | PinSocket_1x19_P2.54mm_Vertical | BOOMELE 2.54-1*19P female header | C319202 | verified |
| JP1 | 3V3 link (remove for USB-only power) | PinHeader_1x02_P2.54mm_Vertical | XFCN PZ254V-11-02P + jumper | C492401 | verified |
| C38 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| C39 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| U3 | DRV8871DDAR | HTSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.4x3.2mm | TI DRV8871DDAR | C75864 | verified |
| R62 | 47k | R_0603_1608Metric | UNI-ROYAL 0603WAF4702T5E | C25819 | verified |
| C41 | 10u/50V | C_1210_3225Metric | Samsung CL32A106KBJNNNE | C380537 | verified |
| C42 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C40 | 100u/35V | CP_Elec_6.3x7.7 | Lelon VZH101M1VTR-0607 | C176683 | verified |
| J6 | Peristaltic pump 12 V (red = PUMP_O1) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| Q1 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R63 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R64 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| D10 | M7 (1N4007) | D_SMA | MDD M7 (1N4007, 1 A 1000 V) | C95872 | verified |
| J7 | Solenoid valve 12 V NC | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| Q2 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R65 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R66 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R67 | 1k 1/4W | R_1206_3216Metric | UNI-ROYAL 1206W4F1001T5E | C4410 | verified |
| Q3 | AO3400A | SOT-23 | AO3400A | C20917 | verified |
| R68 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R69 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R70 | 1k 1/4W | R_1206_3216Metric | UNI-ROYAL 1206W4F1001T5E | C4410 | verified |
| J8 | Sensor-block LEDs (450 nm blue, 850 nm IR) | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| U4 | MCP6002T-I/SN | SOIC-8_3.9x4.9mm_P1.27mm | Microchip MCP6002T-I/SN | C7377 | verified |
| R71 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C61 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R72 | 1M | R_0603_1608Metric | UNI-ROYAL 0603WAF1004T5E | C22935 | verified |
| C62 | 1n | C_0603_1608Metric | Samsung CL10B102KB8NNNC X7R 50V | C1588 | verified |
| R73 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C63 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R74 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C64 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| C65 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| J9 | Photodiodes BPW34: transmission, 90-degree scatter (anodes to GND) | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R75 | 330 | R_0603_1608Metric | UNI-ROYAL 0603WAF3300T5E | C23138 | verified |
| R76 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| R77 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| C66 | 1n | C_0603_1608Metric | Samsung CL10B102KB8NNNC X7R 50V | C1588 | verified |
| J10 | EC electrodes (titanium pins E1, E2) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| R78 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R79 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C67 | 1n | C_0603_1608Metric | Samsung CL10B102KB8NNNC X7R 50V | C1588 | verified |
| J11 | Sump stream-detect probe | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| R80 | 47k | R_0603_1608Metric | UNI-ROYAL 0603WAF4702T5E | C25819 | verified |
| R81 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C68 | 1n | C_0603_1608Metric | Samsung CL10B102KB8NNNC X7R 50V | C1588 | verified |
| J12 | Chamber-B floor leak probe | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| J13 | DS18B20 temperature probe | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| R82 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| J14 | VL53L1X ToF presence sensor (I2C) | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R83 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R84 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| J15 | Telemetry UART (ESP32 TX out, RX in) to USB-serial | JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical | JST B3B-PH-K-S(LF)(SN) | C131339 | verified |
| J16 | microSD (SPI log) | microSD_HC_Molex_104031-0811 | Molex 104031-0811 | C585350 | verified |
| R86 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| R87 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| R88 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| R89 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C69 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| C70 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. No DevKit, JP1 out: 12 V current-limited to 150 mA -> under 15 mA, TP2/TP3 = 3.30 V, D6 on; reversed supply draws nothing.
2. Fit JP1 + DevKit, 12 V at 500 mA limit -> 60-120 mA. Flash with JP1 removed and 12 V off (USB only).
3. Console: prime fwd/rev, valve, status, raw - see trishna/MANUFACTURING_MANUAL.md sections 8-9.

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
