/* TRISHNA fixed-length 48-byte telemetry frame (little-endian, packed).
 * Every record the device emits - event results, state transitions, errors, heartbeats, calibration snapshots - uses this one layout,
 * so a receiver can resynchronise on the 0xA5 0x5A preamble and reject corruption with the CRC alone.
 *
 * Offset Size Field            Meaning / scaling
 *  0     1   sync0            0xA5
 *  1     1   sync1            0x5A
 *  2     1   version          TR_FRAME_VERSION (1)
 *  3     1   type             tr_frame_type_t
 *  4     2   seq              frame counter, wraps at 65535
 *  6     4   unix_s           UTC seconds (0 when the clock is not set; see flag TR_FLAG_TIME_VALID)
 * 10     2   ms               milliseconds within the second (0..999)
 * 12     4   uptime_s         seconds since boot
 * 16     1   state            tr_state_t after the transition / at the time of the record
 * 17     1   prev_state       tr_state_t before the transition
 * 18     2   event_id         user-event counter (persists across reboots)
 * 20     2   flags            TR_FLAG_* bit field
 * 22     2   error_code       tr_error_t (0 = none)
 * 24     2   temp_cx100       sample temperature, degC x 100 (int16; INT16_MIN = no reading)
 * 26     2   ec25_x100        conductivity at 25 degC, mS/cm x 100 (0..655.35)
 * 28     2   cell_ohm         EC cell resistance, ohm (65535 = open / air)
 * 30     2   sg_x10000        specific-gravity estimate x 10000 (e.g. 10215 = 1.0215; 0 = none)
 * 32     2   a450_x1000       absorbance at 450 nm x 1000 (int16, log10(I0/I))
 * 34     2   turb_x1000       turbidity index x 1000 (scatter/transmission at 850 nm, blank subtracted)
 * 36     2   tx_blue_mv       transmission photodiode, blue LED on, dark-subtracted, mV
 * 38     2   tx_ir_mv         transmission photodiode, IR LED on, dark-subtracted, mV
 * 40     2   sc_ir_mv         scatter photodiode, IR LED on, dark-subtracted, mV
 * 42     2   vin_mv           12 V supply measured, mV
 * 44     1   hydration        tr_hydration_t
 * 45     1   quality          sample-quality score 0..100
 * 46     2   crc16            CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF) over bytes 0..45
 */
#ifndef TRISHNA_FRAME_H
#define TRISHNA_FRAME_H
#include <stdint.h>
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif

#define TR_FRAME_LEN 48
#define TR_SYNC0 0xA5
#define TR_SYNC1 0x5A
#define TR_FRAME_VERSION 1

typedef enum { TR_FT_RESULT = 1, TR_FT_STATE = 2, TR_FT_ERROR = 3, TR_FT_HEARTBEAT = 4, TR_FT_CAL = 5, TR_FT_LIVE = 6 } tr_frame_type_t;

enum {
    TR_FLAG_TIME_VALID   = 1u << 0,   /* unix_s comes from SNTP */
    TR_FLAG_PRESENCE     = 1u << 1,   /* ToF sees a user */
    TR_FLAG_STREAM       = 1u << 2,   /* sump probe sees a urine stream */
    TR_FLAG_VALVE_OPEN   = 1u << 3,
    TR_FLAG_PUMP_FWD     = 1u << 4,
    TR_FLAG_PUMP_REV     = 1u << 5,
    TR_FLAG_AIR          = 1u << 6,   /* EC cell open: chamber not full */
    TR_FLAG_LEAK         = 1u << 7,
    TR_FLAG_OPT_SAT      = 1u << 8,   /* a photodiode channel saturated */
    TR_FLAG_SD_OK        = 1u << 9,
    TR_FLAG_TOF_OK       = 1u << 10,
    TR_FLAG_TEMP_OK      = 1u << 11,
    TR_FLAG_DILUTED      = 1u << 12,  /* sample EC too close to the rinse-water blank */
    TR_FLAG_CAL_DEFAULT  = 1u << 13,  /* EC / SG model still on factory defaults */
    TR_FLAG_FAULT_LATCH  = 1u << 14,
    TR_FLAG_FALLBACK_TRG = 1u << 15   /* event started by presence fallback, not by the sump probe */
};

#pragma pack(push, 1)
typedef struct {
    uint8_t  sync0, sync1, version, type;
    uint16_t seq;
    uint32_t unix_s;
    uint16_t ms;
    uint32_t uptime_s;
    uint8_t  state, prev_state;
    uint16_t event_id;
    uint16_t flags;
    uint16_t error_code;
    int16_t  temp_cx100;
    uint16_t ec25_x100;
    uint16_t cell_ohm;
    uint16_t sg_x10000;
    int16_t  a450_x1000;
    uint16_t turb_x1000;
    uint16_t tx_blue_mv;
    uint16_t tx_ir_mv;
    uint16_t sc_ir_mv;
    uint16_t vin_mv;
    uint8_t  hydration;
    uint8_t  quality;
    uint16_t crc16;
} tr_frame_t;
#pragma pack(pop)

#if defined(__cplusplus)
static_assert(sizeof(tr_frame_t) == TR_FRAME_LEN, "tr_frame_t must be 48 bytes");
#else
_Static_assert(sizeof(tr_frame_t) == TR_FRAME_LEN, "tr_frame_t must be 48 bytes");
#endif

uint16_t tr_crc16(const uint8_t *data, size_t len);
/* Fill sync, version and CRC; serialise into out[48] (explicit little-endian, independent of the host's struct layout). */
void tr_frame_seal(tr_frame_t *f, uint8_t out[TR_FRAME_LEN]);
/* Parse 48 bytes; returns 0 on success, -1 bad preamble/version, -2 CRC mismatch. */
int tr_frame_parse(const uint8_t in[TR_FRAME_LEN], tr_frame_t *f);
/* Saturating conversions used when filling the frame. */
uint16_t tr_u16_sat(float v);
int16_t tr_i16_sat(float v);

#ifdef __cplusplus
}
#endif
#endif
