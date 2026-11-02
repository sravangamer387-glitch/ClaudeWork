# Jal-Netra ultrasonic flow main board (rev A)

Jal-Netra main board: STM32G431 transit-time measurement (bridge-driven piezo, input mux, two-stage low-noise receive chain, gain select, 12-bit 4 MS/s ADC), USB-C powered, OLED/UART/SWD.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 86 x 66 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.15 mm, via 0.6/0.3 mm, GND pour on both layers, 128 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 78 parts, 51 nets.

## Circuit description
- **Transmit:** TIM3 channels on PA6/PA4 (transducer A) and PB0/PB1 (transducer B) generate a 6-cycle 1 MHz burst; the second pin of each pair is inverted for bridge drive (6.6 Vpp). 22 ohm series resistors protect the pins; on receive one leg is held low by its timer pin and the other is high-impedance.
- **Receive:** 10 nF + 1 k tap from the transducer's high leg, BAV99 clamp to the rails, TS5A3159 selects transducer A or B into LNA1 (OPA356, x10.2) and LNA2 (x10.2); TS5A3159 U7 selects 20 dB or 40 dB into a 33 ohm / 22 pF filter and ADC1 (PA0). Mid-supply bias 1.65 V from AVDD (ferrite-filtered 3.3 V).
- **Rest:** STM32G431CBT6 with 8 MHz crystal, SWD header, boot0 pull-down, USB-C power-only (5.1 k CC, PTC, TVS), AP2112K-3.3, OLED and UART headers, buzzer, LED, test button, test points on the receive chain.

### Simulation: `../../jal-netra/sim/lna_results.txt`
```
SPICE (ngspice) of the receive chain, source impedance 270 ohm (piezo at 1 MHz), OPA356-class model (A0 1e5, GBW 200 MHz):
stage 1 gain at 1 MHz        = 20.1 dB (target 20 dB)
stage 1 + 2 gain at 1 MHz   = 40.9 dB (target 40 dB)
stage 1 upper -3 dB          = 20 MHz
stage 1 + 2 band (-3 dB)      = 1.5 kHz ... 14 MHz
```

