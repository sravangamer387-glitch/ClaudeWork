"""TRISHNA reagentless urinal hydration / biomarker monitor - main controller board (carrier for an ESP32-DevKitC-32E).
12 V in -> PTC -> TVS -> reverse-polarity PMOS -> VM; AP63203 buck -> +3V3 (digital) -> ferrite -> +3V3A (op-amps).
Loads: DRV8871 H-bridge for the reversible 12 V peristaltic pump (forward = sample, reverse = backwash), AO3400A + M7 (1N4007) flyback for the 12 V
fresh-water solenoid. Sensors: bipolar ratiometric EC cell (GPIO-driven, 330 R reference), two photodiode TIAs (MCP6002) for 450 nm absorbance and
850 nm transmission / 90-degree scatter, LED drivers from 12 V, DS18B20 1-Wire, sump stream-detect and chamber-B leak probes, VL53L1X ToF presence (I2C),
microSD (SPI) frame log, UART telemetry header."""
from .blocks import *
W, H = 120, 84
V = lambda **k: dict(k, lcsc_status="verified")
NMOS = lambda ref, x, y, g, d: V(ref=ref, sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=x, y=y, rot=0, lcsc="C20917", mpn="AO3400A", nets={"1": g, "2": "GND", "3": d})
R1206 = lambda ref, val, x, y, a, b, rot=0: V(ref=ref, sym="Device:R", fp="Resistor_SMD:R_1206_3216Metric", value=val + " 1/4W", x=x, y=y, rot=rot, lcsc="C4410", mpn="UNI-ROYAL 1206W4F1001T5E", nets={"1": a, "2": b})
SOCK19 = lambda ref, x, nets, nc, val: V(ref=ref, sym="Connector_Generic:Conn_01x19", fp="Connector_PinSocket_2.54mm:PinSocket_1x19_P2.54mm_Vertical", value=val, x=x, y=DK_Y, rot=0,
                                          lcsc="C319202", mpn="BOOMELE 2.54-1*19P female header", nets=nets, nc=nc)
