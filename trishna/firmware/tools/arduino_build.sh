#!/bin/bash
# Compile the TRISHNA firmware with arduino-cli instead of PlatformIO (same Arduino-ESP32 2.0.17 core).
# Needs once:  arduino-cli core install esp32:esp32@2.0.17
#              arduino-cli lib install OneWire DallasTemperature VL53L1X
# usage: tools/arduino_build.sh [arduino-cli path]  ->  build/arduino/trishna.ino.bin (+ .bootloader.bin, .partitions.bin)
# flash:  arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 --input-dir build/arduino
set -eu
CLI=${1:-arduino-cli}
FW=$(cd "$(dirname "$0")/.." && pwd)
STAGE=$(mktemp -d)/trishna
mkdir -p "$STAGE" "$FW/build/arduino"
cp "$FW"/src/*.cpp "$FW"/src/*.h "$FW"/lib/trishna_core/src/*.c "$FW"/lib/trishna_core/src/*.h "$STAGE/"
printf '// Arduino IDE / arduino-cli entry: the real setup() and loop() are in main.cpp\n' > "$STAGE/trishna.ino"
"$CLI" compile --fqbn esp32:esp32:esp32:PartitionScheme=default,CPUFreq=240,FlashSize=4M --warnings all \
  --output-dir "$FW/build/arduino" "$STAGE" 2>&1 | tee "$FW/build/arduino/compile.log" | grep -E "warning|error|Sketch uses|Global variables" || true
grep -q "Sketch uses" "$FW/build/arduino/compile.log"
