/* Firmware for the rev B PCBs (ATmega328P-AU), pin maps taken from utility10/pcb/boards/*.py. Build: make boards (one hex per board).
 * -DBOARD=2 Gas Taraju | 3 Fridge Door Guard | 4 Bijli Meter Reader | 5 Bijli Log | 6 Chulha Timers | 7 Rain Alert | 8 Tap Litre Meter
 * (1 Seeti Counter has its own file seeti_prod.cpp; 9 Kheti-Mitra is products/05-kheti-mitra built with -DLED_PIN=7.)
 * STATUS: compiles and fits; the control logic is the host-tested engine in utilcore.c; the display/RTC/HX711 drivers (board_drivers.h) and the
 * UI flows below have NOT been run on real hardware. Treat the first prototype run as bring-up of this file as well as of the board. */
#include <Arduino.h>
#include <avr/eeprom.h>
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <avr/power.h>
#include "utilcore.h"
#include "board_drivers.h"
#ifndef BOARD
#define BOARD 3
#endif
static const uint8_t PIN_BZ = 9, PIN_LED = 7, PIN_BTN = 2;
static void beep(int ms) { tone(PIN_BZ, 2400, ms); }
static void clock_init() {
#if F_CPU == 4000000UL
    clock_prescale_set(clock_div_2);                                 /* fuses give 8 MHz RC; 4 MHz keeps the part inside its speed grade down to 1.8 V (2 x AAA, backup cells) */
#endif
}
static bool pressed(uint8_t pin, uint32_t *t0, bool *longp, uint16_t long_ms) {      /* returns true once on a short release; sets *longp when held for long_ms */
    bool d = digitalRead(pin) == LOW; uint32_t now = millis(); *longp = false;
    if (d && !*t0) *t0 = now ? now : 1;
    if (d && *t0 && now - *t0 >= long_ms) { *longp = true; return false; }
    if (!d && *t0) { bool shortp = now - *t0 < long_ms && now - *t0 > 30; *t0 = 0; return shortp; }
    return false;
}
#if BOARD == 3                                                       /* ---------------- Fridge Door Guard: reed D3 (LOW = closed), buzzer D9, LED D7, button D2 ---------------- */
static fd_t F;
void setup() { clock_init(); pinMode(3, INPUT_PULLUP); pinMode(PIN_BTN, INPUT_PULLUP); pinMode(PIN_BZ, OUTPUT); pinMode(PIN_LED, OUTPUT); fd_init(&F, 60000UL, 180000UL); beep(60); }
void loop() {
    fd_step(&F, millis(), digitalRead(3) == HIGH);
    if (F.sound == 1) beep(80); if (F.sound == 2) tone(PIN_BZ, 2000); else if (F.sound == 0) noTone(PIN_BZ);
    digitalWrite(PIN_LED, F.st != FD_CLOSED && (millis() / 500) % 2);
    if (digitalRead(PIN_BTN) == LOW) beep(40);                       /* test beep */
    delay(50);
}
#elif BOARD == 4                                                     /* ---------------- Bijli Meter Reader: SIG A0 (LOW = meter LED lit), TM1637 DIO D4 / CLK D3, reset button D2, LED D7 ---------------- */
#ifndef IMP_PER_KWH
#define IMP_PER_KWH 1600                                             /* set per meter model from the label: build with -DIMP_PER_KWH=3200 etc. */
#endif
static bm_t M; static TM1637 D;
void setup() { clock_init(); pinMode(PIN_LED, OUTPUT); pinMode(PIN_BTN, INPUT_PULLUP); D.init(3, 4); bm_init(&M, IMP_PER_KWH); D.text("bIJL"); delay(800); }
void loop() {
    static int lo = 1023, hi = 0; static uint32_t decay = 0, t0 = 0, view = 0; bool lg;
    int a = analogRead(A0); if (a < lo) lo = a; if (a > hi) hi = a; if (millis() > decay) { decay = millis() + 20000; lo++; hi--; }
    bool on = hi - lo > 40 && a < (lo + hi) / 2; digitalWrite(PIN_LED, on); bm_sample(&M, millis(), on);
    if (pressed(PIN_BTN, &t0, &lg, 2000)) view++;                    /* short press: next screen */
    if (lg) { M.pulses = 0; M.day_pulses = 0; }                      /* hold 2 s: reset the bill period */
    static uint32_t nx = 0; if (millis() > nx) { nx = millis() + 400;
        switch (view % 3) { case 0: D.number((int32_t)(bm_kwh(&M) * 100.0f + 0.5f), 1); break;                       /* kWh with two decimals (e.g. 12.34) */
                            case 1: D.number((int32_t)(bm_watts(&M, millis()) + 0.5f)); break;                        /* watts */
                            default: D.number((int32_t)(bm_bill(&M, bm_kwh(&M)) + 0.5f)); } }                         /* estimated bill in Rs */
    delay(2);
}
#elif BOARD == 5                                                     /* ---------------- Bijli Log: MAINS A0 (divider of VBUS), OLED + DS3231 on I2C, button D2, LED D7 ---------------- */
static pc_t P; static OLED O; static RTC3231 R; static bool have_rtc;
static void fmt2(char *p, uint8_t v) { p[0] = '0' + v / 10; p[1] = '0' + v % 10; }
static void epoch_to_str(uint32_t e, char *out) {                    /* "DD/MM HH:MM" from epoch seconds */
    uint32_t days = e / 86400UL, sod = e % 86400UL; int z = (int)days + 719468; int era = z / 146097; int doe = z - era * 146097; int yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365; int doy = doe - (365 * yoe + yoe / 4 - yoe / 100); int mp = (5 * doy + 2) / 153; int d = doy - (153 * mp + 2) / 5 + 1; int m = mp + (mp < 10 ? 3 : -9);
    fmt2(out, d); out[2] = '/'; fmt2(out + 3, m); out[5] = ' '; fmt2(out + 6, sod / 3600); out[8] = ':'; fmt2(out + 9, (sod % 3600) / 60); out[11] = 0;
}
static void set_clock() {                                            /* hold the button at power-up: short press = +1, hold 1.5 s = next field (year, month, day, hour, minute) */
    RTC3231::T t = {0, 0, 12, 1, 1, 2026}; static const char *name[5] = {"YEAR", "MONTH", "DAY", "HOUR", "MINUTE"}; uint8_t f = 0; uint32_t t0 = 0; bool lg;
    while (f < 5) {
        char l[22]; snprintf(l, sizeof l, "SET %s", name[f]); O.line(0, l); snprintf(l, sizeof l, "%04u-%02u-%02u %02u:%02u", t.y, t.mo, t.d, t.h, t.mi); O.line(1, l); O.line(2, "SHORT=+1  HOLD=NEXT"); O.line(3, "");
        while (true) { if (pressed(PIN_BTN, &t0, &lg, 1500)) break; if (lg) { f++; while (digitalRead(PIN_BTN) == LOW) {} t0 = 0; break; } }
        if (f >= 5) break; if (!lg) { switch (f) { case 0: t.y = t.y >= 2040 ? 2025 : t.y + 1; break; case 1: t.mo = t.mo % 12 + 1; break; case 2: t.d = t.d % 31 + 1; break; case 3: t.h = (t.h + 1) % 24; break; default: t.mi = (t.mi + 1) % 60; } }
    }
    R.write(t);
}
void setup() { clock_init(); pinMode(PIN_LED, OUTPUT); pinMode(PIN_BTN, INPUT_PULLUP); O.init(); O.clear(); pc_init(&P); RTC3231::T t; have_rtc = R.read(&t); O.line(0, "BIJLI LOG"); if (!have_rtc) O.line(1, "RTC NOT FOUND"); if (digitalRead(PIN_BTN) == LOW && have_rtc) { while (digitalRead(PIN_BTN) == LOW) {} set_clock(); } delay(600); }
void loop() {
    static uint32_t last = 0, t0 = 0, view = 0; bool lg;
    if (pressed(PIN_BTN, &t0, &lg, 1500)) view++;
    if (millis() - last >= 1000) {
        last += 1000; RTC3231::T t; uint32_t e = 0; if (have_rtc && R.read(&t)) e = RTC3231::epoch(t); else e = millis() / 1000;
        bool was = P.out; bool ok = analogRead(A0) > 250;           /* VBUS/2 through the divider: about 2.5 V at 3.3 V supply is ~775 counts; below ~250 = mains gone */
        pc_sample(&P, e, ok); digitalWrite(PIN_LED, !ok);
        char l[22]; char ts[12];
        if (view % 2 == 0) { O.line(0, ok ? "MAINS OK" : "POWER CUT"); snprintf(l, sizeof l, "CUTS %lu", (unsigned long)P.count); O.line(1, l); snprintf(l, sizeof l, "OUT %lu MIN", (unsigned long)(P.total_out_s / 60)); O.line(2, l);
            if (P.n) { uint8_t i = (P.head + PC_LOG - 1) % PC_LOG; epoch_to_str(P.start_s[i], ts); snprintf(l, sizeof l, "LAST %s", ts); O.line(3, l); } else O.line(3, "NO CUTS YET"); }
        else { for (uint8_t k = 0; k < 4; k++) { if (k < P.n) { uint8_t i = (P.head + PC_LOG - 1 - k) % PC_LOG; epoch_to_str(P.start_s[i], ts); snprintf(l, sizeof l, "%s %lum", ts, (unsigned long)(P.dur_s[i] / 60)); O.line(k, l); } else O.line(k, ""); } }
        (void)was;
    }
}
#elif BOARD == 6                                                     /* ---------------- Chulha Timers: buttons D2..D5, buzzer D9, TM1637 DIO A4 / CLK A5 ---------------- */
static ct_t C; static uint32_t press[4]; static TM1637 D;
void setup() { clock_init(); for (uint8_t i = 2; i < 6; i++) pinMode(i, INPUT_PULLUP); pinMode(PIN_BZ, OUTPUT); D.init(A5, A4); ct_init(&C); D.text("tIn "); }
void loop() {
    uint32_t now = millis();
    for (uint8_t i = 0; i < 4; i++) { bool d = digitalRead(2 + i) == LOW; if (d && !press[i]) press[i] = now ? now : 1; if (!d && press[i]) { if (now - press[i] < 1000) ct_add(&C, i, now, 60); press[i] = 0; } if (d && press[i] && now - press[i] >= 1000) { ct_ack(&C, i); ct_set(&C, i, now, 0); press[i] = 0xFFFFFFFFUL; } }
    for (uint8_t i = 0; i < 4; i++) if (press[i] == 0xFFFFFFFFUL && digitalRead(2 + i) == HIGH) press[i] = 0;
    uint8_t r = ct_step(&C, now); if (r) { if ((now / 250) % 2) tone(PIN_BZ, 2000); else noTone(PIN_BZ); } else noTone(PIN_BZ);
    static uint32_t nx = 0; if (now > nx) { nx = now + 250; uint32_t best = 0xFFFFFFFFUL; uint8_t ch = 0; for (uint8_t i = 0; i < 4; i++) if (C.active[i]) { uint32_t s = ct_remaining_s(&C, i, now); if (s < best) { best = s; ch = i; } }
        if (best == 0xFFFFFFFFUL) D.text("----"); else { char b[5]; uint32_t m = best / 60, s = best % 60; if (m > 99) { m = 99; } b[0] = '0' + m / 10; b[1] = '0' + m % 10; b[2] = '0' + s / 10; b[3] = '0' + s % 10; b[4] = 0; D.text(b, true); (void)ch; } }
    delay(10);
}
#elif BOARD == 7                                                     /* ---------------- Rain Alert: plate drive A2, sense A0, mute D2, buzzer D9, LED D7 ---------------- */
static rain_t R; static uint32_t vnow = 0;
ISR(WDT_vect) {}
static void sleep_1s() {
    cli(); wdt_reset(); MCUSR &= ~_BV(WDRF); WDTCSR |= _BV(WDCE) | _BV(WDE); WDTCSR = _BV(WDIE) | _BV(WDP2) | _BV(WDP1);
    set_sleep_mode(SLEEP_MODE_PWR_DOWN); sleep_enable(); ADCSRA &= ~_BV(ADEN); sei(); sleep_cpu(); sleep_disable(); ADCSRA |= _BV(ADEN); wdt_disable(); vnow += 1000;
}
void setup() { clock_init(); pinMode(PIN_BTN, INPUT_PULLUP); pinMode(A2, OUTPUT); pinMode(PIN_BZ, OUTPUT); pinMode(PIN_LED, OUTPUT); rain_init(&R); R.wet_thr = 400; R.dry_thr = 250; beep(60); }
void loop() {
    digitalWrite(A2, HIGH); delay(2); uint16_t v = analogRead(A0); digitalWrite(A2, LOW);
    rain_step(&R, vnow, v, digitalRead(PIN_BTN) == LOW); digitalWrite(PIN_LED, R.raining);
    if (R.alert) { for (int i = 0; i < 25; i++) { if ((vnow / 400) % 2) tone(PIN_BZ, 1800); else noTone(PIN_BZ); delay(20); vnow += 20; rain_step(&R, vnow, v, digitalRead(PIN_BTN) == LOW); if (!R.alert) break; } noTone(PIN_BZ); }
    else sleep_1s();
}
#elif BOARD == 8                                                     /* ---------------- Tap Litre Meter: flow D3 (INT1), button D2, buzzer D9, LED D7, OLED I2C ---------------- */
#ifndef PULSES_PER_LITRE
#define PULSES_PER_LITRE 450.0f                                      /* typical YF-S201 value; calibrate per sensor lot with a 10 L bucket and rebuild / store */
#endif
static tap_t T; static volatile uint32_t pulses; static OLED O; static const float targets[4] = {5, 10, 20, 50}; static uint8_t ti = 1;
static void isr() { pulses++; }
void setup() { clock_init(); pinMode(3, INPUT_PULLUP); pinMode(PIN_BTN, INPUT_PULLUP); pinMode(PIN_BZ, OUTPUT); pinMode(PIN_LED, OUTPUT); attachInterrupt(digitalPinToInterrupt(3), isr, FALLING); O.init(); O.clear(); tap_init(&T, PULSES_PER_LITRE); T.target_l = targets[ti]; }
static void fl(char *b, float v) { dtostrf(v, 6, 2, b); }
void loop() {
    static uint32_t t0 = 0, nx = 0; bool lg; noInterrupts(); uint32_t n = pulses; pulses = 0; interrupts(); tap_pulses(&T, millis(), n); tap_step(&T, millis());
    if (pressed(PIN_BTN, &t0, &lg, 1500)) { ti = (ti + 1) & 3; T.target_l = targets[ti]; T.target_hit = false; beep(40); }       /* short press: next target 5/10/20/50 L */
    if (T.target_hit) { beep(100); }
    digitalWrite(PIN_LED, T.in_session);
    if (millis() > nx) { nx = millis() + 500; char l[22], b[10]; O.line(0, T.in_session ? "FLOWING" : "TAP LITRE METER"); fl(b, tap_session_l(&T)); snprintf(l, sizeof l, "SESSION%sL", b); O.line(1, l); fl(b, tap_day_l(&T)); snprintf(l, sizeof l, "TODAY  %sL", b); O.line(2, l); dtostrf(T.target_l, 4, 0, b); snprintf(l, sizeof l, "TARGET %sL", b); O.line(3, l); }
}
#else                                                                /* ---------------- Gas Taraju: HX711 DOUT D2 / SCK D3, TARE D8, LEDs D5 green D6 amber D7 red, buzzer D9, TM1637 DIO A4 / CLK A5 ---------------- */
static gas_scale_t G; static TM1637 D;
struct Cal { int32_t zero; float cpk; float tare_kg; uint16_t magic; };
static Cal cal; static Cal EEMEM ee_cal = {0, 22000.0f, 15.3f, 0};
static const uint8_t PIN_TARE = 8;
static int32_t read_avg() { int32_t s = 0; for (uint8_t i = 0; i < 8; i++) { bool ok = false; int32_t v; do { v = hx711_read(2, 3, &ok); } while (!ok); s += v; } return s / 8; }
static void wait_press() { while (digitalRead(PIN_TARE) == LOW) {} delay(50); while (digitalRead(PIN_TARE) == HIGH) {} delay(50); while (digitalRead(PIN_TARE) == LOW) {} }
void setup() { clock_init();
    pinMode(2, INPUT); pinMode(3, OUTPUT); digitalWrite(3, LOW); pinMode(PIN_TARE, INPUT_PULLUP); for (uint8_t i = 5; i < 8; i++) pinMode(i, OUTPUT); pinMode(PIN_BZ, OUTPUT); D.init(A5, A4);
    eeprom_read_block(&cal, &ee_cal, sizeof cal); if (cal.magic != 0xC0DE) { cal.zero = 0; cal.cpk = 22000.0f; cal.tare_kg = 15.3f; cal.magic = 0xC0DE; }
    if (digitalRead(PIN_TARE) == LOW) {                              /* hold TARE at power-up: calibration. 1) empty plate, press TARE; 2) 20 kg on the plate, press TARE */
        while (digitalRead(PIN_TARE) == LOW) {} D.text("Zero"); wait_press(); int32_t z = read_avg(); D.text("20  "); wait_press(); int32_t c = read_avg();
        cal.zero = z; cal.cpk = (float)(c - z) / 20.0f; eeprom_update_block(&cal, &ee_cal, sizeof cal); D.text("donE"); delay(1500);
    }
    gs_init(&G, cal.zero, cal.cpk, cal.tare_kg, 14.2f); D.text("gAS "); delay(800);
}
void loop() {
    bool ok; int32_t c = hx711_read(2, 3, &ok); if (ok) gs_sample(&G, millis(), c);
    static uint32_t t0 = 0; bool lg; if (pressed(PIN_TARE, &t0, &lg, 1500)) { G.zero_counts = read_avg(); beep(40); }          /* short press: re-zero the empty plate */
    int p = gs_percent(&G); bool st = G.stable; digitalWrite(5, st && p > 30); digitalWrite(6, st && p <= 30 && p > 15); digitalWrite(7, st && p <= 15);
    if (st && p <= 15 && (millis() / 1000) % 60 == 0) beep(200);
    static uint32_t nx = 0; if (millis() > nx) { nx = millis() + 500; if (!st) D.text("----"); else D.number(p); }
}
#endif
