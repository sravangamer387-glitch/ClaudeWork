#!/bin/bash
# Build every ESP32 firmware in the portfolio with PlatformIO and print one line per project.
# usage: tools/pio_build_all.sh [pio path]     (needs api/dl.registry.platformio.org reachable)
set -u
PIO=${1:-pio}; ROOT=$(cd "$(dirname "$0")/.." && pwd); fail=0
for d in trishna/firmware kinetic/firmware mitti-netra/firmware biotray/firmware aquaponics/firmware geotech/node sorter/firmware agrover/firmware; do
  log=$(mktemp)
  if (cd "$ROOT/$d" && "$PIO" run > "$log" 2>&1); then
    own=$(grep -E "warning:" "$log" | grep -v "/.pio/libdeps/\|/packages/framework" | wc -l)
    echo "OK   $d  $(grep -E '^(RAM|Flash):' "$log" | sed 's/\[[= ]*\]//' | tr -s ' ' | tr '\n' ' ') project warnings: $own"
  else
    echo "FAIL $d"; grep -E "error" "$log" | head -8; fail=1
  fi
  rm -f "$log"
done
exit $fail
