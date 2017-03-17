# Embedded file name: scripts/common/Lib/test/test_shlex.py
import unittest
import shlex
from test import test_support
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

data = 'x|x|\nfoo bar|foo|bar|\n foo bar|foo|bar|\n foo bar |foo|bar|\nfoo   bar    bla     fasel|foo|bar|bla|fasel|\nx y  z              xxxx|x|y|z|xxxx|\n\\x bar|\\|x|bar|\n\\ x bar|\\|x|bar|\n\\ bar|\\|bar|\nfoo \\x bar|foo|\\|x|bar|\nfoo \\ x bar|foo|\\|x|bar|\nfoo \\ bar|foo|\\|bar|\nfoo "bar" bla|foo|"bar"|bla|\n"foo" "bar" "bla"|"foo"|"bar"|"bla"|\n"foo" bar "bla"|"foo"|bar|"bla"|\n"foo" bar bla|"foo"|bar|bla|\nfoo \'bar\' bla|foo|\'bar\'|bla|\n\'foo\' \'bar\' \'bla\'|\'foo\'|\'bar\'|\'bla\'|\n\'foo\' bar \'bla\'|\'foo\'|bar|\'bla\'|\n\'foo\' bar bla|\'foo\'|bar|bla|\nblurb foo"bar"bar"fasel" baz|blurb|foo"bar"bar"fasel"|baz|\nblurb foo\'bar\'bar\'fasel\' baz|blurb|foo\'bar\'bar\'fasel\'|baz|\n""|""|\n\'\'|\'\'|\nfoo "" bar|foo|""|bar|\nfoo \'\' bar|foo|\'\'|bar|\nfoo "" "" "" bar|foo|""|""|""|bar|\nfoo \'\' \'\' \'\' bar|foo|\'\'|\'\'|\'\'|bar|\n\\""|\\|""|\n"\\"|"\\"|\n"foo\\ bar"|"foo\\ bar"|\n"foo\\\\ bar"|"foo\\\\ bar"|\n"foo\\\\ bar\\"|"foo\\\\ bar\\"|\n"foo\\\\" bar\\""|"foo\\\\"|bar|\\|""|\n"foo\\\\ bar\\" dfadf"|"foo\\\\ bar\\"|dfadf"|\n"foo\\\\\\ bar\\" dfadf"|"foo\\\\\\ bar\\"|dfadf"|\n"foo\\\\\\x bar\\" dfadf"|"foo\\\\\\x bar\\"|dfadf"|\n"foo\\x bar\\" dfadf"|"foo\\x bar\\"|dfadf"|\n\\\'\'|\\|\'\'|\n\'foo\\ bar\'|\'foo\\ bar\'|\n\'foo\\\\ bar\'|\'foo\\\\ bar\'|\n"foo\\\\\\x bar\\" df\'a\\ \'df\'|"foo\\\\\\x bar\\"|df\'a|\\|\'df\'|\n\\"foo"|\\|"foo"|\n\\"foo"\\x|\\|"foo"|\\|x|\n"foo\\x"|"foo\\x"|\n"foo\\ "|"foo\\ "|\nfoo\\ xx|foo|\\|xx|\nfoo\\ x\\x|foo|\\|x|\\|x|\nfoo\\ x\\x\\""|foo|\\|x|\\|x|\\|""|\n"foo\\ x\\x"|"foo\\ x\\x"|\n"foo\\ x\\x\\\\"|"foo\\ x\\x\\\\"|\n"foo\\ x\\x\\\\""foobar"|"foo\\ x\\x\\\\"|"foobar"|\n"foo\\ x\\x\\\\"\\\'\'"foobar"|"foo\\ x\\x\\\\"|\\|\'\'|"foobar"|\n"foo\\ x\\x\\\\"\\\'"fo\'obar"|"foo\\ x\\x\\\\"|\\|\'"fo\'|obar"|\n"foo\\ x\\x\\\\"\\\'"fo\'obar" \'don\'\\\'\'t\'|"foo\\ x\\x\\\\"|\\|\'"fo\'|obar"|\'don\'|\\|\'\'|t\'|\n\'foo\\ bar\'|\'foo\\ bar\'|\n\'foo\\\\ bar\'|\'foo\\\\ bar\'|\nfoo\\ bar|foo|\\|bar|\nfoo#bar\\nbaz|foobaz|\n:-) ;-)|:|-|)|;|-|)|\n\xe1\xe9\xed\xf3\xfa|\xe1|\xe9|\xed|\xf3|\xfa|\n'
posix_data = 'x|x|\nfoo bar|foo|bar|\n foo bar|foo|bar|\n foo bar |foo|bar|\nfoo   bar    bla     fasel|foo|bar|bla|fasel|\nx y  z              xxxx|x|y|z|xxxx|\n\\x bar|x|bar|\n\\ x bar| x|bar|\n\\ bar| bar|\nfoo \\x bar|foo|x|bar|\nfoo \\ x bar|foo| x|bar|\nfoo \\ bar|foo| bar|\nfoo "bar" bla|foo|bar|bla|\n"foo" "bar" "bla"|foo|bar|bla|\n"foo" bar "bla"|foo|bar|bla|\n"foo" bar bla|foo|bar|bla|\nfoo \'bar\' bla|foo|bar|bla|\n\'foo\' \'bar\' \'bla\'|foo|bar|bla|\n\'foo\' bar \'bla\'|foo|bar|bla|\n\'foo\' bar bla|foo|bar|bla|\nblurb foo"bar"bar"fasel" baz|blurb|foobarbarfasel|baz|\nblurb foo\'bar\'bar\'fasel\' baz|blurb|foobarbarfasel|baz|\n""||\n\'\'||\nfoo "" bar|foo||bar|\nfoo \'\' bar|foo||bar|\nfoo "" "" "" bar|foo||||bar|\nfoo \'\' \'\' \'\' bar|foo||||bar|\n\\"|"|\n"\\""|"|\n"foo\\ bar"|foo\\ bar|\n"foo\\\\ bar"|foo\\ bar|\n"foo\\\\ bar\\""|foo\\ bar"|\n"foo\\\\" bar\\"|foo\\|bar"|\n"foo\\\\ bar\\" dfadf"|foo\\ bar" dfadf|\n"foo\\\\\\ bar\\" dfadf"|foo\\\\ bar" dfadf|\n"foo\\\\\\x bar\\" dfadf"|foo\\\\x bar" dfadf|\n"foo\\x bar\\" dfadf"|foo\\x bar" dfadf|\n\\\'|\'|\n\'foo\\ bar\'|foo\\ bar|\n\'foo\\\\ bar\'|foo\\\\ bar|\n"foo\\\\\\x bar\\" df\'a\\ \'df"|foo\\\\x bar" df\'a\\ \'df|\n\\"foo|"foo|\n\\"foo\\x|"foox|\n"foo\\x"|foo\\x|\n"foo\\ "|foo\\ |\nfoo\\ xx|foo xx|\nfoo\\ x\\x|foo xx|\nfoo\\ x\\x\\"|foo xx"|\n"foo\\ x\\x"|foo\\ x\\x|\n"foo\\ x\\x\\\\"|foo\\ x\\x\\|\n"foo\\ x\\x\\\\""foobar"|foo\\ x\\x\\foobar|\n"foo\\ x\\x\\\\"\\\'"foobar"|foo\\ x\\x\\\'foobar|\n"foo\\ x\\x\\\\"\\\'"fo\'obar"|foo\\ x\\x\\\'fo\'obar|\n"foo\\ x\\x\\\\"\\\'"fo\'obar" \'don\'\\\'\'t\'|foo\\ x\\x\\\'fo\'obar|don\'t|\n"foo\\ x\\x\\\\"\\\'"fo\'obar" \'don\'\\\'\'t\' \\\\|foo\\ x\\x\\\'fo\'obar|don\'t|\\|\n\'foo\\ bar\'|foo\\ bar|\n\'foo\\\\ bar\'|foo\\\\ bar|\nfoo\\ bar|foo bar|\nfoo#bar\\nbaz|foo|baz|\n:-) ;-)|:-)|;-)|\n\xe1\xe9\xed\xf3\xfa|\xe1\xe9\xed\xf3\xfa|\n'

