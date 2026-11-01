.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -Wno-misleading-indentation -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_rv.c lib/rv_nav.c -lm -o build/test_rv && ./build/test_rv
clean:
	rm -rf build
