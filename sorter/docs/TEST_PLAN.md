# SORTER test plan (bench steps not yet run)
A (PC): `cd firmware && make test`; `python3 vision/classify.py --selftest`; `python3 cad/gripper.py`.
B (belt): measure belt mm per step with a ruler over 1 m; set `steps_per_mm`; verify the S-curve start/stop with produce on the belt (no sliding).
C (timing): dummy items (painted wooden blocks) at known spacing; verify fire position error under 3 mm at three belt speeds by marking drop points; count missed/dropped.
D (vision): photograph 200 real items per class under the final lighting; measure accuracy; retrain thresholds or a model; never reuse the synthetic thresholds.
E (handling): drop-test and bruise-test: 100 items through the picker; inspect for damage 24 h later.
