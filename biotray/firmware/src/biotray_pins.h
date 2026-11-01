/* BioTray rev A ESP32-S3 pin map: must match utility10/pcb/boards/biotray.py */
#pragma once
#define PIN_PUMP1 4
#define PIN_PUMP2 5
#define PIN_LIGHT 6     /* PWM, active high gate */
#define PIN_FAN   7
#define PIN_SDA   8
#define PIN_SCL   9
#define PIN_LEVEL 10    /* float switch closes to GND when water present; external 10k pull-up */
#define PIN_ONEWIRE 15
#define PIN_PH_ADC 1    /* 0-3 V pH module output via 1k + 100 nF */
#define PIN_EC_ADC 2
#define PIN_LED   48
