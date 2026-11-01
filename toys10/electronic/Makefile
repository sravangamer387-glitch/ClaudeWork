# make test -> host tests; make hex -> four Nano builds in release/ (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
CF8 = -mmcu=atmega328p -DF_CPU=8000000L -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs
CF = -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs
.PHONY: test hex pcb clean
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined test/test_toycore.c lib/toycore.c -lm -o build/test_toycore && ./build/test_toycore
hex:
	@mkdir -p build/core release
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc $(CF) -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ $(CF) -fno-exceptions -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=16000000L -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/core.a build/core/*.o
	@avr-gcc $(CF) -std=gnu99 -Ilib -c lib/toycore.c -o build/toycore.o
	@for t in 1:reflex_raja 2:taal_memory 3:aloo_bomb 4:beat_runner; do n=$${t%%:*}; name=$${t##*:}; \
	 avr-g++ $(CF) -fno-exceptions -DTOY=$$n -Ilib -c src/main_toys.cpp -o build/main$$n.o && \
	 avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/main$$n.o build/toycore.o build/core.a -lm -o build/$$name.elf && \
	 avr-objcopy -O ihex -R .eeprom build/$$name.elf release/$$name.hex && echo "$$name: $$(avr-size -C --mcu=atmega328p build/$$name.elf | grep Program)"; done
	@avr-g++ $(CF) -fno-exceptions -Ilib -c src/main_arcade.cpp -o build/arcade.o && avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/arcade.o build/toycore.o build/core.a -lm -o build/desi_arcade.elf && avr-objcopy -O ihex -R .eeprom build/desi_arcade.elf release/desi_arcade.hex && echo "desi_arcade: $$(avr-size -C --mcu=atmega328p build/desi_arcade.elf | grep Program)"
pcb:     # rev B boards (3 x AAA = 4.5 V, internal 8 MHz RC): Desi Arcade (PCB_REV_B pin map) and Beat Runner (buzzer on D9)
	@mkdir -p build/core8 release/pcb
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc $(CF8) -c $$f -o build/core8/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ $(CF8) -fno-exceptions -c $$f -o build/core8/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=8000000L -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core8/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/core8.a build/core8/*.o && avr-gcc $(CF8) -std=gnu99 -Ilib -c lib/toycore.c -o build/toycore8.o
	avr-g++ $(CF8) -fno-exceptions -DPCB_REV_B -Ilib -c src/main_arcade.cpp -o build/arcade8.o && avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/arcade8.o build/toycore8.o build/core8.a -lm -o build/arcade_pcb.elf && avr-objcopy -O ihex -R .eeprom build/arcade_pcb.elf release/pcb/desi_arcade_rev_b.hex
	avr-g++ $(CF8) -fno-exceptions -DTOY=4 -DBUZ=9 -Ilib -c src/main_toys.cpp -o build/br8.o && avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/br8.o build/toycore8.o build/core8.a -lm -o build/br_pcb.elf && avr-objcopy -O ihex -R .eeprom build/br_pcb.elf release/pcb/beat_runner_rev_b.hex
	@avr-size -C --mcu=atmega328p build/arcade_pcb.elf build/br_pcb.elf | grep -E "Program|AVR"
clean:
	rm -rf build
