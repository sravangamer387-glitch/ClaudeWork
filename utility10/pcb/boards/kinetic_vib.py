from .blocks import *
W, H = 25, 26
parts = [
 dict(ref="U1", sym="Sensor_Motion:ADXL343", fp="Package_LGA:LGA-14_3x5mm_P0.8mm_LayoutBorder1x6y", value="ADXL345", x=8.5, y=12.5, rot=0, lcsc="C9667", lcsc_status="verified", mpn="ADXL345BCCZ-RL7",
      nets={"1": "+3V3", "2": "GND", "4": "GND", "5": "GND", "6": "+3V3", "7": "S_CS", "12": "S_MISO", "13": "S_MOSI", "14": "S_SCLK"}, nc=["3", "8", "9", "10", "11"]),
 C("C1", "100n", 6, 7.5, "+3V3", "GND", 90), C("C2", "100n", 12, 5.5, "+3V3", "GND", 90), C("C3", "10u", 8.5, 19.5, "+3V3", "GND", 90, "Capacitor_SMD:C_0805_2012Metric"),
 dict(ref="J3", sym="Connector_Generic:Conn_02x03_Odd_Even", fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical", value="SPI to controller", x=19.5, y=8, rot=0, lcsc="C5116479", lcsc_status="verified", mpn="ZHOURI 2.54-2*3",
      nets={"1": "+3V3", "2": "GND", "3": "S_SCLK", "4": "S_MOSI", "5": "S_MISO", "6": "S_CS"})]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("ADXL345 vibration sensor, SPI", ["U1", "C1", "C2", "C3"]), ("CONNECTOR (same pinout as the controller sensor header)", ["J3"])], big=())
S["notes"] = [("KINETIC vibration puck: screw or glue flat to the motor end-cap (rigid, short path to the bearing). ADXL345 in SPI mode 3, 3200 Hz output data rate, +-16 g full resolution. Keep the cable under 30 cm.", 0, 0)]
BOARD = dict(clr=0.15, name="kinetic_vib", title="KINETIC vibration puck (ADXL345, SPI)", rev="A", size=(W, H), corner=2.0, parts=parts, sch=S, supply={"+3V3": "controller via cable", "GND": "controller via cable"},
 holes=[(4, 23), (21.5, 23)], fids=[(3.5, 2.5), (21.5, 2.5)], first=["S_SCLK", "S_MOSI", "S_MISO", "S_CS"], gnd_pour_only=True, silk=[("KINETIC VIB", 12.5, 1.3, 0.8)], stitch=4.0)
BOARD["enc"] = dict(standoff=3.0, side=[], lid=[])
