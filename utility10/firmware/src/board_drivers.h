/* Small drivers for the rev B boards: TM1637 4-digit display, SSD1306 128x32 I2C OLED (text only), DS3231 RTC, HX711 24-bit ADC.
 * Written from the datasheets and public protocol descriptions; compiled and size-checked, NOT yet run on real hardware. */
#pragma once
#include <Arduino.h>
#include <Wire.h>
#include <avr/pgmspace.h>
/* ------------------------------ TM1637 (bit-banged, open-drain style) ------------------------------ */
struct TM1637 {
    uint8_t clk, dio;
    void dly() { delayMicroseconds(5); }
    void init(uint8_t c, uint8_t d) { clk = c; dio = d; pinMode(clk, INPUT); pinMode(dio, INPUT); digitalWrite(clk, LOW); digitalWrite(dio, LOW); }
    void lo(uint8_t p) { pinMode(p, OUTPUT); }                   /* output low (port bit already 0) */
    void hi(uint8_t p) { pinMode(p, INPUT); }                    /* released: the module's pull-up takes the line high */
    void start() { hi(clk); hi(dio); dly(); lo(dio); dly(); lo(clk); }
    void stop() { lo(clk); lo(dio); dly(); hi(clk); dly(); hi(dio); dly(); }
    bool wr(uint8_t b) {
        for (uint8_t i = 0; i < 8; i++) { lo(clk); if (b & 1) hi(dio); else lo(dio); dly(); hi(clk); dly(); b >>= 1; }
        lo(clk); hi(dio); dly(); hi(clk); dly(); bool ack = digitalRead(dio) == LOW; lo(clk); return ack;
    }
    void show(const uint8_t seg[4], uint8_t bright = 3) {
        start(); wr(0x40); stop(); start(); wr(0xC0); for (uint8_t i = 0; i < 4; i++) wr(seg[i]); stop(); start(); wr(0x88 | (bright & 7)); stop();
    }
    static uint8_t glyph(char c) {
        static const uint8_t D[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F};
        if (c >= '0' && c <= '9') return D[c - '0'];
        switch (c) { case '-': return 0x40; case ' ': return 0; case 'E': return 0x79; case 'r': return 0x50; case 'o': return 0x5C; case 'C': return 0x39; case 'A': return 0x77; case 'L': return 0x38; case 'P': return 0x73; case 'U': return 0x3E; case 'n': return 0x54; case 'F': return 0x71; case 'd': return 0x5E; case 'H': return 0x76; case 'S': return 0x6D; case 't': return 0x78; default: return 0; }
    }
    void text(const char *s4, bool colon = false, uint8_t bright = 3) { uint8_t seg[4]; for (uint8_t i = 0; i < 4; i++) seg[i] = glyph(s4[i]); if (colon) seg[1] |= 0x80; show(seg, bright); }
    void number(int32_t v, int8_t dp = -1, bool colon = false) {       /* right-aligned integer, optional decimal point after digit index dp (0..3) */
        char b[5] = "    "; bool neg = v < 0; if (neg) v = -v; int8_t i = 3;
        do { b[i--] = '0' + (v % 10); v /= 10; } while (v && i >= 0); if (neg && i >= 0) b[i] = '-';
        uint8_t seg[4]; for (uint8_t k = 0; k < 4; k++) seg[k] = glyph(b[k]); if (dp >= 0 && dp < 4) seg[dp] |= 0x80; if (colon) seg[1] |= 0x80; show(seg);
    }
};
/* ------------------------------ SSD1306 128x32, text only ------------------------------ */
static const uint8_t FONT5x7[] PROGMEM = {          /* ASCII 0x20..0x5A */
 0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x5F,0x00,0x00, 0x00,0x07,0x00,0x07,0x00, 0x14,0x7F,0x14,0x7F,0x14, 0x24,0x2A,0x7F,0x2A,0x12, 0x23,0x13,0x08,0x64,0x62, 0x36,0x49,0x56,0x20,0x50, 0x00,0x08,0x07,0x03,0x00,
 0x00,0x1C,0x22,0x41,0x00, 0x00,0x41,0x22,0x1C,0x00, 0x2A,0x1C,0x7F,0x1C,0x2A, 0x08,0x08,0x3E,0x08,0x08, 0x00,0x80,0x70,0x30,0x00, 0x08,0x08,0x08,0x08,0x08, 0x00,0x00,0x60,0x60,0x00, 0x20,0x10,0x08,0x04,0x02,
 0x3E,0x51,0x49,0x45,0x3E, 0x00,0x42,0x7F,0x40,0x00, 0x72,0x49,0x49,0x49,0x46, 0x21,0x41,0x49,0x4D,0x33, 0x18,0x14,0x12,0x7F,0x10, 0x27,0x45,0x45,0x45,0x39, 0x3C,0x4A,0x49,0x49,0x31, 0x41,0x21,0x11,0x09,0x07,
 0x36,0x49,0x49,0x49,0x36, 0x46,0x49,0x49,0x29,0x1E, 0x00,0x00,0x14,0x00,0x00, 0x00,0x40,0x34,0x00,0x00, 0x00,0x08,0x14,0x22,0x41, 0x14,0x14,0x14,0x14,0x14, 0x00,0x41,0x22,0x14,0x08, 0x02,0x01,0x59,0x09,0x06,
 0x3E,0x41,0x5D,0x59,0x4E, 0x7C,0x12,0x11,0x12,0x7C, 0x7F,0x49,0x49,0x49,0x36, 0x3E,0x41,0x41,0x41,0x22, 0x7F,0x41,0x41,0x41,0x3E, 0x7F,0x49,0x49,0x49,0x41, 0x7F,0x09,0x09,0x09,0x01, 0x3E,0x41,0x41,0x51,0x73,
 0x7F,0x08,0x08,0x08,0x7F, 0x00,0x41,0x7F,0x41,0x00, 0x20,0x40,0x41,0x3F,0x01, 0x7F,0x08,0x14,0x22,0x41, 0x7F,0x40,0x40,0x40,0x40, 0x7F,0x02,0x1C,0x02,0x7F, 0x7F,0x04,0x08,0x10,0x7F, 0x3E,0x41,0x41,0x41,0x3E,
 0x7F,0x09,0x09,0x09,0x06, 0x3E,0x41,0x51,0x21,0x5E, 0x7F,0x09,0x19,0x29,0x46, 0x26,0x49,0x49,0x49,0x32, 0x03,0x01,0x7F,0x01,0x03, 0x3F,0x40,0x40,0x40,0x3F, 0x1F,0x20,0x40,0x20,0x1F, 0x3F,0x40,0x38,0x40,0x3F,
 0x63,0x14,0x08,0x14,0x63, 0x03,0x04,0x78,0x04,0x03, 0x61,0x59,0x49,0x4D,0x43 };
