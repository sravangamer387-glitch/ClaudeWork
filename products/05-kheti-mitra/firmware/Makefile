# make test  -> host unit tests (gcc);   make hex -> Arduino Nano firmware (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
.PHONY: test hex board clean
test:
	@mkdir -p build && gcc -std=c99 -D_GNU_SOURCE -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined test/test_kheti.c lib/kheti_core.c -lm -o build/test_kheti && ./build/test_kheti
FCPU ?= 16000000L
XFLAGS ?=
hex:
	@mkdir -p build/core build/app
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -fno-exceptions -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core/$$(basename $$f).o 2>/dev/null; done
	avr-g++ -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -fno-exceptions -Wall -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -Ilib -c $(XFLAGS) src/main_kheti.cpp -o build/app/main.o
	avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -Os -Wall -std=gnu99 -Ilib -c lib/kheti_core.c -o build/app/core.o
	avr-ar rcs build/core.a build/core/*.o
	avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/app/*.o build/core.a -lm -o build/kheti.elf
	avr-objcopy -O ihex -R .eeprom build/kheti.elf build/kheti.hex
	@avr-size -C --mcu=atmega328p build/kheti.elf | grep -E "Program|Data"
clean:
	rm -rf build

board:   # Kheti-Mitra rev B PCB: internal 8 MHz RC, status LED on PD7 (utility10/pcb/boards/kheti.py)
	@rm -rf build/core build/app
	$(MAKE) hex FCPU=8000000L XFLAGS=-DLED_PIN=7
	cp build/kheti.hex ../release/kheti_mitra_board_8MHz.hex
