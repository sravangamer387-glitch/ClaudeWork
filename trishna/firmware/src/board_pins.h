// TRISHNA controller rev A - ESP32-DevKitC-32E pin map (must match utility10/pcb/boards/trishna.py and the netlist in docs).
#pragma once

// ---- analog inputs: ADC1 only (ADC2 is unusable while Wi-Fi is on); every input has an RC filter on the board ----
#define PIN_EC_ADC      36   // SENSOR_VP: EC cell node N1 via 100 R / 1 nF
#define PIN_OPT_TX_ADC  39   // SENSOR_VN: transmission TIA (10 k) via 1 k / 10 nF
#define PIN_OPT_SC_ADC  34   // scatter TIA (1 M) via 1 k / 10 nF
#define PIN_VIN_ADC     35   // 12 V monitor: 100 k / 10 k divider + 100 nF  (x11)
#define PIN_SUMP_ADC    32   // sump stream probe via 1 k / 1 nF (4.7 k from LVL_DRV)
#define PIN_LEAK_ADC    33   // chamber-B leak probe via 1 k / 1 nF (47 k from LVL_DRV)

// ---- sensor drive outputs ----
#define PIN_EC_DRV_A    25   // -> 330 R -> electrode E1
#define PIN_EC_DRV_B    26   // -> 100 R -> electrode E2
#define PIN_LVL_DRV     27   // pulses the sump and leak probes only while they are read
#define PIN_LED_BLU     14   // AO3400A gate: 450 nm LED (1 k from 12 V)   [boot: brief PWM, harmless]
#define PIN_LED_IR      15   // AO3400A gate: 850 nm LED (1 k from 12 V)   [strapping pin; 100 k pull-down on the gate net]

// ---- actuators ----
#define PIN_PUMP_IN1    13   // DRV8871 IN1: high = forward (sump -> chamber -> waste)
#define PIN_PUMP_IN2    12   // DRV8871 IN2: high = reverse (backwash)  [strapping pin: must be low at boot - DRV8871 has an internal pull-down]
#define PIN_VALVE        2   // AO3400A gate: fresh-water solenoid      [strapping pin, 100 k pull-down; the DevKit blue LED shows the valve state]

// ---- buses ----
#define PIN_SDA         21
#define PIN_SCL         22
#define PIN_ONEWIRE      4   // DS18B20, 4.7 k pull-up on the board
#define PIN_SD_SCK      18
#define PIN_SD_MISO     19
#define PIN_SD_MOSI     23
#define PIN_SD_CS        5   // 10 k pull-up on the board
#define PIN_TLM_TX      17   // UART2 TX -> J15 pin 2 -> USB-serial RX
#define PIN_TLM_RX      16   // UART2 RX <- J15 pin 3

#define VIN_DIVIDER     11.0f   // (100 k + 10 k) / 10 k
#define TLM_BAUD        115200
#define CONSOLE_BAUD    115200
