# 04 · Bijli Meter Reader

**Tier A** · low-voltage electronics · prototype Rs 900 · price Rs 1299. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
People see the bill once a month. Meters flash an LED per fixed energy (the pulse constant is printed on the meter and varies by maker: 1000, 1600, 3200 imp/kWh appear in sources [S]). Reading it optically gives live watts and a running bill estimate with no wiring.

## How it works
A clip-on photodiode head sits on the meter's pulse LED. The unit counts pulses (20 ms debounce), shows live watts, kWh since reset and an estimated bill from slab rates you enter. **No mains contact.**

## What I verified (and what I did not)
Host tests: 1000 W for one simulated hour produces 1600 pulses and 1.000 kWh; watts from the pulse gap within 4%; idle shows 0 W; slab bill arithmetic; bounce rejected. Slab rates in the code are placeholders, **not a real DISCOM tariff**. Not verified: sensing under sunlight, different LED colours/meter types.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`bm_*`), demo build `firmware/release/bijli_meter.hex`. Nano pins: photodiode A0, LED D13 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (80×50×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Flash a 1 Hz LED at the head: count = 1/s; cover with ambient light: no spurious counts.

## PCB (rev A, first draft)
See `../pcb/README.md`; files in `../pcb/release/bijli/`.

## Prototype budget (Rs 900, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| LDR/photodiode + comparator | 100 |
| 4-digit display | 150 |
| Wires, clip | 150 |
| Power bank cable | 100 |
| **Total** | **900** |

## Designed production BOM (~2,000 units, estimate Rs 325)
| Item | Rs |
|---|---|
| MCU + crystal | 45 |
| Photodiode + amp | 25 |
| 4-digit display | 35 |
| Clip head + cable | 40 |
| Battery/USB | 30 |
| PCB | 30 |
| Enclosure | 50 |
| Packaging | 30 |
| Assembly + test | 40 |

## Economics (marketplace, GST 18 % assumed)
Price Rs 1299 → contribution Rs 366 (33%); BOM +30 %: Rs 252 (23%). The first-draft price was Rs 1099, which made too little margin, so it was raised.

## Manufacturing
Black ABS clip head to block ambient light; EMS for PCBA.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Meter types differ; some new smart meters have no accessible LED; customers may expect an app.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
