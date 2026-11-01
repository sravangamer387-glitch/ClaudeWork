# End-of-line test sheet

| Field | Value |
|---|---|
| Product / board rev | |
| Serial number | |
| Batch / date | |
| Operator | |
| Firmware file + checksum | |

| # | Test | Limit | Measured | Pass / Fail |
|---|---|---|---|---|
| 1 | Visual inspection (polarity, bridges, missing parts) | none found | | |
| 2 | Resistance supply-to-ground, power off | > 1 kohm | | |
| 3 | Supply current at power-on (current limit 50 mA) | per product manual | | |
| 4 | Voltage table (copy the rows from the board README) | per product manual | | |
| 5 | Fuses + flash verify | `avrdude` reports OK | | |
| 6 | Start-up behaviour (beep / LED / display) | per product manual | | |
| 7 | Functional test (product manual section "End-of-line test") | per product manual | | |
| 8 | Final visual, label, packaging | | | |

Result: PASS / FAIL (circle). Rework note:

Signature / date:
