# Embedded file name: scripts/common/Lib/test/test_memoryview.py
"""Unit tests for the memoryview

XXX We need more tests! Some tests are in test_bytes
"""
import unittest
import sys
import gc
import weakref
import array
from test import test_support
import io

class AbstractMemoryTests:
    source_bytes = 'abcdef'

    @property
    def _source(self):
        return self.source_bytes

    @property
    def _types(self):
        return filter(None, [self.ro_type, self.rw_type])

    def check_getitem_with_type(self, tp):
        item = self.getitem_type
        b = tp(self._source)
        oldrefcount = sys.getrefcount(b)
        m = self._view(b)
        self.assertEqual(m[0], item('a'))
        self.assertIsInstance(m[0], bytes)
        self.assertEqual(m[5], item('f'))
        self.assertEqual(m[-1], item('f'))
        self.assertEqual(m[-6], item('a'))
        self.assertRaises(IndexError, lambda : m[6])
        self.assertRaises(IndexError, lambda : m[-7])
        self.assertRaises(IndexError, lambda : m[sys.maxsize])
        self.assertRaises(IndexError, lambda : m[-sys.maxsize])
        self.assertRaises(TypeError, lambda : m[None])
        self.assertRaises(TypeError, lambda : m[0.0])
        self.assertRaises(TypeError, lambda : m['a'])
        m = None
        self.assertEqual(sys.getrefcount(b), oldrefcount)
        return

    def test_getitem(self):
        for tp in self._types:
            self.check_getitem_with_type(tp)

    def test_iter(self):
        for tp in self._types:
            b = tp(self._source)
            m = self._view(b)
            self.assertEqual(list(m), [ m[i] for i in range(len(m)) ])

    def test_repr(self):
        for tp in self._types:
            b = tp(self._source)
            m = self._view(b)
            self.assertIsInstance(m.__repr__(), str)

    def test_setitem_readonly(self):
        if not self.ro_type:
            return
        else:
            b = self.ro_type(self._source)
            oldrefcount = sys.getrefcount(b)
            m = self._view(b)

            def setitem(value):
                m[0] = value

            self.assertRaises(TypeError, setitem, 'a')
            self.assertRaises(TypeError, setitem, 65)
            self.assertRaises(TypeError, setitem, memoryview('a'))
            m = None
            self.assertEqual(sys.getrefcount(b), oldrefcount)
            return

    def test_setitem_writable(self):
        if not self.rw_type:
            return
        else:
            tp = self.rw_type
            b = self.rw_type(self._source)
            oldrefcount = sys.getrefcount(b)
            m = self._view(b)
            m[0] = tp('0')
            self._check_contents(tp, b, '0bcdef')
            m[1:3] = tp('12')
            self._check_contents(tp, b, '012def')
            m[1:1] = tp('')
            self._check_contents(tp, b, '012def')
            m[:] = tp('abcdef')
            self._check_contents(tp, b, 'abcdef')
            m[0:3] = m[2:5]
            self._check_contents(tp, b, 'cdedef')
            m[:] = tp('abcdef')
            m[2:5] = m[0:3]
            self._check_contents(tp, b, 'ababcf')

            def setitem(key, value):
                m[key] = tp(value)

            self.assertRaises(IndexError, setitem, 6, 'a')
            self.assertRaises(IndexError, setitem, -7, 'a')
            self.assertRaises(IndexError, setitem, sys.maxsize, 'a')
            self.assertRaises(IndexError, setitem, -sys.maxsize, 'a')
            self.assertRaises(TypeError, setitem, 0.0, 'a')
            self.assertRaises(TypeError, setitem, (0,), 'a')
            self.assertRaises(TypeError, setitem, 'a', 'a')
            self.assertRaises(ValueError, setitem, 0, '')
            self.assertRaises(ValueError, setitem, 0, 'ab')
            self.assertRaises(ValueError, setitem, slice(1, 1), 'a')
            self.assertRaises(ValueError, setitem, slice(0, 2), 'a')
            m = None
            self.assertEqual(sys.getrefcount(b), oldrefcount)
            return

    def test_delitem(self):
        for tp in self._types:
            b = tp(self._source)
            m = self._view(b)
            with self.assertRaises(TypeError):
                del m[1]
            with self.assertRaises(TypeError):
                del m[1:4]

    def test_tobytes(self):
        for tp in self._types:
            m = self._view(tp(self._source))
            b = m.tobytes()
            expected = ''.join((self.getitem_type(c) for c in 'abcdef'))
            self.assertEqual(b, expected)
            self.assertIsInstance(b, bytes)

    def test_tolist(self):
        for tp in self._types:
            m = self._view(tp(self._source))
            l = m.tolist()
            self.assertEqual(l, map(ord, 'abcdef'))

    def test_compare(self):
        for tp in self._types:
            m = self._view(tp(self._source))
            for tp_comp in self._types:
                self.assertTrue(m == tp_comp('abcdef'))
                self.assertFalse(m != tp_comp('abcdef'))
                self.assertFalse(m == tp_comp('abcde'))
                self.assertTrue(m != tp_comp('abcde'))
                self.assertFalse(m == tp_comp('abcde1'))
                self.assertTrue(m != tp_comp('abcde1'))

            self.assertTrue(m == m)
            self.assertTrue(m == m[:])
            self.assertTrue(m[0:6] == m[:])
            self.assertFalse(m[0:5] == m)
            self.assertFalse(m == u'abcdef')
            self.assertTrue(m != u'abcdef')
            self.assertFalse(u'abcdef' == m)
            self.assertTrue(u'abcdef' != m)

    def check_attributes_with_type(self, tp):
        m = self._view(tp(self._source))
        self.assertEqual(m.format, self.format)
        self.assertIsInstance(m.format, str)
        self.assertEqual(m.itemsize, self.itemsize)
        self.assertEqual(m.ndim, 1)
        self.assertEqual(m.shape, (6,))
        self.assertEqual(len(m), 6)
        self.assertEqual(m.strides, (self.itemsize,))
        self.assertEqual(m.suboffsets, None)
        return m

    def test_attributes_readonly(self):
        if not self.ro_type:
            return
        m = self.check_attributes_with_type(self.ro_type)
        self.assertEqual(m.readonly, True)

    def test_attributes_writable(self):
        if not self.rw_type:
            return
        m = self.check_attributes_with_type(self.rw_type)
        self.assertEqual(m.readonly, False)

    def test_gc(self):
        for tp in self._types:
            if not isinstance(tp, type):
                continue

            class MySource(tp):
                pass

            class MyObject:
                pass

            b = MySource(tp('abc'))
            m = self._view(b)
            o = MyObject()
            b.m = m
            b.o = o
            wr = weakref.ref(o)
            b = m = o = None
            gc.collect()
            self.assertTrue(wr() is None, wr())

        return

    def test_writable_readonly(self):
        tp = self.ro_type
        if tp is None:
            return
        else:
            b = tp(self._source)
            m = self._view(b)
            i = io.BytesIO('ZZZZ')
            self.assertRaises(TypeError, i.readinto, m)
            return


