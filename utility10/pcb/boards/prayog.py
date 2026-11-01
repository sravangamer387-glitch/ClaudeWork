from .blocks import *
W, H = 92, 66
def sock(n, x, y): return jst(f"J{3+n}", 3, x, y, ["+5V", f"AN{n}", "GND"], f"Analog socket A{n}", 0)
usb = usb_c_power(14, 4.31)
for p in usb:                                                    # this board needs the USB data pair (CH340C), not just power
    if p["ref"] == "J1":
        p["nc"] = ["A8", "B8"]; p["nets"].update({"A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM"}); p["value"] = "USB-C data + 5V"
parts = (mcu("+5V", {"30": "RXD", "31": "TXD", "7": "XTAL1", "8": "XTAL2", "23": "AN0", "24": "AN1", "25": "AN2", "26": "AN3", "27": "AN4", "28": "AN5", "19": "AN6", "22": "AN7", "32": "GATE", "2": "TRIG", "9": "ECHO", "11": "LED", "12": "BTN"}, 46, 34) + isp("+5V", 70, 42) + usb +
         [dict(ref="U2", sym="Interface_USB:CH340C", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="CH340C", x=14, y=34, rot=0, lcsc="C84681", lcsc_status="verified", mpn="CH340C",
               nets={"1": "GND", "2": "RXD", "3": "TXD", "4": "V3", "5": "USB_DP", "6": "USB_DM", "13": "DTR", "16": "+5V"}, nc=["7", "8", "9", "10", "11", "12", "14", "15"]),
          C("C6", "100n", 22, 26, "+5V", "GND", 90), C("C7", "100n", 22, 41, "V3", "GND", 90), C("C8", "100n", 26, 26, "DTR", "RESET", 90),
          dict(ref="Y1", sym="Device:Crystal_GND24", fp="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", value="16 MHz", x=33, y=39, rot=0, nets={"1": "XTAL1", "2": "GND", "3": "XTAL2", "4": "GND"}),
          C("C9", "22p", 29, 42.5, "XTAL1", "GND", 90), C("C10", "22p", 33, 44.5, "XTAL2", "GND", 90)] +
         [sock(n, 46 + (n % 4) * 10, 6 + (n // 4) * 9) for n in range(8)] +
         [jst("J11", 3, 62, 58, ["+5V", "GATE", "GND"], "Photogate", 0), jst("J12", 4, 74, 56, ["+5V", "TRIG", "ECHO", "GND"], "Ultrasonic HC-SR04", 0),
          button("SW2", "BTN", 22, 58, "Reaction pad"), TP("TP1", "+5V", 5, 22), TP("TP2", "GND", 5, 28)] + led("+5V", "LED", 8, 58, "Green"))
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("USB-C INPUT: data pair to CH340C, CC pull-downs, PTC, TVS", ["J1", "F1", "D3", "R1", "R2", "C5", "TP1", "TP2"]), ("USB-SERIAL: CH340C, auto-reset capacitor", ["U2", "C6", "C7", "C8"]),
               ("MCU: ATmega328P-AU, 16 MHz crystal", ["U1", "Y1", "C9", "C10", "C1", "C2", "C3", "R7"]), ("8 ANALOG SENSOR SOCKETS A0-A7", ["J3", "J4", "J5", "J6", "J7", "J8", "J9", "J10"]),
               ("PHOTOGATE, ULTRASONIC, REACTION PAD, PROGRAMMING", ["J11", "J12", "SW2", "D1", "R5", "J2"])], big=("U1",))
S["notes"] = [("Prayog hub: Arduino-Nano-class board. CH340C gives USB serial and auto-reset (DTR through 100 nF). Sockets are +5V / signal / GND JST-PH; photogate on D2 (interrupt), ultrasonic trigger D4 and echo D5, reaction pad button D8 and LED D7. Flash firmware/release/prayog.hex over USB with the Arduino bootloader or over ISP.", 20, 330)]
BOARD = dict(name="prayog_hub", title="Prayog STEM lab kit - hub board", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+5V": "USB via PTC", "GND": "USB", "VBUS": "USB", "V3": "CH340C internal 3.3 V"}, single_ok=("V3", "USB_DP", "USB_DM"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(36, 2.5), (W - 14, H - 2.5)], widths={"+5V": 0.4, "VBUS": 0.4}, first=["CC1", "CC2", "VBUS", "USB_DP", "USB_DM", "XTAL1", "XTAL2"], edge_ok=("J1",), clr=0.15,
 silk=[("PRAYOG HUB rev A", 30, H - 1.7, 0.9)] + [(f"A{n}", 46 + (n % 4) * 10 + 2, 3.2 + (n // 4) * 9, 0.8) for n in range(8)] + [("GATE", 62, 54.2, 0.8), ("SONAR", 74, 52.2, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 9.6, 3.8, 1.9)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2)])
