# Embedded file name: scripts/common/Lib/test/test_deque.py
from collections import deque
import unittest
from test import test_support, seq_tests
import gc
import weakref
import copy
import cPickle as pickle
import random
BIG = 100000

def fail():
    raise SyntaxError
    yield 1


class BadCmp():

    def __eq__(self, other):
        raise RuntimeError


class MutateCmp():

    def __init__(self, deque, result):
        self.deque = deque
        self.result = result

    def __eq__(self, other):
        self.deque.clear()
        return self.result


class TestBasic(unittest.TestCase):

    def test_basics(self):
        d = deque(xrange(-5125, -5000))
        d.__init__(xrange(200))
        for i in xrange(200, 400):
            d.append(i)

        for i in reversed(xrange(-200, 0)):
            d.appendleft(i)

        self.assertEqual(list(d), range(-200, 400))
        self.assertEqual(len(d), 600)
        left = [ d.popleft() for i in xrange(250) ]
        self.assertEqual(left, range(-200, 50))
        self.assertEqual(list(d), range(50, 400))
        right = [ d.pop() for i in xrange(250) ]
        right.reverse()
        self.assertEqual(right, range(150, 400))
        self.assertEqual(list(d), range(50, 150))

    def test_maxlen(self):
        self.assertRaises(ValueError, deque, 'abc', -1)
        self.assertRaises(ValueError, deque, 'abc', -2)
        it = iter(range(10))
        d = deque(it, maxlen=3)
        self.assertEqual(list(it), [])
        self.assertEqual(repr(d), 'deque([7, 8, 9], maxlen=3)')
        self.assertEqual(list(d), range(7, 10))
        self.assertEqual(d, deque(range(10), 3))
        d.append(10)
        self.assertEqual(list(d), range(8, 11))
        d.appendleft(7)
        self.assertEqual(list(d), range(7, 10))
        d.extend([10, 11])
        self.assertEqual(list(d), range(9, 12))
        d.extendleft([8, 7])
        self.assertEqual(list(d), range(7, 10))
        d = deque(xrange(200), maxlen=10)
        d.append(d)
        test_support.unlink(test_support.TESTFN)
        fo = open(test_support.TESTFN, 'wb')
        try:
            print >> fo, d,
            fo.close()
            fo = open(test_support.TESTFN, 'rb')
            self.assertEqual(fo.read(), repr(d))
        finally:
            fo.close()
            test_support.unlink(test_support.TESTFN)

        d = deque(range(10), maxlen=None)
        self.assertEqual(repr(d), 'deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])')
        fo = open(test_support.TESTFN, 'wb')
        try:
            print >> fo, d,
            fo.close()
            fo = open(test_support.TESTFN, 'rb')
            self.assertEqual(fo.read(), repr(d))
        finally:
            fo.close()
            test_support.unlink(test_support.TESTFN)

        return

    def test_maxlen_zero(self):
        it = iter(range(100))
        deque(it, maxlen=0)
        self.assertEqual(list(it), [])
        it = iter(range(100))
        d = deque(maxlen=0)
        d.extend(it)
        self.assertEqual(list(it), [])
        it = iter(range(100))
        d = deque(maxlen=0)
        d.extendleft(it)
        self.assertEqual(list(it), [])

    def test_maxlen_attribute(self):
        self.assertEqual(deque().maxlen, None)
        self.assertEqual(deque('abc').maxlen, None)
        self.assertEqual(deque('abc', maxlen=4).maxlen, 4)
        self.assertEqual(deque('abc', maxlen=2).maxlen, 2)
        self.assertEqual(deque('abc', maxlen=0).maxlen, 0)
        with self.assertRaises(AttributeError):
            d = deque('abc')
            d.maxlen = 10
        return

    def test_count(self):
        for s in ('', 'abracadabra', 'simsalabim' * 500 + 'abc'):
            s = list(s)
            d = deque(s)
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                self.assertEqual(s.count(letter), d.count(letter), (s, d, letter))

        self.assertRaises(TypeError, d.count)
        self.assertRaises(TypeError, d.count, 1, 2)

        class BadCompare:

            def __eq__(self, other):
                raise ArithmeticError

        d = deque([1,
         2,
         BadCompare(),
         3])
        self.assertRaises(ArithmeticError, d.count, 2)
        d = deque([1, 2, 3])
        self.assertRaises(ArithmeticError, d.count, BadCompare())

        class MutatingCompare:

            def __eq__(self, other):
                self.d.pop()
                return True

        m = MutatingCompare()
        d = deque([1,
         2,
         3,
         m,
         4,
         5])
        m.d = d
        self.assertRaises(RuntimeError, d.count, 3)
        d = deque([None] * 16)
        for i in range(len(d)):
            d.rotate(-1)

        d.rotate(1)
        self.assertEqual(d.count(1), 0)
        self.assertEqual(d.count(None), 16)
        return

    def test_comparisons(self):
        d = deque('xabc')
        d.popleft()
        for e in [d,
         deque('abc'),
         deque('ab'),
         deque(),
         list(d)]:
            self.assertEqual(d == e, type(d) == type(e) and list(d) == list(e))
            self.assertEqual(d != e, not (type(d) == type(e) and list(d) == list(e)))

        args = map(deque, ('', 'a', 'b', 'ab', 'ba', 'abc', 'xba', 'xabc', 'cba'))
        for x in args:
            for y in args:
                self.assertEqual(x == y, list(x) == list(y), (x, y))
                self.assertEqual(x != y, list(x) != list(y), (x, y))
                self.assertEqual(x < y, list(x) < list(y), (x, y))
                self.assertEqual(x <= y, list(x) <= list(y), (x, y))
                self.assertEqual(x > y, list(x) > list(y), (x, y))
                self.assertEqual(x >= y, list(x) >= list(y), (x, y))
                self.assertEqual(cmp(x, y), cmp(list(x), list(y)), (x, y))

    def test_extend(self):
        d = deque('a')
        self.assertRaises(TypeError, d.extend, 1)
        d.extend('bcd')
        self.assertEqual(list(d), list('abcd'))
        d.extend(d)
        self.assertEqual(list(d), list('abcdabcd'))

    def test_iadd(self):
        d = deque('a')
        d += 'bcd'
        self.assertEqual(list(d), list('abcd'))
        d += d
        self.assertEqual(list(d), list('abcdabcd'))

    def test_extendleft(self):
        d = deque('a')
        self.assertRaises(TypeError, d.extendleft, 1)
        d.extendleft('bcd')
        self.assertEqual(list(d), list(reversed('abcd')))
        d.extendleft(d)
        self.assertEqual(list(d), list('abcddcba'))
        d = deque()
        d.extendleft(range(1000))
        self.assertEqual(list(d), list(reversed(range(1000))))
        self.assertRaises(SyntaxError, d.extendleft, fail())

    def test_getitem(self):
        n = 200
        d = deque(xrange(n))
        l = range(n)
        for i in xrange(n):
            d.popleft()
            l.pop(0)
            if random.random() < 0.5:
                d.append(i)
                l.append(i)
            for j in xrange(1 - len(l), len(l)):
                raise d[j] == l[j] or AssertionError

        d = deque('superman')
        self.assertEqual(d[0], 's')
        self.assertEqual(d[-1], 'n')
        d = deque()
        self.assertRaises(IndexError, d.__getitem__, 0)
        self.assertRaises(IndexError, d.__getitem__, -1)

    def test_setitem(self):
        n = 200
        d = deque(xrange(n))
        for i in xrange(n):
            d[i] = 10 * i

        self.assertEqual(list(d), [ 10 * i for i in xrange(n) ])
        l = list(d)
        for i in xrange(1 - n, 0, -1):
            d[i] = 7 * i
            l[i] = 7 * i

        self.assertEqual(list(d), l)

    def test_delitem(self):
        n = 500
        d = deque(xrange(n))
        self.assertRaises(IndexError, d.__delitem__, -n - 1)
        self.assertRaises(IndexError, d.__delitem__, n)
        for i in xrange(n):
            self.assertEqual(len(d), n - i)
            j = random.randrange(-len(d), len(d))
            val = d[j]
            self.assertIn(val, d)
            del d[j]
            self.assertNotIn(val, d)

        self.assertEqual(len(d), 0)

    def test_reverse(self):
        n = 500
        data = [ random.random() for i in range(n) ]
        for i in range(n):
            d = deque(data[:i])
            r = d.reverse()
            self.assertEqual(list(d), list(reversed(data[:i])))
            self.assertIs(r, None)
            d.reverse()
            self.assertEqual(list(d), data[:i])

        self.assertRaises(TypeError, d.reverse, 1)
        return

    def test_rotate(self):
        s = tuple('abcde')
        n = len(s)
        d = deque(s)
        d.rotate(1)
        self.assertEqual(''.join(d), 'eabcd')
        d = deque(s)
        d.rotate(-1)
        self.assertEqual(''.join(d), 'bcdea')
        d.rotate()
        self.assertEqual(tuple(d), s)
        for i in xrange(n * 3):
            d = deque(s)
            e = deque(d)
            d.rotate(i)
            for j in xrange(i):
                e.rotate(1)

            self.assertEqual(tuple(d), tuple(e))
            d.rotate(-i)
            self.assertEqual(tuple(d), s)
            e.rotate(n - i)
            self.assertEqual(tuple(e), s)

        for i in xrange(n * 3):
            d = deque(s)
            e = deque(d)
            d.rotate(-i)
            for j in xrange(i):
                e.rotate(-1)

            self.assertEqual(tuple(d), tuple(e))
            d.rotate(i)
            self.assertEqual(tuple(d), s)
            e.rotate(i - n)
            self.assertEqual(tuple(e), s)

        d = deque(s)
        e = deque(s)
        e.rotate(BIG + 17)
        dr = d.rotate
        for i in xrange(BIG + 17):
            dr()

        self.assertEqual(tuple(d), tuple(e))
        self.assertRaises(TypeError, d.rotate, 'x')
        self.assertRaises(TypeError, d.rotate, 1, 10)
        d = deque()
        d.rotate()
        self.assertEqual(d, deque())

    def test_len(self):
        d = deque('ab')
        self.assertEqual(len(d), 2)
        d.popleft()
        self.assertEqual(len(d), 1)
        d.pop()
        self.assertEqual(len(d), 0)
        self.assertRaises(IndexError, d.pop)
        self.assertEqual(len(d), 0)
        d.append('c')
        self.assertEqual(len(d), 1)
        d.appendleft('d')
        self.assertEqual(len(d), 2)
        d.clear()
        self.assertEqual(len(d), 0)

    def test_underflow(self):
        d = deque()
        self.assertRaises(IndexError, d.pop)
        self.assertRaises(IndexError, d.popleft)

    def test_clear(self):
        d = deque(xrange(100))
        self.assertEqual(len(d), 100)
        d.clear()
        self.assertEqual(len(d), 0)
        self.assertEqual(list(d), [])
        d.clear()
        self.assertEqual(list(d), [])

    def test_remove(self):
        d = deque('abcdefghcij')
        d.remove('c')
        self.assertEqual(d, deque('abdefghcij'))
        d.remove('c')
        self.assertEqual(d, deque('abdefghij'))
        self.assertRaises(ValueError, d.remove, 'c')
        self.assertEqual(d, deque('abdefghij'))
        d = deque(['a',
         'b',
         BadCmp(),
         'c'])
        e = deque(d)
        self.assertRaises(RuntimeError, d.remove, 'c')
        for x, y in zip(d, e):
            self.assertTrue(x is y)

        for match in (True, False):
            d = deque(['ab'])
            d.extend([MutateCmp(d, match), 'c'])
            self.assertRaises(IndexError, d.remove, 'c')
            self.assertEqual(d, deque())

    def test_repr(self):
        d = deque(xrange(200))
        e = eval(repr(d))
        self.assertEqual(list(d), list(e))
        d.append(d)
        self.assertIn('...', repr(d))

    def test_print(self):
        d = deque(xrange(200))
        d.append(d)
        test_support.unlink(test_support.TESTFN)
        fo = open(test_support.TESTFN, 'wb')
        try:
            print >> fo, d,
            fo.close()
            fo = open(test_support.TESTFN, 'rb')
            self.assertEqual(fo.read(), repr(d))
        finally:
            fo.close()
            test_support.unlink(test_support.TESTFN)

    def test_init(self):
        self.assertRaises(TypeError, deque, 'abc', 2, 3)
        self.assertRaises(TypeError, deque, 1)

    def test_hash(self):
        self.assertRaises(TypeError, hash, deque('abc'))

    def test_long_steadystate_queue_popleft(self):
        for size in (0, 1, 2, 100, 1000):
            d = deque(xrange(size))
            append, pop = d.append, d.popleft
            for i in xrange(size, BIG):
                append(i)
                x = pop()
                if x != i - size:
                    self.assertEqual(x, i - size)

            self.assertEqual(list(d), range(BIG - size, BIG))

    def test_long_steadystate_queue_popright(self):
        for size in (0, 1, 2, 100, 1000):
            d = deque(reversed(xrange(size)))
            append, pop = d.appendleft, d.pop
            for i in xrange(size, BIG):
                append(i)
                x = pop()
                if x != i - size:
                    self.assertEqual(x, i - size)

            self.assertEqual(list(reversed(list(d))), range(BIG - size, BIG))

    def test_big_queue_popleft(self):
        d = deque()
        append, pop = d.append, d.popleft
        for i in xrange(BIG):
            append(i)

        for i in xrange(BIG):
            x = pop()
            if x != i:
                self.assertEqual(x, i)

    def test_big_queue_popright(self):
        d = deque()
        append, pop = d.appendleft, d.pop
        for i in xrange(BIG):
            append(i)

        for i in xrange(BIG):
            x = pop()
            if x != i:
                self.assertEqual(x, i)

    def test_big_stack_right(self):
        d = deque()
        append, pop = d.append, d.pop
        for i in xrange(BIG):
            append(i)

        for i in reversed(xrange(BIG)):
            x = pop()
            if x != i:
                self.assertEqual(x, i)

        self.assertEqual(len(d), 0)

    def test_big_stack_left(self):
        d = deque()
        append, pop = d.appendleft, d.popleft
        for i in xrange(BIG):
            append(i)

        for i in reversed(xrange(BIG)):
            x = pop()
            if x != i:
                self.assertEqual(x, i)

        self.assertEqual(len(d), 0)

    def test_roundtrip_iter_init(self):
        d = deque(xrange(200))
        e = deque(d)
        self.assertNotEqual(id(d), id(e))
        self.assertEqual(list(d), list(e))

    def test_pickle(self):
        d = deque(xrange(200))
        for i in range(pickle.HIGHEST_PROTOCOL + 1):
            s = pickle.dumps(d, i)
            e = pickle.loads(s)
            self.assertNotEqual(id(d), id(e))
            self.assertEqual(list(d), list(e))

    def test_deepcopy(self):
        mut = [10]
        d = deque([mut])
        e = copy.deepcopy(d)
        self.assertEqual(list(d), list(e))
        mut[0] = 11
        self.assertNotEqual(id(d), id(e))
        self.assertNotEqual(list(d), list(e))

    def test_copy(self):
        mut = [10]
        d = deque([mut])
        e = copy.copy(d)
        self.assertEqual(list(d), list(e))
        mut[0] = 11
        self.assertNotEqual(id(d), id(e))
        self.assertEqual(list(d), list(e))

    def test_reversed(self):
        for s in ('abcd', xrange(2000)):
            self.assertEqual(list(reversed(deque(s))), list(reversed(s)))

    def test_gc_doesnt_blowup(self):
        import gc
        d = deque()
        for i in xrange(100):
            d.append(1)
            gc.collect()

    def test_container_iterator(self):

        class C(object):
            pass

        for i in range(2):
            obj = C()
            ref = weakref.ref(obj)
            if i == 0:
                container = deque([obj, 1])
            else:
                container = reversed(deque([obj, 1]))
            obj.x = iter(container)
            del obj
            del container
            gc.collect()
            self.assertTrue(ref() is None, 'Cycle was not collected')

        return


