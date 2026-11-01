# GEONODE foundation monitoring network: build manual

> **Status: signal-processing design with host-tested node feature code (54 checks) and gateway detector; synthetic vibration only. Nothing built, buried or field-tested.** The node is the MITTI-NETRA board with a LoRa breakout instead of the cellular one.

## 1. Parts per node

MITTI-NETRA board (see `mitti-netra/`); UART LoRa module breakout (RAK3172 or RA-08 style, AT commands; India 865-867 MHz plan); antenna; protected Li-ion cell; solar panel; ADXL345 and HX711 are on the board; strain gauges and a waterproof potted enclosure. Gateway: any LoRa gateway or a second node plus a Raspberry Pi running `gateway/anomaly.py`.

## 2. Build

1. Make the MITTI-NETRA board. 2. Plug the LoRa module into socket J6 (match the pinout of your breakout: VBAT, GND, TX, RX, PWRKEY, STATUS). 3. Build node firmware from `geotech/node/lib/gt_feat.[ch]`; run `cd geotech/node && make test` and `python3 geotech/gateway/test_anomaly.py` on a PC. 4. Install the node, record a baseline (the thresholds are install-specific), and calibrate `anomaly.py` from it.

## 3. Commissioning

See `geotech/docs/TEST_PLAN.md`: tap and vehicle tests against the baseline, alarm only after repeated crack-class windows, LoRa range and duty-cycle check.

## 4. Limits

Synthetic data only: the 40-90 Hz cracking signature is an assumption. Buried use needs potting and an antenna strategy not provided here. Not a certified structural-health-monitoring system. General rules: `manuals/STANDARD_PROCEDURES.md`.