class ShlexTest(unittest.TestCase):

    def setUp(self):
        self.data = [ x.split('|')[:-1] for x in data.splitlines() ]
        self.posix_data = [ x.split('|')[:-1] for x in posix_data.splitlines() ]
        for item in self.data:
            item[0] = item[0].replace('\\n', '\n')

        for item in self.posix_data:
            item[0] = item[0].replace('\\n', '\n')

    def splitTest(self, data, comments):
        for i in range(len(data)):
            l = shlex.split(data[i][0], comments=comments)
            self.assertEqual(l, data[i][1:], '%s: %s != %s' % (data[i][0], l, data[i][1:]))

    def oldSplit(self, s):
        ret = []
        lex = shlex.shlex(StringIO(s))
        tok = lex.get_token()
        while tok:
            ret.append(tok)
            tok = lex.get_token()

        return ret

    def testSplitPosix(self):
        """Test data splitting with posix parser"""
        self.splitTest(self.posix_data, comments=True)

    def testCompat(self):
        """Test compatibility interface"""
        for i in range(len(self.data)):
            l = self.oldSplit(self.data[i][0])
            self.assertEqual(l, self.data[i][1:], '%s: %s != %s' % (self.data[i][0], l, self.data[i][1:]))


if not getattr(shlex, 'split', None):
    for methname in dir(ShlexTest):
        if methname.startswith('test') and methname != 'testCompat':
            delattr(ShlexTest, methname)

def test_main():
    test_support.run_unittest(ShlexTest)


if __name__ == '__main__':
    test_main()