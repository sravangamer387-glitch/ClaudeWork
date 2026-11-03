#include "trishna_frame.h"
#include <math.h>
#include <string.h>

uint16_t tr_crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (int b = 0; b < 8; b++) crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021) : (uint16_t)(crc << 1);
    }
    return crc;
}

static void put8(uint8_t *o, size_t *i, uint8_t v) { o[(*i)++] = v; }
static void put16(uint8_t *o, size_t *i, uint16_t v) { o[(*i)++] = (uint8_t)v; o[(*i)++] = (uint8_t)(v >> 8); }
static void put32(uint8_t *o, size_t *i, uint32_t v) { for (int k = 0; k < 4; k++) o[(*i)++] = (uint8_t)(v >> (8 * k)); }
static uint8_t get8(const uint8_t *o, size_t *i) { return o[(*i)++]; }
static uint16_t get16(const uint8_t *o, size_t *i) { uint16_t v = (uint16_t)(o[*i] | (o[*i + 1] << 8)); *i += 2; return v; }
static uint32_t get32(const uint8_t *o, size_t *i) { uint32_t v = 0; for (int k = 0; k < 4; k++) v |= (uint32_t)o[*i + k] << (8 * k); *i += 4; return v; }

void tr_frame_seal(tr_frame_t *f, uint8_t out[TR_FRAME_LEN]) {
    size_t i = 0;
    f->sync0 = TR_SYNC0; f->sync1 = TR_SYNC1; f->version = TR_FRAME_VERSION;
    put8(out, &i, f->sync0); put8(out, &i, f->sync1); put8(out, &i, f->version); put8(out, &i, f->type);
    put16(out, &i, f->seq); put32(out, &i, f->unix_s); put16(out, &i, f->ms); put32(out, &i, f->uptime_s);
    put8(out, &i, f->state); put8(out, &i, f->prev_state); put16(out, &i, f->event_id); put16(out, &i, f->flags); put16(out, &i, f->error_code);
    put16(out, &i, (uint16_t)f->temp_cx100); put16(out, &i, f->ec25_x100); put16(out, &i, f->cell_ohm); put16(out, &i, f->sg_x10000);
    put16(out, &i, (uint16_t)f->a450_x1000); put16(out, &i, f->turb_x1000); put16(out, &i, f->tx_blue_mv); put16(out, &i, f->tx_ir_mv);
    put16(out, &i, f->sc_ir_mv); put16(out, &i, f->vin_mv); put8(out, &i, f->hydration); put8(out, &i, f->quality);
    f->crc16 = tr_crc16(out, TR_FRAME_LEN - 2);
    put16(out, &i, f->crc16);
}

int tr_frame_parse(const uint8_t in[TR_FRAME_LEN], tr_frame_t *f) {
    size_t i = 0;
    if (in[0] != TR_SYNC0 || in[1] != TR_SYNC1 || in[2] != TR_FRAME_VERSION) return -1;
    if (tr_crc16(in, TR_FRAME_LEN - 2) != (uint16_t)(in[46] | (in[47] << 8))) return -2;
    f->sync0 = get8(in, &i); f->sync1 = get8(in, &i); f->version = get8(in, &i); f->type = get8(in, &i);
    f->seq = get16(in, &i); f->unix_s = get32(in, &i); f->ms = get16(in, &i); f->uptime_s = get32(in, &i);
    f->state = get8(in, &i); f->prev_state = get8(in, &i); f->event_id = get16(in, &i); f->flags = get16(in, &i); f->error_code = get16(in, &i);
    f->temp_cx100 = (int16_t)get16(in, &i); f->ec25_x100 = get16(in, &i); f->cell_ohm = get16(in, &i); f->sg_x10000 = get16(in, &i);
    f->a450_x1000 = (int16_t)get16(in, &i); f->turb_x1000 = get16(in, &i); f->tx_blue_mv = get16(in, &i); f->tx_ir_mv = get16(in, &i);
    f->sc_ir_mv = get16(in, &i); f->vin_mv = get16(in, &i); f->hydration = get8(in, &i); f->quality = get8(in, &i); f->crc16 = get16(in, &i);
    return 0;
}

uint16_t tr_u16_sat(float v) {
    if (!(v == v) || v <= 0.0f) return 0;          /* NaN or negative */
    if (v >= 65535.0f) return 65535;
    return (uint16_t)lroundf(v);
}
int16_t tr_i16_sat(float v) {
    if (!(v == v)) return INT16_MIN;
    if (v >= 32767.0f) return 32767;
    if (v <= -32767.0f) return -32767;
    return (int16_t)lroundf(v);
}
