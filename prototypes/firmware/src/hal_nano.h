/* Arduino Nano (ATmega328P) hardware layer for the prototype builds.
 * Build one product at a time with -DPRODUCT_RHYMES / _LAMP / _CRICKET / _BEATLIGHT / _MIDI (see Makefile).
 * Pin maps are in hal_nano.cpp and in the build guides. */
#ifndef HAL_NANO_H
#define HAL_NANO_H
#include "ap1.h"

extern const ap1_hal_t HAL;
void hal_init(void);          /* pin modes, serial to the MP3 module, TM1637 display */

#endif
