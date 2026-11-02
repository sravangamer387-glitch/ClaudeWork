from .blocks import *
W, H = 64, 44
parts = (mcu("+3V0", {"13": "BUZ", "32": "BTN", "1": "REED", "11": "LED"}, 32, 21) + isp("+3V0", 51, 30) + batt_input("+3V0", 11, 37.5, "BATT 2xAAA") + buzzer("+3V0", "BUZ", 9.5, 11) + led("+3V0", "LED", 42, 38.5, "Green") +
         [button("SW2", "BTN", 32, 6, "Silence"), jst("J3", 2, 50, 5, ["REED_J", "GND"], "Reed switch"), R("R8", "1k", 56, 10, "REED_J", "REED", 90), C("C9", "10n", 56, 14, "REED", "GND", 90, lcsc="C1589"), dict(ref="D4", sym="Device:D_TVS", fp="Diode_SMD:D_SOD-323", value="TVS 5V bidir", x=59, y=12, rot=90, nets={"1": "REED_J", "2": "GND"}),
          TP("TP1", "+3V0", 4, 20), TP("TP2", "GND", 4, 24), TP("TP3", "REED", 44, 24)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER INPUT: 2xAAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU, 4 MHz, sleeps between door events", ["U1", "C1", "C2", "C3", "R7"]), ("REED INPUT (door magnet)", ["J3", "R8", "C9", "D4", "TP3"]),
               ("ALARM: buzzer, LED, silence button", ["BZ1", "Q1", "D2", "R6", "D1", "R5", "SW2"]), ("PROGRAMMING", ["J2"])], big=("U1",))
S["notes"] = [("Reed switch closes to GND when the magnet is next to it (door shut); door open -> REED goes high -> INT1 wakes the MCU. Internal pull-up on PD3. Sleep current < 2 uA.", 20, 280), ("Timeline: quiet 60 s, chirp every 10 s, continuous after 180 s; closing the door or the silence button stops it.", 20, 287)]
BOARD = dict(name="fridge_door_guard", title="Fridge Door Guard - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+3V0": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], widths={"+3V0": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["REED", "BUZ"],
 silk=[("FRIDGE DOOR GUARD rev B", 13.5, H - 1.7, 0.9), ("REED", 44.5, 5.0, 0.8), ("ISP", 46.5, 33.0, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J3", "top", 9, 7, 3), ("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7)])
