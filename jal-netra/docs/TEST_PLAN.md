# Jal-Netra test and calibration plan (what must happen before any claim is made)

Nothing in this repository has been run on hardware. The simulations show that the algorithm and the electronics budget *can* reach the targets if the acoustic signal is as assumed. These tests replace assumptions with measurements, in this order. Stop and redesign if a gate fails.

## Gate 1 - the acoustic signal (1 day, bench, water-filled printed spool, no PCB needed)
Equipment: signal generator (6-cycle 1 MHz burst, 6 Vpp), oscilloscope with 100 MHz probes, two 10 mm 1 MHz PZT discs in the spool pockets (potted), a bucket and a small pump.
1. Fill the spool, remove air (tilt, tap). Transmit on A, observe B: **record the received peak amplitude and the arrival time** (expect 40.5 us at 20 C).
2. Gate: received amplitude at the piezo >= 1 mV peak (the budget in `docs/rx_budget.md` gives 22 ps per 1000 pairs at 1 mV). Below 0.3 mV the architecture needs a change (more drive voltage, matching layer, shorter path, 2 MHz).
3. Note crosstalk arriving before 40 us (electrical) and echoes after the main burst (3x ToF = 121 us); the capture window starts at 36.5 us to avoid the first.
4. Swap A/B and compare amplitude: > 3 dB difference means mis-matched transducers.

## Gate 2 - zero stability (3 days)
Spool filled and static (valves closed), inside a box. Log dt (1000 pairs every 10 s) while the water temperature drifts +-5 C. Fit offset = a + b x T. **Gate: residual after the fit < 100 ps rms** (about 0.6 L/h). The firmware's zero tracker (`jn_zero_update`) must reproduce this fit online.

## Gate 3 - flow calibration (1-2 days, gravimetric rig)
Rig: constant-head tank or pump, needle valve, collecting tank on a scale (0.1 g), stopwatch; flows 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20 L/min at two temperatures (15 and 35 C). For each point collect >= 2 kg or 60 s. Fit k_cal and the profile factor versus Re. **Gate: error < 3 % of reading from 0.2 to 20 L/min** and no sign error in reverse flow.

## Gate 4 - leak detection (2 weeks, a real flat)
Install on the main line; log. Introduce a 0.5 L/h drip (burette) at night: the firmware must flag within the 6 h window and never flag normal use (target: zero false alarms over 14 days). Test a burst (open a tap fully) at night.

## Gate 5 - environment and abuse
Pressure 10 bar for 1 h (water-proof, no creep), 60 C for 4 h, freeze (empty spool, -5 C) to check potting, air bubbles (aerated water) -> the firmware should report "dry/air" not a wrong flow, hot-water pulse.

## Gate 6 - compliance (outside this repository)
Drinking-water contact materials (printed PA12 is NOT acceptable for drinking water; production body must be a certified polymer or brass), BIS/legal-metrology approvals for a water meter if it is sold as a billing meter (it would not be: it is a monitor), electrical safety of the USB supply, EMC. All unverified.
