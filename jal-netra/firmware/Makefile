.PHONY: test m4
test:
	@mkdir -p build && gcc -std=c99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined lib/jn_core.c test/test_jn.c -lm -o build/test_jn && ./build/test_jn
m4:   # compile the core for the STM32G4 (Cortex-M4F) to check it builds warning-free and see the size
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -Os -std=c99 -Wall -Wextra -Wshadow -ffunction-sections -c lib/jn_core.c -o build/jn_core_m4.o && arm-none-eabi-size build/jn_core_m4.o
