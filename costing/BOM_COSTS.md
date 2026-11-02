# Priced bills of materials (parts, live LCSC list prices)

Generated 2026-11-02 by `utility10/pcb/costing.py` from each board's `2_assembly/*_BOM_full.csv` and the LCSC product API. USD list prices, ladder price for the quantity bought; INR at an assumed **88 INR/USD**.

**What is and is not in the numbers:** parts only. Not included: bare PCB fabrication, assembly fees (setup, extended-part fees, placement), stencil, shipping, import duty and GST, cell/battery, enclosure, bought-in modules and cables. Planning figures for PCB and assembly are shown separately and are assumptions, not quotes: get a JLC quote before you order. Stock is as returned by LCSC on the run date and changes daily.

## Summary: parts cost per assembled board

| Board | Lines | Parts | 1 board USD | 1 board INR | 10 boards (each) USD | 100 boards (each) USD | 100 boards (each) INR | PCB fab planning (per order of 5) | Stock flags |
|---|---|---|---|---|---|---|---|---|---|
| arcade | 19 | 27 | 4.24 | 373 | 3.72 | 3.15 | 278 | US$8 | none |
| astradand | 25 | 49 | 27.69 | 2437 | 24.66 | 21.36 | 1880 | US$2 | none |
| beatrunner | 17 | 53 | 4.48 | 395 | 3.96 | 3.32 | 292 | US$8 | none |
| bijli | 16 | 23 | 3.16 | 278 | 2.85 | 2.48 | 219 | US$2 | none |
| bijlilog | 21 | 31 | 3.49 | 308 | 3.18 | 2.76 | 243 | US$2 | none |
| biotray | 38 | 67 | 10.82 | 952 | 9.64 | 7.69 | 677 | US$8 | none |
| biowatt | 14 | 29 | 5.96 | 525 | 5.10 | 4.17 | 367 | US$2 | none |
| chulha | 18 | 22 | 4.86 | 428 | 4.34 | 3.63 | 320 | US$2 | none |
| fridge | 18 | 24 | 4.38 | 386 | 3.86 | 3.27 | 287 | US$2 | none |
| gastaraju | 21 | 35 | 5.08 | 447 | 4.44 | 3.66 | 322 | US$2 | none |
| jalnetra | 39 | 78 | 10.10 | 888 | 9.01 | 7.66 | 674 | US$8 | none |
| kheti | 22 | 37 | 6.56 | 577 | 5.83 | 4.80 | 423 | US$8 | none |
| kinetic_ctl | 38 | 59 | 8.49 | 748 | 7.72 | 6.21 | 546 | US$8 | none |
| kinetic_vib | 4 | 5 | 5.55 | 488 | 4.85 | 4.00 | 352 | US$2 | none |
| mitti | 34 | 62 | 12.89 | 1134 | 11.40 | 9.22 | 811 | US$8 | none |
| prayog | 26 | 34 | 4.17 | 367 | 3.77 | 3.21 | 282 | US$8 | none |
| rain | 19 | 27 | 4.46 | 393 | 3.94 | 3.31 | 292 | US$2 | 1 |
| rainplate | 1 | 1 | 0.02 | 2 | 0.02 | 0.02 | 2 | US$2 | none |
| seeti | 24 | 36 | 4.75 | 418 | 4.22 | 3.56 | 313 | US$2 | none |
| tap | 19 | 28 | 4.44 | 391 | 3.92 | 3.31 | 291 | US$2 | none |

Per-board file: `costing/<board>_priced_BOM.csv` (every line with LCSC number, unit price, stock).

## Stock flags (fewer than 100 boards' worth in stock, or zero)

- **rain**: C19224 TVS 5V bidir (low stock, stock 175)

## Planning assumptions (not quotes)

- PCB fabrication: about US$2 (small) to US$8 (large) per order of 5 boards at a standard 2-layer, 1.6 mm spec; ENIG, 2 oz copper or other options cost more.
- JLC assembly: about US$8 setup per order plus per-part placement and a per-unique-part fee for extended parts; with many unique parts this can exceed the parts cost for 1 to 10 boards.
- Through-hole connectors listed as hand-soldered are in the parts total but not in the assembly fee.
