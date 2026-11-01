.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_mn.c lib/mn_core.c -lm -o build/test_mn && ./build/test_mn
clean:
	rm -rf build
