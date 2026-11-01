"""Manufacturing manuals for the three new programmes: KINETIC, MITTI-NETRA, BioTray (+ BioWatt status page). Reads the release folders of the PCBs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mlib import *

def state(rel, name):
    ok = os.path.exists(os.path.join(ROOT, rel, "README.md"))
    if not ok: return False, None, "**PCB not released yet: do not send to a fab**"
    bi = board_info(rel, name)
    return True, bi, ("**order-ready: every automatic check passes**" if bi["rdy"]["order_ready"] else "**not order-ready: see 5_verification/readiness.json**")

COMMON_MAKE = ("1. Upload `{rel}/1_fabrication/{name}_gerbers.zip` to the PCB fab (2 layers, 1.6 mm, ENIG or lead-free HASL, green mask, white silk; {copper}). "
               "2. For assembly upload `2_assembly/{name}_JLC_BOM.csv` and `{name}_JLC_CPL.csv`; check every polarity in the preview (diodes, electrolytic capacitor, USB-C, ESP32 module pin 1). "
               "3. Through-hole connectors and pin sockets are listed with LCSC numbers but are normally hand-soldered. 4. General rules, tolerances and inspection: `manuals/STANDARD_PROCEDURES.md` sections A and B.")

def write(path, lines): open(os.path.join(ROOT, path), "w").write("\n".join(lines)); print("wrote", path)

# ---------------- KINETIC ----------------
ok1, b1, s1 = state("utility10/pcb/release/kinetic_ctl", "kinetic_ctl"); ok2, b2, s2 = state("utility10/pcb/release/kinetic_vib", "kinetic_vib")
L = ["# KINETIC motion controller + vibration puck: manufacturing manual", "", f"> **Status: design only; nothing built, powered or run on a motor.** Controller PCB: {s1}. Vibration puck PCB: {s2}. AI model: trained on synthetic data only. Firmware: motion/vibration core host-tested; ESP32 glue syntax-checked only.", "",
 "## 1. What is made", "", "A 112 x 80 mm controller (ESP32-S3, three StepStick driver sockets, 24 V input, 5 V buck, endstops, host UART/USB) and a 25 x 26 mm ADXL345 vibration puck on a 6-pin SPI cable. Drivers (A4988 / DRV8825 / TMC2209 modules) and motors are bought separately.", "",
 "## 2. Deliverables", "", "| Item | Where | State |", "|---|---|---|", f"| Controller PCB (Gerbers, BOM, CPL, KiCad, STEP) | `utility10/pcb/release/kinetic_ctl/` and `kinetic/hardware/kinetic_ctl/` | {s1} |", f"| Vibration puck PCB | `utility10/pcb/release/kinetic_vib/` and `kinetic/hardware/kinetic_vib/` | {s2} |",
 "| Motion + protocol library and tests | `kinetic/firmware/lib/kn_motion.[ch]`, `kinetic/firmware/test/test_kn.c` | `make test` passes (370 checks) |", "| Vibration model | `kinetic/sim/vib.py`, `kinetic/firmware/lib/kn_vib*.{c,h}` | synthetic data; C matches Python |", "| ESP32 skeleton | `kinetic/firmware/src/main_kinetic.cpp` | syntax-checked, never compiled for ESP32 |",
 "| Enclosure STL (printed) | `utility10/pcb/release/kinetic_ctl/4_enclosure/` | generated from the board outline; unprototyped |", "| Docs | `kinetic/docs/` (CONCEPT, DESIGN, PROTOCOL, TEST_PLAN, economics, vib_results) | |", ""]
if ok1: L += ["## 3. Controller bill of materials", "", bom_table(b1["bom"]), ""]
if ok2: L += ["### Vibration puck bill of materials", "", bom_table(b2["bom"]), ""]
L += ["### Bought-in", "", "StepStick driver modules (1-3), NEMA17 motors, 12-28 V supply (24 V recommended) with current limit capability for bring-up, 1x8 female socket strips are on the BOM, endstop switches, 6-wire cable for the puck (under 30 cm), M2.5 screws.", "",
 "## 4. Make the boards", "", COMMON_MAKE.format(rel="utility10/pcb/release/kinetic_ctl", name="kinetic_ctl", copper="order 2 oz copper if you will drive more than about 1 A per motor phase: the motor traces are 0.4 mm"), "Repeat for `kinetic_vib` (1 oz is fine).", "",
 "## 5. Program", "", "Build with Arduino-ESP32 core 2.x or PlatformIO (`esp32-s3-devkitc-1`): sources `kinetic/firmware/src/main_kinetic.cpp` plus `kinetic/firmware/lib/*.c`. First flash over USB-C (hold BOOT, tap RESET). **Review the skeleton on a bench first: it has never been compiled for the ESP32.**", "",
 "## 6. Commissioning (see `kinetic/docs/TEST_PLAN.md` for the full list)", "", "1. Current-limited 24 V, no drivers fitted: TP1 24 V, TP2 5.0 V, TP3 3.3 V. 2. Reverse the supply once with 100 mA limit: nothing conducts. 3. Fit ONE driver with the motor disconnected; set its current limit; power off; connect the motor. 4. `MOVE X=1000` and watch STEP/DIR on a scope. 5. Endstop trip stops motion and needs `CLEAR`. 6. Puck: device ID 0xE5, rest Z = +1 g.", "",
 "## 7. Safety and limits", "", "Never plug or unplug a motor with power on (destroys drivers). The TVS and bulk capacitor assume at most 28 V. No ESD protection on USB data. The 3.3 V LDO is limited to 600 mA. The vibration classifier is a demonstration trained on simulated faults: do not use it to decide maintenance without retraining on real recordings. Not safety-rated: it is not an emergency-stop system.", ""]
write("kinetic/MANUFACTURING_MANUAL.md", L)

# ---------------- MITTI-NETRA ----------------
ok, b, s = state("utility10/pcb/release/mitti", "mitti_netra")
L = ["# MITTI-NETRA soil and structure telemetry node: manufacturing manual", "", f"> **Status: design only; nothing built or connected to a mobile network.** PCB: {s}. The cellular modem is a plug-in SIM7080G breakout (not on the board). Firmware core host-tested; ESP32 glue syntax-checked only.", "",
 "## 1. What is made", "", "A 90 x 80 mm solar/USB-charged node: ESP32-S3, TP4056 charger for one protected Li-ion cell, 3.3 V LDO, switched socket for a SIM7080G breakout, ADXL345 tilt/vibration, HX711 strain bridge input, capacitive soil probe input, DS18B20 input. An optional Raspberry Pi/Banana Pi runs `camera/crop_index.py`.", "",
 "## 2. Deliverables", "", "| Item | Where | State |", "|---|---|---|", f"| PCB | `utility10/pcb/release/mitti/` and `mitti-netra/hardware/` | {s} |", "| Core library and tests | `mitti-netra/firmware/lib/mn_core.[ch]`, `test/test_mn.c` | `make test` passes (23 checks) |", "| ESP32 skeleton | `mitti-netra/firmware/src/` | syntax-checked only; cellular send is a TODO |", "| Camera analysis | `mitti-netra/camera/crop_index.py` | self-test passes on synthetic scenes |", ""]
if ok: L += ["## 3. Bill of materials", "", bom_table(b["bom"]), ""]
L += ["### Bought-in", "", "SIM7080G (LTE-M/NB-IoT) breakout board with nano-SIM holder and antenna; protected 18650 cell (or protected pouch cell) with JST-PH 2 lead; 5-6 V solar panel (2 W) with JST-PH 2 lead; capacitive soil moisture probe (3.3 V, analog) with JST-PH 3 lead; DS18B20 waterproof probe; strain gauges (350 ohm, GF about 2) with bridge completion; IP65 enclosure with cable glands; a SIM and data plan.", "",
 "## 4. Make the board", "", COMMON_MAKE.format(rel="utility10/pcb/release/mitti", name="mitti_netra", copper="1 oz is fine"), "The ADXL345 is an LGA-14 part: use the fab's reflow assembly; do not hand-solder it.", "",
 "## 5. Program and configure", "", "Arduino-ESP32 core 2.x: `mitti-netra/firmware/src/main_mitti.cpp` plus `firmware/lib/mn_core.c`. Set the placeholders: soil calibration counts (dry air, water), strain excitation/gauge factor/bridge type, tilt and strain thresholds. Install: tilt the node into its final position, power up once: that boot stores the baseline (tilt angles and strain zero) in RTC memory; a power loss loses the baseline.", "",
 "## 6. Test (see `mitti-netra/docs/TEST_PLAN.md`)", "", "Charge LEDs; TP2 3.3 V; deep-sleep current; modem switch toggles VBAT_M; ADXL345 ID 0xE5; tilt plate 10 degrees reads 10 +-0.5; HX711 shunt-resistor check; 7-day outdoor run.", "",
 "## 7. Limits", "", "No cell protection on the board (use protected cells). LDO stops below about 3.55 V on the cell. Strain numbers are conversions, not a calibrated instrument. Carrier APN, bands and a server are not provided. Not safety-rated.", ""]
write("mitti-netra/MANUFACTURING_MANUAL.md", L)

# ---------------- BioTray ----------------
ok, b, s = state("utility10/pcb/release/biotray", "biotray")
L = ["# BioTray vertical-farm tray controller: manufacturing manual", "", f"> **Status: design only; nothing built.** PCB: {s}. Firmware control core host-tested (22 checks); ESP32 glue never compiled. pH/EC calibration values are placeholders.", "",
 "## 1. What is made", "", "A 100 x 80 mm controller: 12 V in, ESP32-S3 (WiFi/MQTT), four low-side 12 V outputs (2 pumps, fan, PWM grow light), DS18B20, I2C (BH1750/SHT31), water-level switch, analog pH and EC inputs.", "",
 "## 2. Deliverables", "", "| Item | Where | State |", "|---|---|---|", f"| PCB | `utility10/pcb/release/biotray/` and `biotray/hardware/` | {s} |", "| Control core + tests | `biotray/firmware/lib/bt_core.[ch]`, `test/test_bt.c` | passes |", "| ESP32 skeleton | `biotray/firmware/src/main_biotray.cpp` | not compiled |", ""]
if ok: L += ["## 3. Bill of materials", "", bom_table(b["bom"]), ""]
L += ["### Bought-in", "", "12 V 3 A adapter (barrel 5.5/2.1, centre positive), 12 V peristaltic or submersible pumps, 12 V fan, 12 V LED grow strip (total under 1.1 A or replace the PTC), DS18B20 probe, BH1750 module, float switch, pH module and probe, EC module and probe, tubing, tray.", "",
 "## 4. Make the board", "", COMMON_MAKE.format(rel="utility10/pcb/release/biotray", name="biotray", copper="1 oz is fine for loads up to about 1 A total"), "",
 "## 5. Program and configure", "", "Arduino-ESP32 core 2.x with PubSubClient, OneWire, DallasTemperature, BH1750. Copy `secrets.h.example` to `secrets.h`. Calibrate pH with pH 4 and pH 7 buffers and EC with a standard solution, then edit `PH_CAL`, `EC_CAL`. MQTT topics: see `biotray/docs/DESIGN.md`.", "",
 "## 6. Test (see `biotray/docs/TEST_PLAN.md`)", "", "Supply rails, reverse-polarity test, dummy loads on every output, dry-run test (remove water: pump stops and latches), 48 h run.", "",
 "## 7. Limits", "", "Water, mains adapter and electricity together: use a GFCI-protected supply and an enclosure with proper sealing. No isolation on the pH probe. Not tested on hardware.", ""]
write("biotray/MANUFACTURING_MANUAL.md", L)

# ---------------- BioWatt ----------------
ok, b, s = state("utility10/pcb/release/biowatt", "biowatt")
L = ["# BioWatt MFC energy-harvester board: manufacturing manual", "", f"> **Status: design only; nothing built or tested with a real fuel cell.** PCB: {s}. Setting resistors derived from the TI BQ25570 datasheet equations (SLUSBH2G).", "",
 "## 1. What is made", "", "A 44 x 40 mm board: BQ25570 harvester (boost charger with MPPT at 50 % of Voc, nano-power buck) from a microbial fuel cell input (J1) into a protected single Li-ion/LiPo cell (J2), with a regulated 3.35 V output and a VBAT_OK flag on J3. Thirteen 1 % megohm resistors set VBAT_OV 3.95 V, VBAT_OK 3.35 V falling / 3.63 V rising and VOUT 3.35 V; the region around them has no ground pour.", "",
 "## 2. Deliverables", "", "| Item | Where | State |", "|---|---|---|", f"| PCB | `utility10/pcb/release/biowatt/` and `biowatt/hardware/biowatt/` | {s} |", "| Energy budget model | `biowatt/sim/budget.py`, `biowatt/docs/budget.md` | assumption-based |", ""]
if ok: L += ["## 3. Bill of materials", "", bom_table(b["bom"]), ""]
L += ["### Bought-in", "", "Protected single Li-ion/LiPo cell (3.7 V) with JST-PH 2 lead; MFC with JST-PH 2 lead; load tag on J3 (BLE/LoRa class: average current well under 1 mA).", "",
 "## 4. Make the board", "", COMMON_MAKE.format(rel="utility10/pcb/release/biowatt", name="biowatt", copper="1 oz is fine"), "The megohm resistors are 0603 1 % parts (5.6 M, 4.3 M, 1 M): check the CPL preview and clean flux residue thoroughly afterwards, then keep the board dry.", "",
 "## 5. Commissioning", "", "1. Bench supply 0.8 V, current-limited 5 mA, on J1: with no cell fitted VSTOR (TP2) rises. 2. Fit a protected cell: VBAT_OK goes high above about 3.63 V and drops below 3.35 V. 3. VOUT (TP3) reads 3.35 V. 4. Then connect the MFC.", "",
 "## 6. Limits", "", "Cold start needs VIN of at least 600 mV: a single MFC (0.5-0.7 V) is marginal, use two in series or a start-up source. C6 is a stocked X7R 10 nF where the datasheet asks for a low-leakage part. MFC power (about 20 uW) supports only a BLE/LoRa tag. Not tested on hardware.", ""]
write("biowatt/MANUFACTURING_MANUAL.md", L)
