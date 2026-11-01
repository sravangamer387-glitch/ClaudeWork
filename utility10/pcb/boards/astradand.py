from .blocks import *
W, H = 146, 26
leds = []; xs = [55, 46, 37, 28, 19, 10]                                  # six WS2812B-Mini pixels along the head, data enters at the right-hand one
for i, x in enumerate(xs):
    din = "LED_DIN" if i == 0 else f"LED_D{i}"; dout = f"LED_D{i + 1}" if i < 5 else None
    nets = {"1": "VLED", "3": "GND", "4": din}
    if dout: nets["2"] = dout
    leds.append(dict(ref=f"D{11 + i}", sym="LED:WS2812B", fp="LED_SMD:LED_WS2812B-Mini_PLCC4_3.5x3.5mm", value="WS2812B-Mini", x=x, y=5, rot=0, nets=nets, nc=[] if dout else ["2"]))
    leds.append(C(f"C{20 + i}", "100n", x, 10.2, "VLED", "GND", 0))
parts = (mcu("+3V3", {"1": "TRIG", "2": "HAPT", "10": "LED_DIN", "13": "BZ_A", "14": "BZ_B", "9": "LED_EN", "23": "VBAT_DIV", "27": "SDA", "28": "SCL", "32": "IMU_INT"}, 100, 12.5) + isp("+3V3", 46, 19, 90) + batt_input("+4V5", 112, 4.5, "BATT 3xAAA") + leds +
         [dict(ref="U2", sym="Sensor_Motion:MPU-6050", fp="Sensor_Motion:InvenSense_QFN-24_4x4mm_P0.5mm", value="MPU-6050", x=70, y=9, rot=0, lcsc="C24112", lcsc_status="verified", mpn="MPU-6050",
               nets={"1": "GND", "8": "+3V3", "9": "GND", "10": "REGOUT", "11": "GND", "12": "IMU_INT", "13": "+3V3", "18": "GND", "20": "CPOUT", "23": "SCL", "24": "SDA"}, nc=["2", "3", "4", "5", "6", "7", "14", "15", "16", "17", "19", "21", "22"]),
          C("C10", "100n", 70.25, 14.6, "REGOUT", "GND", 270), C("C11", "2.2n", 70.75, 3.6, "CPOUT", "GND", 90), C("C12", "100n", 74.6, 11.2, "+3V3", "GND", 90), C("C13", "100n", 66.4, 11.4, "+3V3", "GND", 90),
          R("R20", "4.7k", 77, 5, "+3V3", "SDA", 90), R("R21", "4.7k", 77, 9, "+3V3", "SCL", 90),
          dict(ref="U3", sym="Regulator_Linear:AP2112K-3.3", fp="Package_TO_SOT_SMD:SOT-23-5", value="AP2112K-3.3", x=118, y=17, rot=0, nets={"1": "+4V5", "2": "GND", "3": "+4V5", "5": "+3V3"}, nc=["4"]),
          C("C5", "1u", 114, 17.5, "+4V5", "GND", 90), C("C6", "1u", 123, 17.5, "+3V3", "GND", 90),
          dict(ref="D20", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=132, y=12, rot=0, nets={"1": "VLED", "2": "LED_SRC"}),
          dict(ref="Q3", sym="Device:Q_PMOS_GSD", fp="Package_TO_SOT_SMD:SOT-23", value="AO3401A", x=128, y=22.5, rot=0, lcsc="C15127", lcsc_status="verified", mpn="AO3401A", nets={"1": "LED_G", "2": "+4V5", "3": "LED_SRC"}),
          dict(ref="Q4", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=123, y=22.5, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "LED_PB", "2": "GND", "3": "LED_G"}),
          R("R33", "100k", 131.5, 22.5, "+4V5", "LED_G", 90), R("R34", "1k", 119, 23.5, "LED_EN", "LED_PB", 0),
          C("C7", "10u", 140, 12, "VLED", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
          R("R30", "330", 61, 6, "LED_DIN", "LED_DIN_R", 90), R("R31", "330k", 134, 21, "+4V5", "VBAT_DIV", 90), R("R32", "100k", 137, 21, "VBAT_DIV", "GND", 90),
          dict(ref="BZ1", sym="Device:Buzzer", fp="Buzzer_Beeper:Buzzer_Murata_PKLCS1212E", value="PKLCS1212E4001", x=24, y=18, rot=0, lcsc="C113159", lcsc_status="verified", mpn="PKLCS1212E4001-R1", nets={"1": "BZ_A", "2": "BZ_B"}),
          button("SW2", "TRIG", 58, 20.5, "Cast trigger"),
          dict(ref="Q1", sym="Device:Q_NPN_BEC", fp="Package_TO_SOT_SMD:SOT-23", value="MMBT3904", x=80, y=19.5, rot=0, lcsc="C20526", lcsc_status="verified", mpn="MMBT3904", nets={"1": "HAPT_B", "2": "GND", "3": "HAPT_N"}),
          dict(ref="D2", sym="Device:D", fp="Diode_SMD:D_SOD-323", value="1N4148WS", x=80, y=23.5, rot=0, lcsc="C2128", lcsc_status="verified", mpn="1N4148WS", nets={"1": "+4V5", "2": "HAPT_N"}),
          R("R6", "1k", 85, 21.5, "HAPT", "HAPT_B", 90), jst("J4", 2, 68, 21.5, ["+4V5", "HAPT_N"], "Haptic motor", 0),
          TP("TP1", "+4V5", 111, 23.2), TP("TP2", "GND", 115, 23.2)])
