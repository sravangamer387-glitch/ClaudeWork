# Seeti Counter - main board (rev B)

Clip-on pressure-cooker whistle counter: electret microphone, band-pass amplifier, ATmega328P-AU, buzzer, LED, 2 x AAA.

**Status: engineering release, software-verified only (ERC on the netlist, KiCad DRC, netlist cross-check, SPICE where noted). Not yet built, not reviewed by a second engineer, not certified.**

## Specification
- Board 64 x 44 mm, 2 layers, 1.6 mm FR-4, 1 oz copper, rounded corners R2.5 mm, 4 x M2.5 mounting holes, 2 fiducials.
- Rules used: min track 0.2 mm (power 0.4 mm), min clearance 0.2 mm, via 0.6/0.3 mm, GND pour on both layers, 54 stitching vias.
- Finish: ENIG recommended (HASL lead-free acceptable); green mask, white silk; IPC class 2.
- 36 parts, 24 nets.

## Circuit description
- **Power:** 2 x AAA (3.0 V fresh, about 2.0 V end of life) -> slide switch SW1 -> AO3401A P-MOSFET Q2 (drain = battery side, source = load, gate = GND) = reverse-battery protection with about 50 mV drop. **Clock:** the ATmega328P is specified for 8 MHz only at 2.7 V and above (1.8 V is allowed up to 4 MHz), and two AAA cells fall below 2.7 V about half-way through their life, so the firmware must switch to 4 MHz at boot (`clock_prescale_set(clock_div_2)`, F_CPU = 4 MHz; ADC clock and the 8 kHz audio sampling still work). Check the speed-grade graph in the current datasheet.
- **Microphone amplifier:** electret capsule biased through R1 2.2 k; AC-coupled (C5 1 uF) into an MCP6001 (rail-to-rail, 1 MHz GBW) non-inverting stage biased at VCC/2 (R2/R3 100 k + C7 10 uF so the feedback return is low impedance). Gain 1 + R8/R9 = 1 + 33k/1k = 34 (SPICE 32.9x at 2.8 kHz); C6 220 nF in the feedback return gives a high-pass at 1/(2 pi R9 C6) = 720 Hz which rejects 100 Hz mains hum and cooking noise before the whistle tone (about 2.8 kHz, to be measured). The amplifier stays flat to about 26 kHz, so **R10 1k + C9 22 nF form a 7.2 kHz first-order anti-alias filter** in front of the ADC; with 16 kS/s sampling this is only a mild filter (about 8 dB at 16 kHz): a known limitation.
- **Digital:** ADC0 reads the amplifier; buzzer through MMBT3904 with flyback diode; button on PD2, LED on PD7; ISP header and a 4-pin UART header (115200 baud debug); reset pulled up by 10 k.

### Simulation: `sim/seeti_amp_results.txt`
```
Closed-loop small-signal response of the Seeti microphone amplifier (Rf = 33k, Rg = 1k, Cg = 220 nF, ideal capsule current source into R1 = 2.2k; MCP6001-class op-amp macro model, GBW 1 MHz) followed by the anti-alias filter R10 1k / C9 22n (-3 dB at 7.2 kHz):
gain at 30 Hz        = 4.4 dB
gain at 1 kHz         = 28.7 dB
gain at 2.8 kHz at amplifier output = 30.4 dB (32.9x); at the ADC pin = 29.7 dB
amplifier -3 dB band  = 700 Hz ... 26.1 kHz (relative to the 30.3 dB passband)
at the ADC pin: 8 kHz = 26.9 dB, 12 kHz = 24.1 dB, 16 kHz = 21.5 dB (relative to 0 dB input)
Production firmware should sample at 16 kS/s (Nyquist 8 kHz): the filter then removes about 8 dB of anything near 16 kHz relative to the 2.8 kHz whistle band. The 8 kS/s demo firmware has little anti-aliasing and relies on the narrow Goertzel bin.
```

### Simulation: `sim/seeti_headroom.txt`
```
Closed-loop gain at 2.8 kHz: 32.8x
VCC 3.0 V: output can swing +/-1.47 V around VMID -> undistorted mic input up to 45 mV peak; a 3 mV peak whistle gives 98 mV peak = 34 ADC counts peak
VCC 2.0 V: output can swing +/-0.97 V around VMID -> undistorted mic input up to 30 mV peak; a 3 mV peak whistle gives 98 mV peak = 50 ADC counts peak
```

## Power
Run current estimate: MCU at 4 MHz and 3 V about 2 mA, amplifier 0.1 mA, microphone bias up to 0.5 mA, LED 1 mA when lit: about 3.6 mA -> 2 x AAA (about 1000 mAh to 2.0 V) gives roughly 250 h of cooking time (estimate, not measured). Add sleep modes in firmware if the unit will stay switched on.

## Verification
| Check | Result |
|---|---|
| Electrical rule check on the netlist (own ERC: unconnected pins, single-pin nets, output conflicts, unpowered supplies, symbol/footprint pin match) | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings; unconnected pads: 0 |
| Schematic netlist equals PCB netlist | yes |
| Router failures | 0 |
| 3D STEP export | yes |
| Independent Gerber parse (gerbonara): layers parsed, outline size equals the design | 9 layers, outline [64.1, 44.1] mm, match |

