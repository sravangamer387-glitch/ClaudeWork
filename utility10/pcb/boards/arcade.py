from .blocks import *
W, H = 80, 50
def arc(n, x, y):
    return jst(f"J{4+n}", 3, x, y, [f"B{n}", f"LA{n}", "GND"], f"Arcade button {n}")
parts = (mcu("+4V5", {"13": "BUZ", "32": "B1", "1": "B2", "2": "B3", "9": "B4", "10": "L1", "11": "L2", "12": "L3", "14": "L4", "23": "NOISE"}, 40, 22) + isp("+4V5", 66, 32) + batt_input("+4V5", 11, 43, "BATT 3xAAA") + buzzer("+4V5", "BUZ", 12, 12) +
         [arc(1, 56, 5), arc(2, 56, 12), arc(3, 56, 37), arc(4, 56, 43), R("R10", "330", 48, 7, "L1", "LA1", 90, lcsc=None), R("R11", "330", 51, 7, "L2", "LA2", 90, lcsc=None), R("R12", "330", 48, 31, "L3", "LA3", 90, lcsc=None), R("R13", "330", 51, 31, "L4", "LA4", 90, lcsc=None),
          R("R14", "100k", 30, 34, "+4V5", "NOISE", 90), R("R15", "100k", 30, 40, "NOISE", "GND", 90), TP("TP1", "+4V5", 4, 20), TP("TP2", "GND", 4, 24), TP("TP3", "NOISE", 36, 40)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER INPUT: 3xAAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU. Hold button 2 / 3 at power-on to pick Taal Memory / Aloo Bomb", ["U1", "C1", "C2", "C3", "R7"]),
               ("ARCADE BUTTONS + LAMPS (30 mm buttons with LED)", ["J5", "J6", "J7", "J8", "R10", "R11", "R12", "R13"]), ("ALARM: buzzer", ["BZ1", "Q1", "D2", "R6"]), ("RANDOM SEED / BATTERY DIVIDER + PROGRAMMING", ["R14", "R15", "TP3", "J2"])], big=("U1",))
S["notes"] = [("Desi Arcade: three games (Reflex Raja, Taal Memory, Aloo Bomb) on one board. NOISE node = VCC/2 divider: its ADC noise seeds the random generator and measures the battery.", 20, 280)]
BOARD = dict(name="desi_arcade", title="Desi Arcade - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], widths={"+4V5": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["B1", "B2", "B3", "B4"],
 silk=[("DESI ARCADE rev B", 28, H - 1.7, 0.9)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5), ("J5", "right", 9, 7, 3), ("J6", "right", 9, 7, 3), ("J7", "right", 9, 7, 3), ("J8", "right", 9, 7, 3)], lid=[("grille", "BZ1", 5, 1.2, 7)])
