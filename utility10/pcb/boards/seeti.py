from .common import *
BOARD = dict(name="seeti_counter", title="Seeti Counter main board", rev="rev A", size=(60, 40), parts=[
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=30, y=20, rot=0, nets={
   "4": "+3V0", "6": "+3V0", "18": "+3V0", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "MIC_OUT", "13": "BUZ", "32": "BTN", "11": "LED"}),
 dict(ref="U2", sym="Amplifier_Operational:MCP6001-OT", fp="Package_TO_SOT_SMD:SOT-23-5", value="MCP6001", x=47, y=14, rot=0, nets={"1": "MIC_OUT", "2": "GND", "3": "MIC_AC", "4": "FB", "5": "+3V0"}),
 dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="2xAAA", x=6, y=34, rot=0, nets={"1": "BAT_P", "2": "GND"}),
 dict(ref="SW1", sym="Switch:SW_SPDT", fp="Button_Switch_SMD:SW_SPDT_PCM12", value="Power", x=17, y=35, rot=0, nets={"1": "+3V0", "2": "BAT_P"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=51, y=31, rot=0, nets={"1": "MISO", "2": "+3V0", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x02", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", value="Electret mic", x=55, y=5, rot=0, nets={"1": "MIC_P", "2": "GND"}),
 dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer 3V", x=10, y=15, rot=0, nets={"1": "+3V0", "2": "BZ_N"}),
 dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=14, y=26, rot=0, nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
 dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=21, y=28, rot=0, nets={"1": "+3V0", "2": "BZ_N"}),
 dict(ref="SW2", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Target", x=30, y=6, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Green", x=38, y=35, rot=0, nets={"1": "GND", "2": "LED_A"}),
 R("R1", "2.2k", 51, 9, "+3V0", "MIC_P"), R("R2", "100k", 54, 17, "+3V0", "VMID", 90), R("R3", "100k", 54, 22, "VMID", "GND", 90), R("R4", "100k", 47, 20, "VMID", "MIC_AC"),
 R("R5", "1k", 33, 35, "LED", "LED_A"), R("R6", "1k", 9, 27, "BUZ", "BUZ_B"), R("R7", "10k", 22, 6, "+3V0", "RESET"), R("R8", "100k", 41, 9, "MIC_OUT", "FB"), R("R9", "1k", 41, 13, "FB", "FBN"),
 C("C1", "100n", 21, 17, "+3V0", "GND", 90), C("C2", "100n", 37, 25, "+3V0", "GND", 90), C("C3", "100n", 37, 17, "AREF", "GND", 90), C("C4", "10u", 24, 34, "+3V0", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
 C("C5", "1u", 50, 17, "MIC_P", "MIC_AC", 90), C("C6", "10u", 41, 17, "FBN", "VMID", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C7", "100n", 57, 17, "VMID", "GND", 90),
])
