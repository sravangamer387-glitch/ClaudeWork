from .common import *
W, H = 52, 38
parts = [
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=28, y=22, rot=0, mpn="ATMEGA328P-AU", lcsc="C14877", lcsc_status="verified", nc="rest", nets={
   "4": "+5V", "6": "+5V", "18": "+5V", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "SIG", "1": "DCLK", "2": "DIO", "32": "BTN", "11": "LED"}),
 dict(ref="J1", sym="Connector:USB_C_Receptacle_USB2.0_16P", fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", value="USB-C 5V", x=26, y=4.31, rot=180, lcsc="C165948", lcsc_status="verified", mpn="TYPE-C-31-M-12", nc=["A6", "A7", "A8", "B6", "B7", "B8"],
      nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2", "S1": "GND"}),
 dict(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1206_3216Metric", value="PTC 500mA", x=36, y=7, rot=0, nets={"1": "VBUS", "2": "+5V"}),
 dict(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMA", value="SMAJ5.0A", x=41, y=11, rot=0, nets={"1": "VBUS", "2": "GND"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=25, y=30, rot=0, nets={"1": "MISO", "2": "+5V", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x03", fp="Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", value="Sensor head", x=47.2, y=15, rot=90, nets={"1": "+5V", "2": "SIG_H", "3": "GND"}),
 dict(ref="J4", sym="Connector_Generic:Conn_01x04", fp="Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical", value="TM1637 display", x=5, y=18, rot=90, nets={"1": "GND", "2": "+5V", "3": "DIO", "4": "DCLK"}),
 dict(ref="SW1", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Reset bill", x=16, y=15, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Green", x=43.5, y=34.5, rot=0, nets={"1": "GND", "2": "LED_A"}),
 R("R1", "5.1k", 20, 14, "CC1", "GND", 90), R("R2", "5.1k", 32, 14, "CC2", "GND", 90), R("R3", "10k", 15, 20, "+5V", "RESET", 90), R("R4", "10k", 42, 20, "+5V", "SIG", 90), R("R5", "1k", 39.5, 34.5, "LED", "LED_A"), R("R6", "100", 42, 24, "SIG_H", "SIG", 90, lcsc=None),
 C("C1", "10u", 35.5, 11.5, "+5V", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"), C("C2", "100n", 21, 21, "+5V", "GND", 90), C("C3", "100n", 36, 26, "+5V", "GND", 90), C("C4", "100n", 36, 20, "AREF", "GND", 90), C("C5", "100n", 45, 24, "SIG", "GND", 90),
 TP("TP1", "+5V", 10, 26), TP("TP2", "GND", 10, 30), TP("TP3", "SIG", 46, 28),
]
for p in parts:
    if p.get("lcsc") is None and "lcsc" in p: del p["lcsc"]
S = dict(paper="A3", auto_wire_max=80,
 place={"J1": (45, 75, 0), "R1": (85, 45, 0), "R2": (105, 45, 0), "F1": (125, 60, 0), "D3": (150, 60, 0), "C1": (150, 95, 0), "TP1": (50, 105, 0), "TP2": (70, 105, 0), "TP3": (90, 105, 0),
        "U1": (240, 120, 0), "C2": (205, 40, 0), "C3": (225, 40, 0), "C4": (245, 40, 0), "R3": (265, 40, 0),
        "SW1": (50, 160, 0), "R5": (90, 160, 90), "D1": (115, 160, 0),
        "J3": (330, 65, 90), "R6": (360, 55, 90), "R4": (380, 55, 0), "C5": (380, 90, 0),
        "J2": (215, 225, 0), "J4": (285, 225, 0)},
 blocks=[dict(title="USB-C 5 V INPUT: CC pull-downs, PTC, TVS", x=20, y=22, w=150, h=95), dict(title="MCU: ATmega328P-AU, internal RC 8 MHz", x=180, y=22, w=120, h=170), dict(title="USER: reset button, LED", x=20, y=122, w=150, h=75),
   dict(title="METER SENSOR HEAD INTERFACE", x=305, y=22, w=105, h=110), dict(title="PROGRAMMING / DISPLAY", x=180, y=197, w=170, h=50)],
 notes=[("USB-C power only: 5.1k on CC1/CC2 advertises a 5 V sink; D+/D- unused. PTC limits a fault to 0.5 A, SMAJ5.0A clamps spikes.", 20, 265), ("Head: phototransistor between SIG_H and GND, 10k pull-up R4: SIG falls when the meter LED lights. R6 100R + C5 100n filter the cable.", 20, 273), ("ATmega328P at 5 V may run at 8 MHz (internal RC, fuses lfuse 0xE2 hfuse 0xD9 efuse 0xFD).", 20, 281)])
BOARD = dict(name="bijli_meter_reader", title="Bijli Meter Reader - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"+5V": "USB via F1", "GND": "USB", "VBUS": "USB"}, single_ok=("VBUS",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 3), (34, 35.5)],
 widths={"+5V": 0.4, "VBUS": 0.4}, edge_ok=("J1",), first=["CC1", "CC2", "VBUS"],
 silk=[("BIJLI READER rev B", 14, H - 1.4, 0.8), ("HEAD", 45, 6.6, 0.8), ("DISP", 11.5, 13.0, 0.8), ("ISP", 32.5, 31.0, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 9.6, 3.8, 1.9), ("J3", "right", 9, 7, 3), ("J4", "left", 11, 7, 3)], lid=[("round", "SW1", 5.0), ("round", "D1", 2.2)])
