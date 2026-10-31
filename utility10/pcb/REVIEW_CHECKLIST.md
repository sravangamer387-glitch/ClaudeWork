# Engineer sign-off checklist (one per board, tick before ordering)

The software already checked: electrical rules on the netlist, symbol-to-footprint pin match, KiCad DRC, schematic-vs-PCB netlist equality, SPICE for the analog stages. **None of that replaces a person looking at the design.** A competent electronics engineer needs about half a day per board.

## Schematic
- [ ] Every part's datasheet pinout matches the symbol (especially MCP6001 pin order, AO3401A, USB-C CC pins, JST/headers pin 1).
- [ ] Supply ranges: 2 x AAA board stays within the ATmega328P speed grade at every battery voltage (4 MHz below 2.7 V); brown-out fuse chosen on purpose.
- [ ] Reverse-polarity PMOS (AO3401A): Vgs(th) vs lowest battery voltage; body diode direction; gate to GND is correct for this topology.
- [ ] Analog front end (Seeti): re-run `sim/seeti_amp.cir` with the real capsule model; check noise, mic bias current, input clipping with your whistle recordings.
- [ ] Rain: pull-down and series resistors vs your plate resistance range; TVS standoff voltage (5 V) vs the 5 V rail; leakage of TVS at the sense node (nA) is negligible against 100 k.
- [ ] Bijli: USB-C CC resistors 5.1 k (sink), VBUS TVS clamp vs MCU absolute maximum, PTC hold current vs load.
- [ ] Unused MCU pins: decide pull-ups/outputs in firmware (the schematic marks them not connected).

## Layout
- [ ] Decoupling capacitors adjacent to the MCU VCC/AVCC pins and the op-amp supply pin, with short returns.
- [ ] Analog input trace away from digital/buzzer traces; ground pour continuity under the amplifier.
- [ ] Antenna-like loops: none (low-frequency design) but check the buzzer driver return path.
- [ ] Mounting holes match the enclosure; connectors align with the cut-outs; USB-C shell clearance.
- [ ] Silkscreen readable, polarity marks correct, pin-1 marks, test point labels.
- [ ] Gerber review in a viewer (KiCad GerbView or the fab house's viewer): copper, mask openings (rain plate comb fully open), drill file.

## Manufacturing
- [ ] Upload the Gerber zip to the fab's online DFM; fix anything it flags.
- [ ] BOM: confirm every LCSC number marked "memory" in `*_BOM_full.csv` on lcsc.com (stock, package, value); parts marked "verified" were confirmed by search on 2026-10-31/11-01 but stock changes daily.
- [ ] CPL rotation/position corrections in the fab's assembly preview (SOT-23, TQFP pin-1 orientation).
- [ ] Order 5 boards first; build one fully, run the bring-up steps in the board README, then release the rest.

## Firmware
- [ ] Fuse settings from the board README; clock prescaler (Seeti 4 MHz); ADC prescaler; sampling timing for Seeti (use a timer-triggered ADC for jitter-free 8 kHz sampling in production firmware; the demo uses software timing).
- [ ] Rain: sleep current measured (target < 50 uA average); Seeti/Bijli thresholds calibrated on real devices.
