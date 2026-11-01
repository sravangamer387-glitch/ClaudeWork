"""Print net -> ESP32-S3 GPIO for a board spec, and compare with the PIN_* defines of a firmware pin header: python3 check_pins.py <board> <header.h> <NET=PIN_NAME,...>"""
import sys, re, importlib
sys.path.insert(0, ".")
M = {"4": 4, "5": 5, "6": 6, "7": 7, "8": 15, "9": 16, "10": 17, "11": 18, "12": 8, "13": 19, "14": 20, "15": 3, "16": 46, "17": 9, "18": 10, "19": 11, "20": 12, "21": 13, "22": 14, "23": 21, "24": 47, "25": 48, "26": 45, "27": 0, "28": 35, "29": 36, "30": 37, "31": 38, "32": 39, "33": 40, "34": 41, "35": 42, "36": "RXD0=44", "37": "TXD0=43", "38": 2, "39": 1}
board, hdr, pairs = sys.argv[1], sys.argv[2], sys.argv[3]
u1 = [p for p in importlib.import_module("boards." + board).BOARD["parts"] if p["ref"] == "U1"][0]["nets"]
net2io = {n: M[p] for p, n in u1.items() if p in M}
defs = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define\s+(PIN_\w+)\s+(\d+)", open(hdr).read())}
bad = 0
for pr in pairs.split(","):
    net, name = pr.split("="); io = net2io.get(net); ok = io == defs.get(name); bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {net:14s} board GPIO {io!s:>4}   header {name} = {defs.get(name)}")
sys.exit(1 if bad else 0)
