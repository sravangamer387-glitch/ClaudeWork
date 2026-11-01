from .blocks import *
W, H = 100, 80
V = lambda **k: dict(k, lcsc_status="verified")
parts = [
 V(ref="J2", sym="Connector:Barrel_Jack", fp="Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal", value="12 V DC in", x=8, y=14, rot=0, lcsc="C22434582", mpn="CUI/Same Sky PJ-063AH", nets={"1": "VIN12", "2": "GND"}),
 V(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1812_4532Metric", value="PTC 1A 16V", x=20, y=5, rot=0, lcsc="C142746", mpn="Littelfuse 1812L110/16DR", nets={"1": "VIN12", "2": "VIN_F"}),
 V(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMB", value="SMBJ15A", x=20, y=12, rot=0, lcsc="C83846", mpn="Littelfuse SMBJ15A", nets={"1": "VIN_F", "2": "GND"}),
 V(ref="Q5", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=26, y=16, rot=0, lcsc="C15127", mpn="AO3401A", nets={"1": "GATE", "2": "VM", "3": "VIN_F"}),
 V(ref="D4", sym="Device:D_Zener", fp="Diode_SMD:D_SOD-123", value="BZT52C12", x=26, y=22, rot=0, lcsc="C124196", mpn="DIODES BZT52C12-7-F", nets={"1": "VM", "2": "GATE"}),
 R("R40", "10k", 32, 22, "GATE", "GND", 90),
 V(ref="C30", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=34, y=6, rot=0, lcsc="C7442639", mpn="Lelon VEJ101M1VTT-0607L", nets={"1": "VM", "2": "GND"}),
 V(ref="C31", sym="Device:C", fp="Capacitor_SMD:C_1210_3225Metric", value="10u/50V", x=42, y=6, rot=0, lcsc="C380537", mpn="Samsung CL32A106KBJNNNE", nets={"1": "VM", "2": "GND"}),
 V(ref="U2", sym="Regulator_Switching:AP63205WU", fp="Package_TO_SOT_SMD:TSOT-23-6", value="AP63205WU-7", x=46, y=14, rot=0, lcsc="C2071056", mpn="AP63205WU-7", nets={"1": "+5V", "2": "EN_B", "3": "VM", "4": "GND", "5": "SW", "6": "BST"}),
 R("R41", "100k", 41, 19, "VM", "EN_B", 90), C("C32", "100n", 50.6, 13.05, "BST", "SW", 0),
 V(ref="L1", sym="Device:L", fp="Inductor_SMD:L_Changjiang_FNR5040S", value="4.7u", x=46, y=28, rot=90, lcsc="C167963", mpn="Changjiang FNR5040S4R7MT", nets={"1": "SW", "2": "+5V"}),
 V(ref="C33", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=53, y=30, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+5V", "2": "GND"}),
 V(ref="C34", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=53, y=35, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+5V", "2": "GND"}),
 V(ref="D5", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=66, y=28, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VBUS", "2": "+5V"}),
 V(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=62, y=42, rot=0, lcsc="C51118", mpn="AP2112K-3.3TRG1", nets={"1": "+5V", "2": "GND", "3": "+5V", "5": "+3V3"}, nc=["4"]),
 C("C35", "1u", 56, 43, "+5V", "GND", 90), C("C36", "10u", 68, 43, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 V(ref="U1", sym="RF_Module:ESP32-S3-WROOM-1", fp="RF_Module:ESP32-S3-WROOM-1", value="ESP32-S3-WROOM-1-N8", x=84, y=24, rot=0, lcsc="C2913198", mpn="ESP32-S3-WROOM-1-N8", nc="rest",
   nets={"1": "GND", "40": "GND", "41": "GND", "2": "+3V3", "3": "EN", "27": "BOOT", "4": "PUMP1_G", "5": "PUMP2_G", "6": "LIGHT_G", "7": "FAN_G", "12": "SDA", "17": "SCL", "18": "LEVEL", "8": "ONEWIRE", "39": "PH_ADC", "38": "EC_ADC", "25": "LED", "37": "UART_TX", "36": "UART_RX"}),
 C("C37", "100n", 66, 50, "+3V3", "GND", 90), C("C38", "10u", 70, 50, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 R("R42", "10k", 58, 24, "+3V3", "EN", 90), C("C39", "1u", 58, 29, "EN", "GND", 90),
 button("SW2", "EN", 78, 46, "Reset (EN)"), button("SW3", "BOOT", 86, 46, "Boot (IO0)"),
 dict(ref="J1", sym="Connector:USB_C_Receptacle_USB2.0_16P", fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", value="USB-C", x=52, y=6, rot=180, lcsc="C165948", lcsc_status="verified", mpn="TYPE-C-31-M-12", nc=["A6", "A7", "A8", "B6", "B7", "B8"],
      nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2", "S1": "GND"}),
 R("R43", "5.1k", 56, 20, "CC1", "GND", 90), R("R44", "5.1k", 60, 20, "CC2", "GND", 90),
 LED("D6", "Green", 50, 44, "GND", "LED_A"), R("R45", "1k", 50, 49, "LED", "LED_A", 90),
 jst("J7", 3, 62, 56, ["+3V3", "ONEWIRE", "GND"], "Water temp DS18B20"), R("R46", "4.7k", 55, 56, "+3V3", "ONEWIRE", 90),
 jst("J8", 4, 88, 58, ["+3V3", "SDA", "SCL", "GND"], "I2C (BH1750 / SHT31)"), R("R47", "4.7k", 80, 62, "+3V3", "SDA", 90), R("R48", "4.7k", 84, 62, "+3V3", "SCL", 90),
 jst("J9", 2, 88, 70, ["LEVEL", "GND"], "Water-level float switch"), R("R49", "10k", 80, 70, "+3V3", "LEVEL", 90),
 jst("J10", 3, 70, 66, ["+5V", "PH_J", "GND"], "pH module (0-3 V analog)"), R("R50", "1k", 64, 66, "PH_J", "PH_ADC", 90), C("C40", "100n", 62, 62, "PH_ADC", "GND", 90),
 jst("J11", 3, 70, 74, ["+5V", "EC_J", "GND"], "EC module (0-3 V analog)"), R("R51", "1k", 64, 74, "EC_J", "EC_ADC", 90), C("C41", "100n", 60, 74, "EC_ADC", "GND", 90),
 jst("J12", 3, 24, 36, ["GND", "UART_TX", "UART_RX"], "UART flash/debug (USB-serial adapter)"), TP("TP1", "VM", 6, 34), TP("TP2", "+5V", 6, 40), TP("TP3", "+3V3", 6, 46), TP("TP4", "GND", 6, 52)]
for k, (nm, gnet, lbl) in enumerate([("PUMP1", "PUMP1_G", "Pump 1"), ("PUMP2", "PUMP2_G", "Pump 2"), ("LIGHT", "LIGHT_G", "Grow light (PWM)"), ("FAN", "FAN_G", "Fan")]):
    x0 = 10 + 13 * k; d = f"{nm}_D"
    parts += [V(ref=f"Q{1 + k}", sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=x0, y=58, rot=0, lcsc="C20917", mpn="AO3400A", nets={"1": f"{nm}_GR", "2": "GND", "3": d}),
              R(f"R{10 + k}", "100", x0 - 5, 56, gnet, f"{nm}_GR"), R(f"R{14 + k}", "100k", x0 - 5, 61, f"{nm}_GR", "GND"),
              jst(f"J{3 + k}", 2, x0 + 3, 72, ["VM", d], lbl)]
    if nm != "LIGHT": parts.append(V(ref=f"D{10 + k}", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=x0 + 7, y=67, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VM", "2": d}))
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER IN: 12 V, PTC, TVS, reverse-polarity PMOS with 12 V gate clamp, bulk", ["J2", "F1", "D3", "Q5", "D4", "R40", "C30", "C31", "TP1", "TP4"]), ("5 V BUCK AP63205 + 3.3 V LDO", ["U2", "R41", "C32", "L1", "C33", "C34", "D5", "U3", "C35", "C36", "TP2", "TP3"]),
               ("CONTROLLER: ESP32-S3 (WiFi + MQTT), USB-C", ["U1", "C37", "C38", "R42", "C39", "SW2", "SW3", "D6", "R45", "J1", "R43", "R44", "J12"]),
               ("LOW-SIDE LOAD DRIVERS: 2 pumps, grow-light PWM, fan (12 V)", [f"Q{1 + k}" for k in range(4)] + [f"R{10 + k}" for k in range(4)] + [f"R{14 + k}" for k in range(4)] + [f"J{3 + k}" for k in range(4)] + ["D10", "D11", "D13"]),
               ("SENSORS: water temp, I2C, level switch, pH and EC analog inputs", ["J7", "R46", "J8", "R47", "R48", "J9", "R49", "J10", "R50", "C40", "J11", "R51", "C41"])], big=("U1",))
S["notes"] = [("BioTray: ESP32-S3 grows-tray controller. Two 12 V pumps and a fan are switched low-side with flyback diodes; the grow light is PWM dimmed (no flyback diode: LED strip). Pump, fan and light total must stay under the PTC rating (1.1 A hold): fit a larger PTC or fuse for bigger loads. pH and EC are off-the-shelf analog modules with 0-3 V outputs; calibrate in firmware. Water-level float switch closes to GND when water is present.", 0, 0)]
PRE = [dict(net="BST", layer=0, pts=[(47.14, 13.05), (48.34, 13.05), (49.83, 13.05)], w=0.2), dict(net="SW", layer=0, pts=[(47.14, 14.0), (48.34, 14.0), (51.37, 14.0), (51.37, 13.05)], w=0.4)]
PREV = [("GND", 81.40, 25.36), ("GND", 81.40, 27.56), ("GND", 83.60, 25.36), ("GND", 83.60, 27.56)]
BOARD = dict(pre=PRE, pre_vias=PREV, clr=0.15, name="biotray", title="BioTray vertical-farm tray controller (ESP32-S3, MQTT)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"VIN12": "external 12 V adapter", "VM": "12 V via reverse-polarity PMOS Q5", "+5V": "buck U2 or USB VBUS via D5", "+3V3": "LDO U3", "GND": "supply", "VBUS": "USB host", "VIN_F": "12 V after PTC"}, single_ok=("CC1", "CC2"),
 ws=(0.2, 0.4), widths={"VBUS": 0.4, "VM": 0.4, "+5V": 0.4, "SW": 0.4, "VIN12": 0.4, "VIN_F": 0.4, "PUMP1_D": 0.4, "PUMP2_D": 0.4, "LIGHT_D": 0.4, "FAN_D": 0.4},
 holes=[(3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 48), (95, 52)], first=["CC1", "CC2", "VBUS", "VIN12", "VIN_F", "VM", "SW", "+5V"], edge_ok=("J1",), gnd_pour_only=True,
 silk=[("BioTray rev A", 40, 77, 1.2), ("12V IN", 10, 3.5, 0.9)], stitch=5.0)
BOARD["enc"] = dict(standoff=5.0, side=[("J2", "left", 8, 10, 9)], lid=[])
