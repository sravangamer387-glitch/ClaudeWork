# make test -> host tests; make hex -> eight Nano builds in release/ (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
CF = -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs
.PHONY: test hex clean
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined test/test_util.c lib/utilcore.c -lm -o build/test_util && ./build/test_util
hex:
	@mkdir -p build/core release
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc $(CF) -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ $(CF) -fno-exceptions -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=16000000L -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/core.a build/core/*.o
	@avr-gcc $(CF) -std=gnu99 -Ilib -c lib/utilcore.c -o build/utilcore.o
	@for t in 1:seeti_counter 2:gas_taraju 3:fridge_guard 4:bijli_meter 5:bijli_log 6:chulha_timers 7:rain_alert 8:tap_litre; do n=$${t%%:*}; name=$${t##*:}; \
	 avr-g++ $(CF) -fno-exceptions -DTOOL=$$n -Ilib -c src/main_util.cpp -o build/main$$n.o && \
	 avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/main$$n.o build/utilcore.o build/core.a -lm -o build/$$name.elf && \
	 avr-objcopy -O ihex -R .eeprom build/$$name.elf release/$$name.hex && echo "$$name: $$(avr-size -C --mcu=atmega328p build/$$name.elf | grep Program)"; done
clean:
	rm -rf build
