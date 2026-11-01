# Manufacturing manuals: index

Start with **[STANDARD_PROCEDURES.md](STANDARD_PROCEDURES.md)** (PCB ordering, SMT/THT assembly, soldering, programming, 3D printing, laser cutting, QA, packaging, compliance, troubleshooting) and the [templates](templates/). Each product has a `MANUFACTURING_MANUAL.md` with its bill of materials, build steps, calibration, end-of-line test and limits.

**Honest status:** nothing in this repository has been built, assembled or tested as hardware. 'Order-ready' means the automatic checks pass (KiCad DRC 0 errors, schematic equals layout, every part has a verified LCSC number, Gerber/BOM/CPL consistent): it does **not** mean an engineer has reviewed the layout. Treat the first batch as a prototype run.

## Utility tools

| Project | Manual | Board | Main caveat |
|---|---|---|---|
| Seeti Counter | [utility10/01-seeti-counter/MANUFACTURING_MANUAL.md](../utility10/01-seeti-counter/MANUFACTURING_MANUAL.md) | **order-ready** | firmware compiled, not run on hardware |
| Gas Taraju (LPG cylinder scale) | [utility10/02-gas-taraju/MANUFACTURING_MANUAL.md](../utility10/02-gas-taraju/MANUFACTURING_MANUAL.md) | **order-ready** | load-cell calibration per unit |
| Fridge Door Guard | [utility10/03-fridge-door-guard/MANUFACTURING_MANUAL.md](../utility10/03-fridge-door-guard/MANUFACTURING_MANUAL.md) | **order-ready** |  |
| Bijli Meter Reader | [utility10/04-bijli-meter-reader/MANUFACTURING_MANUAL.md](../utility10/04-bijli-meter-reader/MANUFACTURING_MANUAL.md) | **order-ready** |  |
| Bijli Log | [utility10/05-bijli-log/MANUFACTURING_MANUAL.md](../utility10/05-bijli-log/MANUFACTURING_MANUAL.md) | **order-ready** | OLED/RTC drivers untested |
| Chulha Timers | [utility10/06-chulha-timers/MANUFACTURING_MANUAL.md](../utility10/06-chulha-timers/MANUFACTURING_MANUAL.md) | **order-ready** | display driver untested |
| Rain Alert Bell + plate | [utility10/07-rain-alert/MANUFACTURING_MANUAL.md](../utility10/07-rain-alert/MANUFACTURING_MANUAL.md) | **order-ready** | plate: `rainplate` board |
| Tap Litre Meter | [utility10/08-tap-litre-meter/MANUFACTURING_MANUAL.md](../utility10/08-tap-litre-meter/MANUFACTURING_MANUAL.md) | **order-ready** | needs bucket calibration |
| Masala Rack (laser-cut) | [utility10/09-masala-rack/MANUFACTURING_MANUAL.md](../utility10/09-masala-rack/MANUFACTURING_MANUAL.md) | no PCB | kerf coupon first |
| Laptop Stand (laser-cut) | [utility10/10-laptop-stand/MANUFACTURING_MANUAL.md](../utility10/10-laptop-stand/MANUFACTURING_MANUAL.md) | no PCB | stability limit stated |

## Products

| Project | Manual | Board | Main caveat |
|---|---|---|---|
| 1 Desi Games Studio (print) | [products/01-desi-games/MANUFACTURING_MANUAL.md](../products/01-desi-games/MANUFACTURING_MANUAL.md) | no PCB | language + fact review before print |
| 2 Kalakriti Automata (laser) | [products/02-automata/MANUFACTURING_MANUAL.md](../products/02-automata/MANUFACTURING_MANUAL.md) | no PCB | frame layouts provisional |
| 3 Prayog STEM lab kit | [products/03-prayog/MANUFACTURING_MANUAL.md](../products/03-prayog/MANUFACTURING_MANUAL.md) | no released board | sensors uncalibrated |
| 4 Jal-Rakshak tank controller | [products/04-jal-rakshak/MANUFACTURING_MANUAL.md](../products/04-jal-rakshak/MANUFACTURING_MANUAL.md) | no PCB | **mains version cannot be made**: low-voltage prototype only |
| 5 Kheti-Mitra irrigation | [products/05-kheti-mitra/MANUFACTURING_MANUAL.md](../products/05-kheti-mitra/MANUFACTURING_MANUAL.md) | **order-ready** | field trial required |
| 6 Gas-Suraksha leak alarm | [products/06-gas-suraksha/MANUFACTURING_MANUAL.md](../products/06-gas-suraksha/MANUFACTURING_MANUAL.md) | no PCB | **not certified, not for sale** |

