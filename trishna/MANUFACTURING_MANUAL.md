# TRISHNA - reagentless urinal hydration and biomarker monitor: build manual

> **What this is.** A bench-buildable prototype that catches a 2 mL mid-stream sample from a male urinal and measures it **without chemical consumables**: conductivity (EC), temperature, 450 nm absorbance (urine colour / urochrome) and 850 nm turbidity. From these it estimates specific gravity (SG) and a hydration class, and tracks electrolyte trends. It then backwashes itself with tap water.
>
> **What this is not.** It is not a medical device and does not diagnose anything. The SG figure is an **estimate from conductivity and colour**. It becomes useful only after you calibrate it against a handheld urine refractometer (section 9.4). Even then, treat it as a personal trend, not a lab value. A version sold with health claims would be a medical device under India's Medical Device Rules 2017 (CDSCO). Keep the data local: urine data is sensitive personal data under the DPDP Act 2023.
>
> **Status.**
> - **Controller PCB: order-ready.** DRC 0, 0 unconnected, netlist matches the schematic, ERC 0, independent Gerber check clean, all 88 parts LCSC-verified. Parts about US$9.2 per board for 1 board, US$6.5 each for 100 (PCB fab, assembly and shipping extra). Low stock on the run date: AP63203WU-7 (195) and the PJ-063AH barrel jack (321) - enough for a prototype run; order early.
> - **Firmware:** compiled for the ESP32 (842 kB, no warnings in project code); 19 host unit tests passing.
> - **Bridge:** Python decoder cross-checked against the C frame format.
> - **CAD:** solids checked (2.02 mL wetted chamber, all meshes closed).
> - **Nothing has been built yet.** Sections 8-10 are the build and test procedure.

| Folder | Contents |
|---|---|
| `utility10/pcb/boards/trishna.py` | controller PCB definition (source of truth for the circuit) |
| `utility10/pcb/release/trishna/` + `hardware/` | order-ready PCB release: Gerbers, JLC BOM + CPL, schematic PDF, assembly drawing, STEP |
| `docs/PINOUT_AND_NETLIST.md` | generated pin map, full net list, board BOM (checked against the firmware pin map) |
| `firmware/` | PlatformIO project: `lib/trishna_core` (portable C: frame, filters, EC/optics maths, state machine), `src/` (ESP32 HAL, app, telemetry, console), `test/` |
| `tools/` | `trishna_bridge.py` (UART/SD log -> JSON/CSV/MQTT/ThingsBoard), `trishna_fit_sg.py`, `trishna_trends.py`, `test_bridge.py`, `gen_netlist_doc.py` |
| `mechanical/` | `trishna_cad.py` (parametric CAD), `out/*.stl` + `cad_report.json` + previews, `drawings.py` |
| `docs/drawings/` | plumbing schematic, wall elevation, cable harness, sensor-block drawing (PNG + SVG) |

---

## 1. System specification and logical flow

### 1.1 Measured quantities
| Quantity | How | Range / resolution | Notes |
|---|---|---|---|
| Conductivity EC25 | 2 titanium pins, bipolar 1.6 kHz ratiometric drive, 2-point KCl calibration, temperature-compensated to 25 C (alpha 0.0191 /C) | 0.5-60 mS/cm; about 0.5 % repeatability expected | urine is typically 5-35 mS/cm; tap-water rinse 0.1-1 mS/cm |
| Temperature | DS18B20 stainless probe in the chamber | -10..85 C, 0.0625 C | used for EC compensation |
| Absorbance A450 | 450 nm LED -> 12 mm path -> photodiode, against the rinse-water blank of the same event | 0-2 AU | urochrome colour; a hydration cue |
| Turbidity index | 850 nm transmitted + 90-degree scatter, ratio method, blank subtracted | relative units (0-1) | cloudiness trend; not calibrated NTU |
| SG estimate | `SG = 1 + c_ec*EC25 + c_a450*A450 + c0` | 1.000-1.040 | defaults are population-typical; **fit to your refractometer** |
| Hydration class | SG bands: < 1.010 well hydrated, 1.010-1.020 adequate, 1.021-1.030 low, > 1.030 dehydrated | 4 classes | only reported when sample quality >= 50 |

### 1.2 Event sequence (firmware state machine)
| State | Entered when | Actuators | Measurement | Leaves when |
|---|---|---|---|---|
| `STATE_IDLE` | boot, end of lockout | all off | sump/leak probes every 50 ms, ToF continuous, 12 V every 1 s; slow sump baseline learning | ToF presence AND sump stream signature for 300 ms; or presence 4 s with liquid in the sump (fallback, flagged) |
| `STATE_STREAM_DETECTED` | stream detected | all off | **blank**: EC + optics of the rinse water already in the chamber; start temperature conversion | after **2.0 s** (initial flush/dilution passes the sump) -> SAMPLING; stream gone for 0.5 s -> IDLE ("short event") |
| `STATE_SAMPLING` | delay done | pump **forward** 100 % | live EC 4 Hz (median-5 + EMA tau 0.75 s), LIVE frame 1 Hz | after `sample_ml / flow` (default 6 mL = 3 chamber volumes, 6 s) |
| `STATE_ANALYSIS` | pumping done | all off | EC every 200 ms into a settle detector (8-sample window, rel. SD <= 1 % for 3 updates, at least 2 s); then temperature and optics (5 repeats, median) | result computed (2-9 s) or 15 s timeout |
| `STATE_PURGE_CLEANING` | analysis done | 2 x [valve **open** + pump **reverse** 8 mL, then 0.5 s pause]; then a check | chamber must hold rinse water (EC cell not open); that water is the next event's blank | check done -> LOCKOUT (air = reservoir empty: fault, retried every 10 min) |
| `STATE_LOCKOUT` | after every event, or a fault | all off | none | 30 s elapsed and no fault; a leak latches until `clear` |

Hard limits in every state: pump never on for more than 30 s, valve never open for more than 30 s, and a leak shuts everything off. A task watchdog (8 s) resets the MCU if the loop stalls; all outputs start low.

