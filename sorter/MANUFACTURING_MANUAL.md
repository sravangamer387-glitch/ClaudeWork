# SORTER bio-robotic sorting platform: build manual

> **Status: tracking core host-tested (28 checks), colour vision baseline self-tested on synthetic images, finger geometry generated; no machine built, no real produce imaged.** No new PCB: motion uses the KINETIC controller.

## 1. Parts

KINETIC controller (see `kinetic/`); NEMA17 motors and drivers for conveyor (X) and picker (Y, Z); conveyor belt and rollers; Raspberry Pi/Banana Pi and a camera in a controlled-light box; reject actuator or picker; 3D-printed TPU compliant fingers; guarding and an emergency stop.

## 2. Build

1. Print the finger: `python3 sorter/cad/gripper.py` writes `sorter/cad/out/finger.stl` (TPU, 3D-printing rules in `STANDARD_PROCEDURES.md`). Load-test it with a force gauge and tune rib count and wall thickness. 2. Assemble the conveyor and picker; fit guards over all pinch points. 3. Compile `sorter/firmware/lib/sr_track.c` into the controller firmware; `cd sorter/firmware && make test` on a PC. 4. `python3 sorter/vision/classify.py --selftest`; then collect labelled images from your own line and replace the colour rules with a trained model (the `classify_*` interface stays).

## 3. Calibrate and test

Measure steps per mm of belt, camera-to-pick distance and actuator latency; set the lead accordingly. Run empty belt, then dummy items, then produce; log missed and dropped items. See `sorter/docs/TEST_PLAN.md`.

## 4. Limits

Vision is a baseline calibrated on synthetic discs; real produce will break it. Lighting matters more than the algorithm. Finger geometry is untested. Food-contact materials, hygiene and machine guarding are your responsibility. Not safety-rated. General rules: `manuals/STANDARD_PROCEDURES.md`.
