# 03 · Compliance, Safety and Legal Checklist

Most facts below come from consultant/vendor pages ([S]) or my background knowledge ([K]). **None is confirmed against official BIS, WPC or CPCB text.** Get a compliance consultant and test lab involved in Phase 0.

## 1. Product approvals (India)
| Topic | What the research found | Applies to | Action |
|---|---|---|---|
| BIS CRS (Compulsory Registration Scheme) | Mandatory for listed electronic/IT products; **IS 13252** cited for adapters/IT/AV equipment [S]; Bluetooth speakers cited under IS 616:2017 by vendors but CRS coverage not confirmed [S] | Speaker, controller, charger/adapter | Check the current BIS CRS list; get lab quote |
| Lithium battery | **IS 16046** (Part 2:2018) cited for lithium systems; power banks registered under IS 13252 [S]. LiFePO4 pack inside a speaker needs a certification route | Speaker/lights batteries | Choose certified cells/packs; ask BIS-recognised lab |
| Wireless | **WPC ETA** needed for Bluetooth and other de-licensed radio; authorised Indian representative for foreign makers; RF test in a recognised lab; import-licence rules disagree between sources [S] | Controller (Bluetooth), light hub (2.4 GHz), wireless mics | Use pre-approved radio modules; apply for ETA; confirm with WPC |
| E-waste and battery rules | E-Waste (Management) Rules 2022 reportedly cover many electronics; batteries under Battery Waste Management Rules 2022; EPR obligations for producers [S] | All electronics, batteries | Check thresholds, register if needed |
| Legal Metrology | Packaged-goods declarations apply [K] | Retail packs | Label MRP, quantity, maker, month/year |
| LED lighting safety | LED luminaire safety standards may apply to the light fixtures [K] | Light kit | Check applicable IS standards and test scope |
| Mains safety | Class II insulation, creepage/clearance, 150–270 V tolerance for Indian supply [K] | Any mains-powered unit | Design for it from day one |
| Customs/import | If importing parts or finished goods: duty, BIS/WPC at import [K] | ODM or imported modules | Check duty codes with a customs broker |

## 2. Safety design rules (all products)
1. **Hearing:** built-in limiter and a "party" level cap; documented maximum SPL; warning in manual.
2. **Battery:** LiFePO4 preferred; BMS with cell balancing, over-current, short-circuit, over/under-temperature and charge protection; thermal fuse; vented, flame-retardant enclosure; drop and crush tests; do not exceed airline limits without checking.
3. **Photosensitivity:** no flash above 3 per second by default; separate warned strobe mode; fade rates tested like the toy lamp.
4. **Optical safety:** no lasers in v1; LED optics eye-safe; surface temperature limits.
5. **Heat:** thermal derating for amplifiers and LED engines; temperature limits in 40–45 °C ambient.
6. **Water/dust:** target IPX4 splash for outdoors; test before claiming.
7. **Mains:** double insulation, strain relief, fuses, surge tolerance.
8. **Mechanical:** stable stands, handle load ratings, tip-over test.
9. **Children and clinical claims:** none; keep marketing claims factual.

## 3. Intellectual property and content
- Use **open/royalty-free DJ software** (for example Mixxx) and class-compliant MIDI/audio; verify the licence terms before shipping any bundled software or app.
- Bluetooth/codecs (aptX etc.) may carry licence fees; start with SBC/AAC.
- No licensed music bundled; include only royalty-free demo tracks. Public performance of music needs the user's own licences (e.g., venues) – state clearly.
- Trademark search for the name; design registrations for the industrial design.
- Patent landscape check around beat-synced lighting and DJ control layouts before launch.

## 4. Certification budget (very rough, assumption)
BIS CRS registrations (2–3 products) ₹3–8 lakh; WPC ETA (2 radios) ₹1–3 lakh; battery certification ₹2–5 lakh; EMC/safety tests ₹2–5 lakh; legal/IP ₹2–4 lakh. **Total ₹10–25 lakh and 4–8 months**, partly parallel to development.
