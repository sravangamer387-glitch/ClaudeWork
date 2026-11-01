/* KINETIC controller (kinetic_ctl rev A) ESP32-S3 pin map: must match utility10/pcb/boards/kinetic_ctl.py */
#pragma once
#define PIN_X_STEP 4
#define PIN_X_DIR  5
#define PIN_X_EN   6
#define PIN_Y_STEP 7
#define PIN_Y_DIR  15
#define PIN_Y_EN   16
#define PIN_Z_STEP 17
#define PIN_Z_DIR  18
#define PIN_Z_EN   8
#define PIN_ES_X   9
#define PIN_ES_Y   10
#define PIN_ES_Z   11
#define PIN_S_CS   12
#define PIN_S_SCLK 13
#define PIN_S_MOSI 14
#define PIN_S_MISO 21
#define PIN_VM_SENSE 1     /* 24 V divider 100k/10k: Vm = adc_volts * 11 */
#define PIN_LED    48
#define PIN_UART_TX 43     /* TXD0 */
#define PIN_UART_RX 44     /* RXD0 */
