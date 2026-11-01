# AQUAPONICS design notes
**Forecaster.** Holt linear smoothing (alpha 0.3, beta 0.1) on 10-minute samples. The one-step error variance is tracked and the forecast uncertainty grows as sqrt(1 + 0.3 h). A breach is reported if the forecast minus 2 sigma crosses the lower limit while the trend is falling (or plus 2 sigma crosses the upper limit while rising). At least 6 samples are needed before any alert.
**Dosing safety.** Pulse length, minimum interval, daily cap and lockout are all configuration; on lockout the controller keeps measuring and alarming but stops dosing until the day rolls over or a human intervenes.
**DO.** Saturation from temperature (fresh water, sea level); altitude and salinity corrections are not applied.
**Why on the BioTray board.** Same 12 V low-side outputs and ESP32-S3; only the firmware and the sensors differ, so the board status (DRC 0 / unconnected 0) carries over.
