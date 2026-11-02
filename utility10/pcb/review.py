"""Design-review checks beyond DRC/ERC, for every released board: part identity vs LCSC data, stock, capacitor voltage margins, LED currents,
IC decoupling distance, pull-ups, input protection. usage: python3 review.py [board...]  -> costing/REVIEW_<board>.json and prints findings."""
import sys, os, re, json, glob, importlib, math
sys.path.insert(0, ".")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CACHE = json.load(open(os.path.join(ROOT, "costing", "prices_lcsc.json")))
DETAIL = os.path.join(ROOT, "costing", "lcsc_detail.json")
detail = json.load(open(DETAIL)) if os.path.exists(DETAIL) else {}
import subprocess, time
def get_detail(c):
    if c in detail: return detail[c]
    out = subprocess.run(["curl", "-s", "-m", "30", f"https://wmsc.lcsc.com/ftps/wm/product/detail?productCode={c}"], capture_output=True, text=True).stdout
    try:
        r = json.loads(out)["result"]
        detail[c] = dict(model=r.get("productModel"), intro=r.get("productIntroEn"), desc=r.get("productDescEn"), pkg=r.get("encapStandard"), cycle=r.get("productCycle"), stock=r.get("stockNumber"),
                         params={p.get("paramNameEn"): p.get("paramValueEn") for p in (r.get("paramVOList") or [])}, brand=r.get("brandNameEn"))
    except Exception as e: detail[c] = dict(error=str(e)[:60])
    time.sleep(0.2); return detail[c]
def num(v):
    m = re.match(r"^\s*([\d.]+)\s*([pnuµmkMG]?)", v or "")
    if not m: return None
    return float(m.group(1)) * dict(p=1e-12, n=1e-9, u=1e-6, **{"µ": 1e-6}, m=1e-3, k=1e3, M=1e6, G=1e9).get(m.group(2), 1)
def rail_v(n):
    n = n.upper()
    for pat, v in ((r"24V", 24), (r"12V", 12), (r"\+?5V|VBUS|VUSB", 5), (r"3V3|\+3\.3", 3.3), (r"VBAT|VSTOR", 4.2), (r"VCC_CHG|SOLAR", 6.5), (r"VOUT", 3.35)):
        if re.search(pat, n): return v
    return None
