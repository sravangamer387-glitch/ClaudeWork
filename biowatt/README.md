# BioWatt: microbial-fuel-cell (MFC) energy-harvesting power board

Programme 2 (bio-electronics), harvester. **Status: concept, energy-budget model and parts research only. NO PCB is released. The harvester IC's setpoint resistors could not be derived because the vendor datasheet was not reachable from the build environment (ti.com, st.com, mouser.com all failed DNS), and I will not guess analog thresholds that protect a battery.**

## Intended design
Harvester IC with maximum-power-point tracking (candidates available on LCSC: **TI BQ25570 `C506250`** with boost charger + nano-power buck, or **ST SPV1050 `C5181469`**; the TI BQ25504 is the usual choice but is not stocked at LCSC) -> storage element (small Li cell or supercapacitor) -> 3.3 V rail for a low-power sensor tag. A cold-start threshold of a few hundred millivolts is the main compatibility question for a single 0.5-0.7 V MFC.

## What exists
| File | Content |
|---|---|
| `sim/budget.py` -> `docs/budget.md` | assumption-based energy budget: harvested joules per day vs. what a WiFi, BLE or LoRa node needs |
| `docs/CONCEPT.md` | use cases and limits |
| `docs/PCB_BLOCKERS.md` | the exact items needed to release the board and how to unblock them |

## Key finding from the model
One small soil MFC (about 20 uW at the maximum power point) yields about 1 J per day after the harvester: a WiFi ESP32 report costs about 2 J, and even deep sleep costs about 3 J per day. So **MFC power can run only a BLE/LoRa-class sensor tag, or trickle-charge a backup cell; it cannot run BioTray**, which needs watts. A 4-cell series stack (about 0.5 mW) supports around ten WiFi reports a day.

## To finish this board
See `docs/PCB_BLOCKERS.md`: supply the BQ25570 (or SPV1050) datasheet text or allow the host, then the resistor set, layout and release follow the same pipeline as the other boards (about half a day).
