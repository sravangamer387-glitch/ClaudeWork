# GEONODE: foundation and geotechnical monitoring network (LoRa nodes + gateway anomaly detection)

Programme 4 (civil + electrical + AI). **Status: signal-processing design, node feature extractor (C) and gateway detector (Python) host-tested on synthetic vibration; no hardware of its own; nothing built, buried or field-tested.**

## Architecture
- **Node = the MITTI-NETRA board** (ESP32-S3, ADXL345, HX711 strain input, solar/Li-ion) with a **UART LoRa module breakout** (e.g. an RAK3172 or RA-08 style AT-command module) plugged into the same modem socket (VBAT, GND, TX, RX, PWRKEY, STATUS) instead of the cellular breakout. No new PCB: it inherits the MITTI-NETRA board status (see `mitti-netra/`).
- **Node firmware idea** (`node/lib/gt_feat.[ch]`): every cycle, wake, sample 2 s at 200 Hz, compute six features (rms, low-band 3-20 Hz fraction, high-band >30 Hz fraction, kurtosis, crest, peak), pack a 12-byte CRC-8 frame, send over LoRa, sleep. Slow strain and tilt go in a second, rarer frame (MITTI-NETRA frame format).
- **Gateway** (`gateway/anomaly.py`): classifies each window as AMBIENT, VEHICLE or CRACK with transparent thresholds calibrated from an install-time baseline recording; `CrackTracker` raises a structural alarm only after repeated crack-class windows (default 3 in 30), so one vehicle or knock never alarms.

## Results (synthetic data; `gateway/test_anomaly.py`, `node/` `make test`)
Ambient and gusty ambient 100 % correct, vehicle 100 %, crack 95 % (the missed 5 % are the weakest single impulses), held-out seed holds; vehicle traffic alone never raises the alarm. The C feature code matches the Python definition within 0.2 % on six test windows and survives quantisation into the 12-byte frame (54 checks, ASan/UBSan).

## Honest limits
Synthetic vibration only: real concrete cracking, soil coupling, sensor mounting and weather differ. The thresholds are install-specific and must be re-derived from a real baseline; the cracking signature (40-90 Hz decaying bursts) is an assumption, not a measurement. LoRa regional frequency plan (India 865-867 MHz), duty cycle and gateway are your responsibility. Buried installation needs waterproof potting and an antenna strategy that this design does not provide. Not a certified structural-health-monitoring system and not a substitute for engineering inspection.
