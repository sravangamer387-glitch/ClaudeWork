from .blocks import *
W, H = 44, 40
V = lambda **k: dict(k, lcsc_status="verified")
def RM(ref, val, x, y, n1, n2, rot=0, lcsc="C22935", mpn="UNI-ROYAL 0603WAF1004T5E"):
    return V(ref=ref, sym="Device:R", fp="Resistor_SMD:R_0603_1608Metric", value=val, x=x, y=y, rot=rot, lcsc=lcsc, mpn=mpn, nets={"1": n1, "2": n2})
R56 = lambda ref, x, y, n1, n2, rot=0: RM(ref, "5.6M", x, y, n1, n2, rot, "C2933237", "FOJAN FRC0603F5604TS")
R43 = lambda ref, x, y, n1, n2, rot=0: RM(ref, "4.3M", x, y, n1, n2, rot, "C136595", "FH RS-03L4304FT")
R1M = lambda ref, x, y, n1, n2, rot=0: RM(ref, "1M", x, y, n1, n2, rot)
parts = [
 V(ref="U1", sym="Battery_Management:BQ25570", fp="Package_DFN_QFN:QFN-20-1EP_3.5x3.5mm_P0.5mm_EP2x2mm", value="BQ25570RGRR", x=22, y=17, rot=0, lcsc="C506250", mpn="BQ25570RGRR",
   nets={"1": "GND", "2": "VIN_DC", "3": "GND", "4": "VREF_SAMP", "5": "GND", "6": "VSTOR", "7": "OV_N", "8": "VRDIV", "9": "GND", "10": "OKH_N", "11": "OKP_N", "12": "VSET_N", "13": "VBAT_OK", "14": "VOUT", "15": "GND", "16": "LBUCK", "17": "GND", "18": "VBAT", "19": "VSTOR", "20": "LBOOST", "21": "GND"}),
 V(ref="J1", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="MFC in (+ / -)", x=5, y=8, rot=0, lcsc="C131337", mpn="JST B2B-PH-K-S", nets={"1": "VIN_DC", "2": "GND"}),
 V(ref="J2", sym="Connector_Generic:Conn_01x02", fp="Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", value="Storage cell (+ / -), protected", x=33, y=5, rot=0, lcsc="C131337", mpn="JST B2B-PH-K-S", nets={"1": "VBAT", "2": "GND"}),
 V(ref="J3", sym="Connector_Generic:Conn_01x03", fp="Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical", value="Tag out (VOUT, GND, VBAT_OK)", x=37, y=33, rot=0, lcsc="C131339", mpn="JST B3B-PH-K-S", nets={"1": "VOUT", "2": "GND", "3": "VBAT_OK"}),
 V(ref="L1", sym="Device:L", fp="Inductor_SMD:L_Coilcraft_LPS4018", value="22u", x=11, y=14, rot=90, lcsc="C5278935", mpn="Coilcraft LPS4018-223MRC", nets={"1": "LBOOST", "2": "VIN_DC"}),
 V(ref="L2", sym="Device:L", fp="Inductor_SMD:L_Changjiang_FNR3015S", value="10u", x=34, y=14, rot=0, lcsc="C42427989", mpn="ZE ZENR3015T100M", nets={"1": "LBUCK", "2": "VOUT"}),
 C("C1", "4.7u", 14, 20, "VIN_DC", "GND", 90), C("C2", "100n", 20, 8, "VSTOR", "GND", 90), C("C3", "4.7u", 25, 8, "VSTOR", "GND", 90),
 V(ref="C4", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=29, y=9, rot=90, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "VBAT", "2": "GND"}),
 V(ref="C5", sym="Device:C", fp="Capacitor_SMD:C_0805_2012Metric", value="22u/10V", x=38, y=19, rot=90, lcsc="C29277", mpn="Samsung CL21A226MPQNNNE", nets={"1": "VOUT", "2": "GND"}),
 C("C6", "10n", 14, 26, "VREF_SAMP", "GND", 90),
 # --- high-impedance setting dividers (VRDIV on top, GND at the bottom); 13 resistors, all 1% 0603; chains run left to right: GND ... VRDIV
 R56("R3", 8, 30, "GND", "OV_N"), R1M("R2", 12, 30, "OV_N", "OV_A"), R56("R1", 16, 30, "OV_A", "VRDIV"),                                                                       # ROV1 = 5.6M (bottom), ROV2 = 1M + 5.6M (top)
 R43("R4", 8, 34, "GND", "OKP_N"), R56("R5", 12, 34, "OKP_N", "OK_A"), R1M("R6", 16, 34, "OK_A", "OK_B"), R1M("R7", 20, 34, "OK_B", "OK_C"), R1M("R8", 24, 34, "OK_C", "OKH_N"), R1M("R9", 28, 34, "OKH_N", "VRDIV"),   # ROK1 = 4.3M, ROK2 = 5.6M+1M+1M, ROK3 = 1M
 R43("R10", 21, 30, "GND", "VSET_N"), R56("R11", 25, 30, "VSET_N", "OUT_A"), R1M("R12", 29, 30, "OUT_A", "OUT_B"), R1M("R13", 33, 30, "OUT_B", "VRDIV"),                       # ROUT1 = 4.3M, ROUT2 = 5.6M+1M+1M
 TP("TP1", "VIN_DC", 5, 14), TP("TP2", "VSTOR", 30, 22), TP("TP3", "VOUT", 40, 26), TP("TP4", "GND", 9, 38)]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("INPUT + HARVESTER: BQ25570 boost charger, MPPT at 50 % of Voc (VOC_SAMP to GND), 22 uH boost inductor", ["U1", "J1", "L1", "C1", "C2", "C3", "C6", "TP1", "TP2"]), ("STORAGE + OUTPUT: protected cell, 10 uH buck, 3.3 V rail, VBAT_OK", ["J2", "C4", "L2", "C5", "J3", "TP3", "TP4"]),
               ("HIGH-IMPEDANCE SETTING DIVIDERS (no ground pour nearby): VBAT_OV, VBAT_OK / hysteresis, VOUT", [f"R{i}" for i in range(1, 14)])], big=("U1",))
