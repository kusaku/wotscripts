# Embedded file name: scripts/common/Lib/test/test_difflib.py
import difflib
from test.test_support import run_unittest, findfile
import unittest
import doctest
import sys

class TestWithAscii(unittest.TestCase):

    def test_one_insert(self):
        sm = difflib.SequenceMatcher(None, 'b' * 100, 'a' + 'b' * 100)
        self.assertAlmostEqual(sm.ratio(), 0.995, places=3)
        self.assertEqual(list(sm.get_opcodes()), [('insert', 0, 0, 0, 1), ('equal', 0, 100, 1, 101)])
        sm = difflib.SequenceMatcher(None, 'b' * 100, 'b' * 50 + 'a' + 'b' * 50)
        self.assertAlmostEqual(sm.ratio(), 0.995, places=3)
        self.assertEqual(list(sm.get_opcodes()), [('equal', 0, 50, 0, 50), ('insert', 50, 50, 50, 51), ('equal', 50, 100, 51, 101)])
        return

    def test_one_delete(self):
        sm = difflib.SequenceMatcher(None, 'a' * 40 + 'c' + 'b' * 40, 'a' * 40 + 'b' * 40)
        self.assertAlmostEqual(sm.ratio(), 0.994, places=3)
        self.assertEqual(list(sm.get_opcodes()), [('equal', 0, 40, 0, 40), ('delete', 40, 41, 40, 40), ('equal', 41, 81, 40, 80)])
        return


class TestAutojunk(unittest.TestCase):
    """Tests for the autojunk parameter added in 2.7"""

    def test_one_insert_homogenous_sequence(self):
        seq1 = 'b' * 200
        seq2 = 'a' + 'b' * 200
        sm = difflib.SequenceMatcher(None, seq1, seq2)
        self.assertAlmostEqual(sm.ratio(), 0, places=3)
        sm = difflib.SequenceMatcher(None, seq1, seq2, autojunk=False)
        self.assertAlmostEqual(sm.ratio(), 0.9975, places=3)
        return


class TestSFbugs(unittest.TestCase):

    def test_ratio_for_null_seqn(self):
        s = difflib.SequenceMatcher(None, [], [])
        self.assertEqual(s.ratio(), 1)
        self.assertEqual(s.quick_ratio(), 1)
        self.assertEqual(s.real_quick_ratio(), 1)
        return

    def test_comparing_empty_lists(self):
        group_gen = difflib.SequenceMatcher(None, [], []).get_grouped_opcodes()
        self.assertRaises(StopIteration, group_gen.next)
        diff_gen = difflib.unified_diff([], [])
        self.assertRaises(StopIteration, diff_gen.next)
        return

    def test_added_tab_hint(self):
        diff = list(difflib.Differ().compare(['\tI am a buggy'], ['\t\tI am a bug']))
        self.assertEqual('- \tI am a buggy', diff[0])
        self.assertEqual('?            --\n', diff[1])
        self.assertEqual('+ \t\tI am a bug', diff[2])
        self.assertEqual('? +\n', diff[3])


patch914575_from1 = '\n   1. Beautiful is beTTer than ugly.\n   2. Explicit is better than implicit.\n   3. Simple is better than complex.\n   4. Complex is better than complicated.\n'
patch914575_to1 = '\n   1. Beautiful is better than ugly.\n   3.   Simple is better than complex.\n   4. Complicated is better than complex.\n   5. Flat is better than nested.\n'
patch914575_from2 = '\n\t\tLine 1: preceeded by from:[tt] to:[ssss]\n  \t\tLine 2: preceeded by from:[sstt] to:[sssst]\n  \t \tLine 3: preceeded by from:[sstst] to:[ssssss]\nLine 4:  \thas from:[sst] to:[sss] after :\nLine 5: has from:[t] to:[ss] at end\t\n'
patch914575_to2 = '\n    Line 1: preceeded by from:[tt] to:[ssss]\n    \tLine 2: preceeded by from:[sstt] to:[sssst]\n      Line 3: preceeded by from:[sstst] to:[ssssss]\nLine 4:   has from:[sst] to:[sss] after :\nLine 5: has from:[t] to:[ss] at end\n'
patch914575_from3 = 'line 0\n1234567890123456789012345689012345\nline 1\nline 2\nline 3\nline 4   changed\nline 5   changed\nline 6   changed\nline 7\nline 8  subtracted\nline 9\n1234567890123456789012345689012345\nshort line\njust fits in!!\njust fits in two lines yup!!\nthe end'
patch914575_to3 = 'line 0\n1234567890123456789012345689012345\nline 1\nline 2    added\nline 3\nline 4   chanGEd\nline 5a  chanGed\nline 6a  changEd\nline 7\nline 8\nline 9\n1234567890\nanother long line that needs to be wrapped\njust fitS in!!\njust fits in two lineS yup!!\nthe end'

