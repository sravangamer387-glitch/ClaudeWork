# ASTRADAND test and bring-up plan (gates: do not skip a gate)

**Gate 0 (software, done):** `make test` in `astradand/firmware`: 83 checks; `sim/gesture_sim.py`: confusion matrices in `gesture_results.md`.

**Gate 1: board bring-up (1 day, 2 boards).**
1. Visual and short test; 4.5 V from a current-limited supply (50 mA): +3V3 = 3.3 V, TP1 = battery minus 0.05 V.
2. Flash with ISP (fuses lfuse 0xE2 hfuse 0xD9 efuse 0xFD, `astradand/firmware/release/astradand_8MHz.hex`).
3. I2C scan finds 0x68; WHO_AM_I register reads 0x68; gyro bias at rest within +-5 dps; accel z about 16384 counts.
4. LED switch Q3: D5 high powers the pixels (VLED about 4.2 V), D5 low gives under 10 uA; pixels light in order; **scope the data line: bit widths 3 cycles (375 ns) for 0 and 6 cycles (750 ns) for 1**; if any LED is wrong, adjust the asm.
5. Piezo plays the six tunes at the intended pitches; haptic motor pulses; battery reading within +-3 % of a multimeter.
6. Sleep current: with the wand still for 45 s, pack current under 100 uA (target); wake on a tap.

**Gate 2: recogniser on real hands (2 days, 10 people).** Log raw IMU traces over serial/SD (add a debug build), 30 casts per spell per person. Re-run `gesture_sim.py` on the recorded data: target 90 % correct, under 3 % wrong spell. Adjust templates (per-spell means from the data), D_MAX and the rotation tolerance; decide whether a left-handed mode is needed.

**Gate 3: user test (1 week).** Children 9-14 and adults: time to first successful cast, spells mistaken, battery life (target 20 h of play), comfort of the grip and trigger force (about 2-3 N).

**Gate 4: safety and compliance (outside this repository).** Toy standard (IS 9873) applicability, battery compartment screw closure (the shell is screw-closed), small parts (crystal, trigger cap, screws are retained), LED photobiological safety (diffused, but measure), noise at the ear (piezo under 85 dB at 25 cm), EMC, e-waste/EPR, Legal Metrology marks.

**End-of-line test per unit (production):** programme + verify; I2C scan; gyro bias check; draw circle and Z with a robot-arm or a hand test (2 of 2); LED colour sweep seen on all six pixels; sound and haptic on; battery 4.5 V +-0.2; sleep current; record on `manuals/templates/eol_test_sheet.md`.
