"""Part helpers with LCSC numbers. LCSC status: 'verified' = number confirmed by a web search on 2026-10-31/11-01; 'memory' = my recollection, MUST be checked on lcsc.com before ordering."""
LCSC = {  # value/footprint key -> (lcsc, status, mpn)
 "ATmega328P-AU": ("C14877", "verified", "ATMEGA328P-AU"), "MCP6001": ("C116490", "verified", "MCP6001T-I/OT"), "MMBT3904": ("C20526", "verified", "MMBT3904 (JSCJ)"),
 "1N4148WS": ("C2128", "verified", "1N4148WS (JSCJ)"), "AO3401A": ("C15127", "verified", "AO3401A (AOS)"), "USB-C": ("C165948", "verified", "TYPE-C-31-M-12 (Korean Hroparts)"),
 "100n": ("C14663", "verified", "0603 100nF X7R"), "1u": ("C15849", "verified", "0603 1uF X7R"), "10u": ("C15850", "verified", "0805 10uF X5R"), "10n": ("C57112", "verified", "0603 10nF X7R"),
 "1k": ("C21190", "verified", "0603 1k 1%"), "2.2k": ("C4190", "verified", "0603 2.2k 1%"), "5.1k": ("C23186", "verified", "0603 5.1k 1%"), "10k": ("C25804", "verified", "0603 10k 1%"), "100k": ("C25803", "verified", "0603 100k 1%"), "4.7k": ("C23162", "verified", "0603 4.7k 1%"),
}
def _l(d, key):
    if key in LCSC: d["lcsc"], d["lcsc_status"], d["mpn"] = LCSC[key]
    return d
def R(ref, val, x, y, n1, n2, rot=0, fp="Resistor_SMD:R_0603_1608Metric", **kw): return _l(dict(ref=ref, sym="Device:R", fp=fp, value=val, x=x, y=y, rot=rot, nets={"1": n1, "2": n2}, **kw), val)
def C(ref, val, x, y, n1, n2, rot=0, fp="Capacitor_SMD:C_0603_1608Metric", **kw): return _l(dict(ref=ref, sym="Device:C", fp=fp, value=val, x=x, y=y, rot=rot, nets={"1": n1, "2": n2}, **kw), val)
def LED(ref, val, x, y, k, a, rot=0, **kw): return dict(ref=ref, sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value=val, x=x, y=y, rot=rot, nets={"1": k, "2": a}, **kw)
def TP(ref, net, x, y): return dict(ref=ref, sym="Connector:TestPoint", fp="TestPoint:TestPoint_Pad_D1.5mm", value="TP", x=x, y=y, rot=0, nets={"1": net}, tp=True)
def grid(refs, x0, y0, cols=4, dx=32, dy=34, rot=0):
    return {r: (x0 + (i % cols) * dx, y0 + (i // cols) * dy, rot) for i, r in enumerate(refs)}
