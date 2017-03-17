# Embedded file name: scripts/common/Lib/test/test_class.py
"""Test the functionality of Python classes implementing operators."""
import unittest
from test import test_support
testmeths = ['add',
 'radd',
 'sub',
 'rsub',
 'mul',
 'rmul',
 'div',
 'rdiv',
 'mod',
 'rmod',
 'divmod',
 'rdivmod',
 'pow',
 'rpow',
 'rshift',
 'rrshift',
 'lshift',
 'rlshift',
 'and',
 'rand',
 'or',
 'ror',
 'xor',
 'rxor',
 'contains',
 'getitem',
 'getslice',
 'setitem',
 'setslice',
 'delitem',
 'delslice',
 'neg',
 'pos',
 'abs',
 'init']
callLst = []

def trackCall(f):

    def track(*args, **kwargs):
        callLst.append((f.__name__, args))
        return f(*args, **kwargs)

    return track


class AllTests():
    trackCall = trackCall

    @trackCall
    def __coerce__(self, *args):
        return (self,) + args

    @trackCall
    def __hash__(self, *args):
        return hash(id(self))

    @trackCall
    def __str__(self, *args):
        return 'AllTests'

    @trackCall
    def __repr__(self, *args):
        return 'AllTests'

    @trackCall
    def __int__(self, *args):
        return 1

    @trackCall
    def __float__(self, *args):
        return 1.0

    @trackCall
    def __long__(self, *args):
        return 1L

    @trackCall
    def __oct__(self, *args):
        return '01'

    @trackCall
    def __hex__(self, *args):
        return '0x1'

    @trackCall
    def __cmp__(self, *args):
        return 0


method_template = '@trackCall\ndef __%(method)s__(self, *args):\n    pass\n'
for method in testmeths:
    exec method_template % locals() in AllTests.__dict__

del method
del method_template

