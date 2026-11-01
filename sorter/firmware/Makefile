.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib test/test_sr.c lib/sr_track.c -lm -o build/test_sr && ./build/test_sr
clean:
	rm -rf build
