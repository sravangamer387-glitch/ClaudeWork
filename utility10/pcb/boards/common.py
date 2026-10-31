def R(ref, val, x, y, n1, n2, rot=0, fp="Resistor_SMD:R_0603_1608Metric"): return dict(ref=ref, sym="Device:R", fp=fp, value=val, x=x, y=y, rot=rot, nets={"1": n1, "2": n2})
def C(ref, val, x, y, n1, n2, rot=0, fp="Capacitor_SMD:C_0603_1608Metric"): return dict(ref=ref, sym="Device:C", fp=fp, value=val, x=x, y=y, rot=rot, nets={"1": n1, "2": n2})
def LED(ref, val, x, y, k, a, rot=0): return dict(ref=ref, sym="Device:LED", fp="LED_SMD:LED_0603_1608Metric", value=val, x=x, y=y, rot=rot, nets={"1": k, "2": a})
