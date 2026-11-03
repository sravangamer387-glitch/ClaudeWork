/* Minimal Unity-compatible test harness for building the TRISHNA tests with plain gcc when PlatformIO (and its bundled Unity)
 * is not available. Implements only the macros used in test/test_core/test_core.c. With PlatformIO, the real Unity is used instead. */
#ifndef TRISHNA_UNITY_SHIM_H
#define TRISHNA_UNITY_SHIM_H
#include <stdio.h>
#include <math.h>
#include <setjmp.h>
#include <stdint.h>
void setUp(void);
void tearDown(void);
static int u_tests, u_fail; static jmp_buf u_jmp; static const char *u_name;
#define U_FAIL(msg, line) do { printf("%s:%d:%s:FAIL: %s\n", __FILE__, line, u_name, msg); longjmp(u_jmp, 1); } while (0)
#define UNITY_BEGIN() (u_tests = 0, u_fail = 0)
#define UNITY_END() (printf("\n-----------------------\n%d Tests %d Failures 0 Ignored\n%s\n", u_tests, u_fail, u_fail ? "FAIL" : "OK"), u_fail)
#define RUN_TEST(fn) do { u_name = #fn; u_tests++; setUp(); if (setjmp(u_jmp) == 0) { fn(); printf("%s:%d:%s:PASS\n", __FILE__, __LINE__, #fn); } else u_fail++; tearDown(); } while (0)
#define U_CMP(e, a, fmt, T) do { T _e = (T)(e), _a = (T)(a); if (_e != _a) { char _m[160]; snprintf(_m, sizeof _m, "Expected " fmt " Was " fmt, _e, _a); U_FAIL(_m, __LINE__); } } while (0)
#define TEST_ASSERT_EQUAL_INT(e, a) U_CMP(e, a, "%d", int)
#define TEST_ASSERT_EQUAL_INT16(e, a) U_CMP(e, a, "%d", int)
#define TEST_ASSERT_EQUAL_UINT8(e, a) U_CMP(e, a, "%u", unsigned)
#define TEST_ASSERT_EQUAL_UINT16(e, a) U_CMP(e, a, "%u", unsigned)
#define TEST_ASSERT_EQUAL_UINT32(e, a) U_CMP(e, a, "%lu", unsigned long)
#define TEST_ASSERT_EQUAL_HEX8(e, a) U_CMP(e, a, "0x%02X", unsigned)
#define TEST_ASSERT_EQUAL_HEX16(e, a) U_CMP(e, a, "0x%04X", unsigned)
#define TEST_ASSERT_TRUE(c) do { if (!(c)) U_FAIL("Expected TRUE: " #c, __LINE__); } while (0)
#define TEST_ASSERT_FALSE(c) do { if (c) U_FAIL("Expected FALSE: " #c, __LINE__); } while (0)
#define TEST_ASSERT_FLOAT_WITHIN(d, e, a) do { double _d = (d), _e = (e), _a = (a); if (!(fabs(_e - _a) <= _d)) { char _m[160]; snprintf(_m, sizeof _m, "Expected %g +/- %g Was %g", _e, _d, _a); U_FAIL(_m, __LINE__); } } while (0)
#endif
