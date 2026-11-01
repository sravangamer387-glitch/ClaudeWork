.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -Wno-misleading-indentation -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_kn.c lib/kn_motion.c -lm -o build/test_kn && ./build/test_kn
clean:
	rm -rf build
