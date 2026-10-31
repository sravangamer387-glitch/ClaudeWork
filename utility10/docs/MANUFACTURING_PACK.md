# Manufacturing pack (applies to all utility tools; per-tool details are in each README)

## Files that exist
| Tool type | Files ready | Files NOT ready |
|---|---|---|
| Laser (Masala Rack, Laptop Stand) | `out/*.svg`, `out/*.dxf` (CUT + ENGRAVE layers, mm), results of fit/strength checks | assembly drawings, jigs, packaging dieline |
| Electronics (8 tools) | tested C engines, Nano demo `.hex`, enclosure STL prototype shells, BOM with estimated costs, pin maps, end-of-line tests | **PCB schematic/layout/Gerbers**, production enclosure tooling, firmware for the final MCU, certification |

## RFQ template (send to 3 vendors per process)
- **Laser shop:** material (9 mm / 6 mm MDF, BWP ply, bamboo), sheet size 600×450 / 600×600, files DXF, kerf and tolerance ±0.2 mm, quantity breaks 100/500/1,000, deburr + sand, packing, lead time, sample price. Ask for a kerf test coupon first (slot width 8.95 mm for a 9 mm board; adjust).
- **PCBA/EMS (Hyderabad leads in `electronics-toys/phase1-market-and-rules.md`):** need a schematic and layout first; ask for DFM review, MOQ, price at 500/1,000/2,000, test jig cost, warranty on assembly, RoHS declaration, who sources the MCU.
- **Injection moulder:** only after 500 units sell from 3D-printed/laser shells; tool cost typically Rs 1.5–5 lakh per housing (assumption, get quotes).
- **Printing (manuals, boxes):** Hindi/Telugu/English quick-start card; Legal Metrology marks.

## PCB design rules to hand to the EMS (my recommendations)
Single 2-layer board, MCU ATmega328P (as the Nano demos) or a cost-down Cortex-M0; keep every product low-voltage (≤ 5 V); mains only through a certified bought-in USB adapter; reverse-polarity protection; pads for programming header; silkscreen version and date.

## Quality checks before shipping each unit
Run the end-of-line test listed in the tool README; log serial/batch; 24 h burn-in for sampled units (1 per 50); drop test of the housing from 1 m.

## Open items for the owner
Choose Tier A items first; commission schematic+layout (about 1–2 weeks per board, freelance) for Seeti Counter, Bijli Meter Reader and Rain Alert Bell; test the first prototype with 5 real users; get lab quotes if any claim touches safety.
