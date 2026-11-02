from .blocks import *
W, H = 86, 60
bz = buzzer("+5V", "MISO", 12, 24)                 # BZ1, Q1, D2, R6: buzzer on D12 (MISO, shared with ISP like an Arduino Nano)
for p in bz:
    if p["ref"] == "BZ1":                          # ACTIVE buzzer: the firmware switches D12 on and off; 68 ohm sets about 3 V across it from 5 V
        p.update(value="Buzzer active 3V", lcsc="C3015483", lcsc_status="verified", mpn="S&S SUN-1275Y-0327-50P7.6", nets={"1": "BZ_P", "2": "BZ_N"})
    if p["ref"] == "D2": p.update(x=24, y=31, rot=0, nets={"1": "BZ_P", "2": "BZ_N"})        # clamp directly across the buzzer
parts = (mcu("+5V", {"11": "PROBE_DRV", "12": "SUMP", "13": "TANK_LOW", "14": "TANK_FULL", "10": "PUMP_G", "32": "BTN"}, 52, 33) + isp("+5V", 74, 48) + bz + led("+5V", "SCK", 70, 40, "Green") +
         [dict(ref="J1", sym="Connector:Barrel_Jack", fp="Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal", value="12 V DC in", x=14, y=2, rot=0, nets={"1": "VIN", "2": "GND"}),
          dict(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1812_4532Metric", value="PTC 1A 16V", x=24, y=5, rot=0, nets={"1": "VIN", "2": "VIN_F"}),
          dict(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMB", value="SMBJ15A", x=24, y=11, rot=0, nets={"1": "VIN_F", "2": "GND"}),
          dict(ref="Q3", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=33, y=6, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "GND", "2": "+12V", "3": "VIN_F"}),
          R("R17", "100k", 33, 11, "+12V", "GND", 90),
          dict(ref="U3", sym="Regulator_Linear:AMS1117-5.0", fp="Package_TO_SOT_SMD:SOT-223-3_TabPin2", value="AMS1117-5.0", x=45, y=8, rot=0, nets={"1": "GND", "2": "+5V", "3": "+12V"}),
          C("C6", "10u", 39, 6, "+12V", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C7", "10u", 52, 8, "+5V", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C8", "100n", 55, 8, "+5V", "GND", 90),
          dict(ref="Q4", sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=30, y=50, rot=0, nets={"1": "PUMP_GR", "2": "GND", "3": "PUMP_D"}),
          R("R16", "100", 36, 50, "PUMP_G", "PUMP_GR"), R("R18", "100k", 36, 54, "PUMP_GR", "GND"),
          dict(ref="D7", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=22, y=46, rot=0, nets={"1": "+12V", "2": "PUMP_D"}),
          dict(ref="J5", sym="Connector:Screw_Terminal_01x02", fp="TerminalBlock:TerminalBlock_bornier-2_P5.08mm", value="Pump 12V DC, max 1 A (LOW VOLTAGE ONLY)", x=12, y=54, rot=0, nets={"1": "+12V", "2": "PUMP_D"}),
          R("R30", "68", 44, 20, "+5V", "BZ_P", 90),
          jst("J6", 4, 76, 14, ["PROBE_COM", "SUMP_J", "LOW_J", "FULL_J"], "Probes: COM, SUMP, TANK LOW, TANK FULL", 90),
          R("R20", "1k", 63, 6, "PROBE_DRV", "PROBE_COM", 90),
          R("R21", "10k", 63, 11, "SUMP_J", "SUMP", 90), R("R22", "100k", 67, 11, "SUMP", "GND", 90),
          R("R23", "10k", 63, 16, "LOW_J", "TANK_LOW", 90), R("R24", "100k", 67, 16, "TANK_LOW", "GND", 90),
          R("R25", "10k", 63, 21, "FULL_J", "TANK_FULL", 90), R("R26", "100k", 67, 21, "TANK_FULL", "GND", 90),
          button("SW2", "BTN", 58, 54, "Reset fault"), TP("TP1", "+12V", 40, 16), TP("TP2", "+5V", 4, 34), TP("TP3", "GND", 4, 38), TP("TP4", "PUMP_G", 44, 54)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("12 V INPUT: jack, PTC, TVS, reverse-polarity PMOS", ["J1", "F1", "D3", "Q3", "R17", "C6", "TP1", "TP3"]), ("5 V REGULATOR", ["U3", "C7", "C8", "TP2"]), ("MCU: ATmega328P-AU, 8 MHz internal", ["U1", "C1", "C2", "C3", "R7"]),
               ("PUMP DRIVER (12 V DC, low voltage only): logic-level NMOS, flyback diode, terminal", ["Q4", "R16", "R18", "D7", "J5", "TP4"]), ("AC-EXCITED WATER PROBES: common drive through 1 k, each sense 10 k series, 100 k pull-down", ["J6", "R20", "R21", "R22", "R23", "R24", "R25", "R26"]),
               ("ALARM, STATUS, PROGRAMMING", ["BZ1", "R30", "Q1", "D2", "R6", "D1", "R5", "SW2", "J2"])], big=("U1",))
S["notes"] = [("Jal-Rakshak LOW-VOLTAGE prototype board (never mains). 12 V DC in through PTC, TVS and reverse-polarity PMOS; AMS1117-5.0 for logic. The probe common electrode is driven by D7 through 1 k; a probe reads wet only if its sense pin follows the drive HIGH and LOW (AC excitation, no electrolysis). Pump: 12 V DC mini pump up to 1 A on J5, low-side AO3400A with SS14 flyback. Status LED on D13 and active buzzer on D12 share the ISP lines as on an Arduino Nano. Firmware: products/04-jal-rakshak/firmware (8 MHz build).", 0, 0)]
BOARD = dict(name="jal_rakshak", title="Jal-Rakshak tank controller - low-voltage prototype board (NOT for mains)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"VIN": "DC jack", "VIN_F": "after PTC", "+12V": "after reverse-polarity PMOS", "+5V": "AMS1117", "GND": "jack"}, single_ok=("PUMP_G",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(36, 2.5), (W - 14, H - 2.5)], widths={"+5V": 0.4, "+12V": 0.4, "VIN": 0.4, "VIN_F": 0.4, "PUMP_D": 0.4}, first=["PUMP_D", "+12V", "VIN", "VIN_F", "SUMP", "TANK_LOW", "TANK_FULL"], edge_ok=("J1", "J5", "J6"),
 silk=[("JAL-RAKSHAK rev A: LOW VOLTAGE ONLY", 46, H - 1.7, 0.8), ("12V IN", 14, 16.5, 0.8), ("PUMP", 12, 49.5, 0.8), ("PROBES", 76, 4.5, 0.7)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, battery=False, side=[("J1", "top", 11, 11, 5), ("J5", "bottom", 12, 9, 4), ("J6", "right", 12, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7)], note="indoor, dry use near the pump controller; probe and pump cables through the side openings; low voltage only")
