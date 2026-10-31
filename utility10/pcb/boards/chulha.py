from .blocks import *
W, H = 72, 48
parts = (mcu("+4V5", {"13": "BUZ", "32": "B1", "1": "B2", "2": "B3", "9": "B4", "27": "DIO", "28": "DCLK"}, 36, 24) + isp("+4V5", 56, 32) + batt_input("+4V5", 11, 41.5, "BATT 3xAAA") + buzzer("+4V5", "BUZ", 13.5, 14) +
         [button("SW2", "B1", 42, 6, "CH1"), button("SW3", "B2", 50, 6, "CH2"), button("SW4", "B3", 58, 6, "CH3"), button("SW5", "B4", 65, 11, "CH4"), jst("J4", 4, 66.5, 27, ["GND", "+4V5", "DIO", "DCLK"], "TM1637 display", 90),
          TP("TP1", "+4V5", 4, 24), TP("TP2", "GND", 4, 28), TP("TP3", "DIO", 52, 40)])
S = sch_layout([("POWER INPUT: 3xAAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU", ["U1", "C1", "C2", "C3", "R7"]), ("CHANNEL BUTTONS (tap +1 min, hold 1 s = clear)", ["SW2", "SW3", "SW4", "SW5"]),
               ("ALARM: buzzer", ["BZ1", "Q1", "D2", "R6"]), ("DISPLAY + PROGRAMMING", ["J4", "J2", "TP3"])], big=("U1",))
S["notes"] = [("Display: a standard TM1637 6-digit module on J4 (shows the soonest channel mm:ss and the channel number). Each channel button adds 1 minute; a ringing channel is silenced by its own button.", 20, 280)]
BOARD = dict(name="chulha_timers", title="Chulha Timers - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], widths={"+4V5": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["B1", "B2", "B3", "B4", "DIO", "DCLK"],
 silk=[("CHULHA TIMERS rev B", 26, H - 1.7, 0.9), ("DISPLAY", 63, 22.5, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "bottom", 9, 7, 3), ("J4", "right", 12, 7, 3), ("SW1", "bottom", 8, 5, 2.5)], lid=[("round", "SW2", 5.0), ("round", "SW3", 5.0), ("round", "SW4", 5.0), ("round", "SW5", 5.0), ("grille", "BZ1", 5, 1.2, 7)])
