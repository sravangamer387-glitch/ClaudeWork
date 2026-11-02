from .blocks import *
W, H = 110, 78
V = lambda **k: dict(k, lcsc_status="verified")
def RV(ref, val, x, y, n1, n2, lcsc, mpn, rot=90): return V(ref=ref, sym="Device:R", fp="Resistor_SMD:R_0603_1608Metric", value=val, x=x, y=y, rot=rot, lcsc=lcsc, mpn=mpn, nets={"1": n1, "2": n2})
MOS = lambda ref, x, y, g, d: V(ref=ref, sym="Device:Q_NMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3400A", x=x, y=y, rot=0, lcsc="C20917", mpn="AO3400A", nets={"1": g, "2": "GND", "3": d})
NPN = lambda ref, x, y, b, c: V(ref=ref, sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=x, y=y, rot=0, lcsc="C20526", mpn="MMBT3904", nets={"1": b, "2": "GND", "3": c})
SOCK6 = lambda ref, x, y, nets, val: V(ref=ref, sym="Connector_Generic:Conn_01x06", fp="Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical", value=val, x=x, y=y, rot=90, lcsc="C22438156", mpn="hanxia HX PM2.54-1x6P ZC-Y", nets={str(i + 1): n for i, n in enumerate(nets)})
SOCK8 = lambda ref, x, y, nets, val, nc: V(ref=ref, sym="Connector_Generic:Conn_01x08", fp="Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical", value=val, x=x, y=y, rot=0, lcsc="C22438158", mpn="hanxia HX PM2.54-1x8P ZC-Y", nets={str(i + 1): n for i, n in enumerate(nets) if n}, nc=nc)
LADDER = [("1k", "C21190", "UNI-ROYAL 0603WAF1001T5E"), ("2.2k", "C4190", "UNI-ROYAL 0603WAF2201T5E"), ("3.9k", "C23018", "UNI-ROYAL 0603WAF3901T5E"), ("6.8k", "C23212", "UNI-ROYAL 0603WAF6801T5E"),
          ("12k", "C22790", "UNI-ROYAL 0603WAF1202T5E"), ("22k", "C31850", "UNI-ROYAL 0603WAF2202T5E"), ("47k", "C25819", "UNI-ROYAL 0603WAF4702T5E")]
