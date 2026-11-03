#!/usr/bin/env python3
"""TRISHNA local bridge: UART (or a microSD log file) -> validated frames -> JSON lines / CSV / MQTT (plain broker or ThingsBoard).

  pip install pyserial paho-mqtt
  # live, print JSON lines and keep a CSV:
  python3 trishna_bridge.py --port /dev/ttyUSB0 --csv trishna.csv
  # live, to a local Mosquitto broker (topic trishna/<device>/<type>):
  python3 trishna_bridge.py --port /dev/ttyUSB0 --mqtt-host 127.0.0.1
  # live, to ThingsBoard (device access token; telemetry on v1/devices/me/telemetry):
  python3 trishna_bridge.py --port /dev/ttyUSB0 --mqtt-host 127.0.0.1 --tb-token YOUR_DEVICE_TOKEN
  # offline: replay the microSD log
  python3 trishna_bridge.py --replay /media/sd/trishna.bin --csv trishna.csv
"""
import argparse, csv, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trishna_frames import Deframer

CSV_COLS = ["host_time", "type", "seq", "unix_s", "ms", "uptime_s", "state", "prev_state", "event_id", "error", "temp_c", "ec25_mscm", "cell_ohm", "sg",
            "a450", "turbidity", "tx_blue_mv", "tx_ir_mv", "sc_ir_mv", "vin_v", "hydration", "quality", "flags"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--port", help="serial port of the USB-serial adapter on J15 (e.g. /dev/ttyUSB0, COM5)")
    src.add_argument("--replay", help="binary frame log (trishna.bin from the microSD card)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--csv", help="append decoded frames to this CSV file")
    ap.add_argument("--quiet", action="store_true", help="no JSON lines on stdout")
    ap.add_argument("--mqtt-host"); ap.add_argument("--mqtt-port", type=int, default=1883)
    ap.add_argument("--device", default="trishna-01", help="device name used in the plain-MQTT topic")
    ap.add_argument("--tb-token", help="ThingsBoard device access token (switches to the ThingsBoard topic and payload)")
    a = ap.parse_args()

    mq = None
    if a.mqtt_host:
        import paho.mqtt.client as mqtt
        try:
            mq = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)       # paho-mqtt 2.x
        except AttributeError:
            mq = mqtt.Client()                                       # paho-mqtt 1.x
        if a.tb_token:
            mq.username_pw_set(a.tb_token)
        mq.connect(a.mqtt_host, a.mqtt_port, keepalive=60); mq.loop_start()

    out = None
    if a.csv:
        new = not os.path.exists(a.csv)
        fh = open(a.csv, "a", newline=""); out = csv.DictWriter(fh, CSV_COLS, extrasaction="ignore")
        if new:
            out.writeheader()

    def emit(f):
        f["host_time"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        if not a.quiet:
            print(json.dumps(f), flush=True)
        if out:
            row = dict(f); row["flags"] = "|".join(f["flags"]); out.writerow(row); fh.flush()
        if mq:
            if a.tb_token:
                ts = f["unix_s"] * 1000 + f["ms"] if f["unix_s"] else int(time.time() * 1000)
                vals = {k: v for k, v in f.items() if k not in ("flags", "host_time") and v is not None}
                vals["flags"] = ",".join(f["flags"])
                mq.publish("v1/devices/me/telemetry", json.dumps({"ts": ts, "values": vals}), qos=1)
            else:
                mq.publish(f"trishna/{a.device}/{f['type']}", json.dumps(f), qos=1)

    d = Deframer()
    if a.replay:
        with open(a.replay, "rb") as fp:
            for f in d.feed(fp.read()):
                emit(f)
    else:
        import serial
        with serial.Serial(a.port, a.baud, timeout=0.2) as s:
            while True:
                chunk = s.read(256)
                if chunk:
                    for f in d.feed(chunk):
                        emit(f)
    print(f"# frames ok {d.good}, rejected {d.bad}", file=sys.stderr)


if __name__ == "__main__":
    main()
