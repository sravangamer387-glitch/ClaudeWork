# Jal-Rakshak water-tank controller: manufacturing manual

> **Read this first. What can and cannot be manufactured today.**
> - **Can be built today:** the **low-voltage bench prototype** (Arduino Nano + 12 V mini pump + relay module) for demonstrations and field-logic testing. **Never connect mains to it.**
> - **Cannot be manufactured today:** the **mains product**. The mains side (isolated supply, relay/contactor for 0.5-1 HP pumps with 3-5x starting current, fuse, surge protection, creepage/clearance, IP54 housing, installation manual) is **not designed**, and BIS/electrical-safety applicability has not been checked. This repository contains no mains PCB. A qualified electrical-safety engineer must design and review that part and a lab must test it before any sale. This manual refuses to give mains wiring instructions for that reason.

## 1. What the controller does (rules in `firmware/lib/jal_core.c`)
60 s power-return delay; start only when the tank is below LOW and the sump has water; stop at FULL (debounced); dry-run protection (sump probe dry 5 s: stop, retry after 10 min up to 3 times, then latch); 120 s minimum off time; probe-fault detection; run-time limit learned from previous fills (+10 %, 30 min until learned); blink codes 0-5; AC-excited probes (no corrosion). 20 host tests pass with sanitizers (simulated house, power cuts, probe ripple, fault injection).

## 2. Prototype build (about Rs 1,820)
| Item | Notes |
|---|---|
| Arduino Nano clone | flash `products/04-jal-rakshak/release/jal_rakshak.hex` |
| 12 V mini diaphragm pump + 12 V adapter | low voltage only |
| Relay module (opto-isolated, 5 V coil) | drives the pump supply, **flyback diode across the pump** |
| 3 stainless probes (sump, tank LOW, tank FULL) + 1 common electrode | stainless screws on a PVC holder |
| 3 x 100 kohm | sense pin pull-downs |
| Status LED, buzzer, hold/reset button | |
| Bucket(s) as sump and tank, tubing | |

Wiring (from `firmware/src/main_jal.cpp`): common probe electrode driven by **D7**; sense pins **D8 (sump), D9 (tank LOW), D10 (tank FULL)** each pulled to GND with 100 kohm; relay input **D6**; status LED **D13**; buzzer **D12**; reset/clear-fault button **D2** to GND. Probe logic: a probe is wet only if its sense pin follows D7 high **and** low (AC excitation).

Steps: 1. Build on a breadboard or perfboard. 2. Flash the hex with the Nano bootloader (`avrdude -p m328p -c arduino -P <port> -b 57600 -U flash:w:jal_rakshak.hex:i`; some clones need `-b 115200`). 3. Fill the buckets, check each probe by water level; verify the power-return delay (60 s) by cycling power. 4. Run the fault tests: dry the sump (blink code 3), short FULL to LOW (code 4), disconnect FULL (run-time limit, code 5).

## 3. Acceptance test of the prototype
- Pump never starts within 60 s of power return; never restarts within 120 s of a stop.
- Pump stops within 6 s of an impossible probe combination and stays stopped until reset.
- Pump never runs with the sump probe dry.
- Overflow with a dead FULL probe is limited by the learned run-time limit (about 4 % of the tank in the simulation; set the limit to about 1.1 x the real fill time for the installation).

## 4. What must exist before a mains product can be built (not done)
Isolated low-voltage probe side (reinforced insulation), certified isolated supply, relay or contactor sized for motor starting current, fuse, surge protection, PCB creepage/clearance slots, IP54 enclosure with strain relief, installation manual, safety test report, BIS/CRS applicability, e-waste EPR, Legal Metrology. Estimated fixed cost Rs 4-8 lakh (assumption). Designed production BOM Rs 660; price recommendation Rs 1,999-2,199 (at Rs 1,299 it loses money).

## 5. Alternative: low-voltage alarm-only version
A battery-powered alarm (no mains) avoids most of the safety work but competes with Rs 199-400 products.

## 6. Known limits
No real water, probes, motor currents, mains behaviour or EMC tested; hard-water probe fouling unknown; installers must set the run-time limit per tank.
