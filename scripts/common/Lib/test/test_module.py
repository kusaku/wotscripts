# Embedded file name: scripts/common/Lib/test/test_module.py
import unittest
from test.test_support import run_unittest, gc_collect
import sys
ModuleType = type(sys)

class ModuleTests(unittest.TestCase):

    def test_uninitialized(self):
        foo = ModuleType.__new__(ModuleType)
        self.assertTrue(foo.__dict__ is None)
        self.assertRaises(SystemError, dir, foo)
        try:
            s = foo.__name__
            self.fail('__name__ = %s' % repr(s))
        except AttributeError:
            pass

        self.assertEqual(foo.__doc__, ModuleType.__doc__)
        return

    def test_no_docstring(self):
        foo = ModuleType('foo')
        self.assertEqual(foo.__name__, 'foo')
        self.assertEqual(foo.__doc__, None)
        self.assertEqual(foo.__dict__, {'__name__': 'foo',
         '__doc__': None})
        return

    def test_ascii_docstring(self):
        foo = ModuleType('foo', 'foodoc')
        self.assertEqual(foo.__name__, 'foo')
        self.assertEqual(foo.__doc__, 'foodoc')
        self.assertEqual(foo.__dict__, {'__name__': 'foo',
         '__doc__': 'foodoc'})

    def test_unicode_docstring(self):
        foo = ModuleType('foo', u'foodoc\u1234')
        self.assertEqual(foo.__name__, 'foo')
        self.assertEqual(foo.__doc__, u'foodoc\u1234')
        self.assertEqual(foo.__dict__, {'__name__': 'foo',
         '__doc__': u'foodoc\u1234'})

    def test_reinit(self):
        foo = ModuleType('foo', u'foodoc\u1234')
        foo.bar = 42
        d = foo.__dict__
        foo.__init__('foo', 'foodoc')
        self.assertEqual(foo.__name__, 'foo')
        self.assertEqual(foo.__doc__, 'foodoc')
        self.assertEqual(foo.bar, 42)
        self.assertEqual(foo.__dict__, {'__name__': 'foo',
         '__doc__': 'foodoc',
         'bar': 42})
        self.assertTrue(foo.__dict__ is d)

    @unittest.expectedFailure
    def test_dont_clear_dict(self):

        def f():
            foo = ModuleType('foo')
            foo.bar = 4
            return foo

        gc_collect()
        self.assertEqual(f().__dict__['bar'], 4)

    def test_clear_dict_in_ref_cycle(self):
        destroyed = []
        m = ModuleType('foo')
        m.destroyed = destroyed
        s = 'class A:\n    def __del__(self, destroyed=destroyed):\n        destroyed.append(1)\na = A()'
        exec s in m.__dict__
        del m
        gc_collect()
        self.assertEqual(destroyed, [1])


def test_main():
    run_unittest(ModuleTests)


if __name__ == '__main__':
    test_main()