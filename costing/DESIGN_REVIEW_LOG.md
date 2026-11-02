# Design review log (2026-11-02): defects found by the in-depth review and what was done

Method: automated checks (`utility10/pcb/review.py` part identity, stock, capacitor voltage, LED current, decoupling, pull-ups; `utility10/pcb/pincheck.py` supply and ground pin names against the nets) plus a manual read of every diode, polarised part and transistor against the KiCad symbol and footprint pin conventions (diode pin 1 = cathode, pad 1 = cathode).

## Defects found and fixed

| # | Where | Defect | Effect if built | Fix |
|---|---|---|---|---|
| 1 | MITTI-NETRA D1, D2 | Schottky diodes from solar and USB into the charger were fitted backwards (cathode on the source) | The TP4056 would never receive power from solar or USB | Nets swapped and part rotated 180 degrees; copper unchanged; schematic regenerated; checks re-run |
| 2 | KINETIC controller D5, BioTray D5 | The "USB 5 V into +5V" diode was backwards (cathode on VBUS) | The 5 V buck output would back-feed the USB port, and USB could not power the logic | Same fix |
| 3 | Parts at LCSC | Out of stock: 100 nF 0603 (C14663), 10 nF 0603 (C57112), Everlight 0603 LEDs, WS2812B-Mini, 1x2 header; very low stock: 100 uF 35 V (85), 2x3 header (340) | Order would fail at the fab or stall | Replaced by in-stock equivalents with the same footprint (see `manuals/ORDERING_GUIDE.md`) |
| 4 | Green indicator LED | Everlight 518 nm green (Vf about 3.3 V) from a 3.3 V rail | Almost dark | Yellow-green KENTO KT-0603YG (Vf about 2 V) |
| 5 | Gas-Suraksha demo firmware | Drives the buzzer with plain on/off, which silences a passive magnetic buzzer | No sound | New board uses an ACTIVE buzzer (see its manual) |

## Checked and found correct
Flyback diodes (cathode to supply, anode to the driven node) on all buzzer, pump, fan and valve drivers; unidirectional TVS orientation (cathode to the positive rail); gate-clamp Zener orientation on the reverse-polarity PMOS stages; P-channel reverse-polarity stages (drain on the battery side); polarised capacitor orientation; LED orientation; NPN (B, E, C) and PMOS (G, S, D) pin order against the SOT-23 footprints; AP2112K pin order; supply and ground pin names of every IC against its symbol (0 errors on all 20 boards).

## Open recommendations (not blocking)
- Passive magnetic buzzers (12 mm, 16 ohm) are driven at 4.2 to 4.5 V from a transistor: the estimated current is above the 30 mA rating for continuous use; fine for short beeps, add a 22 ohm series resistor if the buzzer gets warm.
- Order confidence for BQ25570 (stock about 390), the 12 mm passive buzzer (140) and PESD5V0S1BA (175) is limited for volume orders.
- Nothing has been built: every conclusion here comes from files and datasheet reading, not from measurement.
