# Embedded file name: scripts/common/Lib/test/test_linecache.py
""" Tests for the linecache module """
import linecache
import unittest
import os.path
from test import test_support as support
FILENAME = linecache.__file__
INVALID_NAME = '!@$)(!@#_1'
EMPTY = ''
TESTS = 'inspect_fodder inspect_fodder2 mapping_tests'
TESTS = TESTS.split()
TEST_PATH = os.path.dirname(support.__file__)
MODULES = 'linecache abc'.split()
MODULE_PATH = os.path.dirname(FILENAME)
SOURCE_1 = '\n" Docstring "\n\ndef function():\n    return result\n\n'
SOURCE_2 = '\ndef f():\n    return 1 + 1\n\na = f()\n\n'
SOURCE_3 = '\ndef f():\n    return 3'

class LineCacheTests(unittest.TestCase):

    def test_getline(self):
        getline = linecache.getline
        self.assertEqual(getline(FILENAME, 32768), EMPTY)
        self.assertEqual(getline(FILENAME, -1), EMPTY)
        self.assertRaises(TypeError, getline, FILENAME, 1.1)
        self.assertEqual(getline(EMPTY, 1), EMPTY)
        self.assertEqual(getline(INVALID_NAME, 1), EMPTY)
        for entry in TESTS:
            filename = os.path.join(TEST_PATH, entry) + '.py'
            for index, line in enumerate(open(filename)):
                self.assertEqual(line, getline(filename, index + 1))

        for entry in MODULES:
            filename = os.path.join(MODULE_PATH, entry) + '.py'
            for index, line in enumerate(open(filename)):
                self.assertEqual(line, getline(filename, index + 1))

        empty = linecache.getlines('a/b/c/__init__.py')
        self.assertEqual(empty, [])

    def test_no_ending_newline(self):
        self.addCleanup(support.unlink, support.TESTFN)
        with open(support.TESTFN, 'w') as fp:
            fp.write(SOURCE_3)
        lines = linecache.getlines(support.TESTFN)
        self.assertEqual(lines, ['\n', 'def f():\n', '    return 3\n'])

    def test_clearcache(self):
        cached = []
        for entry in TESTS:
            filename = os.path.join(TEST_PATH, entry) + '.py'
            cached.append(filename)
            linecache.getline(filename, 1)

        cached_empty = [ fn for fn in cached if fn not in linecache.cache ]
        self.assertEqual(cached_empty, [])
        linecache.clearcache()
        cached_empty = [ fn for fn in cached if fn in linecache.cache ]
        self.assertEqual(cached_empty, [])

    def test_checkcache(self):
        getline = linecache.getline
        source_name = support.TESTFN + '.py'
        self.addCleanup(support.unlink, source_name)
        with open(source_name, 'w') as source:
            source.write(SOURCE_1)
        getline(source_name, 1)
        source_list = []
        with open(source_name) as source:
            for index, line in enumerate(source):
                self.assertEqual(line, getline(source_name, index + 1))
                source_list.append(line)

        with open(source_name, 'w') as source:
            source.write(SOURCE_2)
        linecache.checkcache('dummy')
        for index, line in enumerate(source_list):
            self.assertEqual(line, getline(source_name, index + 1))

        linecache.checkcache(source_name)
        with open(source_name) as source:
            for index, line in enumerate(source):
                self.assertEqual(line, getline(source_name, index + 1))
                source_list.append(line)


def test_main():
    support.run_unittest(LineCacheTests)


if __name__ == '__main__':
    test_main()