S["notes"] = [("BioWatt: BQ25570 values per the TI datasheet (SLUSBH2G) equations. VBAT_OV = 1.5 * VBIAS * (1 + ROV2/ROV1) with VBIAS = 1.21 V: ROV1 = 5.6 M, ROV2 = 5.6 M + 1 M gives 3.95 V (cell charged to about 3.95 V). VBAT_OK = VBIAS * (1 + ROK2/ROK1): ROK1 = 4.3 M, ROK2 = 5.6 M + 1 M + 1 M gives 3.35 V falling; VBAT_OK_HYST = VBIAS * (1 + (ROK2 + ROK3)/ROK1) with ROK3 = 1 M gives 3.63 V rising. VOUT = VBIAS * (1 + ROUT2/ROUT1): ROUT1 = 4.3 M, ROUT2 = 5.6 M + 1 M + 1 M gives 3.35 V. Each divider sum is at most 13 M as the datasheet recommends. Use a PROTECTED single Li-ion/LiPo cell. Clean flux residue thoroughly: the dividers are megohm-level.", 0, 0)]
PRE = [
    dict(net="OV_N", layer=0, pts=[(8.825, 30), (11.175, 30)], w=0.2),
    dict(net="OV_A", layer=0, pts=[(12.825, 30), (15.175, 30)], w=0.2),
    dict(net="OKP_N", layer=0, pts=[(8.825, 34), (11.175, 34)], w=0.2),
    dict(net="OK_A", layer=0, pts=[(12.825, 34), (15.175, 34)], w=0.2),
    dict(net="OK_B", layer=0, pts=[(16.825, 34), (19.175, 34)], w=0.2),
    dict(net="OK_C", layer=0, pts=[(20.825, 34), (23.175, 34)], w=0.2),
    dict(net="OKH_N", layer=0, pts=[(24.825, 34), (27.175, 34)], w=0.2),
    dict(net="VSET_N", layer=0, pts=[(21.825, 30), (24.175, 30)], w=0.2),
    dict(net="OUT_A", layer=0, pts=[(25.825, 30), (28.175, 30)], w=0.2),
    dict(net="OUT_B", layer=0, pts=[(29.825, 30), (32.175, 30)], w=0.2),
    dict(net="VRDIV", layer=0, pts=[(16.825, 30), (16.825, 32), (33.825, 32), (33.825, 30)], w=0.2),
    dict(net="VRDIV", layer=0, pts=[(28.825, 34), (28.825, 32)], w=0.2)]