parts = [dict(p, nets={k: ("LED_DIN" if v == "LED_DIN_R" else v) for k, v in p["nets"].items()}) if p["ref"] == "R30" else p for p in parts]
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
parts = [dict(p, nets={k: v for k, v in p["nets"].items() if v is not None}) for p in parts]
S = sch_layout([("POWER: 3xAAA, switch, reverse-polarity PMOS, 3.3 V LDO, LED supply diode, battery divider", ["J1", "SW1", "Q2", "C4", "U3", "C5", "C6", "Q3", "Q4", "R33", "R34", "D20", "C7", "R31", "R32", "TP1", "TP2"]), ("MCU: ATmega328P-AU, 3.3 V, 8 MHz internal", ["U1", "C1", "C2", "C3", "R7", "J2"]),
               ("MOTION: MPU-6050 6-axis IMU on I2C", ["U2", "C10", "C11", "C12", "C13", "R20", "R21"]), ("LIGHT: six WS2812B-Mini pixels (daisy chain), each with 100 nF", [f"D{11 + i}" for i in range(6)] + [f"C{20 + i}" for i in range(6)] + ["R30"]),
               ("TRIGGER, SOUND, HAPTIC", ["SW2", "BZ1", "Q1", "D2", "R6", "J4"])], big=("U1",))
S["notes"] = [("ASTRADAND: hold the trigger, draw a shape in the air, release. The 6-axis IMU is read over I2C at 50 Hz; the ATmega matches the drawn path against six spell templates. Piezo is driven differentially from OC1A/OC1B (D9/D10). LEDs are fed from +4V5 through a high-side switch (Q3, driven by Q4 from D5) and a Schottky (D20), so the pixels draw nothing in sleep so that their 0.7 x VDD data threshold stays below the 3.3 V logic level; the firmware caps the pixel current.", 20, 300)]
PRE = [dict(net="REGOUT", layer=0, pts=[(70.25, 10.95), (70.25, 13.825)], w=0.2), dict(net="CPOUT", layer=0, pts=[(70.75, 7.05), (70.75, 4.375)], w=0.2),
       dict(net="SDA", layer=0, pts=[(68.75, 7.05), (68.75, 5.6)], w=0.2), dict(net="SDA", layer=1, pts=[(68.75, 5.6), (75.6, 4.175)], w=0.2), dict(net="SDA", layer=0, pts=[(75.6, 4.175), (77.0, 4.175)], w=0.2),
       dict(net="SCL", layer=0, pts=[(69.25, 7.05), (69.25, 6.0), (69.65, 5.5)], w=0.2), dict(net="SCL", layer=1, pts=[(69.65, 5.5), (75.6, 8.175)], w=0.2), dict(net="SCL", layer=0, pts=[(75.6, 8.175), (77.0, 8.175)], w=0.2),
       dict(net="+3V3", layer=0, pts=[(71.95, 10.25), (73.4, 10.25), (73.4, 11.975), (74.6, 11.975)], w=0.2), dict(net="+3V3", layer=0, pts=[(69.25, 10.95), (69.25, 12.175), (66.4, 12.175)], w=0.2)]
PREV = [("SDA", 68.75, 5.6), ("SDA", 75.6, 4.175), ("SCL", 69.65, 5.5), ("SCL", 75.6, 8.175)]      # IMU escape routes by hand: the 0.5 mm pitch QFN cannot be escaped by the grid router; I2C goes under the board on B.Cu for 7 mm
BOARD = dict(pre=PRE, pre_vias=PREV, clr=0.15, name="astradand_main", title="ASTRADAND gesture wand - main board", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S, supply={"+4V5": "battery via Q2", "+3V3": "LDO U3", "VLED": "battery via Q3 and D20", "LED_SRC": "battery via Q3", "GND": "battery", "BAT_P": "battery"}, single_ok=("BAT_P", "BZ_A", "BZ_B", "HAPT_N", "LED_D6"),
 holes=[(3.5, 22.5), (W - 3.5, 22.5)], fids=[(14, 24), (W - 3.5, 3.5)], widths={"+4V5": 0.4, "VLED": 0.4}, first=["LED_DIN", "SDA", "SCL", "IMU_INT", "+3V3", "BAT_P", "BAT_SW"], gnd_pour_only=True,
 silk=[("ASTRADAND rev A", 76, 1.8, 0.9), ("TRIG", 58, 17.5, 0.7), ("MOTOR", 68, 18.8, 0.7)], stitch=4.0)
BOARD["enc"] = dict(standoff=4.0, side=[("SW2", "top", 4, 3, 1.5), ("J1", "bottom", 9, 7, 3)], lid=[("round", "SW2", 5.0)])
