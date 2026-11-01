# AQUAPONICS test plan (bench and tank steps not yet run)
A (PC): `cd firmware && make test` (DO saturation table, forecaster lead time, no false alerts, stuck/range sensor checks, 7-day dosing simulation, daily cap and lockout, no dosing on bad sensor, aerator hysteresis).
B (bench, BioTray board): each channel with a dummy load; DS18B20, pH and ADS1115 DO readings with calibration solutions (pH 4/7, air-saturated and 0 mg/L sodium sulfite solution).
C (dry tank trial, water only, no fish): run 7 days with deliberate pH drift (add a little acid/base) and verify alerts, dosing pulses and the daily cap; pull the pH probe and verify lockout and an alarm.
D (fish): only after C, with an experienced operator, start with a low stocking density and keep manual test kits and an independent battery aerator.
