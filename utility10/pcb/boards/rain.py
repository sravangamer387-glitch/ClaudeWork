from .common import *
BOARD = dict(name="rain_alert_main", title="Rain Alert indoor unit", rev="rev A", size=(56, 38), parts=[
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=30, y=20, rot=0, nets={
   "4": "+4V5", "6": "+4V5", "18": "+4V5", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "SENSE", "9": "DRV_MCU", "13": "BUZ", "32": "BTN", "11": "LED"}),
 dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="3xAA", x=6, y=34, rot=0, nets={"1": "BAT_P", "2": "GND"}),
 dict(ref="SW1", sym="Switch:SW_SPDT", fp="Button_Switch_SMD:SW_SPDT_PCM12", value="Power", x=17, y=35, rot=0, nets={"1": "+4V5", "2": "BAT_P"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=50, y=30, rot=0, nets={"1": "MISO", "2": "+4V5", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x02", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", value="Rain plate", x=52, y=6, rot=0, nets={"1": "DRV", "2": "SENSE"}),
 dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer 85dB", x=10, y=14, rot=0, nets={"1": "+4V5", "2": "BZ_N"}),
 dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=14, y=26, rot=0, nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
 dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=21, y=28, rot=0, nets={"1": "+4V5", "2": "BZ_N"}),
 dict(ref="SW2", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Mute", x=30, y=6, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Red", x=40, y=34, rot=0, nets={"1": "GND", "2": "LED_A"}),
 R("R1", "1k", 44, 11, "DRV_MCU", "DRV"), R("R2", "100k", 47, 15, "SENSE", "GND", 90), R("R5", "1k", 34, 34, "LED", "LED_A"), R("R6", "1k", 9, 27, "BUZ", "BUZ_B"), R("R7", "10k", 22, 6, "+4V5", "RESET"),
 C("C1", "100n", 22, 17, "+4V5", "GND", 90), C("C2", "100n", 38, 25, "+4V5", "GND", 90), C("C3", "100n", 38, 17, "AREF", "GND", 90), C("C4", "10u", 24, 34, "+4V5", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"), C("C5", "10n", 47, 19, "SENSE", "GND", 90),
])
