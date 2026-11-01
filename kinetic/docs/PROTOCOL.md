# KINETIC line protocol
ASCII lines terminated by `\n`, 115200 baud (USB-CDC ignores the rate). Optional checksum: append `*HH` where HH is the CRC-8 (polynomial 0x07, initial 0) of every character before the `*`, in hex. A wrong checksum gives `ERR checksum`.

| Command | Example | Meaning |
|---|---|---|
| `MOVE` | `MOVE X=1000 Y=-250 F=2000` | absolute move (steps) of the named axes; F = speed limit in steps/s (never above the configured vmax) |
| `LIMITS` | `LIMITS F=2000 A=20000 J=400000` | set vmax (F), amax (A), jmax (J) |
| `STOP` | `STOP` | halt immediately (no deceleration ramp: use only for emergencies) |
| `CLEAR` | `CLEAR` | clear a halt (after an endstop trip, back off by hand first) |
| `HOME` | `HOME X=0` | parsed but not implemented in the skeleton |

Replies: `OK ...` or `ERR <reason>`; unsolicited `VIB <class> <name> hz=<shaft Hz>` after a steady-speed window. Classes: 0 healthy, 1 outer-race, 2 inner-race, 3 unbalance.
