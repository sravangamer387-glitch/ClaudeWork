# Next Portfolio – Proposals for Your Review

Prepared 2026-10-31. **Nothing here is started. Approve, change or reject each proposal and I will build the approved ones end to end and save everything (repo + Drive).** Evidence tags: [S] found in web research, [K] my background knowledge, (assumption) my estimate.

## 0. Where the earlier work stands
Done and saved: gravity toys (research, 5 designs, physics checks, business pack), electronic toys (top 50, platform firmware/hardware/enclosures), DJ system plan, ten prototype build packs (₹690–2,120 each). **Still open, because they need people, hardware or a decision:** physical building/bench tests, Drop Quest puzzle solver (rules decision after kids try it), PCB layout, certification, content recording, price/part verification.

## 1. Rules I now apply when choosing products (learned from the toy work)
1. **Per-unit contribution decides everything.** Cheap electronic toys earned ₹44–75 per unit; products with a ₹300–500+ contribution (or B2B pricing) can pay back fixed costs.
2. **Prefer products I can design, simulate and verify completely** on this machine: firmware with tests, physics/kinematics simulation, CAD/laser files, print-ready art, manuals.
3. **Avoid radio, lithium, mains and medical/safety-critical claims in version 1**: they add certification cost and time (BIS CRS, WPC, battery rules).
4. **India-specific problem or language/culture fit**; local manufacture (laser, print, simple PCB) in Hyderabad.
5. **Every prototype ≤ ₹3,000.**
6. Design costs run 20–50 % above guesses, so I show margins at +30 % BOM too.

