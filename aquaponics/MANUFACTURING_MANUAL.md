# AQUAPONICS controller: build manual

> **Status: control and forecasting core host-tested (13 checks); nothing built or run on live fish.** No new PCB: it runs on the BioTray board (`biotray/`, order-ready). ALL BIOLOGICAL LIMITS ARE PLACEHOLDERS: tune them with an aquaculture expert.

## 1. Parts

BioTray board (see `biotray/MANUFACTURING_MANUAL.md`); DS18B20 waterproof probe; analog pH module + probe; analog EC module + probe; analog dissolved-oxygen module + probe; ADS1115 breakout on the I2C header; 12 V circulation pump; 12 V dosing (peristaltic) pump + pH-down reservoir; relay module for the aerator (the FAN output drives the relay coil, flyback is on the board); backup battery aerator (strongly recommended); GFCI-protected supply; sealed enclosure for the wet environment.

## 2. Build

1. Build and test the BioTray board first. 2. Wire PUMP1 = circulation, PUMP2 = dosing, FAN = aerator relay coil, sensors as in `aquaponics/docs/DESIGN.md`. 3. Compile `aquaponics/firmware/src/main_aquaponics.cpp` with `firmware/lib/aq_core.c` (Arduino-ESP32 2.x): **the firmware compiles for the ESP32-S3 (tools/esp32_build.sh, 0 warnings, binary in `aquaponics/firmware/release/`); bring it up on a bench.** 4. Run `cd aquaponics/firmware && make test` on a PC (13 checks).

## 3. Calibrate

pH with pH 4 and 7 buffers, EC with a standard solution, DO with its 0 % and saturated points, then set the scale factors (placeholders in the skeleton). Set band limits for your species.

## 4. Commissioning

Dry run with water only and no fish for at least a week: dosing never exceeds the daily cap, a pulled probe stops dosing (bad-reading lockout), aeration follows the DO forecast, power-cut behaviour is safe. See `aquaponics/docs/TEST_PLAN.md`.

## 5. Limits

No ammonia/nitrite/nitrate sensing: test with a kit daily at first. Straight-line forecasts cannot foresee pump failure or feeding spikes. Mains aerators need a proper relay and a rated enclosure. Not tested on live animals. General rules: `manuals/STANDARD_PROCEDURES.md`.
