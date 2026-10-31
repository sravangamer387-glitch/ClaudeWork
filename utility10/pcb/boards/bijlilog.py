from .blocks import *
W, H = 68, 52
parts = (mcu("VSYS", {"23": "MAINS", "27": "SDA", "28": "SCL", "11": "LED", "32": "BTN"}, 36, 32) + isp("VSYS", 56, 38) + usb_c_power(22, 4.31) + led("VSYS", "LED", 46, 46, "Green") +
         [dict(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=47, y=10, rot=0, nets={"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": "+3V3"}, nc=["4"]),
          C("C6", "1u", 42.5, 11, "+5V", "GND", 90), C("C7", "1u", 52, 11, "+3V3", "GND", 90),
          dict(ref="D5", sym="Device:D_Schottky", fp="Diode_SMD:D_SOD-323", value="BAT54WS", x=57, y=15, rot=90, nets={"1": "VSYS", "2": "+3V3"}),
          dict(ref="D6", sym="Device:D_Schottky", fp="Diode_SMD:D_SOD-323", value="BAT54WS", x=61, y=15, rot=90, nets={"1": "VSYS", "2": "BAT_P"}),
          jst("J6", 2, 61, 22, ["BAT_P", "GND"], "BATT 2xAAA backup", 90), C("C8", "10u", 55, 21, "VSYS", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
          R("R12", "100k", 11, 21, "VBUS", "MAINS", 90), R("R13", "100k", 11, 26, "MAINS", "GND", 90),
          jst("J4", 4, 5, 36, ["GND", "VSYS", "SCL", "SDA"], "OLED 0.91in I2C", 90), jst("J5", 4, 14, 36, ["GND", "VSYS", "SDA", "SCL"], "RTC DS3231 module", 90),
          R("R10", "4.7k", 23, 40, "VSYS", "SDA", 90), R("R11", "4.7k", 26, 40, "VSYS", "SCL", 90), button("SW2", "BTN", 36, 47, "Scroll / clear"), TP("TP1", "VSYS", 20, 48), TP("TP2", "GND", 14, 48), TP("TP3", "MAINS", 6, 20)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
parts = [dict(p, nets={k: v for k, v in p["nets"].items() if v is not None}) for p in parts]
S = sch_layout([("USB-C 5 V INPUT: CC pull-downs, PTC, TVS; mains-present sense", ["J1", "F1", "D3", "R1", "R2", "C5", "R12", "R13", "TP3"]), ("POWER: 3.3 V LDO, battery backup diode-OR", ["U3", "C6", "C7", "D5", "D6", "J6", "C8", "TP1", "TP2"]),
               ("MCU: ATmega328P-AU, 4 MHz", ["U1", "C1", "C2", "C3", "R7"]), ("I2C: OLED + RTC", ["J4", "J5", "R10", "R11"]), ("USER + PROGRAMMING", ["SW2", "D1", "R5", "J2"])], big=("U1",))
S["notes"] = [("VSYS = USB-derived 3.3 V or the 2xAAA backup, whichever is higher (Schottky OR, about 0.3 V drop). When VBUS disappears MAINS goes low: the firmware logs the cut start; when it returns it logs the duration. RTC module keeps wall-clock time.", 20, 280)]
BOARD = dict(name="bijli_log", title="Bijli Log (power-cut logger) - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"VSYS": "diode-OR of 3V3 and battery", "+5V": "USB via PTC", "+3V3": "LDO U3", "GND": "USB / battery", "VBUS": "USB", "BAT_P": "battery"}, single_ok=("BAT_P", "VBUS"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], widths={"VSYS": 0.4, "+3V3": 0.4, "+5V": 0.4, "VBUS": 0.4, "BAT_P": 0.4}, first=["CC1", "CC2", "VBUS", "SDA", "SCL"], edge_ok=("J1",),
 silk=[("BIJLI LOG rev B", 28, H - 1.7, 0.9), ("OLED", 6, 44.5, 0.8), ("RTC", 15, 44.5, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 9.6, 3.8, 1.9), ("J4", "left", 11, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2)])
