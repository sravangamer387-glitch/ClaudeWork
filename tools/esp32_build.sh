#!/bin/bash
# Compile the ESP32-S3 firmware of KINETIC, MITTI-NETRA, BioTray and AQUAPONICS with arduino-cli (core esp32:esp32@2.0.17).
# usage: tools/esp32_build.sh [arduino-cli path]   -> build/esp32/<project>/*.bin and a size line per project; exits non-zero on any failure.
# Needs once: arduino-cli core install esp32:esp32@2.0.17; arduino-cli lib install OneWire DallasTemperature PubSubClient BH1750 "Adafruit ADS1X15"
set -u
CLI=${1:-arduino-cli}; ROOT=$(cd "$(dirname "$0")/.." && pwd); OUT=$ROOT/build/esp32; STAGE=$(mktemp -d)
FQBN="esp32:esp32:esp32s3:CDCOnBoot=cdc,PSRAM=disabled,FlashSize=8M"
fail=0
build() {  # name, src dir, lib dir, main cpp
  local n=$1 src=$2 lib=$3 main=$4 d=$STAGE/$1
  mkdir -p "$d"; cp "$ROOT/$src"/*.h "$d/" 2>/dev/null; cp "$ROOT/$lib"/*.c "$ROOT/$lib"/*.h "$d/" 2>/dev/null
  cp "$ROOT/$src/$main" "$d/$n.ino"
  [ -f "$ROOT/$src/secrets.h.example" ] && cp "$ROOT/$src/secrets.h.example" "$d/secrets.h"
  sed -i 's#"../../../biotray/firmware/src/biotray_pins.h"#"biotray_pins.h"#' "$d/$n.ino"
  [ "$n" = aquaponics ] && cp "$ROOT/biotray/firmware/src/biotray_pins.h" "$d/"
  mkdir -p "$OUT/$n"
  if "$CLI" compile --fqbn "$FQBN" --output-dir "$OUT/$n" --warnings all "$d" > "$OUT/$n/compile.log" 2>&1; then
    echo "OK   $n: $(grep -E 'Sketch uses|Global variables' "$OUT/$n/compile.log" | tr '\n' ' ')"
  else echo "FAIL $n (see build/esp32/$n/compile.log)"; grep -E "error" "$OUT/$n/compile.log" | head -15; fail=1; fi
}
build kinetic   kinetic/firmware/src     kinetic/firmware/lib     main_kinetic.cpp
build mitti     mitti-netra/firmware/src mitti-netra/firmware/lib main_mitti.cpp
build biotray   biotray/firmware/src     biotray/firmware/lib     main_biotray.cpp
build aquaponics aquaponics/firmware/src aquaponics/firmware/lib  main_aquaponics.cpp
libcheck() {  # name, lib dir: compile a project core library for the ESP32-S3 (no application yet)
  local n=$1 lib=$2 d=$STAGE/$1; mkdir -p "$d" "$OUT/$n"; cp "$ROOT/$lib"/*.c "$ROOT/$lib"/*.h "$d/"
  printf '#include <Arduino.h>\nvoid setup() {}\nvoid loop() {}\n' > "$d/$n.ino"
  if "$CLI" compile --fqbn "$FQBN" --output-dir "$OUT/$n" --warnings all "$d" > "$OUT/$n/compile.log" 2>&1; then echo "OK   $n (library compile check)"; else echo "FAIL $n"; grep error "$OUT/$n/compile.log" | head; fail=1; fi
}
libcheck geotech_lib geotech/node/lib
libcheck sorter_lib  sorter/firmware/lib
libcheck agrover_lib agrover/firmware/lib
rm -rf "$STAGE"; exit $fail
