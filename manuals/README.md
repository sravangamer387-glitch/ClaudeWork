# Manufacturing manuals: index

Start with **[STANDARD_PROCEDURES.md](STANDARD_PROCEDURES.md)** (PCB ordering, SMT/THT assembly, soldering, programming, 3D printing, laser cutting, QA, packaging, compliance, troubleshooting) and the [templates](templates/). Each product has a `MANUFACTURING_MANUAL.md` with its bill of materials, build steps, calibration, end-of-line test and limits.

**Honest status:** nothing in this repository has been built, assembled or tested as hardware. 'Order-ready' means the automatic checks pass (KiCad DRC 0 errors, schematic equals layout, every part has a verified LCSC number, Gerber/BOM/CPL consistent): it does **not** mean an engineer has reviewed the layout. Treat the first batch as a prototype run.

## Utility tools

| Project | Manual | Ordering | Board | Order confidence | Works as intended | Main caveat |
|---|---|---|---|---|---|---|
| Seeti Counter | [manual](../utility10/01-seeti-counter/MANUFACTURING_MANUAL.md) | [ordering](../utility10/01-seeti-counter/ORDERING.md) | **order-ready** | Medium-High | Medium | firmware compiled, not run on hardware |
| Gas Taraju (LPG cylinder scale) | [manual](../utility10/02-gas-taraju/MANUFACTURING_MANUAL.md) | [ordering](../utility10/02-gas-taraju/ORDERING.md) | **order-ready** | Medium-High | Medium | load-cell calibration per unit |
| Fridge Door Guard | [manual](../utility10/03-fridge-door-guard/MANUFACTURING_MANUAL.md) | [ordering](../utility10/03-fridge-door-guard/ORDERING.md) | **order-ready** | Medium-High | Medium-High |  |
| Bijli Meter Reader | [manual](../utility10/04-bijli-meter-reader/MANUFACTURING_MANUAL.md) | [ordering](../utility10/04-bijli-meter-reader/ORDERING.md) | **order-ready** | High | Medium |  |
| Bijli Log | [manual](../utility10/05-bijli-log/MANUFACTURING_MANUAL.md) | [ordering](../utility10/05-bijli-log/ORDERING.md) | **order-ready** | High | Medium | OLED/RTC drivers untested |
| Chulha Timers | [manual](../utility10/06-chulha-timers/MANUFACTURING_MANUAL.md) | [ordering](../utility10/06-chulha-timers/ORDERING.md) | **order-ready** | Medium-High | Medium-High | display driver untested |
| Rain Alert Bell + plate | [manual](../utility10/07-rain-alert/MANUFACTURING_MANUAL.md) | [ordering](../utility10/07-rain-alert/ORDERING.md) | **order-ready** | Medium-High | Medium | plate: `rainplate` board |
| Tap Litre Meter | [manual](../utility10/08-tap-litre-meter/MANUFACTURING_MANUAL.md) | [ordering](../utility10/08-tap-litre-meter/ORDERING.md) | **order-ready** | Medium-High | Medium | needs bucket calibration |
| Masala Rack (laser-cut) | [manual](../utility10/09-masala-rack/MANUFACTURING_MANUAL.md) | [ordering](../utility10/09-masala-rack/ORDERING.md) | no PCB | Medium-High | Medium-High | kerf coupon first |
| Laptop Stand (laser-cut) | [manual](../utility10/10-laptop-stand/MANUFACTURING_MANUAL.md) | [ordering](../utility10/10-laptop-stand/ORDERING.md) | no PCB | Medium-High | Medium-High | stability limit stated |

## Products

