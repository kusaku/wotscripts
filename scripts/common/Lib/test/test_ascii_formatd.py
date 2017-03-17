# Embedded file name: scripts/common/Lib/test/test_ascii_formatd.py
import unittest
from test.test_support import check_warnings, run_unittest, import_module
import_module('_ctypes')
from ctypes import pythonapi, create_string_buffer, sizeof, byref, c_double
PyOS_ascii_formatd = pythonapi.PyOS_ascii_formatd

class FormatDeprecationTests(unittest.TestCase):

    def test_format_deprecation(self):
        buf = create_string_buffer(' ' * 100)
        with check_warnings(('PyOS_ascii_formatd is deprecated', DeprecationWarning)):
            PyOS_ascii_formatd(byref(buf), sizeof(buf), '%+.10f', c_double(10.0))
            self.assertEqual(buf.value, '+10.0000000000')


class FormatTests(unittest.TestCase):

    def test_format(self):
        buf = create_string_buffer(' ' * 100)
        tests = [('%f', 100.0),
         ('%g', 100.0),
         ('%#g', 100.0),
         ('%#.2g', 100.0),
         ('%#.2g', 123.4567),
         ('%#.2g', 1.234567e+200),
         ('%e', 1.234567e+200),
         ('%e', 1.234),
         ('%+e', 1.234),
         ('%-e', 1.234)]
        with check_warnings(('PyOS_ascii_formatd is deprecated', DeprecationWarning)):
            for format, val in tests:
                PyOS_ascii_formatd(byref(buf), sizeof(buf), format, c_double(val))
                self.assertEqual(buf.value, format % val)


def test_main():
    run_unittest(FormatDeprecationTests, FormatTests)


if __name__ == '__main__':
    test_main()