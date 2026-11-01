# ASTRADAND design notes

## Architecture
```
 3 x AAA (4.5 V) -> slide switch -> AO3401A (reverse-polarity) -> +4V5 --+-> AP2112K-3.3 -> +3V3 -> ATmega328P, MPU-6050, I2C pull-ups
                                                                         +-> Q3 (AO3401A) <- Q4 <- D5 -> SS14 -> VLED -> 6 x WS2812B-Mini
                                                                         +-> haptic motor (NPN Q1 + flyback D2) ; battery divider 330k/100k -> A0
 MPU-6050 --I2C(400 kHz)--> ATmega328P --D6--> WS2812 data (3.3 V logic, VDD 4.1-4.3 V: VIH = 0.7 x VDD stays below 3.3 V)
 piezo (Murata 12x12) driven in antiphase from OC1A/OC1B (6.6 Vpp across the element)
```
## Power budget (estimates; measure at Gate 1)
| State | Current | Basis |
|---|---|---|
| Awake, idle (mana bar, dim) | about 20 mA | MCU 8 MHz 3.3 V about 4 mA, MPU-6050 gyro+accel about 4 mA, LDO 0.05 mA, six pixels at about 2 mA each |
| Casting (1.4 s effect) | up to about 140 mA peak | LED budget 1500 channel units = 20 mA x 1500/255 = 118 mA, plus piezo and motor bursts |
| Asleep | about 90 uA | MPU-6050 accel-only cycle about 20 uA, LDO 55 uA, divider 10 uA, leakage; pixels switched off by Q3 |
3 x AAA alkaline (about 1000 mAh to 3.5 V): about 40 h awake-idle, months asleep. WS2812 idle current is about 1 mA per pixel, which is why Q3 switches the supply off in sleep.

## Voltage domains and why
The MPU-6050 needs 2.375-3.46 V, so MCU and IMU run from the 3.3 V LDO (no level shifters). The ATmega328P at 3.3 V is inside its 8 MHz speed grade. A WS2812B needs a data high of 0.7 x VDD: with VDD about 4.2 V (battery minus the MOSFET and Schottky drops) that is 2.9 V, below the 3.3 V from the MCU; at a fresh 4.65 V pack without the Schottky it would be 3.26 V: marginal, hence D20.

## Gesture pipeline (50 Hz)
1. While the trigger is up: keep the last 12 gyro samples (bias estimate).
2. Trigger down: bias = mean of those samples; roll angle from gravity in the first 5 accel samples.
3. While held: rotate (gy, gz) by the roll, subtract bias, integrate into a 2-D path (degrees) stored as int16 in 1/16 degree (112 points max, 2.24 s).
4. Release: reject if extent < 12 degrees; resample to 16 points by arc length; centre and scale by the bounding box; compare to 6 templates at -20..+20 degrees rotation; accept the best if its mean point distance <= 0.14 and (second - best)/second >= 0.10.
Why integrate only while the trigger is held: it removes segmentation, bounds the drift to under 2.2 s, and makes "start" explicit for the player.

## Mechanical notes
Hilt 232 x 34 mm, wall 2.4 mm; board rails every 34 mm; 12 screw bosses on the split plane; offset light slit (7.4 mm wide, 52 mm long) above the pixels with a 6.8 mm diffuser crystal; battery saddle (inner 12.6 mm) under the board; decorative bands and grip flutes. First-pass dimensions: print, test-fit, adjust.

## Known weaknesses
MPU-6050 is end-of-life-ish (consider ICM-42688 or LSM6DS3TR-C with a code change); the router-generated PCB is unreviewed; WS2812 timing is software-bit-banged with interrupts disabled for about 200 us per frame (sampling at 50 Hz tolerates it; I2C reads are not interrupted); gyro integration drift limits useful gestures to about 2 s.
