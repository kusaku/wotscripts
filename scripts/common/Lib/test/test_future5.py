# Embedded file name: scripts/common/Lib/test/test_future5.py
from __future__ import unicode_literals, print_function
import sys
import unittest
from . import test_support

class TestMultipleFeatures(unittest.TestCase):

    def test_unicode_literals(self):
        self.assertIsInstance(u'', unicode)

    def test_print_function(self):
        with test_support.captured_output(u'stderr') as s:
            print(u'foo', file=sys.stderr)
        self.assertEqual(s.getvalue(), u'foo\n')


def test_main():
    test_support.run_unittest(TestMultipleFeatures)