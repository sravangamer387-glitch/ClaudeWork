# BioWatt energy budget (assumption-based model, not measured)

Harvester efficiency assumed 60 %. E_report = energy per transmission (wake, sense, send); P_sleep = sleep power.

| MFC | Voc V | Rint ohm | Pmax uW | harvested J/day | node | E_report J | P_sleep uW | sleep J/day | reports/day possible |
|---|---|---|---|---|---|---|---|---|---|
| small soil MFC (cheap electrodes) | 0.65 | 5000 | 21 | 1.10 | ESP32-S3 WiFi + MQTT report | 1.98 | 33 | 2.85 | 0.0 |
| small soil MFC (cheap electrodes) | 0.65 | 5000 | 21 | 1.10 | ESP32-S3 BLE advert only | 0.08 | 33 | 2.85 | 0.0 |
| small soil MFC (cheap electrodes) | 0.65 | 5000 | 21 | 1.10 | ultra-low-power MCU + LoRa packet | 0.15 | 7 | 0.57 | 3.5 |
| good lab MFC | 0.7 | 1000 | 122 | 6.35 | ESP32-S3 WiFi + MQTT report | 1.98 | 33 | 2.85 | 1.8 |
| good lab MFC | 0.7 | 1000 | 122 | 6.35 | ESP32-S3 BLE advert only | 0.08 | 33 | 2.85 | 42.4 |
| good lab MFC | 0.7 | 1000 | 122 | 6.35 | ultra-low-power MCU + LoRa packet | 0.15 | 7 | 0.57 | 38.9 |
| 4 good cells in series (2.8 V, 4 kohm total) | 2.8 | 4000 | 490 | 25.40 | ESP32-S3 WiFi + MQTT report | 1.98 | 33 | 2.85 | 11.4 |
| 4 good cells in series (2.8 V, 4 kohm total) | 2.8 | 4000 | 490 | 25.40 | ESP32-S3 BLE advert only | 0.08 | 33 | 2.85 | 273.3 |
| 4 good cells in series (2.8 V, 4 kohm total) | 2.8 | 4000 | 490 | 25.40 | ultra-low-power MCU + LoRa packet | 0.15 | 7 | 0.57 | 167.2 |

**Reading the table.** A single small MFC gives a few joules per day. A WiFi report costs about 2 J, and even deep sleep costs 2-3 J per day, so a WiFi ESP32 cannot run from one small MFC at all; a LoRa/BLE node reporting a few times a day can. Even a 4-cell series stack (about 0.5 mW) supports only about ten WiFi reports a day; a WiFi tray controller with pumps and lights needs watts, so it needs mains or a battery.
BioTray itself (pumps, LEDs, WiFi) needs watts and is NOT meant to run from an MFC: BioWatt powers a low-power *sensor tag* (soil/water temperature, moisture, level) that reports to the tray, or trickle-charges a backup cell.

The MPPT fraction (50-80 % of Voc) and the harvester start-up voltage matter more than the IC's headline efficiency: a single 0.65 V MFC sits close to the cold-start threshold of the common harvester ICs (hundreds of mV), so verify start-up on the real cell.
