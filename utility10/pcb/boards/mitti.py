from .blocks import *
W, H = 90, 80
V = lambda **k: dict(k, lcsc_status="verified")
parts = [
 V(ref="U1", sym="RF_Module:ESP32-S3-WROOM-1", fp="RF_Module:ESP32-S3-WROOM-1", value="ESP32-S3-WROOM-1-N8", x=76, y=26, rot=0, lcsc="C2913198", mpn="ESP32-S3-WROOM-1-N8", nc="rest",
   nets={"1": "GND", "40": "GND", "41": "GND", "2": "+3V3", "3": "EN", "27": "BOOT", "8": "ONEWIRE", "9": "MODEM_TX", "10": "MODEM_RX", "11": "MODEM_PWRKEY", "12": "MODEM_STATUS", "6": "MODEM_EN", "4": "HX_DT", "5": "HX_SCK", "17": "ACC_INT", "18": "SDA", "19": "SCL", "39": "SOIL_ADC", "38": "VBAT_ADC", "25": "LED", "37": "UART_TX", "36": "UART_RX"}),
 C("C37", "100n", 62, 36, "+3V3", "GND", 90), C("C38", "10u", 58, 36, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 R("R42", "10k", 60, 22, "+3V3", "EN", 90), C("C39", "1u", 60, 27, "EN", "GND", 90), button("SW2", "EN", 58, 46, "Reset (EN)"), button("SW3", "BOOT", 66, 46, "Boot (IO0)"),
 dict(ref="J1", sym="Connector:USB_C_Receptacle_USB2.0_16P", fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", value="USB-C (charge + program)", x=34, y=6, rot=180, lcsc="C165948", lcsc_status="verified", mpn="TYPE-C-31-M-12", nc=["A6", "A7", "A8", "B6", "B7", "B8"],
      nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2", "S1": "GND"}),
 R("R43", "5.1k", 32, 20, "CC1", "GND", 90), R("R44", "5.1k", 36, 20, "CC2", "GND", 90),
 jst("J2", 2, 6, 6, ["SOLAR", "GND"], "Solar panel 5-6 V"),
 V(ref="D1", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=16, y=6, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "SOLAR", "2": "VCC_CHG"}),
 V(ref="D2", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=16, y=12, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VBUS", "2": "VCC_CHG"}),
 C("C1", "10u", 24, 6, "VCC_CHG", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 V(ref="U4", sym="KN:TP4056", fp="Package_SO:HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm", value="TP4056", x=16, y=24, rot=0, lcsc="C382139", mpn="TPOWER TP4056", nets={"1": "GND", "2": "PROG", "3": "GND", "4": "VCC_CHG", "5": "VBAT", "6": "STDBY_K", "7": "CHRG_K", "8": "VCC_CHG"}),
 R("R1", "2.2k", 6, 28, "PROG", "GND", 90), C("C2", "10u", 26, 28, "VBAT", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 LED("D3", "Red (charging)", 8, 34, "CHRG_K", "CHRG_A"), R("R2", "1k", 8, 39, "VCC_CHG", "CHRG_A", 90), LED("D4", "Green (done)", 14, 34, "STDBY_K", "STDBY_A"), R("R3", "1k", 14, 39, "VCC_CHG", "STDBY_A", 90),
 jst("J3", 2, 28, 44, ["VBAT", "GND"], "Li-ion cell (protected!)"),
 V(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=38, y=32, rot=0, lcsc="C51118", mpn="AP2112K-3.3TRG1", nets={"1": "VBAT", "2": "GND", "3": "VBAT", "5": "+3V3"}, nc=["4"]),
 C("C3", "1u", 32, 33, "VBAT", "GND", 90), C("C4", "10u", 44, 33, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 R("R4", "330k", 20, 46, "VBAT", "VBAT_ADC", 90), R("R5", "330k", 20, 51, "VBAT_ADC", "GND", 90), C("C5", "100n", 25, 51, "VBAT_ADC", "GND", 90),
 V(ref="Q1", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=8, y=56, rot=0, lcsc="C15127", mpn="AO3401A", nets={"1": "MGATE", "2": "VBAT", "3": "VBAT_M"}),
 R("R6", "100k", 14, 55, "VBAT", "MGATE", 90),
 V(ref="Q2", sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=14, y=62, rot=0, lcsc="C20917", mpn="AO3400A", nets={"1": "MEN_GR", "2": "GND", "3": "MGATE"}),
 R("R7", "100", 8, 62, "MODEM_EN", "MEN_GR"), R("R8", "100k", 8, 66, "MEN_GR", "GND"),
 V(ref="C6", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=24, y=66, rot=0, lcsc="C7442639", mpn="Lelon VEJ101M1VTT-0607L", nets={"1": "VBAT_M", "2": "GND"}),
 V(ref="C7", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=31, y=64, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "VBAT_M", "2": "GND"}),
 dict(ref="J6", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="Cellular modem (SIM7080G breakout)", x=40, y=66, rot=0, lcsc="C5116479", lcsc_status="verified", mpn="ZHOURI 2.54-2*3", nets={"1": "VBAT_M", "2": "GND", "3": "MODEM_TX", "4": "MODEM_RX", "5": "MODEM_PWRKEY", "6": "MODEM_STATUS"}),
 V(ref="U5", sym="Sensor_Motion:ADXL343", fp="Package_LGA:LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y", value="ADXL345", x=62, y=50, rot=0, lcsc="C9667", mpn="ADXL345BCCZ-RL7", nets={"1": "+3V3", "2": "GND", "4": "GND", "5": "GND", "6": "+3V3", "7": "+3V3", "12": "GND", "13": "SDA", "14": "SCL", "8": "ACC_INT"}, nc=["3", "9", "10", "11"]),
 C("C8", "100n", 56, 48, "+3V3", "GND", 90), C("C9", "100n", 68, 46, "+3V3", "GND", 90), R("R9", "4.7k", 66, 54, "+3V3", "SDA", 90), R("R10", "4.7k", 70, 54, "+3V3", "SCL", 90),
 V(ref="U2", sym="Analog_ADC:HX711", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="HX711", x=80, y=64, rot=0, lcsc="C43656", mpn="HX711", nc=["2", "9", "10", "13"],
   nets={"1": "+3V3", "3": "AVDD", "4": "AVDD", "5": "GND", "6": "VBG", "7": "A_N", "8": "A_P", "11": "HX_SCK", "12": "HX_DT", "14": "GND", "15": "GND", "16": "+3V3"}),
 R("R11", "100", 74, 60, "+3V3", "AVDD", 90), C("C10", "100n", 78, 60, "AVDD", "GND", 90), C("C11", "100n", 84, 60, "+3V3", "GND", 90), C("C12", "100n", 66, 68, "VBG", "GND", 90), C("C13", "10u", 70, 62, "AVDD", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
 R("R12", "100", 66, 72, "AVDD", "EXC", 90), C("C14", "100n", 62, 70, "EXC", "GND", 90), C("C15", "100n", 82, 70, "A_P", "A_N", 90),
 jst("J4", 4, 80, 76, ["EXC", "GND", "A_P", "A_N"], "Strain-gauge bridge E+ E- A+ A-"),
 jst("J5", 3, 30, 77, ["+3V3", "SOIL_J", "GND"], "Soil probe (capacitive, 3.3 V)"),
 V(ref="J7", sym="Connector_Generic:Conn_01x03", fp="Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", value="DS18B20 temp", x=46, y=77, rot=0, lcsc="C131339", mpn="JST B3B-PH-K-S", nets={"1": "+3V3", "2": "ONEWIRE", "3": "GND"}),
 R("R13", "4.7k", 52, 76, "+3V3", "ONEWIRE", 90), R("R15", "1k", 22, 76, "SOIL_J", "SOIL_ADC", 90), C("C16", "100n", 22, 72, "SOIL_ADC", "GND", 90),
 LED("D5", "Green", 34, 50, "GND", "LED_A"), R("R14", "1k", 34, 45, "LED", "LED_A", 90),
 jst("J8", 3, 50, 10, ["GND", "UART_TX", "UART_RX"], "UART flash/debug (USB-serial adapter)"), TP("TP1", "VBAT", 4, 50), TP("TP2", "+3V3", 4, 44), TP("TP3", "GND", 4, 14)]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("CHARGER: solar + USB, TP4056, Li-ion cell, 3.3 V LDO", ["J2", "D1", "D2", "C1", "U4", "R1", "C2", "D3", "R2", "D4", "R3", "J3", "U3", "C3", "C4", "R4", "R5", "C5", "TP1", "TP2", "TP3"]),
               ("CONTROLLER: ESP32-S3 (deep sleep between reports), USB-C", ["U1", "C37", "C38", "R42", "C39", "SW2", "SW3", "D5", "R14", "J1", "R43", "R44", "J8"]),
               ("CELLULAR MODEM SOCKET: high-side switch, burst capacitors, UART", ["Q1", "R6", "Q2", "R7", "R8", "C6", "C7", "J6"]),
               ("SENSORS: tilt/vibration (ADXL345), strain bridge (HX711), soil probe, temperature", ["U5", "C8", "C9", "R9", "R10", "R15", "C16", "U2", "R11", "C10", "C11", "C12", "C13", "R12", "C14", "C15", "J4", "J5", "J7", "R13"])], big=("U1",))
S["notes"] = [("MITTI-NETRA: solar/USB charge a protected 1S Li-ion cell through a TP4056 (charge current about 0.58 A with R1 = 2.2 k). The ESP32-S3 deep-sleeps and reports through a plug-in SIM7080G breakout (LTE-M / NB-IoT) that is powered through the high-side switch Q1 only while transmitting; the socket brings out VBAT, GND, UART and PWRKEY/STATUS: match your breakout's pinout. ADXL345 on I2C gives tilt and vibration; HX711 reads a strain-gauge bridge; capacitive soil probe on an ADC pin; DS18B20 temperature on 1-Wire. LDO cutoff: the node stops regulating below about 3.55 V on the cell.", 0, 0)]
PREV = [("GND", 73.40, 27.36), ("GND", 73.40, 29.56), ("GND", 75.60, 27.36), ("GND", 75.60, 29.56)]
BOARD = dict(pre_vias=PREV, clr=0.15, name="mitti_netra", title="MITTI-NETRA soil and structure telemetry node (ESP32-S3 + LTE-M modem socket)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"VBAT": "Li-ion cell", "VBAT_M": "VBAT through Q1", "VCC_CHG": "solar/USB through D1/D2", "+3V3": "LDO U3", "GND": "battery", "VBUS": "USB host", "AVDD": "HX711 analog supply via R11", "SOLAR": "solar panel"}, single_ok=("CC1", "CC2", "STDBY_K"),
 ws=(0.2, 0.4), widths={"VBUS": 0.4, "VBAT": 0.4, "VBAT_M": 0.4, "VCC_CHG": 0.4, "SOLAR": 0.4},
 holes=[(3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, H - 3.5), (W - 14, H - 3.5)], first=["CC1", "CC2", "VBUS", "VBAT", "VBAT_M", "VCC_CHG", "+3V3", "SDA", "SCL"], edge_ok=("J1",), gnd_pour_only=True,
 silk=[("MITTI-NETRA rev A", 10, 77, 1.1)], stitch=5.0)
BOARD["enc"] = dict(standoff=5.0, side=[("J2", "left", 6, 6, 4)], lid=[])
