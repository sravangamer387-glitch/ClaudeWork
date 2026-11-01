# MITTI-NETRA soil and structure telemetry node: manufacturing manual

> **Status: design only; nothing built or connected to a mobile network.** PCB: **PCB not released yet: do not send to a fab**. The cellular modem is a plug-in SIM7080G breakout (not on the board). Firmware core host-tested; ESP32 glue syntax-checked only.

## 1. What is made

A 90 x 72 mm solar/USB-charged node: ESP32-S3, TP4056 charger for one protected Li-ion cell, 3.3 V LDO, switched socket for a SIM7080G breakout, ADXL345 tilt/vibration, HX711 strain bridge input, capacitive soil probe input, DS18B20 input. An optional Raspberry Pi/Banana Pi runs `camera/crop_index.py`.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB | `utility10/pcb/release/mitti/` and `mitti-netra/hardware/` | **PCB not released yet: do not send to a fab** |
| Core library and tests | `mitti-netra/firmware/lib/mn_core.[ch]`, `test/test_mn.c` | `make test` passes (23 checks) |
| ESP32 skeleton | `mitti-netra/firmware/src/` | syntax-checked only; cellular send is a TODO |
| Camera analysis | `mitti-netra/camera/crop_index.py` | self-test passes on synthetic scenes |

### Bought-in

SIM7080G (LTE-M/NB-IoT) breakout board with nano-SIM holder and antenna; protected 18650 cell (or protected pouch cell) with JST-PH 2 lead; 5-6 V solar panel (2 W) with JST-PH 2 lead; capacitive soil moisture probe (3.3 V, analog) with JST-PH 3 lead; DS18B20 waterproof probe; strain gauges (350 ohm, GF about 2) with bridge completion; IP65 enclosure with cable glands; a SIM and data plan.

## 4. Make the board

1. Upload `utility10/pcb/release/mitti/1_fabrication/mitti_netra_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; 1 oz is fine). 2. For assembly upload `2_assembly/mitti_netra_JLC_BOM.csv` and `mitti_netra_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.
The ADXL345 is an LGA-14 part: use the fab's reflow assembly; do not hand-solder it.

## 5. Program and configure

Arduino-ESP32 core 2.x: `mitti-netra/firmware/src/main_mitti.cpp` plus `firmware/lib/mn_core.c`. Set the placeholders: soil calibration counts (dry air, water), strain excitation/gauge factor/bridge type, tilt and strain thresholds. Install: tilt the node into its final position, power up once: that boot stores the baseline (tilt angles and strain zero) in RTC memory; a power loss loses the baseline.

## 6. Test (see `mitti-netra/docs/TEST_PLAN.md`)

Charge LEDs; TP2 3.3 V; deep-sleep current; modem switch toggles VBAT_M; ADXL345 ID 0xE5; tilt plate 10 degrees reads 10 +-0.5; HX711 shunt-resistor check; 7-day outdoor run.

## 7. Limits

No cell protection on the board (use protected cells). LDO stops below about 3.55 V on the cell. Strain numbers are conversions, not a calibrated instrument. Carrier APN, bands and a server are not provided. Not safety-rated.
