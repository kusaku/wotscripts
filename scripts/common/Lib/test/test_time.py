# Embedded file name: scripts/common/Lib/test/test_time.py
from test import test_support
import time
import unittest
import sys

class TimeTestCase(unittest.TestCase):

    def setUp(self):
        self.t = time.time()

    def test_data_attributes(self):
        time.altzone
        time.daylight
        time.timezone
        time.tzname

    def test_clock(self):
        time.clock()

    def test_conversions(self):
        self.assertTrue(time.ctime(self.t) == time.asctime(time.localtime(self.t)))
        self.assertTrue(long(time.mktime(time.localtime(self.t))) == long(self.t))

    def test_sleep(self):
        time.sleep(1.2)

    def test_strftime(self):
        tt = time.gmtime(self.t)
        for directive in ('a', 'A', 'b', 'B', 'c', 'd', 'H', 'I', 'j', 'm', 'M', 'p', 'S', 'U', 'w', 'W', 'x', 'X', 'y', 'Y', 'Z', '%'):
            format = ' %' + directive
            try:
                time.strftime(format, tt)
            except ValueError:
                self.fail('conversion specifier: %r failed.' % format)

        if sys.platform.startswith('win'):
            with self.assertRaises(ValueError):
                time.strftime('%f')

    def test_strftime_bounds_checking(self):
        self.assertRaises(ValueError, time.strftime, '', (1899, 1, 1, 0, 0, 0, 0, 1, -1))
        if time.accept2dyear:
            self.assertRaises(ValueError, time.strftime, '', (-1, 1, 1, 0, 0, 0, 0, 1, -1))
            self.assertRaises(ValueError, time.strftime, '', (100, 1, 1, 0, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, -1, 1, 0, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 13, 1, 0, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, -1, 0, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 32, 0, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, -1, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 24, 0, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, -1, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 60, 0, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 0, -1, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 0, 62, 0, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 0, 0, -2, 1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 0, 0, 0, -1, -1))
        self.assertRaises(ValueError, time.strftime, '', (1900, 1, 1, 0, 0, 0, 0, 367, -1))

    def test_default_values_for_zero(self):
        expected = '2000 01 01 00 00 00 1 001'
        result = time.strftime('%Y %m %d %H %M %S %w %j', (0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(expected, result)

    def test_strptime(self):
        tt = time.gmtime(self.t)
        for directive in ('a', 'A', 'b', 'B', 'c', 'd', 'H', 'I', 'j', 'm', 'M', 'p', 'S', 'U', 'w', 'W', 'x', 'X', 'y', 'Y', 'Z', '%'):
            format = '%' + directive
            strf_output = time.strftime(format, tt)
            try:
                time.strptime(strf_output, format)
            except ValueError:
                self.fail("conversion specifier %r failed with '%s' input." % (format, strf_output))

    def test_asctime(self):
        time.asctime(time.gmtime(self.t))
        self.assertRaises(TypeError, time.asctime, 0)
        self.assertRaises(TypeError, time.asctime, ())
        try:
            time.asctime((12345, 1, 1, 0, 0, 0, 0, 1, 0))
        except ValueError:
            pass

    @unittest.skipIf(not hasattr(time, 'tzset'), 'time module has no attribute tzset')
    def test_tzset(self):
        from os import environ
        xmas2002 = 1040774400.0
        eastern = 'EST+05EDT,M4.1.0,M10.5.0'
        victoria = 'AEST-10AEDT-11,M10.5.0,M3.5.0'
        utc = 'UTC+0'
        org_TZ = environ.get('TZ', None)
        try:
            environ['TZ'] = eastern
            time.tzset()
            environ['TZ'] = utc
            time.tzset()
            self.assertEqual(time.gmtime(xmas2002), time.localtime(xmas2002))
            self.assertEqual(time.daylight, 0)
            self.assertEqual(time.timezone, 0)
            self.assertEqual(time.localtime(xmas2002).tm_isdst, 0)
            environ['TZ'] = eastern
            time.tzset()
            self.assertNotEqual(time.gmtime(xmas2002), time.localtime(xmas2002))
            self.assertEqual(time.tzname, ('EST', 'EDT'))
            self.assertEqual(len(time.tzname), 2)
            self.assertEqual(time.daylight, 1)
            self.assertEqual(time.timezone, 18000)
            self.assertEqual(time.altzone, 14400)
            self.assertEqual(time.localtime(xmas2002).tm_isdst, 0)
            self.assertEqual(len(time.tzname), 2)
            environ['TZ'] = victoria
            time.tzset()
            self.assertNotEqual(time.gmtime(xmas2002), time.localtime(xmas2002))
            self.assertIn(time.tzname[0], 'AESTEST', time.tzname[0])
            self.assertTrue(time.tzname[1] == 'AEDT', str(time.tzname[1]))
            self.assertEqual(len(time.tzname), 2)
            self.assertEqual(time.daylight, 1)
            self.assertEqual(time.timezone, -36000)
            self.assertEqual(time.altzone, -39600)
            self.assertEqual(time.localtime(xmas2002).tm_isdst, 1)
        finally:
            if org_TZ is not None:
                environ['TZ'] = org_TZ
            elif environ.has_key('TZ'):
                del environ['TZ']
            time.tzset()

        return

    def test_insane_timestamps(self):
        for func in (time.ctime, time.gmtime, time.localtime):
            for unreasonable in (-1e+200, 1e+200):
                self.assertRaises(ValueError, func, unreasonable)

    def test_ctime_without_arg(self):
        time.ctime()
        time.ctime(None)
        return

    def test_gmtime_without_arg(self):
        gt0 = time.gmtime()
        gt1 = time.gmtime(None)
        t0 = time.mktime(gt0)
        t1 = time.mktime(gt1)
        self.assertTrue(0 <= t1 - t0 < 0.2)
        return

    def test_localtime_without_arg(self):
        lt0 = time.localtime()
        lt1 = time.localtime(None)
        t0 = time.mktime(lt0)
        t1 = time.mktime(lt1)
        self.assertTrue(0 <= t1 - t0 < 0.2)
        return

    def test_mktime(self):
        for t in (-2, -1, 0, 1):
            try:
                tt = time.localtime(t)
            except (OverflowError, ValueError):
                pass
            else:
                self.assertEqual(time.mktime(tt), t)


def test_main():
    test_support.run_unittest(TimeTestCase)


if __name__ == '__main__':
    test_main()