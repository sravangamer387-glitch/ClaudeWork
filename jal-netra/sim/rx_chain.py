"""Receive-chain noise budget and the resulting transit-time resolution. LNA noise from datasheet-class values (ASSUMED, verify):
OPA356 input noise 5.8 nV/rtHz; piezo source impedance about 270 ohm; 1 kOhm series + feedback network; ADC 12-bit, 3.3 V, LSB 0.806 mV."""
import math, os
K = 1.380649e-23; T = 300.0
def en_total(rs=270.0, rg=240.0, rf=2200.0, en=5.8e-9):
    r_fb = rg * rf / (rg + rf); return math.sqrt(en ** 2 + 4 * K * T * (rs + r_fb))
BW = 2.0e6                                                  # measurement bandwidth set by the 6-cycle burst (about 1/(6 us))
LSB = 3.3 / 4096; q_rms = LSB / math.sqrt(12)
rows = ["| received amplitude at the piezo (mV pk) | gain (dB) | signal at ADC (mV pk) | LNA noise at ADC (uV rms) | ADC quantisation (uV rms) | SNR per sample (dB) | predicted std of dt after 1000 pairs (ps) | flow resolution (L/h) |", "|---|---|---|---|---|---|---|---|"]
en = en_total(); out = []
for a_mv in (0.5, 1, 2, 5, 10, 20, 50, 100):
    best = None
    for gdb in (20.1, 40.9):
        g = 10 ** (gdb / 20); sig = a_mv * 1e-3 * g
        if sig > 1.55: continue                              # would clip (rail-to-rail swing +-1.65 V)
        noise = math.sqrt((en * math.sqrt(BW) * g) ** 2 + q_rms ** 2); snr = 20 * math.log10(sig / noise)
        if best is None or snr > best[3]: best = (gdb, sig, noise, snr)
    if not best: rows.append(f"| {a_mv} | - | clips | | | | | |"); continue
    gdb, sig, noise, snr = best
    sd = 75.0 * 10 ** ((30 - snr) / 20)                      # twin: 75 ps at 30 dB SNR, N = 1000 (scales with 1/SNR)
    q_lph = (sd * 1e-12) * 1482.4 ** 2 / (2 * 0.060) * (math.pi * 0.012 ** 2 / 4) * 3.6e6 * 0.75
    rows.append(f"| {a_mv} | {gdb} | {sig*1e3:.0f} | {math.sqrt((en*math.sqrt(BW)*10**(gdb/20))**2)*1e6:.0f} | {q_rms*1e6:.0f} | {snr:.1f} | {sd:.0f} | {q_lph:.2f} |")
txt = f"Input-referred noise density {en*1e9:.1f} nV/rtHz over {BW/1e6:.0f} MHz = {en*math.sqrt(BW)*1e6:.1f} uV rms (LNA + source + feedback resistors). Gain selected automatically for the best SNR without clipping (U7).\n\n" + "\n".join(rows) + "\n\nReading: the first-stage-only 20 dB setting is limited by ADC quantisation; the 40 dB setting by the LNA noise. If the real received amplitude is below about 1 mV the design needs more averaging (time) or a higher drive/transducer efficiency; if it is above 20 mV the 20 dB path is used. **The received amplitude after a 60 mm water path is an assumption to be measured on the first spool.**"
open(os.path.join(os.path.dirname(__file__), "..", "docs", "rx_budget.md"), "w").write(txt + "\n"); print(txt)
