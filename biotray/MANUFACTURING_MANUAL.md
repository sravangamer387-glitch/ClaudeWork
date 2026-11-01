# BioTray vertical-farm tray controller: manufacturing manual

> **Status: design only; nothing built.** PCB: **PCB not released yet: do not send to a fab**. Firmware control core host-tested (22 checks); ESP32 glue never compiled. pH/EC calibration values are placeholders.

## 1. What is made

A 100 x 80 mm controller: 12 V in, ESP32-S3 (WiFi/MQTT), four low-side 12 V outputs (2 pumps, fan, PWM grow light), DS18B20, I2C (BH1750/SHT31), water-level switch, analog pH and EC inputs.

## 2. Deliverables

| Item | Where | State |
|---|---|---|
| PCB | `utility10/pcb/release/biotray/` and `biotray/hardware/` | **PCB not released yet: do not send to a fab** |
| Control core + tests | `biotray/firmware/lib/bt_core.[ch]`, `test/test_bt.c` | passes |
| ESP32 skeleton | `biotray/firmware/src/main_biotray.cpp` | not compiled |

### Bought-in

12 V 3 A adapter (barrel 5.5/2.1, centre positive), 12 V peristaltic or submersible pumps, 12 V fan, 12 V LED grow strip (total under 1.1 A or replace the PTC), DS18B20 probe, BH1750 module, float switch, pH module and probe, EC module and probe, tubing, tray.

## 4. Make the board

1. Upload `utility10/pcb/release/biotray/1_fabrication/biotray_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; 1 oz is fine for loads up to about 1 A total). 2. For assembly upload `2_assembly/biotray_JLC_BOM.csv` and `biotray_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). 3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.

## 5. Program and configure

Arduino-ESP32 core 2.x with PubSubClient, OneWire, DallasTemperature, BH1750. Copy `secrets.h.example` to `secrets.h`. Calibrate pH with pH 4 and pH 7 buffers and EC with a standard solution, then edit `PH_CAL`, `EC_CAL`. MQTT topics: see `biotray/docs/DESIGN.md`.

## 6. Test (see `biotray/docs/TEST_PLAN.md`)

Supply rails, reverse-polarity test, dummy loads on every output, dry-run test (remove water: pump stops and latches), 48 h run.

## 7. Limits

Water, mains adapter and electricity together: use a GFCI-protected supply and an enclosure with proper sealing. No isolation on the pH probe. Not tested on hardware.
