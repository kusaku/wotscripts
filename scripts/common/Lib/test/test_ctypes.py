# Embedded file name: scripts/common/Lib/test/test_ctypes.py
import unittest
from test.test_support import run_unittest, import_module
import_module('_ctypes')

def test_main():
    import ctypes.test
    skipped, testcases = ctypes.test.get_tests(ctypes.test, 'test_*.py', verbosity=0)
    suites = [ unittest.makeSuite(t) for t in testcases ]
    run_unittest(unittest.TestSuite(suites))


if __name__ == '__main__':
    test_main()