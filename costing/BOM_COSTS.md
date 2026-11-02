# Priced bills of materials (parts, live LCSC list prices)

Generated 2026-11-02 by `utility10/pcb/costing.py` from each board's `2_assembly/*_BOM_full.csv` and the LCSC product API. USD list prices, ladder price for the quantity bought; INR at an assumed **88 INR/USD**.

**What is and is not in the numbers:** parts only. Not included: bare PCB fabrication, assembly fees (setup, extended-part fees, placement), stencil, shipping, import duty and GST, cell/battery, enclosure, bought-in modules and cables. Planning figures for PCB and assembly are shown separately and are assumptions, not quotes: get a JLC quote before you order. Stock is as returned by LCSC on the run date and changes daily.

## Summary: parts cost per assembled board

| Board | Lines | Parts | 1 board USD | 1 board INR | 10 boards (each) USD | 100 boards (each) USD | 100 boards (each) INR | PCB fab planning (per order of 5) | Stock flags |
|---|---|---|---|---|---|---|---|---|---|
| arcade | 19 | 27 | 4.23 | 372 | 3.70 | 3.14 | 276 | US$8 | 1 |
| astradand | 25 | 49 | 27.74 | 2441 | 24.69 | 21.39 | 1882 | US$2 | 2 |
| beatrunner | 17 | 53 | 4.68 | 412 | 4.16 | 3.48 | 307 | US$8 | 2 |
| bijli | 16 | 23 | 3.15 | 278 | 2.84 | 2.48 | 218 | US$2 | 2 |
| bijlilog | 21 | 31 | 3.49 | 307 | 3.18 | 2.76 | 243 | US$2 | 2 |
| biotray | 38 | 67 | 10.85 | 955 | 9.66 | 7.71 | 679 | US$8 | 3 |
| biowatt | 14 | 29 | 5.96 | 525 | 5.11 | 4.17 | 367 | US$2 | 2 |
| chulha | 18 | 22 | 4.85 | 426 | 4.32 | 3.62 | 318 | US$2 | 1 |
| fridge | 18 | 24 | 4.38 | 385 | 3.86 | 3.27 | 288 | US$2 | 3 |
| gastaraju | 21 | 35 | 5.10 | 449 | 4.46 | 3.68 | 324 | US$2 | 4 |
| jalnetra | 39 | 78 | 10.10 | 888 | 9.01 | 7.66 | 674 | US$8 | 3 |
| kheti | 22 | 37 | 6.55 | 576 | 5.83 | 4.80 | 422 | US$8 | 2 |
| kinetic_ctl | 38 | 59 | 8.50 | 748 | 7.73 | 6.21 | 547 | US$8 | 3 |
| kinetic_vib | 4 | 5 | 5.53 | 487 | 4.83 | 3.99 | 351 | US$2 | 1 |
| mitti | 34 | 62 | 12.92 | 1137 | 11.43 | 9.25 | 814 | US$8 | 4 |
| prayog | 26 | 34 | 4.17 | 367 | 3.76 | 3.20 | 282 | US$8 | 2 |
| rain | 19 | 27 | 4.46 | 392 | 3.93 | 3.31 | 291 | US$2 | 3 |
| rainplate | 1 | 1 | 0.02 | 2 | 0.02 | 0.02 | 2 | US$2 | 1 |
| seeti | 24 | 36 | 4.74 | 417 | 4.22 | 3.56 | 313 | US$2 | 2 |
| tap | 19 | 28 | 4.44 | 390 | 3.91 | 3.31 | 291 | US$2 | 2 |

Per-board file: `costing/<board>_priced_BOM.csv` (every line with LCSC number, unit price, stock).

## Stock flags (fewer than 100 boards' worth in stock, or zero)

- **arcade**: C14663 100n (out of stock, stock 0)
- **astradand**: C14663 100n (out of stock, stock 0)
- **astradand**: C114583 WS2812B-Mini (out of stock, stock 0)
- **beatrunner**: C14663 100n (out of stock, stock 0)
- **beatrunner**: C72044 Red (out of stock, stock 0)
- **bijli**: C72043 Green (out of stock, stock 0)
- **bijli**: C14663 100n (out of stock, stock 0)
- **bijlilog**: C14663 100n (out of stock, stock 0)
- **bijlilog**: C72043 Green (out of stock, stock 0)
- **biotray**: C7442639 100u/35V (low stock, stock 85)
- **biotray**: C14663 100n (out of stock, stock 0)
- **biotray**: C72043 Green (out of stock, stock 0)
- **biowatt**: C14663 100n (out of stock, stock 0)
- **biowatt**: C57112 10n (out of stock, stock 0)
- **chulha**: C14663 100n (out of stock, stock 0)
- **fridge**: C14663 100n (out of stock, stock 0)
- **fridge**: C72043 Green (out of stock, stock 0)
- **fridge**: C57112 10n (out of stock, stock 0)
- **gastaraju**: C14663 100n (out of stock, stock 0)
- **gastaraju**: C72043 Green (out of stock, stock 0)
- **gastaraju**: C72038 Amber (out of stock, stock 0)
- **gastaraju**: C72044 Red (out of stock, stock 0)
- **jalnetra**: C57112 10n (out of stock, stock 0)
- **jalnetra**: C14663 100n (out of stock, stock 0)
- **jalnetra**: C72043 Green (out of stock, stock 0)
- **kheti**: C14663 100n (out of stock, stock 0)
- **kheti**: C72043 Green (out of stock, stock 0)
- **kinetic_ctl**: C7442639 100u/35V (low stock, stock 85)
- **kinetic_ctl**: C14663 100n (out of stock, stock 0)
- **kinetic_ctl**: C72043 Green (out of stock, stock 0)
- **kinetic_vib**: C14663 100n (out of stock, stock 0)
- **mitti**: C14663 100n (out of stock, stock 0)
- **mitti**: C72044 Red (out of stock, stock 0)
- **mitti**: C72043 Green (out of stock, stock 0)
- **mitti**: C7442639 100u/35V (low stock, stock 85)
- **prayog**: C14663 100n (out of stock, stock 0)
- **prayog**: C72043 Green (out of stock, stock 0)
- **rain**: C72044 Red (out of stock, stock 0)
- **rain**: C19224 TVS 5V bidir (low stock, stock 175)
- **rain**: C14663 100n (out of stock, stock 0)
- **rainplate**: C5116481 Cable (out of stock, stock 0)
- **seeti**: C72043 Green (out of stock, stock 0)
- **seeti**: C14663 100n (out of stock, stock 0)
- **tap**: C14663 100n (out of stock, stock 0)
- **tap**: C72043 Green (out of stock, stock 0)

## Planning assumptions (not quotes)

- PCB fabrication: about US$2 (small) to US$8 (large) per order of 5 boards at a standard 2-layer, 1.6 mm spec; ENIG, 2 oz copper or other options cost more.
- JLC assembly: about US$8 setup per order plus per-part placement and a per-unique-part fee for extended parts; with many unique parts this can exceed the parts cost for 1 to 10 boards.
- Through-hole connectors listed as hand-soldered are in the parts total but not in the assembly fee.
