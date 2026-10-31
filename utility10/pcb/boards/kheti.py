from .blocks import *
W, H = 86, 60
parts = (mcu("+5V", {"10": "VALVE_G", "23": "SOIL1", "24": "SOIL2", "1": "RAIN", "32": "BTN", "11": "LED"}, 52, 33) + isp("+5V", 74, 48) + led("+5V", "LED", 70, 40, "Green") +
         [dict(ref="J1", sym="Connector:Barrel_Jack", fp="Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal", value="12 V DC in", x=14, y=2, rot=0, nets={"1": "VIN", "2": "GND"}),
          dict(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1812_4532Metric", value="PTC 1A 16V", x=24, y=5, rot=0, nets={"1": "VIN", "2": "VIN_F"}),
          dict(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMB", value="SMBJ15A", x=24, y=11, rot=0, nets={"1": "VIN_F", "2": "GND"}),
          dict(ref="Q3", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=33, y=6, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "GND", "2": "+12V", "3": "VIN_F"}),
          R("R17", "100k", 33, 11, "+12V", "GND", 90),
          dict(ref="U3", sym="Regulator_Linear:AMS1117-5.0", fp="Package_TO_SOT_SMD:SOT-223-3_TabPin2", value="AMS1117-5.0", x=45, y=8, rot=0, nets={"1": "GND", "2": "+5V", "3": "+12V"}),
          C("C6", "10u", 39, 6, "+12V", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C7", "10u", 52, 8, "+5V", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C8", "100n", 55, 8, "+5V", "GND", 90),
          dict(ref="Q4", sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=30, y=50, rot=0, nets={"1": "VALVE_GR", "2": "GND", "3": "VALVE_D"}),
          R("R16", "100", 36, 50, "VALVE_G", "VALVE_GR"), R("R18", "100k", 36, 54, "VALVE_GR", "GND"),
          dict(ref="D7", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=22, y=46, rot=0, nets={"1": "+12V", "2": "VALVE_D"}),
          dict(ref="J5", sym="Connector:Screw_Terminal_01x02", fp="TerminalBlock:TerminalBlock_bornier-2_P5.08mm", value="Valve 12V", x=12, y=54, rot=0, nets={"1": "+12V", "2": "VALVE_D"}),
          jst("J6", 3, 72, 6, ["+5V", "SOIL1_J", "GND"], "Soil sensor 1"), jst("J7", 3, 72, 13, ["+5V", "SOIL2_J", "GND"], "Soil sensor 2"), jst("J8", 3, 72, 20, ["+5V", "RAIN_J", "GND"], "Rain sensor"),
          R("R20", "1k", 62, 10, "SOIL1_J", "SOIL1", 90), C("C9", "100n", 65, 10, "SOIL1", "GND", 90), R("R21", "1k", 62, 17, "SOIL2_J", "SOIL2", 90), C("C10", "100n", 65, 17, "SOIL2", "GND", 90),
          R("R22", "1k", 62, 24, "RAIN_J", "RAIN", 90), R("R23", "10k", 59, 24, "+5V", "RAIN", 90), C("C11", "100n", 65, 24, "RAIN", "GND", 90),
          button("SW2", "BTN", 62, 5, "Hold"), TP("TP1", "+12V", 4, 26), TP("TP2", "+5V", 4, 30), TP("TP3", "GND", 4, 34), TP("TP4", "VALVE_G", 44, 54)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("12 V INPUT: jack, PTC, TVS, reverse-polarity PMOS", ["J1", "F1", "D3", "Q3", "R17", "C6", "TP1", "TP3"]), ("5 V REGULATOR", ["U3", "C7", "C8", "TP2"]), ("MCU: ATmega328P-AU", ["U1", "C1", "C2", "C3", "R7"]),
               ("VALVE DRIVER: logic-level NMOS, flyback diode, terminal", ["Q4", "R16", "R18", "D7", "J5", "TP4"]), ("SENSORS: 2 x soil (analog), rain (digital)", ["J6", "J7", "J8", "R20", "C9", "R21", "C10", "R22", "R23", "C11"]), ("USER + PROGRAMMING", ["SW2", "D1", "R5", "J2"])], big=("U1",))
S["notes"] = [("Valve: 12 V DC solenoid (about 0.3 A) switched low-side by Q4 with Schottky flyback D7. Q3 (AO3401A) blocks a reversed 12 V plug, D3 (SMBJ15A) clamps surges, F1 limits a fault to 1 A. AMS1117-5.0 drops 12 -> 5 V for about 40 mA of logic and sensors (about 0.3 W).", 20, 280)]
BOARD = dict(name="kheti_mitra", title="Kheti-Mitra irrigation controller - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"VIN": "DC jack", "VIN_F": "after PTC", "+12V": "after reverse-polarity PMOS", "+5V": "AMS1117", "GND": "jack"}, single_ok=("VALVE_G",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(36, 2.5), (W - 14, H - 2.5)], widths={"+5V": 0.4, "+12V": 0.4, "VIN": 0.4, "VIN_F": 0.4, "VALVE_D": 0.4}, first=["SOIL1", "SOIL2", "VALVE_D", "+12V", "VIN", "VIN_F"], edge_ok=("J1", "J5"),
 silk=[("KHETI-MITRA rev B", 40, H - 1.7, 0.9), ("12V IN", 14, 16.5, 0.8), ("VALVE", 12, 49.5, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 11, 11, 5), ("J5", "bottom", 12, 9, 4), ("J6", "right", 9, 7, 3), ("J7", "right", 9, 7, 3), ("J8", "right", 9, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2)])
