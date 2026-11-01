# BioWatt: microbial-fuel-cell (MFC) energy-harvesting power board

Programme 2 (bio-electronics), harvester. **Status: board designed and order-ready (DRC 0, unconnected 0, netlist match, ERC 0, all parts LCSC-verified). Not built or tested on hardware.** Values are derived from the TI BQ25570 datasheet (SLUSBH2G) equations: VBAT_OV 3.95 V, VBAT_OK 3.35 V falling / 3.63 V rising, VOUT 3.35 V, MPPT 50 % of Voc.

## Intended design
Harvester IC with maximum-power-point tracking (candidates available on LCSC: **TI BQ25570 `C506250`** with boost charger + nano-power buck, or **ST SPV1050 `C5181469`**; the TI BQ25504 is the usual choice but is not stocked at LCSC) -> storage element (small Li cell or supercapacitor) -> 3.3 V rail for a low-power sensor tag. A cold-start threshold of a few hundred millivolts is the main compatibility question for a single 0.5-0.7 V MFC.

## What exists
| File | Content |
|---|---|
| `sim/budget.py` -> `docs/budget.md` | assumption-based energy budget: harvested joules per day vs. what a WiFi, BLE or LoRa node needs |
| `docs/CONCEPT.md` | use cases and limits |
| `hardware/biowatt/` | release package: Gerbers, JLC BOM/CPL, schematic PDF, fab/assembly PDFs, enclosure STLs, DRC/ERC reports, screenshots |
| `MANUFACTURING_STATUS.md` | ordering and bring-up notes |

## Key finding from the model
One small soil MFC (about 20 uW at the maximum power point) yields about 1 J per day after the harvester: a WiFi ESP32 report costs about 2 J, and even deep sleep costs about 3 J per day. So **MFC power can run only a BLE/LoRa-class sensor tag, or trickle-charge a backup cell; it cannot run BioTray**, which needs watts. A 4-cell series stack (about 0.5 mW) supports around ten WiFi reports a day.

## Limits (honest)
- Cold start of the BQ25570 needs VIN >= 600 mV: a single 0.5-0.7 V MFC is marginal; plan a two-cell series MFC or a start-up source and verify on a real cell.
- C6 (VREF_SAMP hold capacitor) is a stocked X7R 10 nF; the datasheet asks for a low-leakage part (C0G/film). Swap it if the MPPT sample drifts.
- Setting dividers are megohm-level: clean flux residue, keep the board dry, use a PROTECTED single Li-ion/LiPo cell.
- Parts are LCSC search results of 2026-11-01, not live stock checks. BQ25504 is not stocked at LCSC.
