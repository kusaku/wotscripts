# Embedded file name: scripts/common/Lib/test/test_weakref.py
import gc
import sys
import unittest
import UserList
import weakref
import operator
from test import test_support
ref_from_del = None

class C():

    def method(self):
        pass


class Callable():
    bar = None

    def __call__(self, x):
        self.bar = x


def create_function():

    def f():
        pass

    return f


def create_bound_method():
    return C().method


def create_unbound_method():
    return C.method


class TestBase(unittest.TestCase):

    def setUp(self):
        self.cbcalled = 0

    def callback(self, ref):
        self.cbcalled += 1


class ReferencesTestCase(TestBase):

    def test_basic_ref(self):
        self.check_basic_ref(C)
        self.check_basic_ref(create_function)
        self.check_basic_ref(create_bound_method)
        self.check_basic_ref(create_unbound_method)
        o = C()
        wr = weakref.ref(o)
        repr(wr)
        del o
        repr(wr)

    def test_basic_callback(self):
        self.check_basic_callback(C)
        self.check_basic_callback(create_function)
        self.check_basic_callback(create_bound_method)
        self.check_basic_callback(create_unbound_method)

    def test_multiple_callbacks(self):
        o = C()
        ref1 = weakref.ref(o, self.callback)
        ref2 = weakref.ref(o, self.callback)
        del o
        self.assertTrue(ref1() is None, 'expected reference to be invalidated')
        self.assertTrue(ref2() is None, 'expected reference to be invalidated')
        self.assertTrue(self.cbcalled == 2, 'callback not called the right number of times')
        return

    def test_multiple_selfref_callbacks(self):

        def callback(object, self = self):
            self.ref()

        c = C()
        self.ref = weakref.ref(c, callback)
        ref1 = weakref.ref(c, callback)
        del c

    def test_proxy_ref(self):
        o = C()
        o.bar = 1
        ref1 = weakref.proxy(o, self.callback)
        ref2 = weakref.proxy(o, self.callback)
        del o

        def check(proxy):
            proxy.bar

        self.assertRaises(weakref.ReferenceError, check, ref1)
        self.assertRaises(weakref.ReferenceError, check, ref2)
        self.assertRaises(weakref.ReferenceError, bool, weakref.proxy(C()))
        self.assertTrue(self.cbcalled == 2)

    def check_basic_ref(self, factory):
        o = factory()
        ref = weakref.ref(o)
        self.assertTrue(ref() is not None, 'weak reference to live object should be live')
        o2 = ref()
        self.assertTrue(o is o2, '<ref>() should return original object if live')
        return

    def check_basic_callback(self, factory):
        self.cbcalled = 0
        o = factory()
        ref = weakref.ref(o, self.callback)
        del o
        self.assertTrue(self.cbcalled == 1, "callback did not properly set 'cbcalled'")
        self.assertTrue(ref() is None, 'ref2 should be dead after deleting object reference')
        return

    def test_ref_reuse(self):
        o = C()
        ref1 = weakref.ref(o)
        proxy = weakref.proxy(o)
        ref2 = weakref.ref(o)
        self.assertTrue(ref1 is ref2, 'reference object w/out callback should be re-used')
        o = C()
        proxy = weakref.proxy(o)
        ref1 = weakref.ref(o)
        ref2 = weakref.ref(o)
        self.assertTrue(ref1 is ref2, 'reference object w/out callback should be re-used')
        self.assertTrue(weakref.getweakrefcount(o) == 2, 'wrong weak ref count for object')
        del proxy
        self.assertTrue(weakref.getweakrefcount(o) == 1, 'wrong weak ref count for object after deleting proxy')

    def test_proxy_reuse(self):
        o = C()
        proxy1 = weakref.proxy(o)
        ref = weakref.ref(o)
        proxy2 = weakref.proxy(o)
        self.assertTrue(proxy1 is proxy2, 'proxy object w/out callback should have been re-used')

    def test_basic_proxy(self):
        o = C()
        self.check_proxy(o, weakref.proxy(o))
        L = UserList.UserList()
        p = weakref.proxy(L)
        self.assertFalse(p, 'proxy for empty UserList should be false')
        p.append(12)
        self.assertEqual(len(L), 1)
        self.assertTrue(p, 'proxy for non-empty UserList should be true')
        with test_support.check_py3k_warnings():
            p[:] = [2, 3]
        self.assertEqual(len(L), 2)
        self.assertEqual(len(p), 2)
        self.assertIn(3, p, "proxy didn't support __contains__() properly")
        p[1] = 5
        self.assertEqual(L[1], 5)
        self.assertEqual(p[1], 5)
        L2 = UserList.UserList(L)
        p2 = weakref.proxy(L2)
        self.assertEqual(p, p2)
        L3 = UserList.UserList(range(10))
        p3 = weakref.proxy(L3)
        with test_support.check_py3k_warnings():
            self.assertEqual(L3[:], p3[:])
            self.assertEqual(L3[5:], p3[5:])
            self.assertEqual(L3[:5], p3[:5])
            self.assertEqual(L3[2:5], p3[2:5])

    def test_proxy_unicode(self):

        class C(object):

            def __str__(self):
                return 'string'

            def __unicode__(self):
                return u'unicode'

        instance = C()
        self.assertIn('__unicode__', dir(weakref.proxy(instance)))
        self.assertEqual(unicode(weakref.proxy(instance)), u'unicode')

    def test_proxy_index(self):

        class C:

            def __index__(self):
                return 10

        o = C()
        p = weakref.proxy(o)
        self.assertEqual(operator.index(p), 10)

    def test_proxy_div(self):

        class C:

            def __floordiv__(self, other):
                return 42

            def __ifloordiv__(self, other):
                return 21

        o = C()
        p = weakref.proxy(o)
        self.assertEqual(p // 5, 42)
        p //= 5
        self.assertEqual(p, 21)

    def test_shared_ref_without_callback(self):
        self.check_shared_without_callback(weakref.ref)

    def test_shared_proxy_without_callback(self):
        self.check_shared_without_callback(weakref.proxy)

    def check_shared_without_callback(self, makeref):
        o = Object(1)
        p1 = makeref(o, None)
        p2 = makeref(o, None)
        self.assertTrue(p1 is p2, 'both callbacks were None in the C API')
        del p1
        del p2
        p1 = makeref(o)
        p2 = makeref(o, None)
        self.assertTrue(p1 is p2, 'callbacks were NULL, None in the C API')
        del p1
        del p2
        p1 = makeref(o)
        p2 = makeref(o)
        self.assertTrue(p1 is p2, 'both callbacks were NULL in the C API')
        del p1
        del p2
        p1 = makeref(o, None)
        p2 = makeref(o)
        self.assertTrue(p1 is p2, 'callbacks were None, NULL in the C API')
        return

    def test_callable_proxy(self):
        o = Callable()
        ref1 = weakref.proxy(o)
        self.check_proxy(o, ref1)
        self.assertTrue(type(ref1) is weakref.CallableProxyType, 'proxy is not of callable type')
        ref1('twinkies!')
        self.assertTrue(o.bar == 'twinkies!', 'call through proxy not passed through to original')
        ref1(x='Splat.')
        self.assertTrue(o.bar == 'Splat.', 'call through proxy not passed through to original')
        self.assertRaises(TypeError, ref1)
        self.assertRaises(TypeError, ref1, 1, 2, 3)

    def check_proxy(self, o, proxy):
        o.foo = 1
        self.assertTrue(proxy.foo == 1, 'proxy does not reflect attribute addition')
        o.foo = 2
        self.assertTrue(proxy.foo == 2, 'proxy does not reflect attribute modification')
        del o.foo
        self.assertTrue(not hasattr(proxy, 'foo'), 'proxy does not reflect attribute removal')
        proxy.foo = 1
        self.assertTrue(o.foo == 1, 'object does not reflect attribute addition via proxy')
        proxy.foo = 2
        self.assertTrue(o.foo == 2, 'object does not reflect attribute modification via proxy')
        del proxy.foo
        self.assertTrue(not hasattr(o, 'foo'), 'object does not reflect attribute removal via proxy')

    def test_proxy_deletion(self):

        class Foo:
            result = None

            def __delitem__(self, accessor):
                self.result = accessor

        g = Foo()
        f = weakref.proxy(g)
        del f[0]
        self.assertEqual(f.result, 0)

    def test_proxy_bool(self):

        class List(list):
            pass

        lyst = List()
        self.assertEqual(bool(weakref.proxy(lyst)), bool(lyst))

    def test_getweakrefcount(self):
        o = C()
        ref1 = weakref.ref(o)
        ref2 = weakref.ref(o, self.callback)
        self.assertTrue(weakref.getweakrefcount(o) == 2, 'got wrong number of weak reference objects')
        proxy1 = weakref.proxy(o)
        proxy2 = weakref.proxy(o, self.callback)
        self.assertTrue(weakref.getweakrefcount(o) == 4, 'got wrong number of weak reference objects')
        del ref1
        del ref2
        del proxy1
        del proxy2
        self.assertTrue(weakref.getweakrefcount(o) == 0, 'weak reference objects not unlinked from referent when discarded.')
        self.assertTrue(weakref.getweakrefcount(1) == 0, 'got wrong number of weak reference objects for int')

    def test_getweakrefs(self):
        o = C()
        ref1 = weakref.ref(o, self.callback)
        ref2 = weakref.ref(o, self.callback)
        del ref1
        self.assertTrue(weakref.getweakrefs(o) == [ref2], 'list of refs does not match')
        o = C()
        ref1 = weakref.ref(o, self.callback)
        ref2 = weakref.ref(o, self.callback)
        del ref2
        self.assertTrue(weakref.getweakrefs(o) == [ref1], 'list of refs does not match')
        del ref1
        self.assertTrue(weakref.getweakrefs(o) == [], 'list of refs not cleared')
        self.assertTrue(weakref.getweakrefs(1) == [], 'list of refs does not match for int')

    def test_newstyle_number_ops(self):

        class F(float):
            pass

        f = F(2.0)
        p = weakref.proxy(f)
        self.assertTrue(p + 1.0 == 3.0)
        self.assertTrue(1.0 + p == 3.0)

    def test_callbacks_protected(self):

        class BogusError(Exception):
            pass

        data = {}

        def remove(k):
            del data[k]

        def encapsulate():
            f = lambda : ()
            data[weakref.ref(f, remove)] = None
            raise BogusError
            return

        try:
            encapsulate()
        except BogusError:
            pass
        else:
            self.fail('exception not properly restored')

        try:
            encapsulate()
        except BogusError:
            pass
        else:
            self.fail('exception not properly restored')

    def test_sf_bug_840829(self):
        import gc

        class C(object):
            pass

        c = C()
        wr = weakref.ref(c, lambda ignore: gc.collect())
        del c
        del wr
        c1 = C()
        c1.i = C()
        wr = weakref.ref(c1.i, lambda ignore: gc.collect())
        c2 = C()
        c2.c1 = c1
        del c1
        del c2

    def test_callback_in_cycle_1(self):
        import gc

        class J(object):
            pass

        class II(object):

            def acallback(self, ignore):
                self.J

        I = II()
        I.J = J
        I.wr = weakref.ref(J, I.acallback)
        del I
        del J
        del II
        gc.collect()

    def test_callback_in_cycle_2(self):
        import gc

        class J(object):
            pass

        class II:

            def acallback(self, ignore):
                self.J

        I = II()
        I.J = J
        I.wr = weakref.ref(J, I.acallback)
        del I
        del J
        del II
        gc.collect()

    def test_callback_in_cycle_3(self):
        import gc

        class C:

            def cb(self, ignore):
                self.me
                self.c1
                self.wr

        c1, c2 = C(), C()
        c2.me = c2
        c2.c1 = c1
        c2.wr = weakref.ref(c1, c2.cb)
        del c1
        del c2
        gc.collect()

    def test_callback_in_cycle_4(self):
        import gc

        class C(object):

            def cb(self, ignore):
                self.me
                self.c1
                self.wr

        class D:
            pass

        c1, c2 = D(), C()
        c2.me = c2
        c2.c1 = c1
        c2.wr = weakref.ref(c1, c2.cb)
        del c1
        del c2
        del C
        del D
        gc.collect()

    def test_callback_in_cycle_resurrection(self):
        import gc
        alist = []

        class C(object):

            def __init__(self, value):
                self.attribute = value

            def acallback(self, ignore):
                alist.append(self.c)

        c1, c2 = C(1), C(2)
        c1.c = c2
        c2.c = c1
        c1.wr = weakref.ref(c2, c1.acallback)
        c2.wr = weakref.ref(c1, c2.acallback)

        def C_went_away(ignore):
            alist.append('C went away')

        wr = weakref.ref(C, C_went_away)
        del c1
        del c2
        del C
        self.assertEqual(alist, [])
        gc.collect()
        self.assertEqual(alist, ['C went away'])
        self.assertEqual(wr(), None)
        del alist[:]
        gc.collect()
        self.assertEqual(alist, [])
        return

    def test_callbacks_on_callback(self):
        import gc
        alist = []

        def safe_callback(ignore):
            alist.append('safe_callback called')

        class C(object):

            def cb(self, ignore):
                alist.append('cb called')

        c, d = C(), C()
        c.other = d
        d.other = c
        callback = c.cb
        c.wr = weakref.ref(d, callback)
        d.wr = weakref.ref(callback, d.cb)
        external_wr = weakref.ref(callback, safe_callback)
        self.assertTrue(external_wr() is callback)
        del callback
        del c
        del d
        del C
        self.assertEqual(alist, [])
        gc.collect()
        self.assertEqual(alist, ['safe_callback called'])
        self.assertEqual(external_wr(), None)
        del alist[:]
        gc.collect()
        self.assertEqual(alist, [])
        return

    def test_gc_during_ref_creation(self):
        self.check_gc_during_creation(weakref.ref)

    def test_gc_during_proxy_creation(self):
        self.check_gc_during_creation(weakref.proxy)

    def check_gc_during_creation(self, makeref):
        thresholds = gc.get_threshold()
        gc.set_threshold(1, 1, 1)
        gc.collect()

        class A:
            pass

        def callback(*args):
            pass

        referenced = A()
        a = A()
        a.a = a
        a.wr = makeref(referenced)
        try:
            a = A()
            weakref.ref(referenced, callback)
        finally:
            gc.set_threshold(*thresholds)

    def test_ref_created_during_del(self):

        class Target(object):

            def __del__(self):
                global ref_from_del
                ref_from_del = weakref.ref(self)

        w = Target()

    def test_init(self):
        r = weakref.ref(Exception)
        self.assertRaises(TypeError, r.__init__, 0, 0, 0, 0, 0)
        gc.collect()

    def test_classes(self):

        class A(object):
            pass

        class B:
            pass

        l = []
        weakref.ref(int)
        a = weakref.ref(A, l.append)
        A = None
        gc.collect()
        self.assertEqual(a(), None)
        self.assertEqual(l, [a])
        b = weakref.ref(B, l.append)
        B = None
        gc.collect()
        self.assertEqual(b(), None)
        self.assertEqual(l, [a, b])
        return


class SubclassableWeakrefTestCase(TestBase):

    def test_subclass_refs(self):

        class MyRef(weakref.ref):

            def __init__(self, ob, callback = None, value = 42):
                self.value = value
                super(MyRef, self).__init__(ob, callback)

            def __call__(self):
                self.called = True
                return super(MyRef, self).__call__()

        o = Object('foo')
        mr = MyRef(o, value=24)
        self.assertTrue(mr() is o)
        self.assertTrue(mr.called)
        self.assertEqual(mr.value, 24)
        del o
        self.assertTrue(mr() is None)
        self.assertTrue(mr.called)
        return

    def test_subclass_refs_dont_replace_standard_refs(self):

        class MyRef(weakref.ref):
            pass

        o = Object(42)
        r1 = MyRef(o)
        r2 = weakref.ref(o)
        self.assertTrue(r1 is not r2)
        self.assertEqual(weakref.getweakrefs(o), [r2, r1])
        self.assertEqual(weakref.getweakrefcount(o), 2)
        r3 = MyRef(o)
        self.assertEqual(weakref.getweakrefcount(o), 3)
        refs = weakref.getweakrefs(o)
        self.assertEqual(len(refs), 3)
        self.assertTrue(r2 is refs[0])
        self.assertIn(r1, refs[1:])
        self.assertIn(r3, refs[1:])

    def test_subclass_refs_dont_conflate_callbacks(self):

        class MyRef(weakref.ref):
            pass

        o = Object(42)
        r1 = MyRef(o, id)
        r2 = MyRef(o, str)
        self.assertTrue(r1 is not r2)
        refs = weakref.getweakrefs(o)
        self.assertIn(r1, refs)
        self.assertIn(r2, refs)

    def test_subclass_refs_with_slots(self):

        class MyRef(weakref.ref):
            __slots__ = ('slot1', 'slot2')

            def __new__(type, ob, callback, slot1, slot2):
                return weakref.ref.__new__(type, ob, callback)

            def __init__(self, ob, callback, slot1, slot2):
                self.slot1 = slot1
                self.slot2 = slot2

            def meth(self):
                return self.slot1 + self.slot2

        o = Object(42)
        r = MyRef(o, None, 'abc', 'def')
        self.assertEqual(r.slot1, 'abc')
        self.assertEqual(r.slot2, 'def')
        self.assertEqual(r.meth(), 'abcdef')
        self.assertFalse(hasattr(r, '__dict__'))
        return

    def test_subclass_refs_with_cycle(self):

        class MyRef(weakref.ref):
            pass

        def callback(w):
            self.cbcalled += 1

        o = C()
        r1 = MyRef(o, callback)
        r1.o = o
        del o
        del r1
        self.assertEqual(self.cbcalled, 0)
        o = C()
        r1 = MyRef(o, callback)
        r2 = MyRef(o, callback)
        r1.r = r2
        r2.o = o
        del o
        del r2
        del r1
        self.assertEqual(self.cbcalled, 0)


class Object():

    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return '<Object %r>' % self.arg


class MappingTestCase(TestBase):
    COUNT = 10

    def test_weak_values(self):
        dict, objects = self.make_weak_valued_dict()
        for o in objects:
            self.assertTrue(weakref.getweakrefcount(o) == 1, 'wrong number of weak references to %r!' % o)
            self.assertTrue(o is dict[o.arg], 'wrong object returned by weak dict!')

        items1 = dict.items()
        items2 = dict.copy().items()
        items1.sort()
        items2.sort()
        self.assertTrue(items1 == items2, 'cloning of weak-valued dictionary did not work!')
        del items1
        del items2
        self.assertTrue(len(dict) == self.COUNT)
        del objects[0]
        self.assertTrue(len(dict) == self.COUNT - 1, 'deleting object did not cause dictionary update')
        del objects
        del o
        self.assertTrue(len(dict) == 0, 'deleting the values did not clear the dictionary')
        dict = weakref.WeakValueDictionary()
        self.assertRaises(KeyError, dict.__getitem__, 1)
        dict[2] = C()
        self.assertRaises(KeyError, dict.__getitem__, 2)

    def test_weak_keys(self):
        dict, objects = self.make_weak_keyed_dict()
        for o in objects:
            self.assertTrue(weakref.getweakrefcount(o) == 1, 'wrong number of weak references to %r!' % o)
            self.assertTrue(o.arg is dict[o], 'wrong object returned by weak dict!')

        items1 = dict.items()
        items2 = dict.copy().items()
        self.assertTrue(set(items1) == set(items2), 'cloning of weak-keyed dictionary did not work!')
        del items1
        del items2
        self.assertTrue(len(dict) == self.COUNT)
        del objects[0]
        self.assertTrue(len(dict) == self.COUNT - 1, 'deleting object did not cause dictionary update')
        del objects
        del o
        self.assertTrue(len(dict) == 0, 'deleting the keys did not clear the dictionary')
        o = Object(42)
        dict[o] = 'What is the meaning of the universe?'
        self.assertIn(o, dict)
        self.assertNotIn(34, dict)

    def test_weak_keyed_iters(self):
        dict, objects = self.make_weak_keyed_dict()
        self.check_iters(dict)
        refs = dict.keyrefs()
        self.assertEqual(len(refs), len(objects))
        objects2 = list(objects)
        for wr in refs:
            ob = wr()
            self.assertIn(ob, dict)
            self.assertEqual(ob.arg, dict[ob])
            objects2.remove(ob)

        self.assertEqual(len(objects2), 0)
        objects2 = list(objects)
        self.assertEqual(len(list(dict.iterkeyrefs())), len(objects))
        for wr in dict.iterkeyrefs():
            ob = wr()
            self.assertIn(ob, dict)
            self.assertEqual(ob.arg, dict[ob])
            objects2.remove(ob)

        self.assertEqual(len(objects2), 0)

    def test_weak_valued_iters(self):
        dict, objects = self.make_weak_valued_dict()
        self.check_iters(dict)
        refs = dict.valuerefs()
        self.assertEqual(len(refs), len(objects))
        objects2 = list(objects)
        for wr in refs:
            ob = wr()
            self.assertEqual(ob, dict[ob.arg])
            self.assertEqual(ob.arg, dict[ob.arg].arg)
            objects2.remove(ob)

        self.assertEqual(len(objects2), 0)
        objects2 = list(objects)
        self.assertEqual(len(list(dict.itervaluerefs())), len(objects))
        for wr in dict.itervaluerefs():
            ob = wr()
            self.assertEqual(ob, dict[ob.arg])
            self.assertEqual(ob.arg, dict[ob.arg].arg)
            objects2.remove(ob)

        self.assertEqual(len(objects2), 0)

    def check_iters(self, dict):
        items = dict.items()
        for item in dict.iteritems():
            items.remove(item)

        self.assertTrue(len(items) == 0, 'iteritems() did not touch all items')
        keys = dict.keys()
        for k in dict:
            keys.remove(k)

        self.assertTrue(len(keys) == 0, '__iter__() did not touch all keys')
        keys = dict.keys()
        for k in dict.iterkeys():
            keys.remove(k)

        self.assertTrue(len(keys) == 0, 'iterkeys() did not touch all keys')
        values = dict.values()
        for v in dict.itervalues():
            values.remove(v)

        self.assertTrue(len(values) == 0, 'itervalues() did not touch all values')

    def test_make_weak_keyed_dict_from_dict(self):
        o = Object(3)
        dict = weakref.WeakKeyDictionary({o: 364})
        self.assertTrue(dict[o] == 364)

    def test_make_weak_keyed_dict_from_weak_keyed_dict(self):
        o = Object(3)
        dict = weakref.WeakKeyDictionary({o: 364})
        dict2 = weakref.WeakKeyDictionary(dict)
        self.assertTrue(dict[o] == 364)

    def make_weak_keyed_dict(self):
        dict = weakref.WeakKeyDictionary()
        objects = map(Object, range(self.COUNT))
        for o in objects:
            dict[o] = o.arg

        return (dict, objects)

    def make_weak_valued_dict(self):
        dict = weakref.WeakValueDictionary()
        objects = map(Object, range(self.COUNT))
        for o in objects:
            dict[o.arg] = o

        return (dict, objects)

    def check_popitem(self, klass, key1, value1, key2, value2):
        weakdict = klass()
        weakdict[key1] = value1
        weakdict[key2] = value2
        self.assertTrue(len(weakdict) == 2)
        k, v = weakdict.popitem()
        self.assertTrue(len(weakdict) == 1)
        if k is key1:
            self.assertTrue(v is value1)
        else:
            self.assertTrue(v is value2)
        k, v = weakdict.popitem()
        self.assertTrue(len(weakdict) == 0)
        if k is key1:
            self.assertTrue(v is value1)
        else:
            self.assertTrue(v is value2)

    def test_weak_valued_dict_popitem(self):
        self.check_popitem(weakref.WeakValueDictionary, 'key1', C(), 'key2', C())

    def test_weak_keyed_dict_popitem(self):
        self.check_popitem(weakref.WeakKeyDictionary, C(), 'value 1', C(), 'value 2')

    def check_setdefault(self, klass, key, value1, value2):
        self.assertTrue(value1 is not value2, 'invalid test -- value parameters must be distinct objects')
        weakdict = klass()
        o = weakdict.setdefault(key, value1)
        self.assertIs(o, value1)
        self.assertIn(key, weakdict)
        self.assertIs(weakdict.get(key), value1)
        self.assertIs(weakdict[key], value1)
        o = weakdict.setdefault(key, value2)
        self.assertIs(o, value1)
        self.assertIn(key, weakdict)
        self.assertIs(weakdict.get(key), value1)
        self.assertIs(weakdict[key], value1)

    def test_weak_valued_dict_setdefault(self):
        self.check_setdefault(weakref.WeakValueDictionary, 'key', C(), C())

    def test_weak_keyed_dict_setdefault(self):
        self.check_setdefault(weakref.WeakKeyDictionary, C(), 'value 1', 'value 2')

    def check_update(self, klass, dict):
        weakdict = klass()
        weakdict.update(dict)
        self.assertEqual(len(weakdict), len(dict))
        for k in weakdict.keys():
            self.assertIn(k, dict, 'mysterious new key appeared in weak dict')
            v = dict.get(k)
            self.assertIs(v, weakdict[k])
            self.assertIs(v, weakdict.get(k))

        for k in dict.keys():
            self.assertIn(k, weakdict, 'original key disappeared in weak dict')
            v = dict[k]
            self.assertIs(v, weakdict[k])
            self.assertIs(v, weakdict.get(k))

    def test_weak_valued_dict_update(self):
        self.check_update(weakref.WeakValueDictionary, {1: C(),
         'a': C(),
         C(): C()})

    def test_weak_keyed_dict_update(self):
        self.check_update(weakref.WeakKeyDictionary, {C(): 1,
         C(): 2,
         C(): 3})

    def test_weak_keyed_delitem(self):
        d = weakref.WeakKeyDictionary()
        o1 = Object('1')
        o2 = Object('2')
        d[o1] = 'something'
        d[o2] = 'something'
        self.assertTrue(len(d) == 2)
        del d[o1]
        self.assertTrue(len(d) == 1)
        self.assertTrue(d.keys() == [o2])

    def test_weak_valued_delitem(self):
        d = weakref.WeakValueDictionary()
        o1 = Object('1')
        o2 = Object('2')
        d['something'] = o1
        d['something else'] = o2
        self.assertTrue(len(d) == 2)
        del d['something']
        self.assertTrue(len(d) == 1)
        self.assertTrue(d.items() == [('something else', o2)])

    def test_weak_keyed_bad_delitem(self):
        d = weakref.WeakKeyDictionary()
        o = Object('1')
        self.assertRaises(KeyError, d.__delitem__, o)
        self.assertRaises(KeyError, d.__getitem__, o)
        self.assertRaises(TypeError, d.__delitem__, 13)
        self.assertRaises(TypeError, d.__getitem__, 13)
        self.assertRaises(TypeError, d.__setitem__, 13, 13)

    def test_weak_keyed_cascading_deletes(self):
        d = weakref.WeakKeyDictionary()
        mutate = False

        class C(object):

            def __init__(self, i):
                self.value = i

            def __hash__(self):
                return hash(self.value)

            def __eq__(self, other):
                if mutate:
                    del objs[-1]
                return self.value == other.value

        objs = [ C(i) for i in range(4) ]
        for o in objs:
            d[o] = o.value

        del o
        objs = d.keys()
        objs.reverse()
        mutate = True
        count = 0
        for o in objs:
            count += 1
            del d[o]

        self.assertEqual(len(d), 0)
        self.assertEqual(count, 2)


from test import mapping_tests

class WeakValueDictionaryTestCase(mapping_tests.BasicTestMappingProtocol):
    """Check that WeakValueDictionary conforms to the mapping protocol"""
    __ref = {'key1': Object(1),
     'key2': Object(2),
     'key3': Object(3)}
    type2test = weakref.WeakValueDictionary

    def _reference(self):
        return self.__ref.copy()


class WeakKeyDictionaryTestCase(mapping_tests.BasicTestMappingProtocol):
    """Check that WeakKeyDictionary conforms to the mapping protocol"""
    __ref = {Object('key1'): 1,
     Object('key2'): 2,
     Object('key3'): 3}
    type2test = weakref.WeakKeyDictionary

    def _reference(self):
        return self.__ref.copy()


libreftest = ' Doctest for examples in the library reference: weakref.rst\n\n>>> import weakref\n>>> class Dict(dict):\n...     pass\n...\n>>> obj = Dict(red=1, green=2, blue=3)   # this object is weak referencable\n>>> r = weakref.ref(obj)\n>>> print r() is obj\nTrue\n\n>>> import weakref\n>>> class Object:\n...     pass\n...\n>>> o = Object()\n>>> r = weakref.ref(o)\n>>> o2 = r()\n>>> o is o2\nTrue\n>>> del o, o2\n>>> print r()\nNone\n\n>>> import weakref\n>>> class ExtendedRef(weakref.ref):\n...     def __init__(self, ob, callback=None, **annotations):\n...         super(ExtendedRef, self).__init__(ob, callback)\n...         self.__counter = 0\n...         for k, v in annotations.iteritems():\n...             setattr(self, k, v)\n...     def __call__(self):\n...         \'\'\'Return a pair containing the referent and the number of\n...         times the reference has been called.\n...         \'\'\'\n...         ob = super(ExtendedRef, self).__call__()\n...         if ob is not None:\n...             self.__counter += 1\n...             ob = (ob, self.__counter)\n...         return ob\n...\n>>> class A:   # not in docs from here, just testing the ExtendedRef\n...     pass\n...\n>>> a = A()\n>>> r = ExtendedRef(a, foo=1, bar="baz")\n>>> r.foo\n1\n>>> r.bar\n\'baz\'\n>>> r()[1]\n1\n>>> r()[1]\n2\n>>> r()[0] is a\nTrue\n\n\n>>> import weakref\n>>> _id2obj_dict = weakref.WeakValueDictionary()\n>>> def remember(obj):\n...     oid = id(obj)\n...     _id2obj_dict[oid] = obj\n...     return oid\n...\n>>> def id2obj(oid):\n...     return _id2obj_dict[oid]\n...\n>>> a = A()             # from here, just testing\n>>> a_id = remember(a)\n>>> id2obj(a_id) is a\nTrue\n>>> del a\n>>> try:\n...     id2obj(a_id)\n... except KeyError:\n...     print \'OK\'\n... else:\n...     print \'WeakValueDictionary error\'\nOK\n\n'
__test__ = {'libreftest': libreftest}

def test_main():
    test_support.run_unittest(ReferencesTestCase, MappingTestCase, WeakValueDictionaryTestCase, WeakKeyDictionaryTestCase, SubclassableWeakrefTestCase)
    test_support.run_doctest(sys.modules[__name__])


if __name__ == '__main__':
    test_main()