class BaseBytesMemoryTests(AbstractMemoryTests):
    ro_type = bytes
    rw_type = bytearray
    getitem_type = bytes
    itemsize = 1
    format = 'B'


class BaseMemoryviewTests:

    def _view(self, obj):
        return memoryview(obj)

    def _check_contents(self, tp, obj, contents):
        self.assertEqual(obj, tp(contents))


class BaseMemorySliceTests:
    source_bytes = 'XabcdefY'

    def _view(self, obj):
        m = memoryview(obj)
        return m[1:7]

    def _check_contents(self, tp, obj, contents):
        self.assertEqual(obj[1:7], tp(contents))

    def test_refs(self):
        for tp in self._types:
            m = memoryview(tp(self._source))
            oldrefcount = sys.getrefcount(m)
            m[1:2]
            self.assertEqual(sys.getrefcount(m), oldrefcount)


class BaseMemorySliceSliceTests:
    source_bytes = 'XabcdefY'

    def _view(self, obj):
        m = memoryview(obj)
        return m[:7][1:]

    def _check_contents(self, tp, obj, contents):
        self.assertEqual(obj[1:7], tp(contents))


class BytesMemoryviewTest(unittest.TestCase, BaseMemoryviewTests, BaseBytesMemoryTests):

    def test_constructor(self):
        for tp in self._types:
            ob = tp(self._source)
            self.assertTrue(memoryview(ob))
            self.assertTrue(memoryview(object=ob))
            self.assertRaises(TypeError, memoryview)
            self.assertRaises(TypeError, memoryview, ob, ob)
            self.assertRaises(TypeError, memoryview, argument=ob)
            self.assertRaises(TypeError, memoryview, ob, argument=True)


class BytesMemorySliceTest(unittest.TestCase, BaseMemorySliceTests, BaseBytesMemoryTests):
    pass


class BytesMemorySliceSliceTest(unittest.TestCase, BaseMemorySliceSliceTests, BaseBytesMemoryTests):
    pass


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()