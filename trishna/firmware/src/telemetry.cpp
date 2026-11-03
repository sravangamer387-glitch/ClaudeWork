#include "telemetry.h"
#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include "board_pins.h"

static QueueHandle_t g_q = nullptr;
static volatile uint32_t g_drop = 0, g_sent = 0;
static uint16_t g_seq = 0;
static bool g_sd = false;
static portMUX_TYPE g_mux = portMUX_INITIALIZER_UNLOCKED;
static const char *LOG_PATH = "/trishna.bin";
struct Item { uint8_t b[TR_FRAME_LEN]; };

static void tlm_task(void *) {
    Item it;
    File log;
    uint32_t since_flush = 0;
    for (;;) {
        if (xQueueReceive(g_q, &it, pdMS_TO_TICKS(1000)) == pdTRUE) {
            Serial2.write(it.b, TR_FRAME_LEN);                 // UART FIFO + driver buffer: returns quickly
            g_sent++;
            if (g_sd) {
                if (!log) log = SD.open(LOG_PATH, FILE_APPEND);
                if (log) { log.write(it.b, TR_FRAME_LEN); if (++since_flush >= 4) { log.flush(); since_flush = 0; } }
                else g_sd = false;                              // card removed or failed: keep streaming over UART
            }
        } else if (log) { log.flush(); since_flush = 0; }      // idle for 1 s: make the log durable
    }
}

void tlm_init() {
    Serial2.setTxBufferSize(1024);
    Serial2.begin(TLM_BAUD, SERIAL_8N1, PIN_TLM_RX, PIN_TLM_TX);
    SPI.begin(PIN_SD_SCK, PIN_SD_MISO, PIN_SD_MOSI, PIN_SD_CS);
    g_sd = SD.begin(PIN_SD_CS, SPI, 10000000);
    g_q = xQueueCreate(32, sizeof(Item));
    xTaskCreatePinnedToCore(tlm_task, "tlm", 4096, nullptr, 2, nullptr, 0);
}

bool tlm_send(tr_frame_t &f) {
    Item it;
    portENTER_CRITICAL(&g_mux); f.seq = g_seq++; portEXIT_CRITICAL(&g_mux);
    tr_frame_seal(&f, it.b);
    if (!g_q || xQueueSend(g_q, &it, 0) != pdTRUE) { g_drop++; return false; }
    return true;
}

bool tlm_sd_ok() { return g_sd; }
uint32_t tlm_dropped() { return g_drop; }
uint32_t tlm_sent() { return g_sent; }
