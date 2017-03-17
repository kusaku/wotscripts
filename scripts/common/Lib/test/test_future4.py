# Embedded file name: scripts/common/Lib/test/test_future4.py
from __future__ import unicode_literals
import unittest
from test import test_support

class TestFuture(unittest.TestCase):

    def assertType(self, obj, typ):
        self.assertTrue(type(obj) is typ, u'type(%r) is %r, not %r' % (obj, type(obj), typ))

    def test_unicode_strings(self):
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType(u' ', unicode)
        self.assertType('', str)
        self.assertType('', str)
        self.assertType('', str)
        self.assertType('', str)
        self.assertType(' ', str)
        self.assertType(' ', str)
        self.assertType(' ', str)
        self.assertType(' ', str)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)
        self.assertType(u'', unicode)


def test_main():
    test_support.run_unittest(TestFuture)


if __name__ == u'__main__':
    test_main()