Enclosure (prototype shell for 3D printing): outer 69.2 x 49.2 x 20.6 mm, collision/opening check: pass

## Bill of materials
| Ref | Value | Footprint | Manufacturer part | LCSC # | LCSC status |
|---|---|---|---|---|---|
| U1 | ATmega328P-AU | TQFP-32_7x7mm_P0.8mm | ATMEGA328P-AU | C14877 | verified |
| U2 | MCP6001 | SOT-23-5 | MCP6001T-I/OT | C116490 | verified |
| J1 | BATT 2xAAA | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| SW1 | Power | SW_SPDT_PCM12 |  |  |  |
| Q2 | AO3401A | SOT-23 | AO3401A | C15127 | verified |
| J2 | ISP | PinHeader_2x03_P2.54mm_Vertical |  |  |  |
| J3 | MIC electret | JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical |  |  |  |
| J4 | UART | PinHeader_1x04_P2.54mm_Vertical |  |  |  |
| BZ1 | Buzzer 3V | Buzzer_12x9.5RM7.6 |  |  |  |
| Q1 | MMBT3904 | SOT-23 | MMBT3904 | C20526 | verified |
| D2 | 1N4148WS | D_SOD-323 | 1N4148WS | C2128 | verified |
| SW2 | Target | SW_SPST_B3U-1000P |  |  |  |
| D1 | Green | LED_0603_1608Metric |  |  |  |
| R1 | 2.2k | R_0603_1608Metric | 0603 2.2k 1% | C4190 | memory |
| R2 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | memory |
| R3 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | memory |
| R4 | 100k | R_0603_1608Metric | 0603 100k 1% | C25803 | memory |
| R5 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R6 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| R7 | 10k | R_0603_1608Metric | 0603 10k 1% | C25804 | memory |
| R8 | 33k | R_0603_1608Metric |  |  |  |
| R9 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| C1 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C2 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C3 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| C4 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C5 | 1u | C_0603_1608Metric | 0603 1uF X7R | C15849 | memory |
| C6 | 220n | C_0603_1608Metric |  |  |  |
| C7 | 10u | C_0805_2012Metric | 0805 10uF X5R | C15850 | memory |
| C8 | 100n | C_0603_1608Metric | 0603 100nF X7R | C14663 | memory |
| R10 | 1k | R_0603_1608Metric | 0603 1k 1% | C21190 | memory |
| C9 | 22n | C_0603_1608Metric |  |  |  |
| TP1 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP2 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP3 | TP | TestPoint_Pad_D1.5mm |  |  |  |
| TP4 | TP | TestPoint_Pad_D1.5mm |  |  |  |

`verified` = LCSC number confirmed by web search on 2026-10-31/11-01; `memory` = from my recollection, **check on lcsc.com before ordering**; empty = no number chosen (through-hole connectors, switches, buzzer, test points: hand-assembled or chosen by the buyer). `*_JLC_BOM.csv` / `*_JLC_CPL.csv` list only the parts with an LCSC number; JLCPCB rotation corrections (CPL) must be checked in their viewer.

## Assembly notes
- Reflow (JLCPCB SMT): all SMD parts with an LCSC number. Hand-solder: JST connectors, pin headers, buzzer, switches, test points as listed in the BOM. Fiducials and mounting holes are in the Gerbers.
- Polarity: LED cathode toward GND (silk marks), electrolytic none, diode D2 cathode to +V, Q2 orientation as footprint (SOT-23 pin 1 = gate).
- Programming: ISP header J2 (pin 1 = MISO, square pad). Flash `../../../firmware/release/*.hex` built for 8 MHz (`make hex` with F_CPU=8000000).

## Bring-up and test
1. Insert 2 x AAA with switch OFF; measure BAT_P to GND (J1 pins) = 2.8-3.2 V.
2. Switch ON: TP1 (+3V0) = battery minus about 0.05 V; no heating.
3. VMID (R2/R3 junction) = VCC/2 +-0.05 V; TP3 (MIC_OUT) = VCC/2 +-0.1 V with no sound (same DC at the ADC pin through R10).
4. Flash firmware over ISP (J2): `avrdude -p m328p -c usbasp -U lfuse:w:0xE2:m -U hfuse:w:0xD9:m -U efuse:w:0xFE:m` (internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz).
5. Play a 2.8 kHz tone from a phone at 10 cm: TP3 swings about +-100 mV peak and the firmware counts whistles.

## Files
`seeti_counter.kicad_pcb/.kicad_sch/.kicad_pro` (KiCad 7), `gerbers/` (Gerber X2 + drill, zip), `seeti_counter_JLC_BOM.csv`, `seeti_counter_JLC_CPL.csv`, `seeti_counter_BOM_full.csv`, `seeti_counter.step`, `seeti_counter_schematic.pdf`, `seeti_counter_assembly_top.pdf`, `seeti_counter_copper.pdf`, `seeti_counter_enclosure_base.stl/_lid.stl`.

## Known limits and review checklist
- Layout was produced by a custom router and software placement; a human layout review (analog routing, ground returns, creepage, connector mechanics, silkscreen) is still required.
- Not verified: EMC, ESD (apart from TVS parts where fitted), thermal, real component tolerances, supplier stock/price, assembly house design-for-manufacture check (run JLCPCB's DFM check on the Gerbers).
- Firmware thresholds are placeholders to be calibrated on prototypes.
