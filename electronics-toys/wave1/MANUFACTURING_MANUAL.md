# Wave 1 electronics toys (rhymes player P1, star lamp P3, handheld cricket P4): manufacturing status

> **Prototype-level design only: not ready to manufacture.** Firmware logic is tested on the host (73 checks); a pin map, power netlist, BOM, enclosures (7 STL parts) and a draft factory test spec exist; **there is no PCB layout, no schematic in KiCad, and no real MCU port.**

## What exists
| Item | Where |
|---|---|
| Portable firmware core and three apps (rhymes player, lamp, cricket) | `electronics-toys/wave1/firmware/` (`make test`: 73 checks) |
| Pin map, power netlist, BOM, power budget, design-to-cost | `hardware/out/` (`pinmap.csv`, `netlist_power_and_shared.csv`, `bom.csv`, `power_budget.md`, `design_to_cost.md`) |
| Enclosures | `enclosure/out/*.stl` (rhymes top/bottom/battery door, lamp base/dome, cricket top/bottom) + `checks.md` |
| Factory test spec (draft) | `docs/factory-test-spec.md` (100 % per-unit tests: idle current, reverse battery, 3V3 rail, battery divider, every button, ...) |
| Breadboard prototypes (Rs 1,370-2,120) | `prototypes/` (E1 rhymes player, E2 star lamp, E3 cricket) |

## What must be done before manufacture (from the README's own list)
1. PCB layout and a full KiCad schematic (use the repository's board toolchain: `utility10/pcb/`).
2. Real MCU port: HAL implementation, timers, ADC battery check (low-battery tone), flash/boot, watchdog.
3. Bench tests: current draw, sound level (keep toy buzzer/speaker levels within the standard), battery life, EMC pre-scan, drop test.
4. Tooling-grade CAD: draft angles, fillets, snap fits, ribs, gating.
5. Content: recorded rhymes/stories/lullabies with talent releases (copyright).
6. Compliance: IS 15644 / IS 9873 testing, BIS licence, labels, manuals.
7. Part numbers, prices and availability are unverified candidates: verify each (this repository's `lcsc_fill.py` shows how it is done for the PCBs).
MP3 module command codes were written from recollection and must be checked on the real module. The lamp's colour change limit (one level per 20 ms, no flashing) is enforced by tests and must be re-verified on hardware.

## Prototype build
Follow `prototypes/guides/electronics-prototypes.md` (wiring, SD-card layout, flashing, acceptance tests) and the manual in `prototypes/MANUFACTURING_MANUAL.md`.
