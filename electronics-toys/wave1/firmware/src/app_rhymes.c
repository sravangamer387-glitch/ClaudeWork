#include "ap1.h"

static const uint8_t SLEEP_MIN[] = {0, 15, 30, 60};
#define SLEEP_N ((uint8_t)(sizeof SLEEP_MIN / sizeof SLEEP_MIN[0]))

static void show(rhymes_t *r) {
    r->hal->led_set(RH_LED_PLAY, r->playing ? 255 : 0);
    r->hal->led_set(RH_LED_SLEEP, r->sleep_armed ? 255 : 0);
}

static void play_current(rhymes_t *r) {
    /* folders on the card are 01..0N (one per language), files 001..NNN */
    df_play_folder_track(&r->df, (uint8_t)(r->lang + 1u), r->track);
    r->playing = true;
    r->started = true;
}

void rhymes_init(rhymes_t *r, const ap1_hal_t *hal, uint8_t lang_count, const uint8_t *tracks_per_lang) {
    *r = (rhymes_t){0};
    r->hal = hal;
    r->lang_count = lang_count > RH_MAX_LANG ? (uint8_t)RH_MAX_LANG : lang_count;
    if (r->lang_count == 0) r->lang_count = 1;
    for (uint8_t i = 0; i < r->lang_count; i++) r->tracks[i] = tracks_per_lang[i] ? tracks_per_lang[i] : 1u;
    df_init(&r->df, hal, RH_VOL_CAP);
    df_cmd(&r->df, DF_CMD_SRC, 2);                 /* SD card */
    r->vol = df_volume(&r->df, RH_VOL_DEFAULT);
    r->track = 1;
    show(r);
}

void rhymes_event(rhymes_t *r, btn_evt_t e) {
    if (e.kind != BTN_EVT_PRESS) return;
    switch (e.idx) {
    case RH_BTN_PLAY:
        if (r->playing) { df_cmd(&r->df, DF_CMD_PAUSE, 0); r->playing = false; }
        else if (r->started) { df_cmd(&r->df, DF_CMD_PLAY, 0); r->playing = true; }
        else play_current(r);
        break;
    case RH_BTN_NEXT:
        r->track = (uint8_t)(r->track >= r->tracks[r->lang] ? 1u : r->track + 1u);
        play_current(r);
        break;
    case RH_BTN_PREV:
        r->track = (uint8_t)(r->track <= 1u ? r->tracks[r->lang] : r->track - 1u);
        play_current(r);
        break;
    case RH_BTN_VOLUP: r->vol = df_volume(&r->df, (uint8_t)(r->vol + 2u)); break;
    case RH_BTN_VOLDN: r->vol = df_volume(&r->df, (uint8_t)(r->vol >= 2u ? r->vol - 2u : 0u)); break;
    case RH_BTN_LANG:
        r->lang = (uint8_t)((r->lang + 1u) % r->lang_count);
        r->track = 1;
        play_current(r);
        break;
    case RH_BTN_SLEEP:
        r->sleep_idx = (uint8_t)((r->sleep_idx + 1u) % SLEEP_N);
        r->sleep_armed = SLEEP_MIN[r->sleep_idx] != 0;
        if (r->sleep_armed) r->sleep_deadline = r->hal->millis() + (uint32_t)SLEEP_MIN[r->sleep_idx] * 60000u;
        break;
    default: break;
    }
    show(r);
}

void rhymes_tick(rhymes_t *r) {
    if (r->sleep_armed && (int32_t)(r->hal->millis() - r->sleep_deadline) >= 0) {
        df_cmd(&r->df, DF_CMD_STOP, 0);
        r->playing = false;
        r->started = false;     /* after STOP a resume would not know the track: restart it instead */
        r->sleep_armed = false;
        r->sleep_idx = 0;
        show(r);
    }
}
