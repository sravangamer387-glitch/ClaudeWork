# AQUAPONICS: closed-loop aquaponic controller with edge forecasting

Programme 5 (biotech + agriculture + electrical + AI). **Status: control and forecasting core host-tested (13 checks); runs on the BioTray board with a different firmware; nothing built or run on fish. ALL BIOLOGICAL LIMITS ARE PLACEHOLDERS: tune them for your fish and plants with an expert.**

## What it does
- Reads water temperature (DS18B20), pH, EC, and dissolved oxygen (analog DO module through an ADS1115 on the I2C header).
- **Edge forecasting:** a Holt linear-trend model per variable (one sample per 10 min) predicts when pH, DO or temperature will leave its band within the next 2 hours, with a growing uncertainty margin (`aq_steps_to_breach`): the alert comes before the threshold is crossed (test: 6-40 samples ahead on a drifting pH, no false alert on a stable noisy series).
- **Dosing:** pH correction by short pump pulses with dead-band, minimum interval, **daily cap and lockout** (an unattended probe fault cannot empty the reservoir), and no dosing at all on a bad reading (out of range or stuck sensor).
- **Aeration:** DO against temperature-dependent saturation (Benson-Krause), with hysteresis, plus pre-emptive aeration when the DO forecast breaches.
- Hardware: **BioTray board** (see `biotray/`), channel map PUMP1 circulation, PUMP2 dosing, FAN output = aerator relay coil (flyback on board), LIGHT optional.

## Folders
`firmware/lib/aq_core.[ch]` core; `firmware/test/` (`make test`); `firmware/src/main_aquaponics.cpp` firmware (compiles for the ESP32-S3 with 0 warnings; binaries in `firmware/release/`); `docs/`.

## Honest limits
No ammonia/nitrite/nitrate sensing (these kill fish before pH moves: test with a kit daily at first); forecasting uses straight-line trends and cannot foresee sudden events (pump failure, power cut, feeding spikes); the pH and DO scale factors in the skeleton are placeholders; mains aerators must be switched through a proper relay module with an enclosure rated for wet environments; a power-cut fail-safe (battery aerator) is strongly recommended; not tested on live animals.
