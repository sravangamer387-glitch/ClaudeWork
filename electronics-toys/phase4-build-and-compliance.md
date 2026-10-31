# Phase 4 · Build, Test and Compliance Plan

Status: plan. Verify every regulatory step with BIS, the test lab and a compliance consultant.

## 1. Platform architecture (shared across Wave 1)
**A. Audio board**
- MCU or voice/flash-player IC with SD or onboard flash, class-D amplifier, 0.5–1 W speaker, up to 8 buttons, LED driver, battery holder (3×AA/AAA), on/off switch, volume control.
- Power: alkaline AA/AAA only (no lithium in Wave 1). Battery compartment closed with a captive screw.
- Sound level limit: design for safe listening; confirm acoustic limit in the standards with the lab.
- Firmware features: language select, sleep timer, low-battery tone, factory test mode.
**B. Motor board**: H-bridge, 1–2 DC motors or servos, IR or ultrasonic sensors, touch bumper, speaker/LEDs.
**C. STEM kit board**: MCU, breadboard-style sockets, sensors, buzzer, LEDs, USB-less (avoid computer connectivity in Wave 1).

## 2. Design rules (apply to every product)
1. No radio, no lithium cells, no cameras, no app accounts in Wave 1.
2. Battery compartment: secured by screw; no button cells accessible to children; polarity marked.
3. Enclosure: ABS/PP, R≥2 mm edges, no small detachable parts for under 3.
4. Cables/wires: none exposed; low voltage only (≤ 4.5–6 V).
5. Conformal coating or sealed PCBs against moisture; no sharp solder tails.
6. Thermal: battery and motor temperatures within limits during stall/fault tests.
7. Label: age grade, battery type and installation, warnings, manufacturer address, MRP, month/year, lot code, EPR/e-waste marking where required.

## 3. Compliance workflow
| Step | Action | Notes |
|---|---|---|
| 1 | Pre-compliance: send 2 prototypes to a lab (Bharat Test House / Krishna Met Lab / Intertek) for IS 15644 and IS 9873 gap check | [S] labs; confirm scope |
| 2 | Freeze design; declare product family (same supply layout, chassis, power, battery) | grouping rule from [S] |
| 3 | BIS licence application for factory; lab test report on production-representative samples | domestic route claimed ~30–35 working days [S, unverified] |
| 4 | Radio products only: separate WPC/ETA approval before design freeze | Not in Wave 1; verify rules |
| 5 | E-waste rules: check whether you need EPR registration (CPCB); micro-enterprise exclusion reported [S] | verify |
| 6 | Battery Waste Management Rules: check producer obligations for alkaline batteries supplied | verify |
| 7 | Legal Metrology labelling | verify with CA/Legal Metrology |
| 8 | Marketplace documents: ISI licence number on listing only after issuance | |

## 4. Manufacturing flow
1. Prototype PCB (5–10 pcs) at a Hyderabad PCB/EMS lead (Metro Circuits, Tescom, Accord Power Digital Products, Argus Embedded) [S].
2. Pilot run 100 units: SMT, AOI, functional test jig, burn-in 24 h on sample.
3. Plastic enclosure: 3D-print/laser prototypes first; injection tooling only after the pilot sells (use moulders from the gravity-toys list).
4. Final assembly and packing at your own small unit or the EMS partner.
5. Outgoing QC: 100 % function test (every button, sound, LED, motor); AQL sampling for cosmetic/packaging; battery-compartment torque and drop test.
6. Traceability: lot code on PCB and box; keep test logs for 3 years.

## 5. Test plan (per product family)
Electrical safety and temperature rise; battery compartment security; drop, tumble and torque tests; sound pressure level; small-parts and sharp-edge checks; paint/plastic heavy-metal tests; label durability; EMC pre-check (radiated noise from motors and audio); 100-hour reliability on sample; environmental (35–40 °C, high humidity).

## 6. Vendor RFQ essentials (electronics)
Send BOM + Gerbers + firmware spec; ask for: SMT/AOI capability, MOQ, lead time, test-jig support, component sourcing and traceability, IPC-A-610 compliance, who owns the files and the firmware source, ESD controls, BIS experience, references. Insist that you hold the source code, Gerbers and BOM.

## 7. Phase gates
| Gate | Criteria |
|---|---|
| G1 Concept | Contribution ≥ 25 % on real quotes; no radio/lithium; family fits a platform |
| G2 Prototype | Passes internal function and drop tests; kids' play test (10 children) |
| G3 Pre-compliance | Lab gap report with no critical findings |
| G4 Pilot | 100 units, <2 % functional failures, packaging approved |
| G5 Launch | BIS licence in hand, listings approved, stock ≥ 2 months demand |
