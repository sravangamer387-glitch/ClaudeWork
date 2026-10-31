"""Electrical rule checks run on the board spec (KiCad 7 CLI has no ERC). Returns (errors, warnings)."""
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
from sexp import *
OUT = ("output", "power_out", "tri_state")
def run(B):
    errs, warns = [], []
    refs = [p["ref"] for p in B["parts"]]
    for r in set(refs):
        if refs.count(r) > 1: errs.append(f"duplicate reference {r}")
    nets = {}
    for p in B["parts"]:
        sym = pins(resolve(*p["sym"].split(":"))); nc = p.get("nc", [])
        for num, v in sym.items():
            ptype = v[6]; net = p["nets"].get(num)
            if net is None:
                if nc != "rest" and num not in nc and ptype != "no_connect": errs.append(f"{p['ref']} pin {num} ({v[5]}) unconnected and not declared NC")
                continue
            nets.setdefault(net, []).append((p["ref"], num, v[5], ptype))
        for num in p["nets"]:
            if num not in sym: errs.append(f"{p['ref']}: net assigned to pin {num} which the symbol {p['sym']} does not have")
    supply = B.get("supply", {})
    for net, pl in nets.items():
        if len(pl) < 2 and net not in B.get("single_ok", ()): errs.append(f"net {net} has only one pin: {pl}")
        outs = [x for x in pl if x[3] in OUT]
        if len(outs) > 1: errs.append(f"net {net} has multiple outputs: {outs}")
        pin_in = [x for x in pl if x[3] == "power_in"]
        if pin_in and not outs and net not in supply: errs.append(f"net {net} drives power input pins {pin_in} but has no declared source (add to B['supply'])")
        if all(x[3] == "input" for x in pl): warns.append(f"net {net} has only input pins")
    return errs, warns, nets