class ClassTests(unittest.TestCase):

    def setUp(self):
        callLst[:] = []

    def assertCallStack(self, expected_calls):
        actualCallList = callLst[:]
        if expected_calls != actualCallList:
            self.fail('Expected call list:\n  %s\ndoes not match actual call list\n  %s' % (expected_calls, actualCallList))

    def testInit(self):
        foo = AllTests()
        self.assertCallStack([('__init__', (foo,))])

    def testBinaryOps(self):
        testme = AllTests()
        callLst[:] = []
        testme + 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__add__', (testme, 1))])
        callLst[:] = []
        1 + testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__radd__', (testme, 1))])
        callLst[:] = []
        testme - 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__sub__', (testme, 1))])
        callLst[:] = []
        1 - testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rsub__', (testme, 1))])
        callLst[:] = []
        testme * 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__mul__', (testme, 1))])
        callLst[:] = []
        1 * testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rmul__', (testme, 1))])
        if 1 / 2 == 0:
            callLst[:] = []
            testme / 1
            self.assertCallStack([('__coerce__', (testme, 1)), ('__div__', (testme, 1))])
            callLst[:] = []
            1 / testme
            self.assertCallStack([('__coerce__', (testme, 1)), ('__rdiv__', (testme, 1))])
        callLst[:] = []
        testme % 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__mod__', (testme, 1))])
        callLst[:] = []
        1 % testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rmod__', (testme, 1))])
        callLst[:] = []
        divmod(testme, 1)
        self.assertCallStack([('__coerce__', (testme, 1)), ('__divmod__', (testme, 1))])
        callLst[:] = []
        divmod(1, testme)
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rdivmod__', (testme, 1))])
        callLst[:] = []
        testme ** 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__pow__', (testme, 1))])
        callLst[:] = []
        1 ** testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rpow__', (testme, 1))])
        callLst[:] = []
        testme >> 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rshift__', (testme, 1))])
        callLst[:] = []
        1 >> testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rrshift__', (testme, 1))])
        callLst[:] = []
        testme << 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__lshift__', (testme, 1))])
        callLst[:] = []
        1 << testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rlshift__', (testme, 1))])
        callLst[:] = []
        testme & 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__and__', (testme, 1))])
        callLst[:] = []
        1 & testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rand__', (testme, 1))])
        callLst[:] = []
        testme | 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__or__', (testme, 1))])
        callLst[:] = []
        1 | testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__ror__', (testme, 1))])
        callLst[:] = []
        testme ^ 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__xor__', (testme, 1))])
        callLst[:] = []
        1 ^ testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__rxor__', (testme, 1))])

    def testListAndDictOps(self):
        testme = AllTests()

        class Empty:
            pass

        try:
            1 in Empty()
            self.fail('failed, should have raised TypeError')
        except TypeError:
            pass

        callLst[:] = []
        1 in testme
        self.assertCallStack([('__contains__', (testme, 1))])
        callLst[:] = []
        testme[1]
        self.assertCallStack([('__getitem__', (testme, 1))])
        callLst[:] = []
        testme[1] = 1
        self.assertCallStack([('__setitem__', (testme, 1, 1))])
        callLst[:] = []
        del testme[1]
        self.assertCallStack([('__delitem__', (testme, 1))])
        callLst[:] = []
        testme[:42]
        self.assertCallStack([('__getslice__', (testme, 0, 42))])
        callLst[:] = []
        testme[:42] = 'The Answer'
        self.assertCallStack([('__setslice__', (testme,
           0,
           42,
           'The Answer'))])
        callLst[:] = []
        del testme[:42]
        self.assertCallStack([('__delslice__', (testme, 0, 42))])
        callLst[:] = []
        testme[2:1024:10]
        self.assertCallStack([('__getitem__', (testme, slice(2, 1024, 10)))])
        callLst[:] = []
        testme[2:1024:10] = 'A lot'
        self.assertCallStack([('__setitem__', (testme, slice(2, 1024, 10), 'A lot'))])
        callLst[:] = []
        del testme[2:1024:10]
        self.assertCallStack([('__delitem__', (testme, slice(2, 1024, 10)))])
        callLst[:] = []
        testme[:42, ..., :24:, 24, 100]
        self.assertCallStack([('__getitem__', (testme, (slice(None, 42, None),
            Ellipsis,
            slice(None, 24, None),
            24,
            100)))])
        callLst[:] = []
        testme[:42, ..., :24:, 24, 100] = 'Strange'
        self.assertCallStack([('__setitem__', (testme, (slice(None, 42, None),
            Ellipsis,
            slice(None, 24, None),
            24,
            100), 'Strange'))])
        callLst[:] = []
        del testme[:42, ..., :24:, 24, 100]
        self.assertCallStack([('__delitem__', (testme, (slice(None, 42, None),
            Ellipsis,
            slice(None, 24, None),
            24,
            100)))])
        getslice = AllTests.__getslice__
        del AllTests.__getslice__
        setslice = AllTests.__setslice__
        del AllTests.__setslice__
        delslice = AllTests.__delslice__
        del AllTests.__delslice__
        callLst[:] = []
        testme[:42]
        self.assertCallStack([('__getitem__', (testme, slice(0, 42, None)))])
        callLst[:] = []
        testme[:42] = 'The Answer'
        self.assertCallStack([('__setitem__', (testme, slice(0, 42, None), 'The Answer'))])
        callLst[:] = []
        del testme[:42]
        self.assertCallStack([('__delitem__', (testme, slice(0, 42, None)))])
        AllTests.__getslice__ = getslice
        AllTests.__setslice__ = setslice
        AllTests.__delslice__ = delslice
        return

    @test_support.cpython_only
    def testDelItem(self):

        class A:
            ok = False

            def __delitem__(self, key):
                self.ok = True

        a = A()
        from _testcapi import sequence_delitem
        sequence_delitem(a, 2)
        self.assertTrue(a.ok)

    def testUnaryOps(self):
        testme = AllTests()
        callLst[:] = []
        -testme
        self.assertCallStack([('__neg__', (testme,))])
        callLst[:] = []
        +testme
        self.assertCallStack([('__pos__', (testme,))])
        callLst[:] = []
        abs(testme)
        self.assertCallStack([('__abs__', (testme,))])
        callLst[:] = []
        int(testme)
        self.assertCallStack([('__int__', (testme,))])
        callLst[:] = []
        long(testme)
        self.assertCallStack([('__long__', (testme,))])
        callLst[:] = []
        float(testme)
        self.assertCallStack([('__float__', (testme,))])
        callLst[:] = []
        oct(testme)
        self.assertCallStack([('__oct__', (testme,))])
        callLst[:] = []
        hex(testme)
        self.assertCallStack([('__hex__', (testme,))])

    def testMisc(self):
        testme = AllTests()
        callLst[:] = []
        hash(testme)
        self.assertCallStack([('__hash__', (testme,))])
        callLst[:] = []
        repr(testme)
        self.assertCallStack([('__repr__', (testme,))])
        callLst[:] = []
        str(testme)
        self.assertCallStack([('__str__', (testme,))])
        callLst[:] = []
        testme == 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (testme, 1))])
        callLst[:] = []
        testme < 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (testme, 1))])
        callLst[:] = []
        testme > 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (testme, 1))])
        callLst[:] = []
        eval('testme <> 1')
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (testme, 1))])
        callLst[:] = []
        testme != 1
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (testme, 1))])
        callLst[:] = []
        1 == testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (1, testme))])
        callLst[:] = []
        1 < testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (1, testme))])
        callLst[:] = []
        1 > testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (1, testme))])
        callLst[:] = []
        eval('1 <> testme')
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (1, testme))])
        callLst[:] = []
        1 != testme
        self.assertCallStack([('__coerce__', (testme, 1)), ('__cmp__', (1, testme))])

    def testGetSetAndDel(self):

        class ExtraTests(AllTests):

            @trackCall
            def __getattr__(self, *args):
                return 'SomeVal'

            @trackCall
            def __setattr__(self, *args):
                pass

            @trackCall
            def __delattr__(self, *args):
                pass

        testme = ExtraTests()
        callLst[:] = []
        testme.spam
        self.assertCallStack([('__getattr__', (testme, 'spam'))])
        callLst[:] = []
        testme.eggs = 'spam, spam, spam and ham'
        self.assertCallStack([('__setattr__', (testme, 'eggs', 'spam, spam, spam and ham'))])
        callLst[:] = []
        del testme.cardinal
        self.assertCallStack([('__delattr__', (testme, 'cardinal'))])

    def testDel(self):
        x = []

        class DelTest:

            def __del__(self):
                x.append('crab people, crab people')

        testme = DelTest()
        del testme
        import gc
        gc.collect()
        self.assertEqual(['crab people, crab people'], x)

    def testBadTypeReturned(self):

        class BadTypeClass:

            def __int__(self):
                return None

            __float__ = __int__
            __long__ = __int__
            __str__ = __int__
            __repr__ = __int__
            __oct__ = __int__
            __hex__ = __int__

        for f in [int,
         float,
         long,
         str,
         repr,
         oct,
         hex]:
            self.assertRaises(TypeError, f, BadTypeClass())

    def testMixIntsAndLongs(self):

        class IntLongMixClass:

            @trackCall
            def __int__(self):
                return 42L

            @trackCall
            def __long__(self):
                return 64

        mixIntAndLong = IntLongMixClass()
        callLst[:] = []
        as_int = int(mixIntAndLong)
        self.assertEqual(type(as_int), long)
        self.assertEqual(as_int, 42L)
        self.assertCallStack([('__int__', (mixIntAndLong,))])
        callLst[:] = []
        as_long = long(mixIntAndLong)
        self.assertEqual(type(as_long), long)
        self.assertEqual(as_long, 64)
        self.assertCallStack([('__long__', (mixIntAndLong,))])

    def testHashStuff(self):

        class C0:
            pass

        hash(C0())

        class C1:

            def __cmp__(self, other):
                return 0

        self.assertRaises(TypeError, hash, C1())

        class C2:

            def __eq__(self, other):
                return 1

        self.assertRaises(TypeError, hash, C2())

    def testSFBug532646(self):

        class A:
            pass

        A.__call__ = A()
        a = A()
        try:
            a()
        except RuntimeError:
            pass
        else:
            self.fail('Failed to raise RuntimeError')

    def testForExceptionsRaisedInInstanceGetattr2(self):

        def booh(self):
            raise AttributeError('booh')

        class A:
            a = property(booh)

        try:
            A().a
        except AttributeError as x:
            if str(x) != 'booh':
                self.fail('attribute error for A().a got masked: %s' % x)

        class E:
            __eq__ = property(booh)

        E() == E()

        class I:
            __init__ = property(booh)

        try:
            I()
        except AttributeError as x:
            pass
        else:
            self.fail('attribute error for I.__init__ got masked')

    def testHashComparisonOfMethods(self):

        class A:

            def __init__(self, x):
                self.x = x

            def f(self):
                pass

            def g(self):
                pass

            def __eq__(self, other):
                return self.x == other.x

            def __hash__(self):
                return self.x

        class B(A):
            pass

        a1 = A(1)
        a2 = A(2)
        self.assertEqual(a1.f, a1.f)
        self.assertNotEqual(a1.f, a2.f)
        self.assertNotEqual(a1.f, a1.g)
        self.assertEqual(a1.f, A(1).f)
        self.assertEqual(hash(a1.f), hash(a1.f))
        self.assertEqual(hash(a1.f), hash(A(1).f))
        self.assertNotEqual(A.f, a1.f)
        self.assertNotEqual(A.f, A.g)
        self.assertEqual(B.f, A.f)
        self.assertEqual(hash(B.f), hash(A.f))
        a = A(hash(A.f.im_func) ^ -1)
        hash(a.f)


def test_main():
    with test_support.check_py3k_warnings(('.+__(get|set|del)slice__ has been removed', DeprecationWarning), ('classic int division', DeprecationWarning), ('<> not supported', DeprecationWarning)):
        test_support.run_unittest(ClassTests)


if __name__ == '__main__':
    test_main()