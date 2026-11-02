"""Confidence ratings per project. Order confidence is computed from the automated review (costing/REVIEW_findings.json);
works-as-intended confidence is an evidence-based engineering judgement recorded here with its reasons. Run after review.py."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FIND = json.load(open(os.path.join(ROOT, "costing", "REVIEW_findings.json")))
SCALE = ["Low", "Low-Medium", "Medium", "Medium-High", "High"]
RUBRIC_ORDER = ("**High**: every LCSC part live-checked (identity, package, stock above 500, not end-of-life) and the Gerber/BOM/CPL files pass all automatic gates. "
                "**Medium-High**: same, but one or more parts have limited stock (still enough for a prototype run) or a substituted part whose pad geometry is unproven. "
                "**Medium**: parts depend on a vendor module, a hand-sourced item or a manual cross-check. **Low**: no board or no verified parts yet.")
RUBRIC_WORKS = ("An engineering judgement, **not a measurement**: nothing has been built. It weighs (a) how standard the circuit is (datasheet reference design versus novel), (b) the evidence we have (host-run firmware tests, simulation, pin-map checks, datasheet equations), "
                "(c) risks that only hardware can reveal (analog front ends, RF, power switching, mains, calibration, uncompiled firmware). **High** would need a built and tested unit, so no project is rated High. "
                "**Medium-High**: standard circuit, strong test evidence, low-risk failure modes. **Medium**: expect to find one or two issues in bring-up. **Low-Medium**: significant parts of the behaviour are assumed. **Low**: concept or software only.")
# key -> (works confidence, reasons, what to do first)
W = {
 "utility10/01-seeti-counter": ("Medium", "Mic front end and clap/whistle detector are analog and tuned on synthetic audio; the firmware itself passes 115 host checks; the documented limit is that quiet whistles are missed.", "Bench-test the microphone gain with real claps before ordering more than 5 boards."),
 "utility10/02-gas-taraju": ("Medium", "HX711 load-cell chain is a standard circuit; accuracy depends on the cell, mounting and calibration, which only a build can show.", "Calibrate with a known weight; check drift over a day."),
 "utility10/03-fridge-door-guard": ("Medium-High", "Reed switch, timer and buzzer: simple circuit, simple firmware; TVS and input conditioning follow standard practice.", "Test the reed gap and the 2-minute alarm on the bench."),
 "utility10/04-bijli-meter-reader": ("Medium", "Optical pulse reading of a meter LED depends on the sensor alignment and ambient light; circuit is standard.", "Try on a real meter with a shroud before enclosure work."),
 "utility10/05-bijli-log": ("Medium", "Current/voltage logging front end is analog and uncalibrated; mains-adjacent measurement needs isolation care.", "Do not connect to mains until a qualified electrician reviews the isolation; start with a bench supply."),
 "utility10/06-chulha-timers": ("Medium-High", "Multi-timer with buttons, LEDs and buzzer; simple circuit; firmware tested on the host.", "Check button debounce and the buzzer volume on the first board."),
 "utility10/07-rain-alert": ("Medium", "Conductive rain plate corrodes and drifts; electronics are simple and protected with TVS.", "Use the plate for a week outdoors before deciding on a coating."),
 "utility10/08-tap-litre-meter": ("Medium", "Hall/flow-pulse counting is standard; the litres-per-pulse constant depends on the flow sensor.", "Calibrate against a measured bucket."),
 "products/03-prayog": ("Medium-High", "Educational kit with a straightforward MCU board; 40 host checks on the statistics and command code.", "Run the kit's own experiments on the first unit."),
 "products/05-kheti-mitra": ("Medium", "Irrigation controller with 12 V switching and soil sensing; 22 host checks pass; field conditions (water, sun, surge) are the risk.", "Run with a lamp as the load for 48 hours before any valve or pump."),
 "toys10/01-reflex-raja": ("Medium-High", "Shares the Desi Arcade board; game logic tested with about 80,000 host checks.", "Play-test the buttons and the buzzer."),
 "toys10/02-taal-memory": ("Medium-High", "Same board and test base as Reflex Raja.", "Play-test the buttons and the buzzer."),
 "toys10/03-aloo-bomb": ("Medium-High", "Same board; game logic host-tested; the potato-clock mechanics are the unknown.", "Test timing with a real potato."),
 "toys10/04-beat-runner": ("Medium-High", "Rhythm game on its own board; logic host-tested; LEDs and buzzer circuits are standard.", "Check the LED brightness and button spacing."),
 "kinetic": ("Medium", "ESP32-S3 controller with three StepStick sockets and a 24 V to 5 V buck. Motion library (370 checks) and protocol are host-tested; the ESP32 firmware has never been compiled; drivers and motors are bought in. The vibration model is trained on synthetic data only.", "Power with a current-limited supply and no drivers; then one driver and one motor at low current."),
 "mitti-netra": ('Medium', 'Charger thermal pad now grounded with thermal vias; NTC window stops Li-ion charging outside about 6 to 44 C; power diodes corrected; IP65 box with a printed mounting plate; firmware core 23 checks and the pin map match; the cellular modem is a plug-in breakout and the ESP32 skeleton has never been compiled.', 'Bring up power and charging first (check TEMP voltage at room temperature), then the modem last.'),
 "biotray": ("Medium", "12 V low-side drivers, ESP32 and sensors; 22 host checks; calibration constants are placeholders; wet environment.", "Dummy loads on all outputs first; seal the enclosure before any water."),
 "biowatt": ("Low-Medium", "BQ25570 with megohm setting dividers computed from datasheet equations; cold start needs at least 600 mV (marginal for one microbial fuel cell); the hold capacitor is X7R where the datasheet asks for low leakage; leakage on a dirty board shifts the thresholds.", "Test with a bench supply at 0.8 V first, clean flux thoroughly, then try the fuel cell."),
 "geotech": ("Low-Medium", "Detector logic and feature code are host-tested (54 checks) but on synthetic vibration; the crack signature is an assumption; node hardware is the MITTI-NETRA board with a LoRa module.", "Record real vibration for a week and re-derive the thresholds before trusting any alarm."),
 "aquaponics": ("Low-Medium", "Control and forecasting core passes 13 checks; biological limits are placeholders; no ammonia or nitrite sensing; live animals depend on it.", "Run a week with water only; tune limits with an aquaculture expert before any fish."),
 "sorter": ("Low", "Tracking core passes 28 checks; the vision is a colour-rule baseline tested on synthetic discs; the gripper geometry is untested; machine guarding is your responsibility.", "Image real produce under fixed light and replace the classifier before building the conveyor."),
 "agrover": ("Low-Medium", "Navigation and power core pass 19 simulated-field checks; dead-reckoning only; chassis plates untested with real motors; needs a safety review and an emergency stop.", "Drive on blocks first, then slowly in a clear area with the stop in hand."),
 "jal-netra": ("Low-Medium", "Clamp-on ultrasonic transit-time measurement has a hard analog front end; the manual itself says Gate 1 acoustic test comes first and it is not sellable.", "Run the Gate 1 acoustic test with the evaluation setup before any more boards."),
 "astradand": ("Medium", "IMU gesture recognition validated against a Python reference (46/46) and on synthetic gestures; hardware (haptics, six addressable LEDs) is new; the LED part was replaced with a pin-compatible one whose pads are unproven.", "Order 2 boards, check the LED footprint fit, then run the gesture self-test."),
 "gravity-toys": ("Medium", "All five toys now have prototype drawings (Santulan lathe drawing, marble-tower posts and groove spec, ramp-racer car and ladder stand, Galton assembly guide, Drop Quest v1 rules with 60 solver-verified levels and laser parts); physics checks PASS; none built or play-tested.", "Cut or turn one of each and play-test; measure ramp times and marble behaviour."),
 "electronics-toys/wave1": ('Low-Medium', 'AP1 board added (ATmega328P, MP3 module socket, 4-digit display through two chained 74HC595s with a 7-LED ball lane, 7-button resistor ladder, lamp and motor drivers); all three apps now build for the board (about 6 kB each) and pass 76 host checks. The MP3 command codes are from memory and must be checked on the real module; the ladder thresholds are calculated, not measured.', 'Bench-test one board per product: ladder readings, MP3 commands, display multiplexing.'),
 "prototypes": ("Medium", "Bench prototype packs on breadboards with 26 host checks; no PCB.", "Use as learning kits; do not sell."),
 "dj-setup": ("Low", "Plan only; not manufacturable.", "Treat as a concept."),
 "utility10/09-masala-rack": ("Medium-High", "Laser-cut rack: fit depends on kerf; stability limit stated.", "Cut a kerf coupon first."),
 "utility10/10-laptop-stand": ("Medium-High", "Laser-cut stand: fit depends on kerf; stability limit stated.", "Cut a kerf coupon and load-test."),
 "products/01-desi-games": ("Medium", "Printed game; needs language and fact review before print.", "Proofread with native speakers."),
 "products/02-automata": ('Medium', 'Laser cut files regenerated with correct kerf compensation (outlines outward, holes inward, gear backlash only once); cam and gear checks PASS; frame layouts and figure artwork are still first-pass.', 'Cut one kit in scrap MDF and run the mechanism.'),
 "products/04-jal-rakshak": ('Medium', 'Low-voltage board reuses the Kheti-Mitra 12 V front end and pump driver; the firmware rules pass 20 simulated checks and an 8 MHz PCB build exists (3.2 kB); real probes, water, pump currents untested; the mains version is still out of scope.', 'Bench test with a 12 V pump and probes in a bucket; never connect mains.'),
 "products/06-gas-suraksha": ('Low-Medium', 'Prototype/logging board carries the tested alarm engine (34 checks) with an active buzzer and a UART log header; MQ-6 thresholds are placeholders and it is not a certified detector.', 'Log real sensor data for a week; never use or sell as a safety device.'),
 "toys10/05-rangoli-spiro": ("Medium-High", "Laser-cut gears; kerf test first.", "Cut a kerf coupon."),
 "toys10/06-paper-rocket": ("Medium", "v1 changed to a stomp launcher (no pump, valve or stored pressure); laser-cut stand and parts list exist; range and energy are model estimates until measured.", "Build one, fire 20 rockets in an open area and measure the range; keep foam noses mandatory."),
 "toys10/07-tilt-maze": ("Medium", "Gimbal now drawn (two sheets, kerf-compensated, tilt and clearance checks PASS) but never cut; dowel fits and knob feel need a test.", "Cut one set in scrap MDF and test the tilt range and axle fits."),
 "toys10/08-band-racer": ("Medium-High", "Cut file now kerf-compensated (wheels, axle holes, band slots at nominal size); simple mechanism.", "Cut one in cardboard or MDF and test the band drive."),
 "toys10/09-marble-cricket": ("Medium", "Cut file now kerf-compensated (peg holes at 6.2 mm press fit); pocket scoring needs a calibration drop.", "Cut one, drop 200 marbles and check the pocket distribution."),
 "toys10/10-katha-cubes": ("Medium-High", "Cube net and the 36 words ready; Hindi and Telugu checked for consistency (grandmother term aligned, gender-neutral problem phrases) but a native-speaker review is still required before print; icons are optional for the prototype.", "Print text-only cubes for the prototype; get the words reviewed by native speakers before the production print."),
}
NOBOARD_ORDER = {"Medium-High": "No parts at risk: local laser-cutting or printing, no part numbers.", "Medium": "Local fabrication or module-based; quote before ordering.", "Low": "Nothing orderable yet."}
def order_conf(board, path, works):
    if board is None:
        if works == "Low" and path in ("electronics-toys/wave1", "dj-setup", "products/04-jal-rakshak", "products/06-gas-suraksha"): return "Low", "no board and no verified part list yet"
        if path in ("geotech", "aquaponics", "sorter", "agrover"): return "Medium", "uses other boards plus bought-in modules; each module's pinout must be checked against its datasheet"
        if path in ("prototypes",): return "Medium", "breadboard parts from local vendors"
        return "Medium-High", "no electronic parts to source: local laser-cutting or printing"
    F = FIND.get(board, [])
    errs = [f for f in F if f[0] == "error"]; warns = [f for f in F if f[0] == "warn"]
    if errs: return "Low", "; ".join(f[2] for f in errs)[:140]
    if not warns: return "High", "all parts live-checked, none flagged"
    import re
    items = []
    for w in warns:
        m = re.match(r"^(\w+) (C\d+) (.*?): low stock (\d+)", w[2])
        if m: items.append(f"{m.group(1)} {m.group(3)} (stock {m.group(4)})")
    why = "; ".join(items)[:170]
    if board in ("astradand",): return "Medium", "substitute addressable LED whose pad geometry is unproven; other parts verified"
    if board in ("biowatt",): return "Medium-High", "all parts verified; the BQ25570 stock is limited (about 400) and the hold capacitor is a substitute grade"
    return "Medium-High", "limited stock on: " + why
def table():
    src = open(os.path.join(ROOT, "manuals", "gen_index.py")).read(); ns = {}; exec(src[src.index("ROWS = ["):src.index("L = [")], ns)
    out = []
    for grp, rows in ns["ROWS"]:
        for name, path, board, cav in rows:
            w = W.get(path); 
            if not w: continue
            oc, ow = order_conf(board, path, w[0]); out.append(dict(group=grp, name=name, path=path, board=board, order=oc, order_why=ow, works=w[0], works_why=w[1], first=w[2]))
    return out
if __name__ == "__main__":
    t = table(); L = ["# Confidence ratings (ordering and works-as-intended)", "", "Two columns for every project. They answer different questions:", "", "- **Order confidence:** how sure we are that you can buy exactly these parts and files and get what the BOM says. " + RUBRIC_ORDER, "- **Works-as-intended confidence:** how sure we are that the design does its job when built. " + RUBRIC_WORKS, "",
        "**Plan for one respin.** Even a clean design review usually leaves one or two bring-up findings on a first board; order the small quantity first (5 boards) and keep the files in this repository as the single source of truth.", "", "| Project | Order confidence | Works-as-intended | Why (works) | First thing to do |", "|---|---|---|---|---|"]
    for r in t: L.append(f"| {r['name']} | **{r['order']}** ({r['order_why']}) | **{r['works']}** | {r['works_why']} | {r['first']} |")
    open(os.path.join(ROOT, "costing", "CONFIDENCE.md"), "w").write("\n".join(L) + "\n"); json.dump(t, open(os.path.join(ROOT, "costing", "confidence.json"), "w"), indent=1); print(len(t), "projects rated")
