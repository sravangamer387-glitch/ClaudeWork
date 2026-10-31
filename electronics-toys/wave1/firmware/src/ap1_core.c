#include "ap1.h"

/* ---------------- buttons ---------------- */
static void push(btn_scan_t *b, uint8_t idx, uint8_t kind) {
    if (b->qn == BTN_QUEUE) return; /* drop on overflow, never block */
    b->q[b->qt].idx = idx;
    b->q[b->qt].kind = kind;
    b->qt = (uint8_t)((b->qt + 1u) % BTN_QUEUE);
    b->qn++;
}

void btn_init(btn_scan_t *b, const ap1_hal_t *hal, uint8_t n) {
    *b = (btn_scan_t){0};
    b->hal = hal;
    b->n = n > BTN_MAX ? BTN_MAX : n;
}

void btn_update(btn_scan_t *b) {
    uint32_t now = b->hal->millis();
    for (uint8_t i = 0; i < b->n; i++) {
        bool raw = b->hal->button_raw(i);
        if (raw != b->last_raw[i]) {
            b->last_raw[i] = raw;
            b->t_change[i] = now;
        } else if (raw != b->stable[i] && (uint32_t)(now - b->t_change[i]) >= BTN_DEBOUNCE_MS) {
            b->stable[i] = raw;
            if (raw) {
                b->t_press[i] = now;
                b->long_sent[i] = false;
                push(b, i, BTN_EVT_PRESS);
            } else {
                push(b, i, BTN_EVT_RELEASE);
            }
        }
        if (b->stable[i] && !b->long_sent[i] && (uint32_t)(now - b->t_press[i]) >= BTN_LONG_MS) {
            b->long_sent[i] = true;
            push(b, i, BTN_EVT_LONG);
        }
    }
}

bool btn_pop(btn_scan_t *b, btn_evt_t *out) {
    if (b->qn == 0) return false;
    *out = b->q[b->qh];
    b->qh = (uint8_t)((b->qh + 1u) % BTN_QUEUE);
    b->qn--;
    return true;
}

/* ---------------- MP3 module protocol ---------------- */
size_t df_build(uint8_t out[DF_FRAME_LEN], uint8_t cmd, uint16_t param) {
    uint8_t p1 = (uint8_t)(param >> 8), p2 = (uint8_t)(param & 0xFFu);
    uint16_t sum = (uint16_t)(0xFFu + 0x06u + cmd + 0x00u + p1 + p2);
    uint16_t chk = (uint16_t)(0u - sum);
    out[0] = 0x7E; out[1] = 0xFF; out[2] = 0x06; out[3] = cmd; out[4] = 0x00;
    out[5] = p1; out[6] = p2; out[7] = (uint8_t)(chk >> 8); out[8] = (uint8_t)(chk & 0xFFu); out[9] = 0xEF;
    return DF_FRAME_LEN;
}

bool df_parse(const uint8_t *in, size_t n, uint8_t *cmd, uint16_t *param) {
    if (n != DF_FRAME_LEN || in[0] != 0x7E || in[1] != 0xFF || in[2] != 0x06 || in[9] != 0xEF) return false;
    uint16_t sum = (uint16_t)(in[1] + in[2] + in[3] + in[4] + in[5] + in[6]);
    uint16_t chk = (uint16_t)((in[7] << 8) | in[8]);
    if ((uint16_t)(sum + chk) != 0u) return false;
    *cmd = in[3];
    *param = (uint16_t)((in[5] << 8) | in[6]);
    return true;
}

void df_init(df_t *d, const ap1_hal_t *hal, uint8_t vol_cap) {
    d->hal = hal;
    d->vol_cap = vol_cap > DF_VOL_MAX ? (uint8_t)DF_VOL_MAX : vol_cap;
    d->frames = 0;
}

void df_cmd(df_t *d, uint8_t cmd, uint16_t param) {
    uint8_t f[DF_FRAME_LEN];
    df_build(f, cmd, param);
    d->hal->uart_write(f, DF_FRAME_LEN);
    d->frames++;
}

uint8_t df_volume(df_t *d, uint8_t v) {
    if (v > d->vol_cap) v = d->vol_cap;
    df_cmd(d, DF_CMD_VOL_SET, v);
    return v;
}

void df_play_folder_track(df_t *d, uint8_t folder, uint8_t track) {
    df_cmd(d, DF_CMD_FOLDER, (uint16_t)((folder << 8) | track));
}