class TestVariousIteratorArgs(unittest.TestCase):

    def test_constructor(self):
        for s in ('123',
         '',
         range(1000),
         ('do', 1.2),
         xrange(2000, 2200, 5)):
            for g in (seq_tests.Sequence,
             seq_tests.IterFunc,
             seq_tests.IterGen,
             seq_tests.IterFuncStop,
             seq_tests.itermulti,
             seq_tests.iterfunc):
                self.assertEqual(list(deque(g(s))), list(g(s)))

            self.assertRaises(TypeError, deque, seq_tests.IterNextOnly(s))
            self.assertRaises(TypeError, deque, seq_tests.IterNoNext(s))
            self.assertRaises(ZeroDivisionError, deque, seq_tests.IterGenExc(s))

    def test_iter_with_altered_data(self):
        d = deque('abcdefg')
        it = iter(d)
        d.pop()
        self.assertRaises(RuntimeError, it.next)

    def test_runtime_error_on_empty_deque(self):
        d = deque()
        it = iter(d)
        d.append(10)
        self.assertRaises(RuntimeError, it.next)


class Deque(deque):
    pass


class DequeWithBadIter(deque):

    def __iter__(self):
        raise TypeError


class TestSubclass(unittest.TestCase):

    def test_basics(self):
        d = Deque(xrange(25))
        d.__init__(xrange(200))
        for i in xrange(200, 400):
            d.append(i)

        for i in reversed(xrange(-200, 0)):
            d.appendleft(i)

        self.assertEqual(list(d), range(-200, 400))
        self.assertEqual(len(d), 600)
        left = [ d.popleft() for i in xrange(250) ]
        self.assertEqual(left, range(-200, 50))
        self.assertEqual(list(d), range(50, 400))
        right = [ d.pop() for i in xrange(250) ]
        right.reverse()
        self.assertEqual(right, range(150, 400))
        self.assertEqual(list(d), range(50, 150))
        d.clear()
        self.assertEqual(len(d), 0)

    def test_copy_pickle(self):
        d = Deque('abc')
        e = d.__copy__()
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))
        e = Deque(d)
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))
        s = pickle.dumps(d)
        e = pickle.loads(s)
        self.assertNotEqual(id(d), id(e))
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))
        d = Deque('abcde', maxlen=4)
        e = d.__copy__()
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))
        e = Deque(d)
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))
        s = pickle.dumps(d)
        e = pickle.loads(s)
        self.assertNotEqual(id(d), id(e))
        self.assertEqual(type(d), type(e))
        self.assertEqual(list(d), list(e))

    def test_weakref(self):
        d = deque('gallahad')
        p = weakref.proxy(d)
        self.assertEqual(str(p), str(d))
        d = None
        self.assertRaises(ReferenceError, str, p)
        return

    def test_strange_subclass(self):

        class X(deque):

            def __iter__(self):
                return iter([])

        d1 = X([1, 2, 3])
        d2 = X([4, 5, 6])
        d1 == d2


