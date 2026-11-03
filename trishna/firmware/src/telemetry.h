// Asynchronous telemetry: the application only enqueues sealed 48-byte frames (never blocks); a FreeRTOS task on core 0 writes them
// to UART2 (J15, binary, 115200 8N1) for the local server bridge and appends them to /trishna.bin on the microSD card.
#pragma once
#include <stdint.h>
#include "trishna_frame.h"

void tlm_init();                                // starts UART2, mounts the SD card, creates the queue and the task
bool tlm_send(tr_frame_t &f);                   // fills seq, seals, enqueues; false when the queue was full (frame dropped)
bool tlm_sd_ok();
uint32_t tlm_dropped();
uint32_t tlm_sent();
