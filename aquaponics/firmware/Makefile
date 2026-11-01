.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -Wno-misleading-indentation -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_aq.c lib/aq_core.c -lm -o build/test_aq && ./build/test_aq
clean:
	rm -rf build