| Project | Manual | Ordering | Board | Order confidence | Works as intended | Main caveat |
|---|---|---|---|---|---|---|
| 1 Desi Games Studio (print) | [manual](../products/01-desi-games/MANUFACTURING_MANUAL.md) | [ordering](../products/01-desi-games/ORDERING.md) | no PCB | Medium-High | Medium | language + fact review before print |
| 2 Kalakriti Automata (laser) | [manual](../products/02-automata/MANUFACTURING_MANUAL.md) | [ordering](../products/02-automata/ORDERING.md) | no PCB | Medium-High | Medium | frame layouts provisional |
| 3 Prayog STEM lab kit | [manual](../products/03-prayog/MANUFACTURING_MANUAL.md) | [ordering](../products/03-prayog/ORDERING.md) | **order-ready** | High | Medium-High | sensors uncalibrated |
| 4 Jal-Rakshak tank controller | [manual](../products/04-jal-rakshak/MANUFACTURING_MANUAL.md) | [ordering](../products/04-jal-rakshak/ORDERING.md) | **order-ready** | Medium-High | Medium | **mains version cannot be made**: low-voltage prototype only |
| 5 Kheti-Mitra irrigation | [manual](../products/05-kheti-mitra/MANUFACTURING_MANUAL.md) | [ordering](../products/05-kheti-mitra/ORDERING.md) | **order-ready** | Medium-High | Medium | field trial required |
| 6 Gas-Suraksha leak alarm | [manual](../products/06-gas-suraksha/MANUFACTURING_MANUAL.md) | [ordering](../products/06-gas-suraksha/ORDERING.md) | **order-ready** | High | Low-Medium | **not certified, not for sale** |

## Toys (10)

| Project | Manual | Ordering | Board | Order confidence | Works as intended | Main caveat |
|---|---|---|---|---|---|---|
| 01 Reflex Raja | [manual](../toys10/01-reflex-raja/MANUFACTURING_MANUAL.md) | [ordering](../toys10/01-reflex-raja/ORDERING.md) | **order-ready** | Medium-High | Medium-High | shares the Desi Arcade board |
| 02 Taal Memory | [manual](../toys10/02-taal-memory/MANUFACTURING_MANUAL.md) | [ordering](../toys10/02-taal-memory/ORDERING.md) | **order-ready** | Medium-High | Medium-High | shares the Desi Arcade board |
| 03 Aloo Bomb | [manual](../toys10/03-aloo-bomb/MANUFACTURING_MANUAL.md) | [ordering](../toys10/03-aloo-bomb/ORDERING.md) | **order-ready** | Medium-High | Medium-High | shares the Desi Arcade board |
| 04 Beat Runner | [manual](../toys10/04-beat-runner/MANUFACTURING_MANUAL.md) | [ordering](../toys10/04-beat-runner/ORDERING.md) | **order-ready** | Medium-High | Medium-High |  |
| 05 Rangoli Spiro Gears | [manual](../toys10/05-rangoli-spiro/MANUFACTURING_MANUAL.md) | [ordering](../toys10/05-rangoli-spiro/ORDERING.md) | no PCB | Medium-High | Medium-High | kerf test first |
| 06 Paper Rocket Launcher | [manual](../toys10/06-paper-rocket/MANUFACTURING_MANUAL.md) | [ordering](../toys10/06-paper-rocket/ORDERING.md) | no PCB | Medium-High | Medium | projectile toy: lab review before sale; no drawings |
| 07 Tilt Maze | [manual](../toys10/07-tilt-maze/MANUFACTURING_MANUAL.md) | [ordering](../toys10/07-tilt-maze/ORDERING.md) | no PCB | Medium-High | Medium | gimbal drawn and checked; cut one test set |
| 08 Rubber-band Racer | [manual](../toys10/08-band-racer/MANUFACTURING_MANUAL.md) | [ordering](../toys10/08-band-racer/ORDERING.md) | no PCB | Medium-High | Medium-High | provisional cut file |
| 09 Marble Cricket | [manual](../toys10/09-marble-cricket/MANUFACTURING_MANUAL.md) | [ordering](../toys10/09-marble-cricket/ORDERING.md) | no PCB | Medium-High | Medium | provisional cut file; calibration drop |
| 10 Katha Cubes | [manual](../toys10/10-katha-cubes/MANUFACTURING_MANUAL.md) | [ordering](../toys10/10-katha-cubes/ORDERING.md) | no PCB | Medium-High | Medium-High | illustrations and proofreading missing |

## Bio / agri / civil / robotics programmes

