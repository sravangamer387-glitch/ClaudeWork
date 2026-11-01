import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mlib import *
FUSE = {"4MHz": ("0xE2", "0xD9", "0xFE", "internal 8 MHz RC, CKDIV8 off, brown-out 1.8 V; the firmware then divides the clock to 4 MHz (2 x AAA supply may fall to 2.0 V)"),
        "8MHz": ("0xE2", "0xD9", "0xFD", "internal 8 MHz RC, CKDIV8 off, brown-out 2.7 V (the 8 MHz speed-grade limit): the unit resets cleanly when the battery is flat")}
T = {
 "01-seeti-counter": dict(board="seeti", name="seeti_counter", rel="utility10/pcb/release/seeti", hex="seeti_prod.hex", clk="4MHz", pcs="2 x AAA", title="Seeti Counter",
   acc=["**Heat-resistant microphone clip.** Solder the electret capsule (J3, 2-pin JST-PH lead, + toward the marked pin) to a 30 cm 2-core lead. Fix the capsule in the clip behind a stainless-steel mesh window so steam cannot reach it. The clip must hold the capsule 10 cm from the cooker vent and be rated to 85 C (use a high-temperature ABS or metal spring clip; do not use a PLA part near the vent).", "Add a magnet or hook to the unit's back so it stays on the hood; the electronics unit itself must stay at least 10 cm from the vent."],
   cal=["Whistle frequency is an assumption (2.8 kHz in the tests). Record 5 real cookers of the brands you target, find the dominant whistle frequency and amplitude with a phone spectrum app, and set the filter frequency in `firmware/lib/utilcore.c` (`seeti_*`) before the production run. Re-run the 115 host tests (`make test`)."],
   eol=["Play a 2.8 kHz tone from a phone speaker at 10 cm for 1 s: the counter increments; play white noise: it must not count.", "Press the button to select 1, 3 and 6 whistles; after the selected count the buzzer rings 5 times.", "Battery: measure the supply current at 3.0 V; it should be a few mA (estimate 3.6 mA); a unit above 10 mA fails."],
   tr=[("Counts nothing", "microphone polarity reversed or gain too low: check TP3 swing at a 2.8 kHz tone, about +-100 mV"), ("Counts noise", "threshold or filter frequency wrong for this microphone placement; see the limit in the README (amplitude 300 against noise 1200 counted 0 of 3)")]),
 "02-gas-taraju": dict(board="gastaraju", name="gas_taraju", rel="utility10/pcb/release/gastaraju", hex="boards/gas_taraju.hex", clk="8MHz", pcs="3 x AA", title="Gas Taraju (LPG cylinder scale)",
   acc=["**Plate and load cells.** Laser-cut the 330 mm plate from the SVG/DXF in `utility10/out/` (check the product README for the file name); fit four load cells (half-bridge or full-bridge, wiring to the HX711 E+/E-/A+/A- inputs) under the plate corners on a rigid, level base with four rubber feet. A warped base or a plate that rocks destroys accuracy.", "Bonded-load-cell wiring: keep cable lengths equal and short; shield away from the buzzer lead."],
   cal=["Per-unit calibration is mandatory. Zero the empty plate, place a certified 20 kg reference weight, record counts per kg and offset, store in EEPROM; repeat at 5, 10, 15 kg to check linearity (error under +-0.1 kg). The user enters the cylinder tare weight stamped on the collar."],
   eol=["Zero the plate; place a 20 kg reference weight: reading within +-0.1 kg; remove: returns to 0 +-0.05 kg.", "Place a 14.2 kg net cylinder-equivalent (use test weights): reads 100 %; check the LED/buzzer low warning at 15 %."],
   tr=[("Reading drifts", "plate not rigid, one load cell loaded unevenly, or HX711 supply noisy: check the 4V5 rail ripple"), ("This is not a leak detector", "do not describe it as a gas safety device: it is a weight scale only")],),
 "03-fridge-door-guard": dict(board="fridge", name="fridge_door_guard", rel="utility10/pcb/release/fridge", hex="boards/fridge_guard.hex", clk="4MHz", pcs="2 x AAA", title="Fridge Door Guard",
   acc=["**Reed switch and magnet.** Solder the reed switch (J3) to a 20 cm 2-core lead and fix it in the housing edge; glue a small neodymium magnet into a second housing piece; mounting is by 3M adhesive so the two halves face each other across the door gap with under 5 mm separation (alignment tolerance is not verified: test with the real fridge)."],
   cal=["None. Verify that the reed closes reliably at the real door gap and magnet distance (try 2, 4 and 6 mm)."],
   eol=["Magnet near the reed: silent; magnet away 65 s: chirp; 185 s: continuous alarm; magnet back: silent.", "Count the openings logged after 11 short opens: no warning should have sounded."],
   tr=[("Alarm sounds with the door closed", "magnet too far or reed contact stuck: replace the reed"), ("Battery empties early", "check sleep behaviour; battery life is not measured")]),
 "04-bijli-meter-reader": dict(board="bijli", name="bijli_meter_reader", rel="utility10/pcb/release/bijli", hex="boards/bijli_meter.hex", clk="8MHz", pcs="5 V USB charger (not supplied with the PCB)", title="Bijli Meter Reader",
   acc=["**Clip-on sensor head.** Solder the phototransistor/photodiode (J3 3-pin lead: +5 V, SIG, GND) on a 1.5 m cable inside a black ABS clip that blocks ambient light and sits over the meter's pulse LED; use heat-shrink at the cable exit. **There is no mains contact: never open the meter or touch its terminals.**", "Display: a TM1637 4-digit module plugs into the 4-pin JST-PH J4 (GND, +5V, DIO, CLK)."],
   cal=["Enter the meter constant (pulses per kWh, printed on the meter) in the setup; verify with a known load (a 100 W lamp for 10 minutes gives about 0.017 kWh)."],
   eol=["Flash a 1 Hz LED at the head: count = 1 per second; cover with ambient light: no spurious counts.", "Check that watts and kWh are displayed and the estimated bill uses the slab rates entered."],
   tr=[("No pulses", "head not aligned to the pulse LED: check SIG voltage swing, at least 0.5 V drop when the LED is lit"), ("Count too high", "ambient light leak: improve the clip shielding")]),
 "05-bijli-log": dict(board="bijlilog", name="bijli_log", rel="utility10/pcb/release/bijlilog", hex="boards/bijli_log.hex", clk="4MHz", pcs="5 V USB charger + 2 x AAA backup", title="Bijli Log",
   acc=["**Modules.** OLED 0.91 in I2C module on J4 and DS3231 RTC module on J5 (GND, +V, SDA, SCL order is printed on the board). Fit a CR2032/AAA backup as per the README; use a certified, BIS-registered 5 V adapter: the unit itself is low voltage."],
   cal=["Set the RTC time once at the factory (and again by the user after a battery replacement). Check the RTC drift over 24 h (module spec about +-2 ppm for DS3231; clone modules vary)."],
   eol=["Remove 5 V for 10 s: one cut of 10 s +-1 s is logged; restore power.", "Pull the cable again twice: the count increases and the last-cut screen updates.", "Check the log survives a full power removal (backup cell holds the RTC)."],
   tr=[("Time resets after power loss", "RTC battery missing or dead"), ("OLED blank", "wrong module pinout: some modules swap GND and VCC")]),
 "06-chulha-timers": dict(board="chulha", name="chulha_timers", rel="utility10/pcb/release/chulha", hex="boards/chulha_timers.hex", clk="8MHz", pcs="3 x AAA", title="Chulha Timers",
   acc=["**Magnet back.** Glue a flat ferrite or neodymium magnet (about 30 x 20 x 3 mm) to the back plate with epoxy; keep it away from the display ribbon. TM1637 display module goes on J4."],
   cal=["None. Check the timing accuracy over 10 minutes against a reference stopwatch: the internal RC oscillator is about +-1 to 2 %, which is 6-12 s in 10 minutes: decide whether that is acceptable (a crystal is not fitted) and say so on the pack."],
   eol=["Set 1:00 on each of the four channels (tap adds one minute): four independent rings within +-1 s of each other.", "Hold a button 1 s: the channel clears."],
   tr=[("Timers run fast/slow", "internal RC tolerance: calibrate OSCCAL on the unit if tighter accuracy is needed")]),
 "07-rain-alert": dict(board="rain", name="rain_alert_main", rel="utility10/pcb/release/rain", hex="boards/rain_alert.hex", clk="8MHz", pcs="3 x AA", title="Rain Alert Bell (indoor unit + rain plate)",
   acc=["**Rain plate** (separate PCB, `utility10/pcb/release/rainplate`): order **ENIG** finish and no mask over the comb; solder a 2-core outdoor cable (UV-resistant, up to 10 m) to the two pads and seal the solder joints and cable entry with silicone or hot-melt. Mount the plate tilted about 10 degrees so water drains. A TVS diode on the indoor unit protects against surge on the long cable.", "Connect to J3 on the indoor unit (DRV, SENSE)."],
   cal=["Wet threshold and 3 s debounce are firmware constants; check with tap water and with dew (a damp cloth should not trigger within 3 s)."],
   eol=["Wet the plate with a drop of water for 4 s: alert rings; dry the plate: the alert clears after 2 minutes.", "Mute button: rings stop for 30 minutes; check it rings again if still wet afterwards."],
   tr=[("Corrodes in monsoon", "check ENIG was ordered, plate not exposed to current continuously (the circuit pulses 5 ms)"), ("False alerts", "cable pickup: use twisted pair, shorter cable")]),
 "08-tap-litre-meter": dict(board="tap", name="tap_litre_meter", rel="utility10/pcb/release/tap", hex="boards/tap_litre.hex", clk="8MHz", pcs="3 x AAA", title="Tap Litre Meter",
   acc=["**Flow sensor.** Use a flow sensor with a lot calibration sheet (a Hall-effect turbine type, 3 wires: +, GND, signal into J3). Connect with hose barbs/G1/2 fittings; use thread tape. Pot or conformally coat the electronics module and keep the flow sensor, not the electronics, in the water path."],
   cal=["Pulses per litre (450 is a typical datasheet value) must be calibrated per sensor lot: run 10 L from a calibrated bucket, divide pulses by 10, enter in the setup (stored in EEPROM)."],
   eol=["Run 10 L from a calibrated bucket: reading 10 L +-0.2 L (adjust pulses/L).", "Stop flow for 5 s: the session ends; start again: a new session starts; set the target to 10 L: the buzzer rings at 10 L."],
   tr=[("Reads high/low", "calibration not done or flow rate outside the sensor range"), ("Leaks", "re-tape threads; never over-tighten plastic fittings")]),
}
ARD = {"1": "D3", "2": "D4", "9": "D5", "10": "D6", "11": "D7", "12": "D8", "13": "D9", "14": "D10", "15": "D11", "16": "D12", "17": "D13", "23": "A0", "24": "A1", "25": "A2", "26": "A3", "27": "A4", "28": "A5", "19": "A6", "22": "A7", "30": "D0", "31": "D1", "32": "D2"}
def pinmap(board):
    import importlib; sys.path.insert(0, os.path.join(ROOT, "utility10", "pcb"))
    B = importlib.import_module("boards." + board).BOARD; u = [p for p in B["parts"] if p["ref"] == "U1"][0]
    rows = ["| Arduino pin | ATmega pin | Net |", "|---|---|---|"]
    for k, v in sorted(u["nets"].items(), key=lambda kv: int(kv[0])):
        if k in ARD and v not in ("MOSI", "MISO", "SCK", "GND"): rows.append(f"| {ARD[k]} | {k} | {v} |")
    return "\n".join(rows)
