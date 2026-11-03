"""Decoder for the TRISHNA 48-byte telemetry frame (layout in firmware/lib/trishna_core/src/trishna_frame.h). No third-party imports."""
import struct

FRAME_LEN = 48
SYNC = b"\xA5\x5A"
FMT = "<4BHIHI2B3Hh3Hh5H2BH"           # little-endian, packed
assert struct.calcsize(FMT) == FRAME_LEN
FIELDS = ["sync0", "sync1", "version", "type", "seq", "unix_s", "ms", "uptime_s", "state", "prev_state", "event_id", "flags", "error_code",
          "temp_cx100", "ec25_x100", "cell_ohm", "sg_x10000", "a450_x1000", "turb_x1000", "tx_blue_mv", "tx_ir_mv", "sc_ir_mv", "vin_mv",
          "hydration", "quality", "crc16"]
TYPES = {1: "result", 2: "state", 3: "error", 4: "heartbeat", 5: "cal", 6: "live"}
STATES = ["STATE_IDLE", "STATE_STREAM_DETECTED", "STATE_SAMPLING", "STATE_ANALYSIS", "STATE_PURGE_CLEANING", "STATE_LOCKOUT"]
ERRORS = ["none", "leak", "reservoir empty", "temperature sensor", "SD card", "ToF sensor", "optics saturated", "short event",
          "supply low", "supply high", "actuator time limit", "no sample", "analysis timeout", "telemetry queue full"]
FLAGS = ["time_valid", "presence", "stream", "valve_open", "pump_fwd", "pump_rev", "air", "leak", "opt_sat", "sd_ok", "tof_ok", "temp_ok",
         "diluted", "cal_default", "fault_latched", "fallback_trigger"]
HYDRATION = ["unknown", "well hydrated", "adequate", "low", "dehydrated"]


def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def decode(buf: bytes) -> dict:
    """Decode one 48-byte frame into engineering units. Raises ValueError on a bad preamble, version or CRC."""
    if len(buf) != FRAME_LEN or buf[:2] != SYNC or buf[2] != 1:
        raise ValueError("bad preamble/version")
    raw = dict(zip(FIELDS, struct.unpack(FMT, buf)))
    if crc16(buf[:46]) != raw["crc16"]:
        raise ValueError("crc mismatch")
    st = lambda i: STATES[i] if i < len(STATES) else f"state{i}"
    d = {
        "type": TYPES.get(raw["type"], str(raw["type"])), "seq": raw["seq"], "unix_s": raw["unix_s"], "ms": raw["ms"], "uptime_s": raw["uptime_s"],
        "state": st(raw["state"]), "prev_state": st(raw["prev_state"]), "event_id": raw["event_id"],
        "flags": [n for i, n in enumerate(FLAGS) if raw["flags"] >> i & 1], "flags_raw": raw["flags"],
        "error": ERRORS[raw["error_code"]] if raw["error_code"] < len(ERRORS) else str(raw["error_code"]), "error_code": raw["error_code"],
        "temp_c": None if raw["temp_cx100"] == -32768 else raw["temp_cx100"] / 100.0,
        "ec25_mscm": raw["ec25_x100"] / 100.0, "cell_ohm": None if raw["cell_ohm"] == 65535 else raw["cell_ohm"],
        "sg": raw["sg_x10000"] / 10000.0 if raw["sg_x10000"] else None, "a450": raw["a450_x1000"] / 1000.0, "turbidity": raw["turb_x1000"] / 1000.0,
        "tx_blue_mv": raw["tx_blue_mv"], "tx_ir_mv": raw["tx_ir_mv"], "sc_ir_mv": raw["sc_ir_mv"], "vin_v": raw["vin_mv"] / 1000.0,
        "hydration": HYDRATION[raw["hydration"]] if raw["hydration"] < len(HYDRATION) else str(raw["hydration"]), "quality": raw["quality"],
    }
    return d


class Deframer:
    """Feed arbitrary byte chunks; yields decoded frames, resynchronising on the A5 5A preamble after noise or corruption."""
    def __init__(self):
        self.buf = bytearray(); self.good = 0; self.bad = 0

    def feed(self, chunk: bytes):
        self.buf += chunk
        while True:
            i = self.buf.find(SYNC)
            if i < 0:
                del self.buf[:-1]; return
            if i:
                del self.buf[:i]
            if len(self.buf) < FRAME_LEN:
                return
            try:
                f = decode(bytes(self.buf[:FRAME_LEN]))
            except ValueError:
                self.bad += 1; del self.buf[:1]; continue      # false preamble or corrupted frame: slide one byte
            self.good += 1; del self.buf[:FRAME_LEN]
            yield f