struct OLED {
    static const uint8_t ADDR = 0x3C;
    bool cmd(uint8_t c) { Wire.beginTransmission(ADDR); Wire.write(0x00); Wire.write(c); return Wire.endTransmission() == 0; }
    bool init() {
        static const uint8_t seq[] = {0xAE, 0xD5, 0x80, 0xA8, 0x1F, 0xD3, 0x00, 0x40, 0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x02, 0x81, 0x8F, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6, 0xAF};
        Wire.begin(); Wire.setClock(100000); bool ok = true; for (uint8_t i = 0; i < sizeof seq; i++) ok &= cmd(seq[i]); return ok;
    }
    /* write one 21-character line (uppercase only; other characters become blanks) into page row 0..3 */
    void line(uint8_t row, const char *s) {
        cmd(0x21); cmd(0); cmd(127); cmd(0x22); cmd(row); cmd(row);
        uint8_t col = 0; uint8_t buf[16]; uint8_t n = 0;
        auto put = [&](uint8_t b) { buf[n++] = b; if (n == 16) { Wire.beginTransmission(ADDR); Wire.write(0x40); Wire.write(buf, n); Wire.endTransmission(); n = 0; } col++; };
        for (uint8_t i = 0; i < 21; i++) {
            char c = *s ? *s++ : ' '; if (c >= 'a' && c <= 'z') c -= 32; if (c < 0x20 || c > 0x5A) c = ' ';
            for (uint8_t k = 0; k < 5; k++) put(pgm_read_byte(&FONT5x7[(c - 0x20) * 5 + k])); put(0);
        }
        while (col < 128) put(0); if (n) { Wire.beginTransmission(ADDR); Wire.write(0x40); Wire.write(buf, n); Wire.endTransmission(); }
    }
    void clear() { for (uint8_t r = 0; r < 4; r++) line(r, ""); }
};
/* ------------------------------ DS3231 ------------------------------ */
struct RTC3231 {
    static uint8_t bcd(uint8_t v) { return (v >> 4) * 10 + (v & 15); }
    static uint8_t tobcd(uint8_t v) { return (uint8_t)(((v / 10) << 4) | (v % 10)); }
    static uint32_t days_from_civil(int y, int m, int d) { y -= m <= 2; int era = y / 400; int yoe = y - era * 400; int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1; int doe = yoe * 365 + yoe / 4 - yoe / 100 + doy; return (uint32_t)(era * 146097 + doe - 719468); }
    struct T { uint8_t s, mi, h, d, mo; uint16_t y; };
    bool read(T *t) {
        Wire.beginTransmission(0x68); Wire.write(0); if (Wire.endTransmission() != 0) return false; if (Wire.requestFrom(0x68, 7) != 7) return false;
        t->s = bcd(Wire.read() & 0x7F); t->mi = bcd(Wire.read()); t->h = bcd(Wire.read() & 0x3F); Wire.read(); t->d = bcd(Wire.read()); t->mo = bcd(Wire.read() & 0x1F); t->y = 2000 + bcd(Wire.read()); return true;
    }
    bool write(const T &t) { Wire.beginTransmission(0x68); Wire.write(0); Wire.write(tobcd(t.s)); Wire.write(tobcd(t.mi)); Wire.write(tobcd(t.h)); Wire.write(1); Wire.write(tobcd(t.d)); Wire.write(tobcd(t.mo)); Wire.write(tobcd(t.y - 2000)); return Wire.endTransmission() == 0; }
    static uint32_t epoch(const T &t) { return days_from_civil(t.y, t.mo, t.d) * 86400UL + t.h * 3600UL + t.mi * 60UL + t.s; }     /* seconds since 1970 (fits uint32 until 2106) */
};
/* ------------------------------ HX711 ------------------------------ */
static inline int32_t hx711_read(uint8_t dout, uint8_t sck, bool *ready) {
    if (digitalRead(dout)) { *ready = false; return 0; } *ready = true; int32_t v = 0; noInterrupts();
    for (uint8_t i = 0; i < 24; i++) { digitalWrite(sck, HIGH); delayMicroseconds(1); v = (v << 1) | digitalRead(dout); digitalWrite(sck, LOW); delayMicroseconds(1); }
    digitalWrite(sck, HIGH); delayMicroseconds(1); digitalWrite(sck, LOW); interrupts();          /* 25th pulse: channel A gain 128 */
    if (v & 0x800000L) v |= 0xFF000000L; return v;
}
