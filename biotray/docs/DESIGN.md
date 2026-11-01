# BioTray design
## Hardware (`utility10/pcb/boards/biotray.py`, 100 x 80 mm)
12 V barrel jack -> 1.1 A PTC -> SMBJ15A TVS -> AO3401A reverse-polarity PMOS with a 12 V zener gate clamp -> VM rail (loads, buck). AP63205 buck (4.7 uH, 2 x 22 uF) -> 5 V -> AP2112K -> 3.3 V. USB-C (native USB) programs the ESP32-S3 and powers the logic through an SS14. Four AO3400A low-side drivers (100 ohm gate resistor, 100 k pull-down); SS14 flyback diodes on pumps and fan. Sensor inputs: DS18B20 (4.7 k pull-up), I2C 4-pin (4.7 k pull-ups), float switch (10 k pull-up to 3.3 V), pH and EC analog inputs through 1 k + 100 nF (the module outputs must not exceed 3.0 V).

## Control (`firmware/lib/bt_core.c`)
Light: `bt_light_pwm` (ramps scale linearly across the first/last `ramp_min` minutes; over-midnight periods supported). Pump: `bt_pump_step` (period, run time, max run time, minimum off time, dry-run latch). Fan: `bt_fan` (on at 28 C, off at 25 C by default). Calibration: `bt_cal_apply` two-point; `bt_ec_compensate`. Filter: median of 9 then EMA. JSON: `bt_json`.

## MQTT
`farm/<tray>/state` JSON every 30 s; `farm/<tray>/status` = `offline` (retained last will); command `farm/<tray>/cmd/pump_clear` clears the dry-run fault. Use a broker on your LAN with authentication and TLS where possible.

## Risks
Pump failure stuck-on (add a hardware timer or a second MOSFET in series for safety-critical use); mains-powered adapter in a wet environment; ESP32-S3 LDO limit (600 mA) during WiFi bursts; pH/EC probe drift (recalibrate weekly).
