# 01 · Seeti Counter

**Tier A** · low-voltage electronics · prototype Rs 1080 · price Rs 999. Status: designed and verified as far as a computer can; **no prototype built, nothing field-tested.**

## Problem
Indian pressure-cooker recipes are written in whistles ('3 seeti'), and people forget to count. Induction cooktops with built-in counters exist (Prestige lists an automatic whistle counter [S]); there is no cheap retrofit for the ordinary gas-stove cooker.

## How it works
A heat-shielded clip puts a small microphone about 10 cm from the whistle. A Goertzel filter looks for the whistle's narrow tone; a whistle must last 0.4 s to count. After N whistles (button picks 1–6) a buzzer rings 5 times.

## What I verified (and what I did not)
Synthetic kitchen audio (noise + 100 Hz hum): 3/3 whistles counted, 0 counts for 100 ms clinks, 0 for loud noise alone, 0 for a different-frequency tone, 3/3 with whistle 1.5k vs noise 1.5k amplitude. **Limit found:** a whistle at amplitude 300 against noise 1200 counted 0 of 3, so mic placement and gain matter. The whistle frequency (2.8 kHz here) is an assumption: **record 5 real cookers and set it**.

## Firmware and electronics
Engine `firmware/lib/utilcore.c` (`seeti_*`), demo build `firmware/release/seeti_counter.hex`. Nano pins: mic A0, buzzer D9, button D2, LED D13 (wiring notes in the header of `firmware/src/main_util.cpp`). Low voltage only. A custom PCB is **not laid out**; the Nano demo and the pin map above are the starting point for the EMS.

Enclosure: `enclosure_body.stl` / `enclosure_lid.stl` (70×45×22 mm, 2.4 mm walls, watertight): a simple prototype shell; production tooling needs a proper design.

End-of-line test: Play a 2.8 kHz tone from a phone speaker at 10 cm for 1 s: counter must increment; play white noise: must not.

## Prototype budget (Rs 1080, limit Rs 3,000)
| Item | Rs |
|---|---|
| Nano clone | 400 |
| Mic module | 150 |
| Buzzer, button, LED | 80 |
| Breadboard, wires | 250 |
| Power bank cable | 100 |
| Cardboard box + clip | 100 |
| **Total** | **1080** |

## Designed production BOM (~2,000 units, estimate Rs 305)
| Item | Rs |
|---|---|
| MCU + crystal | 45 |
| Electret mic amp module | 40 |
| Buzzer | 12 |
| PCB | 30 |
| 2×AAA holder + switch | 18 |
| Heat-resistant clip/magnet mount | 40 |
| Enclosure | 50 |
| Packaging + Hindi/Telugu manual | 30 |
| Assembly + test | 40 |

## Economics (marketplace, GST 18 % assumed)
Price Rs 999 → contribution Rs 269 (32%); BOM +30 %: Rs 163 (19%). The first-draft price was Rs 899, which made too little margin, so it was raised.

## Manufacturing
PCBA at a Hyderabad EMS; ABS housing; mic port with a stainless mesh; heat limit: keep ≥ 10 cm from the vent and rated to 85 °C.
RFQ: price at 500 / 1,000 / 2,000 units, MOQ, lead time, tolerance/test report, sample cost; own the files.

## Compliance (to verify)
Battery safety, BIS requirement for any bought-in adapter, EMC, e-waste EPR, Legal Metrology labelling; no safety claims.

## Risks
Whistle frequency varies by cooker brand; steam moisture on the mic; kitchen heat; false counts from a second cooker.

## Next steps
Build the prototype from the budget → test with 5 users → adjust → RFQ.
