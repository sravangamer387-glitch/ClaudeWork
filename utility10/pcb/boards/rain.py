from .common import *
W, H = 60, 42
parts = [
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=33, y=22, rot=0, mpn="ATMEGA328P-AU", lcsc="C14877", lcsc_status="verified", nc="rest", nets={
   "4": "+4V5", "6": "+4V5", "18": "+4V5", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "SENSE", "25": "DRV_MCU", "13": "BUZ", "32": "BTN", "11": "LED"}),
 dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="BATT 3xAA", x=11, y=36.5, rot=0, nets={"1": "BAT_P", "2": "GND"}),
 dict(ref="SW1", sym="Switch:SW_SPDT", fp="Button_Switch_SMD:SW_SPDT_PCM12", value="Power", x=22, y=37.5, rot=0, nc=["3"], nets={"1": "BAT_SW", "2": "BAT_P"}),
 dict(ref="Q2", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=30, y=37, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "GND", "2": "+4V5", "3": "BAT_SW"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=48, y=29, rot=0, nets={"1": "MISO", "2": "+4V5", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="Rain plate", x=48, y=9.5, rot=0, nets={"1": "DRV", "2": "SENSE_J"}),
 dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer 85dB", x=14, y=11, rot=0, nets={"1": "+4V5", "2": "BZ_N"}),
 dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=15, y=26, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
 dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=22, y=28, rot=0, lcsc="C2128", lcsc_status="verified", mpn="1N4148WS", nets={"1": "+4V5", "2": "BZ_N"}),
 dict(ref="SW2", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Mute", x=33, y=6, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Red", x=44, y=37.5, rot=0, nets={"1": "GND", "2": "LED_A"}),
 dict(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SOD-323", value="TVS 5V bidir", x=54, y=14, rot=90, nets={"1": "DRV", "2": "GND"}),
 dict(ref="D4", sym="Device:D_TVS", fp="Diode_SMD:D_SOD-323", value="TVS 5V bidir", x=54, y=19, rot=90, nets={"1": "SENSE_J", "2": "GND"}),
 R("R1", "1k", 42, 9, "DRV_MCU", "DRV"), R("R2", "100k", 47, 22, "SENSE", "GND", 90), R("R3", "1k", 42, 13, "SENSE_J", "SENSE"), R("R5", "1k", 39, 37.5, "LED", "LED_A"), R("R6", "1k", 10, 28, "BUZ", "BUZ_B"), R("R7", "10k", 26, 6, "+4V5", "RESET"),
 C("C1", "100n", 23, 19, "+4V5", "GND", 90), C("C2", "100n", 42, 26, "+4V5", "GND", 90), C("C3", "100n", 42, 18, "AREF", "GND", 90), C("C4", "10u", 35, 37, "+4V5", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"), C("C5", "2.2n", 50, 23, "SENSE", "GND", 90, lcsc=None),
 TP("TP1", "+4V5", 4, 20), TP("TP2", "GND", 4, 24), TP("TP3", "SENSE", 40, 31),
]
for p in parts:
    if p.get("lcsc") is None and "lcsc" in p: del p["lcsc"]
S = dict(paper="A3", auto_wire_max=80,
 place={"J1": (35, 50, 90), "SW1": (70, 50, 0), "Q2": (105, 55, 0), "C4": (135, 60, 0), "TP1": (35, 90, 0), "TP2": (55, 90, 0),
        "U1": (235, 125, 0), "C1": (180, 40, 0), "C2": (200, 40, 0), "C3": (220, 40, 0), "R7": (240, 40, 0),
        "BZ1": (45, 135, 0), "D2": (85, 135, 0), "Q1": (50, 175, 0), "R6": (25, 175, 90), "R5": (95, 165, 0), "D1": (95, 195, 0), "SW2": (50, 215, 0),
        "J3": (320, 55, 90), "R1": (350, 45, 0), "D3": (380, 60, 0), "R3": (350, 100, 0), "D4": (380, 115, 0), "R2": (330, 150, 0), "C5": (360, 150, 0), "TP3": (390, 150, 0),
        "J2": (200, 235, 0)},
 blocks=[dict(title="POWER INPUT: 3xAA, switch, reverse-polarity PMOS", x=20, y=22, w=140, h=85), dict(title="MCU: ATmega328P-AU, internal RC 8 MHz", x=165, y=22, w=130, h=190),
         dict(title="ALARM: buzzer driver, LED, mute", x=20, y=112, w=140, h=120), dict(title="PROGRAMMING", x=165, y=217, w=130, h=45), dict(title="RAIN PLATE INTERFACE: pulsed drive, series R + TVS", x=300, y=22, w=115, h=190)],
 notes=[("Plate is driven only while measuring (DRV high ~2-5 ms, then low): no DC across the wet plate, far less electrolytic corrosion.", 20, 272), ("SENSE node: plate R + 1k vs 100k pull-down, 2.2 nF filter. Cable lines have 1k series R and bidirectional TVS to GND (lightning/ESD).", 20, 279), ("3xAA 4.5 V: 8 MHz is within spec down to 2.7 V; fuses lfuse 0xE2 hfuse 0xD9 efuse 0xFD (BOD 2.7 V).", 20, 286)])
BOARD = dict(name="rain_alert_main", title="Rain Alert Bell - indoor unit", rev="B", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"+4V5": "battery via Q2", "GND": "battery"}, single_ok=("BAT_P",),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (W - 14, H - 2.5)],
 widths={"+4V5": 0.4, "BAT_P": 0.4, "BAT_SW": 0.4}, first=["SENSE", "DRV"],
 silk=[("RAIN ALERT BELL rev B", 36, H - 1.3, 0.9), ("PLATE", 46, 6.6, 0.8), ("BATT+", 9, 33.2, 0.8), ("ISP", 48, 25, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "bottom", 9, 7, 3), ("J3", "top", 9, 7, 3), ("SW1", "bottom", 8, 5, 2.5)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7)])