| Project | Manual | Ordering | Board | Order confidence | Works as intended | Main caveat |
|---|---|---|---|---|---|---|
| KINETIC motion controller + vibration puck | [manual](../kinetic/MANUFACTURING_MANUAL.md) | [ordering](../kinetic/ORDERING.md) | **order-ready** | High | Medium | never run on a motor; AI on synthetic data |
| MITTI-NETRA soil + structure node | [manual](../mitti-netra/MANUFACTURING_MANUAL.md) | [ordering](../mitti-netra/ORDERING.md) | **order-ready** | High | Medium | modem is a plug-in breakout |
| BioTray vertical-farm controller | [manual](../biotray/MANUFACTURING_MANUAL.md) | [ordering](../biotray/ORDERING.md) | **order-ready** | Medium-High | Medium | calibration values are placeholders |
| BioWatt MFC harvester | [manual](../biowatt/MANUFACTURING_MANUAL.md) | [ordering](../biowatt/ORDERING.md) | **order-ready** | Medium-High | Low-Medium | cold start needs 600 mV; marginal on one MFC |
| GEONODE foundation monitoring | [manual](../geotech/MANUFACTURING_MANUAL.md) | [ordering](../geotech/ORDERING.md) | no PCB | Medium | Low-Medium | synthetic data; reuses MITTI-NETRA board |
| AQUAPONICS controller | [manual](../aquaponics/MANUFACTURING_MANUAL.md) | [ordering](../aquaponics/ORDERING.md) | no PCB | Medium | Low-Medium | runs on BioTray; biological limits are placeholders |
| SORTER bio-robotic platform | [manual](../sorter/MANUFACTURING_MANUAL.md) | [ordering](../sorter/ORDERING.md) | no PCB | Medium | Low | vision baseline only; uses KINETIC |
| AGROVER solar rover | [manual](../agrover/MANUFACTURING_MANUAL.md) | [ordering](../agrover/ORDERING.md) | no PCB | Medium | Low-Medium | dead-reckoning only; safety review needed |

## Other projects

| Project | Manual | Ordering | Board | Order confidence | Works as intended | Main caveat |
|---|---|---|---|---|---|---|
| Jal-Netra (engineering marvel) | [manual](../jal-netra/MANUFACTURING_MANUAL.md) | [ordering](../jal-netra/ORDERING.md) | **order-ready** | Medium-High | Low-Medium | **Gate 1 acoustic test first; not sellable** |
| ASTRADAND gesture wand (sci-fi project) | [manual](../astradand/MANUFACTURING_MANUAL.md) | [ordering](../astradand/ORDERING.md) | **order-ready** | Medium | Medium | software-verified; never built; Hindi names unreviewed |
| Gravity toys (5) | [manual](../gravity-toys/MANUFACTURING_MANUAL.md) | [ordering](../gravity-toys/ORDERING.md) | no PCB | Medium-High | Medium | all 5 drawn; Drop Quest has 60 verified levels |
| Wave 1 electronics toys | [manual](../electronics-toys/wave1/MANUFACTURING_MANUAL.md) | [ordering](../electronics-toys/wave1/ORDERING.md) | no released board | High | Low-Medium | AP1 board designed; MP3 module, display and buttons are bought-in |
| Prototype packs (10) | [manual](../prototypes/MANUFACTURING_MANUAL.md) | [ordering](../prototypes/ORDERING.md) | no PCB | Medium | Medium | bench prototypes |
| DJ / party system | [manual](../dj-setup/MANUFACTURING_MANUAL.md) | [ordering](../dj-setup/ORDERING.md) | no PCB | Medium | Low-Medium | programme plan; phase-0 prototypes D1/D2 in prototypes/ |


**Confidence columns:** see [`costing/CONFIDENCE.md`](../costing/CONFIDENCE.md) for the rubric and the reason behind every rating. Ordering how-to for any project: [`ORDERING_GUIDE.md`](ORDERING_GUIDE.md). Priced bills of materials: [`costing/BOM_COSTS.md`](../costing/BOM_COSTS.md).