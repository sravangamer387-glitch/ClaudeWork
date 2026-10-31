# Product 6 · Gas-Suraksha – plug-on LPG leak alarm (cylinder-side unit)

> **SAFETY STATUS: PROTOTYPE ONLY. NOT CERTIFIED. DO NOT SELL OR RELY ON IT AS A SAFETY DEVICE.**
> This package contains a tested alarm *engine* and a demo build. Nothing here has been tested with real gas, and a hobby metal-oxide sensor is not a certified gas detector. Test with a lighter-gas sample in a bag outdoors, never near ignition. Any commercial version needs a certified lab (electrical safety, EMC, gas-detector performance), a product-liability review and a lawyer's view on claims. Standards named below (IS 13432 for mechanical detectors, EN 50194-1 for domestic gas alarms with 10–20 % LEL alarm levels) come from my background knowledge and secondary sources and **must be verified**.

## 1. Product
A small unit that sits on the floor beside the LPG cylinder (LPG is heavier than air), strapped or placed in a puck-shaped housing (`enclosure/gas_puck_*.stl`, 90 × 60 × 38 mm, grille on the bottom face). USB 5 V power with 3 × AA backup. Green = OK, amber = warm-up/early warning, red + continuous buzzer = alarm, flashing = sensor fault. Silence button (5 minutes), test button. A relay output hook exists in the firmware for a future shut-off valve (not used in v1).

## 2. What is built and verified (`firmware/`)
- `lib/gas_core.{h,c}`: portable C99 alarm engine; **34 host checks pass** (gcc -Wall -Wextra -Wshadow, ASan + UBSan; `make test`).
- `src/main_gas.cpp` builds to `release/gas_suraksha_demo.hex` for an Arduino Nano (7.3 kB flash, 345 B RAM) with watchdog.

| Behaviour | Verified by test |
|---|---|
| 24 h of clean air with ±25-count day/night swing: no alarm, no warning | yes |
| Fast leak (+0.5 counts/s): alarm after 310 s (when the alarm level is reached) | yes (simulated signal) |
| **Slow leak (+25 counts/h) cannot be "learned" as clean air**: alarms after 6.3 h | yes; the baseline may rise only 6 counts/h |
| 5 s alcohol-like spike ignored; 10 s spike alarms | yes |
| Gas present at power-up: baseline is **not** adopted, alarm still sounds and stays on for an hour | yes |
| Open or shorted sensor → fault chirp after 10 s; recovers when the signal returns | yes |
| Sensor aged beyond +80 counts drift → FAULT (latched) and **still alarms on real gas** | yes (this was a bug found and fixed during testing: the fault first flapped back to warm-up) |
| Silence: 5 minutes quiet, then re-sounds; re-sounds early if gas rises 50 % | yes |
| Test button, low-battery chirp, watchdog reset (short warm-up), millis() wrap-around, 200,000 random readings | yes |

**Limits:** thresholds (counts) are placeholders; a real unit needs a **two-point gas calibration at the factory** and temperature/humidity compensation, which are not done. Sensor cross-sensitivity (alcohol, hair spray, cooking fumes), poisoning by silicones and ageing are not modelled; the tests use synthetic signals I generated, not real sensor data.

## 3. How fast could it warn? (`sim/leak_time.py`, `docs/leak_time_table.md`)
Well-mixed 20 m³ kitchen model, time to reach 10 % LEL including firmware delay:
| leak g/min | 0.5 air changes/h | 2 | 5 |
|---|---|---|---|
| 1 | 110 min | never | never |
| 2 | 43 min | never | never |
| 5 | 16 min | 20 min | never |
| 20 | 4 min | 4 min | 5 min |

Reading: small leaks in a ventilated kitchen never reach 10 % LEL (which is not itself a hazard), medium leaks take tens of minutes, a large leak (regulator or hose failure) takes minutes. Gas pools low, so the real reading near the cylinder is higher than this mixed model; **not validated with real gas**.

## 4. Economics (`docs/econ.py`; marketplace; designed BOM Rs 515 vs my first guess of about Rs 400)
| Price Rs | Contribution Rs | Margin | If BOM +30 % |
|---|---|---|---|
| 799 | −125 | −18 % | −305 (−45 %) |
| 1,299 | 144 | 13 % | −36 (−3 %) |
| 1,799 | 477 | 31 % | 297 (19 %) |
| 2,299 | 810 | 42 % | 630 (32 %) |

**Finding:** at a Rs 799–999 "gadget" price the unit loses money. It only works at Rs 1,800+, a price at which buyers will expect a certified brand, and the model excludes certification, insurance and false-alarm returns. **Recommendation: do not list this on marketplaces until a lab quote and a liability opinion exist; treat the current package as a design study or consider selling to LPG distributors/housing societies after certification.**

## 5. Prototype (about Rs 1,200)
Nano 350 · MQ-6 module 150 · buzzer, 3 LEDs, 2 buttons, resistors 120 · breadboard/jumpers 150 · 3 × AA holder + USB power 150 · 3D-printed puck 200 (or cardboard) · lighter-gas test bag 50 · misc 100 = **about Rs 1,270** (estimates). Calibrate: record clean-air counts for a day, then counts in a bag of lighter gas; set `clean_air_nominal`, `alarm_delta` (≈10 % LEL equivalent), `alarm_abs` in `main_gas.cpp`.

## 6. Compliance checklist (all to verify)
Toys QCO does not apply. Likely relevant: electrical safety and EMC for the adapter/product, BIS requirements for the power adapter, EN 50194-1-style performance testing for domestic gas detectors (alarm at 10–20 % LEL, response time, drift, humidity), IS 13432 (mechanical LPG leak detectors), Legal Metrology labelling, e-waste and battery rules. Claims: never say "prevents accidents", "certified", or "detects all leaks".

## 7. Risks
Liability if it fails (the largest), false alarms (alcohol/cooking) causing returns, sensor poisoning/ageing, buyers treating it as a replacement for regulator inspection and ventilation, cheap uncertified imports on marketplaces.

## 8. Next steps
Real-sensor logging for a week in a kitchen → calibrate thresholds → get a lab quote and a liability opinion → decide whether to continue.
