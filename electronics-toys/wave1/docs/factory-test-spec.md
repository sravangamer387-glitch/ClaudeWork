# Factory Test Specification (AP1 products) – draft

Use with a simple test jig (pogo pins on the PCB, programmable supply, USB-UART). Entering test mode: hold BTN0 while switching on, or pull TEST_MODE (PC7) low.

## Per-unit tests (100 % of units)
| # | Test | Pass criterion |
|---|---|---|
| 1 | Supply current at 4.5 V, idle | within limit set from golden-unit measurements (record 10 units first) |
| 2 | Reverse battery connected | no current, no damage |
| 3 | 3V3 rail | 3.3 V ± 5 % |
| 4 | Battery divider reading | ADC within ±3 % of true voltage |
| 5 | Every button, one at a time | firmware reports the right index |
| 6 | Every LED / segment / lane LED | automated light check by camera or operator step |
| 7 | MP3 module: send RESET, SRC, VOLUME, play test track | module answers; speaker plays tone at set level |
| 8 | Speaker | no buzz or distortion at max cap volume (operator or microphone jig) |
| 9 | Motor (lamp rotor) | spins smoothly, current within limit |
| 10 | Burn-in sample (1 in 50, 24 h) | no failures |

## Final assembly checks
Battery door torque, no loose parts when shaken, label content (age, warnings, batteries, MRP, lot code, maker address), outgoing visual inspection, serial/lot logged.

## Records
Store results per serial for 3 years; keep golden units and a golden audio card.
