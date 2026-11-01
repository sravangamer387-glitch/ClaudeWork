# BioTray: ESP32-S3 vertical-farm tray controller (WiFi + MQTT)

Programme 2 (bio-electronics), tray controller. **Status: designed, control core host-tested (22 checks), PCB checked in software; nothing built or run on hardware. pH/EC calibration values in the firmware are placeholders.**

## What it does
- Switches two 12 V pumps and a fan (low-side MOSFETs with flyback diodes) and dims a 12 V grow light (PWM).
- Photoperiod with sunrise/sunset ramps; hourly (configurable) irrigation with **dry-run protection** (a missing water signal latches a fault and the pump stays off until cleared by an MQTT command); fan with hysteresis.
- Reads water temperature (DS18B20), ambient light (BH1750 on I2C), a water-level float switch, and pH and EC from off-the-shelf analog modules (0-3 V), with median + EMA filtering and two-point calibration; EC is temperature compensated (2 %/K).
- Publishes a JSON state to MQTT every 30 s (`farm/<tray>/state`); retained `status` last-will.

## Folders
| Path | Content |
|---|---|
| `firmware/lib/bt_core.[ch]` | all control logic (portable C, host-tested) |
| `firmware/test/` | `make test` |
| `firmware/src/` | ESP32-S3 glue skeleton (not compiled) + pin map |
| `docs/` | DESIGN, TEST_PLAN, economics, MQTT topics |
| `hardware/` | release folder of the `biotray` board |
| `MANUFACTURING_MANUAL.md` | build, test, commissioning |

## Honest limits
Not compiled for the ESP32; total 12 V load must stay under the 1.1 A PTC hold current (replace the PTC for bigger loads); no isolation for the pH probe (use an isolated pH module in a shared water tank); water-contact safety, GFCI and enclosure sealing are the installer's responsibility; no WiFi provisioning UI (credentials in `secrets.h`).