SEG = ["A", "B", "C", "D", "E", "F", "G", "DP"]; QPIN = {"A": "15", "B": "1", "C": "2", "D": "3", "E": "4", "F": "5", "G": "6", "DP": "7"}
parts = (mcu("+4V5", {"30": "RXD", "31": "TXD", "32": "MP3_BUSY", "1": "PWM_R", "9": "PWM_G", "10": "PWM_B", "13": "BUZ", "14": "MOTOR", "23": "DIG0", "24": "DIG1", "25": "DIG2", "26": "DIG3",
                     "27": "LED_PLAY", "28": "LED_SLEEP", "19": "BTN_ADC", "22": "VBAT_ADC", "2": "TEST"}, 56, 40) + isp("+4V5", 60, 70) + batt_input("+4V5", 10, 70, "BATT 3xAA") + buzzer("+4V5", "BUZ", 90, 46) +
         led("+4V5", "LED_PLAY", 40, 30, "Green", "D1", "R5") + led("+4V5", "LED_SLEEP", 40, 34, "Amber", "D4", "R8") + [
    # MP3 player module socket (DFPlayer Mini pinout): left row VCC RX TX DAC_R DAC_L SPK1 GND SPK2, right row BUSY USB- USB+ ADKEY2 ADKEY1 IO2 GND IO1 (top to bottom)
    SOCK8("J8", 10, 10, ["+4V5", "MP3_RX", "MP3_TX", None, None, "SPK1", "GND", "SPK2"], "MP3 module left row (VCC RX TX DACR DACL SPK1 GND SPK2)", ["4", "5"]),
    SOCK8("J9", 30.32, 10, ["MP3_BUSY", None, None, None, None, None, "GND", None], "MP3 module right row (BUSY .. GND IO1)", ["2", "3", "4", "5", "6", "8"]),
    R("R10", "1k", 38, 12, "TXD", "MP3_RX", 90), R("R11", "1k", 38, 16, "MP3_TX", "RXD", 90), C("C21", "100n", 38, 22, "+4V5", "GND", 90),
    V(ref="C20", sym="Device:C_Polarized", fp="Capacitor_SMD:CP_Elec_6.3x7.7", value="100u/35V", x=24, y=36, rot=0, lcsc="C176683", mpn="Lelon VZH101M1VTR-0607", nets={"1": "+4V5", "2": "GND"}),
    jst("J10", 2, 12, 34, ["SPK1", "SPK2"], "Speaker 3 W 4-8 ohm"),
    # 4-digit 0.56 in common-cathode display (5641AS type) plugged into two 1x6 sockets; top row = display pins 12..7, bottom row = pins 1..6
    SOCK6("J11", 64, 8, ["DK1", "SEG_A", "SEG_F", "DK2", "DK3", "SEG_B"], "Display top row (pins 12 11 10 9 8 7)"),
    SOCK6("J12", 64, 23.24, ["SEG_E", "SEG_D", "SEG_DP", "SEG_C", "SEG_G", "DK4"], "Display bottom row (pins 1 2 3 4 5 6)"),
    dict(ref="U4", sym="74xx:74HC595", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="74HC595", x=84, y=34, rot=0,
         nets=dict({QPIN[s]: "Q" + s for s in SEG}, **{"8": "GND", "16": "+4V5", "10": "+4V5", "13": "GND", "14": "MOSI", "11": "SCK", "12": "MISO", "9": "QH1"})),
    C("C23", "100n", 90, 28, "+4V5", "GND", 90),
    # second 74HC595 daisy-chained from U4 QH': seven ball-lane LEDs for the cricket game (shift 16 bits: lane byte first, then segments)
    dict(ref="U5", sym="74xx:74HC595", fp="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm", value="74HC595", x=100, y=32, rot=0,
         nets=dict({QPIN[s_]: f"LANE{i}" for i, s_ in enumerate(SEG[:7])}, **{"8": "GND", "16": "+4V5", "10": "+4V5", "13": "GND", "14": "QH1", "11": "SCK", "12": "MISO"}), nc=["7", "9"]),
    C("C25", "100n", 106, 32, "+4V5", "GND", 90)] +
    [R(f"R{60 + i}", "1k", 68 + 5 * i, 70.5, f"LANE{i}", f"LANE{i}_A", 90) for i in range(7)] +
    [dict(ref=f"D{10 + i}", sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value="Red", x=68 + 5 * i, y=74, rot=0, nets={"1": "GND", "2": f"LANE{i}_A"}) for i in range(7)] +
    [RV(f"R{20 + i}", "220", 58 + 3 * i, 29, "Q" + s, "SEG_" + s, "C22962", "UNI-ROYAL 0603WAF2200T5E") for i, s in enumerate(SEG)] +
    [NPN(f"Q{5 + k}", 68 + 6 * k, 56, f"DIG{k}_B", f"DK{k + 1}") for k in range(4)] + [R(f"R{28 + k}", "1k", 68 + 6 * k, 60, f"DIG{k}", f"DIG{k}_B", 90) for k in range(4)] +
    # seven buttons on one ADC input (resistor ladder, 10 k pull-up): single presses are decoded in the HAL
    [button(f"SW{2 + k}", f"BTN{k}_N", 10 + 8 * k, 62, f"Button {k + 1}") for k in range(7)] +
    [RV(f"R{40 + k}", v, 10 + 8 * k, 66, "BTN_ADC", f"BTN{k}_N", c, m) for k, (v, c, m) in enumerate(LADDER)] +
    [R("R47", "10k", 48, 52, "+4V5", "BTN_ADC", 90), C("C24", "100n", 51, 52, "BTN_ADC", "GND", 90),
     # LED channels (star lamp) and projector motor: low-side AO3400A, gate 100 R, pull-down 100 k
     MOS("Q9", 8, 44, "R_G", "R_K"), MOS("Q10", 16, 44, "G_G", "G_K"), MOS("Q11", 24, 44, "B_G", "B_K"), MOS("Q12", 32, 44, "M_G", "MOT_N"),
     R("R50", "100", 8, 48, "PWM_R", "R_G", 90), R("R51", "100", 16, 48, "PWM_G", "G_G", 90), R("R52", "100", 24, 48, "PWM_B", "B_G", 90), R("R53", "100", 32, 48, "MOTOR", "M_G", 90),
     R("R54", "100k", 11, 48, "R_G", "GND", 90), R("R55", "100k", 19, 48, "G_G", "GND", 90), R("R56", "100k", 27, 48, "B_G", "GND", 90), R("R57", "100k", 35, 48, "M_G", "GND", 90),
     jst("J13", 4, 10, 56, ["+4V5", "R_K", "G_K", "B_K"], "RGB LED (common anode) / lamp"), jst("J14", 2, 28, 56, ["+4V5", "MOT_N"], "Projector motor"),
     V(ref="D8", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=40, y=56, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "+4V5", "2": "MOT_N"}),
     R("R58", "100k", 42, 44, "+4V5", "VBAT_ADC", 90), R("R59", "100k", 45, 44, "VBAT_ADC", "GND", 90), C("C22", "100n", 42, 40, "VBAT_ADC", "GND", 90),
     TP("TP1", "+4V5", 104, 10), TP("TP2", "GND", 104, 14), TP("TP4", "TEST", 104, 18)])
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER: 3xAA, switch, reverse-polarity PMOS", ["J1", "SW1", "Q2", "C4", "TP1", "TP2"]), ("MCU: ATmega328P-AU, 8 MHz internal", ["U1", "C1", "C2", "C3", "R7", "J2", "TP4", "R58", "R59", "C22"]),
               ("MP3 MODULE (DFPlayer Mini type) + SPEAKER", ["J8", "J9", "R10", "R11", "C20", "C21", "J10"]), ("4-DIGIT DISPLAY: 74HC595 segments, NPN digit drivers", ["U4", "C23", "J11", "J12"] + [f"R{20 + i}" for i in range(8)] + [f"Q{5 + k}" for k in range(4)] + [f"R{28 + k}" for k in range(4)]),
               ("SEVEN BUTTONS ON ONE ADC (resistor ladder)", [f"SW{2 + k}" for k in range(7)] + [f"R{40 + k}" for k in range(7)] + ["R47", "C24"]),
               ("BALL LANE (cricket): second 74HC595 + 7 LEDs", ["U5", "C25"] + [f"R{60 + i}" for i in range(7)] + [f"D{10 + i}" for i in range(7)]), ("LAMP + MOTOR DRIVERS, BUZZER, LEDS", ["Q9", "Q10", "Q11", "Q12", "R50", "R51", "R52", "R53", "R54", "R55", "R56", "R57", "J13", "J14", "D8", "BZ1", "Q1", "D2", "R6", "D1", "R5", "D4", "R8"])], big=("U1",))