## Toys (10)

| Project | Manual | Board | Main caveat |
|---|---|---|---|
| 01 Reflex Raja | [toys10/01-reflex-raja/MANUFACTURING_MANUAL.md](../toys10/01-reflex-raja/MANUFACTURING_MANUAL.md) | **order-ready** | shares the Desi Arcade board |
| 02 Taal Memory | [toys10/02-taal-memory/MANUFACTURING_MANUAL.md](../toys10/02-taal-memory/MANUFACTURING_MANUAL.md) | **order-ready** | shares the Desi Arcade board |
| 03 Aloo Bomb | [toys10/03-aloo-bomb/MANUFACTURING_MANUAL.md](../toys10/03-aloo-bomb/MANUFACTURING_MANUAL.md) | **order-ready** | shares the Desi Arcade board |
| 04 Beat Runner | [toys10/04-beat-runner/MANUFACTURING_MANUAL.md](../toys10/04-beat-runner/MANUFACTURING_MANUAL.md) | no released board |  |
| 05 Rangoli Spiro Gears | [toys10/05-rangoli-spiro/MANUFACTURING_MANUAL.md](../toys10/05-rangoli-spiro/MANUFACTURING_MANUAL.md) | no PCB | kerf test first |
| 06 Paper Rocket Launcher | [toys10/06-paper-rocket/MANUFACTURING_MANUAL.md](../toys10/06-paper-rocket/MANUFACTURING_MANUAL.md) | no PCB | projectile toy: lab review before sale; no drawings |
| 07 Tilt Maze | [toys10/07-tilt-maze/MANUFACTURING_MANUAL.md](../toys10/07-tilt-maze/MANUFACTURING_MANUAL.md) | no PCB | gimbal frame drawing missing |
| 08 Rubber-band Racer | [toys10/08-band-racer/MANUFACTURING_MANUAL.md](../toys10/08-band-racer/MANUFACTURING_MANUAL.md) | no PCB | provisional cut file |
| 09 Marble Cricket | [toys10/09-marble-cricket/MANUFACTURING_MANUAL.md](../toys10/09-marble-cricket/MANUFACTURING_MANUAL.md) | no PCB | provisional cut file; calibration drop |
| 10 Katha Cubes | [toys10/10-katha-cubes/MANUFACTURING_MANUAL.md](../toys10/10-katha-cubes/MANUFACTURING_MANUAL.md) | no PCB | illustrations and proofreading missing |

## Other projects

| Project | Manual | Board | Main caveat |
|---|---|---|---|
| Jal-Netra (engineering marvel) | [jal-netra/MANUFACTURING_MANUAL.md](../jal-netra/MANUFACTURING_MANUAL.md) | **order-ready** | **Gate 1 acoustic test first; not sellable** |
| Gravity toys (5) | [gravity-toys/MANUFACTURING_MANUAL.md](../gravity-toys/MANUFACTURING_MANUAL.md) | no PCB | drawings partial |
| Wave 1 electronics toys | [electronics-toys/wave1/MANUFACTURING_MANUAL.md](../electronics-toys/wave1/MANUFACTURING_MANUAL.md) | no PCB | no PCB: not manufacturable yet |
| Prototype packs (10) | [prototypes/MANUFACTURING_MANUAL.md](../prototypes/MANUFACTURING_MANUAL.md) | no PCB | bench prototypes |
| DJ / party system | [dj-setup/MANUFACTURING_MANUAL.md](../dj-setup/MANUFACTURING_MANUAL.md) | no PCB | plan only: not manufacturable |
