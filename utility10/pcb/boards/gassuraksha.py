from .blocks import *
W, H = 84, 60
V = lambda **k: dict(k, lcsc_status="verified")
usb = usb_c_power(16, 4.31)                       # J1 USB-C 5 V (power only), F1, D3, R1, R2, C5 -> +5V
batt = batt_input("+4V5", 6, 53, "BATT 3xAA")      # J1 (renamed J5), SW1, Q2, C4 -> +4V5
for p in batt:
    if p["ref"] == "J1": p["ref"] = "J5"
bz = buzzer("VSYS", "BUZ", 4, 22)                  # BZ1, Q1, D2, R6
for p in bz:
    if p["ref"] == "BZ1":                          # ACTIVE buzzer (built-in oscillator): the firmware switches it on and off; series resistor sets about 3 V across it
        p.update(value="Buzzer active 3V", lcsc="C3015483", lcsc_status="verified", mpn="S&S SUN-1275Y-0327-50P7.6", nets={"1": "BZ_P", "2": "BZ_N"})
parts = (usb + batt + bz + mcu("VSYS", {"32": "SILENCE", "1": "TEST", "12": "BUZ", "13": "LED_G", "14": "LED_A", "23": "SENSE_F", "24": "BATSENSE", "30": "RXD", "31": "TXD", "7": "XTAL1", "8": "XTAL2"}, 50, 31) + isp("VSYS", 74, 37) + [
    R("R20", "47", 8, 22, "VSYS", "BZ_P", 90),
    V(ref="D6", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=30, y=22, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VSYS", "2": "+5V"}),
    V(ref="D7", sym="Device:D_Schottky", fp="Diode_SMD:D_SMA", value="SS14", x=34, y=50, rot=0, lcsc="C84343", mpn="SS14", nets={"1": "VSYS", "2": "+4V5"}),
    C("C20", "10u", 40, 14, "VSYS", "GND", 0, "Capacitor_SMD:C_0805_2012Metric"),
    dict(ref="Y1", sym="Device:Crystal_GND24", fp="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", value="16 MHz", x=35.5, y=34.5, rot=0, nets={"1": "XTAL1", "2": "GND", "3": "XTAL2", "4": "GND"}),
    C("C9", "22p", 31.5, 37, "XTAL1", "GND", 90), C("C10", "22p", 31.5, 32, "XTAL2", "GND", 90),
    dict(ref="J3", sym="Connector_Generic:Conn_01x04", fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", value="MQ-6 module: VCC GND DO AO", x=78, y=8, rot=0, lcsc="C5116483", lcsc_status="verified", mpn="ZHOURI 2.54-1*4", nets={"1": "VSYS", "2": "GND", "3": "MQ_DO", "4": "SENSE"}),
    R("R10", "1k", 62, 20, "SENSE", "SENSE_F", 90), C("C11", "100n", 66, 20, "SENSE_F", "GND", 90),
    R("R11", "220k", 62, 44, "+4V5", "BATSENSE", 90), R("R12", "220k", 66, 44, "BATSENSE", "GND", 90), C("C12", "100n", 70, 44, "BATSENSE", "GND", 90),
    jst("J4", 3, 74, 52, ["GND", "TXD", "RXD"], "UART log (adapter RX, TX)"),
    button("SW2", "SILENCE", 18, 36, "Silence"), button("SW3", "TEST", 18, 44, "Test"),
    TP("TP1", "VSYS", 44, 6), TP("TP2", "GND", 50, 6), TP("TP3", "SENSE", 82, 20)] +
    led("VSYS", "LED_G", 40, 56, "Green", "D1", "R5") + led("VSYS", "LED_A", 50, 56, "Amber", "D4", "R8") + led("VSYS", "MOSI", 60, 56, "Red", "D5", "R9"))
for p in parts:
    if p.get("lcsc", 1) is None: del p["lcsc"]
S = sch_layout([("POWER: USB-C 5 V and 3xAA backup OR-ed into VSYS through Schottky diodes", ["J1", "F1", "D3", "R1", "R2", "C5", "J5", "SW1", "Q2", "C4", "D6", "D7", "C20", "TP1", "TP2"]), ("MCU: ATmega328P-AU, 16 MHz, ISP and UART header", ["U1", "Y1", "C9", "C10", "C1", "C2", "C3", "R7", "J2", "J4"]),
               ("SENSOR: MQ-6 module socket, filtered analog input, battery divider", ["J3", "R10", "C11", "R11", "R12", "C12", "TP3"]), ("ALARM: active buzzer, three LEDs, silence and test buttons", ["BZ1", "R20", "Q1", "D2", "R6", "D1", "R5", "D4", "R8", "D5", "R9", "SW2", "SW3"])], big=("U1",))
S["notes"] = [("Gas-Suraksha PROTOTYPE / DATA-LOGGING BOARD, NOT A CERTIFIED GAS DETECTOR. It carries the alarm engine from firmware/lib/gas_core on an ATmega328P with a socket for a common MQ-6 module (VCC, GND, DO, AO: check your module's pin order). USB-C 5 V and a 3xAA pack are OR-ed through Schottky diodes into VSYS (about 4.1 to 4.7 V): the MQ-6 heater sees this, so calibrate readings per supply. The ACTIVE 3 V buzzer is fed through 47 ohm; the firmware switches pin D8 on and off. D11 (red LED) shares the MOSI line like an Arduino D13 LED. Program through the ISP header (firmware/release/gas_suraksha_demo.hex, 16 MHz, external crystal fuses); read logs on the UART header at 115200 baud. Do not sell or rely on it as a safety device.", 0, 0)]
BOARD = dict(clr=0.15, name="gas_suraksha", title="Gas-Suraksha prototype and data-logging board (NOT a certified gas detector)", rev="A", size=(W, H), corner=2.5, parts=parts, sch=S,
 supply={"VSYS": "USB 5 V or 3xAA via Schottky diodes", "+5V": "USB via PTC", "+4V5": "battery via Q2", "GND": "supply", "VBUS": "USB host", "BAT_P": "battery", "BAT_SW": "battery switch"}, single_ok=("CC1", "CC2", "MQ_DO"),
 holes=[(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], fids=[(14, H - 2.5), (W - 14, H - 2.5)], widths={"VBUS": 0.4, "VSYS": 0.4, "+5V": 0.4}, first=["CC1", "CC2", "VBUS", "VSYS", "XTAL1", "XTAL2"], edge_ok=("J1",), gnd_pour_only=True,
 silk=[("GAS-SURAKSHA PROTOTYPE rev A: NOT CERTIFIED", 18, H - 1.6, 0.8), ("MQ-6", 78, 3.2, 0.7), ("UART", 74, 48.3, 0.7)], stitch=5.0)
BOARD["enc"] = dict(standoff=4.0, side=[("J1", "top", 9.6, 3.8, 1.9)], lid=[("round", "SW2", 5.0), ("round", "D1", 2.2), ("round", "D4", 2.2), ("round", "D5", 2.2)])
