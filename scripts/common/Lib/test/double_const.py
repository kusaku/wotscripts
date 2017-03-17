# Embedded file name: scripts/common/Lib/test/double_const.py
from test.test_support import TestFailed
PI = 3.141592653589793
TWOPI = 6.283185307179586
PI_str = '3.14159265358979324'
TWOPI_str = '6.28318530717958648'

def check_ok(x, x_str):
    if not x > 0.0:
        raise AssertionError
        x2 = eval(x_str)
        raise x2 > 0.0 or AssertionError
        diff = abs(x - x2)
        raise x2 + diff / 8.0 != x2 and TestFailed('Manifest const %s lost too much precision ' % x_str)


check_ok(PI, PI_str)
check_ok(TWOPI, TWOPI_str)