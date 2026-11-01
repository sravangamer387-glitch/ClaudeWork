# make test -> host tests; make hex -> ATmega328P builds (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
FCPU ?= 8000000L
.PHONY: test hex clean
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib -Itest test/test_ad.c lib/ad_core.c -lm -o build/test_ad && ./build/test_ad
hex:
	@mkdir -p build/core release
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -fno-exceptions -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/core.a build/core/*.o
	@avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -fno-exceptions -std=gnu++11 -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -I$(ARD)/libraries/Wire/src -Ilib -c src/main_astradand.cpp -o build/main.o
	@avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -Os -std=gnu99 -Ilib -c lib/ad_core.c -o build/ad_core.o
	@avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -Os -fno-exceptions -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -I$(ARD)/libraries/Wire/src -c $(ARD)/libraries/Wire/src/Wire.cpp -o build/Wire.o
	@avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -Os -std=gnu99 -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $(ARD)/libraries/Wire/src/utility/twi.c -o build/twi.o
	@avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/main.o build/ad_core.o build/Wire.o build/twi.o build/core.a -lm -o build/astradand.elf
	@avr-objcopy -O ihex -R .eeprom build/astradand.elf release/astradand_8MHz.hex
	@avr-size -C --mcu=atmega328p build/astradand.elf | grep -E "Program|Data"
clean:
	rm -rf build
