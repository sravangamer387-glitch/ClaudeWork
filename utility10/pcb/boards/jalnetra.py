"""Jal-Netra rev A: inline ultrasonic water meter / leak monitor main board (STM32G431, BTL piezo drive, 2-stage LNA, USB-C powered)."""
from .blocks import *
W, H = 86, 66
V3 = "+3V3"
parts = [
 dict(ref="U1", sym="MCU_ST_STM32G4:STM32G431C_6-8-B_Tx", fp="Package_QFP:LQFP-48_7x7mm_P0.5mm", value="STM32G431CBT6", x=48, y=36, rot=0, mpn="STM32G431CBT6", nc="rest", nets={
   "24": V3, "36": V3, "48": V3, "1": V3, "21": "AVDD", "20": "AVDD", "19": "GND", "23": "GND", "35": "GND", "47": "GND", "7": "NRST", "45": "BOOT0", "5": "XIN", "6": "XOUT", "37": "SWDIO", "38": "SWCLK",
   "14": "TXA1", "12": "TXA2", "16": "TXB1", "17": "TXB2", "8": "ADC_IN", "9": "MUX_SEL", "10": "GAIN_SEL", "13": "BUZ", "11": "LED", "18": "BTN", "39": "SCL", "44": "SDA", "22": "UART_TX", "25": "UART_RX"}),
 dict(ref="U4", sym="Analog_Switch:TS5A3159DCK", fp="Package_TO_SOT_SMD:SOT-363_SC-70-6", value="TS5A3159", x=22, y=36, rot=0, nets={"1": "RXA", "2": "GND", "3": "RXB", "4": "LNA_IN", "5": "AVDD", "6": "MUX_SEL"}),
 dict(ref="U5", sym="Amplifier_Operational:OPA356xxDBV", fp="Package_TO_SOT_SMD:SOT-23-5", value="OPA356", x=22, y=24, rot=0, nets={"1": "LNA1_OUT", "2": "GND", "3": "LNA1_P", "4": "LNA1_FB", "5": "AVDD"}),
 dict(ref="U6", sym="Amplifier_Operational:OPA356xxDBV", fp="Package_TO_SOT_SMD:SOT-23-5", value="OPA356", x=22, y=14, rot=0, nets={"1": "LNA2_OUT", "2": "GND", "3": "LNA2_P", "4": "LNA2_FB", "5": "AVDD"}),
 dict(ref="U7", sym="Analog_Switch:TS5A3159DCK", fp="Package_TO_SOT_SMD:SOT-363_SC-70-6", value="TS5A3159", x=34, y=14, rot=0, nets={"1": "LNA1_OUT", "2": "GND", "3": "LNA2_OUT", "4": "ADC_PRE", "5": "AVDD", "6": "GAIN_SEL"}),
 dict(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=70, y=22, rot=0, nc=["4"], nets={"1": "+5V", "2": "GND", "3": "+5V", "5": V3}),
 dict(ref="FB1", sym="Device:FerriteBead", fp="Inductor_SMD:L_0603_1608Metric", value="BLM18 600R", x=36, y=26, rot=90, nets={"1": V3, "2": "AVDD"}),
 dict(ref="Y1", sym="Device:Crystal_GND24", fp="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", value="8 MHz", x=32, y=33, rot=0, nets={"1": "XIN", "2": "GND", "3": "XOUT", "4": "GND"}),
 dict(ref="D5", sym="Diode:BAV99", fp="Package_TO_SOT_SMD:SOT-23", value="BAV99", x=14, y=44, rot=0, nets={"1": "GND", "2": "RXA", "3": V3}),
 dict(ref="D6", sym="Diode:BAV99", fp="Package_TO_SOT_SMD:SOT-23", value="BAV99", x=14, y=52, rot=0, nets={"1": "GND", "2": "RXB", "3": V3}),
 jst("J6", 2, 5, 40, ["TA1", "TA2"], "Transducer A (BTL)", 90), jst("J7", 2, 5, 52, ["TB1", "TB2"], "Transducer B (BTL)", 90),
 R("R30", "22", 30, 56, "TXA1", "TA1"), R("R31", "22", 30, 59, "TXA2", "TA2"), R("R32", "22", 38, 56, "TXB1", "TB1"), R("R33", "22", 38, 59, "TXB2", "TB2"),
 C("C20", "10n", 10, 36, "TA1", "RXA_C", 0), R("R35", "1k", 13, 38, "RXA_C", "RXA", 0), C("C21", "10n", 10, 46, "TB1", "RXB_C", 0), R("R36", "1k", 13, 48, "RXB_C", "RXB", 0),
 C("C22", "100n", 26, 36, "AVDD", "GND", 90), C("C23", "100n", 26, 20, "AVDD", "GND", 90), C("C24", "100n", 30, 14, "AVDD", "GND", 90), C("C25", "1u", 42, 31, "AVDD", "GND", 90),
 R("R10", "10k", 8, 21, "AVDD", "VMID", 90), R("R11", "10k", 8, 25, "VMID", "GND", 90), C("C27", "1u", 11, 25, "VMID", "GND", 90),
 C("C28", "10n", 26, 31, "LNA_IN", "LNA1_C", 0), R("R12", "100k", 28, 28, "LNA1_C", "VMID", 90), R("R13", "2.2k", 16, 27, "LNA1_OUT", "LNA1_FB"), R("R14", "240", 16, 30, "LNA1_FB", "LNA1_G"), C("C29", "1u", 19, 31, "LNA1_G", "VMID", 0),
 R("R15", "0", 26, 33, "LNA1_C", "LNA1_P", 0, lcsc=None),
 C("C30", "10n", 28, 17, "LNA1_OUT", "LNA2_C", 0), R("R16", "100k", 30, 20, "LNA2_C", "VMID", 90), R("R17", "1k", 15, 9, "LNA2_OUT", "LNA2_FB"), R("R18", "100", 18, 9, "LNA2_FB", "LNA2_G"), C("C31", "1u", 21, 9, "LNA2_G", "VMID", 0), R("R19", "0", 26, 14, "LNA2_C", "LNA2_P", 90, lcsc=None),
 R("R20", "33", 38, 18, "ADC_PRE", "ADC_IN"), C("C32", "22p", 41, 18, "ADC_IN", "GND", 90, lcsc=None),
 C("C1", "100n", 40.5, 43.5, V3, "GND", 90), C("C2", "100n", 55.5, 43.5, V3, "GND", 90), C("C3", "100n", 55.5, 28.5, V3, "GND", 90), C("C4", "100n", 48, 46.5, V3, "GND", 0), C("C33", "100n", 38, 44, "AVDD", "GND", 90), C("C34", "4.7u", 44, 28, V3, "GND", 90),
 C("C35", "15p", 32, 29, "XIN", "GND", 90, lcsc=None), C("C36", "15p", 32, 37.5, "XOUT", "GND", 90, lcsc=None), R("R21", "10k", 58, 46, "BOOT0", "GND", 90), R("R22", "10k", 40.5, 28.5, V3, "NRST", 90), C("C37", "100n", 40.5, 24, "NRST", "GND", 90),
 C("C38", "1u", 74, 26, V3, "GND", 90), C("C39", "1u", 66, 22, "+5V", "GND", 90),
 jst("J4", 4, 80, 26, ["GND", V3, "SCL", "SDA"], "OLED I2C", 90), R("R23", "4.7k", 72, 31, V3, "SCL", 90), R("R24", "4.7k", 75, 31, V3, "SDA", 90),
 jst("J5", 4, 80, 40, ["GND", V3, "UART_TX", "UART_RX"], "UART host / BLE", 90),
 dict(ref="J3", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="SWD", x=50, y=56, rot=0, nets={"1": V3, "2": "SWDIO", "3": "GND", "4": "SWCLK", "5": "GND", "6": "NRST"}),
 button("SW2", "BTN", 66, 36, "Test / zero"),
 TP("TP1", V3, 4, 8), TP("TP2", "GND", 4, 12), TP("TP3", "LNA1_OUT", 40, 8), TP("TP4", "LNA2_OUT", 44, 8), TP("TP5", "ADC_IN", 48, 8), TP("TP6", "RXA", 18, 60),
] + usb_c_power(58, 4.31)
parts += [dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer", x=60, y=56, rot=0, nets={"1": V3, "2": "BZ_N"}),
          dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=76, y=52, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
          dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=76, y=47, rot=0, lcsc="C2128", lcsc_status="verified", mpn="1N4148WS", nets={"1": V3, "2": "BZ_N"}),
          R("R7", "1k", 76, 57, "BUZ", "BUZ_B")] + led(V3, "LED", 40, 62, "Green")
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]

