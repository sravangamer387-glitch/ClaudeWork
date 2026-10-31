/* Jal-Netra firmware skeleton for the STM32G431 (NOT built or run on target: no HAL/CMSIS is included in this repository).
 * It documents the intended timing and DMA flow around the tested core (lib/jn_core.c). Register-level details must be completed on hardware.
 *
 * Clocks: HSE 8 MHz -> PLL -> SYSCLK 170 MHz; TIM3 clocked 170 MHz; ADC1 clocked from PLL/4 -> 42.5 MHz (12-bit: 15 ADC cycles = 2.8 MS/s... use 4 MS/s by sampling time 2.5 cycles + 12.5 = 15 cycles at 60 MHz; set per datasheet).
 *
 * One transit-time shot (A transmits, B receives; then roles swap):
 *   1. Mux U4 selects the RX transducer (MUX_SEL), gain U7 selected (GAIN_SEL).
 *   2. TX pins: TIM3 CH1 / CH2 (second channel inverted): 6 periods of 1.000 MHz (ARR = 169), then both pins low; the receiving transducer's driven leg is held low by its own TIM3 channel forced low.
 *   3. TIM1 (or TIM3 CH4 compare) triggers ADC1 at exactly t_trigger = ToF_estimate - 4 us after the first TX edge: ADC runs 64 conversions at 4 MS/s into a DMA buffer (circular-free, one shot).
 *   4. DMA complete interrupt: subtract mid-scale (about 2048), call jn_demod() and jn_tof_coarse(); jn_acc_add(up, down).
 *   5. After 1000 pairs (about 0.5 s incl. 200 us repetition per shot) call jn_acc_result(), jn_flow_lpm(), jn_zero_update(), then sleep (STOP mode) until the next measurement.
 * Measurement schedule: 1 s when flow was seen in the last 10 s, otherwise every 10 s (battery/USB energy is not critical on USB power).
 * Self test: at power-up transmit with the RX switch on both transducers and verify amplitude > threshold; report 'dry pipe' if amplitude collapses (air in the spool).
 */
#include "../lib/jn_core.h"
/* ... startup, clock, GPIO, TIM3, ADC1+DMA, USART3, I2C1 (OLED) driver code to be written against the ST HAL ... */