S["notes"] = [("AP1 shared audio platform (rhymes player, star lamp, cricket game). ATmega328P at 8 MHz internal from 3xAA. MP3 module: 1 k series on both UART lines, BUSY on D2. Seven buttons share ADC6 through a ladder (10 k pull-up; 1 k ... 47 k to each button): decode one press at a time in the HAL. Display: U4 74HC595 drives segments a..g, dp from QA..QH (matches seg_write bit0..7), digits through MMBT3904 low-side; U5 (chained from U4 QH') drives the seven ball-lane LEDs: shift the lane byte first, then the segment byte. SER/SRCLK/RCLK share MOSI/SCK/MISO with the ISP header. Lamp: three AO3400A on PWM D3/D5/D6 to a common-anode LED; motor on D10 with SS14 flyback. Arduino tone() uses Timer2, which also drives D3: do not use the buzzer and red PWM together. Populate per product (see the manual).", 0, 0)]
BOARD = dict(name="ap1_audio", title="AP1 shared audio platform (rhymes player, star lamp, cricket game)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"+4V5": "3xAA via Q2", "GND": "battery", "BAT_P": "battery", "BAT_SW": "battery switch"}, single_ok=(),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(46, H - 2.5), (104, 24)], widths={"+4V5": 0.4, "SPK1": 0.4, "SPK2": 0.4, "MOT_N": 0.4, "R_K": 0.4, "G_K": 0.4, "B_K": 0.4},
 first=["SPK1", "SPK2", "+4V5", "MOT_N", "BTN_ADC"], gnd_pour_only=True, silk=[("AP1 AUDIO PLATFORM rev A", 80, H - 1.7, 0.9), ("MP3", 18, 4.5, 0.7), ("DISPLAY", 70, 4.0, 0.7)], stitch=6.0)
BOARD["enc"] = dict(standoff=4.0, inner_height=22, side=[("SW1", "bottom", 8, 5, 2.5)], lid=[("grille", "BZ1", 5, 1.2, 7), ("abs_rect", 70.35, 15.6, 52, 20), ("abs_rect", 83, 74, 36, 5)] + [("round", f"SW{2 + k}", 5.0) for k in range(7)] + [("round", "D1", 2.2), ("round", "D4", 2.2)],
                    note="shared platform box: display window over the 4-digit display (cover with tinted acrylic), seven button plungers, speaker grille to add for the chosen speaker; 3 x AA bay with a screwed door")
