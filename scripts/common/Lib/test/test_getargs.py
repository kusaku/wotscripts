# Embedded file name: scripts/common/Lib/test/test_getargs.py
"""
Test the internal getargs.c implementation

 PyArg_ParseTuple() is defined here.

The test here is not intended to test all of the module, just the
single case that failed between 2.1 and 2.2a2.
"""
import marshal
import unittest
from test import test_support

class GetArgsTest(unittest.TestCase):

    def test_with_marshal(self):
        arg = unicode('\\222', 'unicode-escape')
        self.assertRaises(UnicodeError, marshal.loads, arg)


def test_main():
    test_support.run_unittest(GetArgsTest)


if __name__ == '__main__':
    test_main()