### 1.3 Why the design differs from the brief in four places
1. **Pump driver = H-bridge (DRV8871), not a single MOSFET.** A single low-side N-MOSFET can only turn a DC motor on in one direction. The backwash needs the pump **reversed**, which needs a bridge. The DRV8871's own MOSFET body diodes clamp the motor's back-EMF, and its 47 k ILIM sets a current limit of about 1.4 A. A diode across a reversible motor would short the supply in one direction, so there must not be one.
2. **Solenoid MOSFET = AO3400A (SOT-23), not IRLZ44N.** The ESP32 drives the gate with 3.3 V. The IRLZ44N is only specified from 4-5 V gate drive. The AO3400A is specified at 2.5 V (about 0.05 ohm), carries 5.7 A, and is assembled by JLCPCB. The **mandatory flyback diode is kept**: M7 = SMD 1N4007 (1 A, 1000 V) across the coil.
3. **Fresh water comes from an open reservoir, not a mains tap.** The rinse line is next to a drain carrying urine. Connecting it to drinking-water plumbing would need a certified backflow preventer. A gravity reservoir with an air gap avoids the cross-connection completely. The solenoid must therefore be a **direct-acting, zero-minimum-pressure** valve: RO-type pilot valves need 0.02 MPa and will not open.
4. **"Exactly 2 mL" comes from the chamber volume, not the pump dose.** A peristaltic pump's volume per second drifts with tube wear. The chamber is a fixed 2.0 mL flow-through cell. The pump pushes 3 chamber volumes through it so the previous rinse water is displaced (about 95 %), then stops. The 2 mL measured is whatever fills the cell.

---

## 2. Electronics

### 2.1 Block description (controller PCB, 120 x 84 mm, 2 layers)
- **Power input:** a 12 V 2 A adapter (5.5/2.1 mm plug, centre positive) feeds barrel jack J1. From there: 2 A PTC fuse F1 (R+O SMD1812-200-16), then SMBJ15A TVS D3 to GND, then an **AO3401A reverse-polarity P-MOSFET** Q5 (12 V Zener D4 clamps Vgs, 10 k R40 pulls the gate down), giving the rail **VM**. Bulk: 100 uF/35 V (C30), 10 uF/50 V X5R 1210 (C31).
- **3.3 V buck:** AP63203WU-7 (U2, fixed 3.3 V, 2 A, 1.1 MHz). VIN = VM with 10 uF/50 V; EN through 100 k to VM (always on). BST 100 nF (C32), 4.7 uH inductor L1 (FNR5040S), 2 x 22 uF/10 V X5R at the output. The BST and SW nodes are hand pre-routed short and wide.
- **Analog rail:** +3V3, then ferrite bead FB1 (BLM18AG601, 600 ohm at 100 MHz), giving **+3V3A**, with 10 uF + 100 nF. It powers only the MCP6002 TIAs.
- **12 V monitor:** VM, 100 k / 10 k divider, GPIO35 (100 nF filter). The firmware multiplies by 11 and reports supply low (< 10.5 V) or high (> 14 V).
- **ESP32-DevKitC-32E** plugs into two 1x19 female sockets (J4, J5, 25.4 mm apart). It is fed through **JP1** (2-pin link) into its 3V3 pin, with 10 uF + 100 nF there. **Rule: remove JP1 before plugging USB into the DevKit**, because two supplies must never drive 3V3 at once (section 8.4).
- **Pump:** DRV8871DDAR (U3), VM with 100 uF + 10 uF + 100 nF, ILIM 47 k (about 1.4 A trip). IN1 = GPIO13, IN2 = GPIO12, PWM 20 kHz. Outputs go to J6.
- **Solenoid:** AO3400A Q1. Gate from GPIO2 through 100 R (R63), 100 k pull-down (R64). Drain to J7 pin 2; J7 pin 1 = VM. M7 (1N4007) D10 across the coil (cathode to VM).
- **Optics:**
  - LED drives: Q2 (blue) and Q3 (IR) are AO3400A low-side switches with the same 100 R / 100 k gate network. Anodes are fed from VM through 1 k / 1206 / 0.25 W (R67, R70): about 9 mA blue, 10.5 mA IR.
  - Photodiode front end: MCP6002 (U4) runs as two transimpedance amplifiers in zero-bias photovoltaic mode: cathode to the inverting input, anode and non-inverting input to GND.
    - Transmission: Rf 10 k, Cf 10 nF.
    - Scatter: Rf 1 M, Cf 1 nF.
    - Each output feeds the ADC through 1 k / 10 nF.
- **EC cell:** GPIO25, then R75 330 R, then electrode E1 (net EC_N1). Electrode E2 (EC_E2) goes through R76 100 R to GPIO26. EC_N1 also feeds GPIO36 through 100 R / 1 nF.
- **Sump and leak probes:** GPIO27 (LVL_DRV) feeds 4.7 k to SUMP_P (J11) and 47 k to LEAK_P (J12). Each node goes to its ADC (GPIO32, GPIO33) through 1 k / 1 nF; the far probe pin is GND. LVL_DRV is pulsed for about 200 us only while read: average DC under 3 uA.
- **Digital:** DS18B20 on GPIO4 (4.7 k pull-up, J13). VL53L1X on I2C GPIO21/22 (4.7 k pull-ups, J14). Telemetry UART2 TX GPIO17 / RX GPIO16 to J15. microSD Molex 104031-0811 (J16) on SPI GPIO18/19/23, CS GPIO5, with 10 k pull-ups on CS, MISO, DAT1 and DAT2, and 10 uF + 100 nF.
- **Test points:** TP1 VM, TP2 +3V3, TP3 +3V3A, TP4 GND. Green LED D6 = 3.3 V present.

### 2.2 EC measurement principle (why GPIOs can drive the cell directly)
Phase A: GPIO25 high, GPIO26 low, so V_A = Vdd (Rc + Rb) / Rt. Phase B: the reverse, so V_B = Vdd (Rref + Ra) / Rt. The ratio **q = V_A / V_B = (Rc + Rb) / (Rref + Ra)** does not depend on the 3.3 V level or the high-side pin resistance. Ra and Rb (pin resistances plus R76) are absorbed by the two-point calibration, which fits the cell constant K and Rb.

