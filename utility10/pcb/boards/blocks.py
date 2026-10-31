"""Reusable, already-verified building blocks (relative placements taken from the Seeti/Rain layouts)."""
from .common import *
import math
def mcu(vcc, nets, x, y, ref="U1", nc="rest"):
    base = {"4": vcc, "6": vcc, "18": vcc, "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK"}
    base.update(nets)
    return [dict(ref=ref, sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=x, y=y, rot=0, mpn="ATMEGA328P-AU", lcsc="C14877", lcsc_status="verified", nc=nc, nets=base),
            C("C1", "100n", x - 10, y - 3, vcc, "GND", 90), C("C2", "100n", x + 8, y + 4, vcc, "GND", 90), C("C3", "100n", x + 8, y - 4, "AREF", "GND", 90), R("R7", "10k", x - 7, y - 15, vcc, "RESET")]
def isp(vcc, x, y, rot=0): return [dict(ref="J2", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="ISP", x=x, y=y, rot=rot, nets={"1": "MISO", "2": vcc, "3": "SCK", "4": "MOSI", "5": "RESET", "6": "GND"})]
def batt_input(vcc, x, y, label="BATT"):
    """JST battery connector, slide switch, reverse-polarity PMOS (drain = battery side) -> vcc"""
    return [dict(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value=label, x=x, y=y, rot=0, nets={"1": "BAT_P", "2": "GND"}),
            dict(ref="SW1", sym="Switch:SW_SPDT", fp="Button_Switch_SMD:SW_SPDT_PCM12", value="Power", x=x + 11, y=y + 1, rot=0, nc=["3"], nets={"1": "BAT_SW", "2": "BAT_P"}),
            dict(ref="Q2", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=x + 19, y=y + 0.5, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "GND", "2": vcc, "3": "BAT_SW"}),
            C("C4", "10u", x + 24, y - 0.5, vcc, "GND", 0, "Capacitor_SMD:C_0805_2012Metric")]
def buzzer(vcc, drive_net, x, y):
    """buzzer BZ1, NPN driver Q1, flyback D2, base resistor R6; (x, y) = buzzer pin 1"""
    return [dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_12x9.5RM7.6", value="Buzzer", x=x, y=y, rot=0, nets={"1": vcc, "2": "BZ_N"}),
            dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=x + 5.5, y=y + 15, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "BUZ_B", "2": "GND", "3": "BZ_N"}),
            dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=x + 12.5, y=y + 17, rot=0, lcsc="C2128", lcsc_status="verified", mpn="1N4148WS", nets={"1": vcc, "2": "BZ_N"}),
            R("R6", "1k", x + 0.5, y + 17, drive_net, "BUZ_B")]
def led(vcc_unused, net, x, y, color="Green", ref="D1", rref="R5"):
    return [dict(ref=ref, sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value=color, x=x + 4, y=y, rot=0, nets={"1": "GND", "2": ref + "_A"}), R(rref, "1k", x, y, net, ref + "_A")]
def button(ref, net, x, y, value="Button"): return dict(ref=ref, sym="Switch:SW_Push", fp="Button_Switch_SMD:SW_SPST_B3U-1000P", value=value, x=x, y=y, rot=0, nets={"1": net, "2": "GND"})
def usb_c_power(x, y):
    """USB-C power-only input with CC resistors, PTC and TVS -> +5V (relative to the connector origin)"""
    return [dict(ref="J1", sym="Connector:USB_C_Receptacle_USB2.0_16P", fp="Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", value="USB-C 5V", x=x, y=y, rot=180, lcsc="C165948", lcsc_status="verified", mpn="TYPE-C-31-M-12", nc=["A6", "A7", "A8", "B6", "B7", "B8"],
                 nets={"A1": "GND", "B12": "GND", "A12": "GND", "B1": "GND", "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS", "A5": "CC1", "B5": "CC2", "S1": "GND"}),
            dict(ref="F1", sym="Device:Polyfuse", fp="Fuse:Fuse_1206_3216Metric", value="PTC 500mA", x=x + 10, y=y + 2.7, rot=0, nets={"1": "VBUS", "2": "+5V"}),
            dict(ref="D3", sym="Device:D_TVS", fp="Diode_SMD:D_SMA", value="SMAJ5.0A", x=x + 15, y=y + 6.7, rot=0, nets={"1": "VBUS", "2": "GND"}),
            R("R1", "5.1k", x - 6, y + 9.7, "CC1", "GND", 90), R("R2", "5.1k", x + 6, y + 9.7, "CC2", "GND", 90), C("C5", "10u", x + 9.5, y + 7.2, "+5V", "GND", 0, "Capacitor_SMD:C_0805_2012Metric")]
def jst(ref, n, x, y, nets, value, rot=0):
    sym = {2: "Conn_01x02", 3: "Conn_01x03", 4: "Conn_01x04", 5: "Conn_01x05", 6: "Conn_01x06"}[n]
    return dict(ref=ref, sym=f"Connector_Generic:{sym}", fp=f"Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical", value=value, x=x, y=y, rot=rot, nets={str(i + 1): v for i, v in enumerate(nets)})
def sch_layout(groups, big=("U1",), paper="A3", cell=(36, 33), maxw=400):
    """auto schematic layout: groups = [(title, [refs])]; returns S dict (place + blocks)"""
    place = {}; blocks = []; x = 20; y = 22; rowh = 0
    for title, refs in groups:
        isbig = any(r in big for r in refs)
        cols = 1 if isbig and len(refs) == 1 else 4
        n = len(refs); rows = math.ceil(n / cols); w = cols * cell[0] + 8 if not isbig else 130; h = rows * cell[1] + 16 if not isbig else 170
        if x + w > maxw: x = 20; y += rowh + 6; rowh = 0
        blocks.append(dict(title=title, x=x, y=y, w=w, h=h))
        for i, r in enumerate(refs):
            if isbig and r in big: place[r] = (x + 70, y + 95, 0)
            else: place[r] = (x + 22 + (i % cols) * cell[0], y + 24 + (i // cols) * cell[1], 0)
        x += w + 6; rowh = max(rowh, h)
    return dict(paper=paper, place=place, blocks=blocks, notes=[])
