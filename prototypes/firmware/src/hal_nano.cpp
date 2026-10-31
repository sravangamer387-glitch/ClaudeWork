#include <Arduino.h>
#include <SoftwareSerial.h>
#include "hal_nano.h"

/* ---------------- pin maps (Arduino Nano digital pin numbers; A0=14, A1=15) ---------------- */
#if defined(PRODUCT_RHYMES)
static const uint8_t BTN_PINS[] = {2, 3, 4, 5, 6, 7, 8};     /* PLAY NEXT PREV VOL+ VOL- LANG SLEEP, to GND, internal pull-up */
static const uint8_t LED_PINS[] = {9, 12};                    /* PLAY led, SLEEP led (via 330R) */
#define USE_MP3 1
#elif defined(PRODUCT_LAMP)
static const uint8_t BTN_PINS[] = {2, 4, 7};                  /* MODE TIMER SONG */
static const uint8_t LED_PINS[] = {5, 6, 9};                  /* R G B: PWM to logic-level MOSFET gates */
#define MOTOR_PIN 8                                           /* projector rotor via NPN/MOSFET */
#define USE_MP3 1
#elif defined(PRODUCT_CRICKET)
static const uint8_t BTN_PINS[] = {2, 3};                     /* BAT START */
static const uint8_t LED_PINS[] = {4, 5, 6, 7, 8, 9, 12};     /* lane LEDs 0..5, result LED */
#define BUZZER_PIN 13
#define TM_CLK 14                                             /* A0 */
#define TM_DIO 15                                             /* A1 */
#elif defined(PRODUCT_MIDI)
static const uint8_t BTN_PINS[] = {2, 3, 4, 5, 6, 7, 8, 9};   /* 8 buttons: PLAY1 CUE1 PLAY2 CUE2 + 4 pads */
static const uint8_t LED_PINS[] = {0};
#elif defined(PRODUCT_BEATLIGHT)
static const uint8_t BTN_PINS[] = {2};
static const uint8_t LED_PINS[] = {5, 6, 9};                  /* R G B PWM */
#else
#error "define one PRODUCT_* macro"
#endif

#define N_BTN (sizeof BTN_PINS / sizeof BTN_PINS[0])
#define N_LED (sizeof LED_PINS / sizeof LED_PINS[0])

#ifdef USE_MP3
static SoftwareSerial mp3(10, 11);                            /* RX=D10 (from module TX), TX=D11 (to module RX via 1k) */
#endif

/* ---------------- TM1637 4-digit display (bit-banged) ---------------- */
#ifdef TM_CLK
static uint8_t tm_buf[4];
static void tm_delay(void) { delayMicroseconds(5); }
static void tm_start(void) { digitalWrite(TM_CLK, HIGH); digitalWrite(TM_DIO, HIGH); tm_delay(); digitalWrite(TM_DIO, LOW); tm_delay(); }
static void tm_stop(void) { digitalWrite(TM_CLK, LOW); tm_delay(); digitalWrite(TM_DIO, LOW); tm_delay(); digitalWrite(TM_CLK, HIGH); tm_delay(); digitalWrite(TM_DIO, HIGH); tm_delay(); }
static void tm_byte(uint8_t b) {
    for (uint8_t i = 0; i < 8; i++) {
        digitalWrite(TM_CLK, LOW);
        digitalWrite(TM_DIO, (b & 1) ? HIGH : LOW);
        tm_delay(); digitalWrite(TM_CLK, HIGH); tm_delay();
        b >>= 1;
    }
    digitalWrite(TM_CLK, LOW); pinMode(TM_DIO, INPUT); tm_delay();   /* ACK slot: module pulls DIO low */
    digitalWrite(TM_CLK, HIGH); tm_delay(); digitalWrite(TM_CLK, LOW);
    pinMode(TM_DIO, OUTPUT);
}
static void tm_flush(void) {
    tm_start(); tm_byte(0x40); tm_stop();                                   /* auto-increment write */
    tm_start(); tm_byte(0xC0); for (uint8_t i = 0; i < 4; i++) tm_byte(tm_buf[i]); tm_stop();
    tm_start(); tm_byte(0x88 | 5); tm_stop();                               /* display on, brightness 5/7 */
}
#endif

/* ---------------- HAL functions ---------------- */
static uint32_t h_millis(void) { return (uint32_t)millis(); }
static bool h_button(uint8_t i) { return i < N_BTN && digitalRead(BTN_PINS[i]) == LOW; }
static void h_uart(const uint8_t *d, size_t n) {
#ifdef USE_MP3
    mp3.write(d, n);
#else
    (void)d; (void)n;
#endif
}
#if !defined(PRODUCT_LAMP) && !defined(PRODUCT_BEATLIGHT)
static bool is_pwm(uint8_t pin) { return pin == 3 || pin == 5 || pin == 6 || pin == 9 || pin == 10 || pin == 11; }
#endif
static void h_led(uint8_t i, uint8_t level) {
    if (i >= N_LED) return;
#if defined(PRODUCT_LAMP) || defined(PRODUCT_BEATLIGHT)
    analogWrite(LED_PINS[i], level);
#else
    if (is_pwm(LED_PINS[i])) analogWrite(LED_PINS[i], level); else digitalWrite(LED_PINS[i], level > 127 ? HIGH : LOW);
#endif
}
static void h_seg(uint8_t digit, uint8_t mask) {
#ifdef TM_CLK
    if (digit < 4) { tm_buf[digit] = mask; if (digit == 3) tm_flush(); }
#else
    (void)digit; (void)mask;
#endif
}
static void h_buzzer(uint16_t hz, uint16_t ms) {
#ifdef BUZZER_PIN
    if (hz == 0) noTone(BUZZER_PIN); else tone(BUZZER_PIN, hz, ms);
#else
    (void)hz; (void)ms;
#endif
}

const ap1_hal_t HAL = {h_millis, h_button, h_uart, h_led, h_seg, h_buzzer};

void hal_init(void) {
    for (uint8_t i = 0; i < N_BTN; i++) pinMode(BTN_PINS[i], INPUT_PULLUP);
#if !defined(PRODUCT_MIDI)
    for (uint8_t i = 0; i < N_LED; i++) { pinMode(LED_PINS[i], OUTPUT); digitalWrite(LED_PINS[i], LOW); }
#endif
#ifdef MOTOR_PIN
    pinMode(MOTOR_PIN, OUTPUT); digitalWrite(MOTOR_PIN, HIGH);        /* projector rotor on (simple prototype behaviour) */
#endif
#ifdef BUZZER_PIN
    pinMode(BUZZER_PIN, OUTPUT);
#endif
#ifdef TM_CLK
    pinMode(TM_CLK, OUTPUT); pinMode(TM_DIO, OUTPUT);
#endif
#ifdef USE_MP3
    mp3.begin(9600);
    delay(1500);                                                      /* MP3 module needs ~1 s to boot before commands */
#endif
}