LEDV = {"red": 2.0, "green": 2.1, "amber": 2.1, "yellow": 2.1, "blue": 3.0, "white": 3.0}
def review(mod):
    B = importlib.import_module("boards." + mod).BOARD
    import lcsc_fill; lcsc_fill.fill(B["parts"])
    parts = {p["ref"]: p for p in B["parts"]}; F = []   # (severity, check, text)
    nets = {}
    for ref, p in parts.items():
        for pin, n in (p.get("nets") or {}).items(): nets.setdefault(n, []).append((ref, pin))
    # R1/R2 identity, stock
    for ref, p in parts.items():
        c = p.get("lcsc")
        if not c: continue
        d = get_detail(c)
        if d.get("error"): F.append(("warn", "lcsc-lookup", f"{ref} {c}: no data ({d['error']})")); continue
        fp = (p.get("fp") or "").upper(); pk = (d.get("pkg") or "").upper().replace("-", "").replace("DO214AA", "SMB").replace("DO214AC", "SMA").replace("DO214AB", "SMC").replace("SOT25", "SOT23").replace("SMD3535", "3535")
        tok = re.search(r"(0201|0402|0603|0805|1206|1210|1812|SOT\d+|SOIC\d*|SOP\d*|SMA|SMB|SMC|QFN|LGA|SOD\d+|TO\d+|DFN|HSOP|SSOP|TSSOP|DIP|PLCC4|3535|5050)", fp.replace("_", "").replace("-", ""))
        if tok and p.get("fp", "").split(":")[0] in ("Resistor_SMD", "Capacitor_SMD", "LED_SMD", "Diode_SMD", "Inductor_SMD") and tok.group(1) not in pk and tok.group(1) != "SMA":
            F.append(("warn", "package", f"{ref} {c}: footprint {p['fp']} vs LCSC package {d.get('pkg')}"))
        if (d.get("stock") or 0) == 0: F.append(("error", "stock", f"{ref} {c} {p.get('value')}: out of stock at LCSC"))
        elif (d.get("stock") or 0) < 500: F.append(("warn", "stock", f"{ref} {c} {p.get('value')}: low stock {d.get('stock')}"))
        if d.get("cycle") not in (None, "normal"): F.append(("warn", "lifecycle", f"{ref} {c}: LCSC status {d.get('cycle')}"))
        ref0 = ref.rstrip("0123456789"); v = p.get("value") or ""; vn = num(v.split("/")[0])
        txt = ((d.get("intro") or "") + " " + (d.get("desc") or "") + " " + json.dumps(d.get("params") or {})).replace("Ω", "ohm").replace("μ", "u").replace("µ", "u")
        if ref0 in ("R", "C", "L") and vn:
            want = vn; found = [num(m) for m in re.findall(r"([\d.]+\s*[pnuµmkMG]?)(?:F|ohm|H|Ω)", txt)]
            if found and not any(f and abs(math.log10(f / want)) < 0.02 for f in found if f): F.append(("error", "value", f"{ref} {c}: value {v} not found in LCSC description ({(d.get('intro') or '')[:60]})"))
        # R3 capacitor voltage
        if ref0 == "C":
            m = re.search(r"([\d.]+)\s*V", txt); vr = float(m.group(1)) if m else None
            volts = [rail_v(n) for n in (p["nets"] or {}).values() if rail_v(n)]
            if vr and volts and max(volts) * 1.5 > vr: F.append(("warn", "cap-voltage", f"{ref} {c}: rated {vr} V on a {max(volts)} V net (derate 50 %)"))
    # R4 decoupling distance (uses placement in spec x,y)
    for ref, p in parts.items():
        if not ref.startswith("U"): continue
        for pin, n in (p.get("nets") or {}).items():
            if rail_v(n) and n.upper() not in ("GND",) and not re.search(r"VBAT_|VBUS", n.upper()):
                caps = [q for q in parts.values() if q["ref"].startswith("C") and n in (q.get("nets") or {}).values() and "GND" in (q.get("nets") or {}).values()]
                if not caps: F.append(("warn", "decoupling", f"{ref}: supply net {n} has no capacitor to GND on the board")); break
                near = min(math.hypot(q["x"] - p["x"], q["y"] - p["y"]) for q in caps)
                lim = 25 if ref == "U1" and "ESP32" in (p.get("value") or "") else 16
                if near > lim: F.append(("info", "decoupling", f"{ref}: nearest {n} capacitor is {near:.0f} mm from the part centre"))
                break
    # R6 LED current
    for ref, p in parts.items():
        if p.get("sym") != "Device:LED": continue
        col = next((k for k in LEDV if k in (p.get("value") or "").lower()), None); vf = LEDV.get(col, 2.1)
        an = [n for pin, n in p["nets"].items() if n != "GND"]
        for n in an:
            rs = [q for q in parts.values() if q["ref"].startswith("R") and n in q["nets"].values()]
            for r in rs:
                other = [x for x in r["nets"].values() if x != n]; rv = num(r["value"]); sv = rail_v(other[0]) if other else None
                if sv is None and other and other[0] in nets:   # a GPIO drive net: assume 3.3 V
                    sv = 3.3
                if sv and rv:
                    i = (sv - vf) / rv * 1000
                    if i < 0.3: F.append(("warn", "led-current", f"{ref} ({col}): about {i:.2f} mA at {sv} V through {r['ref']} {r['value']}: very dim"))
                    elif i > 15: F.append(("warn", "led-current", f"{ref}: about {i:.1f} mA, above the 0603 rating margin"))
    # R7 pull-ups
    for sig in ("SDA", "SCL"):
        if sig in nets and len(nets[sig]) >= 2 and not any(q["ref"].startswith("R") for q in parts.values() if sig in (q.get("nets") or {}).values()):
            F.append(("warn", "i2c-pullup", f"{sig} has no pull-up resistor on the board"))
    if any("ESP32" in (p.get("value") or "") for p in parts.values()):
        if not any(q["ref"].startswith("R") and "EN" in q["nets"].values() for q in parts.values()): F.append(("error", "esp32-en", "EN has no pull-up resistor"))
        if not any(q["ref"].startswith("C") and "EN" in q["nets"].values() for q in parts.values()): F.append(("warn", "esp32-en", "EN has no capacitor (reset delay)"))
    # R8 single-pin nets
    for n, pins in nets.items():
        if len(pins) == 1 and n not in tuple(B.get("single_ok", ())) and not n.startswith("unconnected"): F.append(("info", "single-pin-net", f"net {n} has one pin: {pins[0][0]}.{pins[0][1]}"))
    return F
if __name__ == "__main__":
    mods = sys.argv[1:] or [os.path.basename(p) for p in sorted(glob.glob(os.path.join(HERE, "release", "*"))) if os.path.isdir(p)]
    allr = {}
    for m in mods:
        try: F = review(m)
        except Exception as e: F = [("error", "review-crash", repr(e)[:120])]
        allr[m] = F; print(f"== {m}: {sum(1 for f in F if f[0] == 'error')} errors, {sum(1 for f in F if f[0] == 'warn')} warnings, {sum(1 for f in F if f[0] == 'info')} info")
        for f in F: print("   ", f[0].upper(), f[1], "-", f[2])
    json.dump(detail, open(DETAIL, "w"), indent=1); json.dump(allr, open(os.path.join(ROOT, "costing", "REVIEW_findings.json"), "w"), indent=1)
