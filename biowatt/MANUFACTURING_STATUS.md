# BioWatt MFC harvester: status page (no manufacturing manual yet)

> **Status: concept and energy-budget model only. No PCB is released.** See `biowatt/docs/PCB_BLOCKERS.md` for the exact missing input (harvester IC setpoint resistors from the vendor datasheet).

## What you can do now

- Run `python3 biowatt/sim/budget.py` and replace the assumptions with your own measured MFC data (polarisation sweep).
- Decide the load: a BLE/LoRa sensor tag, not WiFi (see `biowatt/docs/budget.md`).
- Provide the datasheet text so the board can be completed through the normal pipeline.