def gen(slug, c):
    readme = rd(f"utility10/{slug}/README.md"); fl = readme.split("\n")[2] if readme else ""
    how = section(readme, "How it works"); ver = section(readme, "What I verified"); enc = [l for l in readme.splitlines() if l.startswith("Enclosure:")]
    comp = section(readme, "Compliance"); risks = section(readme, "Risks"); prod_b = section(readme, "Designed production BOM")
    bi = board_info(c["rel"], c["name"]) if c["rel"] and os.path.exists(os.path.join(ROOT, c["rel"], "README.md")) else None
    L = [f"# {c['title']}: manufacturing manual", "", "> **Status: design only.** Nothing here has been built or tested as hardware. This manual tells you exactly what to make, buy, assemble, program and test, and how to accept or reject a unit; expect to correct it after the first prototype run (5 units).", ""]
    L += [f"**Product summary.** {how}", "", f"**Product line / price in the plan:** {re.sub(r'\*+', '', fl)}", ""]
    L += ["## 1. What you are building: deliverables", "", "| Deliverable | Where | State |", "|---|---|---|"]
    if bi:
        r = bi["rdy"]; L += [f"| PCB: Gerbers, BOM, CPL, KiCad project | `{c['rel']}/` | **{'order-ready: every automatic check passes' if r['order_ready'] else 'NOT order-ready'}** (DRC errors {bi['ver']['drc_errors']}, netlist match {bi['ver']['netlist_match']}) |"]
    else: L += ["| PCB | `utility10/pcb/` (layout in progress) | **not released**: do not send to a fab |"]
    hexp = f"utility10/firmware/release/{c['clk']}/{c['hex']}"
    L += [f"| Firmware (`{c['hex']}`) | `{hexp}`, source `utility10/firmware/src/main_board.cpp` (seeti: `seeti_prod.cpp`), drivers `board_drivers.h`, engine `utility10/firmware/lib/utilcore.c` | engine host-tested (115 checks); board firmware compiles but is **not yet run on hardware** (see section 6) |", f"| Enclosure STL (prototype shell) | `utility10/{slug}/enclosure_body.stl`, `enclosure_lid.stl` and the board's `4_enclosure/` | prototype shell only |", f"| Mechanical / bought-in parts | section 3 | listed |", f"| Test sheet | `manuals/templates/eol_test_sheet.md` | template |", ""]
    if c.get("note"): L += [c["note"], ""]
    L += ["## 2. Before you start", "- Read `manuals/STANDARD_PROCEDURES.md` (sections A-F, J, K).", "- Tools: soldering iron, flux, multimeter, USBasp programmer + avrdude, calipers, 3D printer or print service, bench supply with current limit.", f"- Power source for this product: **{c['pcs']}**.", ""]
    L += ["## 3. Bill of materials", ""]
    if bi:
        L += [f"### 3a. Circuit board parts ({len([r for r in bi['bom'] if r['Value'] != 'TP'])} parts, {count_tp(bi['bom'])} test points)", "", "SMD parts marked `SMT (JLC)` are assembled by the fab from the JLC BOM; parts marked `hand/THT` are soldered by you. Every LCSC number was checked against an LCSC/JLCPCB listing on 2026-11-01; re-check stock on the day you order.", "", bom_table(bi["bom"]), ""]
    L += ["### 3b. Bought-in and mechanical items (estimates for about 2,000 units; replace with quotes)", "", prod_b or "See the product README.", ""]
    L += ["## 4. Step 1: fabricate the PCB", ""]
    if bi:
        L += [f"Upload `{c['rel']}/1_fabrication/{c['name']}_gerbers.zip` with the settings in STANDARD_PROCEDURES section A. Finish: " + ("**ENIG** for the rain plate, HASL lead-free for this board." if c["board"] == "rain" else "HASL lead-free."), f"Board size and layer list are in `{c['rel']}/README.md`.", ""]
    else: L += ["The PCB for this product is not released yet: see section 'Status of the PCB'.", ""]
    L += ["## 5. Step 2: assemble the board", "", "1. Order SMT assembly as in STANDARD_PROCEDURES section B (or hand-solder the SMD parts in section D order).", "2. Solder the through-hole parts listed `hand/THT` in 3a.", "3. Clean, inspect under magnification, and compare with `2_assembly/*_assembly_top.pdf`.", ""]
    L += ["## 6. Step 3: program the microcontroller", "", f"1. Connect a USBasp to the 6-pin ISP header J2 (pin 1 = square pad) with the board powered ({c['pcs']}).", f"2. Set fuses: `avrdude -p m328p -c usbasp -U lfuse:w:{FUSE[c['clk']][0]}:m -U hfuse:w:{FUSE[c['clk']][1]}:m -U efuse:w:{FUSE[c['clk']][2]}:m`  ({FUSE[c['clk']][3]}).", f"3. Flash and verify: `avrdude -p m328p -c usbasp -U flash:w:{hexp}:i` then `-U flash:v:{hexp}:i`.", "4. Remove the programmer, power-cycle the board, and confirm the start-up behaviour (section 9).", "", "If you change the supply type (for example USB instead of batteries) use the hex built for that clock (`4MHz` for 2 x AAA, `8MHz` for every other tool)."]
    L += ["", "Firmware pin map (generated from the PCB spec, so firmware and board agree):", "", pinmap(c["board"]), "", "**What is verified:** the control logic (`utilcore.c`) passes 115 host tests. **What is not:** the display, OLED, RTC and HX711 drivers and the button flows in `main_board.cpp` were written from datasheets and only compile-checked. Budget bring-up time for them on the first prototype.", ""]
    L += ["", "## 7. Step 4: electrical bring-up", ""]
    L += [section(bi["readme"], "Bring-up and test") if bi else "Not available until the PCB is released.", ""]
    L += ["## 8. Step 5: sensors, cables and mechanical assembly", ""] + [f"- {a}" for a in c["acc"]] + [""]
    L += ["## 9. Step 6: enclosure and final assembly", "", f"1. Print the shell (STANDARD_PROCEDURES section G). {enc[0] if enc else ''}", "2. Place the board on the standoffs (4 mm), fasten with M2.5 screws (6 mm), route cables through the cut-outs, close the lid.", "3. Label: serial number, rev, battery type/polarity, warnings.", "", "## 10. Step 7: calibration", ""] + [f"- {x}" for x in c["cal"]] + [""]
    L += ["## 11. Step 8: end-of-line functional test (every unit)", ""] + [f"{i+1}. {x}" for i, x in enumerate(c["eol"])] + ["", "Record results on `manuals/templates/eol_test_sheet.md`. Accept only if every line passes.", ""]
    L += ["## 12. Packaging, documents, compliance", "", "- In the box: unit, batteries or note on the required adapter, mounting accessories, quick-start card (`manuals/templates/quick_start_card.md`), warranty card.", "- Compliance items to verify before sale: " + (comp.replace("\n", " ") or "see STANDARD_PROCEDURES K") + ".", "- Labelling: STANDARD_PROCEDURES K.", ""]
    L += ["## 13. Troubleshooting (product specific)", "", "| Symptom | Cause / action |", "|---|---|"] + [f"| {a} | {b} |" for a, b in c["tr"]] + ["", "General issues: STANDARD_PROCEDURES section L.", ""]
    L += ["## 14. Known limits and risks", "", ver or "", "", risks or "", "", "Nothing in this manual replaces testing with real users, a design review by a PCB engineer, and the compliance checks above.", ""]
    if not bi: L += ["## Status of the PCB", "The board is still being routed or reviewed. When it passes all automatic checks its folder appears in `utility10/pcb/release/` and this manual is regenerated.", ""]
    p = os.path.join(ROOT, "utility10", slug, "MANUFACTURING_MANUAL.md"); open(p, "w").write("\n".join(L)); return p
if __name__ == "__main__":
    for s, c in T.items(): print(gen(s, c))
