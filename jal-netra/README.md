# Jal-Netra ("water eye") - inline ultrasonic water meter and leak monitor

**The engineering challenge I chose:** measure household water flow with *no moving parts*, down to a **1 litre per hour** drip, using a 12 mm brass-and-polymer spool and a 170 MHz microcontroller, and decide from that signal alone whether a house has a leak or a burst. The physics is hard: at 1 L/h the two ultrasonic transit times (upstream and downstream, about 40.5 microseconds each) differ by **0.18 nanosecond**, about 1/5,000 of one carrier cycle, and the electronics may not drift by more than that.

**Status: designed, simulated and unit-tested; the schematic and board are rule-checked; the spool CAD is generated. Nothing has been built or measured on water.** `docs/TEST_PLAN.md` lists six gates; the first (does enough ultrasound reach the receiver?) can sink the whole architecture and must be run first.

## 1. Why an inline spool and not a clamp-on sensor
A clamp-on version (sensors strapped on the outside of a pipe) was my first idea. The research and a quick attenuation estimate rejected it for homes: most Indian domestic plumbing is PVC/CPVC/GI, and ultrasound passing four plastic wall crossings loses far more than a 12-bit receiver can recover; commercial clamp-on meters list plastic pipes as the hard case. The inline spool replaces the two pipe walls by water, which is what residential ultrasonic meters do. [S] Texas Instruments' reference designs (TIDM-1019 with the MSP430FR6047, and a TDC1000/TDC7200 chip set with a 52 ps time-to-digital LSB) show the same measurement approach in water meters.

## 2. How it measures
Two 1 MHz piezo discs face each other across a 60 mm measuring bore (12 mm diameter). Water enters and leaves through side ports (Z-body, CAD in `cad/`). A 6-cycle burst goes one way, then the other, 1000 pairs per measurement. The transit-time difference is
`dt = 2 L v / c^2` (L path length, v mean axial velocity, c sound speed in water). At L = 60 mm, c = 1482 m/s: 1 L/min = 10.7 ns, 1 L/h = 0.18 ns (table in `sim/physics.py`).
- **Phase, not threshold:** the received burst is sampled at 4 MS/s (12 bit, 64 samples), demodulated at 1 MHz (Hann-windowed I/Q) and the phase difference between the two directions gives dt = dphi / (2 pi f0). Averaging 1000 pairs shrinks the noise 30-fold.
- **Absolute time of flight** (envelope threshold crossing) gives c, hence **water temperature to about 0.2 C** with no sensor, and removes the temperature error of c^2.
- **Zero drift:** the electronics' own offset (several ns, drifting tens of ps per C) is learned only when the pipe is quiet (`jn_zero_update`: slow integrator plus temperature slope).
- **Flow profile:** laminar and turbulent flow average differently along the path; the profile factor depends on the Reynolds number (assumed model, to be calibrated on a rig).
- **Leak logic:** a state machine at 1 Hz: normal use (events), a continuous trickle with **no five-minute pause for 6 hours = leak**, more than 25 L/min for 2 minutes = burst, a garden hose is only "usage".

## 3. What was verified, with numbers
| Layer | Evidence |
|---|---|
| Physics model | `sim/physics.py` (Marczak sound speed 1482.4 m/s at 20 C, viscosity, profile factor) |
| Measurement chain "digital twin" | `sim/twin.py`, Monte Carlo: unbiased estimator; std of dt after 1000 pairs: **75 ps at 30 dB SNR, 24 ps at 40 dB**, i.e. about 0.42 / 0.13 L/h (`docs/twin_results.md`, `out/twin_overview.png`) |
| Same algorithm in C | `firmware/lib/jn_core.c`, `make test`: 18 checks pass with sanitizers; 1000-pair std **78 ps** (matches the Python twin), coarse arrival, physics, reverse flow sign, zero tracker residual **13 ps** after 2 h of a 12 C temperature ramp, leak scenario: **drip leak (0.02 L/min, 1.2 L/h) flagged at 8.0 h after it starts, burst flagged 2 minutes after it starts, zero false alarms** over three days of simulated normal use, a 15 L/min garden hose is not a leak. Compiles warning-free for the Cortex-M4F: 2.1 KB code (`make m4`) |
| Receive electronics | SPICE (`sim/lna.cir`): stage gains 20.1 dB and 40.9 dB, -3 dB band 1.5 kHz-14 MHz; noise/ADC budget in `docs/rx_budget.md` (best case 22 ps at 1 mV received amplitude) |
| Hardware | `hardware/`: KiCad schematic and 2-layer PCB (STM32G431, bridge-drive from two timer pins, clamp + mux + two OPA356 stages + gain switch, USB-C power, OLED/UART/SWD), own ERC and KiCad DRC results in `hardware/README.md` |
| Mechanics | `cad/spool.py`: Z-body 99 x 64 mm, 20 ml fluid volume, pressure drop 2.8 kPa at 10 L/min and 11 kPa at 20 L/min (loss coefficient 2.6 assumed), hoop stress 2.5 MPa at 10 bar with 4 mm walls |

## 4. Honest limits (read these)
1. **No acoustic measurement exists.** The received amplitude after a 60 mm water path is assumed (budget tables sweep 0.5-100 mV). Gate 1 of the test plan measures it.
2. The Monte Carlo covers white noise and quantisation only. Real limits will be **systematics**: electrical crosstalk, acoustic echoes, transducer mismatch, bubbles, scale on the faces, temperature gradients, and the zero drift. The zero tracker was tested against a *linear* offset model only.
3. Flow-profile factor and loss coefficient are textbook assumptions; accuracy claims (< 3 %) are targets, not results.
4. The PCB is 2-layer for a prototype; production should be 4-layer with a guarded receive trace.
5. The STM32 firmware around the core is a documented **skeleton** (`firmware/src/main_stm32g4.c`), not built for the target.
6. Materials for drinking-water contact, legal-metrology approvals and compliance are not addressed (not a billing meter).
7. **Economics:** designed BOM about Rs 2,970; at a Rs 5,499 consumer price the contribution is about zero (`docs/economics.txt`). The product only works commercially at about Rs 7,000+ (apartment blocks, tank-line monitoring, builders) or after a cost-down (amplifier, transducer sourcing).

## 5. Where things are
`sim/` physics, digital twin, receive-chain budget, SPICE, plots · `firmware/` tested core + target skeleton · `hardware/` KiCad project, Gerbers, BOM, STEP, fab notes · `cad/` spool and fluid-volume STLs, piezo reference · `docs/` results, economics, test plan.
