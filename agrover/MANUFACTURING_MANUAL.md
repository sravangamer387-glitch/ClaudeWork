# AGROVER solar field rover: build manual

> **Status: navigation, avoidance and power core host-tested in a simulated field (19 checks); chassis plates generated; no custom PCB; nothing built, driven or taken outdoors.**

## 1. Parts

ESP32-S3 dev board; 4 x 12 V geared DC motors with quadrature encoders; 2 x dual H-bridge drivers rated at least twice the stall current; 4S LiFePO4 pack with BMS; 50 W solar panel with a LiFePO4 MPPT controller (14.4 V absorption); 3 x ultrasonic sensors with 5 V to 3.3 V level shifting; 20 A fuse, main switch, reverse-polarity protection, **hardware emergency stop**; wheels, M3 hardware.

## 2. Build

1. Cut the plates: `python3 agrover/cad/chassis.py` writes `agrover/cad/out/base_plate.svg`, `top_deck.svg`, `sensor_bracket.svg` (laser-cutting rules in `STANDARD_PROCEDURES.md`; check slot sizes against your motors and battery). 2. Mount motors, battery on strap slots, drivers, controller; fuse next to the battery. 3. Compile `agrover/firmware/lib/rv_nav.c` into your ESP32 sketch; `cd agrover/firmware && make test` on a PC.

## 3. Commissioning

Wheels off the ground first: direction and encoder sign per wheel; then low speed in a clear area with the emergency stop in hand: straight line, turn, obstacle approach, return-to-charge thresholds (30 % return, 15 % sleep, 40 % wake with sun). See `agrover/docs/TEST_PLAN.md`.

## 4. Limits

Dead-reckoning plus reactive avoidance: no GNSS or SLAM, wheel slip will drift the pose. Ultrasonics miss thin stalks. SoC table is typical, not your pack. A moving robot with batteries outdoors needs a safety review. General rules: `manuals/STANDARD_PROCEDURES.md`.
