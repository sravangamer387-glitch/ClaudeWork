#!/usr/bin/env python3
"""Overall bench-prototype budget for the WHOLE portfolio: every released PCB (JLCPCB fab + economic SMT assembly, live LCSC part prices),
one LCSC cart of hand-soldered parts, the bought-in / mechanical items for one complete bench unit of every project, and one-time tools.
Board costs are computed from costing/*_priced_BOM.csv with the same fee model as gen_first_order.py; bought-in figures are estimates with
their basis stated. Writes costing/FULL_BENCH_BUDGET.md.   usage: python3 manuals/gen_full_budget.py   (run utility10/pcb/costing.py first)"""
import collections, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_first_order as fo
ROOT, REL, COST, INR = fo.ROOT, fo.REL, fo.COST, fo.INR

BOARDS = sorted(d for d in os.listdir(REL) if os.path.isdir(os.path.join(REL, d)))
ASSEMBLED, SPARE = 2, 0.2
SHIP_USD = 55.0            # one consolidated JLCPCB parcel (about 125 PCBs + parts), DHL/FedEx to India
CUSTOMS = 0.35             # basic duty + IGST, budgeted on the parcel value

# (group, project, INR, basis) - bought-in modules, mechanics and test items for ONE complete bench unit; PCB parts are NOT included here
BOUGHT = [
 ("Utility tools", "Seeti Counter", 250, "battery holder + cells, clip; mic and buzzer are on the PCB"),
 ("Utility tools", "Gas Taraju (LPG scale)", 900, "4 x 50 kg half-bridge load cells, MDF plate, 20 kg test weight (README budget minus the Nano/breadboard)"),
 ("Utility tools", "Fridge Door Guard", 200, "MC-38 reed + magnet, 2 x AAA holder + cells (first-order list)"),
 ("Utility tools", "Bijli Meter Reader", 300, "USB adapter + cable, printed shroud for the meter LED"),
 ("Utility tools", "Bijli Log", 350, "USB adapter + cable, backup cell"),
 ("Utility tools", "Chulha Timers", 250, "TM1637 module, magnet, 3 x AAA holder + cells (first-order list)"),
 ("Utility tools", "Rain Alert Bell + plate", 300, "3 x AA holder + cells, 5 m twin cable for the plate"),
 ("Utility tools", "Tap Litre Meter", 550, "YF-S201 hall flow sensor, tap adapter fittings, holder + cells"),
 ("Utility tools", "Masala Rack (laser-cut)", 850, "documented prototype budget (MDF 9 mm, laser job, finish)"),
 ("Utility tools", "Laptop Stand (laser-cut)", 700, "documented prototype budget"),
 ("Products", "1 Desi Games Studio (print)", 1300, "documented prototype budget (colour prints, card, dice, box)"),
 ("Products", "2 Kalakriti Automata (laser)", 940, "documented prototype budget (MDF, laser job, dowels)"),
 ("Products", "3 Prayog STEM hub", 1950, "starter sensor set, 12 JST leads, USB-C cable (first-order list)"),
 ("Products", "4 Jal-Rakshak tank controller", 1150, "12 V adapter, SS probe rods + cable, 12 V test pump as load (12 V version only)"),
 ("Products", "5 Kheti-Mitra irrigation", 1300, "12 V adapter, 12 V NC valve, soil probe, lamp as test load"),
 ("Products", "6 Gas-Suraksha leak alarm", 400, "MQ-6 sensor module, 3 x AA holder + cells (test with a lighter's gas, outdoors)"),
 ("Toys", "01-03 Desi Arcade (one board, three games)", 500, "4 x 30 mm LED arcade buttons, 3 x AAA holder + cells (first-order list)"),
 ("Toys", "04 Beat Runner", 250, "1 x 30 mm arcade button, 3 x AAA holder + cells"),
 ("Toys", "05 Rangoli Spiro Gears", 700, "documented prototype budget"),
 ("Toys", "06 Paper Rocket stomp launcher", 1100, "documented prototype budget"),
 ("Toys", "07 Tilt Maze", 950, "documented prototype budget"),
 ("Toys", "08 Rubber-band Racer", 600, "documented prototype budget"),
 ("Toys", "09 Marble Cricket", 1110, "documented prototype budget"),
 ("Toys", "10 Katha Cubes", 400, "documented prototype budget"),
 ("Programmes", "KINETIC motion controller + vibration puck", 2600, "NEMA17 motor, TMC2209 driver module, 24 V 3 A supply, coupling + test rig"),
 ("Programmes", "MITTI-NETRA soil + structure node", 4000, "SIM7080G breakout + antenna, data SIM, 6 V 2 W panel, protected 18650, IP65 box + glands, soil probe hardware (manual figures)"),
 ("Programmes", "BioTray vertical-farm controller", 5100, "2 x 12 V pumps, fan, LED grow strip, analog pH + EC modules with probes, BH1750, DS18B20, float switch, 12 V 3 A adapter, IP65 box"),
 ("Programmes", "BioWatt MFC harvester", 1800, "2 cells: carbon-felt electrodes, containers, salt bridge/membrane, protected LiPo, bench resistors"),
 ("Programmes", "AQUAPONICS controller (uses a BioTray board)", 5500, "ADS1115, pH probe, 2 dosing pumps, 30 L tank + grow bed + plumbing (no fish in the bench phase)"),
 ("Programmes", "GEONODE foundation monitoring (no PCB yet)", 5000, "2 nodes (ESP32 + LoRa module + tilt/vibration sensor + battery) + 1 gateway (ESP32 + LoRa)"),
 ("Programmes", "SORTER bio-robotic platform (no PCB yet)", 8000, "mini conveyor + geared motor, 2-axis servo arm, silicone for the soft gripper, ESP32-CAM; a Raspberry Pi + camera adds about Rs 6,000"),
 ("Programmes", "AGROVER solar rover (no PCB yet)", 10000, "4WD chassis + motors, 2 motor drivers, 20 W panel, Li-ion pack + BMS + charger, ESP32, GPS, 3 ultrasonic sensors"),
 ("Other", "Jal-Netra clamp-on flow monitor", 3500, "pair of ultrasonic transducers, couplant, clamp hardware, a 1 m pipe test rig with a reference flow"),
 ("Other", "ASTRADAND gesture wand", 1000, "LiPo cell, resin/clear PETG crystal, hilt print, charger lead"),
 ("Other", "Wave 1 electronics toys (AP1 platform)", 1150, "DFPlayer + microSD, speaker, 4-digit module + lead, RGB lamp, small motor, 3 x AA holder + cells, acrylic window"),
 ("Other", "Gravity toys (5) bench prototypes", 5970, "documented budgets G1-G5 (marble run, Drop Quest, Galton board, balance set, ramp racers)"),
 ("Other", "DJ / party system - phase-0 prototypes only", 3570, "documented budgets D1 + D2 (light controller, MIDI controller); the full system is a separate business plan"),
 ("Other", "TRISHNA urinal hydration monitor", 9930, "first-order list: DevKit, pump, valve, ToF, probe, photodiodes, plumbing, glands, KCl standards, refractometer, chemicals"),
]
TOOLS = [
 ("Temperature-controlled soldering station + tips", 2500), ("Digital multimeter", 1000), ("Bench power supply 0-30 V 5 A with current limit", 4500),
 ("USBasp programmer + ISP adapter", 300), ("JST-PH crimper + kit", 900), ("Hand tools: cutters, strippers, tweezers, files, calipers", 1500),
 ("Drill + bits 1.0-6 mm + M3/M5 taps", 2500), ("3D printer, Ender-3 class (skip if you use a print service: budget about Rs 4,000 instead)", 18000),
 ("PETG filament 4 kg (black 3 kg, clear 0.5 kg, white 0.5 kg)", 4800), ("Consumables: solder, flux, IPA, heat-shrink, RTV, epoxy, PTFE tape, wire stock, screws/inserts", 3000),
 ("Calibration and test stock: pH 4/7 buffers, KCl standards, 1 kg + 5 kg test weights, measuring cylinders", 1500)]

