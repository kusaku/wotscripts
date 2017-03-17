# Embedded file name: scripts/common/Lib/test/test_stringprep.py
import unittest
from test import test_support
from stringprep import *

class StringprepTests(unittest.TestCase):

    def test(self):
        self.assertTrue(in_table_a1(u'\u0221'))
        self.assertFalse(in_table_a1(u'\u0222'))
        self.assertTrue(in_table_b1(u'\xad'))
        self.assertFalse(in_table_b1(u'\xae'))
        self.assertTrue(map_table_b2(u'A'), u'a')
        self.assertTrue(map_table_b2(u'a'), u'a')
        self.assertTrue(map_table_b3(u'A'), u'a')
        self.assertTrue(map_table_b3(u'a'), u'a')
        self.assertTrue(in_table_c11(u' '))
        self.assertFalse(in_table_c11(u'!'))
        self.assertTrue(in_table_c12(u'\xa0'))
        self.assertFalse(in_table_c12(u'\xa1'))
        self.assertTrue(in_table_c12(u'\xa0'))
        self.assertFalse(in_table_c12(u'\xa1'))
        self.assertTrue(in_table_c11_c12(u'\xa0'))
        self.assertFalse(in_table_c11_c12(u'\xa1'))
        self.assertTrue(in_table_c21(u'\x1f'))
        self.assertFalse(in_table_c21(u' '))
        self.assertTrue(in_table_c22(u'\x9f'))
        self.assertFalse(in_table_c22(u'\xa0'))
        self.assertTrue(in_table_c21_c22(u'\x9f'))
        self.assertFalse(in_table_c21_c22(u'\xa0'))
        self.assertTrue(in_table_c3(u'\ue000'))
        self.assertFalse(in_table_c3(u'\uf900'))
        self.assertTrue(in_table_c4(u'\uffff'))
        self.assertFalse(in_table_c4(u'\x00'))
        self.assertTrue(in_table_c5(u'\ud800'))
        self.assertFalse(in_table_c5(u'\ud7ff'))
        self.assertTrue(in_table_c6(u'\ufff9'))
        self.assertFalse(in_table_c6(u'\ufffe'))
        self.assertTrue(in_table_c7(u'\u2ff0'))
        self.assertFalse(in_table_c7(u'\u2ffc'))
        self.assertTrue(in_table_c8(u'\u0340'))
        self.assertFalse(in_table_c8(u'\u0342'))
        self.assertTrue(in_table_d1(u'\u05be'))
        self.assertFalse(in_table_d1(u'\u05bf'))
        self.assertTrue(in_table_d2(u'A'))
        self.assertFalse(in_table_d2(u'@'))


def test_main():
    test_support.run_unittest(StringprepTests)


if __name__ == '__main__':
    test_main()