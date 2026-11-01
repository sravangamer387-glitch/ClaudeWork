# MITTI-NETRA design
## Hardware (`utility10/pcb/boards/mitti.py`, 90 x 80 mm, 2 layers)
| Block | Parts | Notes |
|---|---|---|
| Charger | TP4056 (C382139) with PROG = 2.2 k (about 0.58 A); solar and USB OR-ed by two SS14 diodes | solar input 5-6 V nominal; the TP4056 is a linear charger, so a 6 V panel wastes the difference as heat; no MPPT |
| Cell | JST-PH 2 for one protected 18650 / pouch cell | no protection IC on board |
| Regulator | AP2112K-3.3 from the cell | stops regulating below about 3.55 V |
| Controller | ESP32-S3-WROOM-1-N8, native USB for programming | antenna keep-out at the right edge |
| Modem socket | 2x3 header: VBAT_M, GND, TX, RX, PWRKEY, STATUS; AO3401A high-side switch driven by an AO3400A; 100 uF + 22 uF burst capacitors | the modem is powered only while transmitting |
| Tilt / vibration | ADXL345 on I2C (address 0x53), INT1 wakes the ESP32 | wake threshold set in firmware |
| Strain | HX711 (copy of the verified Gas Taraju circuit) + JST-PH 4 bridge connector | 3.3 V excitation: full-scale only about +-13 mV at gain 128 |
| Soil / temperature | JST-PH 3 for a capacitive probe (analog, through 1 k + 100 nF), JST-PH 3 for a DS18B20 with 4.7 k pull-up | |
| Battery sense | 330 k / 330 k divider (about 6 uA) | measure only when awake |

## Firmware core (`firmware/lib/mn_core.c`)
- Soil: two-point calibration (dry-air and water-immersed ADC counts), clamped 0-100 %.
- Tilt: roll = atan2(ay, az), pitch = atan2(-ax, sqrt(ay^2+az^2)); the alarm uses the *change* from an installation baseline, not the absolute angle.
- Strain: V = raw * (0.5*AVDD/gain) / 2^23; microstrain = 1e6 * k * V / (Vex * GF) with k = 4 for a quarter bridge (check your wiring) and zero offset taken at installation.
- Alarm: rising level needs `debounce` consecutive readings; falling uses a hysteresis band; magnitude uses |x|.
- Frame: 26 bytes, big-endian: 0xA5, version 1, node id, unix time, soil %x10, temp x10, roll x100, pitch x100, microstrain (int32), battery mV, level, flags, CRC-16/CCITT-FALSE.
- Interval policy: 6 h base; 1 h after rain; 30 min WATCH; 10 min ALARM; x4 if the cell is below 3.55 V and the level is not ALARM.

## Edge camera (`camera/crop_index.py`)
ExG = 2g - r - b on chromatic coordinates, Otsu threshold, canopy cover and mean ExG of canopy pixels. Self-test passes on synthetic scenes (also at 40 % brightness). Only numbers are uplinked.

## Cellular outline (not implemented)
Power the modem with MODEM_EN, pulse PWRKEY, wait for STATUS, AT+CPIN?, AT+CNMP/CMNB for LTE-M or NB-IoT, AT+CGDCONT with your APN, open a TCP/UDP or MQTT session, send the 26-byte frame (base64 or binary), power the modem down. Carrier APN and band settings must be confirmed with your SIM provider.

## Risks
Cell undervoltage and LDO cutoff; modem inrush (the 100 uF + 22 uF may need to be larger for 2G fallback, which this design does not use); strain-gauge drift; rain ingress (needs a sealed enclosure and cable glands); GNSS not included.