The drive is a balanced square wave (equal time in each polarity) and both pins rest low. No net DC flows through the sample, so there is no electrolysis and no plating of the electrodes. With the design cell (two 1.0 mm titanium pins 7 mm apart, 4 mm exposed, K about 2.6 /cm), urine at 5-35 mS/cm puts V_A and V_B between 0.4 V and 2.4 V. That is the accurate part of the ESP32 ADC's 11 dB range.

### 2.3 Pinout, net list and BOM
See **`docs/PINOUT_AND_NETLIST.md`**, generated from the board file:
- every DevKit pin with its net and role
- the complete net list as copy-ready `NET: REF.pin, ...` lines (56 nets)
- the grouped BOM with every LCSC number (88 parts)

The KiCad files in `utility10/pcb/release/trishna/3_design/` (schematic, PCB, `.net`) are the authoritative design and open directly in KiCad 7+.

Key decoupling, by rail:
- VM: 2 x 100 uF/35 V + 2 x 10 uF/50 V + 100 nF
- 3V3: 2 x 22 uF at the buck, plus 10 uF + 100 nF at the DevKit and at the microSD
- 3V3A: 10 uF + 100 nF
- op-amp: 100 nF
- every ADC input has its own RC filter

---

## 3. Firmware

### 3.1 Build, flash, test
```
cd trishna/firmware
pio run -e esp32dev                 # build (espressif32 6.9.0 = Arduino-ESP32 2.0.17)
pio run -e esp32dev -t upload       # flash over the DevKit USB (JP1 removed, 12 V off - section 8.4)
pio device monitor -b 115200        # console: type help
pio test -e native                  # core unit tests on the PC
make -C test/host                   # same tests without PlatformIO (plain gcc)
tools/arduino_build.sh              # alternative build with arduino-cli (same core)
```
Libraries (pulled by PlatformIO): OneWire, DallasTemperature, Pololu VL53L1X. Flash: about 842 kB of 1.3 MB; RAM: 47 kB.

### 3.2 Structure
| File | Role |
|---|---|
| `lib/trishna_core/src/trishna_frame.*` | 48-byte frame: packed struct (static size check), explicit little-endian serialiser, CRC-16/CCITT-FALSE, parser |
| `lib/trishna_core/src/trishna_filters.*` | moving average + window SD, first-order IIR (EMA), median-of-5 / median-of-N, settle detector |
| `lib/trishna_core/src/trishna_sense.*` | EC ratio, cell resistance, conductivity, 25 C compensation, 2-point calibration, air detection; absorbance; turbidity; SG model; hydration class; quality score |
| `lib/trishna_core/src/trishna_fsm.*` | state machine (`STATE_IDLE` ... `STATE_LOCKOUT`), pure logic with time as an input; actuator limits; faults |
| `src/board_pins.h` | pin map (checked against the PCB by `tools/gen_netlist_doc.py`) |
| `src/hal.*` | ADC (eFuse-calibrated mV), bipolar EC drive, probe pulses, optics sequence, DRV8871 PWM, valve, DS18B20 (non-blocking), VL53L1X |
| `src/telemetry.*` | FreeRTOS queue (32 frames) + task on core 0: UART2 binary stream and append to `/trishna.bin` on the microSD card; never blocks the control loop |
| `src/app.*` | inputs -> FSM -> outputs, the requested measurements, frame building, heartbeat (60 s) |
| `src/console.*` | USB console: status, raw, event, purge, clear, prime, valve, cal ec1/ec2/solve, cal flow, cal sg, set, wifi, save |
| `src/settings.*` | NVS storage (calibration, timings, thresholds, event counter) |

### 3.3 Signal filtering
- **During sampling** (pump running, liquid moving): EC is measured every 250 ms (8 bipolar cycles), passed through a **median-of-5** (removes bubble spikes), then an **EMA with tau = 0.75 s** (smooths sloshing). It is published as LIVE frames at 1 Hz, so you can watch the fill.
- **During analysis** (pump stopped): every 200 ms, 32 bipolar cycles are averaged into one ratio and fed to the **settle detector**: an 8-sample moving window, done when its relative standard deviation stays <= 1 % for 3 consecutive updates and at least 2 s have passed. This waits out the kinetic sloshing after the pump stops instead of using a fixed delay. A 9 s cap guarantees progress.
- **Optics:** dark / blue / IR readings are each 32 ADC samples, taken after 25 ms settling (more than 20 TIA time constants), repeated 5 times; the median is used.

### 3.4 The 48-byte frame
The full layout with offsets is in `trishna_frame.h`. Summary: preamble `A5 5A`, version, type (1 result, 2 state transition, 3 error, 4 heartbeat, 5 calibration, 6 live), sequence, UTC seconds + ms (0 when unsynced), uptime, state + previous state, event id, 16 flag bits, error code, temperature x100, EC25 x100, cell ohm, SG x10000, A450 x1000, turbidity x1000, three photodiode mV, supply mV, hydration class, quality 0-100, CRC-16.

The receiver resynchronises on the preamble and drops anything with a bad CRC (tested in `tools/test_bridge.py` with noise, a corrupted frame and a false preamble). Time stamps are real UTC once Wi-Fi credentials are stored (`wifi <ssid> <pass>`, `save`, `reboot`); the device uses Wi-Fi only for SNTP.

### 3.5 Local server sandbox
```
pip install pyserial paho-mqtt
python3 tools/trishna_bridge.py --port /dev/ttyUSB0 --csv trishna.csv                                  # JSON lines + CSV
python3 tools/trishna_bridge.py --port /dev/ttyUSB0 --mqtt-host 127.0.0.1                             # Mosquitto: trishna/trishna-01/<type>
python3 tools/trishna_bridge.py --port /dev/ttyUSB0 --mqtt-host <tb-host> --tb-token <DEVICE_TOKEN>   # ThingsBoard telemetry
python3 tools/trishna_bridge.py --replay /media/sd/trishna.bin --csv trishna.csv                      # offline, from the SD log
python3 tools/trishna_trends.py trishna.csv                                                            # daily SG / EC25 / electrolyte z-score
```
J15 pinout: 1 GND, 2 TX (ESP32 out, goes to the adapter's RX), 3 RX (ESP32 in, from the adapter's TX). Use a 3.3 V USB-serial adapter (CP2102 / CH340) and **do not connect its 5 V pin**.

