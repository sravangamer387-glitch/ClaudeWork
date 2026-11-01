/* MITTI-NETRA rev A ESP32-S3 pin map: must match utility10/pcb/boards/mitti.py (checked by tools/check_pins.py) */
#pragma once
#define PIN_ONEWIRE 15
#define PIN_MODEM_TX 16       /* net MODEM_TX: ESP32 TX output toward the modem breakout RX */
#define PIN_MODEM_RX 17       /* net MODEM_RX: ESP32 RX input from the modem breakout TX */
#define PIN_MODEM_PWRKEY 18
#define PIN_MODEM_STATUS 8
#define PIN_MODEM_EN 6
#define PIN_HX_DT 4
#define PIN_HX_SCK 5
#define PIN_ACC_INT 9
#define PIN_SDA 10
#define PIN_SCL 11
#define PIN_SOIL_ADC 1
#define PIN_VBAT_ADC 2
#define PIN_LED 48