S = sch_layout([("USB-C 5 V INPUT + 3.3 V LDO + filtered analog supply", ["J1", "F1", "D3", "R2", "C5", "R1", "U3", "C38", "C39", "FB1", "C25", "TP1", "TP2"]), ("MCU: STM32G431CBT6 (170 MHz, 12-bit ADC 4 MSPS, 8 MHz crystal)", ["U1", "Y1", "C35", "C36", "C1", "C2", "C3", "C4", "C33", "C34", "R21", "R22", "C37"]),
               ("TRANSDUCER DRIVE: 22 ohm series, BTL from two timer pins, clamp + AC-coupled receive tap", ["J6", "J7", "R30", "R31", "R32", "R33", "C20", "R35", "C21", "R36", "D5", "D6"]),
               ("RECEIVE CHAIN: input mux, 2 x OPA356 (x10 each), gain-select mux, ADC anti-alias", ["U4", "U5", "U6", "U7", "C22", "C23", "C24", "R10", "R11", "C27", "C28", "R12", "R13", "R14", "C29", "R15", "C30", "R16", "R17", "R18", "C31", "R19", "R20", "C32", "TP3", "TP4", "TP5", "TP6"]),
               ("ALARM, LED, BUTTON", ["BZ1", "Q1", "D2", "R7", "D1", "R5", "SW2"]), ("OLED, UART, SWD", ["J4", "R23", "R24", "J5", "J3"])], big=("U1",), maxw=410)
