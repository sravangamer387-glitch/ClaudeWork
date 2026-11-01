.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_bt.c lib/bt_core.c -lm -o build/test_bt && ./build/test_bt
clean:
	rm -rf build