---

## 4. Mechanical design

### 4.1 Architecture
Two separate printed boxes on the wall:
- **Chamber A (electronics):** about 105 x 141 x 39 mm. It hangs **40 mm above** chamber B.
- **Chamber B (fluidics):** about 175 x 155 x 78 mm.

Water from a leak in B can only run down and away. Nothing in B can drip into A, because the cables enter A from below through glands, and every gland and port faces down. The 40 mm air gap is a drip break. Each box closes with its own lid, compressing a 2.5 mm solid silicone cord in a groove (about 25 % squeeze), held by M3 screws into brass heat-set inserts in lugs **outside** the gasket line. A screw hole never crosses the seal. Target: splash-proof (IP54-like), not immersion.

### 4.2 Parts to print (all PETG unless noted; STL in `mechanical/out/`)
| Part | Size (mm) | Settings | Qty |
|---|---|---|---|
| `trishna_sensor_block` | 36 x 36 x 38 | **black** PETG (light-tight), 0.15 mm layers, **100 % infill**, 5 perimeters, 240-245 C, outer walls 30 mm/s, flow 1.03-1.05. Print upright (bore vertical). Must be pore-free: it holds liquid under pump pressure | 1 (+1 spare) |
| `trishna_chamberA_base` / `_lid` | 137 x 154.5 x 39 / 124 x 160 x 4.5 | 0.2 mm, 4 perimeters (>= 1.6 mm walls), 6 top/bottom, 30 % gyroid; base printed back-face down, lid groove up | 1 each |
| `trishna_chamberB_base` / `_lid` | 207 x 168.5 x 78 / 194 x 174 x 4.5 | as chamber A; needs a 210 x 210 mm bed or better | 1 each |
| `trishna_sump_insert` | 70 dia x 28 | 0.15 mm, 100 % infill; set the drain diameter in `sump_insert(d_drain=...)` first | 1 |
| `trishna_pump_bracket` | 60 x 60 x 40 | 0.2 mm, 40 % infill | 1 |
| `trishna_valve_saddle` | 40 x 44 x 12 | 0.2 mm, 40 % infill | 1 |
| `trishna_port_retainer` | 12 x 18 x 3 | black, 100 % | 5 |
Total filament about 600 g (buy 1 kg black PETG). Regenerate after any change: `/path/to/python mechanical/trishna_cad.py` (needs `manifold3d trimesh numpy`), then `render.py` and `drawings.py`.

### 4.3 Sensor block (the 2 mL flow cell)
See `docs/drawings/sensor_block_drawing.png` and `mechanical/out/trishna_sensor_block_sections.png`.
- **Bore:** 12.0 mm diameter x 17.0 mm (z 10-27), with 2 mm conical transitions to 3 mm channels at both ends. Geometric volume 2.117 mL; **wetted volume 2.018 mL** with the temperature probe inserted, computed from the solid model.
- **Inlet:** at the **bottom**, outlet at the **top** (M5 x 0.8 tapped, 6 mm deep, for M5 to 4 mm hose-barb fittings in PP or nylon). Upward flow pushes air out of the top, so the cell fills completely.
- **Optical path:** 12 mm across the bore.
  - +X face: two 5 mm LEDs (450 nm at z 13, 850 nm at z 23). Each port is tilted 22.6 degrees so it aims at the transmission photodiode on the -X face (z 18).
  - +Y face: the 90-degree scatter photodiode (z 20.5), where the IR beam crosses the axis. It shares the +Y wall with the metal parts, so it looks at the plain black -Y wall and never at a reflection.
- **Temperature:** DS18B20 6 mm probe through +Y at z 11.5 (O-ring 6 x 1.5), tip 2 mm past the bore axis.
- **Electrodes:** two 1.0 mm titanium Gr 2 pins through +Y at z 25.5, x +/- 3.5, protruding 4 mm into the bore.
- **Mounting:** 4 x M3 x 45 through the corners onto the chamber-B shelf (28 x 28 mm square).
- **Port seals:** every optical port is a 5.1 mm through-hole plus a 7.2 mm counterbore for a 5 x 1 mm O-ring under the component's flange. A printed retainer covers it, and the back is potted with black RTV (light-tight, splash-proof).

### 4.4 Chamber layout (box coordinates: X along the wall, Y up, Z out of the wall)
- **Chamber A**
  - Inside: 100 x 136 x 36. The PCB sits on 4 x 6 mm standoffs (M3 inserts) with its x axis vertical and the barrel jack pointing **down**.
  - Bottom wall: jack hole 10.4 mm at X 22. G1 M16 at X 46, G2 M16 at X 70, G3 M12 at X 91.
  - Left wall: M12 glands G4-G7 at Y 30 / 55 / 80 / 105.
- **Chamber B**
  - Inside: 170 x 150 x 75.
  - Floor: a 4 mm V that falls to the centre drain (P4, X 85). The leak probe is two M3 stainless screws at X 73 and X 97.
  - Sensor shelf (top face Y 32) holds the block at X 85, Z 36. Its probe side faces +X and its LED side faces the lid.
  - Pump bracket bosses at (20 / 70, 75 / 125) and valve saddle bosses at (125 / 155, 100 / 135), all with M3 inserts.
  - 5 cable-tie anchors for the tubes.
  - Bottom wall: P1 sample in (X 40), P2 waste out (X 62), P3 fresh water in (X 128), all M12 glands on the tubes.
  - Top wall: G1-G4 to chamber A (X 55, 80, 102, 122).
- **Sump insert:** a 70 mm disc with 10 drain holes and a 30 mm cup, 2 mm floor, overflow notch at 18 mm (**11.3 mL** held). Side M5 port 5 mm above the floor to the sample tube; two titanium stream-probe pins 10 mm apart, 9 mm up the cup wall; three 6 mm feet.

### 4.5 Plumbing
See `docs/drawings/plumbing_schematic.png` (flow directions per state) and `docs/drawings/wall_elevation.png` (heights).

