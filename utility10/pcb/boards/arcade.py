from .blocks import *
W, H = 80, 50
def arc(n, x, y):
    return jst(f"J{4+n}", 3, x, y, [f"B{n}", f"LA{n}", "GND"], f"Arcade button {n}")
parts = (mcu("+4V5", {"13": "BUZ", "30": "B1", "31": "B2", "32": "B3", "28": "B4", "24": "L1", "25": "L2", "26": "L3", "27": "L4", "23": "NOISE"}, 40, 22) + isp("+4V5", 66, 38) + batt_input("+4V5", 11, 43, "BATT 3xAAA") + buzzer("+4V5", "BUZ", 12, 12) +
         [arc(1, 62, 6), arc(2, 62, 13), arc(3, 62, 20), arc(4, 62, 27), R("R10", "330", 50, 14, "L1", "LA1", 90, lcsc=None), R("R11", "330", 50, 18, "L2", "LA2", 90, lcsc=None), R("R12", "330", 50, 22, "L3", "LA3", 90, lcsc=None), R("R13", "330", 50, 26, "L4", "LA4", 90, lcsc=None),
          R("R14", "100k", 50, 33, "+4V5", "NOISE", 90), R("R15", "100k", 53, 33, "NOISE", "GND", 90), TP("TP1", "+4V5", 4, 20), TP("TP2", "GND", 4, 24), TP("TP3", "NOISE", 56, 36)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER INPUT: 3xAAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU. Hold button 2 / 3 at power-on to pick Taal Memory / Aloo Bomb", ["U1", "C1", "C2", "C3", "R7"]),
               ("ARCADE BUTTONS + LAMPS (30 mm buttons with LED)", ["J5", "J6", "J7", "J8", "R10", "R11", "R12", "R13"]), ("ALARM: buzzer", ["BZ1", "Q1", "D2", "R6"]), ("RANDOM SEED / BATTERY DIVIDER + PROGRAMMING", ["R14", "R15", "TP3", "J2"])], big=("U1",))
S["notes"] = [("Desi Arcade: three games (Reflex Raja, Taal Memory, Aloo Bomb) on one board. NOISE node = VCC/2 divider: its ADC noise seeds the random generator and measures the battery.", 20, 280)]
BOARD = dict(name="desi_arcade", title="Desi Arcade - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], gnd_pour_only=True, widths={}, first=["+4V5", "BAT_P", "BAT_SW", "B1", "B2", "B3", "B4"],
 silk=[("DESI ARCADE rev B", 28, H - 1.7, 0.9)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5), ("J5", "right", 9, 7, 3), ("J6", "right", 9, 7, 3), ("J7", "right", 9, 7, 3), ("J8", "right", 9, 7, 3)], lid=[("grille", "BZ1", 5, 1.2, 7)])
