from .blocks import *
W, H = 150, 46
def L(n, x, y): return [dict(ref=f"D{10+n}", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Red", x=x, y=y, rot=90, nets={"1": "GND", "2": f"LK{n}"}), R(f"R{20+n}", "330", x, y + 4.5, f"Q{n}", f"LK{n}", 90)]
parts = (mcu("+4V5", {"13": "BUZ", "32": "BTN"}, 68, 18) + isp("+4V5", 82, 5) + batt_input("+4V5", 10, 9, "BATT 3xAAA") + buzzer("+4V5", "BUZ", 118, 8) +
         [dict(ref="U2", sym="74xx:74HC595", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="74HC595", x=44, y=22, rot=0, lcsc="C5947", lcsc_status="verified", mpn="74HC595D",
               nets={"1": "Q1", "2": "Q2", "3": "Q3", "4": "Q4", "5": "Q5", "6": "Q6", "7": "Q7", "8": "GND", "9": "Q7S", "10": "+4V5", "11": "MISO", "12": "SCK", "13": "GND", "14": "MOSI", "15": "Q0", "16": "+4V5"}),
          dict(ref="U3", sym="74xx:74HC595", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="74HC595", x=96, y=22, rot=0, lcsc="C5947", lcsc_status="verified", mpn="74HC595D",
               nets={"1": "Q9", "2": "Q10", "3": "Q11", "4": "Q12", "5": "Q13", "6": "Q14", "7": "Q15", "8": "GND", "9": None, "10": "+4V5", "11": "MISO", "12": "SCK", "13": "GND", "14": "Q7S", "15": "Q8", "16": "+4V5"}, nc=["9"]),
          C("C5", "100n", 44, 31, "+4V5", "GND", 0), C("C6", "100n", 96, 31, "+4V5", "GND", 0),
          jst("J3", 2, 142, 14, ["BTN", "GND"], "Arcade button", 90), TP("TP1", "+4V5", 4, 20), TP("TP2", "GND", 4, 26)])
for n in range(16):                                 # outputs of the two registers are named Q0..Q15 above (U2: 15,1..7 -> Q0..Q7; U3 15,1..7 -> Q8..Q15)
    parts += L(n, 8 + n * 8.0, 35)
parts = [p for p in parts if p]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
parts = [dict(p, nets={k: v for k, v in p["nets"].items() if v is not None}) for p in parts]
S = sch_layout([("POWER INPUT: 3xAAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU", ["U1", "C1", "C2", "C3", "R7"]), ("SHIFT REGISTERS 2 x 74HC595 -> 16 LEDs", ["U2", "U3", "C5", "C6"]),
               ("LEDS", [f"D{10+n}" for n in range(16)] + [f"R{20+n}" for n in range(16)]), ("BUTTON, BUZZER, PROGRAMMING", ["J3", "BZ1", "Q1", "D2", "R6", "J2"])], big=("U1",))
S["notes"] = [("Beat Runner: 16 LEDs in a row on two cascaded 74HC595 (data on D11, shift clock D12, latch D13 as in firmware; shared with the ISP header). Notes scroll toward LED 0; press the big arcade button on time.", 20, 300)]
BOARD = dict(name="beat_runner", title="Beat Runner - main board", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(44, 2.5), (W - 14, H - 2.5)], gnd_pour_only=True, widths={}, first=["+4V5", "BAT_P", "BAT_SW", "MOSI", "SCK", "MISO"], clr=0.15,
 silk=[("BEAT RUNNER rev A", 60, H - 1.7, 0.9)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "left", 9, 7, 3), ("J3", "right", 9, 7, 3)], lid=[("grille", "BZ1", 5, 1.2, 7)])