| Tube | From -> to | Size | Length (target) |
|---|---|---|---|
| T1 | sump insert M5 barb -> P1 gland -> pump inlet | 3 x 5 mm silicone | as short as the install allows (<= 1.2 m) |
| T2 | pump outlet -> sensor block bottom (M5 barb) | 3 x 5 mm | <= 15 cm |
| T3 | sensor block top (M5 barb) -> tee | 3 x 5 mm | <= 15 cm |
| T4 | tee -> check valve (flow away from the block) -> P2 gland -> urinal bowl, ending 2 cm above the drain | 3 x 5 mm / 4 x 6 mm | as needed, falling all the way |
| T5 | reservoir bulkhead -> P3 gland -> solenoid inlet; solenoid outlet -> tee | 4 x 6 mm (reducers to the valve's barbs) | as needed |
| P4 | chamber-B drain -> into T4 below the check valve, or its own tube to the bowl | 4 x 6 mm | as needed |

Rules:
1. The pump tube that sits in the pump head is the pump's own tube; replace it every 6 months.
2. All barbs are 4 mm aquarium size; 3 x 5 mm silicone is stretched onto them, which seals without clips at these pressures. Add a small cable tie on the pump outlet and on both block barbs.
3. The **check valve** goes on the waste side of the tee, arrow pointing away from the block. Without it, the reversed pump pulls waste back into the chamber.
4. The reservoir outlet must be at least 300 mm above chamber B, with the tube falling continuously (no loops where air can sit), and the reservoir open to air. Fill it with **tap water**, not RO or distilled: the chamber-full check needs at least 0.1 mS/cm.
5. T4 ends in the bowl above the drain. Never connect it into a closed drain pipe, which would siphon or back-pressure the check valve.

---

## 5. Bill of materials

### 5.1 PCB
88 parts on the JLCPCB assembly, all LCSC-verified. See `utility10/pcb/release/trishna/2_assembly/` and the priced list `costing/trishna_priced_BOM.csv`. Through-hole parts are hand-soldered (sockets, JST connectors, JP1, barrel jack); the ordering guide lists them.

### 5.2 Bought-in items (India sources; prices are rough guides, check before ordering)
| Item | Qty | Spec / example | Where | Approx. INR |
|---|---|---|---|---|
| ESP32-DevKitC-32E | 1 | **38-pin, 1.0 in (25.4 mm) row spacing**, WROOM-32E or 32D (not WROVER: GPIO16/17 are used). 30-pin DOIT boards do not fit | element14 India, Robu.in | 900-1,100 (clones 450) |
| 12 V DC adapter | 1 | 12 V 2 A, 5.5 x 2.1 mm, centre positive, BIS-marked | local, Amazon.in | 300-450 |
| Peristaltic pump | 1 | 12 V DC, about 0.2-0.4 A, 3 x 5 mm tube, 40-100 mL/min (e.g. Kamoer NKP-DC-S10B, or generic "12V DC dosing pump") | Robu.in, Amazon.in | 450-2,500 |
| Solenoid valve | 1 | 12 V DC **normally closed, direct-acting, 0 MPa minimum**, <= 6 W, 1/8 in or 6-8 mm barbs, food-grade body (water-dispenser / coffee-machine type). **Not** an RO pilot valve | Amazon.in, Robu.in | 250-600 |
| VL53L1X ToF breakout | 1 | 3.3 V, I2C (Pololu #3415 or CJMCU-531) | Robu.in, Robocraze | 600-900 |
| DS18B20 waterproof probe | 1 | 6 x 50 mm stainless sheath, 1 m 3-wire cable | Robu.in | 120-200 |
| Photodiodes | 2 (+1) | **OSRAM SFH 203** (5 mm clear, 400-1100 nm, +/- 75 deg); SFH 203 P also fits | element14 India, Mouser India | 60-90 each |
| LED 450 nm | 1 (+1) | 5 mm water-clear blue, 30 deg or wider | local, Robu.in | 10 |
| LED 850 nm | 1 (+1) | 5 mm IR, 850 nm, 30 deg or wider (e.g. Vishay TSHG6200, or generic 850 nm) | element14, Robu.in | 15-60 |
| Titanium wire | 30 cm | Grade 2, 1.0 mm | Amazon.in (anodising / jewellery wire) | 300-500 |
| Silicone tubing | 2 m + 2 m | food-grade 3 x 5 mm and 4 x 6 mm | Amazon.in, aquarium shops | 150 each |
| M5 to 4 mm hose-barb fittings | 6 | **PP or nylon** (no plain brass in urine), M5 x 0.8 male | Amazon.in, pneumatics shops | 40 each |
| Check valve | 2 | 4 mm aquarium duckbill (one spare) | aquarium shops | 30 each |
| Tee 4 mm | 2 | aquarium PP tee | aquarium shops | 20 each |
| Reducers | 2 | 6-8 mm to 4 mm barb (valve to tubing) | aquarium / Amazon.in | 30 each |
| Cable glands | 4 x M16 + 10 x M12 | nylon, IP68, M16 x 1.5 (4-8 mm) / M12 x 1.5 (3-6.5 mm) | Robu.in, local electrical | kit 300 |
| O-rings | 4 x 5 x 1, 1 x 6 x 1.5 | NBR or silicone | metric O-ring kit (Amazon.in) | 250 |
| Silicone cord | 1.5 m | 2.5 mm solid | Amazon.in | 200 |
| Heat-set inserts | 40 | M3 x 5.7 for 4.0 mm holes | Robu.in | 250 |
| Screws | - | 22 x M3 x 8 (lids), 4 x M3 x 6 (PCB), 8 x M3 x 8 (brackets), 4 x M3 x 45 + nuts (block), 2 x M3 x 10 A2 stainless + 2 ring terminals (leak probe), 10 x M2 x 6 self-tapping (retainers), 8 wall screws + plugs | hardware shop | 300 |
| Cables | - | 1 m 4-core 0.5 mm2; 1 m 8-core 0.22 mm2 alarm cable; 1 m 2-core shielded; 3 m 2-core 0.22 mm2; 2 m 4-core 0.22 mm2 | local electrical | 300 |
| JST PH kit | 1 | PH 2.0 housings 2/3/4-pin + SPH-002T-P0.5S crimps | Robu.in | 250 |
| USB-serial adapter | 1 | CP2102 or CH340, 3.3 V logic | Robu.in | 150 |
| microSD | 1 | 8-32 GB, FAT32 | any | 300 |
| Reservoir | 1 | 1.5-2 L food container + 4 mm aquarium bulkhead | local | 200 |
| Sealants | - | black RTV silicone (neutral cure), 2-part epoxy (Araldite Standard), PTFE tape | hardware shop | 400 |
| Calibration | - | KCl standards 1413 uS/cm and 12.88 mS/cm (Hanna HI7031 / HI7030 sachets) or self-made (section 9.2); handheld **urine-SG refractometer** with ATC (1.000-1.050) | lab suppliers, Amazon.in | 600 + 900-1,500 |
| Bench fluids | - | NaCl, KCl, urea (lab grade or 46 % N fertiliser urea for bench tests), riboflavin tablet or yellow food colour, citric acid | chemist, grocery | 200 |
| Filament | 1 kg | black PETG | Robu.in, local | 1,200 |

---

## 6. Tool checklist
- **Soldering:** temperature-controlled iron. Leaded 63/37 0.6 mm solder at 330-350 C, or lead-free SAC305 at 360-380 C. Chisel tip for the barrel jack and sockets, fine tip for JST pins. Flux pen, desoldering braid, isopropyl alcohol and brush.
- **Measuring:** multimeter with continuity buzzer; bench power supply 0-15 V with current limit (or the 12 V adapter plus an inline 0.5 A fuse for first power-up); calipers.
- **Crimping and wiring:** JST PH crimper (Engineer PA-09 or SN-28B), wire strippers for AWG 20-30, flush cutters, heat-shrink 2/3/6 mm, heat gun.
- **Wire gauges:** 0.5 mm2 (AWG 20) for VM, pump and valve; 0.22 mm2 (AWG 24) for signals; shielded 2-core for the photodiodes.
- **Mechanical:** soldering-iron tip for heat-set inserts (M3), 230-250 C; drill + bits 1.0, 2.5, 4.2, 5.1 mm; M5 x 0.8 and M3 x 0.5 taps with a tap wrench; deburring tool; hobby knife; files; zip ties.
- **Plumbing:** tube cutter or sharp scissors, 60 mL syringe, 10 mL and 25 mL measuring cylinders, small beakers or cups, PTFE tape (2 wraps on M5 threads into PETG; do not over-tighten).
- **Adhesives:** 2-part epoxy (electrode pins, drain barb); black neutral-cure RTV (optical potting, gland backup). No cyanoacrylate on wetted surfaces.
- **Safety:** nitrile gloves and safety glasses for any work with urine, and a 1 % sodium hypochlorite (diluted bleach) wipe for surfaces. **Never** run bleach through the device: the chlorine attacks titanium-oxide films and silicone.
- **Computer:** VS Code + PlatformIO (or arduino-cli), Python 3 with pyserial / paho-mqtt, a micro-USB cable.

---

## 7. PCB order and assembly
1. Order from JLCPCB with the files in `utility10/pcb/release/trishna/`: 2 layers, 1.6 mm, HASL, PCB Assembly (economic, top). Follow `trishna/ORDERING.md` for the steps and the parts list.
2. Hand-solder the through-hole parts in this order, smallest first:
   - JP1 header
   - J4 / J5 1x19 sockets: insert the DevKit into them before soldering, so they align with its pins, then remove it
   - JST PH J6-J15
   - barrel jack J1
3. Clean the flux with IPA. Inspect DRV8871 U3 pin 1 and the AO3400A / AO3401A orientation against `*_assembly_top.pdf`.

---

## 8. Electronics bring-up (before anything wet)
### 8.1 Unpowered checks
- No DevKit plugged in, JP1 removed.
- Resistance between VM (TP1) and GND (TP4): above 1 kohm (it rises as the caps charge).
- Between +3V3 (TP2) and GND: above 1 kohm.

### 8.2 First power, no DevKit
1. Set the bench supply to 12.0 V with a 150 mA current limit and connect it via a 5.5 mm plug.
2. Expect:
   - idle current under 15 mA
   - TP1 VM = 11.9-12.0 V
   - TP2 +3V3 = 3.30 V +/- 0.05
   - TP3 +3V3A = 3.30 V
   - green D6 on
3. Reverse the supply polarity for 2 seconds: the current must stay near 0 (the PMOS blocks).
4. Restore the polarity.

### 8.3 Fit the DevKit, then power from 12 V
1. Power off. Fit JP1. Insert the DevKit with its USB end toward the "USB END" silk.
2. Power on at 12 V with the limit raised to 500 mA. Expect 60-120 mA.
3. With 12 V on, the DevKit's 3V3 pin reads 3.30 V.

### 8.4 Flashing
1. Either **power the board from 12 V and keep JP1 fitted, with USB disconnected**, or **remove JP1 and flash over USB with 12 V off**. Never have JP1 fitted while both USB and 12 V are connected: the DevKit's own 3.3 V regulator would fight the buck.
2. Remove JP1, plug in USB, run `pio run -t upload`, unplug USB, refit JP1, power from 12 V.
3. For day-to-day logs without USB, use J15 + the bridge.

### 8.5 Actuators without plumbing
Connect the pump and valve leads, with nothing filled. In the console (USB with JP1 removed, or a USB-serial adapter on J15 with 12 V):
1. `prime fwd 2000`: the pump turns. Mark the forward direction on the pump head with a marker.
2. `prime rev 2000`: the pump runs the other way.
3. If forward pumps the wrong way, swap the pump leads at J6. Do not change the firmware.
4. `valve 1000`: the valve clicks and the DevKit blue LED (GPIO2) lights.
5. Confirm with a meter: VALVE_D falls to near 0 V while open and returns to 12 V. The flyback diode keeps the turn-off spike under 13 V; check this with an oscilloscope if you have one.

### 8.6 Sensors dry
- `status`:
  - the sump and leak probes read about 3,300 mV (open)
  - the ToF distance changes as you move a hand
  - vin is about 12 V
- `raw`:
  - EC phase voltages show the air condition (Va about 3.3 V, Vb under 25 mV, air = 1)
  - temperature reads room temperature
  - optics dark readings are under 30 mV
- LEDs: look at the sensor block's LED ports through a phone camera. IR shows as purple-white during the IR step.

---

## 9. Calibration
### 9.1 Photodiode gain check (clear water in the chamber)
1. Fill the chamber with tap water (`purge`).
2. Run `raw`. Target **blue tx and IR tx 1,500-2,500 mV**.
3. If they read above 3,000 mV (saturated): fit a lower Rf for R71 (4.7 k), or a larger LED resistor (R67 / R70 1.5 k).
4. If they read below 500 mV: fit a higher Rf for R71 (22-47 k).
5. Scatter (sc) reads 20-300 mV in clear water. Check that it rises when a drop of milk is added.

### 9.2 Conductivity, 2-point
Standards:
- **1.413 mS/cm:** 0.7456 g KCl per litre of distilled water (0.01 M).
- **12.88 mS/cm:** 7.456 g KCl per litre (0.1 M).
- Weigh to +/- 1 mg, or buy the Hanna HI7031 / HI7030 sachets.

Procedure:
1. Put the inlet tube in standard 1 and run `prime fwd 15000`, so 3+ chamber volumes go through and the old content is displaced.
2. Wait 1 minute for the temperature to settle, then `cal ec1 1.413`.
3. Rinse: `prime fwd 15000` with distilled water, then with standard 2.
4. `cal ec2 12.88`, then `cal ec solve`. Expect **K about 2-4 /cm** and Rb 50-250 ohm.
5. `save`.
6. Verify with a third solution (for example 5 g/L NaCl, about 9.5 mS/cm at 25 C). It should read within 3 %.

### 9.3 Pump flow
1. Put the outlet tube in a 25 mL measuring cylinder and run `prime fwd 10000`.
2. Read the collected volume and enter it: `cal flow 9.6` (mL).
3. The console prints the new sample time. `save`.
4. Repeat monthly: the volume per second falls as the tube wears.

### 9.4 SG model (the important one)
1. Over 1-2 weeks, for at least 10 events, also catch a few mL of the same stream in a clean cup. Measure it with the refractometer (calibrated to 1.000 with water first).
2. Note the device's event id, shown in the bridge output, and write `event_id,sg` lines in `refractometer.csv`.
3. Include first-morning (concentrated) and after-drinking (dilute) samples.
4. Run `python3 tools/trishna_fit_sg.py trishna.csv refractometer.csv`.
5. Type the printed `cal sg ...` line into the console, then `save`. Flag `cal_default` clears once both EC and SG are calibrated.
6. If the fit's RMS error is above 0.004, conductivity is not tracking your SG well (glucose or protein raise SG without raising EC). Use the device for trends only.

### 9.5 Presence and stream thresholds
1. `set presence_mm <distance>`: the ToF reading with you standing at the urinal, plus 150 mm.
2. Stream: pour 30 mL of the synthetic urine (10.2) into the sump at about 15 mL/s. `status` must show stream 1 within 0.3 s.
3. If it doesn't: `set stream_abs_mv 800`.
4. `save`.

---

## 10. Mechanical and plumbing assembly, leak test, validation
### 10.1 Assembly (in this order)
1. **Prepare the prints.**
   - Remove any brim.
   - Ream the optical ports with a 5.1 mm drill by hand and the probe port with a 6.2 mm drill.
   - Drill the electrode holes 1.0 mm.
   - Tap the 4 M5 ports (the block's top and bottom, the sump side port, and any spare) with M5 x 0.8: 3 turns in, half a turn back, keeping it square.
   - Tap M3 for the leak screws.
   - Melt in the heat-set inserts (iron at 240 C, press square, stop flush).
2. **Sensor block.**
   - **Electrodes:** push two 25 mm titanium pins through the electrode holes until 4 mm shows in the bore (check with a small mirror and a light). Pot the outside with epoxy. After it cures, crimp a ferrule on each pin and solder the H2 wires to the ferrules (titanium itself cannot be soldered).
   - **LEDs and photodiodes:** fit an O-ring 5 x 1 over each LED and photodiode. Push each into its port until the flange seats: blue at the lower +X port, IR at the upper +X port, SFH 203 transmission on -X, SFH 203 scatter on +Y. Screw on a retainer with 2 x M2 x 6 and pot behind it with black RTV.
   - **Temperature probe:** O-ring 6 x 1.5 on the DS18B20 probe. Push it in until the tip just passes the bore axis (2 mm: the sheath stops 18 mm into the port). Retainer + RTV.
   - **Fittings:** screw in the two M5 barbs with 2 wraps of PTFE tape, hand-tight plus 1/8 turn.
   - Let the RTV cure for 24 h.
3. **Bench leak test of the block.**
   - Cap the top barb with a short tube, folded and tied.
   - Fill the block through the bottom barb with a 60 mL syringe and press firmly for 30 s, about 0.5-1 bar by hand.
   - Pass: no drop on a dry tissue wrapped round the block.
   - If it seeps through the print, re-print at 245 C with flow 1.05. Painting the outside with thin epoxy is a temporary fix.
4. **Chamber B.**
   - Mount the pump bracket and the pump, with the pump head toward the bottom wall.
   - Mount the valve on its saddle (2 zip ties).
   - Bolt the block onto the shelf with 4 x M3 x 45 + nuts.
   - Fit the leak screws with ring terminals inside.
   - Fit the bottom-wall tube glands (P1, P2, P3) and epoxy the 4 mm drain barb into P4.
   - Route T2 and T3 short, then the tee and the check valve (arrow away from the block), with T4 to P2. Run T5 from P3 to the valve inlet, and the valve outlet to the tee.
   - Tie every tube to the anchors.
5. **Chamber A.**
   - Fit the PCB on the standoffs (4 x M3 x 6) and the glands.
   - Pass the harness cables H1, H2, H3 and the DS18B20 cable up through B's top glands and A's bottom glands. Leave 5 cm service loops. Crimp the JST contacts.
   - Tighten the gland nuts until the seal grips the cable sheath (it must not rotate).
6. **Lids.**
   - Press the silicone cord into each lid groove, starting at a corner, without stretching it. Cut it to butt-join with a drop of RTV.
   - Fit the lids: tighten the screws in a cross pattern to finger-tight plus 1/4 turn. Over-tightening bows the lid between screws.
7. **Wall.**
   - Mount B with its bottom at least 150 mm above the sump outlet level. Mount A 40 mm above B. Mount the reservoir with its outlet at least 300 mm above B.
   - All glands and ports face down.
   - Run T1 from the sump insert and T4 into the bowl.

### 10.2 System leak test (wet, before the first real use)
1. Fill the reservoir. Run `purge` 3 times: the chamber fills and air leaves via the tee and T4.
2. Put T1's end in a cup of water and run `prime fwd 20000`. Then `purge`.
3. Open chamber B. Dry paper towels on the V-floor and around every joint must stay dry. The leak probe must read about 3,300 mV in `status`.
4. **Pump dead-head test (max 3 s):** pinch T4 shut, then `prime fwd 3000`. The DRV8871 current limit protects the pump. No joint may weep.
5. **Leak-detection test:** drip 2 mL of tap water onto the V-floor between the M3 screws. Within 0.2 s the system goes to LOCKOUT with error `leak` and everything stops. `clear` resets it after drying.

### 10.3 Bench fluids
| Fluid | Recipe (per litre of tap water) | Expected |
|---|---|---|
| A: synthetic urine, normal | 8.0 g NaCl, 1.6 g KCl, 20 g urea, 1/4 riboflavin (vitamin B2) tablet crushed, or yellow food colour to a pale straw tint | refractometer SG about 1.014-1.016; EC25 about 16 mS/cm |
| B: concentrated | double A | SG about 1.028-1.032; EC25 about 30 mS/cm |
| C: dilute | A diluted 1:3 with tap water | SG about 1.004-1.006; EC25 about 4-5 mS/cm |
| D: turbid | A + 2 mL milk | turbidity index clearly above A's |
| E: flush water | tap water | must NOT trigger without presence |

Measure each fluid with the refractometer and record its real SG: these recipes are approximate.

### 10.4 Validation protocol: the automated catch-and-purge
Set up:
- Run the bridge with `--csv val.csv`.
- Put a cardboard target in front of the ToF at the presence distance, to simulate a person.
- "Stream" = pour the fluid steadily into the sump insert from a 250 mL jug at about 15 mL/s for 12 s. Use a funnel if needed.

| # | Test | Procedure | Pass criteria (frames in `val.csv` / console) |
|---|---|---|---|
| V1 | Normal event | target present, pour A | states in order: IDLE -> STREAM_DETECTED -> SAMPLING (starts 2.0 +/- 0.1 s later) -> ANALYSIS -> PURGE_CLEANING -> LOCKOUT -> IDLE (30 s later); one RESULT frame with quality >= 80, no `diluted` flag, EC25 within 5 % of the lab EC of A, temperature valid |
| V2 | Repeatability | V1 x 10 with fluid A (wait for IDLE between) | EC25 CV <= 2 %; A450 SD <= 0.01; SG estimate range <= 0.002 |
| V3 | Carry-over | alternate B, C, B, C (4 events) | C after B reads within 3 % of C alone; B after C within 3 % of B alone (needs the 3-volume flush) |
| V4 | Purge effectiveness | after V3, `raw` (chamber holds rinse water) | EC within 10 % of reservoir water; A450 vs blank under 0.01 |
| V5 | Short event | target present, 1 s pour | ERROR frame `short event`, back to IDLE, pump never ran |
| V6 | Flush only | no target, pour E for 10 s | no event (stays IDLE) |
| V7 | Fallback | target present 5 s, sump already full of A, no pour | event with `fallback_trigger` flag, quality reduced by 10 |
| V8 | Dilution guard | target present, pour C then immediately E | RESULT with `diluted` flag or quality < 60 |
| V9 | Reservoir empty | empty the reservoir, run `event` | PURGE check finds air -> ERROR `reservoir empty`, LOCKOUT; refill, wait for the 10-minute retry (or `purge`) -> fault clears |
| V10 | Leak | as 10.2 step 5, during SAMPLING | pump and valve off within 0.2 s, ERROR `leak`, stays latched until `clear` |
| V11 | Supply | run from 10.0 V, then 14.5 V | ERROR `supply low` / `supply high` frames; operation continues at 10.8-13.5 V |
| V12 | Telemetry integrity | `--replay` the SD file after V1-V10 | same frames as the live CSV, 0 rejected; `status`: dropped 0 |

Record the results in `docs/validation_log.md`, a table with the date, firmware version, fluid lot and measured vs expected. A failed V1-V4 means the sensing or plumbing needs work before any real use.

---

## 11. Operation, hygiene and maintenance
- **Daily:** nothing. Check `status` or the dashboard for faults.
- **Weekly:** refill the reservoir with fresh tap water and wipe the sump insert.
- **Monthly descaling:**
  1. Fill the reservoir with 2 % citric acid (20 g/L) and run `purge` 3 times.
  2. Wait 15 minutes, then `purge` 3 times with tap water.
  3. Check the photodiode readings with `raw` (they should return to the 9.1 values).
- **Every 6 months:** replace the pump tube and the silicone T2 / T3 tubes, check the O-rings, and recalibrate EC (9.2) and flow (9.3).
- **Handling:** wear gloves; anything that touched urine goes in a sealed bag; wash your hands.
- **Power:** the 12 V adapter plugs into a socket at least 1.2 m above the floor, on an RCD-protected circuit. Everything near water is 12 V SELV.

## 12. Known limits and open risks
1. **The SG estimate is the weak link.** Conductivity follows salts, not urea, glucose or protein. Even after per-user fitting, expect +/- 0.003-0.005 SG. Confirm against a refractometer monthly.
2. **Absorbance is relative to the rinse blank,** not to a reference standard. Window fouling is cancelled to first order by the per-event blank, but deposits still drift: the monthly descaling and the 9.1 check matter.
3. The printed flow cell's watertightness depends on print quality: section 10.1 step 3 is mandatory.
4. **Mid-stream timing** assumes the sump probe sees the stream within 0.3 s and the cup is refreshed in under 2 s at 15-20 mL/s. A waterless urinal, where the cup keeps old urine, only works through the presence fallback, which is flagged.
5. **Titanium electrodes** are durable, but check them for deposits at the 6-month service.
6. **Not certified:** no electrical-safety, EMC or medical approval. For personal bench use only.