class SubclassWithKwargs(deque):

    def __init__(self, newarg = 1):
        deque.__init__(self)


class TestSubclassWithKwargs(unittest.TestCase):

    def test_subclass_with_kwargs(self):
        SubclassWithKwargs(newarg=1)


libreftest = '\nExample from the Library Reference:  Doc/lib/libcollections.tex\n\n>>> from collections import deque\n>>> d = deque(\'ghi\')                 # make a new deque with three items\n>>> for elem in d:                   # iterate over the deque\'s elements\n...     print elem.upper()\nG\nH\nI\n>>> d.append(\'j\')                    # add a new entry to the right side\n>>> d.appendleft(\'f\')                # add a new entry to the left side\n>>> d                                # show the representation of the deque\ndeque([\'f\', \'g\', \'h\', \'i\', \'j\'])\n>>> d.pop()                          # return and remove the rightmost item\n\'j\'\n>>> d.popleft()                      # return and remove the leftmost item\n\'f\'\n>>> list(d)                          # list the contents of the deque\n[\'g\', \'h\', \'i\']\n>>> d[0]                             # peek at leftmost item\n\'g\'\n>>> d[-1]                            # peek at rightmost item\n\'i\'\n>>> list(reversed(d))                # list the contents of a deque in reverse\n[\'i\', \'h\', \'g\']\n>>> \'h\' in d                         # search the deque\nTrue\n>>> d.extend(\'jkl\')                  # add multiple elements at once\n>>> d\ndeque([\'g\', \'h\', \'i\', \'j\', \'k\', \'l\'])\n>>> d.rotate(1)                      # right rotation\n>>> d\ndeque([\'l\', \'g\', \'h\', \'i\', \'j\', \'k\'])\n>>> d.rotate(-1)                     # left rotation\n>>> d\ndeque([\'g\', \'h\', \'i\', \'j\', \'k\', \'l\'])\n>>> deque(reversed(d))               # make a new deque in reverse order\ndeque([\'l\', \'k\', \'j\', \'i\', \'h\', \'g\'])\n>>> d.clear()                        # empty the deque\n>>> d.pop()                          # cannot pop from an empty deque\nTraceback (most recent call last):\n  File "<pyshell#6>", line 1, in -toplevel-\n    d.pop()\nIndexError: pop from an empty deque\n\n>>> d.extendleft(\'abc\')              # extendleft() reverses the input order\n>>> d\ndeque([\'c\', \'b\', \'a\'])\n\n\n\n>>> def delete_nth(d, n):\n...     d.rotate(-n)\n...     d.popleft()\n...     d.rotate(n)\n...\n>>> d = deque(\'abcdef\')\n>>> delete_nth(d, 2)   # remove the entry at d[2]\n>>> d\ndeque([\'a\', \'b\', \'d\', \'e\', \'f\'])\n\n\n\n>>> def roundrobin(*iterables):\n...     pending = deque(iter(i) for i in iterables)\n...     while pending:\n...         task = pending.popleft()\n...         try:\n...             yield task.next()\n...         except StopIteration:\n...             continue\n...         pending.append(task)\n...\n\n>>> for value in roundrobin(\'abc\', \'d\', \'efgh\'):\n...     print value\n...\na\nd\ne\nb\nf\nc\ng\nh\n\n\n>>> def maketree(iterable):\n...     d = deque(iterable)\n...     while len(d) > 1:\n...         pair = [d.popleft(), d.popleft()]\n...         d.append(pair)\n...     return list(d)\n...\n>>> print maketree(\'abcdefgh\')\n[[[[\'a\', \'b\'], [\'c\', \'d\']], [[\'e\', \'f\'], [\'g\', \'h\']]]]\n\n'
__test__ = {'libreftest': libreftest}

def test_main(verbose = None):
    import sys
    test_classes = (TestBasic,
     TestVariousIteratorArgs,
     TestSubclass,
     TestSubclassWithKwargs)
    test_support.run_unittest(*test_classes)
    if verbose and hasattr(sys, 'gettotalrefcount'):
        import gc
        counts = [None] * 5
        for i in xrange(len(counts)):
            test_support.run_unittest(*test_classes)
            gc.collect()
            counts[i] = sys.gettotalrefcount()

        print counts
    from test import test_deque
    test_support.run_doctest(test_deque, verbose)
    return


if __name__ == '__main__':
    test_main(verbose=True)