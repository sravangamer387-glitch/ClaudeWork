# Ordering guide: how to buy the boards and parts for any project in this repository

Applies to every project that has a circuit board or bought-in parts. Each project also has its own `ORDERING.md` next to its manual with the exact files, the part list with prices and the stock warnings. Prices and stock quoted in this repository come from LCSC on the run date (see `costing/BOM_COSTS.md`); **vendors, prices, shipping and customs rules change, so check each before paying.** Nothing here is a quotation.

## 1. The short path (a board with SMD parts)

1. Open the project's `ORDERING.md`. It lists the Gerber ZIP, the assembly BOM and the placement (CPL) file.
2. Order the board and SMD assembly at **JLCPCB** (section 3). Add the hand-fit parts to the same LCSC cart (section 4) so one shipment arrives.
3. Buy the modules, motors, batteries and similar items in India (section 5), or overseas if you can wait.
4. Have the printed and laser-cut parts made locally (section 5).
5. When everything has arrived, follow the project's `MANUFACTURING_MANUAL.md`: assemble, program, test.

## 2. Accounts and paperwork you need

- **JLCPCB** account (jlcpcb.com), one shipping address, payment by card or PayPal. A second address field for the *importer* may ask for a company name and tax ID for business orders.
- **LCSC** account (lcsc.com) for loose parts; it uses the same part numbers (C-numbers) that the BOM files carry.
- **GST invoice and business details:** if you buy in India for a business, give your GSTIN to Indian vendors to receive an input-tax-credit invoice.
- **Import code:** commercial imports into India normally need an Importer Exporter Code (IEC). Small personal courier shipments are treated differently. Ask the courier or a customs broker which applies to you before ordering in quantity.

## 3. JLCPCB: boards and assembly, step by step

1. *Order now*, upload the project's Gerber ZIP. Check the preview: outline, both copper layers, silkscreen, drills.
2. Standard settings used by all boards here: 2 layers, 1.6 mm FR-4, green mask, white silk, minimum quantity 5. Surface finish: lead-free HASL for ordinary boards; **ENIG** for boards with fine-pitch or LGA/QFN parts. Use 2 oz copper only where the project's manual says so.
3. Enable **PCB Assembly**, *Economic*, *Top side*. Upload the project's `*_JLC_BOM.csv` and `*_JLC_CPL.csv`.
4. In the parts step each BOM line must be matched to an LCSC part. If a part shows *out of stock*, do not accept a part with a different footprint. Use a same-value, same-package replacement and write it in the project's BOM so the record stays correct.
5. In the placement preview, compare pin 1 and polarity of every IC, diode, LED, polarised capacitor, USB-C and connector with the project's `*_assembly_top.pdf`. Ask JLCPCB support to rotate any wrong part before you approve.
6. Answer the engineering-review questions (they ask about rotations and missing parts) and pay. Typical lead time: 3 to 5 days build plus 5 to 10 days express shipping.
7. On arrival, inspect with the checklist in `manuals/STANDARD_PROCEDURES.md` (sections A and B) before powering anything.

Notes: some parts are *Extended* parts in the JLCPCB library and carry a per-part fee for each unique part on the order, which can exceed the parts cost for 1 to 10 boards. Through-hole connectors and pin sockets are not assembled in Economic assembly; they are in the "hand-fit parts" table of the project's `ORDERING.md`.

## 4. LCSC: loose parts

- Search by the C-number (for example `C1591`). Check stock, minimum order quantity and package (reel versus cut tape).
- Order together with JLCPCB when possible: the combined shipment saves courier fees. Add 10 to 20 per cent spares of resistors and capacitors.
- Keep the part page URL and the datasheet in your records; counterfeit risk is low at LCSC but is high on open marketplaces.

## 5. India: whom to approach and what to buy there

| Need | Suggested sources | How to approach |
|---|---|---|
| Common modules (ESP32 dev boards, relay modules, ultrasonic sensors, pH / EC / DO modules, load cells, HX711, LoRa modules) | Robu.in, Robocraze, ThinkRobotics, Sunrom Electronics, Amazon.in | Order online; quote the exact module name from the manual; ask for a GST invoice. |
| Branded ICs and connectors in small quantity | element14 India, Mouser India, DigiKey India | Order by manufacturer part number; compare landed price with LCSC plus customs. |
| Stepper motors, drivers, wheels, couplers | Robu.in, Robocraze, StepperOnline (overseas) | Check the motor current and shaft against the manual. |
| Li-ion, LiFePO4 cells and packs, solar panels, MPPT controllers | Authorised battery and solar dealers; Amazon.in with invoice | Always buy **protected** cells or packs with a BMS; avoid unbranded cells. Airlines and post restrict batteries: buy locally. |
| Laser-cut parts (acrylic, MDF, plywood) | Local laser-cutting shops (IndiaMART, Justdial, maker spaces) | Email the SVG/DXF from the repository with material, thickness, quantity; ask for a kerf coupon first. |
| 3D-printed parts (PLA, PETG, TPU) | Local 3D-print service bureaus, maker spaces; filament from Robu.in or Robocraze | Send the STL, material, layer height, infill, quantity. Ask for one sample before the batch. |
| Hardware, tubing, fasteners, enclosures | Local hardware shops, Robu.in, Amazon.in | Bring the part drawing; buy 20 per cent extra. |
| Aquarium and lab items (buffers, test kits, fish) | Local aquarium and lab-chemical suppliers; licensed aquaculture suppliers for live fish | Fish and chemicals need a competent person, not just a vendor. |

A request-for-quote message that works for any vendor:

> Subject: Quotation request: <project name>
> Please quote for <quantity> of the attached <file type: STL / SVG / BOM> in <material or part number>. Include unit price, GST, delivery time to <city>, minimum order, and warranty or return terms. Attached: <file names>.

## 6. What the parts price does not include

The priced BOMs in `costing/` are **parts only**. On top of that budget for:

- **PCB fabrication:** about US$2 for 5 small boards at standard options, more for large boards, ENIG or 2 oz copper.
- **Assembly:** a setup fee per order, a placement fee per part, and the Extended-part fee per unique part. Ask for the quote in the cart before paying.
- **Stencil**, if you assemble yourself.
- **Shipping:** courier express from China to India is a significant share on small orders.
- **Customs duty and GST** on the whole consignment value, plus the courier's clearance fee. The rate depends on the item classification and changes; ask the courier for the duty estimate, or a customs broker.
- **Exchange rate:** the INR figures use an assumed 88 INR per US dollar; update the constant in `utility10/pcb/costing.py` and re-run it.
- **Enclosure, battery, cables and modules** that are not on the board BOM.

## 7. Compliance before you sell (not needed for personal prototypes)

Radios (ESP32 Wi-Fi/BLE, LoRa, cellular) need the relevant India approvals (WPC equipment-type approval for the frequency used; use pre-certified modules). Mains-connected products, chargers and many electronics need BIS registration or testing. Gas, water and metering products may need legal-metrology or other approvals. Each project's manual lists what it knows. Ask an accredited test lab or a compliance consultant for the current rules before selling.

## 8. Checklist before you press *Pay*

- [ ] The Gerber ZIP, BOM and CPL are the ones from the project's `release` folder (not an older copy).
- [ ] The preview shows the right outline, drills and no missing layers.
- [ ] Every BOM line has a match and stock; any substitute has the same footprint.
- [ ] Polarity and pin 1 checked in the placement preview.
- [ ] Hand-fit parts and bought-in items are on an order too.
- [ ] Total cost including shipping, customs and GST is approved.
- [ ] You have a place to inspect and test the boards on arrival.