## 2. Evidence gathered
| Topic | Finding | Source |
|---|---|---|
| School STEM labs | About 10,000 Atal Tinkering Labs exist; Budget 2025 plans 50,000 more in government schools over five years. I found **no information on how kits are procured** (tenders, vendor lists) | [S] [IANS](https://ianslive.in/10k-atal-tinkering-labs-in-last-11-years-fuelling-innovation-from-schools-nirmala-sitharaman--20250606113109), [Business Today](https://businesstoday.in/amp/union-budget/story/union-budget-2025-govt-to-set-up-atal-tinkering-labs-in-50000-schools-over-five-years-462949-2025-02-01) |
| Water-tank controllers | Alarms sell at ₹199–400; automatic controllers (V-Guard, Havells) ₹2,500–4,500; Crompton sells a LoRa wireless controller. No market-size data found | [S] [Outlook Business](https://www.outlookbusiness.com/spotlight/pr-wire/crompton-simplifies-household-water-management-with-intellisense-smartpro), [IndiaMART](https://m.indiamart.com/proddetail/digital-water-level-controller-indicator-with-alarm-option-2856388867033.html?pos=1) |
| Soil moisture / irrigation | India soil-moisture sensor market about $12.9M (2025) rising to $34.8M by 2034; sensors ₹500–5,000; controllers ₹3,000–25,000 | [S] [IMARC](https://www.imarcgroup.com/report/en/india-soil-moisture-sensor-market), [Khetiwadi](https://khetiwadi.com/gadgets/smart-irrigation-controller) |
| Emergency LED lights | Start at about ₹200; **BIS IS 16102 (Part 1):2026 now covers LED lamps with non-removable rechargeable batteries**; licence holders had to move to the revised version by 2 Aug 2026 | [S] [Certification India](https://www.certification-india.com/en/india-updates-bis-requirements-for-led-lamps-standard-2026/), [Syska](https://ace.electronicsforu.com/buzz/new-products/led-bulbs/syska-launches-rechargeable-led-batten-in-india/) |

## 3. Long list (14 considered) and verdict
| # | Idea | Verdict |
|---|---|---|
| 1 | Desi card & board games (maths, cricket, GK, market) | **Propose** |
| 2 | Kalakriti automata kits (cam-driven Indian folk figures) | **Propose** |
| 3 | School STEM lab kit ("Prayog") | **Propose** |
| 4 | Jal-Rakshak water-tank controller | **Propose** (with certification caveat) |
| 5 | Kheti-Mitra irrigation controller | **Propose** |
| 6 | LPG / gas-leak alarm | Defer: safety-critical claims need standards testing; revisit with a lab partner |
| 7 | Rechargeable emergency LED light | Reject: price war from ₹200 and new IS 16102 scope for built-in batteries |
| 8 | Smart plugs / energy meters | Reject for now: mains + BIS CRS + radio approvals |
| 9 | WiFi/Bluetooth gadgets | Reject for now: WPC/ETA process |
| 10 | Generic Arduino-compatible boards | Reject: ₹300 clones, no margin |
| 11 | Component/transistor tester kit | Maybe later: small niche, fold into the STEM kit as a module |
| 12 | Festival LED décor controllers | Reject: seasonal, thin margins |
| 13 | Medical gadgets (oximeter etc.) | Reject: regulated |
| 14 | Drones | Reject: registration rules, high BOM |

## 4. The five proposals

Marketplace/B2B unit economics (`economics.py`; BOM lines are guesses, channel fees as in the toy files):

| Product | Channel | Price ₹ | BOM guess ₹ | Contribution ₹ | Margin | Margin if BOM +30 % |
|---|---|---|---|---|---|---|
| 1 Desi card & board games | marketplace | 599 | 120 | 272 | 48 % | 40 % |
| 2 Kalakriti automata kits | marketplace | 899 | 220 | 377 | 44 % | 35 % |
| 3 School STEM lab kit | B2B | 7,999 | 3,200 | 1,667 | 25 % | 9 % |
| 4 Jal-Rakshak tank controller | marketplace | 1,299 | 395 | 284 | 26 % | 13 % |
| 5 Kheti-Mitra irrigation controller | marketplace | 1,799 | 520 | 471 | 31 % | 19 % |

### Proposal 1 · Desi Games Studio (print-and-box games, no electronics)
- **Product:** four games for ages 7+, in Hindi, Telugu and English: *Cricket Dhamaka* (card game with overs and runs), *Ganit Ladder* (snakes-and-ladders for multiplication tables), *India Yatra* (general-knowledge cards), *Sabzi Mandi* (market game teaching change and percentages).
- **I will build:** rules, balance simulations (Monte Carlo of thousands of games to check fairness, length and tie rates), print-ready card decks and boards (PDF/SVG), box dielines, language versions, printer RFQ pack, listing copy, costing, play-test sheets.
- **Prototype cost:** ₹300–900 (printed at a local shop).
- **Why:** highest margin, lowest risk, no certification beyond toy rules (verify whether games for under-14s fall under the toys QCO), fully buildable by me.
- **Risks:** copycats (games are easy to copy: mitigate with art, language content, series); quiz facts must be verified; marketplace discovery.

### Proposal 2 · Kalakriti Automata Kits (hand-cranked laser-cut mechanisms)
- **Product:** four kits for ages 8+: dancing peacock (cam and follower), bullock cart (crank-rocker), modak-lifting Ganesh, rotating diya wheel (gear train). No electronics, no batteries.
- **I will build:** kinematic simulations (cam profiles, follower lift, pressure angle < 30°, no interference, crank torque), parametric laser-cut SVGs, assembly manuals, packaging, RFQ for Hyderabad laser shops, listing copy.
- **Prototype cost:** ₹600–1,200 (laser-cut MDF).
- **Why:** gift-market friendly, 35–44 % margin, culture fit, works with the same laser shops as the gravity toys.
- **Risks:** small parts and finger-pinch rules for children; assembly difficulty (mitigate with instructions and tolerance tests); cheap Chinese wooden puzzle competition.

### Proposal 3 · "Prayog" School STEM Lab Kit (ATL-style, B2B)
- **Product:** a shared sensor board plus 12 modules (temperature, light, sound, distance, pH-style analog input, force, etc.) with **20 experiments mapped to school science chapters** (mapping to be verified), student worksheets, teacher guide, data logging to a laptop with a free offline viewer.
- **I will build:** firmware library with host tests, 20 experiment write-ups with expected results and error analysis, the logging tool, board pin map/BOM, enclosure CAD, RFQ, price list for schools.
- **Prototype cost:** ₹2,500–3,000 (Nano + 6 modules).
- **Why:** 10,000 labs exist and 50,000 more are planned [S]; repeat orders; high price per sale.
- **Risks:** procurement route unknown (tenders/GeM/dealers); long sales cycle; **margin collapses to about 9 % if BOM runs 30 % over**, so design-to-cost matters; educational kits for 14+ may fall outside the toys QCO (get legal advice).

### Proposal 4 · Jal-Rakshak Water-Tank Controller
- **Product:** controller for overhead-tank pumps: starts the pump when the tank is low, stops when full, **dry-run protection, minimum-off time, 60-second power-return delay** (voltage-fluctuation protection), probe-fault alarm, AC-excited probes that do not corrode, regional-language LED/buzzer codes.
- **I will build:** controller firmware with host tests, a tank-and-pump simulation to verify no short-cycling and correct protection behaviour, schematic/pin map/BOM, IP54 enclosure CAD, installation guide, RFQ, listing copy.
- **Prototype cost:** ₹1,300–2,000 (12 V mini pump and bucket demo; **no mains in the prototype**).
- **Why:** real daily pain in Indian apartments and homes; incumbent controllers cost ₹2,500–4,500 [S].
- **Risks:** **mains switching means BIS CRS/electrical-safety certification and a safe design (isolation, creepage)**; a ₹199–400 alarm market undercuts the low end; margin about 13 % at +30 % BOM.

### Proposal 5 · Kheti-Mitra Irrigation Controller
- **Product:** corrosion-free capacitive soil-moisture sensors plus a controller that opens a 12 V valve by moisture and schedule, with rain/hold override and a buzzer/LED status; solar-ready design; regional-language quick-start card; for terrace gardens, nurseries and small farms.
- **I will build:** sensor calibration method, controller firmware with host tests, **a soil-water-balance simulation over a synthetic 90-day weather series to quantify water use against a plain timer** (with honest limits), schematic/BOM, IP65 enclosure CAD, field-test protocol, listing copy.
- **Prototype cost:** ₹1,800–2,600.
- **Why:** growing sensor market [S]; pricing headroom (₹3,000–25,000 competitors [S]).
- **Risks:** farmer adoption and field reliability (rain, dust, heat); selling to farmers needs dealers; savings claims must be proven in the field, not by simulation.

## 5. What I will deliver for every approved proposal
Requirements and spec; design (firmware / CAD / print art / mechanism, as applicable); **verification on this machine** (tests and simulations, with every failure reported); prototype build pack ≤ ₹3,000 with budget, wiring/assembly guide and acceptance tests; unit-cost model with +30 % sensitivity; compliance checklist; RFQ pack; listing copy; risks. Saved to the repo and mirrored to Drive, as before.

## 6. Recommended order
1. **Games** and **Automata** first: highest margin, no electronics, complete verification possible.
2. **Kheti-Mitra** and **Jal-Rakshak** next (low-voltage prototypes; certification plan in the report).
3. **Prayog STEM kit** after, once you know how you would sell to schools.

## 7. Questions for you
1. Which proposals do you approve (all five, a subset, or changes)?
2. Languages for the games: Hindi, Telugu, English as proposed, or others?
3. For Jal-Rakshak: are you willing to take on mains-certification work, or should I design a low-voltage-only version first?
4. Anything else you want added or removed from the list (a field or product idea of your own)?
