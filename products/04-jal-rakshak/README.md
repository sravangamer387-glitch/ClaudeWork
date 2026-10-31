# Product 4 · Jal-Rakshak Water-Tank Controller

Starts and stops an overhead-tank pump, protects it from dry running and short-cycling, survives power cuts, and tells the user what is wrong with a blink code. Status: **control logic built and tested against a simulated house; Nano prototype firmware compiles; no hardware built; mains-side design and certification not done.**

## 1. Behaviour (rules in `firmware/lib/jal_core.c`)
| Rule | Default |
|---|---|
| **Power-return delay** after any reset or power cut before the pump may start (protects the motor from voltage swings) | 60 s |
| Start only when the tank is **below LOW** and the **sump has water**; stop when **FULL** (debounced to ignore water ripple) | 3-5 s confirmation |
| **Dry-run protection:** sump probe dry for 5 s stops the pump; auto-retry after 10 min, up to 3 tries, then latched until reset | 10 min / 3 tries |
| **Minimum off time** against short-cycling | 120 s |
| **Probe-fault detection:** FULL wet while LOW dry (impossible) for 5 s stops the pump and latches | 5 s |
| **Run-time limit** learned from previous fills (+10 %); 30 min until a fill has been learned. Protects against a dead FULL probe or a leak | learned |
| Status blink code: 0 booting, 1 idle, 2 pumping, 3 dry, 4 probe fault, 5 run-time limit | |
| Probes use **AC excitation** (no electrolysis, no corroding probes) | |

## 2. Verification (`firmware/test/test_jal.c`: **20 checks pass**, sanitizers on)
A simulated 1,000 L tank, a 1,000 L sump with municipal supply only 6-8 am and 6-8 pm, a 0.5 L/s pump, a 790 L/day household profile, random 1-4 hour power cuts, probe ripple, and fault injection:
- **30 normal days:** 1.0 pump starts per day; **0 L overflow**; tank never below 176 L; **0 s of dry running** (the sump probe sits 30 L above empty); no run shorter than 5 minutes; **no start within 60 s of a power return; no restart within 120 s of a stop**; the pump only stops when the tank is really full (lowest level at a stop 976 L).
- **Sump runs out while pumping:** pump stops, one start only, fault latched (blink code 3), dry running 0 s.
- **Impossible probe combination:** pump stops and fault latches within 6 s; reset clears it.
- **Dead FULL probe:** the run-time limit stops the pump; overflow about **43 L (4 % of the tank)** in this scenario. This is a *limitation*: for other tank/pump combinations the installer must set the limit to about 1.1 × the fill time, otherwise a dead probe overflows more.
- **A real logic bug was caught:** the minimum-off timer started at power-up and stacked on the power-return delay, so the pump waited 120 s instead of 60 s. Fixed and tested.
- **Not verified:** real water, real probes, real motor currents, mains behaviour, EMC.

## 3. Hardware and prototype
- Prototype (low-voltage only): Arduino Nano clone 400 · 12 V mini pump 350 · relay module 80 · stainless probes 100 · bucket, tube 300 · resistors 50 · LED, buzzer 40 · breadboard, wires 250 · 12 V adapter 250 = **Rs 1,820** (estimates). Firmware: `release/jal_rakshak.hex` (3.2 KB, 7 % RAM); pins in `firmware/src/main_jal.cpp`. **Never connect mains to the prototype.**
- **Production requirements (not designed):** isolated low-voltage probe side (reinforced insulation to the mains side), certified isolated supply, relay or contactor rated for the pump's starting current (0.5-1 HP = 370-750 W, starting current 3-5 x), fuse, surge protection, creepage/clearance and slots on the PCB, IP54 enclosure, strain relief, installation manual. Have an electrical-safety engineer review before any mains build.

## 4. Economics (marketplace; `docs/econ.py`)
Designed production BOM **Rs 660** (the earlier top-down guess was Rs 395: the certified isolated supply, relay, probe cable and enclosure cost more). At **Rs 1,299 the product loses money**; **Rs 1,799: contribution Rs 308 (20 %), 5 % if BOM +30 %; Rs 2,199: Rs 574 (31 %), 18 % if +30 %.** Incumbent controllers are Rs 2,500-4,500 [S], so **Rs 1,999-2,199 is the recommended price**. Fixed launch costs (design review, safety/BIS testing, tooling): about Rs 4-8 lakh (assumption). Competition below: Rs 199-400 alarms.

## 5. Compliance
Mains-switching equipment: BIS CRS/electrical-safety applicability and the right standard must be confirmed with a lab (**I did not verify**); e-waste EPR check; Legal Metrology labelling; age/children warnings not needed but include electrical warnings. A **low-voltage-only alarm version** (battery, no mains) avoids most of this but competes with Rs 199-400 products.

## 6. Listing and manufacturing
Listing draft: "Jal-Rakshak Water Tank Pump Controller – Auto Start/Stop, Dry-Run & Overflow Protection, Power-Cut Delay | Hindi/Telugu Guide." Do not claim "BIS certified" until it is. RFQ: Hyderabad EMS (see Phase 1 leads in `electronics-toys`) for PCBA, test jig (probe simulator), and an injection moulder for the IP54 enclosure.

## 7. Risks
Electrical safety and liability (main risk); installation errors; probe fouling in hard water; margin sensitivity; incumbents' brand and dealer reach; settings per tank (limit time).
