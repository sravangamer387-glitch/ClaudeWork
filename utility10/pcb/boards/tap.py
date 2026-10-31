from .blocks import *
W, H = 68, 46
parts = (mcu("+4V5", {"13": "BUZ", "32": "BTN", "1": "FLOW", "27": "SDA", "28": "SCL", "11": "LED"}, 34, 23) + isp("+4V5", 52, 32) + batt_input("+4V5", 11, 40, "BATT 3xAA") + buzzer("+4V5", "BUZ", 11.5, 13) + led("+4V5", "LED", 44, 40, "Green") +
         [button("SW2", "BTN", 34, 6, "Reset / target"), jst("J3", 3, 52, 6, ["+4V5", "FLOW_J", "GND"], "Flow sensor"), R("R8", "1k", 58, 12.5, "FLOW_J", "FLOW_S", 90), R("R9", "10k", 58, 17.5, "+4V5", "FLOW", 90), C("C9", "100n", 54.5, 17.5, "FLOW", "GND", 90), dict(ref="D4", sym="Device:D_TVS", fp="Diode_SMD:D_SOD-323", value="TVS 5V bidir", x=62, y=15, rot=90, nets={"1": "FLOW_J", "2": "GND"}),
          jst("J4", 4, 62, 26, ["GND", "+4V5", "SCL", "SDA"], "OLED 0.91in I2C", 90), R("R10", "4.7k", 47, 20, "+4V5", "SDA", 90, lcsc=None), R("R11", "4.7k", 50, 20, "+4V5", "SCL", 90, lcsc=None), TP("TP1", "+4V5", 4, 22), TP("TP2", "GND", 4, 26), TP("TP3", "FLOW", 44, 30)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
parts = [dict(p, nets={k: ("FLOW" if v == "FLOW_S" else v) for k, v in p["nets"].items()}) if p["ref"] == "R8" else p for p in parts]
# R8 joins the cable pin FLOW_J to the MCU node FLOW directly (1k series), R9/C9 pull-up and filter sit on FLOW
S = sch_layout([("POWER INPUT: 3xAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU, wakes on flow pulses", ["U1", "C1", "C2", "C3", "R7"]), ("FLOW SENSOR INPUT (hall, 3-wire)", ["J3", "R8", "R9", "C9", "D4", "TP3"]),
               ("ALARM, LED, BUTTON", ["BZ1", "Q1", "D2", "R6", "D1", "R5", "SW2"]), ("DISPLAY (OLED I2C) + PROGRAMMING", ["J4", "R10", "R11", "J2"])], big=("U1",))
S["notes"] = [("Flow sensor must be a 3.5-24 V type (e.g. YF-S201C class) because 3xAA falls to about 3.6 V; pulses per litre (about 450) are calibrated with a 10 L bucket. SIG is pulled up by R9 and filtered by C9.", 20, 280)]
BOARD = dict(name="tap_litre_meter", title="Tap Litre Meter - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], widths={"+4V5": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["FLOW", "SDA", "SCL"],
 silk=[("TAP LITRE METER rev B", 40, H - 1.3, 0.9), ("FLOW", 47, 5.0, 0.8), ("OLED", 58, 21.5, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J3", "top", 9, 7, 3), ("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5), ("J4", "right", 11, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7)])
