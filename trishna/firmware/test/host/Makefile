# Build and run the TRISHNA core unit tests with plain gcc (no PlatformIO needed): make -C test/host
CORE := ../../lib/trishna_core/src
CFLAGS := -std=c11 -O1 -g -Wall -Wextra -Werror -Wno-unused-function -I. -I$(CORE)
SRC := ../test_core/test_core.c $(CORE)/trishna_frame.c $(CORE)/trishna_filters.c $(CORE)/trishna_sense.c $(CORE)/trishna_fsm.c

run: test_core
	./test_core

test_core: $(SRC) unity.h $(wildcard $(CORE)/*.h)
	$(CC) $(CFLAGS) -o $@ $(SRC) -lm

clean:
	rm -f test_core golden_frames.bin

.PHONY: run clean
