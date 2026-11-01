.PHONY: test clean
test:
	@mkdir -p build && gcc -std=gnu99 -Wall -Wextra -Wshadow -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined -Ilib -Itest test/test_gt.c lib/gt_feat.c -lm -o build/test_gt && ./build/test_gt
clean:
	rm -rf build
