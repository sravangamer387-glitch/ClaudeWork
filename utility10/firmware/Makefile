# make test -> host tests; make hex -> eight Nano builds in release/ (needs gcc-avr avr-libc arduino-core-avr)
ARD = /usr/share/arduino/hardware/arduino/avr
FCPU ?= 16000000L
RELDIR ?= release
CF = -mmcu=atmega328p -DF_CPU=$(FCPU) -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs
.PHONY: test hex prod seeti_prod boards clean
prod:   # production clocks: 4 MHz (2xAAA boards) and 8 MHz (3xAA / USB boards); the board READMEs say which hex to use
	$(MAKE) hex FCPU=4000000L RELDIR=release/4MHz
	$(MAKE) hex FCPU=8000000L RELDIR=release/8MHz
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined test/test_util.c lib/utilcore.c -lm -o build/test_util && ./build/test_util
hex:
	@mkdir -p build/core$(FCPU) $(RELDIR)
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc $(CF) -c $$f -o build/core$(FCPU)/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ $(CF) -fno-exceptions -c $$f -o build/core$(FCPU)/$$(basename $$f).o || exit 1; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=$(FCPU) -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/core$(FCPU)/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/core$(FCPU).a build/core$(FCPU)/*.o
	@avr-gcc $(CF) -std=gnu99 -Ilib -c lib/utilcore.c -o build/utilcore$(FCPU).o
	@for t in 1:seeti_counter 2:gas_taraju 3:fridge_guard 4:bijli_meter 5:bijli_log 6:chulha_timers 7:rain_alert 8:tap_litre; do n=$${t%%:*}; name=$${t##*:}; \
	 avr-g++ $(CF) -fno-exceptions -DTOOL=$$n -Ilib -c src/main_util.cpp -o build/main$$n.o && \
	 avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/main$$n.o build/utilcore$(FCPU).o build/core$(FCPU).a -lm -o build/$$name.elf && \
	 avr-objcopy -O ihex -R .eeprom build/$$name.elf $(RELDIR)/$$name.hex && echo "$$name: $$(avr-size -C --mcu=atmega328p build/$$name.elf | grep Program)"; done
seeti_prod:   # production firmware for the Seeti rev B board (4 MHz)
	@mkdir -p build/core4000000L release/4MHz
	$(MAKE) hex FCPU=4000000L RELDIR=release/4MHz >/dev/null
	avr-g++ -mmcu=atmega328p -DF_CPU=4000000L -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -fno-exceptions -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -Ilib -c src/seeti_prod.cpp -o build/seeti_prod.o
	avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/seeti_prod.o build/utilcore4000000L.o build/core4000000L.a -lm -o build/seeti_prod.elf
	avr-objcopy -O ihex -R .eeprom build/seeti_prod.elf release/4MHz/seeti_prod.hex
	@avr-size -C --mcu=atmega328p build/seeti_prod.elf | grep -E "Program|Data"

boards:    # PCB firmware: one hex per rev B board (see src/main_board.cpp)
	@mkdir -p build/core$(FCPU) $(RELDIR)/boards
	$(MAKE) hex FCPU=$(FCPU) RELDIR=$(RELDIR)/tmp >/dev/null
	@for t in 2:gas_taraju 3:fridge_guard 4:bijli_meter 5:bijli_log 6:chulha_timers 7:rain_alert 8:tap_litre; do n=$${t%%:*}; name=$${t##*:}; \
	 avr-g++ $(CF) -fno-exceptions -DBOARD=$$n -Ilib -I$(ARD)/libraries/Wire/src -c src/main_board.cpp -o build/board$$n.o && \
	 avr-g++ $(CF) -fno-exceptions -I$(ARD)/libraries/Wire/src -c $(ARD)/libraries/Wire/src/Wire.cpp -o build/Wire.o && avr-gcc $(CF) -std=gnu99 -c $(ARD)/libraries/Wire/src/utility/twi.c -o build/twi.o && \
	 avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/board$$n.o build/Wire.o build/twi.o build/utilcore$(FCPU).o build/core$(FCPU).a -lm -o build/board_$$name.elf && \
	 avr-objcopy -O ihex -R .eeprom build/board_$$name.elf $(RELDIR)/boards/$$name.hex && echo "board $$name: $$(avr-size -C --mcu=atmega328p build/board_$$name.elf | grep -E 'Program|Data' | tr '\n' ' ')"; done
	@rm -rf $(RELDIR)/tmp
clean:
	rm -rf build
