# GEONODE design notes
- **Why features on the node:** a raw 2 s window is 800 bytes; a LoRa frame carries tens of bytes at low data rate. Six features in 12 bytes keep airtime and energy low; a gateway that wants raw data can request a window by downlink.
- **Why transparent thresholds:** the gateway shows *why* a window was flagged (kurtosis, band fractions), which an engineer can inspect and tune; a black-box model trained on simulated data would hide that.
- **Crack vs vehicle:** vehicles put energy at 3-20 Hz with a smooth envelope (low kurtosis); cracking is a short broadband burst (high kurtosis, high-frequency fraction, large peak). A weak crack barely raises the RMS, so impulses are tested before the RMS gate.
- **Alarm logic:** `CrackTracker(n=3, horizon=30)`; tune by structure.
- **Hardware reuse:** the node is the MITTI-NETRA board; strain and tilt drift use its alarm state machine (`mn_core`).
