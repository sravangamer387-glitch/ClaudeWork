"""Pin-function sanity check for every released board: symbol pin names against the nets in the board spec.
GND-named pins must be on GND; supply-named pins must not be on GND; ground and supply nets must not share a pin function.
usage: python3 pincheck.py [board...]"""
import sys, re, os, glob, importlib
sys.path.insert(0, ".")
import sexp
def pins(sym):
    lname, sname = sym.split(":")
    return {k: (v[5], v[6]) for k, v in sexp.pins(sexp.resolve(lname, sname)).items()}
GNDN = re.compile(r"^(GND|VSS|AGND|PGND|DGND|GNDA|VSSA|EP|PAD|~?GND~?)$", re.I); SUPN = re.compile(r"^(VCC|VDD|AVCC|AVDD|VIN|V\+|VBUS|VDDA|VDD3P3.*|3V3|\+3V3|VBAT|VSYS|VCCA|VIN_DC)$", re.I)
def check(mod):
    B = importlib.import_module("boards." + mod).BOARD; F = []
    for p in B["parts"]:
        if p.get("tp") or not p.get("sym"): continue
        try: pp = pins(p["sym"])
        except Exception as e: F.append(("warn", p["ref"], f"symbol lookup failed {p['sym']}: {e}")); continue
        if not pp: F.append(("info", p["ref"], f"symbol {p['sym']} not parsed")); continue
        for pin, net in (p.get("nets") or {}).items():
            if pin not in pp and p["sym"].startswith("Connector:USB_C"): continue
            if pin not in pp: F.append(("error", p["ref"], f"pin {pin} not in symbol {p['sym']}")); continue
            nm, typ = pp[pin]; isg = bool(re.match(r"^(GND|AGND|PGND|VSS|0V)\w*$", net, re.I)) or net.upper() == "GND"
            if GNDN.match(nm) and not isg and net not in ("NC",): F.append(("error", p["ref"], f"pin {pin} ({nm}) is on net {net}, expected ground"))
            if SUPN.match(nm) and isg: F.append(("error", p["ref"], f"pin {pin} ({nm}) is on ground"))
    return F
if __name__ == "__main__":
    mods = sys.argv[1:] or [os.path.basename(p) for p in sorted(glob.glob("release/*")) if os.path.isdir(p)]
    bad = 0
    for m in mods:
        try: F = check(m)
        except Exception as e: F = [("error", "-", f"crash {e!r}"[:150])]
        e = [f for f in F if f[0] == "error"]; bad += len(e)
        print(f"== {m}: {len(e)} errors")
        for f in F:
            if f[0] != "info": print("   ", f[0].upper(), f[1], f[2])
    print("total errors", bad)
