from .common import *
BOARD = dict(name="bijli_meter_reader", title="Bijli Meter Reader main board", rev="rev A", size=(48, 34), first=["VBUS", "BTN"], parts=[
 dict(ref="U1", sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=27, y=19, rot=0, nets={
   "4": "+5V", "6": "+5V", "18": "+5V", "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK",
   "23": "SIG", "1": "DCLK", "2": "DIO", "32": "BTN", "11": "LED"}),
 dict(ref="J1", sym="Connector:USB_B_Micro", fp="Connector_USB:USB_Micro-B_Amphenol_10118194_Horizontal", value="Micro-USB 5V", x=24, y=5, rot=0, nets={"1": "VBUS", "5": "GND", "6": "GND"}),
 dict(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_0805_2012Metric", value="500mA PTC", x=33, y=5, rot=0, nets={"1": "VBUS", "2": "+5V"}),
 dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=42, y=24, rot=0, nets={"1": "MISO", "2": "+5V", "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"}),
 dict(ref="J3", sym="Connector_Generic:Conn_01x03", fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", value="Sensor head", x=3.5, y=24, rot=0, nets={"1": "+5V", "2": "SIG", "3": "GND"}),
 dict(ref="J4", sym="Connector_Generic:Conn_01x04", fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", value="TM1637 display", x=44.5, y=7, rot=0, nets={"1": "GND", "2": "+5V", "3": "DIO", "4": "DCLK"}),
 dict(ref="SW1", sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value="Reset bill", x=20, y=11.5, rot=0, nets={"1": "BTN", "2": "GND"}),
 dict(ref="D1", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Green", x=37, y=31, rot=0, nets={"1": "GND", "2": "LED_A"}),
 R("R3", "10k", 14, 15, "+5V", "RESET", 90), R("R4", "10k", 11, 20, "+5V", "SIG", 90), R("R5", "1k", 33, 31, "LED", "LED_A"),
 C("C1", "10u", 36, 10, "+5V", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"), C("C2", "100n", 20, 17, "+5V", "GND", 90), C("C3", "100n", 35, 25, "+5V", "GND", 90), C("C4", "100n", 35, 17, "AREF", "GND", 90), C("C5", "100n", 11, 25, "SIG", "GND", 90),
])
