from .blocks import *
W, H = 112, 80
V = lambda **k: dict(k, lcsc_status="verified")
parts = [
 V(ref="J5", sym="Connector:Screw_Terminal_01x02", fp="TerminalBlock:TerminalBlock_bornier-2_P5.08mm", value="24 V in", x=8, y=14, rot=0, lcsc="C474952", mpn="KF128-5.08-2P-AA", nets={"1": "VIN24", "2": "GND"}),
 V(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMB", value="SMBJ28A", x=20, y=6, rot=0, lcsc="C178227", mpn="Littelfuse SMBJ28A", nets={"1": "VIN24", "2": "GND"}),
 V(ref="Q5", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=22, y=14, rot=0, lcsc="C15127", mpn="AO3401A", nets={"1": "GATE", "2": "VM", "3": "VIN24"}),
 V(ref="D4", sym="Device:D_Zener", fp="Diode_SMD:D_SOD-123", value="BZT52C12", x=22, y=20, rot=0, lcsc="C124196", mpn="DIODES BZT52C12-7-F", nets={"1": "VM", "2": "GATE"}),
 R("R40", "10k", 28, 20, "GATE", "GND", 90),
 V(ref="C30", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=30, y=6, rot=0, lcsc="C176683", mpn="Lelon VZH101M1VTR-0607", nets={"1": "VM", "2": "GND"}),
 V(ref="C31", sym="Device:C", fp="Capacitor_SMD:C_1210_3225Metric", value="10u/50V", x=40, y=6, rot=0, lcsc="C380537", mpn="Samsung CL32A106KBJNNNE", nets={"1": "VM", "2": "GND"}),
 V(ref="U2", sym="Regulator_Switching:AP63205WU", fp="Package_TO_SOT_SMD:TSOT-23-6", value="AP63205WU-7", x=44, y=12, rot=0, lcsc="C2071056", mpn="AP63205WU-7", nets={"1": "+5V", "2": "EN_B", "3": "VM", "4": "GND", "5": "SW", "6": "BST"}),
 R("R41", "100k", 40, 18, "VM", "EN_B", 90),
 C("C32", "100n", 48.6, 11.05, "BST", "SW", 0),
 V(ref="L1", sym="Device:L", fp="Inductor_SMD:L_Changjiang_FNR5040S", value="4.7u", x=44, y=26, rot=90, lcsc="C167963", mpn="Changjiang FNR5040S4R7MT", nets={"1": "SW", "2": "+5V"}),
 V(ref="C33", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=50, y=28, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+5V", "2": "GND"}),
 V(ref="C34", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=50, y=33, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+5V", "2": "GND"}),
 V(ref="D5", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=66, y=28, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VBUS", "2": "+5V"}),
 V(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=48, y=40, rot=0, lcsc="C51118", mpn="AP2112K-3.3TRG1", nets={"1": "+5V", "2": "GND", "3": "+5V", "5": "+3V3"}, nc=["4"]),
 C("C35", "1u", 42, 41, "+5V", "GND", 90), C("C36", "10u", 54, 41, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 V(ref="U1", sym="RF_Module:ESP32-S3-WROOM-1", fp="RF_Module:ESP32-S3-WROOM-1", value="ESP32-S3-WROOM-1-N8", x=92, y=26, rot=0, lcsc="C2913198", mpn="ESP32-S3-WROOM-1-N8", nc="rest",
   nets={"1": "GND", "40": "GND", "41": "GND", "2": "+3V3", "3": "EN", "27": "BOOT", "4": "X_STEP", "5": "X_DIR", "6": "X_EN", "7": "Y_STEP", "8": "Y_DIR", "9": "Y_EN", "10": "Z_STEP", "11": "Z_DIR", "12": "Z_EN",
         "17": "ES_X", "18": "ES_Y", "19": "ES_Z", "20": "S_CS", "21": "S_SCLK", "22": "S_MOSI", "23": "S_MISO", "39": "VM_SENSE", "25": "LED", "37": "UART_TX", "36": "UART_RX"}),
 C("C37", "100n", 74, 34, "+3V3", "GND", 90), C("C38", "10u", 70, 34, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 R("R42", "10k", 76, 22, "+3V3", "EN", 90), C("C39", "1u", 76, 27, "EN", "GND", 90),
 button("SW2", "EN", 74, 40, "Reset (EN)"), button("SW3", "BOOT", 74, 46, "Boot (IO0)"),
 dict(ref="J1", sym="Connector:USB_C_Receptacle_USB2.0_16P", fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", value="USB-C", x=58, y=6, rot=180, lcsc="C165948", lcsc_status="verified", mpn="TYPE-C-31-M-12", nc=["A6", "A7", "A8", "B6", "B7", "B8"],
      nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2", "S1": "GND"}),
 R("R43", "5.1k", 56, 20, "CC1", "GND", 90), R("R44", "5.1k", 60, 20, "CC2", "GND", 90),
 LED("D6", "Green", 20, 38, "GND", "LED_A"), R("R45", "1k", 20, 43, "LED", "LED_A", 90),
 R("R46", "100k", 28, 28, "VM", "VM_SENSE", 90), R("R47", "10k", 28, 33, "VM_SENSE", "GND", 90), C("C40", "100n", 33, 33, "VM_SENSE", "GND", 90),
 jst("J7", 3, 74, 70, ["GND", "UART_TX", "UART_RX"], "Host UART (Pi/PC)"),
 dict(ref="J3", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="Vibration sensor SPI", x=74, y=58, rot=0, lcsc="C2894964", lcsc_status="verified", mpn="HCTL PZ254-2-03-Z-8.5", nets={"1": "+3V3", "2": "GND", "3": "S_SCLK", "4": "S_MOSI", "5": "S_MISO", "6": "S_CS"}),
 jst("J8", 3, 100, 54, ["+3V3", "ES_X_J", "GND"], "Endstop X"), jst("J9", 3, 100, 62, ["+3V3", "ES_Y_J", "GND"], "Endstop Y"), jst("J10", 3, 100, 70, ["+3V3", "ES_Z_J", "GND"], "Endstop Z"),
 R("R48", "1k", 90, 54, "ES_X_J", "ES_X", 90), C("C41", "100n", 85, 54, "ES_X", "GND", 90), R("R49", "1k", 90, 62, "ES_Y_J", "ES_Y", 90), C("C42", "100n", 85, 62, "ES_Y", "GND", 90), R("R50", "1k", 90, 70, "ES_Z_J", "ES_Z", 90), C("C43", "100n", 85, 70, "ES_Z", "GND", 90),
 TP("TP1", "VM", 6, 30), TP("TP2", "+5V", 6, 36), TP("TP3", "+3V3", 6, 42), TP("TP4", "GND", 6, 48)]
for k, ax in enumerate("XYZ"):
    x0 = 12 + 22 * k
    parts += [dict(ref=f"J{11 + 2 * k}", sym="Connector_Generic:Conn_01x08", fp="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", value=f"{ax} driver logic", x=x0, y=46, rot=0, lcsc="C22438158", lcsc_status="verified", mpn="hanxia HX PM2.54-1x8P",
                   nets={"1": f"{ax}_EN", "2": "+3V3", "3": "+3V3", "4": "+3V3", "5": f"{ax}_RS", "6": f"{ax}_RS", "7": f"{ax}_STEP", "8": f"{ax}_DIR"}),
              dict(ref=f"J{12 + 2 * k}", sym="Connector_Generic:Conn_01x08", fp="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", value=f"{ax} driver power/motor", x=x0 + 12.7, y=46, rot=0, lcsc="C22438158", lcsc_status="verified", mpn="hanxia HX PM2.54-1x8P",
                   nets={"1": "VM", "2": "GND", "3": f"M{ax}_2B", "4": f"M{ax}_2A", "5": f"M{ax}_1A", "6": f"M{ax}_1B", "7": "+3V3", "8": "GND"}),
              jst(f"J{20 + k}", 4, x0 + 6, 72, [f"M{ax}_1A", f"M{ax}_1B", f"M{ax}_2A", f"M{ax}_2B"], f"Motor {ax}"),
              R(f"R{51 + k}", "10k", x0 + 3, 42, "+3V3", f"{ax}_RS", 90)]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER IN: 24 V, TVS, reverse-polarity PMOS with 12 V gate clamp, bulk", ["J5", "D3", "Q5", "D4", "R40", "C30", "C31", "TP1", "TP4"]), ("5 V BUCK AP63205 + 3.3 V LDO", ["U2", "R41", "C32", "L1", "C33", "C34", "D5", "U3", "C35", "C36", "TP2", "TP3"]),
               ("CONTROLLER: ESP32-S3 (native USB, step/dir for 3 axes, SPI sensor)", ["U1", "C37", "C38", "R42", "C39", "SW2", "SW3", "D6", "R45", "R46", "R47", "C40"]), ("USB-C", ["J1", "R43", "R44"]),
               ("DRIVER SOCKETS (A4988 / DRV8825 / TMC2209 StepStick) + MOTOR OUTPUTS", [f"J{11 + 2 * k}" for k in range(3)] + [f"J{12 + 2 * k}" for k in range(3)] + [f"J{20 + k}" for k in range(3)] + [f"R{51 + k}" for k in range(3)]),
               ("ENDSTOPS, HOST UART, VIBRATION SENSOR", ["J7", "J3", "J8", "J9", "J10", "R48", "R49", "R50", "C41", "C42", "C43"])], big=("U1",))
S["notes"] = [("KINETIC: 24 V in (12-28 V), 5 V buck, 3.3 V LDO, ESP32-S3 runs the jerk-limited motion planner (kn_motion) and the vibration classifier (kn_vib). Three StepStick sockets; microstep pins MS1-3 are tied to 3.3 V (1/16 on A4988, 1/32 on DRV8825) and RESET/SLEEP are pulled up. Current limit is set on each driver module. Endstops are normally-closed to GND recommended.", 0, 0)]
PRE = [dict(net="BST", layer=0, pts=[(45.14, 11.05), (46.34, 11.05), (47.83, 11.05)], w=0.2), dict(net="SW", layer=0, pts=[(45.14, 12.0), (46.34, 12.0), (49.37, 12.0), (49.37, 11.05)], w=0.4)]
PREV = [("GND", 89.40, 27.36), ("GND", 89.40, 29.56), ("GND", 91.60, 27.36), ("GND", 91.60, 29.56)]
BOARD = dict(pre=PRE, pre_vias=PREV, clr=0.15, name="kinetic_ctl", title="KINETIC stepper / servo motion controller - main board", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"VIN24": "external 24 V supply", "VM": "24 V via reverse-polarity PMOS Q5", "+5V": "buck U2 or USB VBUS via D5", "+3V3": "LDO U3", "GND": "supply", "VBUS": "USB host"}, single_ok=("CC1", "CC2"),
 holes=[(3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, H - 3.5), (W - 14, H - 3.5)], ws=(0.2, 0.4), widths={"VBUS": 0.4, "VM": 0.4, "+5V": 0.4, "SW": 0.4, "MX_1A": 0.4, "MX_1B": 0.4, "MX_2A": 0.4, "MX_2B": 0.4, "MY_1A": 0.4, "MY_1B": 0.4, "MY_2A": 0.4, "MY_2B": 0.4, "MZ_1A": 0.4, "MZ_1B": 0.4, "MZ_2A": 0.4, "MZ_2B": 0.4, "VIN24": 0.4},
 first=["CC1", "CC2", "VBUS", "VIN24", "VM", "SW", "+5V"], edge_ok=("J1",), gnd_pour_only=True, silk=[("KINETIC rev A", 30, 76, 1.2), ("24V IN", 8, 4, 0.9), ("X", 14, 41, 0.9), ("Y", 36, 41, 0.9), ("Z", 58, 41, 0.9)], stitch=5.0)
BOARD["enc"] = dict(standoff=5.0, side=[("J5", "left", 6, 8, 6), ("J1", "top", 10, 8, 4)], lid=[])
