Pre-built, untested-on-hardware firmware for an Arduino Nano (ATmega328P). Flash with avrdude:
`avrdude -c arduino -p m328p -P /dev/ttyUSB0 -b 57600 -U flash:w:rhymes.hex` (use -b 115200 for the newer Nano bootloader).
Files: rhymes.hex, lamp.hex, cricket.hex, beatlight.hex, midi.hex. Rebuild with `make` in the parent folder.
