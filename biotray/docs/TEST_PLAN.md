# BioTray test plan (bench steps not yet run)
**A (PC):** `cd firmware && make test` (22 checks: ramps, over-midnight light, pump period and run time, dry-run latch, max-run, fan hysteresis, calibration, EC compensation, spike rejection, JSON overflow).
**B (board):** current-limited 12 V: TP1 = 12 V, TP2 = 5.0 V, TP3 = 3.3 V; reverse the supply once with a 100 mA limit: nothing conducts. USB only: ESP32 enumerates.
**C (outputs, 12 V resistive dummy loads first):** each channel switches; the light PWM dims linearly; fan and pumps with real loads show no gate ringing or MOSFET heating at rated current (touch test after 10 min at 1 A total).
**D (sensors):** DS18B20 and BH1750 read; level switch toggles the water flag; pH module in pH 4.0 and 7.0 buffers (set `PH_CAL` with the measured voltages); EC module in a standard solution.
**E (system):** 48 h run on a real tray with a tank: dry-run test (remove water: the pump must stop within one second and the fault must latch), MQTT reconnect after broker restart, schedule across midnight.