def main():
    rows, tot_parts, tot_fees, tot_pcb = [], 0.0, 0.0, 0.0
    cart = collections.OrderedDict()
    for b in BOARDS:
        try: d = fo.board_data(b)
        except (IndexError, FileNotFoundError): continue
        w, h = fo.size(b)
        pcb = 4.0 if w <= 100 and h <= 100 else 9.0
        fees = (8.0 + 1.5 + 3.0 * len(d["ext"])) if d["smt_unique"] else 0.0      # bare PCB (rain plate): no assembly
        parts = d["smt_usd"] * ASSEMBLED * 1.1
        tot_parts += parts; tot_fees += fees; tot_pcb += pcb
        rows.append((b, w, h, len(d["smt_unique"]), len(d["ext"]), parts, pcb, fees))
        for r in d["hand"]:
            c = r["LCSC #"]; e = cart.setdefault(c, dict(mpn=r["Manufacturer part"], need=0, price=d["price"].get(c, 0), boards=set()))
            e["need"] += ASSEMBLED; e["boards"].add(b)
    lcsc = sum((e["need"] + max(1, math.ceil(e["need"] * SPARE))) * e["price"] for e in cart.values()) + 20.0
    jlc = tot_parts + tot_fees + tot_pcb + SHIP_USD
    jlc_inr, duty_inr, lcsc_inr = jlc * INR, jlc * INR * CUSTOMS, lcsc * INR
    bought = sum(x[2] for x in BOUGHT); tools = sum(x[1] for x in TOOLS)
    groups = collections.OrderedDict()
    for g, p, r, why in BOUGHT: groups[g] = groups.get(g, 0) + r
    core = jlc_inr + duty_inr + lcsc_inr + bought
    L = ["# Overall bench-prototype budget: the whole portfolio", "",
         "Generated by `manuals/gen_full_budget.py`. Scope: **one complete, bench-tested unit of every project** (41 projects), built on the released PCBs where one exists. "
         "Board costs are computed from the live-priced BOMs; bought-in figures are estimates (basis stated per line); prices at "
         f"{INR:.0f} INR/USD. Not included: certification and lab testing, field trials, production tooling, travel, your time.", "",
         "## Summary", "", "| Block | INR (approx) |", "|---|---|",
         f"| A. JLCPCB: {len(rows)} PCB designs x 5 boards, {ASSEMBLED} of each SMT-assembled, parts + fees + one consolidated shipment | {jlc_inr:,.0f} |",
         f"| B. Customs duty + IGST on that parcel (about {int(CUSTOMS * 100)} %) | {duty_inr:,.0f} |",
         f"| C. LCSC cart: hand-soldered parts for all assembled boards (+20 % spares) + shipping | {lcsc_inr:,.0f} |",
         f"| D. Bought-in modules, mechanics and test items, one unit per project | {bought:,.0f} |",
         f"| **Core budget (A-D)** | **{core:,.0f}** |",
         f"| E. One-time tools and consumables (only what you do not already own) | {tools:,.0f} |",
         f"| **Total if you start from an empty bench** | **{core + tools:,.0f}** |",
         f"| Contingency: add 15 % for re-spins, breakage and price changes | {(core + tools) * 0.15:,.0f} |",
         f"| **Planning figure** | **about Rs {round((core + tools) * 1.15, -3):,.0f}** |", "",
         "Where the money goes: the JLCPCB **assembly fees** are the largest single block (setup and stencil per design, plus a feeder fee per *extended* part line). "
         "Ordering in two or three batches (as in `costing/FIRST_ORDER.md`) spreads the spend but adds a shipment and its customs each time.", "",
         "## D by group", "", "| Group | INR |", "|---|---|"] + [f"| {g} | {v:,} |" for g, v in groups.items()] + ["",
         "## A. Boards (computed)", "", "| Board | Size mm | SMT lines (extended) | SMT parts for 2 boards (USD) | PCB 5 pcs (USD, est.) | Assembly fees (USD, est.) |", "|---|---|---|---|---|---|"]
    for b, w, h, n, ne, parts, pcb, fees in rows:
        L.append(f"| `{b}` | {w:.0f} x {h:.0f} | {n} ({ne}) | {parts:.2f} | {pcb:.0f} | {fees:.0f} |")
    L += [f"| **{len(rows)} designs** | | | **{tot_parts:.0f}** | **{tot_pcb:.0f}** | **{tot_fees:.0f}** |", "",
          f"JLCPCB total about US${jlc:,.0f} including about US${SHIP_USD:.0f} shipping. Fee model: 8 USD setup + 1.5 USD stencil per design + 3 USD per extended part line "
          "(basic-library lines: common UNI-ROYAL 0603 resistors, Samsung capacitors and a few jellybean parts). **JLCPCB's own quote is authoritative.**", "",
          "## D. Bought-in per project (estimates)", "", "| Group | Project | INR | Basis |", "|---|---|---|---|"]
    for g, p, r, why in BOUGHT: L.append(f"| {g} | {p} | {r:,} | {why} |")
    L += ["", "## E. One-time tools and consumables", "", "| Item | INR |", "|---|---|"] + [f"| {t} | {v:,} |" for t, v in TOOLS] + [f"| **total** | **{tools:,}** |", "",
          "## Cheaper routes", "",
          f"- **Skip the programmes first.** The utility tools, products, toys, TRISHNA and the other order-ready boards make up most of the value; SORTER, AGROVER, GEONODE, "
          f"AQUAPONICS and BioTray bought-in items alone are about Rs {sum(r for g, p, r, w in BOUGHT if g == 'Programmes'):,}.",
          "- **Assemble 2 of each board but buy hand parts for 1** if you only need one unit (saves little: the hand parts are cheap; the JLC fees are per design, not per board).",
          "- **No 3D printer:** use a print service for the enclosures (about Rs 4,000 for all) instead of Rs 18,000.",
          "- **Staged ordering:** batch 1 = `costing/FIRST_ORDER.md` (about Rs 54,000); later batches follow once the first boards pass bring-up.", ""]
    open(os.path.join(COST, "FULL_BENCH_BUDGET.md"), "w").write("\n".join(L))
    print(f"{len(rows)} designs; A {jlc_inr:,.0f}  B {duty_inr:,.0f}  C {lcsc_inr:,.0f}  D {bought:,}  core {core:,.0f}  E {tools:,}  total {core + tools:,.0f}  planning {round((core + tools) * 1.15, -3):,.0f}")
    for g, v in groups.items(): print("  ", g, f"{v:,}")

if __name__ == "__main__":
    main()
