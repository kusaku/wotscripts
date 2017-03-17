# Embedded file name: scripts/common/Lib/test/test_list.py
import sys
from test import test_support, list_tests

class ListTest(list_tests.CommonTest):
    type2test = list

    def test_basic(self):
        self.assertEqual(list([]), [])
        l0_3 = [0,
         1,
         2,
         3]
        l0_3_bis = list(l0_3)
        self.assertEqual(l0_3, l0_3_bis)
        self.assertTrue(l0_3 is not l0_3_bis)
        self.assertEqual(list(()), [])
        self.assertEqual(list((0, 1, 2, 3)), [0,
         1,
         2,
         3])
        self.assertEqual(list(''), [])
        self.assertEqual(list('spam'), ['s',
         'p',
         'a',
         'm'])
        if sys.maxsize == 2147483647:
            self.assertRaises(MemoryError, list, xrange(sys.maxint // 2))
        x = []
        x.extend((-y for y in x))
        self.assertEqual(x, [])

    def test_truth(self):
        super(ListTest, self).test_truth()
        self.assertTrue(not [])
        self.assertTrue([42])

    def test_identity(self):
        self.assertTrue([] is not [])

    def test_len(self):
        super(ListTest, self).test_len()
        self.assertEqual(len([]), 0)
        self.assertEqual(len([0]), 1)
        self.assertEqual(len([0, 1, 2]), 3)

    def test_overflow(self):
        lst = [4,
         5,
         6,
         7]
        n = int((sys.maxint * 2 + 2) // len(lst))

        def mul(a, b):
            return a * b

        def imul(a, b):
            a *= b

        self.assertRaises((MemoryError, OverflowError), mul, lst, n)
        self.assertRaises((MemoryError, OverflowError), imul, lst, n)


def test_main(verbose = None):
    test_support.run_unittest(ListTest)
    import sys
    if verbose and hasattr(sys, 'gettotalrefcount'):
        import gc
        counts = [None] * 5
        for i in xrange(len(counts)):
            test_support.run_unittest(ListTest)
            gc.collect()
            counts[i] = sys.gettotalrefcount()

        print counts
    return


if __name__ == '__main__':
    test_main(verbose=True)