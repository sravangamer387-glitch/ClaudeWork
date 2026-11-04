# TRISHNA - reagentless urinal hydration and biomarker monitor

TRISHNA is a hands-off device for a home male urinal. When someone uses the urinal, it waits 2 s for the first flush to pass, catches a **2 mL mid-stream sample** in a sealed flow cell, and measures it. No reagents or strips are used:
- conductivity
- temperature
- 450 nm colour (absorbance)
- 850 nm turbidity

From these it estimates specific gravity and a hydration class. It then backwashes the cell with tap water and sends every event as a fixed 48-byte binary frame over UART (and to a microSD log), for a local MQTT / ThingsBoard sandbox.

**Start here:** [`MANUFACTURING_MANUAL.md`](MANUFACTURING_MANUAL.md). It covers the specification, the state machine, the electronics, firmware, mechanics and plumbing, the BOM, tools, assembly, bring-up, calibration and the validation protocol.

| What | Where | Status |
|---|---|---|
| Controller PCB (ESP32-DevKitC-32E carrier) | `utility10/pcb/boards/trishna.py` -> `utility10/pcb/release/trishna/`, copy in `hardware/` | see `costing/SIGNOFF.md` |
| Pinout, net list, BOM (generated, cross-checked with the firmware) | [`docs/PINOUT_AND_NETLIST.md`](docs/PINOUT_AND_NETLIST.md) | generated |
| Firmware (PlatformIO, Arduino-ESP32 2.0.17) | `firmware/` | `pio run` builds for the ESP32 (864 kB); `pio test -e native`: 19/19 pass |
| Bridge / calibration / trend tools (Python) | `tools/` | decoder cross-checked against the C frame format |
| Enclosure, 2 mL sensor block, sump insert, brackets (STL) | `mechanical/out/` | solids checked: 2.02 mL wetted chamber, all meshes closed, fit a 220 mm bed |
| Drawings: plumbing schematic, wall elevation, harness, sensor block | `docs/drawings/` | |

**Limits:** this is a wellness / trend prototype, **not a medical device**. The SG value is an estimate that must be fitted to your own refractometer readings. Nothing has been built yet: follow the leak test and the validation protocol (manual section 10) before trusting a single reading.
