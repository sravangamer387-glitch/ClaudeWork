# 02 · Concept and System Architecture

Working name: **"PartyPod"** (placeholder). Everything below is a design hypothesis to be validated in Phase 0–1.

## 1. Product family (modular)
| SKU | Description | Role |
|---|---|---|
| **PP-C Controller** | 2-deck standalone DJ controller: USB-stick/SD playback, USB-C controller mode, 2 mic inputs, 16 pads, filter/echo/loop effects, BPM detect and sync, line/Bluetooth in, line/XLR out | Differentiator |
| **PP-L Light kit** | 4 battery RGBW pars + sync hub; beat/BPM sync from controller or microphone; DMX512 out for pro fixtures; app control | Differentiator |
| **PP-S Speaker** | 100 W peak home speaker, 150 Wh battery, mic input, light ring (phase 2) | Sold alone and as part of kits |
| **PP-X System bundle** | 2 x 300 W speaker + controller + light kit + stands + bag | Hero bundle |

## 2. Sizing (from `calcs/acoustics_power.py`, free-field model)
| Use case | Listener | Avg SPL | Amp power needed | Avg electrical draw | Battery 4 h | Pack weight (LiFePO4) |
|---|---|---|---|---|---|---|
| Living-room party, 1 speaker | 3 m | 85 dB | ~90 W | ~37 W | ~147 Wh | ~1.5 kg |
| Terrace party (60 people), 2 speakers | 5 m | 92 dB | ~630 W total | ~97 W | ~386 Wh | ~3.9 kg |
| Banquet / sangeet hall (200 people) | 8 m | 98 dB | ~3,200 W total | ~370 W | ~1,470 Wh | ~14.7 kg |

Assumptions: crest factor 12 dB, 3 dB power compression, 85 % class-D efficiency, 10 W idle, 100 Wh/kg pack-level, no room gain. **Conclusion: design for home and terrace (≤ about 600 W total); a banquet hall needs a conventional PA, not a battery-portable product.** Batteries above 100 Wh bring air-shipping and carriage limits (verify UN38.3 and airline rules).

## 3. System architecture
```
                       +-------------------+        line / XLR / Bluetooth        +------------------+
  USB stick / SD  ---> |   PP-C Controller | -------------------------------------> |   Any speaker    |
  Phone (BT, USB-C) -> |  SoC + DSP + USB  |                                       |   (PP-S or other) |
  Mics (x2) ---------> |  jog, faders, pads|                                       +------------------+
                       +---------+---------+
                                 | beat / BPM / spectrum / scene data
                       2.4 GHz (approved module)  or  DMX512 (RS-485 cable)
                                 v
                       +-------------------+     +------------+
                       |  PP-L sync hub    | --> | RGBW pars  | (battery, 2-3 h)
                       |  MCU + radio      |     | pixel bars | (later)
                       +-------------------+     +------------+
```
### 3.1 Audio and DJ core (PP-C)
- Application SoC or high-end MCU (Cortex-M7 class) with hardware floating point, 2 stereo decks, 24-bit/48 kHz, real-time time-stretch for tempo sync, USB audio + USB MIDI (class compliant).
- Playback from USB stick/SD (MP3/AAC/FLAC/WAV), BPM and beat-grid analysis (offline at load, cached on stick), loops, cue points, 8 filters/effects.
- Controller mode: sends MIDI to open DJ software on laptop/phone; also exposes a USB audio interface.
- Firmware structure follows the toy platform: portable C core + HAL + host tests. DSP algorithms (filter, echo, beat tracker) can be prototyped and tested in Python/C against recorded audio on this machine.
### 3.2 Lighting (PP-L)
- Light nodes: RGBW LED (10–20 W) with constant-current driver, 3 h battery (LiFePO4 or protected Li-ion), temperature sensor and derating.
- Sync: hub broadcasts beat/BPM/scene frames to nodes (approved 2.4 GHz module) and outputs DMX512 over RS-485 for pro lights.
- **Photosensitivity safety:** default flash rate ≤ 3 flashes/second; strobe is a separate, warned mode; smooth fades like the toy lamp (tested invariants).
- No lasers, no fog machines in v1 (eye-safety classes and fire/regulatory complexity).
### 3.3 Speaker (PP-S/PP-X)
- 2-way driver set, bass reflex or passive radiator, class-D amplifier (TPA3116/TPA3255-class [K]) with DSP: crossover, EQ, limiter, thermal and battery protection, "party" and "clear voice" voicings.
- Battery: LiFePO4 4S (12.8 V) for safety and cycle life; BMS with cell balancing, over-current, over/under-temperature, short-circuit; charge from BIS-approved adapter.
- Mechanical: IPX4 splash resistance target, ≤ 15 kg, trolley or carry handle, rear-vent fan only if needed.
### 3.4 App (optional, phase 3)
Phone app for light scenes, EQ, firmware update; not required for core use.

## 4. Key design decisions to confirm in Phase 1
1. SoC choice and open-software strategy (royalty-free).
2. Battery chemistry/format and where it is made/certified.
3. Radio approach for light sync (module with existing approvals vs own design).
4. ODM speaker vs own speaker design.
5. Enclosure process (injection vs rotomoulding vs wood) – tooling cost versus volume.
6. Wired mic vs wireless mic (wireless mic bands raise licensing questions; start with wired and Bluetooth).

## 5. Rough economics (top-down; `calcs/cost_model.py`)
| Product | Price | BOM guess | Contribution | Margin |
|---|---|---|---|---|
| A Home party speaker, 100 W | ₹14,999 | ₹7,500 | ₹908 | 7 % (needs ~₹20,100 for 25 %) |
| B DJ controller | ₹14,999 | ₹5,400 | ₹3,407 | 27 % |
| C Light kit (4 pars + hub) | ₹12,999 | ₹5,000 | ₹2,442 | 22 % |
| D Party System bundle | ₹59,999 | ₹22,300 | ₹13,004 | 26 % |

Marketplace fee model as in the toy files (GST 18 %, referral 8 % placeholder, closing ₹30, shipping ₹250–900, ads 12 %, returns 8 % of landed cost). **All BOM lines are guesses.** The toy work taught me that real design costing typically raises costs by 20–50 %, so treat these margins as optimistic until Phase 1 produces a designed BOM.
