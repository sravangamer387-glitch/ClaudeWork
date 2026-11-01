from .blocks import *
W, H = 76, 52
parts = (mcu("+4V5", {"13": "BUZ", "12": "TARE", "32": "HX_DOUT", "1": "HX_SCK", "27": "DIO", "28": "DCLK", "9": "LED_G", "10": "LED_A", "11": "LED_R"}, 34, 26) + isp("+4V5", 47, 8) + batt_input("+4V5", 11, 45.5, "BATT 3xAA") + buzzer("+4V5", "BUZ", 9, 15) +
         [dict(ref="U4", sym="Analog_ADC:HX711", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="HX711", x=60, y=17, rot=0, nc=["2", "9", "10", "13"],
               nets={"1": "+4V5", "3": "AVDD", "4": "AVDD", "5": "GND", "6": "VBG", "7": "A_N", "8": "A_P", "11": "HX_SCK", "12": "HX_DOUT", "14": "GND", "15": "GND", "16": "+4V5"}),
          R("R14", "100", 53, 8, "+4V5", "AVDD", 90, lcsc=None), C("C10", "100n", 56, 8, "AVDD", "GND", 90), C("C11", "100n", 66, 8, "+4V5", "GND", 90), C("C12", "100n", 56, 26, "VBG", "GND", 90), C("C13", "10u", 70, 12, "AVDD", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
          R("R15", "100", 66, 25, "AVDD", "EXC", 90, lcsc=None), C("C14", "100n", 69, 25, "EXC", "GND", 90), C("C15", "100n", 66, 29, "A_P", "A_N", 90),
          jst("J3", 4, 48, 46, ["EXC", "GND", "A_P", "A_N"], "Load cell bridge E+ E- A+ A-"), jst("J4", 4, 70, 36, ["GND", "+4V5", "DIO", "DCLK"], "TM1637 4-digit", 90),
          button("SW2", "TARE", 40, 6, "Tare / zero"),
          TP("TP1", "+4V5", 4, 22), TP("TP2", "GND", 4, 26), TP("TP3", "A_P", 40, 48)] + led("+4V5", "LED_G", 46, 33, "Green", "D1", "R5") + led("+4V5", "LED_A", 46, 36.5, "Amber", "D5", "R8") + led("+4V5", "LED_R", 46, 40, "Red", "D6", "R9"))
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
parts = [dict(p, nets={k: v for k, v in p["nets"].items() if v is not None}) for p in parts]
S = sch_layout([("POWER INPUT: 3xAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU", ["U1", "C1", "C2", "C3", "R7"]), ("WEIGH-CELL ADC: HX711 24-bit, load-cell bridge input", ["U4", "R14", "C10", "C11", "C12", "C13", "R15", "C14", "C15", "J3", "TP3"]),
               ("ALARM + LEVEL LEDS + TARE", ["BZ1", "Q1", "D2", "R6", "D1", "R5", "D5", "R8", "D6", "R9", "SW2"]), ("DISPLAY + PROGRAMMING", ["J4", "J2"])], big=("U1",))
S["notes"] = [("Four 50 kg half-bridge load cells under the 33 cm plate are wired into one full bridge at the plate (E+, E-, A+, A-). HX711 channel A, gain 128, 10 SPS, powered at 4.5 V (2.6-5.5 V allowed): AVDD through R14/C10, VFB tied to AVDD, BASE not used.", 20, 280), ("This product measures WEIGHT only: it is not a gas leak detector.", 20, 287)]
BOARD = dict(clr=0.15, name="gas_taraju", title="Gas Taraju (LPG cylinder scale) - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "GND": "battery", "AVDD": "filtered +4V5 (R14)", "EXC": "filtered AVDD (R15)"}, single_ok=("BAT_P", "VBG"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)], gnd_pour_only=True, widths={}, first=["+4V5", "BAT_P", "BAT_SW", "AVDD", "A_P", "A_N", "HX_DOUT", "HX_SCK"],
 silk=[("GAS TARAJU rev B", 24, H - 1.7, 0.9), ("CELL", 46, 43.2, 0.8), ("DISP", 66, 31.5, 0.8)], stitch=2.5)
BOARD["enc"] = dict(standoff=4.0, side=[("J3", "bottom", 11, 7, 3), ("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5), ("J4", "right", 12, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("round", "D5", 2.2), ("round", "D6", 2.2), ("grille", "BZ1", 5, 1.2, 7)])
