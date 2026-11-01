"""BioWatt energy budget: what can a microbial fuel cell (MFC) power?
Model: MFC = open-circuit voltage Voc behind internal resistance Rint (linear polarisation curve), maximum power Pmax = Voc^2 / (4 Rint) at V = Voc/2.
A harvester IC with maximum-power-point tracking (fraction-of-Voc, about 50-80 %) delivers eff * Pmax into storage; a node sleeps at I_sleep and wakes for E_report per report.
All numbers are ASSUMPTIONS to be replaced by measurements of your own MFC (run a polarisation sweep with a resistor box) and your own node (current probe).
usage: python3 budget.py  -> prints a table and writes ../docs/budget.md"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
def mfc_pmax(voc, rint): return voc * voc / (4 * rint)
cells = [("small soil MFC (cheap electrodes)", 0.65, 5000.0), ("good lab MFC", 0.70, 1000.0), ("4 good cells in series (2.8 V, 4 kohm total)", 2.8, 4000.0)]
eff = 0.6                                                                 # harvester efficiency incl. MPPT sampling loss (assumed; real value depends on IC and input power)
nodes = [("ESP32-S3 WiFi + MQTT report", 3.3 * 0.15 * 4.0, 3.3 * 10e-6), ("ESP32-S3 BLE advert only", 3.3 * 0.05 * 0.5, 3.3 * 10e-6), ("ultra-low-power MCU + LoRa packet", 3.3 * 0.045 * 1.0, 3.3 * 2e-6)]
lines = ["# BioWatt energy budget (assumption-based model, not measured)\n", f"Harvester efficiency assumed {eff*100:.0f} %. E_report = energy per transmission (wake, sense, send); P_sleep = sleep power.\n",
         "| MFC | Voc V | Rint ohm | Pmax uW | harvested J/day | node | E_report J | P_sleep uW | sleep J/day | reports/day possible |", "|---|---|---|---|---|---|---|---|---|---|"]
for cn, voc, rint in cells:
    pm = mfc_pmax(voc, rint); jday = eff * pm * 86400
    for nn, er, ps in nodes:
        left = jday - ps * 86400; rpd = max(0.0, left / er)
        lines.append(f"| {cn} | {voc} | {rint:.0f} | {pm*1e6:.0f} | {jday:.2f} | {nn} | {er:.2f} | {ps*1e6:.0f} | {ps*86400:.2f} | {rpd:.1f} |")
lines += ["\n**Reading the table.** A single small MFC gives a few joules per day. A WiFi report costs about 2 J, and even deep sleep costs 2-3 J per day, so a WiFi ESP32 cannot run from one small MFC at all; a LoRa/BLE node reporting a few times a day can. Even a 4-cell series stack (about 0.5 mW) supports only about ten WiFi reports a day; a WiFi tray controller with pumps and lights needs watts, so it needs mains or a battery.",
          "BioTray itself (pumps, LEDs, WiFi) needs watts and is NOT meant to run from an MFC: BioWatt powers a low-power *sensor tag* (soil/water temperature, moisture, level) that reports to the tray, or trickle-charges a backup cell.\n",
          "The MPPT fraction (50-80 % of Voc) and the harvester start-up voltage matter more than the IC's headline efficiency: a single 0.65 V MFC sits close to the cold-start threshold of the common harvester ICs (hundreds of mV), so verify start-up on the real cell."]
open(os.path.join(HERE, "..", "docs", "budget.md"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines[:14]))
