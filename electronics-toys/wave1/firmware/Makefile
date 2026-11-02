CC ?= gcc
CFLAGS = -std=c99 -Wall -Wextra -Werror -Wshadow -Wconversion -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined
SRC = src/ap1_core.c src/app_rhymes.c src/app_lamp.c src/app_cricket.c

test: build/test_all
	./build/test_all

build/test_all: test/test_all.c test/fake_hal.h include/ap1.h $(SRC)
	@mkdir -p build
	$(CC) $(CFLAGS) -Iinclude test/test_all.c $(SRC) -o $@

clean:
	rm -rf build

# ---- AP1 board firmware (ATmega328P, 8 MHz internal): make avr -> release/ap1_{rhymes,lamp,cricket}_8MHz.hex
ARD ?= /usr/share/arduino/hardware/arduino/avr
AVRF = -mmcu=atmega328p -DF_CPU=8000000L -DARDUINO=10806 -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -Iinclude
avr:
	@mkdir -p build/avrcore release
	@for f in $(ARD)/cores/arduino/*.c; do avr-gcc $(AVRF) -c $$f -o build/avrcore/$$(basename $$f).o; done
	@for f in $(ARD)/cores/arduino/*.cpp; do avr-g++ $(AVRF) -fno-exceptions -c $$f -o build/avrcore/$$(basename $$f).o; done
	@for f in $(ARD)/cores/arduino/*.S; do avr-gcc -mmcu=atmega328p -DF_CPU=8000000L -x assembler-with-cpp -I$(ARD)/cores/arduino -c $$f -o build/avrcore/$$(basename $$f).o 2>/dev/null; done
	@avr-ar rcs build/avrcore.a build/avrcore/*.o
	@for p in 1:rhymes 3:lamp 4:cricket; do n=$${p%%:*}; nm=$${p#*:}; \
	 avr-g++ $(AVRF) -Wall -Wextra -fno-exceptions -DPRODUCT=$$n -c src_avr/main_ap1.cpp -o build/main_$$nm.o && \
	 for c in src/*.c; do avr-gcc $(AVRF) -Wall -Wextra -std=gnu99 -c $$c -o build/$$(basename $$c .c)_avr.o; done && \
	 avr-gcc -mmcu=atmega328p -Wl,--gc-sections build/main_$$nm.o build/*_avr.o build/avrcore.a -lm -o build/ap1_$$nm.elf && \
	 avr-objcopy -O ihex -R .eeprom build/ap1_$$nm.elf release/ap1_$${nm}_8MHz.hex && echo "$$nm: $$(avr-size -C --mcu=atmega328p build/ap1_$$nm.elf | grep -E 'Program|Data' | tr -s ' ' | tr '\n' ' ')"; done
