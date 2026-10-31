# Product 5 · Kheti-Mitra Irrigation Controller

Waters terrace gardens, nurseries and small plots **only when the soil is dry**, holds after rain, limits every watering and the daily total, and falls back to a safe timer if its sensors fail. Status: **control logic built and tested in a 90-day soil water-balance simulation; Nano prototype compiles; no hardware built; field behaviour unproven.**

## 1. Behaviour (`firmware/lib/kheti_core.c`)
| Rule | Default |
|---|---|
| Start watering below **48 %** of the sensor's dry-to-wet range (about 50 % of plant-available water in loam) | calibratable |
| Stop above **72 %** (about 90 % available water) | calibratable |
| Minimum interval between waterings (water must soak in before the sensor is trusted again) | 3 h |
| Maximum single watering / maximum per day | 20 min / 60 min |
| Rain hold after the rain sensor was last wet | 12 h |
| One sensor open/shorted: use the other; both failed: **fallback 5 min every 12 h**, status code 4 | |
| Status blink: 1 idle, 2 watering, 3 rain hold, 4 sensor fault, 5 daily limit | |
| Manual hold button | |

## 2. Verification (`firmware/test/test_kheti.c`: **22 checks pass**, sanitizers on)
- **Rule tests:** thresholds and hysteresis, 3 h interval, 20 min limit when the sensor does not respond, 60 min daily limit (even with a 1-minute interval and permanently dry readings), rain hold, single and double sensor failure, and 90 days of operation across the 49.7-day millisecond-counter wrap.
- **90-day water balance** (loam, 300 mm root zone, synthetic weather with about 2 mm/day average rain, 10 weather seeds, valve 0.25 mm/min):

| Strategy | Water applied mm | Deep percolation loss mm | Days below 50 % available water | Plant water use, % of potential |
|---|---|---|---|---|
| **Kheti-Mitra controller** | **256** | **27** | 0.5 | **100 %** |
| Timer 20 min every day | 450 | 233 | 0.0 | 100 % |
| Timer 10 min every day | 225 | 69 | 32.1 | 90 % |
| No irrigation | 0 | 15 | 70.8 | 57 % |

  So against a gardener's generous daily timer the controller **uses about 43 % less water and wastes about nine times less to deep percolation, while keeping plants at full water use**. A 10-minute timer saves similar water but leaves the plants short for a month. **A timer tuned every week to the weather would narrow the gap: I did not test that.**
- **A flaw in my first comparison was caught and fixed:** my first thresholds (35 %) looked better (142 mm, "0 stress days") only because the model let plants under-use water and my stress metric ignored it. After adding *actual versus potential plant water use* and setting thresholds from the usual 50 % allowed depletion, the saving fell from 68 % to 43 %.
- **Not verified (important):** real soil, real sensor response and drift, clogging, roots, plant types, rain-sensor behaviour, salt build-up; the simulation uses one soil type and synthetic weather. **Savings claims must be proven in a field trial before marketing.**

## 3. Prototype (about Rs 1,990)
Nano clone 400 · 2 capacitive soil sensors 240 · rain sensor 80 · 12 V solenoid valve 350 · MOSFET module 60 · 12 V adapter 250 · diode, resistors 20 · pot, soil, tubing, connectors 300 · breadboard, wires 250 · LED, button 40 = **Rs 1,990**. Firmware `release/kheti_mitra.hex` (6.5 KB flash, 16 % RAM); wiring in `firmware/src/main_kheti.cpp` (**flyback diode across the valve; never use the Nano's 5 V pin for the valve**). Calibrate each sensor (dry air / water) and edit the constants.

## 4. Economics (marketplace; `docs/econ.py`)
Designed production BOM **Rs 620** (earlier guess Rs 520). Price Rs 1,799: contribution Rs 355 (23 %), 9 % if BOM +30 %. **Rs 2,299: Rs 687 (35 %), 24 % if +30 %: recommended.** Competitor controllers cost Rs 3,000-25,000 [S]. Valve sold separately (or a bundle with a 12 V valve and tubing at about Rs 2,999). Fixed launch costs about Rs 2-4 lakh (field trial, tooling, testing; assumption).

## 5. Selling and field trial plan
Run a 60-day trial with 10 users (terrace gardens, 2 nurseries, 3 small farms) with a plain timer on the same plots as control; log water used, plant health, sensor drift, failures. Sell through nurseries/agri-input dealers; quick-start card in Hindi, Telugu, English; photo/video install guide.

## 6. Compliance and risks
Low voltage (12 V DC) with a certified adapter: check BIS CRS for the adapter and e-waste EPR; IP65 enclosure claims need testing; no safety-critical claims. Risks: sensor drift and fouling, farmer adoption, rain-sensor false triggers, valve clogging, theft, margin sensitivity.
