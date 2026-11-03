// Hardware access for the TRISHNA controller (Arduino-ESP32 2.0.x).
#pragma once
#include <stdint.h>
#include "trishna_fsm.h"

struct EcRaw { float va_mv, vb_mv, ratio; };
struct OptRaw {
    float dark_tx, dark_sc;            // LEDs off
    float blue_tx;                     // blue on, dark-subtracted (transmission)
    float ir_tx, ir_sc;                // IR on, dark-subtracted (transmission, 90-degree scatter)
    bool saturated;
};
struct TofRaw { bool ok; bool valid; uint16_t mm; };

void hal_init();
void hal_pump(tr_pump_t dir, uint8_t duty);     // DRV8871: forward IN1 PWM, reverse IN2 PWM, off = coast
void hal_valve(bool open);
void hal_all_off();                              // pump, valve, LEDs, EC and probe drives low
EcRaw hal_ec_measure(int cycles);                // bipolar, balanced: equal time in both polarities, both pins low afterwards
void hal_probes(float &sump_mv, float &leak_mv); // pulsed read of sump + leak probes (about 200 us)
OptRaw hal_optics_measure(int repeats);          // dark / blue / IR sequence, median of repeats
float hal_vin_mv();
bool hal_temp_present();
void hal_temp_request();                         // start a 12-bit DS18B20 conversion (750 ms)
float hal_temp_read();                           // degC, NAN when missing
bool hal_tof_init();
TofRaw hal_tof_poll();                           // non-blocking; valid=false when no new data
