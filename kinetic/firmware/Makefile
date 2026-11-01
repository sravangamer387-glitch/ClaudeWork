.PHONY: test clean
CF = -std=gnu99 -Wall -Wextra -Wshadow -Wno-misleading-indentation -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib
test:
	@mkdir -p build
	gcc $(CF) test/test_kn.c lib/kn_motion.c -lm -o build/test_kn && ./build/test_kn | tail -3
	gcc $(CF) test/test_vib.c lib/kn_vib.c -lm -o build/test_vib && ./build/test_vib
clean:
	rm -rf build
