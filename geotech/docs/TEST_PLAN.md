# GEONODE test plan (field steps not yet run)
**A (PC):** `cd node && make test`; `cd gateway && python3 test_anomaly.py`.
**B (bench, MITTI-NETRA board + LoRa breakout):** UART link to the LoRa module (AT reply); send a 12-byte frame to a gateway on the bench; verify CRC rejects corrupted frames.
**C (baseline):** record at least 24 h of 2 s windows at the installation point with no intervention; run `Detector.calibrate` on the windows; store thresholds with the node id.
**D (events):** tap the structure with a hammer at known distances (should classify CRACK-like impulses only if their spectra match; record and adjust), drive a heavy vehicle past (should be VEHICLE), measure false alarms over a week.
**E (system):** battery/solar budget over 30 days; LoRa packet loss at the planned range; alarm latency from event to notification.
