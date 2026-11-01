# SORTER: bio-robotic sorting platform (conveyor + vision + gentle pick/reject)

Programme 6 (mechanical + electrical + biotech + AI). **Status: tracking/timing core host-tested (28 checks), colour-vision baseline self-tested on synthetic images, compliant finger geometry generated; no machine built; no real produce ever imaged.**

## Architecture
- **Motion:** the KINETIC controller (see `kinetic/`) drives the conveyor (axis X) and a picker/reject mechanism (axes Y, Z) with jerk-limited S-curves, so the belt starts and stops without throwing produce. No new PCB.
- **Vision:** a camera over a controlled-light box on a Raspberry Pi/Banana Pi runs `vision/classify.py` (leaf disease fraction, fruit ripeness by hue) and sends `class` plus the belt position at the camera line.
- **Synchronisation:** `firmware/lib/sr_track.[ch]` stores each detection with the belt position (steps), fires the pick when the belt has moved `cam_to_pick - lead` mm (lead = actuator latency x belt speed), de-duplicates the same item seen in consecutive frames, refuses to act late, and counts missed/dropped items. Position-based timing keeps working through stops and speed changes.
- **Gentle handling:** `cad/gripper.py` -> `cad/out/finger.stl`, a Fin-Ray style compliant finger (TPU) that wraps the item; limit the grip pressure (actuator force / contact area) to what the item tolerates.

## Folders
`firmware/` (core + `make test`), `vision/classify.py` (`--selftest`), `cad/`, `docs/`.

## Honest limits
The vision is a colour-rule baseline calibrated on synthetic discs: real produce has shape, shadow, gloss and variety that will break it; collect labelled images from your line and train a proper model (the interface `classify_*` stays). Lighting control matters more than the algorithm (the ripe/overripe split depends on brightness). The finger geometry is untested: print one, load-test it with a force gauge, and tune rib count and wall thickness. Food-contact materials, hygiene and machine-guarding (pinch points on the belt and picker) are your responsibility. Not safety-rated.
