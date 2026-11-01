"""Reusable, already-verified building blocks (relative placements taken from the Seeti/Rain layouts)."""
from .common import *
import math
def mcu(vcc, nets, x, y, ref="U1", nc="rest"):
    base = {"4": vcc, "6": vcc, "18": vcc, "3": "GND", "5": "GND", "21": "GND", "20": "AREF", "29": "RESET", "15": "MOSI", "16": "MISO", "17": "SCK"}
    base.update(nets)
    return [dict(ref=ref, sym="MCU_Microchip_ATmega:ATmega328P-A", fp="Package_QFP:TQFP-32_7x7mm_P0.8mm", value="ATmega328P-AU", x=x, y=y, rot=0, mpn="ATMEGA328P-AU", lcsc="C14877", lcsc_status="verified", nc=nc, nets=base),
            C("C1", "100n", x - 7.5, y + 7.5, vcc, "GND", 90), C("C2", "100n", x + 7.5, y + 7.5, vcc, "GND", 90), C("C3", "100n", x + 7.5, y - 7.5, "AREF", "GND", 90), R("R7", "10k", x - 7.5, y - 7.5, vcc, "RESET", 90)]
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
def sch_layout(groups, big=("U1",), paper="A3", cell=(36, 33), maxw=400, bighalf=None):
    for pp, (PW_, PH_) in ((("A3", (420, 297)), ("A2", (594, 420)), ("A1", (841, 594)))):
        S_ = _sch_layout(groups, big, pp, cell, PW_ - 24, bighalf)
        if all(b_["x"] + b_["w"] <= PW_ - 12 and b_["y"] + b_["h"] <= PH_ - 12 and not (b_["x"] + b_["w"] > PW_ - 120 and b_["y"] + b_["h"] > PH_ - 48) for b_ in S_["blocks"]): return S_
    return S_
def _extent(sym, unit):
    """screen-space extent (xmin, xmax, ymin, ymax) of a symbol's pins relative to its origin, plus pin-stub allowance"""
    from sexp import pins, resolve
    l, n = sym.split(":"); pn = pins(resolve(l, n)); xs = []; ys = []
    for num, (pu, qx, qy, qa, ln, pname, ptype) in pn.items():
        if pu not in (0, unit): continue
        xs.append(qx); ys.append(-qy)
    if not xs: return (-3, 3, -3, 3)
    return (min(xs), max(xs), min(ys), max(ys))
def _sch_layout(groups, big, paper, cell, maxw, bighalf):
    import inspect
    parts = {p["ref"]: p for p in inspect.stack()[2].frame.f_globals.get("parts", [])}
    def ext(r):
        base, u = (r.split("#")[0], int(r.split("#")[1])) if "#" in r else (r, 1)
        p = parts.get(base); e = _extent(p["sym"], u) if p else (-3, 3, -3, 3)
        return e
    MX, MY = 15.0, 13.0                                                     # room for pin stubs, rotated net labels, power symbols and the reference/value text
    place = {}; blocks = []; x = 20; y = 22; rowh = 0
    for title, refs in groups:
        bigs = [r for r in refs if r in big]; small = [r for r in refs if r not in big]
        inner = 0; rows = []; cur = []; curw = 0; BW = 4 * cell[0] + 16
        for r in small:
            e = ext(r); w = (e[1] - e[0]) + 2 * MX; h = (e[3] - e[2]) + 2 * MY
            w = max(w, 24.0)
            if cur and curw + w > BW - 10: rows.append(cur); cur = []; curw = 0
            cur.append((r, e, w, h)); curw += w
        if cur: rows.append(cur)
        ytop = 28.0; maxrowx = 0; rel = {}
        for row in rows:
            rh = max(c[3] for c in row); cx = 8.0
            for (r, e, w, h) in row:
                rel[r] = (cx + MX - e[0], ytop + MY - e[2]); cx += w
            maxrowx = max(maxrowx, cx); ytop += rh
        w_blk = max(BW if not bigs else 130, maxrowx + 8, len(title) * 2.3 + 10)
        if bigs:
            r = bigs[0]; e = ext(r); hw = (e[1] - e[0]) / 2; hh = (e[3] - e[2]) / 2
            by = ytop + (6 if rows else 0) + 14 + hh - (e[2] + e[3]) / 2 * 0
            rel[r] = (max(70, hw + 24 + MX) - (e[0] + e[1]) / 2, by - (e[2] + e[3]) / 2)
            w_blk = max(w_blk, 2 * (hw + 24 + MX)); h = by + hh + 22
        else: h = ytop + 12
        if x + w_blk > maxw: x = 20; y += rowh + 6; rowh = 0
        for r_, (rx_, ry_) in rel.items(): place[r_] = (x + rx_, y + ry_, 0)
        blocks.append(dict(title=title, x=x, y=y, w=w_blk, h=h))
        x += w_blk + 6; rowh = max(rowh, h)
    return dict(paper=paper, place=place, blocks=blocks, notes=[])
