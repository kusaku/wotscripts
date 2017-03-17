# Embedded file name: scripts/common/Lib/test/test_future3.py
from __future__ import nested_scopes
from __future__ import division
import unittest
from test import test_support
x = 2

def nester():
    x = 3

    def inner():
        return x

    return inner()


class TestFuture(unittest.TestCase):

    def test_floor_div_operator(self):
        self.assertEqual(3, 3)

    def test_true_div_as_default(self):
        self.assertAlmostEqual(3.5, 3.5)

    def test_nested_scopes(self):
        self.assertEqual(nester(), 3)


def test_main():
    test_support.run_unittest(TestFuture)


if __name__ == '__main__':
    test_main()