PRE += [dict(net="GND", layer=0, pts=[(22.5, 18.688), (22.5, 17.6)], w=0.2), dict(net="GND", layer=0, pts=[(22.5, 15.312), (22.5, 16.4)], w=0.2)]
PRE += [dict(net="OV_N", layer=0, pts=[(21.5, 18.688), (21.5, 19.7)], w=0.2, goal=False),
        dict(net="VRDIV", layer=0, pts=[(22.0, 18.688), (22.0, 19.2), (22.9, 20.1), (22.9, 21.2)], w=0.2),
        dict(net="OKH_N", layer=0, pts=[(23.0, 18.688), (23.0, 19.0), (24.2, 19.0), (24.2, 20.3)], w=0.2, goal=False),
        dict(net="OKP_N", layer=0, pts=[(23.688, 18.0), (25.3, 18.0), (25.3, 19.8)], w=0.2, goal=False)]
PRE += [dict(net="VREF_SAMP", layer=0, pts=[(20.312, 17.5), (19.2, 17.5), (18.4, 18.3), (18.4, 26.775), (14.55, 26.775)], w=0.2)]
PRE += [dict(net="GND", layer=0, pts=[(7.175, 30), (5.0, 30)], w=0.3), dict(net="GND", layer=0, pts=[(7.175, 34), (5.0, 34)], w=0.3),
        dict(net="GND", layer=0, pts=[(14.0, 25.225), (15.8, 25.225), (15.8, 22.5)], w=0.3), dict(net="GND", layer=0, pts=[(20.175, 30), (20.175, 26.0)], w=0.3)]
PRE += [dict(net="VRDIV", layer=1, pts=[(22.9, 21.4), (22.9, 26.0), (22.0, 27.0), (22.0, 32.0)], w=0.2)]
PRE += [dict(net="OV_N", layer=1, pts=[(21.5, 19.9), (20.6, 20.8), (20.6, 25.5), (10.0, 26.0 + 0.0), (10.0, 30.0)], w=0.2),
        dict(net="OKH_N", layer=1, pts=[(24.2, 20.5), (24.2, 27.0), (26.0, 29.0), (26.0, 34.0)], w=0.2),
        dict(net="OKP_N", layer=1, pts=[(25.3, 19.8), (27.0, 21.5), (27.0, 28.0), (28.5, 31.0), (30.0, 36.0), (10.0, 36.0), (10.0, 34.0)], w=0.2)]
PREV = [("OV_N", 21.5, 19.9), ("VRDIV", 22.9, 21.4), ("OKH_N", 24.2, 20.5), ("OKP_N", 25.3, 19.8), ("GND", 21.4, 16.6), ("GND", 22.6, 17.4), ("GND", 21.4, 17.4), ("GND", 22.6, 16.6), ("OV_N", 10, 30), ("OKP_N", 10, 34), ("OKH_N", 26, 34), ("VRDIV", 22, 32)]
BOARD = dict(pre=PRE, pre_vias=PREV, clr=0.15, name="biowatt", title="BioWatt MFC energy harvester (BQ25570)", rev="A", size=(W, H), corner=2.0, parts=parts, sch=S,
 supply={"GND": "storage cell and MFC return", "VIN_DC": "microbial fuel cell", "VBAT": "storage cell", "VSTOR": "boost charger output", "VOUT": "buck output", "VRDIV": "bias for dividers"}, single_ok=("VBAT_OK", "LBOOST", "LBUCK"),
 holes=[(3.5, H - 3.5), (W - 3.5, 3.5)], fids=[(3.5, 20), (W - 3.5, 22)], first=["VIN_DC", "LBOOST", "VSTOR", "VBAT", "LBUCK", "VOUT", "VRDIV"], gnd_pour_only=False, pour_keepout=[(6.0, 27.5, 35.0, 37.0), (11.5, 23.5, 17.0, 28.5)],
 silk=[("BioWatt rev A", 22, 38.5, 0.9), ("MFC +/-", 5, 3.2, 0.7)], stitch=6.0)
BOARD["enc"] = dict(standoff=3.0, side=[], lid=[])
