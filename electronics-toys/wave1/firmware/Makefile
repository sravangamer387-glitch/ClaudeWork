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
