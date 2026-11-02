# MITTI-NETRA: low-power cellular soil and structure telemetry node

Programme 1 (AgTech and civil automation). **Status: designed, firmware core host-tested, PCB order-ready (DRC 0, unconnected 0, netlist match, ERC 0, all parts LCSC-verified); nothing has been built, powered, or connected to a mobile network. The cellular modem is a plug-in breakout that you must source and match to the socket.**

## What it is
A solar-charged, deep-sleeping ESP32-S3 node that measures **soil moisture and temperature**, **tilt and vibration** (ADXL345) and **strain** (HX711 + a strain-gauge bridge), decides locally whether a structure is drifting (watch/alarm levels with debounce and hysteresis), and reports a 26-byte CRC-protected frame through a SIMCom SIM7080G (LTE-M / NB-IoT) breakout. An optional Raspberry Pi / Banana Pi companion runs an **edge camera analysis** (canopy cover, greenness) on field photos.

Use cases: field soil moisture for irrigation scheduling; retaining walls, bridges, sheds and boundary walls (tilt/strain drift); landslide-prone slopes (tilt).

## Folders
| Path | Content |
|---|---|
| `firmware/lib/mn_core.[ch]` | soil calibration, tilt, strain conversion, alarm state machine, report scheduler, binary frame + CRC-16 (host-tested) |
| `firmware/test/` | `make test` (23 checks, ASan/UBSan) |
| `firmware/src/` | ESP32-S3 firmware: compiles with 0 warnings (`tools/esp32_build.sh`; binaries in `firmware/release/`), not run on hardware |
| `camera/crop_index.py` | edge vision baseline (ExG canopy cover) with a self-test |
| `docs/` | CONCEPT, DESIGN, TEST_PLAN, economics |
| `hardware/` | release folder of `mitti_netra` (copied from `utility10/pcb/release/`) |
| `MANUFACTURING_MANUAL.md` | build, test, install |

## Honest limits
- The SIM7080G itself is not on the board: a breakout plugs into a 2x3 header (VBAT, GND, UART, PWRKEY, STATUS). Different breakouts use different pins; match yours. No AT-command firmware is included beyond a documented outline; network registration, APN settings and server are yours.
- Strain measurement accuracy depends on bridge wiring, adhesive and temperature compensation, none of which is validated here. The numbers are conversions, not a calibrated instrument.
- The LDO stops regulating when the cell falls below about 3.55 V (about 40 % of capacity left); a buck-boost would use more of the cell.
- The camera analysis is a classical colour baseline, not a trained disease model.
- Use a **protected** Li-ion cell: the board has no cell protection IC (the common DW01 part is flagged not recommended for new designs and has little stock).
