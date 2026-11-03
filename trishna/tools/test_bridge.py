#!/usr/bin/env python3
"""Cross-checks the Python decoder against frames sealed by the C firmware library (written by the host unit tests).
usage: make -C ../firmware/test/host && python3 test_bridge.py ../firmware/test/host/golden_frames.bin"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trishna_frames import Deframer, decode, crc16

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "firmware", "test", "host", "golden_frames.bin")
data = open(path, "rb").read()
assert len(data) == 3 * 48, len(data)
assert crc16(b"123456789") == 0x29B1
f0 = decode(data[:48])
checks = [(f0["type"], "result"), (f0["seq"], 513), (f0["unix_s"], 1793664000), (f0["state"], "STATE_ANALYSIS"), (f0["prev_state"], "STATE_SAMPLING"),
          (f0["event_id"], 42), (f0["temp_c"], 34.12), (f0["ec25_mscm"], 18.73), (f0["cell_ohm"], 151), (f0["sg"], 1.0171), (f0["a450"], -0.012),
          (f0["turbidity"], 0.037), (f0["vin_v"], 12.04), (f0["hydration"], "adequate"), (f0["quality"], 90), (sorted(f0["flags"]), sorted(["time_valid", "stream", "temp_ok"]))]
for got, want in checks:
    assert got == want, (got, want)
# stream with noise, a corrupted copy and a false preamble: exactly the 3 good frames must come out, in order
bad = bytearray(data[:48]); bad[20] ^= 0xFF
stream = b"\x00\xA5\x13garbage" + data[:48] + bytes(bad) + b"\xA5\x5A\x01" + data[48:]
d = Deframer(); out = []
for i in range(0, len(stream), 7):                      # feed in odd-sized chunks like a UART would
    out += list(d.feed(stream[i:i + 7]))
assert [f["seq"] for f in out] == [513, 514, 515], [f["seq"] for f in out]
assert out[2]["type"] == "error" and out[2]["error"] == "leak"
print(f"bridge decoder OK: {len(checks)} field checks, resync test passed ({d.good} good, {d.bad} rejected)")
