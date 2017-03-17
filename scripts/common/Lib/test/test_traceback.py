# Embedded file name: scripts/common/Lib/test/test_traceback.py
"""Test cases for traceback module"""
from _testcapi import traceback_print
from StringIO import StringIO
import sys
import unittest
from imp import reload
from test.test_support import run_unittest, is_jython, Error
import traceback

class TracebackCases(unittest.TestCase):

    def get_exception_format(self, func, exc):
        try:
            func()
        except exc as value:
            return traceback.format_exception_only(exc, value)

        raise ValueError, 'call did not raise exception'

    def syntax_error_with_caret(self):
        compile('def fact(x):\n\treturn x!\n', '?', 'exec')

    def syntax_error_with_caret_2(self):
        compile('1 +\n', '?', 'exec')

    def syntax_error_without_caret(self):
        import test.badsyntax_nocaret

    def syntax_error_bad_indentation(self):
        compile('def spam():\n  print 1\n print 2', '?', 'exec')

    def test_caret(self):
        err = self.get_exception_format(self.syntax_error_with_caret, SyntaxError)
        self.assertTrue(len(err) == 4)
        self.assertTrue(err[1].strip() == 'return x!')
        self.assertIn('^', err[2])
        self.assertTrue(err[1].find('!') == err[2].find('^'))
        err = self.get_exception_format(self.syntax_error_with_caret_2, SyntaxError)
        self.assertIn('^', err[2])
        self.assertTrue(err[2].count('\n') == 1)
        self.assertTrue(err[1].find('+') == err[2].find('^'))

    def test_nocaret(self):
        if is_jython:
            return
        err = self.get_exception_format(self.syntax_error_without_caret, SyntaxError)
        self.assertTrue(len(err) == 3)
        self.assertTrue(err[1].strip() == '[x for x in x] = x')

    def test_bad_indentation(self):
        err = self.get_exception_format(self.syntax_error_bad_indentation, IndentationError)
        self.assertTrue(len(err) == 4)
        self.assertTrue(err[1].strip() == 'print 2')
        self.assertIn('^', err[2])
        self.assertTrue(err[1].find('2') == err[2].find('^'))

    def test_bug737473(self):
        import os, tempfile, time
        savedpath = sys.path[:]
        testdir = tempfile.mkdtemp()
        try:
            sys.path.insert(0, testdir)
            testfile = os.path.join(testdir, 'test_bug737473.py')
            print >> open(testfile, 'w'), '\ndef test():\n    raise ValueError'
            if 'test_bug737473' in sys.modules:
                del sys.modules['test_bug737473']
            import test_bug737473
            try:
                test_bug737473.test()
            except ValueError:
                traceback.extract_tb(sys.exc_traceback)

            time.sleep(4)
            print >> open(testfile, 'w'), '\ndef test():\n    raise NotImplementedError'
            reload(test_bug737473)
            try:
                test_bug737473.test()
            except NotImplementedError:
                src = traceback.extract_tb(sys.exc_traceback)[-1][-1]
                self.assertEqual(src, 'raise NotImplementedError')

        finally:
            sys.path[:] = savedpath
            for f in os.listdir(testdir):
                os.unlink(os.path.join(testdir, f))

            os.rmdir(testdir)

    def test_base_exception(self):
        e = KeyboardInterrupt()
        lst = traceback.format_exception_only(e.__class__, e)
        self.assertEqual(lst, ['KeyboardInterrupt\n'])

    def test_string_exception1(self):
        str_type = 'String Exception'
        err = traceback.format_exception_only(str_type, None)
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0], str_type + '\n')
        return

    def test_string_exception2(self):
        str_type = 'String Exception'
        str_value = 'String Value'
        err = traceback.format_exception_only(str_type, str_value)
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0], str_type + ': ' + str_value + '\n')

    def test_format_exception_only_bad__str__(self):

        class X(Exception):

            def __str__(self):
                1 // 0

        err = traceback.format_exception_only(X, X())
        self.assertEqual(len(err), 1)
        str_value = '<unprintable %s object>' % X.__name__
        self.assertEqual(err[0], X.__name__ + ': ' + str_value + '\n')

    def test_without_exception(self):
        err = traceback.format_exception_only(None, None)
        self.assertEqual(err, ['None\n'])
        return

    def test_unicode(self):
        err = AssertionError('\xff')
        lines = traceback.format_exception_only(type(err), err)
        self.assertEqual(lines, ['AssertionError: \xff\n'])
        err = AssertionError(u'\xe9')
        lines = traceback.format_exception_only(type(err), err)
        self.assertEqual(lines, ['AssertionError: \\xe9\n'])


class TracebackFormatTests(unittest.TestCase):

    def test_traceback_format(self):
        try:
            raise KeyError('blah')
        except KeyError:
            type_, value, tb = sys.exc_info()
            traceback_fmt = 'Traceback (most recent call last):\n' + ''.join(traceback.format_tb(tb))
            file_ = StringIO()
            traceback_print(tb, file_)
            python_fmt = file_.getvalue()
        else:
            raise Error('unable to create test traceback string')

        self.assertEqual(traceback_fmt, python_fmt)
        tb_lines = python_fmt.splitlines()
        self.assertEqual(len(tb_lines), 3)
        banner, location, source_line = tb_lines
        self.assertTrue(banner.startswith('Traceback'))
        self.assertTrue(location.startswith('  File'))
        self.assertTrue(source_line.startswith('    raise'))


def test_main():
    run_unittest(TracebackCases, TracebackFormatTests)


if __name__ == '__main__':
    test_main()