class TestSFpatches(unittest.TestCase):

    def test_html_diff(self):
        f1a = (patch914575_from1 + '123\n' * 10) * 3
        t1a = (patch914575_to1 + '123\n' * 10) * 3
        f1b = '456\n' * 10 + f1a
        t1b = '456\n' * 10 + t1a
        f1a = f1a.splitlines()
        t1a = t1a.splitlines()
        f1b = f1b.splitlines()
        t1b = t1b.splitlines()
        f2 = patch914575_from2.splitlines()
        t2 = patch914575_to2.splitlines()
        f3 = patch914575_from3
        t3 = patch914575_to3
        i = difflib.HtmlDiff()
        j = difflib.HtmlDiff(tabsize=2)
        k = difflib.HtmlDiff(wrapcolumn=14)
        full = i.make_file(f1a, t1a, 'from', 'to', context=False, numlines=5)
        tables = '\n'.join(['<h2>Context (first diff within numlines=5(default))</h2>',
         i.make_table(f1a, t1a, 'from', 'to', context=True),
         '<h2>Context (first diff after numlines=5(default))</h2>',
         i.make_table(f1b, t1b, 'from', 'to', context=True),
         '<h2>Context (numlines=6)</h2>',
         i.make_table(f1a, t1a, 'from', 'to', context=True, numlines=6),
         '<h2>Context (numlines=0)</h2>',
         i.make_table(f1a, t1a, 'from', 'to', context=True, numlines=0),
         '<h2>Same Context</h2>',
         i.make_table(f1a, f1a, 'from', 'to', context=True),
         '<h2>Same Full</h2>',
         i.make_table(f1a, f1a, 'from', 'to', context=False),
         '<h2>Empty Context</h2>',
         i.make_table([], [], 'from', 'to', context=True),
         '<h2>Empty Full</h2>',
         i.make_table([], [], 'from', 'to', context=False),
         '<h2>tabsize=2</h2>',
         j.make_table(f2, t2),
         '<h2>tabsize=default</h2>',
         i.make_table(f2, t2),
         '<h2>Context (wrapcolumn=14,numlines=0)</h2>',
         k.make_table(f3.splitlines(), t3.splitlines(), context=True, numlines=0),
         '<h2>wrapcolumn=14,splitlines()</h2>',
         k.make_table(f3.splitlines(), t3.splitlines()),
         '<h2>wrapcolumn=14,splitlines(True)</h2>',
         k.make_table(f3.splitlines(True), t3.splitlines(True))])
        actual = full.replace('</body>', '\n%s\n</body>' % tables)
        with open(findfile('test_difflib_expect.html')) as fp:
            self.assertEqual(actual, fp.read())

    def test_recursion_limit(self):
        limit = sys.getrecursionlimit()
        old = [ (i % 2 and 'K:%d' or 'V:A:%d') % i for i in range(limit * 2) ]
        new = [ (i % 2 and 'K:%d' or 'V:B:%d') % i for i in range(limit * 2) ]
        difflib.SequenceMatcher(None, old, new).get_opcodes()
        return


class TestOutputFormat(unittest.TestCase):

    def test_tab_delimiter(self):
        args = ['one',
         'two',
         'Original',
         'Current',
         '2005-01-26 23:30:50',
         '2010-04-02 10:20:52']
        ud = difflib.unified_diff(lineterm='', *args)
        self.assertEqual(list(ud)[0:2], ['--- Original\t2005-01-26 23:30:50', '+++ Current\t2010-04-02 10:20:52'])
        cd = difflib.context_diff(lineterm='', *args)
        self.assertEqual(list(cd)[0:2], ['*** Original\t2005-01-26 23:30:50', '--- Current\t2010-04-02 10:20:52'])

    def test_no_trailing_tab_on_empty_filedate(self):
        args = ['one',
         'two',
         'Original',
         'Current']
        ud = difflib.unified_diff(lineterm='', *args)
        self.assertEqual(list(ud)[0:2], ['--- Original', '+++ Current'])
        cd = difflib.context_diff(lineterm='', *args)
        self.assertEqual(list(cd)[0:2], ['*** Original', '--- Current'])

    def test_range_format_unified(self):
        spec = '           Each <range> field shall be of the form:\n             %1d", <beginning line number>  if the range contains exactly one line,\n           and:\n            "%1d,%1d", <beginning line number>, <number of lines> otherwise.\n           If a range is empty, its beginning line number shall be the number of\n           the line just before the range, or 0 if the empty range starts the file.\n        '
        fmt = difflib._format_range_unified
        self.assertEqual(fmt(3, 3), '3,0')
        self.assertEqual(fmt(3, 4), '4')
        self.assertEqual(fmt(3, 5), '4,2')
        self.assertEqual(fmt(3, 6), '4,3')
        self.assertEqual(fmt(0, 0), '0,0')

    def test_range_format_context(self):
        spec = '           The range of lines in file1 shall be written in the following format\n           if the range contains two or more lines:\n               "*** %d,%d ****\n", <beginning line number>, <ending line number>\n           and the following format otherwise:\n               "*** %d ****\n", <ending line number>\n           The ending line number of an empty range shall be the number of the preceding line,\n           or 0 if the range is at the start of the file.\n\n           Next, the range of lines in file2 shall be written in the following format\n           if the range contains two or more lines:\n               "--- %d,%d ----\n", <beginning line number>, <ending line number>\n           and the following format otherwise:\n               "--- %d ----\n", <ending line number>\n        '
        fmt = difflib._format_range_context
        self.assertEqual(fmt(3, 3), '3')
        self.assertEqual(fmt(3, 4), '4')
        self.assertEqual(fmt(3, 5), '4,5')
        self.assertEqual(fmt(3, 6), '4,6')
        self.assertEqual(fmt(0, 0), '0')


def test_main():
    difflib.HtmlDiff._default_prefix = 0
    Doctests = doctest.DocTestSuite(difflib)
    run_unittest(TestWithAscii, TestAutojunk, TestSFpatches, TestSFbugs, TestOutputFormat, Doctests)


if __name__ == '__main__':
    test_main()