from .common import *
W, H = 64, 44
parts = [
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=32, y=21, rot=0, mpn="ATMEGA328P-AU", lcsc="C14877", lcsc_status="verified", nc="rest", nets={
   "4": "+3V0", "6": "+3V0", "18": "+3V0", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "ADC_IN", "13": "BUZ", "32": "BTN", "11": "LED", "30": "RXD", "31": "TXD"}),
 dict(ref="U2", sym="Amplifier_Operational:MCP6001-OT", fp="Package_TO_SOT_SMD:SOT-23-5", value="MCP6001", x=52, y=16, rot=0, lcsc="C116490", lcsc_status="verified", mpn="MCP6001T-I/OT", nets={"1": "MIC_OUT", "2": "GND", "3": "MIC_AC", "4": "FB", "5": "+3V0"}),
 dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="BATT 2xAAA", x=11, y=37.5, rot=0, nets={"1": "BAT_P", "2": "GND"}),
 dict(ref="SW1", sym="Switch:SW_SPDT", fp="Button_Switch_SMD:SW_SPDT_PCM12", value="Power", x=22, y=38.5, rot=0, nc=["3"], nets={"1": "BAT_SW", "2": "BAT_P"}),
 dict(ref="Q2", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=30, y=38, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "GND", "2": "+3V0", "3": "BAT_SW"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=51, y=30, rot=0, nets={"1": "MISO", "2": "+3V0", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="MIC electret", x=50, y=5, rot=0, nets={"1": "MIC_P", "2": "GND"}),
 dict(ref="J4", sym="Connector_Generic:Conn_01x04", fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", value="UART", x=36, y=41, rot=90, nets={"1": "GND", "2": "+3V0", "3": "RXD", "4": "TXD"}),
 dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer 3V", x=9.5, y=11, rot=0, nets={"1": "+3V0", "2": "BZ_N"}),
 dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=15, y=25, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
 dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=22, y=27, rot=0, lcsc="C2128", lcsc_status="verified", mpn="1N4148WS", nets={"1": "+3V0", "2": "BZ_N"}),
 dict(ref="SW2", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Target", x=32, y=6, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Green", x=50, y=38, rot=0, nets={"1": "GND", "2": "LED_A"}),
 R("R1", "2.2k", 57, 10, "+3V0", "MIC_P", 90), R("R2", "100k", 58, 18, "+3V0", "VMID", 90), R("R3", "100k", 58, 23, "VMID", "GND", 90), R("R4", "100k", 48, 22, "VMID", "MIC_AC"),
 R("R5", "1k", 46, 36, "LED", "LED_A"), R("R6", "1k", 10, 28, "BUZ", "BUZ_B"), R("R7", "10k", 25, 6, "+3V0", "RESET"), R("R8", "33k", 46, 11, "MIC_OUT", "FB"), R("R9", "1k", 46, 14, "FB", "FBN"),
 C("C1", "100n", 22, 18, "+3V0", "GND", 90), C("C2", "100n", 40, 25, "+3V0", "GND", 90), C("C3", "100n", 40, 17, "AREF", "GND", 90), C("C4", "10u", 35, 37, "+3V0", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
 C("C5", "1u", 54, 22, "MIC_P", "MIC_AC", 90), C("C6", "220n", 50, 26, "FBN", "VMID", 0), C("C7", "10u", 58, 28, "VMID", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C8", "100n", 55.5, 14.2, "+3V0", "GND", 90),
 R("R10", "1k", 42.5, 20.5, "MIC_OUT", "ADC_IN"), C("C9", "22n", 45, 23, "ADC_IN", "GND", 90, lcsc=None),
 TP("TP1", "+3V0", 4, 20), TP("TP2", "GND", 4, 24), TP("TP3", "MIC_OUT", 46, 30), TP("TP4", "BTN", 36, 30),
]
S = dict(paper="A3", wire_hfirst=True, auto_wire_max=80,
 place={"J1": (35, 50, 90), "SW1": (70, 50, 0), "Q2": (105, 55, 0), "C4": (135, 60, 0), "TP1": (35, 90, 0), "TP2": (55, 90, 0),
        "U1": (235, 125, 0), "C1": (180, 40, 0), "C2": (200, 40, 0), "C3": (220, 40, 0), "R7": (240, 40, 0),
        "BZ1": (45, 135, 0), "D2": (85, 135, 0), "Q1": (50, 175, 0), "R6": (25, 175, 90), "R5": (95, 165, 0), "D1": (95, 195, 0), "SW2": (50, 215, 0), "TP4": (85, 215, 0),
        "J3": (310, 45, 90), "R1": (335, 45, 0), "C5": (355, 75, 90), "R2": (380, 45, 0), "R3": (380, 85, 0), "C7": (405, 65, 0), "R4": (335, 100, 90),
        "U2": (350, 150, 0), "C8": (395, 145, 0), "R8": (320, 190, 90), "R9": (345, 190, 90), "C6": (370, 190, 0), "TP3": (395, 190, 0),
        "J2": (170, 235, 0), "J4": (230, 235, 0), "R10": (330, 125, 0), "C9": (360, 125, 90)},
 blocks=[dict(title="POWER INPUT: 2xAAA, switch, reverse-polarity PMOS", x=20, y=22, w=140, h=85), dict(title="MCU: ATmega328P-AU, internal RC, 4 MHz", x=165, y=22, w=130, h=190),
         dict(title="BUZZER, LED, BUTTON", x=20, y=112, w=140, h=120), dict(title="PROGRAMMING / DEBUG", x=165, y=217, w=130, h=45), dict(title="MICROPHONE AMPLIFIER: gain 34, high-pass 0.7 kHz, anti-alias 7 kHz", x=300, y=22, w=115, h=190)],
 notes=[("Supply 2.0-3.3 V. ATmega328P: internal 8 MHz RC, firmware divides to 4 MHz (8 MHz needs >= 2.7 V). Fuses lfuse 0xE2, hfuse 0xD9, efuse 0xFE (BOD 1.8 V).", 20, 272), ("Amp: gain = 1 + R8/R9 = 34 (SPICE: 32.8 at 2.8 kHz), band 0.7-26 kHz (-3 dB) then R10/C9 anti-alias 7.2 kHz, VMID = VCC/2 with 10 uF bypass so the feedback return is low impedance.", 20, 279), ("Q2 (AO3401A): drain=battery side, source=load, gate=GND: blocks reversed batteries.", 20, 286)])
for _p in parts:
    if _p.get('lcsc', 1) is None: del _p['lcsc']
BOARD = dict(name="seeti_counter", title="Seeti Counter - main board", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"+3V0": "battery via Q2", "GND": "battery"}, single_ok=("RXD", "TXD", "BAT_P"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)],
 widths={"+3V0": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["MIC_OUT", "MIC_AC", "FB"],
 silk=[("SEETI COUNTER rev B", 13.5, H - 1.7, 0.9), ("BATT+", 8, 34.0, 0.8), ("MIC", 44.5, 5.0, 0.8), ("ISP", 46.5, 33.0, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J3", "top", 9, 7, 3), ("J1", "bottom", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7, )])
