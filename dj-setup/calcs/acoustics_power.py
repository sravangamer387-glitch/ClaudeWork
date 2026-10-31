#!/usr/bin/env python3
"""Sizing model for the portable DJ system: how much amplifier power, battery and weight does each use-case need?
Usage: python3 -I acoustics_power.py > sizing.md
Free-field acoustic model (no room gain), music crest factor and amplifier efficiency are ASSUMPTIONS to be replaced
by measurements on prototypes."""
import math

CREST_DB = 12.0        # music peak-to-average (dB) when the limiter just starts to act
COMPRESSION_DB = 3.0   # woofer power compression at high drive (dB)
AMP_EFF = 0.85         # class-D efficiency
IDLE_W = 10.0          # DSP, Bluetooth, display, fans (per system)
BATT_ENERGY_WH_PER_KG = 100.0   # LiFePO4 pack level incl. BMS and case (assumption)
HOURS = 4.0

# use case: (name, listener distance m, target AVERAGE SPL at that distance dB(A-ish), system sensitivity dB @1W/1m, light load W)
CASES = [
    ("Living-room party (20-30 people), 1 speaker", 3.0, 85.0, 90.0, 20.0),
    ("Large home / terrace party (60 people), 2 speakers", 5.0, 92.0, 93.0, 40.0),
    ("Banquet / sangeet hall (200 people), 2 stacks", 8.0, 98.0, 96.0, 120.0),
]

print("| Use case | Listener m | Avg SPL dB | Peak SPL @1 m dB | Amp power needed W | Avg electrical draw W | Battery for 4 h Wh | Battery weight kg |")
print("|---|---|---|---|---|---|---|---|")
for name, r, avg, sens, lights in CASES:
    l1_avg = avg + 20 * math.log10(r)          # level at 1 m that gives `avg` at distance r (inverse square law)
    l1_peak = l1_avg + CREST_DB
    p_amp = 10 ** ((l1_peak - sens + COMPRESSION_DB) / 10)   # RMS-equivalent peak power
    p_avg_ac = p_amp / 10 ** (CREST_DB / 10)                 # average power delivered to the speakers
    p_elec = p_avg_ac / AMP_EFF + IDLE_W + lights
    wh = p_elec * HOURS
    kg = wh / BATT_ENERGY_WH_PER_KG
    print(f"| {name} | {r:g} | {avg:g} | {l1_peak:.0f} | {p_amp:.0f} | {p_elec:.0f} | {wh:.0f} | {kg:.1f} |")

print()
print(f"Assumptions: crest factor {CREST_DB:g} dB, power compression {COMPRESSION_DB:g} dB, class-D efficiency {AMP_EFF:.0%}, "
      f"idle/DSP {IDLE_W:g} W, pack {BATT_ENERGY_WH_PER_KG:g} Wh/kg, free field (rooms add reverberant gain).")
print("Rule of thumb check: +3 dB needs 2x amplifier power; +10 dB needs 10x. Doubling listener distance costs 6 dB.")
