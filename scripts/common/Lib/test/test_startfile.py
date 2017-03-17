# Embedded file name: scripts/common/Lib/test/test_startfile.py
import unittest
from test import test_support
import os
from os import path
from time import sleep
startfile = test_support.get_attribute(os, 'startfile')

class TestCase(unittest.TestCase):

    def test_nonexisting(self):
        self.assertRaises(OSError, startfile, 'nonexisting.vbs')

    def test_nonexisting_u(self):
        self.assertRaises(OSError, startfile, u'nonexisting.vbs')

    def test_empty(self):
        empty = path.join(path.dirname(__file__), 'empty.vbs')
        startfile(empty)
        startfile(empty, 'open')
        sleep(0.1)

    def test_empty_u(self):
        empty = path.join(path.dirname(__file__), 'empty.vbs')
        startfile(unicode(empty, 'mbcs'))
        startfile(unicode(empty, 'mbcs'), 'open')
        sleep(0.1)


def test_main():
    test_support.run_unittest(TestCase)


if __name__ == '__main__':
    test_main()