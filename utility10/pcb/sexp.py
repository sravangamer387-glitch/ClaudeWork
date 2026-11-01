"""Minimal KiCad s-expression reader/writer and symbol-library access."""
import re, os, uuid
class Q(str):
    """quoted string atom"""
def parse(text):
    toks = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()"]+', text); pos = 0
    def rd():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == "(":
            lst = []
            while toks[pos] != ")": lst.append(rd())
            pos += 1; return lst
        if t.startswith('"'): return Q(t[1:-1].replace('\\"', '"').replace("\\\\", "\\"))
        return t
    return rd()
def dump(x, indent=0):
    if isinstance(x, list):
        return "(" + " ".join(dump(i) for i in x) + ")"
    if isinstance(x, Q): return '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return str(x)
SYMDIR = "/usr/share/kicad/symbols"; FPDIR = "/usr/share/kicad/footprints"
_libs = {}
def lib(name):
    if name not in _libs:
        _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "symbols", name + ".kicad_sym")
        _libs[name] = parse(open(_p if os.path.exists(_p) else os.path.join(SYMDIR, name + ".kicad_sym")).read())
    return _libs[name]
def symbol(libname, name):
    for e in lib(libname):
        if isinstance(e, list) and e and e[0] == "symbol" and e[1] == name: return e
    raise KeyError(f"{libname}:{name}")
def resolve(libname, name):
    """follow (extends ...) so derived symbols get the parent's graphics and pins"""
    s = symbol(libname, name)
    for e in s[2:]:
        if isinstance(e, list) and e and e[0] == "extends":
            parent = symbol(libname, e[1]); merged = [x for x in parent]
            merged[1] = Q(name)
            for sub in merged:
                if isinstance(sub, list) and sub and sub[0] == "symbol" and sub[1].startswith(parent[1] + "_"):
                    sub[1] = Q(name + sub[1][len(parent[1]):])
            props = {p[1]: p for p in s[2:] if isinstance(p, list) and p and p[0] == "property"}
            merged = [x for x in merged if not (isinstance(x, list) and x and x[0] == "property" and x[1] in props)] + list(props.values())
            return merged
    return s
def pins(sym):
    """returns {number: (unit, x, y, angle, length, name, type)}"""
    out = {}
    def walk(node, unit):
        for e in node[2:]:
            if isinstance(e, list) and e:
                if e[0] == "symbol":
                    m = re.match(r".*_(\d+)_(\d+)$", e[1]); walk(e, int(m.group(1)) if m else unit)
                elif e[0] == "pin":
                    at = next(i for i in e if isinstance(i, list) and i[0] == "at"); ln = next(i for i in e if isinstance(i, list) and i[0] == "length")
                    nm = next(i for i in e if isinstance(i, list) and i[0] == "name")[1]; num = next(i for i in e if isinstance(i, list) and i[0] == "number")[1]
                    out[str(num)] = (unit, float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0, float(ln[1]), str(nm), e[1])
    walk(sym, 0); return out
def uid(): return str(uuid.uuid4())