## Power
MCU 170 MHz about 35 mA while measuring (0.5 s per measurement), LNAs 2 x 8 mA: USB powered only (about 0.1 W average with a 10 s idle period).

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [86.1, 66.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 91.2 x 71.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | STM32G431CBT6 | LQFP-48_7x7mm_P0.5mm | STM32G431CBT6 (LQFP-48) | C529355 | verified |
| U4 | TS5A3159 | SOT-363_SC-70-6 | TI TS5A3159DCKR | C46388 | verified |
| U5 | OPA356 | SOT-23-5 | TI OPA356AIDBVR | C183100 | verified |
| U6 | OPA356 | SOT-23-5 | TI OPA356AIDBVR | C183100 | verified |
| U7 | TS5A3159 | SOT-363_SC-70-6 | TI TS5A3159DCKR | C46388 | verified |
| U3 | AP2112K-3.3 | SOT-23-5 | Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link) | C51118 | verified |
| FB1 | BLM18 600R | L_0603_1608Metric | Murata BLM18AG601SN1D | C19330 | verified |
| Y1 | 8 MHz | Crystal_SMD_3225-4Pin_3.2x2.5mm | YXC X32258MOB4SI 8 MHz 12 pF 3225 (matches the 15 pF load caps) | C2682775 | verified |
| D5 | BAV99 | SOT-23 | JSCJ BAV99 | C68983 | verified |
| D6 | BAV99 | SOT-23 | JSCJ BAV99 | C68983 | verified |
| J6 | Transducer A (BTL) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| J7 | Transducer B (BTL) | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical | JST B2B-PH-K-S(LF)(SN) | C131337 | verified |
| R30 | 22 | R_0603_1608Metric | UNI-ROYAL 0603WAF220JT5E | C23345 | verified |
| R31 | 22 | R_0603_1608Metric | UNI-ROYAL 0603WAF220JT5E | C23345 | verified |
| R32 | 22 | R_0603_1608Metric | UNI-ROYAL 0603WAF220JT5E | C23345 | verified |
| R33 | 22 | R_0603_1608Metric | UNI-ROYAL 0603WAF220JT5E | C23345 | verified |
| C20 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R35 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C21 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R36 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| C22 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C23 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C24 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C25 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| R10 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| R11 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C27 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C28 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R12 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R13 | 2.2k | R_0603_1608Metric | 0603 2.2k 1% | C4190 | verified |
| R14 | 240 | R_0603_1608Metric | UNI-ROYAL 0603WAF2400T5E (JLCPCB listing) | C23350 | verified |
| C29 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| R15 | 0 | R_0603_1608Metric | UNI-ROYAL 0603WAF0000T5E | C21189 | verified |
| C30 | 10n | C_0603_1608Metric | Samsung CL10B103KB8NNNC 0603 10nF X7R 50V | C1589 | verified |
| R16 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | verified |
| R17 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| R18 | 100 | R_0603_1608Metric | UNI-ROYAL 0603WAF1000T5E | C22775 | verified |
| C31 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| R19 | 0 | R_0603_1608Metric | UNI-ROYAL 0603WAF0000T5E | C21189 | verified |
| R20 | 33 | R_0603_1608Metric | UNI-ROYAL 0603WAF330JT5E | C23140 | verified |
| C32 | 22p | C_0603_1608Metric | Samsung CL10C220JB8NNNC C0G | C1653 | verified |
| C1 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C2 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C3 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C4 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C33 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C34 | 4.7u | C_0603_1608Metric | Samsung CL10A475KP8NNNC X5R 10V | C1705 | verified |
| C35 | 15p | C_0603_1608Metric | Samsung CL10C150JB8NNNC C0G | C1644 | verified |
| C36 | 15p | C_0603_1608Metric | Samsung CL10C150JB8NNNC C0G | C1644 | verified |
| R21 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| R22 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | verified |
| C37 | 100n | C_0603_1608Metric | Samsung CL10B104KB8NNNC 0603 100nF X7R 50V | C1591 | verified |
| C38 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| C39 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | verified |
| J4 | OLED I2C | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| R23 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| R24 | 4.7k | R_0603_1608Metric | 0603 4.7k 1% | C23162 | verified |
| J5 | UART host / BLE | JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical | JST B4B-PH-K-S(LF)(SN) | C131334 | verified |
| J3 | SWD | PinHeader_2x03_P2.54mm_Vertical | ZHOURI 2.54-2*3 | C5116479 | verified |
| SW2 | Test / zero | SW_SPST_B3U-1000P | Omron B3U-1000P | C231329 | verified |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP5 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP6 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| J1 | USB-C 5V | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TYPE-C-31-M-12 | C165948 | verified |
| F1 | PTC 500mA | Fuse_1206_3216Metric | Littelfuse 1206L050YR (6 V) | C163512 | verified |
| D3 | SMAJ5.0A | D_SMA | Littelfuse SMAJ5.0A | C83329 | verified |
| R1 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| R2 | 5.1k | R_0603_1608Metric | 0603 5.1k 1% | C23186 | verified |
| C5 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | verified |
| BZ1 | Buzzer | Buzzer_12x9.5RM7.6 | YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz) | C781869 | verified |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| R7 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |
| D1 | Green | LED_0603_1608Metric | Hubei KENTO KT-0603YG yellow-green 570 nm, Vf about 2 V (lights well from 3.3 V with 1 k; the Everlight 19-217 green was out of stock) | C2289 | verified |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | verified |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash the matching image from `utility10/firmware/release/`: Seeti Counter `4MHz/seeti_prod.hex` (production firmware: timer-triggered 16 kS/s ADC, scan mode to find the real whistle frequency, battery check), Rain Alert `8MHz/rain_alert.hex`, Bijli Meter Reader `8MHz/bijli_meter.hex` (demo-grade firmware, to be hardened).

## Bring-up and test
1. USB-C 5 V: +3V3 = 3.3 V, AVDD = 3.28 V, VMID = 1.64 V.
2. Flash over SWD; with the spool dry nothing should be received (amplitude near zero); fill with water: a burst of amplitude A appears at ADC_IN 40.5 us after the transmit edge (TP5).
3. Follow `jal-netra/docs/TEST_PLAN.md` gates 1-3.

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
