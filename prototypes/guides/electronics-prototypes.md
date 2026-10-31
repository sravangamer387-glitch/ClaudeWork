# Build guide · Electronics prototypes (E1 E2 E3 D1 D2) on Arduino Nano

All five firmwares are in `prototypes/firmware/` and **compile for the ATmega328P** (`make`). Not yet run on hardware: expect to debug wiring and tune values on first power-up.

## 0. Tools and set-up
- Soldering iron, multimeter, wire cutters (one-time Rs 1,500). Breadboard/prototype board; the wiring tables below use Arduino pin numbers.
- **Power for prototypes: USB power bank or 5 V phone adapter** into the Nano USB port (clean 5 V). Battery operation is a later step: 3 x AA (4.5 V) is at the lower edge for a 16 MHz ATmega328P and sags as cells drain.
- Flashing: `sudo apt install avrdude` (or use Arduino IDE "Upload Using Programmer"), then  
  `avrdude -c arduino -p m328p -P /dev/ttyUSB0 -b 57600 -U flash:w:build/rhymes.hex` (older Nano bootloader; use `-b 115200` for the newer one). Build with `cd prototypes/firmware && make`.
- Never power LED strips or motors from the Nano 5 V pin; use separate supplies with **common ground**.

## 1. Pin maps (match `src/hal_nano.cpp`)
| Signal | E1 Rhymes | E2 Lamp | E3 Cricket | D1 Beat light | D2 MIDI ctrl |
|---|---|---|---|---|---|
| MP3 module TX → | D10 | D10 | – | – | – |
| MP3 module RX ← (1 kΩ in series) | D11 | D11 | – | – | – |
| Buttons (to GND, internal pull-ups) | D2 PLAY, D3 NEXT, D4 PREV, D5 VOL+, D6 VOL-, D7 LANG, D8 SLEEP | D2 MODE, D4 TIMER, D7 SONG | D2 BAT, D3 START | D2 spare | D2..D9 = 8 buttons |
| LEDs | D9 play, D12 sleep (330 Ω) | PWM D5 R, D6 G, D9 B → MOSFET gates | D4..D9 lane, D12 result (330 Ω) | PWM D5 R, D6 G, D9 B → MOSFET gates | – |
| Other | – | D8 rotor via MOSFET | D13 piezo, A0 TM1637 CLK, A1 TM1637 DIO | A2 microphone | A0..A7 pots, D10/D11 encoder |

## 2. MP3 module wiring (E1, E2)
| Module pin | Connect to |
|---|---|
| VCC | Nano 5V |
| GND | GND |
| RX | D11 through a 1 kΩ resistor |
| TX | D10 |
| SPK1 / SPK2 | speaker (3 W, 4 Ω) |

SD card (FAT32): E1 uses folders `01`, `02`, `03` (one language each) containing `001.mp3`, `002.mp3` … up to 10 files each (edit `TRACKS` in `main_rhymes.cpp` for other counts). E2 uses folder `01` for lullabies (looped).  
**Verify the command codes** (set volume 0x06, folder 0x0F, loop folder 0x17, stop 0x16) against the datasheet of the module you actually bought; clones differ.

## 3. MOSFET channel (E2, D1)
Logic-level N-MOSFET (IRLZ44N or similar): gate to Arduino pin through 100 Ω with 10 kΩ gate-to-GND pull-down; source to GND (common with the Nano); drain to the LED negative. 12 V strip positive to the 12 V adapter.  
E2 with 1 W LEDs on a 5 V rail: series resistor R = (5 − Vf) / I; for I = 250 mA use about 12 Ω / 1 W for red (Vf ≈ 2.0 V) and about 7.5 Ω / 0.5 W for green or blue (Vf ≈ 3.2 V). **Measure the current** before leaving it on.

## 4. Per-prototype notes and acceptance tests
### E1 Rhymes player
Build `make build/rhymes.hex`. Test: (1) power on, wait 2 s, press PLAY: folder 1 track 1 plays; (2) NEXT/PREV wrap at 10 tracks; (3) LANG cycles folders 1→2→3→1; (4) hold VOL+ presses: volume stops rising at the cap (20 of 30); (5) SLEEP once = 15 min then audio stops (LED on while armed); (6) PLAY after sleep restarts the track. Measure SPL at 25 cm at the cap with a phone meter app and record it.
### E2 Star lamp
`make build/lamp.hex`. Test: (1) MODE short press turns on warm white, again cycles colours, rainbow is the 5th; (2) colour changes are smooth (about 5 s end to end): **no flicker or flashing ever**; (3) long-press MODE turns off with fade; (4) TIMER 15 min then 10 s fade-out; (5) SONG loops the lullaby folder.
### E3 Cricket game
`make build/cricket.hex`. Test: (1) START begins; the ball LED walks D4→D9; (2) pressing BAT at the last LED = six, next = four, then two, one; early press = out; (3) display shows runs (2 digits), wickets, balls left; (4) game over after 12 balls or 2 wickets; (5) a missed ball sometimes bowls you out.
### D1 Beat-synced light
`make build/beatlight.hex`, open the serial monitor at 115200 baud: it prints `energy` and `bpm` each second. **Tune `ENERGY_SCALE` in `main_beatlight.cpp`**: silence should read below 6, a kick drum above 40. Set the mic module gain low (MAX9814: GAIN pin to VDD = 40 dB) to avoid noisy silence. Test with a phone playing tracks at 100, 120, 128 BPM near the mic: BPM readout within ±3 after 10 s; lights pulse on kicks, never more than 3 times a second, never fully dark while music plays.
### D2 MIDI controller
`make build/midi.hex`. The Nano sends MIDI bytes over USB serial at 115200; install a serial-to-MIDI bridge (Hairless MIDI) with a virtual MIDI port (loopMIDI on Windows, IAC on macOS). Then in Mixxx choose "PartyPod Prototype" and load `prototypes/mixxx/PartyPod-Proto.midi.xml`. Test: pots send CC 16–23, buttons notes 36–43, encoder CC 40 (1 = +1, 127 = −1). Jitter test: leave pots untouched for 1 minute: no messages should appear.

## 5. What these prototypes prove, and what they do not
They prove the **logic, the user experience and the sensor/audio chain** on cheap hardware. They do not prove production cost, certification (BIS/WPC), EMC, battery life, acoustic quality, or drop and heat survival. The production path (custom PCB, injection tooling) is in `electronics-toys/wave1/`.