DK_X, DK_Y = 62.0, 22.0                     # ESP32-DevKitC left socket pin 1 (antenna end up); right socket 25.4 mm to the right
parts = [
 # ---------------- power input and protection ----------------
 V(ref="J1", sym="Connector:Barrel_Jack", fp="Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal", value="12 V DC in (2 A)", x=8, y=14, rot=0, lcsc="C22434582", mpn="CUI/Same Sky PJ-063AH", nets={"1": "VIN12", "2": "GND"}),
 V(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1812_4532Metric", value="PTC 2A 16V", x=20, y=5, rot=0, lcsc="C46641167", mpn="R+O SMD1812-200-16 (2 A hold)", nets={"1": "VIN12", "2": "VIN_F"}),
 V(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMB", value="SMBJ15A", x=20, y=12, rot=0, lcsc="C83846", mpn="Littelfuse SMBJ15A", nets={"1": "VIN_F", "2": "GND"}),
 V(ref="Q5", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=26, y=16, rot=0, lcsc="C15127", mpn="AO3401A", nets={"1": "GATE", "2": "VM", "3": "VIN_F"}),
 V(ref="D4", sym="Device:D_Zener", fp="Diode_SMD:D_SOD-123", value="BZT52C12", x=26, y=22, rot=0, lcsc="C124196", mpn="DIODES BZT52C12-7-F", nets={"1": "VM", "2": "GATE"}),
 R("R40", "10k", 32, 22, "GATE", "GND", 90),
 V(ref="C30", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=34, y=6, rot=0, lcsc="C176683", mpn="Lelon VZH101M1VTR-0607", nets={"1": "VM", "2": "GND"}),
 V(ref="C31", sym="Device:C", fp="Capacitor_SMD:C_1210_3225Metric", value="10u/50V", x=42, y=6, rot=0, lcsc="C380537", mpn="Samsung CL32A106KBJNNNE", nets={"1": "VM", "2": "GND"}),
 # ---------------- 3.3 V buck (AP63203, fixed 3.3 V, 2 A) + analog rail ----------------
 V(ref="U2", sym="Regulator_Switching:AP63205WU", fp="Package_TO_SOT_SMD:TSOT-23-6", value="AP63203WU-7", x=46, y=14, rot=0, lcsc="C780769", mpn="AP63203WU-7 (3.3 V fixed)", nets={"1": "+3V3", "2": "EN_B", "3": "VM", "4": "GND", "5": "SW", "6": "BST"}),
 R("R41", "100k", 41, 19, "VM", "EN_B", 90), C("C32", "100n", 50.6, 13.05, "BST", "SW", 0),
 V(ref="L1", sym="Device:L", fp="Inductor_SMD:L_Changjiang_FNR5040S", value="4.7u", x=46, y=28, rot=90, lcsc="C167963", mpn="Changjiang FNR5040S4R7MT", nets={"1": "SW", "2": "+3V3"}),
 V(ref="C33", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=53, y=30, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+3V3", "2": "GND"}),
 V(ref="C34", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=53, y=35, rot=0, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "+3V3", "2": "GND"}),
 V(ref="FB1", sym="Device:FerriteBead", fp="Inductor_SMD:L_0603_1608Metric", value="BLM18 600R", x=96, y=10, rot=0, lcsc="C19330", mpn="Murata BLM18AG601SN1D", nets={"1": "+3V3", "2": "+3V3A"}),
 C("C36", "10u", 100, 14, "+3V3A", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C37", "100n", 103, 14, "+3V3A", "GND", 90),
 LED("D6", "Green", 40, 34, "GND", "LED_A"), R("R45", "1k", 40, 38, "+3V3", "LED_A", 90),
 R("R60", "100k", 56, 52, "VM", "VIN_ADC", 90), R("R61", "10k", 56, 57, "VIN_ADC", "GND", 90), C("C60", "100n", 56, 62, "VIN_ADC", "GND", 90),
 TP("TP1", "VM", 4, 30), TP("TP2", "+3V3", 4, 36), TP("TP3", "+3V3A", 110, 6), TP("TP4", "GND", 4, 42),
 # ---------------- ESP32-DevKitC-32E carrier (two 1x19 sockets, 25.4 mm apart) ----------------
 SOCK19("J4", DK_X, {"1": "DK3V3", "3": "EC_ADC", "4": "OPT_TX_ADC", "5": "OPT_SC_ADC", "6": "VIN_ADC", "7": "SUMP_ADC", "8": "LEAK_ADC", "9": "EC_DRV_A", "10": "EC_DRV_B",
                        "11": "LVL_DRV", "12": "LED_BLU", "13": "PUMP_IN2", "14": "GND", "15": "PUMP_IN1"}, ["2", "16", "17", "18", "19"], "DevKitC left: 3V3 EN 36 39 34 35 32 33 25 26 27 14 12 GND 13 D2 D3 CMD 5V"),
 SOCK19("J5", DK_X + 25.4, {"1": "GND", "2": "SD_MOSI", "3": "SCL", "6": "SDA", "7": "GND", "8": "SD_MISO", "9": "SD_SCK", "10": "SD_CS", "11": "TLM_TX", "12": "TLM_RX",
                             "13": "ONEWIRE", "15": "VALVE", "16": "LED_IR"}, ["4", "5", "14", "17", "18", "19"], "DevKitC right: GND 23 22 TX RX 21 GND 19 18 5 17 16 4 0 2 15 D1 D0 CLK"),
 V(ref="JP1", sym="Connector_Generic:Conn_01x02", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", value="3V3 link (remove for USB-only power)", x=56, y=20, rot=0,
   lcsc="C492401", mpn="XFCN PZ254V-11-02P + jumper", nets={"1": "+3V3", "2": "DK3V3"}),
 C("C38", "10u", 56, 28, "DK3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C39", "100n", 56, 33, "DK3V3", "GND", 90),
 # ---------------- reversible peristaltic pump: DRV8871 H-bridge (ILIM 47k -> about 1.4 A trip) ----------------
 V(ref="U3", sym="Driver_Motor:DRV8871DDA", fp="Package_SO:HTSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.4x3.2mm", value="DRV8871DDAR", x=30, y=56, rot=0,
   lcsc="C75864", mpn="TI DRV8871DDAR", nets={"1": "GND", "2": "PUMP_IN2", "3": "PUMP_IN1", "4": "ILIM", "5": "VM", "6": "PUMP_O1", "7": "GND", "8": "PUMP_O2", "9": "GND"}),
 R("R62", "47k", 24.0, 60.0, "ILIM", "GND", 180),
 V(ref="C41", sym="Device:C", fp="Capacitor_SMD:C_1210_3225Metric", value="10u/50V", x=38, y=50, rot=0, lcsc="C380537", mpn="Samsung CL32A106KBJNNNE", nets={"1": "VM", "2": "GND"}),
 C("C42", "100n", 38, 55, "VM", "GND", 90),
 V(ref="C40", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=20, y=46, rot=0, lcsc="C176683", mpn="Lelon VZH101M1VTR-0607", nets={"1": "VM", "2": "GND"}),
 jst("J6", 2, 6, 58, ["PUMP_O1", "PUMP_O2"], "Peristaltic pump 12 V (red = PUMP_O1)"),
 # ---------------- fresh-water solenoid: AO3400A low side + M7 (1N4007) flyback ----------------
 NMOS("Q1", 22, 70, "VALVE_GR", "VALVE_D"), R("R63", "100", 28, 67, "VALVE", "VALVE_GR", 90), R("R64", "100k", 28, 72, "VALVE_GR", "GND", 90),
 V(ref="D10", sym="Device:D", fp="Diode_SMD:D_SMA", value="M7 (1N4007)", x=16, y=64, rot=0, lcsc="C95872", mpn="MDD M7 (1N4007, 1 A 1000 V)", nets={"1": "VM", "2": "VALVE_D"}),
 jst("J7", 2, 6, 68, ["VM", "VALVE_D"], "Solenoid valve 12 V NC"),
 # ---------------- optics: LED drivers (12 V, 1 k / 1206) and two photodiode TIAs ----------------
 NMOS("Q2", 100, 32, "LEDB_GR", "LEDB_K"), R("R65", "100", 94, 30, "LED_BLU", "LEDB_GR", 90), R("R66", "100k", 94, 35, "LEDB_GR", "GND", 90), R1206("R67", "1k", 104, 26, "VM", "LEDB_A", 0),
 NMOS("Q3", 100, 42, "LEDI_GR", "LEDI_K"), R("R68", "100", 94, 40, "LED_IR", "LEDI_GR", 90), R("R69", "100k", 94, 45, "LEDI_GR", "GND", 90), R1206("R70", "1k", 104, 38, "VM", "LEDI_A", 0),
 jst("J8", 4, 108, 48, ["LEDB_A", "LEDB_K", "LEDI_A", "LEDI_K"], "Sensor-block LEDs (450 nm blue, 850 nm IR)"),
 V(ref="U4", sym="Amplifier_Operational:MCP6002-xSN", fp="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", value="MCP6002T-I/SN", x=104, y=62, rot=0, lcsc="C7377", mpn="Microchip MCP6002T-I/SN",
   nets={"1": "TX_OUT", "2": "PD_TX", "3": "GND", "4": "GND", "5": "GND", "6": "PD_SC", "7": "SC_OUT", "8": "+3V3A"}),
 R("R71", "10k", 96, 58, "PD_TX", "TX_OUT", 90), C("C61", "10n", 99, 58, "PD_TX", "TX_OUT", 90),
 R("R72", "1M", 96, 66, "PD_SC", "SC_OUT", 90), C("C62", "1n", 99, 66, "PD_SC", "SC_OUT", 90),
 R("R73", "1k", 110, 56, "TX_OUT", "OPT_TX_ADC", 90), C("C63", "10n", 113, 56, "OPT_TX_ADC", "GND", 90),
 R("R74", "1k", 110, 68, "SC_OUT", "OPT_SC_ADC", 90), C("C64", "10n", 113, 68, "OPT_SC_ADC", "GND", 90), C("C65", "100n", 104, 56.5, "+3V3A", "GND", 0),
 jst("J9", 3, 106, 76, ["PD_TX", "PD_SC", "GND"], "Photodiodes BPW34: transmission, 90-degree scatter (anodes to GND)"),
 # ---------------- EC cell: bipolar ratiometric drive from GPIO25/26, 330 R reference ----------------
 R("R75", "330", 70, 44, "EC_DRV_A", "EC_N1", 0), R("R76", "100", 70, 48, "EC_E2", "EC_DRV_B", 0), R("R77", "100", 74, 40, "EC_N1", "EC_ADC", 90), C("C66", "1n", 77, 40, "EC_ADC", "GND", 90),   # under the DevKit, next to GPIO25/26/36
 jst("J10", 2, 86, 78, ["EC_N1", "EC_E2"], "EC electrodes (titanium pins E1, E2)"),
 # ---------------- sump stream detect + chamber-B leak probe (pulsed from GPIO27) ----------------
 R("R78", "4.7k", 76, 74, "LVL_DRV", "SUMP_P", 90), R("R79", "1k", 79, 74, "SUMP_P", "SUMP_ADC", 90), C("C67", "1n", 82, 74, "SUMP_ADC", "GND", 90),
 jst("J11", 2, 76, 78, ["SUMP_P", "GND"], "Sump stream-detect probe"),
 R("R80", "47k", 64, 74, "LVL_DRV", "LEAK_P", 90), R("R81", "1k", 67, 74, "LEAK_P", "LEAK_ADC", 90), C("C68", "1n", 70, 74, "LEAK_ADC", "GND", 90),
 jst("J12", 2, 64, 78, ["LEAK_P", "GND"], "Chamber-B floor leak probe"),
 # ---------------- digital sensors and links ----------------
 jst("J13", 3, 108, 18, ["+3V3", "ONEWIRE", "GND"], "DS18B20 temperature probe"), R("R82", "4.7k", 100, 20, "+3V3", "ONEWIRE", 90),
 jst("J14", 4, 44, 78, ["+3V3", "SDA", "SCL", "GND"], "VL53L1X ToF presence sensor (I2C)"), R("R83", "4.7k", 46, 72, "+3V3", "SDA", 90), R("R84", "4.7k", 49, 72, "+3V3", "SCL", 90),
 jst("J15", 3, 34, 78, ["GND", "TLM_TX", "TLM_RX"], "Telemetry UART (ESP32 TX out, RX in) to USB-serial"),
 V(ref="J16", sym="Connector:Micro_SD_Card_Det2", fp="Connector_Card:microSD_HC_Molex_104031-0811", value="microSD (SPI log)", x=48, y=60, rot=0, lcsc="C585350", mpn="Molex 104031-0811",
   nets={"1": "SD_DAT2", "2": "SD_CS", "3": "SD_MOSI", "4": "+3V3", "5": "SD_SCK", "6": "GND", "7": "SD_MISO", "8": "SD_DAT1", "11": "GND"}, nc=["9", "10"]),
 R("R86", "10k", 40, 46, "+3V3", "SD_DAT2", 90), R("R87", "10k", 43, 46, "+3V3", "SD_DAT1", 90), R("R88", "10k", 46, 46, "+3V3", "SD_CS", 90), R("R89", "10k", 49, 46, "+3V3", "SD_MISO", 90),
 C("C69", "10u", 40, 56, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"), C("C70", "100n", 40, 61, "+3V3", "GND", 90),
]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER IN: 12 V, 2 A PTC, TVS, reverse-polarity PMOS, bulk", ["J1", "F1", "D3", "Q5", "D4", "R40", "C30", "C31", "TP1", "TP4"]),
                ("3.3 V BUCK AP63203 + ANALOG RAIL (ferrite) + VIN MONITOR", ["U2", "R41", "C32", "L1", "C33", "C34", "FB1", "C36", "C37", "D6", "R45", "TP2", "TP3", "R60", "R61", "C60"]),
                ("ESP32-DevKitC-32E CARRIER (2 x 1x19 sockets) + 3V3 LINK", ["J4", "J5", "JP1", "C38", "C39"]),
                ("PUMP H-BRIDGE DRV8871 (forward sample / reverse backwash)", ["U3", "R62", "C40", "C41", "C42", "J6"]),
                ("SOLENOID DRIVER AO3400A + 1N4007 FLYBACK", ["Q1", "R63", "R64", "D10", "J7"]),
                ("OPTICS: LED DRIVERS + PHOTODIODE TIAs (MCP6002)", ["Q2", "R65", "R66", "R67", "Q3", "R68", "R69", "R70", "J8", "U4", "R71", "C61", "R72", "C62", "R73", "C63", "R74", "C64", "C65", "J9"]),
                ("EC CELL (bipolar ratiometric), SUMP + LEAK PROBES", ["R75", "R76", "R77", "C66", "J10", "R78", "R79", "C67", "J11", "R80", "R81", "C68", "J12"]),
                ("TEMP, ToF, TELEMETRY UART, microSD (SPI)", ["J13", "R82", "J14", "R83", "R84", "J15", "J16", "R86", "R87", "R88", "R89", "C69", "C70"])], big=())
S["notes"] = [("TRISHNA controller. 12 V adapter (2 A) -> PTC -> TVS -> PMOS -> VM. AP63203 makes +3V3; FB1 + 10u/100n make +3V3A for the TIAs. Fit JP1 for normal 12 V operation; REMOVE JP1 before plugging USB into the DevKit. "
               "Pump: DRV8871 IN1/IN2 = GPIO13/GPIO12 (IN1 high = forward/sample, IN2 high = reverse/backwash; both low = coast). Valve: GPIO2 -> AO3400A, M7 flyback across the coil. "
               "EC: GPIO25 -> 330 R -> E1 ... E2 -> 100 R -> GPIO26; alternate polarity every 250 us, sample EC_N1 in each phase: (Rc + Rb) / (Rref + Ra) = V_A / V_B, independent of the 3.3 V level; both pins low when idle (no DC on the electrodes). "
               "Optics: LEDs from 12 V through 1 k (about 9-10 mA); TIA gains 10 k (transmission) and 1 M (scatter): tune so clear water reads 1.5-2.5 V. Sump/leak probes are pulsed from GPIO27 only while sampled.", 0, 0)]
PRE = [dict(net="BST", layer=0, pts=[(47.14, 13.05), (48.34, 13.05), (49.83, 13.05)], w=0.2), dict(net="SW", layer=0, pts=[(47.14, 14.0), (48.34, 14.0), (51.37, 14.0), (51.37, 13.05)], w=0.4),
       dict(net="EN_B", layer=0, pts=[(41.0, 18.18), (41.0, 17.2), (43.4, 14.8), (43.9, 14.0), (44.86, 14.0)], w=0.2),          # buck EN: R41 -> U2.2, fixed so VM/SW cannot wall it in
       dict(net="VM", layer=0, pts=[(44.86, 14.95), (44.86, 16.6), (42.8, 18.66), (42.8, 19.82), (41.0, 19.82)], w=0.4),       # buck VIN: U2.3 -> R41.1
       dict(net="ILIM", layer=0, pts=[(27.12, 57.91), (26.0, 57.91), (24.82, 59.09), (24.82, 60.0)], w=0.2)]                # DRV8871 ILIM -> R62
BOARD = dict(pre=PRE, clr=0.15, name="trishna_ctrl", title="TRISHNA urinal hydration monitor - controller (ESP32-DevKitC carrier)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"VIN12": "external 12 V adapter", "VM": "12 V via reverse-polarity PMOS Q5", "+3V3": "buck U2", "+3V3A": "+3V3 via ferrite FB1", "DK3V3": "+3V3 via JP1", "GND": "supply", "VIN_F": "12 V after PTC"},
 single_ok=("SD_DAT1", "SD_DAT2"), ws=(0.2, 0.4),
 widths={"VM": 0.4, "+3V3": 0.4, "SW": 0.4, "VIN12": 0.4, "VIN_F": 0.4, "PUMP_O1": 0.4, "PUMP_O2": 0.4, "VALVE_D": 0.4, "DK3V3": 0.4},
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(24, 39), (116, 30)], first=["VIN12", "VIN_F", "VM", "SW", "+3V3", "PUMP_O1", "PUMP_O2"], gnd_pour_only=True,
 pour_keepout=[(DK_X - 4, 0.6, DK_X + 29.4, DK_Y - 3)],   # no copper under the DevKit's PCB antenna (it overhangs the sockets toward the top edge)
 silk=[("TRISHNA controller rev A", 96, 82.2, 1.0), ("12V IN 2A", 10, 3.2, 0.9), ("PUMP", 8, 54, 0.8), ("VALVE", 8, 64.5, 0.8), ("USB END", DK_X + 12.7, 70.5, 0.8), ("ANTENNA END", DK_X + 12.7, DK_Y - 4.5, 0.8)], stitch=5.0)
# no generated enclosure: TRISHNA has its own split-chamber enclosure in trishna/mechanical (chamber A holds this PCB on 4 x 6 mm standoffs)
