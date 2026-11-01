# Gas-Suraksha LPG leak alarm: manufacturing manual

> **SAFETY STATUS: PROTOTYPE / DESIGN STUDY ONLY. NOT CERTIFIED. DO NOT SELL IT OR RELY ON IT AS A SAFETY DEVICE.**
> A hobby metal-oxide sensor (MQ-6 class) is not a certified gas detector. This manual covers building a **bench prototype for study**; it deliberately gives no production, marketing or installation instructions. Commercial manufacture requires a certified lab (electrical safety, EMC, gas-detector performance), a product-liability review and a lawyer's view on claims. The standards named in the product README (IS 13432, EN 50194-1) are from background knowledge and must be verified. Never test with real gas near ignition: use a lighter-gas sample in a bag, outdoors.

## 1. What the prototype is
A puck-shaped unit (`enclosure/gas_puck_body.stl`, `gas_puck_lid.stl`, 90 x 60 x 38 mm, grille on the bottom face) to sit on the floor beside an LPG cylinder, USB 5 V with 3 x AA backup: green OK, amber warm-up/early warning, red + continuous buzzer alarm, flashing = sensor fault; silence button (5 min) and test button.

## 2. Parts (about Rs 1,270)
Arduino Nano clone, MQ-6 module (analog out AO), active buzzer, 3 LEDs (green, amber, red) with resistors, 2 buttons, breadboard/jumpers, 3 x AA holder + USB power, 3D-printed puck (or cardboard), a lighter-gas test bag.

Wiring (from `firmware/src/main_gas.cpp`): MQ-6 AO to **A0**; buzzer **D8**; green LED **D9**, amber **D10**, red **D11**; silence button **D2** and test button **D3** (to GND).

## 3. Build and flash
1. Wire as above; print the puck (STANDARD_PROCEDURES G) or use a box with a vent grille.
2. Flash `products/06-gas-suraksha/release/gas_suraksha_demo.hex` to the Nano (bootloader: `avrdude -p m328p -c arduino -P <port> -b 57600 -U flash:w:gas_suraksha_demo.hex:i`).
3. Let the MQ-6 heater warm up (the firmware shows amber during warm-up).

## 4. Calibration (prototype)
1. Record clean-air counts for a day.
2. Record counts in a bag of lighter gas (outdoors); set `clean_air_nominal`, `alarm_delta` (about 10 % LEL equivalent) and `alarm_abs` in `main_gas.cpp`, rebuild with `make hex`.
3. A real product needs a **two-point gas calibration per unit at the factory and temperature/humidity compensation: not done.**

## 5. Tests (prototype, the 34 host checks cover the engine)
Clean air 24 h: no alarm; synthetic fast/slow leaks alarm as designed; 5 s alcohol spike ignored, 10 s spike alarms; open/shorted sensor gives a fault chirp; silence works for 5 min; test button sounds the alarm. These are simulated-signal tests: **nothing here has been tested with real gas or real sensor data.**

## 6. What is not allowed or not done
Selling; claims like "prevents accidents", "certified", "detects all leaks"; installation near ignition sources; reliance as a replacement for regulator inspection and ventilation. Not done: real-sensor logging, thresholds, lab quote, liability opinion. Economics: at Rs 799-999 the unit loses money; it only works at Rs 1,800+ where buyers expect a certified brand.

## 7. Next steps (if continued)
Log a real MQ-6 in a kitchen for a week, calibrate thresholds, get a lab quote and a liability opinion, then decide.
