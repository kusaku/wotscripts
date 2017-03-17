# Embedded file name: scripts/common/Lib/test/test_datetime.py
"""Test date/time type.

See http://www.zope.org/Members/fdrake/DateTimeWiki/TestCases
"""
from __future__ import division
import sys
import pickle
import cPickle
import unittest
from test import test_support
from datetime import MINYEAR, MAXYEAR
from datetime import timedelta
from datetime import tzinfo
from datetime import time
from datetime import date, datetime
pickle_choices = [ (pickler, unpickler, proto) for pickler in (pickle, cPickle) for unpickler in (pickle, cPickle) for proto in range(3) ]
if not len(pickle_choices) == 2 * 2 * 3:
    raise AssertionError
    OTHERSTUFF = (10,
     10L,
     34.5,
     'abc',
     {},
     [],
     ())

    class TestModule(unittest.TestCase):

        def test_constants(self):
            import datetime
            self.assertEqual(datetime.MINYEAR, 1)
            self.assertEqual(datetime.MAXYEAR, 9999)


    class FixedOffset(tzinfo):

        def __init__(self, offset, name, dstoffset = 42):
            if isinstance(offset, int):
                offset = timedelta(minutes=offset)
            if isinstance(dstoffset, int):
                dstoffset = timedelta(minutes=dstoffset)
            self.__offset = offset
            self.__name = name
            self.__dstoffset = dstoffset

        def __repr__(self):
            return self.__name.lower()

        def utcoffset(self, dt):
            return self.__offset

        def tzname(self, dt):
            return self.__name

        def dst(self, dt):
            return self.__dstoffset


    class PicklableFixedOffset(FixedOffset):

        def __init__(self, offset = None, name = None, dstoffset = None):
            FixedOffset.__init__(self, offset, name, dstoffset)


    class TestTZInfo(unittest.TestCase):

        def test_non_abstractness(self):
            useless = tzinfo()
            dt = datetime.max
            self.assertRaises(NotImplementedError, useless.tzname, dt)
            self.assertRaises(NotImplementedError, useless.utcoffset, dt)
            self.assertRaises(NotImplementedError, useless.dst, dt)

        def test_subclass_must_override(self):

            class NotEnough(tzinfo):

                def __init__(self, offset, name):
                    self.__offset = offset
                    self.__name = name

            self.assertTrue(issubclass(NotEnough, tzinfo))
            ne = NotEnough(3, 'NotByALongShot')
            self.assertIsInstance(ne, tzinfo)
            dt = datetime.now()
            self.assertRaises(NotImplementedError, ne.tzname, dt)
            self.assertRaises(NotImplementedError, ne.utcoffset, dt)
            self.assertRaises(NotImplementedError, ne.dst, dt)

        def test_normal(self):
            fo = FixedOffset(3, 'Three')
            self.assertIsInstance(fo, tzinfo)
            for dt in (datetime.now(), None):
                self.assertEqual(fo.utcoffset(dt), timedelta(minutes=3))
                self.assertEqual(fo.tzname(dt), 'Three')
                self.assertEqual(fo.dst(dt), timedelta(minutes=42))

            return

        def test_pickling_base(self):
            orig = tzinfo.__new__(tzinfo)
            self.assertTrue(type(orig) is tzinfo)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertTrue(type(derived) is tzinfo)

        def test_pickling_subclass(self):
            offset = timedelta(minutes=-300)
            orig = PicklableFixedOffset(offset, 'cookie')
            self.assertIsInstance(orig, tzinfo)
            self.assertTrue(type(orig) is PicklableFixedOffset)
            self.assertEqual(orig.utcoffset(None), offset)
            self.assertEqual(orig.tzname(None), 'cookie')
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertIsInstance(derived, tzinfo)
                self.assertTrue(type(derived) is PicklableFixedOffset)
                self.assertEqual(derived.utcoffset(None), offset)
                self.assertEqual(derived.tzname(None), 'cookie')

            return


    class HarmlessMixedComparison():

        def test_harmless_mixed_comparison(self):
            me = self.theclass(1, 1, 1)
            self.assertFalse(me == ())
            self.assertTrue(me != ())
            self.assertFalse(() == me)
            self.assertTrue(() != me)
            self.assertIn(me, [1,
             20L,
             [],
             me])
            self.assertIn([], [me,
             1,
             20L,
             []])

        def test_harmful_mixed_comparison(self):
            me = self.theclass(1, 1, 1)
            self.assertRaises(TypeError, lambda : me < ())
            self.assertRaises(TypeError, lambda : me <= ())
            self.assertRaises(TypeError, lambda : me > ())
            self.assertRaises(TypeError, lambda : me >= ())
            self.assertRaises(TypeError, lambda : () < me)
            self.assertRaises(TypeError, lambda : () <= me)
            self.assertRaises(TypeError, lambda : () > me)
            self.assertRaises(TypeError, lambda : () >= me)
            self.assertRaises(TypeError, cmp, (), me)
            self.assertRaises(TypeError, cmp, me, ())


    class TestTimeDelta(HarmlessMixedComparison, unittest.TestCase):
        theclass = timedelta

        def test_constructor(self):
            eq = self.assertEqual
            td = timedelta
            eq(td(), td(weeks=0, days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0))
            eq(td(1), td(days=1))
            eq(td(0, 1), td(seconds=1))
            eq(td(0, 0, 1), td(microseconds=1))
            eq(td(weeks=1), td(days=7))
            eq(td(days=1), td(hours=24))
            eq(td(hours=1), td(minutes=60))
            eq(td(minutes=1), td(seconds=60))
            eq(td(seconds=1), td(milliseconds=1000))
            eq(td(milliseconds=1), td(microseconds=1000))
            eq(td(weeks=0.14285714285714285), td(days=1))
            eq(td(days=0.041666666666666664), td(hours=1))
            eq(td(hours=0.016666666666666666), td(minutes=1))
            eq(td(minutes=0.016666666666666666), td(seconds=1))
            eq(td(seconds=0.001), td(milliseconds=1))
            eq(td(milliseconds=0.001), td(microseconds=1))

        def test_computations(self):
            eq = self.assertEqual
            td = timedelta
            a = td(7)
            b = td(0, 60)
            c = td(0, 0, 1000)
            eq(a + b + c, td(7, 60, 1000))
            eq(a - b, td(6, 86340))
            eq(-a, td(-7))
            eq(+a, td(7))
            eq(-b, td(-1, 86340))
            eq(-c, td(-1, 86399, 999000))
            eq(abs(a), a)
            eq(abs(-a), a)
            eq(td(6, 86400), a)
            eq(td(0, 0, 60000000), b)
            eq(a * 10, td(70))
            eq(a * 10, 10 * a)
            eq(a * 10L, 10 * a)
            eq(b * 10, td(0, 600))
            eq(10 * b, td(0, 600))
            eq(b * 10L, td(0, 600))
            eq(c * 10, td(0, 0, 10000))
            eq(10 * c, td(0, 0, 10000))
            eq(c * 10L, td(0, 0, 10000))
            eq(a * -1, -a)
            eq(b * -2, -b - b)
            eq(c * -2, -c + -c)
            eq(b * 1440, b * 60 * 24)
            eq(b * 1440, 60 * b * 24)
            eq(c * 1000, td(0, 1))
            eq(1000 * c, td(0, 1))
            eq(a // 7, td(1))
            eq(b // 10, td(0, 6))
            eq(c // 1000, td(0, 0, 1))
            eq(a // 10, td(0, 60480))
            eq(a // 3600000, td(0, 0, 168000))
            eq(td(999999999, 86399, 999999) - td(999999999, 86399, 999998), td(0, 0, 1))
            eq(td(999999999, 1, 1) - td(999999999, 1, 0), td(0, 0, 1))

        def test_disallowed_computations(self):
            a = timedelta(42)
            for i in (1, 1L, 1.0):
                self.assertRaises(TypeError, lambda : a + i)
                self.assertRaises(TypeError, lambda : a - i)
                self.assertRaises(TypeError, lambda : i + a)
                self.assertRaises(TypeError, lambda : i - a)

            x = 2.3
            self.assertRaises(TypeError, lambda : a * x)
            self.assertRaises(TypeError, lambda : x * a)
            self.assertRaises(TypeError, lambda : a / x)
            self.assertRaises(TypeError, lambda : x / a)
            self.assertRaises(TypeError, lambda : a // x)
            self.assertRaises(TypeError, lambda : x // a)
            for zero in (0, 0L):
                self.assertRaises(TypeError, lambda : zero // a)
                self.assertRaises(ZeroDivisionError, lambda : a // zero)

        def test_basic_attributes(self):
            days, seconds, us = (1, 7, 31)
            td = timedelta(days, seconds, us)
            self.assertEqual(td.days, days)
            self.assertEqual(td.seconds, seconds)
            self.assertEqual(td.microseconds, us)

        def test_total_seconds(self):
            td = timedelta(days=365)
            self.assertEqual(td.total_seconds(), 31536000.0)
            for total_seconds in [123456.789012,
             -123456.789012,
             0.123456,
             0,
             1000000.0]:
                td = timedelta(seconds=total_seconds)
                self.assertEqual(td.total_seconds(), total_seconds)

            for ms in [-1, -2, -123]:
                td = timedelta(microseconds=ms)
                self.assertEqual(td.total_seconds(), ((86400 * td.days + td.seconds) * 1000000 + td.microseconds) / 1000000)

        def test_carries(self):
            t1 = timedelta(days=100, weeks=-7, hours=-24 * 51, minutes=-3, seconds=12, microseconds=168000001.0)
            t2 = timedelta(microseconds=1)
            self.assertEqual(t1, t2)

        def test_hash_equality(self):
            t1 = timedelta(days=100, weeks=-7, hours=-24 * 51, minutes=-3, seconds=12, microseconds=168000000)
            t2 = timedelta()
            self.assertEqual(hash(t1), hash(t2))
            t1 += timedelta(weeks=7)
            t2 += timedelta(days=49)
            self.assertEqual(t1, t2)
            self.assertEqual(hash(t1), hash(t2))
            d = {t1: 1}
            d[t2] = 2
            self.assertEqual(len(d), 1)
            self.assertEqual(d[t1], 2)

        def test_pickling(self):
            args = (12, 34, 56)
            orig = timedelta(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_compare(self):
            t1 = timedelta(2, 3, 4)
            t2 = timedelta(2, 3, 4)
            self.assertTrue(t1 == t2)
            self.assertTrue(t1 <= t2)
            self.assertTrue(t1 >= t2)
            self.assertTrue(not t1 != t2)
            self.assertTrue(not t1 < t2)
            self.assertTrue(not t1 > t2)
            self.assertEqual(cmp(t1, t2), 0)
            self.assertEqual(cmp(t2, t1), 0)
            for args in ((3, 3, 3), (2, 4, 4), (2, 3, 5)):
                t2 = timedelta(*args)
                self.assertTrue(t1 < t2)
                self.assertTrue(t2 > t1)
                self.assertTrue(t1 <= t2)
                self.assertTrue(t2 >= t1)
                self.assertTrue(t1 != t2)
                self.assertTrue(t2 != t1)
                self.assertTrue(not t1 == t2)
                self.assertTrue(not t2 == t1)
                self.assertTrue(not t1 > t2)
                self.assertTrue(not t2 < t1)
                self.assertTrue(not t1 >= t2)
                self.assertTrue(not t2 <= t1)
                self.assertEqual(cmp(t1, t2), -1)
                self.assertEqual(cmp(t2, t1), 1)

            for badarg in OTHERSTUFF:
                self.assertEqual(t1 == badarg, False)
                self.assertEqual(t1 != badarg, True)
                self.assertEqual(badarg == t1, False)
                self.assertEqual(badarg != t1, True)
                self.assertRaises(TypeError, lambda : t1 <= badarg)
                self.assertRaises(TypeError, lambda : t1 < badarg)
                self.assertRaises(TypeError, lambda : t1 > badarg)
                self.assertRaises(TypeError, lambda : t1 >= badarg)
                self.assertRaises(TypeError, lambda : badarg <= t1)
                self.assertRaises(TypeError, lambda : badarg < t1)
                self.assertRaises(TypeError, lambda : badarg > t1)
                self.assertRaises(TypeError, lambda : badarg >= t1)

        def test_str(self):
            td = timedelta
            eq = self.assertEqual
            eq(str(td(1)), '1 day, 0:00:00')
            eq(str(td(-1)), '-1 day, 0:00:00')
            eq(str(td(2)), '2 days, 0:00:00')
            eq(str(td(-2)), '-2 days, 0:00:00')
            eq(str(td(hours=12, minutes=58, seconds=59)), '12:58:59')
            eq(str(td(hours=2, minutes=3, seconds=4)), '2:03:04')
            eq(str(td(weeks=-30, hours=23, minutes=12, seconds=34)), '-210 days, 23:12:34')
            eq(str(td(milliseconds=1)), '0:00:00.001000')
            eq(str(td(microseconds=3)), '0:00:00.000003')
            eq(str(td(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999)), '999999999 days, 23:59:59.999999')

        def test_roundtrip(self):
            for td in (timedelta(days=999999999, hours=23, minutes=59, seconds=59, microseconds=999999), timedelta(days=-999999999), timedelta(days=1, seconds=2, microseconds=3)):
                s = repr(td)
                self.assertTrue(s.startswith('datetime.'))
                s = s[9:]
                td2 = eval(s)
                self.assertEqual(td, td2)
                td2 = timedelta(td.days, td.seconds, td.microseconds)
                self.assertEqual(td, td2)

        def test_resolution_info(self):
            self.assertIsInstance(timedelta.min, timedelta)
            self.assertIsInstance(timedelta.max, timedelta)
            self.assertIsInstance(timedelta.resolution, timedelta)
            self.assertTrue(timedelta.max > timedelta.min)
            self.assertEqual(timedelta.min, timedelta(-999999999))
            self.assertEqual(timedelta.max, timedelta(999999999, 86399, 999999.0))
            self.assertEqual(timedelta.resolution, timedelta(0, 0, 1))

        def test_overflow(self):
            tiny = timedelta.resolution
            td = timedelta.min + tiny
            td -= tiny
            self.assertRaises(OverflowError, td.__sub__, tiny)
            self.assertRaises(OverflowError, td.__add__, -tiny)
            td = timedelta.max - tiny
            td += tiny
            self.assertRaises(OverflowError, td.__add__, tiny)
            self.assertRaises(OverflowError, td.__sub__, -tiny)
            self.assertRaises(OverflowError, lambda : -timedelta.max)

        def test_microsecond_rounding(self):
            td = timedelta
            eq = self.assertEqual
            eq(td(milliseconds=0.0004), td(0))
            eq(td(milliseconds=-0.0004), td(0))
            eq(td(milliseconds=0.0006), td(microseconds=1))
            eq(td(milliseconds=-0.0006), td(microseconds=-1))
            us_per_hour = 3600000000.0
            us_per_day = us_per_hour * 24
            eq(td(days=0.4 / us_per_day), td(0))
            eq(td(hours=0.2 / us_per_hour), td(0))
            eq(td(days=0.4 / us_per_day, hours=0.2 / us_per_hour), td(microseconds=1))
            eq(td(days=-0.4 / us_per_day), td(0))
            eq(td(hours=-0.2 / us_per_hour), td(0))
            eq(td(days=-0.4 / us_per_day, hours=-0.2 / us_per_hour), td(microseconds=-1))

        def test_massive_normalization(self):
            td = timedelta(microseconds=-1)
            self.assertEqual((td.days, td.seconds, td.microseconds), (-1, 86399, 999999))

        def test_bool(self):
            self.assertTrue(timedelta(1))
            self.assertTrue(timedelta(0, 1))
            self.assertTrue(timedelta(0, 0, 1))
            self.assertTrue(timedelta(microseconds=1))
            self.assertTrue(not timedelta(0))

        def test_subclass_timedelta(self):

            class T(timedelta):

                @staticmethod
                def from_td(td):
                    return T(td.days, td.seconds, td.microseconds)

                def as_hours(self):
                    sum = self.days * 24 + self.seconds / 3600.0 + self.microseconds / 3600000000.0
                    return round(sum)

            t1 = T(days=1)
            self.assertTrue(type(t1) is T)
            self.assertEqual(t1.as_hours(), 24)
            t2 = T(days=-1, seconds=-3600)
            self.assertTrue(type(t2) is T)
            self.assertEqual(t2.as_hours(), -25)
            t3 = t1 + t2
            self.assertTrue(type(t3) is timedelta)
            t4 = T.from_td(t3)
            self.assertTrue(type(t4) is T)
            self.assertEqual(t3.days, t4.days)
            self.assertEqual(t3.seconds, t4.seconds)
            self.assertEqual(t3.microseconds, t4.microseconds)
            self.assertEqual(str(t3), str(t4))
            self.assertEqual(t4.as_hours(), -1)


    class TestDateOnly(unittest.TestCase):

        def test_delta_non_days_ignored(self):
            dt = date(2000, 1, 2)
            delta = timedelta(days=1, hours=2, minutes=3, seconds=4, microseconds=5)
            days = timedelta(delta.days)
            self.assertEqual(days, timedelta(1))
            dt2 = dt + delta
            self.assertEqual(dt2, dt + days)
            dt2 = delta + dt
            self.assertEqual(dt2, dt + days)
            dt2 = dt - delta
            self.assertEqual(dt2, dt - days)
            delta = -delta
            days = timedelta(delta.days)
            self.assertEqual(days, timedelta(-2))
            dt2 = dt + delta
            self.assertEqual(dt2, dt + days)
            dt2 = delta + dt
            self.assertEqual(dt2, dt + days)
            dt2 = dt - delta
            self.assertEqual(dt2, dt - days)


    class SubclassDate(date):
        sub_var = 1


    class TestDate(HarmlessMixedComparison, unittest.TestCase):
        theclass = date

        def test_basic_attributes(self):
            dt = self.theclass(2002, 3, 1)
            self.assertEqual(dt.year, 2002)
            self.assertEqual(dt.month, 3)
            self.assertEqual(dt.day, 1)

        def test_roundtrip(self):
            for dt in (self.theclass(1, 2, 3), self.theclass.today()):
                s = repr(dt)
                self.assertTrue(s.startswith('datetime.'))
                s = s[9:]
                dt2 = eval(s)
                self.assertEqual(dt, dt2)
                dt2 = self.theclass(dt.year, dt.month, dt.day)
                self.assertEqual(dt, dt2)

        def test_ordinal_conversions(self):
            for y, m, d, n in [(1, 1, 1, 1),
             (1, 12, 31, 365),
             (2, 1, 1, 366),
             (1945, 11, 12, 710347)]:
                d = self.theclass(y, m, d)
                self.assertEqual(n, d.toordinal())
                fromord = self.theclass.fromordinal(n)
                self.assertEqual(d, fromord)
                if hasattr(fromord, 'hour'):
                    self.assertEqual(fromord.hour, 0)
                    self.assertEqual(fromord.minute, 0)
                    self.assertEqual(fromord.second, 0)
                    self.assertEqual(fromord.microsecond, 0)

            for year in xrange(MINYEAR, MAXYEAR + 1, 7):
                d = self.theclass(year, 1, 1)
                n = d.toordinal()
                d2 = self.theclass.fromordinal(n)
                self.assertEqual(d, d2)
                if year > 1:
                    d = self.theclass.fromordinal(n - 1)
                    d2 = self.theclass(year - 1, 12, 31)
                    self.assertEqual(d, d2)
                    self.assertEqual(d2.toordinal(), n - 1)

            dim = [31,
             28,
             31,
             30,
             31,
             30,
             31,
             31,
             30,
             31,
             30,
             31]
            for year, isleap in ((2000, True), (2002, False)):
                n = self.theclass(year, 1, 1).toordinal()
                for month, maxday in zip(range(1, 13), dim):
                    if month == 2 and isleap:
                        maxday += 1
                    for day in range(1, maxday + 1):
                        d = self.theclass(year, month, day)
                        self.assertEqual(d.toordinal(), n)
                        self.assertEqual(d, self.theclass.fromordinal(n))
                        n += 1

        def test_extreme_ordinals(self):
            a = self.theclass.min
            a = self.theclass(a.year, a.month, a.day)
            aord = a.toordinal()
            b = a.fromordinal(aord)
            self.assertEqual(a, b)
            self.assertRaises(ValueError, lambda : a.fromordinal(aord - 1))
            b = a + timedelta(days=1)
            self.assertEqual(b.toordinal(), aord + 1)
            self.assertEqual(b, self.theclass.fromordinal(aord + 1))
            a = self.theclass.max
            a = self.theclass(a.year, a.month, a.day)
            aord = a.toordinal()
            b = a.fromordinal(aord)
            self.assertEqual(a, b)
            self.assertRaises(ValueError, lambda : a.fromordinal(aord + 1))
            b = a - timedelta(days=1)
            self.assertEqual(b.toordinal(), aord - 1)
            self.assertEqual(b, self.theclass.fromordinal(aord - 1))

        def test_bad_constructor_arguments(self):
            self.theclass(MINYEAR, 1, 1)
            self.theclass(MAXYEAR, 1, 1)
            self.assertRaises(ValueError, self.theclass, MINYEAR - 1, 1, 1)
            self.assertRaises(ValueError, self.theclass, MAXYEAR + 1, 1, 1)
            self.theclass(2000, 1, 1)
            self.theclass(2000, 12, 1)
            self.assertRaises(ValueError, self.theclass, 2000, 0, 1)
            self.assertRaises(ValueError, self.theclass, 2000, 13, 1)
            self.theclass(2000, 2, 29)
            self.theclass(2004, 2, 29)
            self.theclass(2400, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2000, 2, 30)
            self.assertRaises(ValueError, self.theclass, 2001, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2100, 2, 29)
            self.assertRaises(ValueError, self.theclass, 1900, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 0)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 32)

        def test_hash_equality(self):
            d = self.theclass(2000, 12, 31)
            e = self.theclass(2000, 12, 31)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)
            d = self.theclass(2001, 1, 1)
            e = self.theclass(2001, 1, 1)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)

        def test_computations(self):
            a = self.theclass(2002, 1, 31)
            b = self.theclass(1956, 1, 31)
            diff = a - b
            self.assertEqual(diff.days, 16790 + len(range(1956, 2002, 4)))
            self.assertEqual(diff.seconds, 0)
            self.assertEqual(diff.microseconds, 0)
            day = timedelta(1)
            week = timedelta(7)
            a = self.theclass(2002, 3, 2)
            self.assertEqual(a + day, self.theclass(2002, 3, 3))
            self.assertEqual(day + a, self.theclass(2002, 3, 3))
            self.assertEqual(a - day, self.theclass(2002, 3, 1))
            self.assertEqual(-day + a, self.theclass(2002, 3, 1))
            self.assertEqual(a + week, self.theclass(2002, 3, 9))
            self.assertEqual(a - week, self.theclass(2002, 2, 23))
            self.assertEqual(a + 52 * week, self.theclass(2003, 3, 1))
            self.assertEqual(a - 52 * week, self.theclass(2001, 3, 3))
            self.assertEqual(a + week - a, week)
            self.assertEqual(a + day - a, day)
            self.assertEqual(a - week - a, -week)
            self.assertEqual(a - day - a, -day)
            self.assertEqual(a - (a + week), -week)
            self.assertEqual(a - (a + day), -day)
            self.assertEqual(a - (a - week), week)
            self.assertEqual(a - (a - day), day)
            for i in (1, 1L, 1.0):
                self.assertRaises(TypeError, lambda : a + i)
                self.assertRaises(TypeError, lambda : a - i)
                self.assertRaises(TypeError, lambda : i + a)
                self.assertRaises(TypeError, lambda : i - a)

            self.assertRaises(TypeError, lambda : day - a)
            self.assertRaises(TypeError, lambda : day * a)
            self.assertRaises(TypeError, lambda : a * day)
            self.assertRaises(TypeError, lambda : day // a)
            self.assertRaises(TypeError, lambda : a // day)
            self.assertRaises(TypeError, lambda : a * a)
            self.assertRaises(TypeError, lambda : a // a)
            self.assertRaises(TypeError, lambda : a + a)

        def test_overflow(self):
            tiny = self.theclass.resolution
            for delta in [tiny, timedelta(1), timedelta(2)]:
                dt = self.theclass.min + delta
                dt -= delta
                self.assertRaises(OverflowError, dt.__sub__, delta)
                self.assertRaises(OverflowError, dt.__add__, -delta)
                dt = self.theclass.max - delta
                dt += delta
                self.assertRaises(OverflowError, dt.__add__, delta)
                self.assertRaises(OverflowError, dt.__sub__, -delta)

        def test_fromtimestamp(self):
            import time
            year, month, day = (1999, 9, 19)
            ts = time.mktime((year,
             month,
             day,
             0,
             0,
             0,
             0,
             0,
             -1))
            d = self.theclass.fromtimestamp(ts)
            self.assertEqual(d.year, year)
            self.assertEqual(d.month, month)
            self.assertEqual(d.day, day)

        def test_insane_fromtimestamp(self):
            for insane in (-1e+200, 1e+200):
                self.assertRaises(ValueError, self.theclass.fromtimestamp, insane)

        def test_today(self):
            import time
            for dummy in range(3):
                today = self.theclass.today()
                ts = time.time()
                todayagain = self.theclass.fromtimestamp(ts)
                if today == todayagain:
                    break
                time.sleep(0.1)

            self.assertTrue(today == todayagain or abs(todayagain - today) < timedelta(seconds=0.5))

        def test_weekday(self):
            for i in range(7):
                self.assertEqual(self.theclass(2002, 3, 4 + i).weekday(), i)
                self.assertEqual(self.theclass(2002, 3, 4 + i).isoweekday(), i + 1)
                self.assertEqual(self.theclass(1956, 1, 2 + i).weekday(), i)
                self.assertEqual(self.theclass(1956, 1, 2 + i).isoweekday(), i + 1)

        def test_isocalendar(self):
            for i in range(7):
                d = self.theclass(2003, 12, 22 + i)
                self.assertEqual(d.isocalendar(), (2003, 52, i + 1))
                d = self.theclass(2003, 12, 29) + timedelta(i)
                self.assertEqual(d.isocalendar(), (2004, 1, i + 1))
                d = self.theclass(2004, 1, 5 + i)
                self.assertEqual(d.isocalendar(), (2004, 2, i + 1))
                d = self.theclass(2009, 12, 21 + i)
                self.assertEqual(d.isocalendar(), (2009, 52, i + 1))
                d = self.theclass(2009, 12, 28) + timedelta(i)
                self.assertEqual(d.isocalendar(), (2009, 53, i + 1))
                d = self.theclass(2010, 1, 4 + i)
                self.assertEqual(d.isocalendar(), (2010, 1, i + 1))

        def test_iso_long_years(self):
            ISO_LONG_YEARS_TABLE = '\n              4   32   60   88\n              9   37   65   93\n             15   43   71   99\n             20   48   76\n             26   54   82\n\n            105  133  161  189\n            111  139  167  195\n            116  144  172\n            122  150  178\n            128  156  184\n\n            201  229  257  285\n            207  235  263  291\n            212  240  268  296\n            218  246  274\n            224  252  280\n\n            303  331  359  387\n            308  336  364  392\n            314  342  370  398\n            320  348  376\n            325  353  381\n        '
            iso_long_years = map(int, ISO_LONG_YEARS_TABLE.split())
            iso_long_years.sort()
            L = []
            for i in range(400):
                d = self.theclass(2000 + i, 12, 31)
                d1 = self.theclass(1600 + i, 12, 31)
                self.assertEqual(d.isocalendar()[1:], d1.isocalendar()[1:])
                if d.isocalendar()[1] == 53:
                    L.append(i)

            self.assertEqual(L, iso_long_years)

        def test_isoformat(self):
            t = self.theclass(2, 3, 2)
            self.assertEqual(t.isoformat(), '0002-03-02')

        def test_ctime(self):
            t = self.theclass(2002, 3, 2)
            self.assertEqual(t.ctime(), 'Sat Mar  2 00:00:00 2002')

        def test_strftime(self):
            t = self.theclass(2005, 3, 2)
            self.assertEqual(t.strftime('m:%m d:%d y:%y'), 'm:03 d:02 y:05')
            self.assertEqual(t.strftime(''), '')
            self.assertEqual(t.strftime('x' * 1000), 'x' * 1000)
            self.assertRaises(TypeError, t.strftime)
            self.assertRaises(TypeError, t.strftime, 'one', 'two')
            self.assertRaises(TypeError, t.strftime, 42)
            self.assertEqual(t.strftime(u'%m'), '03')
            self.assertEqual(t.strftime("'%z' '%Z'"), "'' ''")
            for f in ['%e', '%', '%#']:
                try:
                    t.strftime(f)
                except ValueError:
                    pass

            t.strftime('%f')

        def test_format(self):
            dt = self.theclass(2007, 9, 10)
            self.assertEqual(dt.__format__(''), str(dt))

            class A(self.theclass):

                def __str__(self):
                    return 'A'

            a = A(2007, 9, 10)
            self.assertEqual(a.__format__(''), 'A')

            class B(self.theclass):

                def strftime(self, format_spec):
                    return 'B'

            b = B(2007, 9, 10)
            self.assertEqual(b.__format__(''), str(dt))
            for fmt in ['m:%m d:%d y:%y', 'm:%m d:%d y:%y H:%H M:%M S:%S', '%z %Z']:
                self.assertEqual(dt.__format__(fmt), dt.strftime(fmt))
                self.assertEqual(a.__format__(fmt), dt.strftime(fmt))
                self.assertEqual(b.__format__(fmt), 'B')

        def test_resolution_info(self):
            self.assertIsInstance(self.theclass.min, self.theclass)
            self.assertIsInstance(self.theclass.max, self.theclass)
            self.assertIsInstance(self.theclass.resolution, timedelta)
            self.assertTrue(self.theclass.max > self.theclass.min)

        def test_extreme_timedelta(self):
            big = self.theclass.max - self.theclass.min
            n = (big.days * 24 * 3600 + big.seconds) * 1000000 + big.microseconds
            justasbig = timedelta(0, 0, n)
            self.assertEqual(big, justasbig)
            self.assertEqual(self.theclass.min + big, self.theclass.max)
            self.assertEqual(self.theclass.max - big, self.theclass.min)

        def test_timetuple(self):
            for i in range(7):
                d = self.theclass(1956, 1, 2 + i)
                t = d.timetuple()
                self.assertEqual(t, (1956,
                 1,
                 2 + i,
                 0,
                 0,
                 0,
                 i,
                 2 + i,
                 -1))
                d = self.theclass(1956, 2, 1 + i)
                t = d.timetuple()
                self.assertEqual(t, (1956,
                 2,
                 1 + i,
                 0,
                 0,
                 0,
                 (2 + i) % 7,
                 32 + i,
                 -1))
                d = self.theclass(1956, 3, 1 + i)
                t = d.timetuple()
                self.assertEqual(t, (1956,
                 3,
                 1 + i,
                 0,
                 0,
                 0,
                 (3 + i) % 7,
                 61 + i,
                 -1))
                self.assertEqual(t.tm_year, 1956)
                self.assertEqual(t.tm_mon, 3)
                self.assertEqual(t.tm_mday, 1 + i)
                self.assertEqual(t.tm_hour, 0)
                self.assertEqual(t.tm_min, 0)
                self.assertEqual(t.tm_sec, 0)
                self.assertEqual(t.tm_wday, (3 + i) % 7)
                self.assertEqual(t.tm_yday, 61 + i)
                self.assertEqual(t.tm_isdst, -1)

        def test_pickling(self):
            args = (6, 7, 23)
            orig = self.theclass(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_compare(self):
            t1 = self.theclass(2, 3, 4)
            t2 = self.theclass(2, 3, 4)
            self.assertTrue(t1 == t2)
            self.assertTrue(t1 <= t2)
            self.assertTrue(t1 >= t2)
            self.assertTrue(not t1 != t2)
            self.assertTrue(not t1 < t2)
            self.assertTrue(not t1 > t2)
            self.assertEqual(cmp(t1, t2), 0)
            self.assertEqual(cmp(t2, t1), 0)
            for args in ((3, 3, 3), (2, 4, 4), (2, 3, 5)):
                t2 = self.theclass(*args)
                self.assertTrue(t1 < t2)
                self.assertTrue(t2 > t1)
                self.assertTrue(t1 <= t2)
                self.assertTrue(t2 >= t1)
                self.assertTrue(t1 != t2)
                self.assertTrue(t2 != t1)
                self.assertTrue(not t1 == t2)
                self.assertTrue(not t2 == t1)
                self.assertTrue(not t1 > t2)
                self.assertTrue(not t2 < t1)
                self.assertTrue(not t1 >= t2)
                self.assertTrue(not t2 <= t1)
                self.assertEqual(cmp(t1, t2), -1)
                self.assertEqual(cmp(t2, t1), 1)

            for badarg in OTHERSTUFF:
                self.assertEqual(t1 == badarg, False)
                self.assertEqual(t1 != badarg, True)
                self.assertEqual(badarg == t1, False)
                self.assertEqual(badarg != t1, True)
                self.assertRaises(TypeError, lambda : t1 < badarg)
                self.assertRaises(TypeError, lambda : t1 > badarg)
                self.assertRaises(TypeError, lambda : t1 >= badarg)
                self.assertRaises(TypeError, lambda : badarg <= t1)
                self.assertRaises(TypeError, lambda : badarg < t1)
                self.assertRaises(TypeError, lambda : badarg > t1)
                self.assertRaises(TypeError, lambda : badarg >= t1)

        def test_mixed_compare(self):
            our = self.theclass(2000, 4, 5)
            self.assertRaises(TypeError, cmp, our, 1)
            self.assertRaises(TypeError, cmp, 1, our)

            class AnotherDateTimeClass(object):

                def __cmp__(self, other):
                    return 0

                __hash__ = None

            their = AnotherDateTimeClass()
            self.assertRaises(TypeError, cmp, our, their)

            class Comparable(AnotherDateTimeClass):

                def timetuple(self):
                    return ()

            their = Comparable()
            self.assertEqual(cmp(our, their), 0)
            self.assertEqual(cmp(their, our), 0)
            self.assertTrue(our == their)
            self.assertTrue(their == our)

        def test_bool(self):
            self.assertTrue(self.theclass.min)
            self.assertTrue(self.theclass.max)

        def test_strftime_out_of_range(self):
            cls = self.theclass
            self.assertEqual(cls(1900, 1, 1).strftime('%Y'), '1900')
            for y in (1, 49, 51, 99, 100, 1000, 1899):
                self.assertRaises(ValueError, cls(y, 1, 1).strftime, '%Y')

        def test_replace(self):
            cls = self.theclass
            args = [1, 2, 3]
            base = cls(*args)
            self.assertEqual(base, base.replace())
            i = 0
            for name, newval in (('year', 2), ('month', 3), ('day', 4)):
                newargs = args[:]
                newargs[i] = newval
                expected = cls(*newargs)
                got = base.replace(**{name: newval})
                self.assertEqual(expected, got)
                i += 1

            base = cls(2000, 2, 29)
            self.assertRaises(ValueError, base.replace, year=2001)

        def test_subclass_date(self):

            class C(self.theclass):
                theAnswer = 42

                def __new__(cls, *args, **kws):
                    temp = kws.copy()
                    extra = temp.pop('extra')
                    result = self.theclass.__new__(cls, *args, **temp)
                    result.extra = extra
                    return result

                def newmeth(self, start):
                    return start + self.year + self.month

            args = (2003, 4, 14)
            dt1 = self.theclass(*args)
            dt2 = C(*args, **{'extra': 7})
            self.assertEqual(dt2.__class__, C)
            self.assertEqual(dt2.theAnswer, 42)
            self.assertEqual(dt2.extra, 7)
            self.assertEqual(dt1.toordinal(), dt2.toordinal())
            self.assertEqual(dt2.newmeth(-7), dt1.year + dt1.month - 7)

        def test_pickling_subclass_date(self):
            args = (6, 7, 23)
            orig = SubclassDate(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_backdoor_resistance(self):
            base = '1995-03-25'
            if not issubclass(self.theclass, datetime):
                base = base[:4]
            for month_byte in ('9',
             chr(0),
             chr(13),
             '\xff'):
                self.assertRaises(TypeError, self.theclass, base[:2] + month_byte + base[3:])

            for ord_byte in range(1, 13):
                self.theclass(base[:2] + chr(ord_byte) + base[3:])


    class SubclassDatetime(datetime):
        sub_var = 1


    class TestDateTime(TestDate):
        theclass = datetime

        def test_basic_attributes(self):
            dt = self.theclass(2002, 3, 1, 12, 0)
            self.assertEqual(dt.year, 2002)
            self.assertEqual(dt.month, 3)
            self.assertEqual(dt.day, 1)
            self.assertEqual(dt.hour, 12)
            self.assertEqual(dt.minute, 0)
            self.assertEqual(dt.second, 0)
            self.assertEqual(dt.microsecond, 0)

        def test_basic_attributes_nonzero(self):
            dt = self.theclass(2002, 3, 1, 12, 59, 59, 8000)
            self.assertEqual(dt.year, 2002)
            self.assertEqual(dt.month, 3)
            self.assertEqual(dt.day, 1)
            self.assertEqual(dt.hour, 12)
            self.assertEqual(dt.minute, 59)
            self.assertEqual(dt.second, 59)
            self.assertEqual(dt.microsecond, 8000)

        def test_roundtrip(self):
            for dt in (self.theclass(1, 2, 3, 4, 5, 6, 7), self.theclass.now()):
                s = repr(dt)
                self.assertTrue(s.startswith('datetime.'))
                s = s[9:]
                dt2 = eval(s)
                self.assertEqual(dt, dt2)
                dt2 = self.theclass(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
                self.assertEqual(dt, dt2)

        def test_isoformat(self):
            t = self.theclass(2, 3, 2, 4, 5, 1, 123)
            self.assertEqual(t.isoformat(), '0002-03-02T04:05:01.000123')
            self.assertEqual(t.isoformat('T'), '0002-03-02T04:05:01.000123')
            self.assertEqual(t.isoformat(' '), '0002-03-02 04:05:01.000123')
            self.assertEqual(t.isoformat('\x00'), '0002-03-02\x0004:05:01.000123')
            self.assertEqual(str(t), '0002-03-02 04:05:01.000123')
            t = self.theclass(2, 3, 2)
            self.assertEqual(t.isoformat(), '0002-03-02T00:00:00')
            self.assertEqual(t.isoformat('T'), '0002-03-02T00:00:00')
            self.assertEqual(t.isoformat(' '), '0002-03-02 00:00:00')
            self.assertEqual(str(t), '0002-03-02 00:00:00')

        def test_format(self):
            dt = self.theclass(2007, 9, 10, 4, 5, 1, 123)
            self.assertEqual(dt.__format__(''), str(dt))

            class A(self.theclass):

                def __str__(self):
                    return 'A'

            a = A(2007, 9, 10, 4, 5, 1, 123)
            self.assertEqual(a.__format__(''), 'A')

            class B(self.theclass):

                def strftime(self, format_spec):
                    return 'B'

            b = B(2007, 9, 10, 4, 5, 1, 123)
            self.assertEqual(b.__format__(''), str(dt))
            for fmt in ['m:%m d:%d y:%y', 'm:%m d:%d y:%y H:%H M:%M S:%S', '%z %Z']:
                self.assertEqual(dt.__format__(fmt), dt.strftime(fmt))
                self.assertEqual(a.__format__(fmt), dt.strftime(fmt))
                self.assertEqual(b.__format__(fmt), 'B')

        def test_more_ctime(self):
            import time
            t = self.theclass(2002, 3, 2, 18, 3, 5, 123)
            self.assertEqual(t.ctime(), 'Sat Mar  2 18:03:05 2002')
            t = self.theclass(2002, 3, 22, 18, 3, 5, 123)
            self.assertEqual(t.ctime(), time.ctime(time.mktime(t.timetuple())))

        def test_tz_independent_comparing(self):
            dt1 = self.theclass(2002, 3, 1, 9, 0, 0)
            dt2 = self.theclass(2002, 3, 1, 10, 0, 0)
            dt3 = self.theclass(2002, 3, 1, 9, 0, 0)
            self.assertEqual(dt1, dt3)
            self.assertTrue(dt2 > dt3)
            dt1 = self.theclass(MAXYEAR, 12, 31, 23, 59, 59, 999998)
            us = timedelta(microseconds=1)
            dt2 = dt1 + us
            self.assertEqual(dt2 - dt1, us)
            self.assertTrue(dt1 < dt2)

        def test_strftime_with_bad_tzname_replace(self):

            class MyTzInfo(FixedOffset):

                def tzname(self, dt):

                    class MyStr(str):

                        def replace(self, *args):
                            return None

                    return MyStr('name')

            t = self.theclass(2005, 3, 2, 0, 0, 0, 0, MyTzInfo(3, 'name'))
            self.assertRaises(TypeError, t.strftime, '%Z')

        def test_bad_constructor_arguments(self):
            self.theclass(MINYEAR, 1, 1)
            self.theclass(MAXYEAR, 1, 1)
            self.assertRaises(ValueError, self.theclass, MINYEAR - 1, 1, 1)
            self.assertRaises(ValueError, self.theclass, MAXYEAR + 1, 1, 1)
            self.theclass(2000, 1, 1)
            self.theclass(2000, 12, 1)
            self.assertRaises(ValueError, self.theclass, 2000, 0, 1)
            self.assertRaises(ValueError, self.theclass, 2000, 13, 1)
            self.theclass(2000, 2, 29)
            self.theclass(2004, 2, 29)
            self.theclass(2400, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2000, 2, 30)
            self.assertRaises(ValueError, self.theclass, 2001, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2100, 2, 29)
            self.assertRaises(ValueError, self.theclass, 1900, 2, 29)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 0)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 32)
            self.theclass(2000, 1, 31, 0)
            self.theclass(2000, 1, 31, 23)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, -1)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 24)
            self.theclass(2000, 1, 31, 23, 0)
            self.theclass(2000, 1, 31, 23, 59)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, -1)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, 60)
            self.theclass(2000, 1, 31, 23, 59, 0)
            self.theclass(2000, 1, 31, 23, 59, 59)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, 59, -1)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, 59, 60)
            self.theclass(2000, 1, 31, 23, 59, 59, 0)
            self.theclass(2000, 1, 31, 23, 59, 59, 999999)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, 59, 59, -1)
            self.assertRaises(ValueError, self.theclass, 2000, 1, 31, 23, 59, 59, 1000000)

        def test_hash_equality(self):
            d = self.theclass(2000, 12, 31, 23, 30, 17)
            e = self.theclass(2000, 12, 31, 23, 30, 17)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)
            d = self.theclass(2001, 1, 1, 0, 5, 17)
            e = self.theclass(2001, 1, 1, 0, 5, 17)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)

        def test_computations(self):
            a = self.theclass(2002, 1, 31)
            b = self.theclass(1956, 1, 31)
            diff = a - b
            self.assertEqual(diff.days, 16790 + len(range(1956, 2002, 4)))
            self.assertEqual(diff.seconds, 0)
            self.assertEqual(diff.microseconds, 0)
            a = self.theclass(2002, 3, 2, 17, 6)
            millisec = timedelta(0, 0, 1000)
            hour = timedelta(0, 3600)
            day = timedelta(1)
            week = timedelta(7)
            self.assertEqual(a + hour, self.theclass(2002, 3, 2, 18, 6))
            self.assertEqual(hour + a, self.theclass(2002, 3, 2, 18, 6))
            self.assertEqual(a + 10 * hour, self.theclass(2002, 3, 3, 3, 6))
            self.assertEqual(a - hour, self.theclass(2002, 3, 2, 16, 6))
            self.assertEqual(-hour + a, self.theclass(2002, 3, 2, 16, 6))
            self.assertEqual(a - hour, a + -hour)
            self.assertEqual(a - 20 * hour, self.theclass(2002, 3, 1, 21, 6))
            self.assertEqual(a + day, self.theclass(2002, 3, 3, 17, 6))
            self.assertEqual(a - day, self.theclass(2002, 3, 1, 17, 6))
            self.assertEqual(a + week, self.theclass(2002, 3, 9, 17, 6))
            self.assertEqual(a - week, self.theclass(2002, 2, 23, 17, 6))
            self.assertEqual(a + 52 * week, self.theclass(2003, 3, 1, 17, 6))
            self.assertEqual(a - 52 * week, self.theclass(2001, 3, 3, 17, 6))
            self.assertEqual(a + week - a, week)
            self.assertEqual(a + day - a, day)
            self.assertEqual(a + hour - a, hour)
            self.assertEqual(a + millisec - a, millisec)
            self.assertEqual(a - week - a, -week)
            self.assertEqual(a - day - a, -day)
            self.assertEqual(a - hour - a, -hour)
            self.assertEqual(a - millisec - a, -millisec)
            self.assertEqual(a - (a + week), -week)
            self.assertEqual(a - (a + day), -day)
            self.assertEqual(a - (a + hour), -hour)
            self.assertEqual(a - (a + millisec), -millisec)
            self.assertEqual(a - (a - week), week)
            self.assertEqual(a - (a - day), day)
            self.assertEqual(a - (a - hour), hour)
            self.assertEqual(a - (a - millisec), millisec)
            self.assertEqual(a + (week + day + hour + millisec), self.theclass(2002, 3, 10, 18, 6, 0, 1000))
            self.assertEqual(a + (week + day + hour + millisec), a + week + day + hour + millisec)
            self.assertEqual(a - (week + day + hour + millisec), self.theclass(2002, 2, 22, 16, 5, 59, 999000))
            self.assertEqual(a - (week + day + hour + millisec), a - week - day - hour - millisec)
            for i in (1, 1L, 1.0):
                self.assertRaises(TypeError, lambda : a + i)
                self.assertRaises(TypeError, lambda : a - i)
                self.assertRaises(TypeError, lambda : i + a)
                self.assertRaises(TypeError, lambda : i - a)

            self.assertRaises(TypeError, lambda : day - a)
            self.assertRaises(TypeError, lambda : day * a)
            self.assertRaises(TypeError, lambda : a * day)
            self.assertRaises(TypeError, lambda : day // a)
            self.assertRaises(TypeError, lambda : a // day)
            self.assertRaises(TypeError, lambda : a * a)
            self.assertRaises(TypeError, lambda : a // a)
            self.assertRaises(TypeError, lambda : a + a)

        def test_pickling(self):
            args = (6,
             7,
             23,
             20,
             59,
             1,
             4096)
            orig = self.theclass(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_more_pickling(self):
            a = self.theclass(2003, 2, 7, 16, 48, 37, 444116)
            s = pickle.dumps(a)
            b = pickle.loads(s)
            self.assertEqual(b.year, 2003)
            self.assertEqual(b.month, 2)
            self.assertEqual(b.day, 7)

        def test_pickling_subclass_datetime(self):
            args = (6,
             7,
             23,
             20,
             59,
             1,
             4096)
            orig = SubclassDatetime(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_more_compare(self):
            args = [2000,
             11,
             29,
             20,
             58,
             16,
             999998]
            t1 = self.theclass(*args)
            t2 = self.theclass(*args)
            self.assertTrue(t1 == t2)
            self.assertTrue(t1 <= t2)
            self.assertTrue(t1 >= t2)
            self.assertTrue(not t1 != t2)
            self.assertTrue(not t1 < t2)
            self.assertTrue(not t1 > t2)
            self.assertEqual(cmp(t1, t2), 0)
            self.assertEqual(cmp(t2, t1), 0)
            for i in range(len(args)):
                newargs = args[:]
                newargs[i] = args[i] + 1
                t2 = self.theclass(*newargs)
                self.assertTrue(t1 < t2)
                self.assertTrue(t2 > t1)
                self.assertTrue(t1 <= t2)
                self.assertTrue(t2 >= t1)
                self.assertTrue(t1 != t2)
                self.assertTrue(t2 != t1)
                self.assertTrue(not t1 == t2)
                self.assertTrue(not t2 == t1)
                self.assertTrue(not t1 > t2)
                self.assertTrue(not t2 < t1)
                self.assertTrue(not t1 >= t2)
                self.assertTrue(not t2 <= t1)
                self.assertEqual(cmp(t1, t2), -1)
                self.assertEqual(cmp(t2, t1), 1)

        def verify_field_equality(self, expected, got):
            self.assertEqual(expected.tm_year, got.year)
            self.assertEqual(expected.tm_mon, got.month)
            self.assertEqual(expected.tm_mday, got.day)
            self.assertEqual(expected.tm_hour, got.hour)
            self.assertEqual(expected.tm_min, got.minute)
            self.assertEqual(expected.tm_sec, got.second)

        def test_fromtimestamp(self):
            import time
            ts = time.time()
            expected = time.localtime(ts)
            got = self.theclass.fromtimestamp(ts)
            self.verify_field_equality(expected, got)

        def test_utcfromtimestamp(self):
            import time
            ts = time.time()
            expected = time.gmtime(ts)
            got = self.theclass.utcfromtimestamp(ts)
            self.verify_field_equality(expected, got)

        def test_microsecond_rounding(self):
            self.assertEqual(self.theclass.fromtimestamp(0.9999999), self.theclass.fromtimestamp(1))

        def test_insane_fromtimestamp(self):
            for insane in (-1e+200, 1e+200):
                self.assertRaises(ValueError, self.theclass.fromtimestamp, insane)

        def test_insane_utcfromtimestamp(self):
            for insane in (-1e+200, 1e+200):
                self.assertRaises(ValueError, self.theclass.utcfromtimestamp, insane)

        @unittest.skipIf(sys.platform == 'win32', "Windows doesn't accept negative timestamps")
        def test_negative_float_fromtimestamp(self):
            self.theclass.fromtimestamp(-1.05)

        @unittest.skipIf(sys.platform == 'win32', "Windows doesn't accept negative timestamps")
        def test_negative_float_utcfromtimestamp(self):
            d = self.theclass.utcfromtimestamp(-1.05)
            self.assertEqual(d, self.theclass(1969, 12, 31, 23, 59, 58, 950000))

        def test_utcnow(self):
            import time
            tolerance = timedelta(seconds=1)
            for dummy in range(3):
                from_now = self.theclass.utcnow()
                from_timestamp = self.theclass.utcfromtimestamp(time.time())
                if abs(from_timestamp - from_now) <= tolerance:
                    break

            self.assertTrue(abs(from_timestamp - from_now) <= tolerance)

        def test_strptime(self):
            import _strptime
            string = '2004-12-01 13:02:47.197'
            format = '%Y-%m-%d %H:%M:%S.%f'
            result, frac = _strptime._strptime(string, format)
            expected = self.theclass(*(result[0:6] + (frac,)))
            got = self.theclass.strptime(string, format)
            self.assertEqual(expected, got)

        def test_more_timetuple(self):
            t = self.theclass(2004, 12, 31, 6, 22, 33)
            self.assertEqual(t.timetuple(), (2004, 12, 31, 6, 22, 33, 4, 366, -1))
            self.assertEqual(t.timetuple(), (t.year,
             t.month,
             t.day,
             t.hour,
             t.minute,
             t.second,
             t.weekday(),
             t.toordinal() - date(t.year, 1, 1).toordinal() + 1,
             -1))
            tt = t.timetuple()
            self.assertEqual(tt.tm_year, t.year)
            self.assertEqual(tt.tm_mon, t.month)
            self.assertEqual(tt.tm_mday, t.day)
            self.assertEqual(tt.tm_hour, t.hour)
            self.assertEqual(tt.tm_min, t.minute)
            self.assertEqual(tt.tm_sec, t.second)
            self.assertEqual(tt.tm_wday, t.weekday())
            self.assertEqual(tt.tm_yday, t.toordinal() - date(t.year, 1, 1).toordinal() + 1)
            self.assertEqual(tt.tm_isdst, -1)

        def test_more_strftime(self):
            t = self.theclass(2004, 12, 31, 6, 22, 33, 47)
            self.assertEqual(t.strftime('%m %d %y %f %S %M %H %j'), '12 31 04 000047 33 22 06 366')

        def test_extract(self):
            dt = self.theclass(2002, 3, 4, 18, 45, 3, 1234)
            self.assertEqual(dt.date(), date(2002, 3, 4))
            self.assertEqual(dt.time(), time(18, 45, 3, 1234))

        def test_combine(self):
            d = date(2002, 3, 4)
            t = time(18, 45, 3, 1234)
            expected = self.theclass(2002, 3, 4, 18, 45, 3, 1234)
            combine = self.theclass.combine
            dt = combine(d, t)
            self.assertEqual(dt, expected)
            dt = combine(time=t, date=d)
            self.assertEqual(dt, expected)
            self.assertEqual(d, dt.date())
            self.assertEqual(t, dt.time())
            self.assertEqual(dt, combine(dt.date(), dt.time()))
            self.assertRaises(TypeError, combine)
            self.assertRaises(TypeError, combine, d)
            self.assertRaises(TypeError, combine, t, d)
            self.assertRaises(TypeError, combine, d, t, 1)
            self.assertRaises(TypeError, combine, 'date', 'time')

        def test_replace(self):
            cls = self.theclass
            args = [1,
             2,
             3,
             4,
             5,
             6,
             7]
            base = cls(*args)
            self.assertEqual(base, base.replace())
            i = 0
            for name, newval in (('year', 2),
             ('month', 3),
             ('day', 4),
             ('hour', 5),
             ('minute', 6),
             ('second', 7),
             ('microsecond', 8)):
                newargs = args[:]
                newargs[i] = newval
                expected = cls(*newargs)
                got = base.replace(**{name: newval})
                self.assertEqual(expected, got)
                i += 1

            base = cls(2000, 2, 29)
            self.assertRaises(ValueError, base.replace, year=2001)

        def test_astimezone(self):
            dt = self.theclass.now()
            f = FixedOffset(44, '')
            self.assertRaises(TypeError, dt.astimezone)
            self.assertRaises(TypeError, dt.astimezone, f, f)
            self.assertRaises(TypeError, dt.astimezone, dt)
            self.assertRaises(ValueError, dt.astimezone, f)
            self.assertRaises(ValueError, dt.astimezone, tz=f)

            class Bogus(tzinfo):

                def utcoffset(self, dt):
                    return None

                def dst(self, dt):
                    return timedelta(0)

            bog = Bogus()
            self.assertRaises(ValueError, dt.astimezone, bog)

            class AlsoBogus(tzinfo):

                def utcoffset(self, dt):
                    return timedelta(0)

                def dst(self, dt):
                    return None

            alsobog = AlsoBogus()
            self.assertRaises(ValueError, dt.astimezone, alsobog)

        def test_subclass_datetime(self):

            class C(self.theclass):
                theAnswer = 42

                def __new__(cls, *args, **kws):
                    temp = kws.copy()
                    extra = temp.pop('extra')
                    result = self.theclass.__new__(cls, *args, **temp)
                    result.extra = extra
                    return result

                def newmeth(self, start):
                    return start + self.year + self.month + self.second

            args = (2003, 4, 14, 12, 13, 41)
            dt1 = self.theclass(*args)
            dt2 = C(*args, **{'extra': 7})
            self.assertEqual(dt2.__class__, C)
            self.assertEqual(dt2.theAnswer, 42)
            self.assertEqual(dt2.extra, 7)
            self.assertEqual(dt1.toordinal(), dt2.toordinal())
            self.assertEqual(dt2.newmeth(-7), dt1.year + dt1.month + dt1.second - 7)


    class SubclassTime(time):
        sub_var = 1


    class TestTime(HarmlessMixedComparison, unittest.TestCase):
        theclass = time

        def test_basic_attributes(self):
            t = self.theclass(12, 0)
            self.assertEqual(t.hour, 12)
            self.assertEqual(t.minute, 0)
            self.assertEqual(t.second, 0)
            self.assertEqual(t.microsecond, 0)

        def test_basic_attributes_nonzero(self):
            t = self.theclass(12, 59, 59, 8000)
            self.assertEqual(t.hour, 12)
            self.assertEqual(t.minute, 59)
            self.assertEqual(t.second, 59)
            self.assertEqual(t.microsecond, 8000)

        def test_roundtrip(self):
            t = self.theclass(1, 2, 3, 4)
            s = repr(t)
            self.assertTrue(s.startswith('datetime.'))
            s = s[9:]
            t2 = eval(s)
            self.assertEqual(t, t2)
            t2 = self.theclass(t.hour, t.minute, t.second, t.microsecond)
            self.assertEqual(t, t2)

        def test_comparing(self):
            args = [1,
             2,
             3,
             4]
            t1 = self.theclass(*args)
            t2 = self.theclass(*args)
            self.assertTrue(t1 == t2)
            self.assertTrue(t1 <= t2)
            self.assertTrue(t1 >= t2)
            self.assertTrue(not t1 != t2)
            self.assertTrue(not t1 < t2)
            self.assertTrue(not t1 > t2)
            self.assertEqual(cmp(t1, t2), 0)
            self.assertEqual(cmp(t2, t1), 0)
            for i in range(len(args)):
                newargs = args[:]
                newargs[i] = args[i] + 1
                t2 = self.theclass(*newargs)
                self.assertTrue(t1 < t2)
                self.assertTrue(t2 > t1)
                self.assertTrue(t1 <= t2)
                self.assertTrue(t2 >= t1)
                self.assertTrue(t1 != t2)
                self.assertTrue(t2 != t1)
                self.assertTrue(not t1 == t2)
                self.assertTrue(not t2 == t1)
                self.assertTrue(not t1 > t2)
                self.assertTrue(not t2 < t1)
                self.assertTrue(not t1 >= t2)
                self.assertTrue(not t2 <= t1)
                self.assertEqual(cmp(t1, t2), -1)
                self.assertEqual(cmp(t2, t1), 1)

            for badarg in OTHERSTUFF:
                self.assertEqual(t1 == badarg, False)
                self.assertEqual(t1 != badarg, True)
                self.assertEqual(badarg == t1, False)
                self.assertEqual(badarg != t1, True)
                self.assertRaises(TypeError, lambda : t1 <= badarg)
                self.assertRaises(TypeError, lambda : t1 < badarg)
                self.assertRaises(TypeError, lambda : t1 > badarg)
                self.assertRaises(TypeError, lambda : t1 >= badarg)
                self.assertRaises(TypeError, lambda : badarg <= t1)
                self.assertRaises(TypeError, lambda : badarg < t1)
                self.assertRaises(TypeError, lambda : badarg > t1)
                self.assertRaises(TypeError, lambda : badarg >= t1)

        def test_bad_constructor_arguments(self):
            self.theclass(0, 0)
            self.theclass(23, 0)
            self.assertRaises(ValueError, self.theclass, -1, 0)
            self.assertRaises(ValueError, self.theclass, 24, 0)
            self.theclass(23, 0)
            self.theclass(23, 59)
            self.assertRaises(ValueError, self.theclass, 23, -1)
            self.assertRaises(ValueError, self.theclass, 23, 60)
            self.theclass(23, 59, 0)
            self.theclass(23, 59, 59)
            self.assertRaises(ValueError, self.theclass, 23, 59, -1)
            self.assertRaises(ValueError, self.theclass, 23, 59, 60)
            self.theclass(23, 59, 59, 0)
            self.theclass(23, 59, 59, 999999)
            self.assertRaises(ValueError, self.theclass, 23, 59, 59, -1)
            self.assertRaises(ValueError, self.theclass, 23, 59, 59, 1000000)

        def test_hash_equality(self):
            d = self.theclass(23, 30, 17)
            e = self.theclass(23, 30, 17)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)
            d = self.theclass(0, 5, 17)
            e = self.theclass(0, 5, 17)
            self.assertEqual(d, e)
            self.assertEqual(hash(d), hash(e))
            dic = {d: 1}
            dic[e] = 2
            self.assertEqual(len(dic), 1)
            self.assertEqual(dic[d], 2)
            self.assertEqual(dic[e], 2)

        def test_isoformat(self):
            t = self.theclass(4, 5, 1, 123)
            self.assertEqual(t.isoformat(), '04:05:01.000123')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass()
            self.assertEqual(t.isoformat(), '00:00:00')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=1)
            self.assertEqual(t.isoformat(), '00:00:00.000001')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=10)
            self.assertEqual(t.isoformat(), '00:00:00.000010')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=100)
            self.assertEqual(t.isoformat(), '00:00:00.000100')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=1000)
            self.assertEqual(t.isoformat(), '00:00:00.001000')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=10000)
            self.assertEqual(t.isoformat(), '00:00:00.010000')
            self.assertEqual(t.isoformat(), str(t))
            t = self.theclass(microsecond=100000)
            self.assertEqual(t.isoformat(), '00:00:00.100000')
            self.assertEqual(t.isoformat(), str(t))

        def test_1653736(self):
            t = self.theclass(second=1)
            self.assertRaises(TypeError, t.isoformat, foo=3)

        def test_strftime(self):
            t = self.theclass(1, 2, 3, 4)
            self.assertEqual(t.strftime('%H %M %S %f'), '01 02 03 000004')
            self.assertEqual(t.strftime("'%z' '%Z'"), "'' ''")

        def test_format(self):
            t = self.theclass(1, 2, 3, 4)
            self.assertEqual(t.__format__(''), str(t))

            class A(self.theclass):

                def __str__(self):
                    return 'A'

            a = A(1, 2, 3, 4)
            self.assertEqual(a.__format__(''), 'A')

            class B(self.theclass):

                def strftime(self, format_spec):
                    return 'B'

            b = B(1, 2, 3, 4)
            self.assertEqual(b.__format__(''), str(t))
            for fmt in ['%H %M %S']:
                self.assertEqual(t.__format__(fmt), t.strftime(fmt))
                self.assertEqual(a.__format__(fmt), t.strftime(fmt))
                self.assertEqual(b.__format__(fmt), 'B')

        def test_str(self):
            self.assertEqual(str(self.theclass(1, 2, 3, 4)), '01:02:03.000004')
            self.assertEqual(str(self.theclass(10, 2, 3, 4000)), '10:02:03.004000')
            self.assertEqual(str(self.theclass(0, 2, 3, 400000)), '00:02:03.400000')
            self.assertEqual(str(self.theclass(12, 2, 3, 0)), '12:02:03')
            self.assertEqual(str(self.theclass(23, 15, 0, 0)), '23:15:00')

        def test_repr(self):
            name = 'datetime.' + self.theclass.__name__
            self.assertEqual(repr(self.theclass(1, 2, 3, 4)), '%s(1, 2, 3, 4)' % name)
            self.assertEqual(repr(self.theclass(10, 2, 3, 4000)), '%s(10, 2, 3, 4000)' % name)
            self.assertEqual(repr(self.theclass(0, 2, 3, 400000)), '%s(0, 2, 3, 400000)' % name)
            self.assertEqual(repr(self.theclass(12, 2, 3, 0)), '%s(12, 2, 3)' % name)
            self.assertEqual(repr(self.theclass(23, 15, 0, 0)), '%s(23, 15)' % name)

        def test_resolution_info(self):
            self.assertIsInstance(self.theclass.min, self.theclass)
            self.assertIsInstance(self.theclass.max, self.theclass)
            self.assertIsInstance(self.theclass.resolution, timedelta)
            self.assertTrue(self.theclass.max > self.theclass.min)

        def test_pickling(self):
            args = (20,
             59,
             16,
             4096)
            orig = self.theclass(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_pickling_subclass_time(self):
            args = (20,
             59,
             16,
             4096)
            orig = SubclassTime(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

        def test_bool(self):
            cls = self.theclass
            self.assertTrue(cls(1))
            self.assertTrue(cls(0, 1))
            self.assertTrue(cls(0, 0, 1))
            self.assertTrue(cls(0, 0, 0, 1))
            self.assertTrue(not cls(0))
            self.assertTrue(not cls())

        def test_replace(self):
            cls = self.theclass
            args = [1,
             2,
             3,
             4]
            base = cls(*args)
            self.assertEqual(base, base.replace())
            i = 0
            for name, newval in (('hour', 5),
             ('minute', 6),
             ('second', 7),
             ('microsecond', 8)):
                newargs = args[:]
                newargs[i] = newval
                expected = cls(*newargs)
                got = base.replace(**{name: newval})
                self.assertEqual(expected, got)
                i += 1

            base = cls(1)
            self.assertRaises(ValueError, base.replace, hour=24)
            self.assertRaises(ValueError, base.replace, minute=-1)
            self.assertRaises(ValueError, base.replace, second=100)
            self.assertRaises(ValueError, base.replace, microsecond=1000000)

        def test_subclass_time(self):

            class C(self.theclass):
                theAnswer = 42

                def __new__(cls, *args, **kws):
                    temp = kws.copy()
                    extra = temp.pop('extra')
                    result = self.theclass.__new__(cls, *args, **temp)
                    result.extra = extra
                    return result

                def newmeth(self, start):
                    return start + self.hour + self.second

            args = (4, 5, 6)
            dt1 = self.theclass(*args)
            dt2 = C(*args, **{'extra': 7})
            self.assertEqual(dt2.__class__, C)
            self.assertEqual(dt2.theAnswer, 42)
            self.assertEqual(dt2.extra, 7)
            self.assertEqual(dt1.isoformat(), dt2.isoformat())
            self.assertEqual(dt2.newmeth(-7), dt1.hour + dt1.second - 7)

        def test_backdoor_resistance(self):
            base = '2:59.0'
            for hour_byte in (' ',
             '9',
             chr(24),
             '\xff'):
                self.assertRaises(TypeError, self.theclass, hour_byte + base[1:])


    class TZInfoBase():

        def test_argument_passing(self):
            cls = self.theclass

            class introspective(tzinfo):

                def tzname(self, dt):
                    return dt and 'real' or 'none'

                def utcoffset(self, dt):
                    return timedelta(minutes=dt and 42 or -42)

                dst = utcoffset

            obj = cls(1, 2, 3, tzinfo=introspective())
            expected = cls is time and 'none' or 'real'
            self.assertEqual(obj.tzname(), expected)
            expected = timedelta(minutes=cls is time and -42 or 42)
            self.assertEqual(obj.utcoffset(), expected)
            self.assertEqual(obj.dst(), expected)

        def test_bad_tzinfo_classes(self):
            cls = self.theclass
            self.assertRaises(TypeError, cls, 1, 1, 1, tzinfo=12)

            class NiceTry(object):

                def __init__(self):
                    pass

                def utcoffset(self, dt):
                    pass

            self.assertRaises(TypeError, cls, 1, 1, 1, tzinfo=NiceTry)

            class BetterTry(tzinfo):

                def __init__(self):
                    pass

                def utcoffset(self, dt):
                    pass

            b = BetterTry()
            t = cls(1, 1, 1, tzinfo=b)
            self.assertTrue(t.tzinfo is b)

        def test_utc_offset_out_of_bounds(self):

            class Edgy(tzinfo):

                def __init__(self, offset):
                    self.offset = timedelta(minutes=offset)

                def utcoffset(self, dt):
                    return self.offset

            cls = self.theclass
            for offset, legit in ((-1440, False),
             (-1439, True),
             (1439, True),
             (1440, False)):
                if cls is time:
                    t = cls(1, 2, 3, tzinfo=Edgy(offset))
                elif cls is datetime:
                    t = cls(6, 6, 6, 1, 2, 3, tzinfo=Edgy(offset))
                else:
                    raise 0 or AssertionError('impossible')
                if legit:
                    aofs = abs(offset)
                    h, m = divmod(aofs, 60)
                    tag = '%c%02d:%02d' % (offset < 0 and '-' or '+', h, m)
                    if isinstance(t, datetime):
                        t = t.timetz()
                    self.assertEqual(str(t), '01:02:03' + tag)
                else:
                    self.assertRaises(ValueError, str, t)

        def test_tzinfo_classes(self):
            cls = self.theclass

            class C1(tzinfo):

                def utcoffset(self, dt):
                    return None

                def dst(self, dt):
                    return None

                def tzname(self, dt):
                    return None

            for t in (cls(1, 1, 1), cls(1, 1, 1, tzinfo=None), cls(1, 1, 1, tzinfo=C1())):
                self.assertTrue(t.utcoffset() is None)
                self.assertTrue(t.dst() is None)
                self.assertTrue(t.tzname() is None)

            class C3(tzinfo):

                def utcoffset(self, dt):
                    return timedelta(minutes=-1439)

                def dst(self, dt):
                    return timedelta(minutes=1439)

                def tzname(self, dt):
                    return 'aname'

            t = cls(1, 1, 1, tzinfo=C3())
            self.assertEqual(t.utcoffset(), timedelta(minutes=-1439))
            self.assertEqual(t.dst(), timedelta(minutes=1439))
            self.assertEqual(t.tzname(), 'aname')

            class C4(tzinfo):

                def utcoffset(self, dt):
                    return 'aname'

                def dst(self, dt):
                    return 7

                def tzname(self, dt):
                    return 0

            t = cls(1, 1, 1, tzinfo=C4())
            self.assertRaises(TypeError, t.utcoffset)
            self.assertRaises(TypeError, t.dst)
            self.assertRaises(TypeError, t.tzname)

            class C6(tzinfo):

                def utcoffset(self, dt):
                    return timedelta(hours=-24)

                def dst(self, dt):
                    return timedelta(hours=24)

            t = cls(1, 1, 1, tzinfo=C6())
            self.assertRaises(ValueError, t.utcoffset)
            self.assertRaises(ValueError, t.dst)

            class C7(tzinfo):

                def utcoffset(self, dt):
                    return timedelta(seconds=61)

                def dst(self, dt):
                    return timedelta(microseconds=-81)

            t = cls(1, 1, 1, tzinfo=C7())
            self.assertRaises(ValueError, t.utcoffset)
            self.assertRaises(ValueError, t.dst)
            return

        def test_aware_compare(self):
            cls = self.theclass

            class OperandDependentOffset(tzinfo):

                def utcoffset(self, t):
                    if t.minute < 10:
                        return timedelta(minutes=t.minute)
                    else:
                        return timedelta(minutes=59)

            base = cls(8, 9, 10, tzinfo=OperandDependentOffset())
            d0 = base.replace(minute=3)
            d1 = base.replace(minute=9)
            d2 = base.replace(minute=11)
            for x in (d0, d1, d2):
                for y in (d0, d1, d2):
                    got = cmp(x, y)
                    expected = cmp(x.minute, y.minute)
                    self.assertEqual(got, expected)

            if cls is not time:
                d0 = base.replace(minute=3, tzinfo=OperandDependentOffset())
                d1 = base.replace(minute=9, tzinfo=OperandDependentOffset())
                d2 = base.replace(minute=11, tzinfo=OperandDependentOffset())
                for x in (d0, d1, d2):
                    for y in (d0, d1, d2):
                        got = cmp(x, y)
                        if (x is d0 or x is d1) and (y is d0 or y is d1):
                            expected = 0
                        elif x is y is d2:
                            expected = 0
                        elif x is d2:
                            expected = -1
                        else:
                            raise y is d2 or AssertionError
                            expected = 1
                        self.assertEqual(got, expected)


    class TestTimeTZ(TestTime, TZInfoBase, unittest.TestCase):
        theclass = time

        def test_empty(self):
            t = self.theclass()
            self.assertEqual(t.hour, 0)
            self.assertEqual(t.minute, 0)
            self.assertEqual(t.second, 0)
            self.assertEqual(t.microsecond, 0)
            self.assertTrue(t.tzinfo is None)
            return

        def test_zones(self):
            est = FixedOffset(-300, 'EST', 1)
            utc = FixedOffset(0, 'UTC', -2)
            met = FixedOffset(60, 'MET', 3)
            t1 = time(7, 47, tzinfo=est)
            t2 = time(12, 47, tzinfo=utc)
            t3 = time(13, 47, tzinfo=met)
            t4 = time(microsecond=40)
            t5 = time(microsecond=40, tzinfo=utc)
            self.assertEqual(t1.tzinfo, est)
            self.assertEqual(t2.tzinfo, utc)
            self.assertEqual(t3.tzinfo, met)
            self.assertTrue(t4.tzinfo is None)
            self.assertEqual(t5.tzinfo, utc)
            self.assertEqual(t1.utcoffset(), timedelta(minutes=-300))
            self.assertEqual(t2.utcoffset(), timedelta(minutes=0))
            self.assertEqual(t3.utcoffset(), timedelta(minutes=60))
            self.assertTrue(t4.utcoffset() is None)
            self.assertRaises(TypeError, t1.utcoffset, 'no args')
            self.assertEqual(t1.tzname(), 'EST')
            self.assertEqual(t2.tzname(), 'UTC')
            self.assertEqual(t3.tzname(), 'MET')
            self.assertTrue(t4.tzname() is None)
            self.assertRaises(TypeError, t1.tzname, 'no args')
            self.assertEqual(t1.dst(), timedelta(minutes=1))
            self.assertEqual(t2.dst(), timedelta(minutes=-2))
            self.assertEqual(t3.dst(), timedelta(minutes=3))
            self.assertTrue(t4.dst() is None)
            self.assertRaises(TypeError, t1.dst, 'no args')
            self.assertEqual(hash(t1), hash(t2))
            self.assertEqual(hash(t1), hash(t3))
            self.assertEqual(hash(t2), hash(t3))
            self.assertEqual(t1, t2)
            self.assertEqual(t1, t3)
            self.assertEqual(t2, t3)
            self.assertRaises(TypeError, lambda : t4 == t5)
            self.assertRaises(TypeError, lambda : t4 < t5)
            self.assertRaises(TypeError, lambda : t5 < t4)
            self.assertEqual(str(t1), '07:47:00-05:00')
            self.assertEqual(str(t2), '12:47:00+00:00')
            self.assertEqual(str(t3), '13:47:00+01:00')
            self.assertEqual(str(t4), '00:00:00.000040')
            self.assertEqual(str(t5), '00:00:00.000040+00:00')
            self.assertEqual(t1.isoformat(), '07:47:00-05:00')
            self.assertEqual(t2.isoformat(), '12:47:00+00:00')
            self.assertEqual(t3.isoformat(), '13:47:00+01:00')
            self.assertEqual(t4.isoformat(), '00:00:00.000040')
            self.assertEqual(t5.isoformat(), '00:00:00.000040+00:00')
            d = 'datetime.time'
            self.assertEqual(repr(t1), d + '(7, 47, tzinfo=est)')
            self.assertEqual(repr(t2), d + '(12, 47, tzinfo=utc)')
            self.assertEqual(repr(t3), d + '(13, 47, tzinfo=met)')
            self.assertEqual(repr(t4), d + '(0, 0, 0, 40)')
            self.assertEqual(repr(t5), d + '(0, 0, 0, 40, tzinfo=utc)')
            self.assertEqual(t1.strftime('%H:%M:%S %%Z=%Z %%z=%z'), '07:47:00 %Z=EST %z=-0500')
            self.assertEqual(t2.strftime('%H:%M:%S %Z %z'), '12:47:00 UTC +0000')
            self.assertEqual(t3.strftime('%H:%M:%S %Z %z'), '13:47:00 MET +0100')
            yuck = FixedOffset(-1439, '%z %Z %%z%%Z')
            t1 = time(23, 59, tzinfo=yuck)
            self.assertEqual(t1.strftime("%H:%M %%Z='%Z' %%z='%z'"), "23:59 %Z='%z %Z %%z%%Z' %z='-2359'")

            class Badtzname(tzinfo):

                def tzname(self, dt):
                    return 42

            t = time(2, 3, 4, tzinfo=Badtzname())
            self.assertEqual(t.strftime('%H:%M:%S'), '02:03:04')
            self.assertRaises(TypeError, t.strftime, '%Z')
            return

        def test_hash_edge_cases(self):
            t1 = self.theclass(0, 1, 2, 3, tzinfo=FixedOffset(1439, ''))
            t2 = self.theclass(0, 0, 2, 3, tzinfo=FixedOffset(1438, ''))
            self.assertEqual(hash(t1), hash(t2))
            t1 = self.theclass(23, 58, 6, 100, tzinfo=FixedOffset(-1000, ''))
            t2 = self.theclass(23, 48, 6, 100, tzinfo=FixedOffset(-1010, ''))
            self.assertEqual(hash(t1), hash(t2))

        def test_pickling(self):
            args = (20,
             59,
             16,
             4096)
            orig = self.theclass(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

            tinfo = PicklableFixedOffset(-300, 'cookie')
            orig = self.theclass(5, 6, 7, tzinfo=tinfo)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)
                self.assertIsInstance(derived.tzinfo, PicklableFixedOffset)
                self.assertEqual(derived.utcoffset(), timedelta(minutes=-300))
                self.assertEqual(derived.tzname(), 'cookie')

        def test_more_bool(self):
            cls = self.theclass
            t = cls(0, tzinfo=FixedOffset(-300, ''))
            self.assertTrue(t)
            t = cls(5, tzinfo=FixedOffset(-300, ''))
            self.assertTrue(t)
            t = cls(5, tzinfo=FixedOffset(300, ''))
            self.assertTrue(not t)
            t = cls(23, 59, tzinfo=FixedOffset(1439, ''))
            self.assertTrue(not t)
            t = cls(0, tzinfo=FixedOffset(1439, ''))
            self.assertTrue(t)
            t = cls(0, tzinfo=FixedOffset(1440, ''))
            self.assertRaises(ValueError, lambda : bool(t))
            t = cls(0, tzinfo=FixedOffset(-1440, ''))
            self.assertRaises(ValueError, lambda : bool(t))

        def test_replace(self):
            cls = self.theclass
            z100 = FixedOffset(100, '+100')
            zm200 = FixedOffset(timedelta(minutes=-200), '-200')
            args = [1,
             2,
             3,
             4,
             z100]
            base = cls(*args)
            self.assertEqual(base, base.replace())
            i = 0
            for name, newval in (('hour', 5),
             ('minute', 6),
             ('second', 7),
             ('microsecond', 8),
             ('tzinfo', zm200)):
                newargs = args[:]
                newargs[i] = newval
                expected = cls(*newargs)
                got = base.replace(**{name: newval})
                self.assertEqual(expected, got)
                i += 1

            self.assertEqual(base.tzname(), '+100')
            base2 = base.replace(tzinfo=None)
            self.assertTrue(base2.tzinfo is None)
            self.assertTrue(base2.tzname() is None)
            base3 = base2.replace(tzinfo=z100)
            self.assertEqual(base, base3)
            self.assertTrue(base.tzinfo is base3.tzinfo)
            base = cls(1)
            self.assertRaises(ValueError, base.replace, hour=24)
            self.assertRaises(ValueError, base.replace, minute=-1)
            self.assertRaises(ValueError, base.replace, second=100)
            self.assertRaises(ValueError, base.replace, microsecond=1000000)
            return

        def test_mixed_compare(self):
            t1 = time(1, 2, 3)
            t2 = time(1, 2, 3)
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=None)
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=FixedOffset(None, ''))
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=FixedOffset(0, ''))
            self.assertRaises(TypeError, lambda : t1 == t2)

            class Varies(tzinfo):

                def __init__(self):
                    self.offset = timedelta(minutes=22)

                def utcoffset(self, t):
                    self.offset += timedelta(minutes=1)
                    return self.offset

            v = Varies()
            t1 = t2.replace(tzinfo=v)
            t2 = t2.replace(tzinfo=v)
            self.assertEqual(t1.utcoffset(), timedelta(minutes=23))
            self.assertEqual(t2.utcoffset(), timedelta(minutes=24))
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=Varies())
            self.assertTrue(t1 < t2)
            return

        def test_subclass_timetz(self):

            class C(self.theclass):
                theAnswer = 42

                def __new__(cls, *args, **kws):
                    temp = kws.copy()
                    extra = temp.pop('extra')
                    result = self.theclass.__new__(cls, *args, **temp)
                    result.extra = extra
                    return result

                def newmeth(self, start):
                    return start + self.hour + self.second

            args = (4,
             5,
             6,
             500,
             FixedOffset(-300, 'EST', 1))
            dt1 = self.theclass(*args)
            dt2 = C(*args, **{'extra': 7})
            self.assertEqual(dt2.__class__, C)
            self.assertEqual(dt2.theAnswer, 42)
            self.assertEqual(dt2.extra, 7)
            self.assertEqual(dt1.utcoffset(), dt2.utcoffset())
            self.assertEqual(dt2.newmeth(-7), dt1.hour + dt1.second - 7)


    class TestDateTimeTZ(TestDateTime, TZInfoBase, unittest.TestCase):
        theclass = datetime

        def test_trivial(self):
            dt = self.theclass(1, 2, 3, 4, 5, 6, 7)
            self.assertEqual(dt.year, 1)
            self.assertEqual(dt.month, 2)
            self.assertEqual(dt.day, 3)
            self.assertEqual(dt.hour, 4)
            self.assertEqual(dt.minute, 5)
            self.assertEqual(dt.second, 6)
            self.assertEqual(dt.microsecond, 7)
            self.assertEqual(dt.tzinfo, None)
            return

        def test_even_more_compare(self):
            t1 = self.theclass(1, 1, 1, tzinfo=FixedOffset(1439, ''))
            t2 = self.theclass(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=FixedOffset(-1439, ''))
            self.assertTrue(t1 < t2)
            self.assertTrue(t1 != t2)
            self.assertTrue(t2 > t1)
            self.assertTrue(t1 == t1)
            self.assertTrue(t2 == t2)
            t1 = self.theclass(1, 12, 31, 23, 59, tzinfo=FixedOffset(1, ''))
            t2 = self.theclass(2, 1, 1, 3, 13, tzinfo=FixedOffset(195, ''))
            self.assertEqual(t1, t2)
            t1 = self.theclass(1, 12, 31, 23, 59, tzinfo=FixedOffset(0, ''))
            self.assertTrue(t1 > t2)
            t1 = self.theclass(1, 12, 31, 23, 59, tzinfo=FixedOffset(2, ''))
            self.assertTrue(t1 < t2)
            t1 = self.theclass(1, 12, 31, 23, 59, tzinfo=FixedOffset(1, ''), second=1)
            self.assertTrue(t1 > t2)
            t1 = self.theclass(1, 12, 31, 23, 59, tzinfo=FixedOffset(1, ''), microsecond=1)
            self.assertTrue(t1 > t2)
            t2 = self.theclass.min
            self.assertRaises(TypeError, lambda : t1 == t2)
            self.assertEqual(t2, t2)

            class Naive(tzinfo):

                def utcoffset(self, dt):
                    return None

            t2 = self.theclass(5, 6, 7, tzinfo=Naive())
            self.assertRaises(TypeError, lambda : t1 == t2)
            self.assertEqual(t2, t2)
            t1 = self.theclass(5, 6, 7)
            self.assertEqual(t1, t2)

            class Bogus(tzinfo):

                def utcoffset(self, dt):
                    return timedelta(minutes=1440)

            t1 = self.theclass(2, 2, 2, tzinfo=Bogus())
            t2 = self.theclass(2, 2, 2, tzinfo=FixedOffset(0, ''))
            self.assertRaises(ValueError, lambda : t1 == t2)

        def test_pickling(self):
            args = (6,
             7,
             23,
             20,
             59,
             1,
             4096)
            orig = self.theclass(*args)
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)

            tinfo = PicklableFixedOffset(-300, 'cookie')
            orig = self.theclass(*args, **{'tzinfo': tinfo})
            derived = self.theclass(1, 1, 1, tzinfo=FixedOffset(0, '', 0))
            for pickler, unpickler, proto in pickle_choices:
                green = pickler.dumps(orig, proto)
                derived = unpickler.loads(green)
                self.assertEqual(orig, derived)
                self.assertIsInstance(derived.tzinfo, PicklableFixedOffset)
                self.assertEqual(derived.utcoffset(), timedelta(minutes=-300))
                self.assertEqual(derived.tzname(), 'cookie')

        def test_extreme_hashes(self):
            t = self.theclass(1, 1, 1, tzinfo=FixedOffset(1439, ''))
            hash(t)
            t = self.theclass(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=FixedOffset(-1439, ''))
            hash(t)
            t = self.theclass(5, 5, 5, tzinfo=FixedOffset(-1440, ''))
            self.assertRaises(ValueError, hash, t)

        def test_zones(self):
            est = FixedOffset(-300, 'EST')
            utc = FixedOffset(0, 'UTC')
            met = FixedOffset(60, 'MET')
            t1 = datetime(2002, 3, 19, 7, 47, tzinfo=est)
            t2 = datetime(2002, 3, 19, 12, 47, tzinfo=utc)
            t3 = datetime(2002, 3, 19, 13, 47, tzinfo=met)
            self.assertEqual(t1.tzinfo, est)
            self.assertEqual(t2.tzinfo, utc)
            self.assertEqual(t3.tzinfo, met)
            self.assertEqual(t1.utcoffset(), timedelta(minutes=-300))
            self.assertEqual(t2.utcoffset(), timedelta(minutes=0))
            self.assertEqual(t3.utcoffset(), timedelta(minutes=60))
            self.assertEqual(t1.tzname(), 'EST')
            self.assertEqual(t2.tzname(), 'UTC')
            self.assertEqual(t3.tzname(), 'MET')
            self.assertEqual(hash(t1), hash(t2))
            self.assertEqual(hash(t1), hash(t3))
            self.assertEqual(hash(t2), hash(t3))
            self.assertEqual(t1, t2)
            self.assertEqual(t1, t3)
            self.assertEqual(t2, t3)
            self.assertEqual(str(t1), '2002-03-19 07:47:00-05:00')
            self.assertEqual(str(t2), '2002-03-19 12:47:00+00:00')
            self.assertEqual(str(t3), '2002-03-19 13:47:00+01:00')
            d = 'datetime.datetime(2002, 3, 19, '
            self.assertEqual(repr(t1), d + '7, 47, tzinfo=est)')
            self.assertEqual(repr(t2), d + '12, 47, tzinfo=utc)')
            self.assertEqual(repr(t3), d + '13, 47, tzinfo=met)')

        def test_combine(self):
            met = FixedOffset(60, 'MET')
            d = date(2002, 3, 4)
            tz = time(18, 45, 3, 1234, tzinfo=met)
            dt = datetime.combine(d, tz)
            self.assertEqual(dt, datetime(2002, 3, 4, 18, 45, 3, 1234, tzinfo=met))

        def test_extract(self):
            met = FixedOffset(60, 'MET')
            dt = self.theclass(2002, 3, 4, 18, 45, 3, 1234, tzinfo=met)
            self.assertEqual(dt.date(), date(2002, 3, 4))
            self.assertEqual(dt.time(), time(18, 45, 3, 1234))
            self.assertEqual(dt.timetz(), time(18, 45, 3, 1234, tzinfo=met))

        def test_tz_aware_arithmetic(self):
            import random
            now = self.theclass.now()
            tz55 = FixedOffset(-330, 'west 5:30')
            timeaware = now.time().replace(tzinfo=tz55)
            nowaware = self.theclass.combine(now.date(), timeaware)
            self.assertTrue(nowaware.tzinfo is tz55)
            self.assertEqual(nowaware.timetz(), timeaware)
            self.assertRaises(TypeError, lambda : now - nowaware)
            self.assertRaises(TypeError, lambda : nowaware - now)
            self.assertRaises(TypeError, lambda : now + nowaware)
            self.assertRaises(TypeError, lambda : nowaware + now)
            self.assertRaises(TypeError, lambda : nowaware + nowaware)
            self.assertEqual(now - now, timedelta(0))
            self.assertEqual(nowaware - nowaware, timedelta(0))
            delta = timedelta(weeks=1, minutes=12, microseconds=5678)
            nowawareplus = nowaware + delta
            self.assertTrue(nowaware.tzinfo is tz55)
            nowawareplus2 = delta + nowaware
            self.assertTrue(nowawareplus2.tzinfo is tz55)
            self.assertEqual(nowawareplus, nowawareplus2)
            diff = nowawareplus - delta
            self.assertTrue(diff.tzinfo is tz55)
            self.assertEqual(nowaware, diff)
            self.assertRaises(TypeError, lambda : delta - nowawareplus)
            self.assertEqual(nowawareplus - nowaware, delta)
            tzr = FixedOffset(random.randrange(-1439, 1440), 'randomtimezone')
            nowawareplus = nowawareplus.replace(tzinfo=tzr)
            self.assertTrue(nowawareplus.tzinfo is tzr)
            got = nowaware - nowawareplus
            expected = nowawareplus.utcoffset() - nowaware.utcoffset() - delta
            self.assertEqual(got, expected)
            min = self.theclass(1, 1, 1, tzinfo=FixedOffset(1439, 'min'))
            max = self.theclass(MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=FixedOffset(-1439, 'max'))
            maxdiff = max - min
            self.assertEqual(maxdiff, self.theclass.max - self.theclass.min + timedelta(minutes=2878))

        def test_tzinfo_now(self):
            meth = self.theclass.now
            base = meth()
            off42 = FixedOffset(42, '42')
            another = meth(off42)
            again = meth(tz=off42)
            self.assertTrue(another.tzinfo is again.tzinfo)
            self.assertEqual(another.utcoffset(), timedelta(minutes=42))
            self.assertRaises(TypeError, meth, 16)
            self.assertRaises(TypeError, meth, tzinfo=16)
            self.assertRaises(TypeError, meth, tinfo=off42)
            self.assertRaises(TypeError, meth, off42, off42)
            weirdtz = FixedOffset(timedelta(hours=15, minutes=58), 'weirdtz', 0)
            utc = FixedOffset(0, 'utc', 0)
            for dummy in range(3):
                now = datetime.now(weirdtz)
                self.assertTrue(now.tzinfo is weirdtz)
                utcnow = datetime.utcnow().replace(tzinfo=utc)
                now2 = utcnow.astimezone(weirdtz)
                if abs(now - now2) < timedelta(seconds=30):
                    break
            else:
                self.fail('utcnow(), now(tz), or astimezone() may be broken')

        def test_tzinfo_fromtimestamp(self):
            import time
            meth = self.theclass.fromtimestamp
            ts = time.time()
            base = meth(ts)
            off42 = FixedOffset(42, '42')
            another = meth(ts, off42)
            again = meth(ts, tz=off42)
            self.assertTrue(another.tzinfo is again.tzinfo)
            self.assertEqual(another.utcoffset(), timedelta(minutes=42))
            self.assertRaises(TypeError, meth, ts, 16)
            self.assertRaises(TypeError, meth, ts, tzinfo=16)
            self.assertRaises(TypeError, meth, ts, tinfo=off42)
            self.assertRaises(TypeError, meth, ts, off42, off42)
            self.assertRaises(TypeError, meth)
            timestamp = 1000000000
            utcdatetime = datetime.utcfromtimestamp(timestamp)
            utcoffset = timedelta(hours=-15, minutes=39)
            tz = FixedOffset(utcoffset, 'tz', 0)
            expected = utcdatetime + utcoffset
            got = datetime.fromtimestamp(timestamp, tz)
            self.assertEqual(expected, got.replace(tzinfo=None))
            return

        def test_tzinfo_utcnow(self):
            meth = self.theclass.utcnow
            base = meth()
            off42 = FixedOffset(42, '42')
            self.assertRaises(TypeError, meth, off42)
            self.assertRaises(TypeError, meth, tzinfo=off42)

        def test_tzinfo_utcfromtimestamp(self):
            import time
            meth = self.theclass.utcfromtimestamp
            ts = time.time()
            base = meth(ts)
            off42 = FixedOffset(42, '42')
            self.assertRaises(TypeError, meth, ts, off42)
            self.assertRaises(TypeError, meth, ts, tzinfo=off42)

        def test_tzinfo_timetuple(self):

            class DST(tzinfo):

                def __init__(self, dstvalue):
                    if isinstance(dstvalue, int):
                        dstvalue = timedelta(minutes=dstvalue)
                    self.dstvalue = dstvalue

                def dst(self, dt):
                    return self.dstvalue

            cls = self.theclass
            for dstvalue, flag in ((-33, 1),
             (33, 1),
             (0, 0),
             (None, -1)):
                d = cls(1, 1, 1, 10, 20, 30, 40, tzinfo=DST(dstvalue))
                t = d.timetuple()
                self.assertEqual(1, t.tm_year)
                self.assertEqual(1, t.tm_mon)
                self.assertEqual(1, t.tm_mday)
                self.assertEqual(10, t.tm_hour)
                self.assertEqual(20, t.tm_min)
                self.assertEqual(30, t.tm_sec)
                self.assertEqual(0, t.tm_wday)
                self.assertEqual(1, t.tm_yday)
                self.assertEqual(flag, t.tm_isdst)

            self.assertRaises(TypeError, cls(1, 1, 1, tzinfo=DST('x')).timetuple)
            self.assertEqual(cls(1, 1, 1, tzinfo=DST(1439)).timetuple().tm_isdst, 1)
            self.assertEqual(cls(1, 1, 1, tzinfo=DST(-1439)).timetuple().tm_isdst, 1)
            self.assertRaises(ValueError, cls(1, 1, 1, tzinfo=DST(1440)).timetuple)
            self.assertRaises(ValueError, cls(1, 1, 1, tzinfo=DST(-1440)).timetuple)
            return None

        def test_utctimetuple(self):

            class DST(tzinfo):

                def __init__(self, dstvalue):
                    if isinstance(dstvalue, int):
                        dstvalue = timedelta(minutes=dstvalue)
                    self.dstvalue = dstvalue

                def dst(self, dt):
                    return self.dstvalue

            cls = self.theclass
            self.assertRaises(NotImplementedError, cls(1, 1, 1, tzinfo=DST(0)).utcoffset)

            class UOFS(DST):

                def __init__(self, uofs, dofs = None):
                    DST.__init__(self, dofs)
                    self.uofs = timedelta(minutes=uofs)

                def utcoffset(self, dt):
                    return self.uofs

            for dstvalue in (-33, 33, 0, None):
                d = cls(1, 2, 3, 10, 20, 30, 40, tzinfo=UOFS(-53, dstvalue))
                t = d.utctimetuple()
                self.assertEqual(d.year, t.tm_year)
                self.assertEqual(d.month, t.tm_mon)
                self.assertEqual(d.day, t.tm_mday)
                self.assertEqual(11, t.tm_hour)
                self.assertEqual(13, t.tm_min)
                self.assertEqual(d.second, t.tm_sec)
                self.assertEqual(d.weekday(), t.tm_wday)
                self.assertEqual(d.toordinal() - date(1, 1, 1).toordinal() + 1, t.tm_yday)
                self.assertEqual(0, t.tm_isdst)

            tiny = cls(MINYEAR, 1, 1, 0, 0, 37, tzinfo=UOFS(1439))
            t = tiny.utctimetuple()
            self.assertEqual(t.tm_year, MINYEAR - 1)
            self.assertEqual(t.tm_mon, 12)
            self.assertEqual(t.tm_mday, 31)
            self.assertEqual(t.tm_hour, 0)
            self.assertEqual(t.tm_min, 1)
            self.assertEqual(t.tm_sec, 37)
            self.assertEqual(t.tm_yday, 366)
            self.assertEqual(t.tm_isdst, 0)
            huge = cls(MAXYEAR, 12, 31, 23, 59, 37, 999999, tzinfo=UOFS(-1439))
            t = huge.utctimetuple()
            self.assertEqual(t.tm_year, MAXYEAR + 1)
            self.assertEqual(t.tm_mon, 1)
            self.assertEqual(t.tm_mday, 1)
            self.assertEqual(t.tm_hour, 23)
            self.assertEqual(t.tm_min, 58)
            self.assertEqual(t.tm_sec, 37)
            self.assertEqual(t.tm_yday, 1)
            self.assertEqual(t.tm_isdst, 0)
            return None

        def test_tzinfo_isoformat(self):
            zero = FixedOffset(0, '+00:00')
            plus = FixedOffset(220, '+03:40')
            minus = FixedOffset(-231, '-03:51')
            unknown = FixedOffset(None, '')
            cls = self.theclass
            datestr = '0001-02-03'
            for ofs in (None,
             zero,
             plus,
             minus,
             unknown):
                for us in (0, 987001):
                    d = cls(1, 2, 3, 4, 5, 59, us, tzinfo=ofs)
                    timestr = '04:05:59' + (us and '.987001' or '')
                    ofsstr = ofs is not None and d.tzname() or ''
                    tailstr = timestr + ofsstr
                    iso = d.isoformat()
                    self.assertEqual(iso, datestr + 'T' + tailstr)
                    self.assertEqual(iso, d.isoformat('T'))
                    self.assertEqual(d.isoformat('k'), datestr + 'k' + tailstr)
                    self.assertEqual(str(d), datestr + ' ' + tailstr)

            return

        def test_replace(self):
            cls = self.theclass
            z100 = FixedOffset(100, '+100')
            zm200 = FixedOffset(timedelta(minutes=-200), '-200')
            args = [1,
             2,
             3,
             4,
             5,
             6,
             7,
             z100]
            base = cls(*args)
            self.assertEqual(base, base.replace())
            i = 0
            for name, newval in (('year', 2),
             ('month', 3),
             ('day', 4),
             ('hour', 5),
             ('minute', 6),
             ('second', 7),
             ('microsecond', 8),
             ('tzinfo', zm200)):
                newargs = args[:]
                newargs[i] = newval
                expected = cls(*newargs)
                got = base.replace(**{name: newval})
                self.assertEqual(expected, got)
                i += 1

            self.assertEqual(base.tzname(), '+100')
            base2 = base.replace(tzinfo=None)
            self.assertTrue(base2.tzinfo is None)
            self.assertTrue(base2.tzname() is None)
            base3 = base2.replace(tzinfo=z100)
            self.assertEqual(base, base3)
            self.assertTrue(base.tzinfo is base3.tzinfo)
            base = cls(2000, 2, 29)
            self.assertRaises(ValueError, base.replace, year=2001)
            return

        def test_more_astimezone(self):
            fnone = FixedOffset(None, 'None')
            f44m = FixedOffset(44, '44')
            fm5h = FixedOffset(-timedelta(hours=5), 'm300')
            dt = self.theclass.now(tz=f44m)
            self.assertTrue(dt.tzinfo is f44m)
            self.assertRaises(ValueError, dt.astimezone, fnone)
            self.assertRaises(TypeError, dt.astimezone, None)
            x = dt.astimezone(dt.tzinfo)
            self.assertTrue(x.tzinfo is f44m)
            self.assertEqual(x.date(), dt.date())
            self.assertEqual(x.time(), dt.time())
            got = dt.astimezone(fm5h)
            self.assertTrue(got.tzinfo is fm5h)
            self.assertEqual(got.utcoffset(), timedelta(hours=-5))
            expected = dt - dt.utcoffset()
            expected += fm5h.utcoffset(dt)
            expected = expected.replace(tzinfo=fm5h)
            self.assertEqual(got.date(), expected.date())
            self.assertEqual(got.time(), expected.time())
            self.assertEqual(got.timetz(), expected.timetz())
            self.assertTrue(got.tzinfo is expected.tzinfo)
            self.assertEqual(got, expected)
            return

        def test_aware_subtract(self):
            cls = self.theclass

            class OperandDependentOffset(tzinfo):

                def utcoffset(self, t):
                    if t.minute < 10:
                        return timedelta(minutes=t.minute)
                    else:
                        return timedelta(minutes=59)

            base = cls(8, 9, 10, 11, 12, 13, 14, tzinfo=OperandDependentOffset())
            d0 = base.replace(minute=3)
            d1 = base.replace(minute=9)
            d2 = base.replace(minute=11)
            for x in (d0, d1, d2):
                for y in (d0, d1, d2):
                    got = x - y
                    expected = timedelta(minutes=x.minute - y.minute)
                    self.assertEqual(got, expected)

            base = cls(8, 9, 10, 11, 12, 13, 14)
            d0 = base.replace(minute=3, tzinfo=OperandDependentOffset())
            d1 = base.replace(minute=9, tzinfo=OperandDependentOffset())
            d2 = base.replace(minute=11, tzinfo=OperandDependentOffset())
            for x in (d0, d1, d2):
                for y in (d0, d1, d2):
                    got = x - y
                    if (x is d0 or x is d1) and (y is d0 or y is d1):
                        expected = timedelta(0)
                    elif x is y is d2:
                        expected = timedelta(0)
                    elif x is d2:
                        expected = timedelta(minutes=-48)
                    else:
                        raise y is d2 or AssertionError
                        expected = timedelta(minutes=0 - -48)
                    self.assertEqual(got, expected)

        def test_mixed_compare(self):
            t1 = datetime(1, 2, 3, 4, 5, 6, 7)
            t2 = datetime(1, 2, 3, 4, 5, 6, 7)
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=None)
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=FixedOffset(None, ''))
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=FixedOffset(0, ''))
            self.assertRaises(TypeError, lambda : t1 == t2)

            class Varies(tzinfo):

                def __init__(self):
                    self.offset = timedelta(minutes=22)

                def utcoffset(self, t):
                    self.offset += timedelta(minutes=1)
                    return self.offset

            v = Varies()
            t1 = t2.replace(tzinfo=v)
            t2 = t2.replace(tzinfo=v)
            self.assertEqual(t1.utcoffset(), timedelta(minutes=23))
            self.assertEqual(t2.utcoffset(), timedelta(minutes=24))
            self.assertEqual(t1, t2)
            t2 = t2.replace(tzinfo=Varies())
            self.assertTrue(t1 < t2)
            return

        def test_subclass_datetimetz(self):

            class C(self.theclass):
                theAnswer = 42

                def __new__(cls, *args, **kws):
                    temp = kws.copy()
                    extra = temp.pop('extra')
                    result = self.theclass.__new__(cls, *args, **temp)
                    result.extra = extra
                    return result

                def newmeth(self, start):
                    return start + self.hour + self.year

            args = (2002,
             12,
             31,
             4,
             5,
             6,
             500,
             FixedOffset(-300, 'EST', 1))
            dt1 = self.theclass(*args)
            dt2 = C(*args, **{'extra': 7})
            self.assertEqual(dt2.__class__, C)
            self.assertEqual(dt2.theAnswer, 42)
            self.assertEqual(dt2.extra, 7)
            self.assertEqual(dt1.utcoffset(), dt2.utcoffset())
            self.assertEqual(dt2.newmeth(-7), dt1.hour + dt1.year - 7)


    def first_sunday_on_or_after(dt):
        days_to_go = 6 - dt.weekday()
        if days_to_go:
            dt += timedelta(days_to_go)
        return dt


    ZERO = timedelta(0)
    HOUR = timedelta(hours=1)
    DAY = timedelta(days=1)
    DSTSTART = datetime(1, 4, 1, 2)
    DSTEND = datetime(1, 10, 25, 1)

    class USTimeZone(tzinfo):

        def __init__(self, hours, reprname, stdname, dstname):
            self.stdoffset = timedelta(hours=hours)
            self.reprname = reprname
            self.stdname = stdname
            self.dstname = dstname

        def __repr__(self):
            return self.reprname

        def tzname(self, dt):
            if self.dst(dt):
                return self.dstname
            else:
                return self.stdname

        def utcoffset(self, dt):
            return self.stdoffset + self.dst(dt)

        def dst(self, dt):
            if dt is None or dt.tzinfo is None:
                return ZERO
            elif not dt.tzinfo is self:
                raise AssertionError
                start = first_sunday_on_or_after(DSTSTART.replace(year=dt.year))
                raise start.weekday() == 6 and start.month == 4 and start.day <= 7 or AssertionError
                end = first_sunday_on_or_after(DSTEND.replace(year=dt.year))
                raise end.weekday() == 6 and end.month == 10 and end.day >= 25 or AssertionError
                return start <= dt.replace(tzinfo=None) < end and HOUR
            else:
                return ZERO
                return


    Eastern = USTimeZone(-5, 'Eastern', 'EST', 'EDT')
    Central = USTimeZone(-6, 'Central', 'CST', 'CDT')
    Mountain = USTimeZone(-7, 'Mountain', 'MST', 'MDT')
    Pacific = USTimeZone(-8, 'Pacific', 'PST', 'PDT')
    utc_real = FixedOffset(0, 'UTC', 0)
    utc_fake = FixedOffset(-12 * 60, 'UTCfake', 0)

    class TestTimezoneConversions(unittest.TestCase):
        dston = datetime(2002, 4, 7, 2)
        dstoff = datetime(2002, 10, 27, 1)
        theclass = datetime

        def checkinside(self, dt, tz, utc, dston, dstoff):
            self.assertEqual(dt.dst(), HOUR)
            self.assertEqual(dt.astimezone(tz), dt)
            asutc = dt.astimezone(utc)
            there_and_back = asutc.astimezone(tz)
            if dt.date() == dston.date() and dt.hour == 2:
                self.assertEqual(there_and_back + HOUR, dt)
                self.assertEqual(there_and_back.dst(), ZERO)
                self.assertEqual(there_and_back.astimezone(utc), dt.astimezone(utc))
            else:
                self.assertEqual(dt, there_and_back)
            nexthour_utc = asutc + HOUR
            nexthour_tz = nexthour_utc.astimezone(tz)
            if dt.date() == dstoff.date() and dt.hour == 0:
                self.assertEqual(nexthour_tz, dt.replace(hour=1))
                nexthour_utc += HOUR
                nexthour_tz = nexthour_utc.astimezone(tz)
                self.assertEqual(nexthour_tz, dt.replace(hour=1))
            else:
                self.assertEqual(nexthour_tz - dt, HOUR)

        def checkoutside(self, dt, tz, utc):
            self.assertEqual(dt.dst(), ZERO)
            self.assertEqual(dt.astimezone(tz), dt)
            asutc = dt.astimezone(utc)
            there_and_back = asutc.astimezone(tz)
            self.assertEqual(dt, there_and_back)

        def convert_between_tz_and_utc(self, tz, utc):
            dston = self.dston.replace(tzinfo=tz)
            dstoff = self.dstoff.replace(tzinfo=tz)
            for delta in (timedelta(weeks=13),
             DAY,
             HOUR,
             timedelta(minutes=1),
             timedelta(microseconds=1)):
                self.checkinside(dston, tz, utc, dston, dstoff)
                for during in (dston + delta, dstoff - delta):
                    self.checkinside(during, tz, utc, dston, dstoff)

                self.checkoutside(dstoff, tz, utc)
                for outside in (dston - delta, dstoff + delta):
                    self.checkoutside(outside, tz, utc)

        def test_easy(self):
            self.convert_between_tz_and_utc(Eastern, utc_real)
            self.convert_between_tz_and_utc(Pacific, utc_real)
            self.convert_between_tz_and_utc(Eastern, utc_fake)
            self.convert_between_tz_and_utc(Pacific, utc_fake)
            self.convert_between_tz_and_utc(Eastern, Pacific)
            self.convert_between_tz_and_utc(Pacific, Eastern)

        def test_tricky(self):
            fourback = self.dston - timedelta(hours=4)
            ninewest = FixedOffset(-540, '-0900', 0)
            fourback = fourback.replace(tzinfo=ninewest)
            expected = self.dston.replace(hour=3)
            got = fourback.astimezone(Eastern).replace(tzinfo=None)
            self.assertEqual(expected, got)
            sixutc = self.dston.replace(hour=6, tzinfo=utc_real)
            expected = self.dston.replace(hour=1)
            got = sixutc.astimezone(Eastern).replace(tzinfo=None)
            self.assertEqual(expected, got)
            for utc in (utc_real, utc_fake):
                for tz in (Eastern, Pacific):
                    first_std_hour = self.dstoff - timedelta(hours=2)
                    first_std_hour -= tz.utcoffset(None)
                    asutc = first_std_hour + utc.utcoffset(None)
                    asutcbase = asutc.replace(tzinfo=utc)
                    for tzhour in (0, 1, 1, 2):
                        expectedbase = self.dstoff.replace(hour=tzhour)
                        for minute in (0, 30, 59):
                            expected = expectedbase.replace(minute=minute)
                            asutc = asutcbase.replace(minute=minute)
                            astz = asutc.astimezone(tz)
                            self.assertEqual(astz.replace(tzinfo=None), expected)

                        asutcbase += HOUR

            return

        def test_bogus_dst(self):

            class ok(tzinfo):

                def utcoffset(self, dt):
                    return HOUR

                def dst(self, dt):
                    return HOUR

            now = self.theclass.now().replace(tzinfo=utc_real)
            now.astimezone(ok())

            class notok(ok):

                def dst(self, dt):
                    return None

            self.assertRaises(ValueError, now.astimezone, notok())

        def test_fromutc(self):
            self.assertRaises(TypeError, Eastern.fromutc)
            now = datetime.utcnow().replace(tzinfo=utc_real)
            self.assertRaises(ValueError, Eastern.fromutc, now)
            now = now.replace(tzinfo=Eastern)
            enow = Eastern.fromutc(now)
            self.assertEqual(enow.tzinfo, Eastern)
            self.assertRaises(TypeError, Eastern.fromutc, now, now)
            self.assertRaises(TypeError, Eastern.fromutc, date.today())

            class FauxUSTimeZone(USTimeZone):

                def fromutc(self, dt):
                    return dt + self.stdoffset

            FEastern = FauxUSTimeZone(-5, 'FEastern', 'FEST', 'FEDT')
            start = self.dston.replace(hour=4, tzinfo=Eastern)
            fstart = start.replace(tzinfo=FEastern)
            for wall in (23, 0, 1, 3, 4, 5):
                expected = start.replace(hour=wall)
                if wall == 23:
                    expected -= timedelta(days=1)
                got = Eastern.fromutc(start)
                self.assertEqual(expected, got)
                expected = fstart + FEastern.stdoffset
                got = FEastern.fromutc(fstart)
                self.assertEqual(expected, got)
                got = fstart.replace(tzinfo=utc_real).astimezone(FEastern)
                self.assertEqual(expected, got)
                start += HOUR
                fstart += HOUR

            start = self.dstoff.replace(hour=4, tzinfo=Eastern)
            fstart = start.replace(tzinfo=FEastern)
            for wall in (0, 1, 1, 2, 3, 4):
                expected = start.replace(hour=wall)
                got = Eastern.fromutc(start)
                self.assertEqual(expected, got)
                expected = fstart + FEastern.stdoffset
                got = FEastern.fromutc(fstart)
                self.assertEqual(expected, got)
                got = fstart.replace(tzinfo=utc_real).astimezone(FEastern)
                self.assertEqual(expected, got)
                start += HOUR
                fstart += HOUR


    class Oddballs(unittest.TestCase):

        def test_bug_1028306(self):
            as_date = date.today()
            as_datetime = datetime.combine(as_date, time())
            self.assertTrue(as_date != as_datetime)
            self.assertTrue(as_datetime != as_date)
            self.assertTrue(not as_date == as_datetime)
            self.assertTrue(not as_datetime == as_date)
            self.assertRaises(TypeError, lambda : as_date < as_datetime)
            self.assertRaises(TypeError, lambda : as_datetime < as_date)
            self.assertRaises(TypeError, lambda : as_date <= as_datetime)
            self.assertRaises(TypeError, lambda : as_datetime <= as_date)
            self.assertRaises(TypeError, lambda : as_date > as_datetime)
            self.assertRaises(TypeError, lambda : as_datetime > as_date)
            self.assertRaises(TypeError, lambda : as_date >= as_datetime)
            self.assertRaises(TypeError, lambda : as_datetime >= as_date)
            self.assertTrue(as_date.__eq__(as_datetime))
            different_day = (as_date.day + 1) % 20 + 1
            self.assertTrue(not as_date.__eq__(as_datetime.replace(day=different_day)))
            date_sc = SubclassDate(as_date.year, as_date.month, as_date.day)
            self.assertEqual(as_date, date_sc)
            self.assertEqual(date_sc, as_date)
            datetime_sc = SubclassDatetime(as_datetime.year, as_datetime.month, as_date.day, 0, 0, 0)
            self.assertEqual(as_datetime, datetime_sc)
            self.assertEqual(datetime_sc, as_datetime)


    def test_main():
        test_support.run_unittest(__name__)


    __name__ == '__main__' and test_main()