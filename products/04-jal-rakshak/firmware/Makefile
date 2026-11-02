# make test  -> host unit tests (gcc);   make hex -> Arduino Nano firmware (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
FCPU ?= 16000000L          # Nano: 16 MHz; Jal-Rakshak PCB (no crystal, internal RC): make hex FCPU=8000000L, fuses lfuse=0xE2 hfuse=0xD9 efuse=0xFD
.PHONY: test hex pcb clean
pcb:
	$(MAKE) clean-app hex FCPU=8000000L && mkdir -p release && cp build/jal.hex release/jal_rakshak_pcb_8MHz.hex
clean-app:
	rm -rf build/core build/app build/core.a
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined test/test_jal.c lib/jal_core.c -lm -o build/test_jal && ./build/test_jal
hex:
	@mkdir -p build/core build/app
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -fno-exceptions -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core/$$(basename $$f).o 2>/dev/null; done
	avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -fno-exceptions -Wall -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -Ilib -c src/main_jal.cpp -o build/app/main.o
	avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -Os -Wall -std=gnu99 -Ilib -c lib/jal_core.c -o build/app/core.o
	avr-ar rcs build/core.a build/core/*.o
	avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/app/*.o build/core.a -lm -o build/jal.elf
	avr-objcopy -O ihex -R .eeprom build/jal.elf build/jal.hex
	@avr-size -C --mcu=atmega328p build/jal.elf | grep -E "Program|Data"
clean:
	rm -rf build
