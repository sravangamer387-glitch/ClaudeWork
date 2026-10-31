# Builds the five prototype firmwares for an Arduino Nano (ATmega328P, 16 MHz) with avr-gcc and the Arduino AVR core.
#   sudo apt-get install gcc-avr avr-libc binutils-avr arduino-core-avr
#   make            -> build/<product>.hex + a size report;   make test -> host tests (gcc only)
ARD  = /usr/share/arduino/hardware/arduino/avr
MCU  = atmega328p
COMMON = -mmcu=$(MCU) -DF_CPU=16000000L -DARDUINO=10806 -DARDUINO_AVR_NANO -DARDUINO_ARCH_AVR -Os -ffunction-sections -fdata-sections -Wall
INC  = -I$(ARD)/cores/arduino -I$(ARD)/variants/eightanaloginputs -I$(ARD)/libraries/SoftwareSerial/src -I../../electronics-toys/wave1/firmware/include -Ilib -Isrc
CFLAGS   = $(COMMON) -std=gnu99
CXXFLAGS = $(COMMON) -std=gnu++11 -fno-exceptions -fno-threadsafe-statics -fpermissive
PRODUCTS = rhymes lamp cricket beatlight midi
CORE_C   = $(wildcard $(ARD)/cores/arduino/*.c)
CORE_CPP = $(wildcard $(ARD)/cores/arduino/*.cpp) $(ARD)/libraries/SoftwareSerial/src/SoftwareSerial.cpp
CORE_S   = $(wildcard $(ARD)/cores/arduino/*.S)
AP1_SRC  = ../../electronics-toys/wave1/firmware/src/ap1_core.c ../../electronics-toys/wave1/firmware/src/app_rhymes.c \
           ../../electronics-toys/wave1/firmware/src/app_lamp.c ../../electronics-toys/wave1/firmware/src/app_cricket.c

.PHONY: all test clean
all: $(addprefix build/,$(addsuffix .hex,$(PRODUCTS)))
	@echo; echo "=== size (flash limit 30720 B on Nano with bootloader, SRAM 2048 B) ==="
	@for p in $(PRODUCTS); do printf "%-10s" $$p; avr-size -C --mcu=$(MCU) build/$$p.elf | grep -E "Program:|Data:" | tr '\n' ' '; echo; done

build/core.a: $(CORE_C) $(CORE_CPP) $(CORE_S)
	@mkdir -p build/core
	@for f in $(CORE_C);   do avr-gcc $(CFLAGS)   $(INC) -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(CORE_CPP); do avr-g++ $(CXXFLAGS) $(INC) -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	@for f in $(CORE_S);   do avr-gcc $(COMMON) -x assembler-with-cpp $(INC) -c $$f -o build/core/$$(basename $$f).o || exit 1; done
	avr-gcc-ar rcs $@ build/core/*.o 2>/dev/null || avr-ar rcs $@ build/core/*.o

define BUILD
build/$(1).elf: src/main_$(1).cpp src/hal_nano.cpp lib/dj_core.c $(AP1_SRC) build/core.a
	@mkdir -p build/$(1)
	avr-g++ $(CXXFLAGS) -DPRODUCT_$(2) $(INC) -c src/main_$(1).cpp -o build/$(1)/main.o
	avr-g++ $(CXXFLAGS) -DPRODUCT_$(2) $(INC) -c src/hal_nano.cpp  -o build/$(1)/hal.o
	avr-gcc $(CFLAGS) $(INC) -c lib/dj_core.c -o build/$(1)/dj.o
	@i=0; for f in $(AP1_SRC); do avr-gcc $(CFLAGS) $(INC) -c $$$$f -o build/$(1)/ap1_$$$$i.o; i=$$$$((i+1)); done
	avr-gcc -mmcu=$(MCU) -Wl,--gc-sections build/$(1)/*.o build/core.a -lm -o $$@
build/$(1).hex: build/$(1).elf
	avr-objcopy -O ihex -R .eeprom $$< $$@
endef
$(eval $(call BUILD,rhymes,RHYMES))
$(eval $(call BUILD,lamp,LAMP))
$(eval $(call BUILD,cricket,CRICKET))
$(eval $(call BUILD,beatlight,BEATLIGHT))
$(eval $(call BUILD,midi,MIDI))

test:
	gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -D_GNU_SOURCE test/test_dj.c lib/dj_core.c -lm -o build/test_dj 2>/dev/null || (mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -D_GNU_SOURCE test/test_dj.c lib/dj_core.c -lm -o build/test_dj)
	./build/test_dj
clean:
	rm -rf build
