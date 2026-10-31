Input-referred noise density 6.5 nV/rtHz over 2 MHz = 9.1 uV rms (LNA + source + feedback resistors). Gain selected automatically for the best SNR without clipping (U7).

| received amplitude at the piezo (mV pk) | gain (dB) | signal at ADC (mV pk) | LNA noise at ADC (uV rms) | ADC quantisation (uV rms) | SNR per sample (dB) | predicted std of dt after 1000 pairs (ps) | flow resolution (L/h) |
|---|---|---|---|---|---|---|---|
| 0.5 | 40.9 | 55 | 1013 | 233 | 34.5 | 44 | 0.25 |
| 1 | 40.9 | 111 | 1013 | 233 | 40.6 | 22 | 0.12 |
| 2 | 40.9 | 222 | 1013 | 233 | 46.6 | 11 | 0.06 |
| 5 | 40.9 | 555 | 1013 | 233 | 54.5 | 4 | 0.02 |
| 10 | 40.9 | 1109 | 1013 | 233 | 60.6 | 2 | 0.01 |
| 20 | 20.1 | 202 | 92 | 233 | 58.2 | 3 | 0.02 |
| 50 | 20.1 | 506 | 92 | 233 | 66.1 | 1 | 0.01 |
| 100 | 20.1 | 1012 | 92 | 233 | 72.1 | 1 | 0.00 |

Reading: the first-stage-only 20 dB setting is limited by ADC quantisation; the 40 dB setting by the LNA noise. If the real received amplitude is below about 1 mV the design needs more averaging (time) or a higher drive/transducer efficiency; if it is above 20 mV the 20 dB path is used. **The received amplitude after a 60 mm water path is an assumption to be measured on the first spool.**