S["notes"] = [("Measurement: STM32 TIM3 makes a 6-cycle 1 MHz burst on two pins (second inverted = bridge drive, 6.6 Vpp) into transducer A; transducer B receives through U4/LNA/U7 into ADC1 at 4 MS/s (64 samples DMA). Then roles swap. 1000 up/down pairs per measurement.", 20, 280), ("While receiving, one leg of the transducer is held low by its timer pin and the other is high-impedance and feeds the clamp + mux. LNA1 x10.2 (20 dB), LNA2 x10 (+20 dB), U7 selects 20 or 40 dB.", 20, 287), ("2-layer prototype. Production should use 4 layers (solid analog ground, guarded receive trace) - see docs.", 20, 294)]
S["no_auto"] = {"CC1", "CC2"}
S["no_flag"] = ("VBUS",)
BOARD = dict(clr=0.15, name="jal_netra", title="Jal-Netra ultrasonic flow main board", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S, single_ok=("BAT_P", "TXA1", "TXA2", "TXB1", "TXB2", "VBUS", "RXA_C", "RXB_C", "LNA1_G", "LNA2_G"),
 supply={"+5V": "USB via PTC", "VBUS": "USB", "+3V3": "LDO U3", "AVDD": "ferrite from 3V3", "GND": "USB", "VMID": "divider"}, holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, 2.5), (36, 63.5)],
 gnd_pour_only=True, widths={"VBUS": 0.4}, first=["CC1", "CC2", "VBUS", "+5V", "+3V3", "AVDD", "TXA1", "TXA2", "TXB1", "TXB2", "ADC_IN", "ADC_PRE", "LNA_IN", "LNA1_OUT", "LNA2_OUT", "RXA", "RXB"], edge_ok=("J1",),
 silk=[("JAL-NETRA rev A", 26, H - 1.7, 0.9), ("TX A", 3, 36, 0.8), ("TX B", 3, 48, 0.8)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 9.6, 3.8, 1.9), ("J6", "left", 9, 7, 3), ("J7", "left", 9, 7, 3), ("J4", "right", 11, 7, 3), ("J5", "right", 11, 7, 3)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("grille", "BZ1", 5, 1.2, 7)])
