# Embedded file name: scripts/common/Lib/test/test_re.py
from test.test_support import verbose, run_unittest, import_module
import re
from re import Scanner
import sys
import string
import traceback
from weakref import proxy
import unittest

class ReTests(unittest.TestCase):

    def test_weakref(self):
        s = 'QabbbcR'
        x = re.compile('ab+c')
        y = proxy(x)
        self.assertEqual(x.findall('QabbbcR'), y.findall('QabbbcR'))

    def test_search_star_plus(self):
        self.assertEqual(re.search('x*', 'axx').span(0), (0, 0))
        self.assertEqual(re.search('x*', 'axx').span(), (0, 0))
        self.assertEqual(re.search('x+', 'axx').span(0), (1, 3))
        self.assertEqual(re.search('x+', 'axx').span(), (1, 3))
        self.assertEqual(re.search('x', 'aaa'), None)
        self.assertEqual(re.match('a*', 'xxx').span(0), (0, 0))
        self.assertEqual(re.match('a*', 'xxx').span(), (0, 0))
        self.assertEqual(re.match('x*', 'xxxa').span(0), (0, 3))
        self.assertEqual(re.match('x*', 'xxxa').span(), (0, 3))
        self.assertEqual(re.match('a+', 'xxx'), None)
        return

    def bump_num(self, matchobj):
        int_value = int(matchobj.group(0))
        return str(int_value + 1)

    def test_basic_re_sub(self):
        self.assertEqual(re.sub('(?i)b+', 'x', 'bbbb BBBB'), 'x x')
        self.assertEqual(re.sub('\\d+', self.bump_num, '08.2 -2 23x99y'), '9.3 -3 24x100y')
        self.assertEqual(re.sub('\\d+', self.bump_num, '08.2 -2 23x99y', 3), '9.3 -3 23x99y')
        self.assertEqual(re.sub('.', lambda m: '\\n', 'x'), '\\n')
        self.assertEqual(re.sub('.', '\\n', 'x'), '\n')
        s = '\\1\\1'
        self.assertEqual(re.sub('(.)', s, 'x'), 'xx')
        self.assertEqual(re.sub('(.)', re.escape(s), 'x'), s)
        self.assertEqual(re.sub('(.)', lambda m: s, 'x'), s)
        self.assertEqual(re.sub('(?P<a>x)', '\\g<a>\\g<a>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<a>x)', '\\g<a>\\g<1>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<unk>x)', '\\g<unk>\\g<unk>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<unk>x)', '\\g<1>\\g<1>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('a', '\\t\\n\\v\\r\\f\\a\\b\\B\\Z\\a\\A\\w\\W\\s\\S\\d\\D', 'a'), '\t\n\x0b\r\x0c\x07\x08\\B\\Z\x07\\A\\w\\W\\s\\S\\d\\D')
        self.assertEqual(re.sub('a', '\t\n\x0b\r\x0c\x07', 'a'), '\t\n\x0b\r\x0c\x07')
        self.assertEqual(re.sub('a', '\t\n\x0b\r\x0c\x07', 'a'), chr(9) + chr(10) + chr(11) + chr(13) + chr(12) + chr(7))
        self.assertEqual(re.sub('^\\s*', 'X', 'test'), 'Xtest')

    def test_bug_449964(self):
        self.assertEqual(re.sub('(?P<unk>x)', '\\g<1>\\g<1>\\b', 'xx'), 'xx\x08xx\x08')

    def test_bug_449000(self):
        self.assertEqual(re.sub('\\r\\n', '\\n', 'abc\r\ndef\r\n'), 'abc\ndef\n')
        self.assertEqual(re.sub('\r\n', '\\n', 'abc\r\ndef\r\n'), 'abc\ndef\n')
        self.assertEqual(re.sub('\\r\\n', '\n', 'abc\r\ndef\r\n'), 'abc\ndef\n')
        self.assertEqual(re.sub('\r\n', '\n', 'abc\r\ndef\r\n'), 'abc\ndef\n')

    def test_bug_1140(self):
        for x in ('x', u'x'):
            for y in ('y', u'y'):
                z = re.sub(x, y, u'')
                self.assertEqual(z, u'')
                self.assertEqual(type(z), unicode)
                z = re.sub(x, y, '')
                self.assertEqual(z, '')
                self.assertEqual(type(z), str)
                z = re.sub(x, y, unicode(x))
                self.assertEqual(z, y)
                self.assertEqual(type(z), unicode)
                z = re.sub(x, y, str(x))
                self.assertEqual(z, y)
                self.assertEqual(type(z), type(y))

    def test_bug_1661(self):
        pattern = re.compile('.')
        self.assertRaises(ValueError, re.match, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.search, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.findall, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.compile, pattern, re.I)

    def test_bug_3629(self):
        re.compile('(?P<quote>)(?(quote))')

    def test_sub_template_numeric_escape(self):
        self.assertEqual(re.sub('x', '\\0', 'x'), '\x00')
        self.assertEqual(re.sub('x', '\\000', 'x'), '\x00')
        self.assertEqual(re.sub('x', '\\001', 'x'), '\x01')
        self.assertEqual(re.sub('x', '\\008', 'x'), '\x008')
        self.assertEqual(re.sub('x', '\\009', 'x'), '\x009')
        self.assertEqual(re.sub('x', '\\111', 'x'), 'I')
        self.assertEqual(re.sub('x', '\\117', 'x'), 'O')
        self.assertEqual(re.sub('x', '\\1111', 'x'), 'I1')
        self.assertEqual(re.sub('x', '\\1111', 'x'), 'I1')
        self.assertEqual(re.sub('x', '\\00', 'x'), '\x00')
        self.assertEqual(re.sub('x', '\\07', 'x'), '\x07')
        self.assertEqual(re.sub('x', '\\08', 'x'), '\x008')
        self.assertEqual(re.sub('x', '\\09', 'x'), '\x009')
        self.assertEqual(re.sub('x', '\\0a', 'x'), '\x00a')
        self.assertEqual(re.sub('x', '\\400', 'x'), '\x00')
        self.assertEqual(re.sub('x', '\\777', 'x'), '\xff')
        self.assertRaises(re.error, re.sub, 'x', '\\1', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\8', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\9', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\11', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\18', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\1a', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\90', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\99', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\118', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\11a', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\181', 'x')
        self.assertRaises(re.error, re.sub, 'x', '\\800', 'x')
        self.assertEqual(re.sub('(((((((((((x)))))))))))', '\\11', 'x'), 'x')
        self.assertEqual(re.sub('((((((((((y))))))))))(.)', '\\118', 'xyz'), 'xz8')
        self.assertEqual(re.sub('((((((((((y))))))))))(.)', '\\11a', 'xyz'), 'xza')

    def test_qualified_re_sub(self):
        self.assertEqual(re.sub('a', 'b', 'aaaaa'), 'bbbbb')
        self.assertEqual(re.sub('a', 'b', 'aaaaa', 1), 'baaaa')

    def test_bug_114660(self):
        self.assertEqual(re.sub('(\\S)\\s+(\\S)', '\\1 \\2', 'hello  there'), 'hello there')

    def test_bug_462270(self):
        self.assertEqual(re.sub('x*', '-', 'abxd'), '-a-b-d-')
        self.assertEqual(re.sub('x+', '-', 'abxd'), 'ab-d')

    def test_symbolic_refs(self):
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g<a', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g<', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g<a a>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g<1a1>', 'xx')
        self.assertRaises(IndexError, re.sub, '(?P<a>x)', '\\g<ab>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)|(?P<b>y)', '\\g<b>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)|(?P<b>y)', '\\2', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\\g<-1>', 'xx')

    def test_re_subn(self):
        self.assertEqual(re.subn('(?i)b+', 'x', 'bbbb BBBB'), ('x x', 2))
        self.assertEqual(re.subn('b+', 'x', 'bbbb BBBB'), ('x BBBB', 1))
        self.assertEqual(re.subn('b+', 'x', 'xyz'), ('xyz', 0))
        self.assertEqual(re.subn('b*', 'x', 'xyz'), ('xxxyxzx', 4))
        self.assertEqual(re.subn('b*', 'x', 'xyz', 2), ('xxxyz', 2))

    def test_re_split(self):
        self.assertEqual(re.split(':', ':a:b::c'), ['',
         'a',
         'b',
         '',
         'c'])
        self.assertEqual(re.split(':*', ':a:b::c'), ['',
         'a',
         'b',
         'c'])
        self.assertEqual(re.split('(:*)', ':a:b::c'), ['',
         ':',
         'a',
         ':',
         'b',
         '::',
         'c'])
        self.assertEqual(re.split('(?::*)', ':a:b::c'), ['',
         'a',
         'b',
         'c'])
        self.assertEqual(re.split('(:)*', ':a:b::c'), ['',
         ':',
         'a',
         ':',
         'b',
         ':',
         'c'])
        self.assertEqual(re.split('([b:]+)', ':a:b::c'), ['',
         ':',
         'a',
         ':b::',
         'c'])
        self.assertEqual(re.split('(b)|(:+)', ':a:b::c'), ['',
         None,
         ':',
         'a',
         None,
         ':',
         '',
         'b',
         None,
         '',
         None,
         '::',
         'c'])
        self.assertEqual(re.split('(?:b)|(?::+)', ':a:b::c'), ['',
         'a',
         '',
         '',
         'c'])
        return

    def test_qualified_re_split(self):
        self.assertEqual(re.split(':', ':a:b::c', 2), ['', 'a', 'b::c'])
        self.assertEqual(re.split(':', 'a:b:c:d', 2), ['a', 'b', 'c:d'])
        self.assertEqual(re.split('(:)', ':a:b::c', 2), ['',
         ':',
         'a',
         ':',
         'b::c'])
        self.assertEqual(re.split('(:*)', ':a:b::c', 2), ['',
         ':',
         'a',
         ':',
         'b::c'])

    def test_re_findall(self):
        self.assertEqual(re.findall(':+', 'abc'), [])
        self.assertEqual(re.findall(':+', 'a:b::c:::d'), [':', '::', ':::'])
        self.assertEqual(re.findall('(:+)', 'a:b::c:::d'), [':', '::', ':::'])
        self.assertEqual(re.findall('(:)(:*)', 'a:b::c:::d'), [(':', ''), (':', ':'), (':', '::')])

    def test_bug_117612(self):
        self.assertEqual(re.findall('(a|(b))', 'aba'), [('a', ''), ('b', 'b'), ('a', '')])

    def test_re_match(self):
        self.assertEqual(re.match('a', 'a').groups(), ())
        self.assertEqual(re.match('(a)', 'a').groups(), ('a',))
        self.assertEqual(re.match('(a)', 'a').group(0), 'a')
        self.assertEqual(re.match('(a)', 'a').group(1), 'a')
        self.assertEqual(re.match('(a)', 'a').group(1, 1), ('a', 'a'))
        pat = re.compile('((a)|(b))(c)?')
        self.assertEqual(pat.match('a').groups(), ('a', 'a', None, None))
        self.assertEqual(pat.match('b').groups(), ('b', None, 'b', None))
        self.assertEqual(pat.match('ac').groups(), ('a', 'a', None, 'c'))
        self.assertEqual(pat.match('bc').groups(), ('b', None, 'b', 'c'))
        self.assertEqual(pat.match('bc').groups(''), ('b', '', 'b', 'c'))
        m = re.match('(a)', 'a')
        self.assertEqual(m.group(0), 'a')
        self.assertEqual(m.group(0), 'a')
        self.assertEqual(m.group(1), 'a')
        self.assertEqual(m.group(1, 1), ('a', 'a'))
        pat = re.compile('(?:(?P<a1>a)|(?P<b2>b))(?P<c3>c)?')
        self.assertEqual(pat.match('a').group(1, 2, 3), ('a', None, None))
        self.assertEqual(pat.match('b').group('a1', 'b2', 'c3'), (None, 'b', None))
        self.assertEqual(pat.match('ac').group(1, 'b2', 3), ('a', None, 'c'))
        return None

    def test_re_groupref_exists(self):
        self.assertEqual(re.match('^(\\()?([^()]+)(?(1)\\))$', '(a)').groups(), ('(', 'a'))
        self.assertEqual(re.match('^(\\()?([^()]+)(?(1)\\))$', 'a').groups(), (None, 'a'))
        self.assertEqual(re.match('^(\\()?([^()]+)(?(1)\\))$', 'a)'), None)
        self.assertEqual(re.match('^(\\()?([^()]+)(?(1)\\))$', '(a'), None)
        self.assertEqual(re.match('^(?:(a)|c)((?(1)b|d))$', 'ab').groups(), ('a', 'b'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)b|d))$', 'cd').groups(), (None, 'd'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)|d))$', 'cd').groups(), (None, 'd'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)|d))$', 'a').groups(), ('a', ''))
        p = re.compile('(?P<g1>a)(?P<g2>b)?((?(g2)c|d))')
        self.assertEqual(p.match('abc').groups(), ('a', 'b', 'c'))
        self.assertEqual(p.match('ad').groups(), ('a', None, 'd'))
        self.assertEqual(p.match('abd'), None)
        self.assertEqual(p.match('ac'), None)
        return

    def test_re_groupref(self):
        self.assertEqual(re.match('^(\\|)?([^()]+)\\1$', '|a|').groups(), ('|', 'a'))
        self.assertEqual(re.match('^(\\|)?([^()]+)\\1?$', 'a').groups(), (None, 'a'))
        self.assertEqual(re.match('^(\\|)?([^()]+)\\1$', 'a|'), None)
        self.assertEqual(re.match('^(\\|)?([^()]+)\\1$', '|a'), None)
        self.assertEqual(re.match('^(?:(a)|c)(\\1)$', 'aa').groups(), ('a', 'a'))
        self.assertEqual(re.match('^(?:(a)|c)(\\1)?$', 'c').groups(), (None, None))
        return

    def test_groupdict(self):
        self.assertEqual(re.match('(?P<first>first) (?P<second>second)', 'first second').groupdict(), {'first': 'first',
         'second': 'second'})

    def test_expand(self):
        self.assertEqual(re.match('(?P<first>first) (?P<second>second)', 'first second').expand('\\2 \\1 \\g<second> \\g<first>'), 'second first second first')

    def test_repeat_minmax(self):
        self.assertEqual(re.match('^(\\w){1}$', 'abc'), None)
        self.assertEqual(re.match('^(\\w){1}?$', 'abc'), None)
        self.assertEqual(re.match('^(\\w){1,2}$', 'abc'), None)
        self.assertEqual(re.match('^(\\w){1,2}?$', 'abc'), None)
        self.assertEqual(re.match('^(\\w){3}$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){1,3}$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){1,4}$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){3,4}?$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){3}?$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){1,3}?$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){1,4}?$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^(\\w){3,4}?$', 'abc').group(1), 'c')
        self.assertEqual(re.match('^x{1}$', 'xxx'), None)
        self.assertEqual(re.match('^x{1}?$', 'xxx'), None)
        self.assertEqual(re.match('^x{1,2}$', 'xxx'), None)
        self.assertEqual(re.match('^x{1,2}?$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{3}$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{1,3}$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{1,4}$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{3,4}?$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{3}?$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{1,3}?$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{1,4}?$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{3,4}?$', 'xxx'), None)
        self.assertEqual(re.match('^x{}$', 'xxx'), None)
        self.assertNotEqual(re.match('^x{}$', 'x{}'), None)
        return

    def test_getattr(self):
        self.assertEqual(re.match('(a)', 'a').pos, 0)
        self.assertEqual(re.match('(a)', 'a').endpos, 1)
        self.assertEqual(re.match('(a)', 'a').string, 'a')
        self.assertEqual(re.match('(a)', 'a').regs, ((0, 1), (0, 1)))
        self.assertNotEqual(re.match('(a)', 'a').re, None)
        return

    def test_special_escapes(self):
        self.assertEqual(re.search('\\b(b.)\\b', 'abcd abc bcd bx').group(1), 'bx')
        self.assertEqual(re.search('\\B(b.)\\B', 'abc bcd bc abxd').group(1), 'bx')
        self.assertEqual(re.search('\\b(b.)\\b', 'abcd abc bcd bx', re.LOCALE).group(1), 'bx')
        self.assertEqual(re.search('\\B(b.)\\B', 'abc bcd bc abxd', re.LOCALE).group(1), 'bx')
        self.assertEqual(re.search('\\b(b.)\\b', 'abcd abc bcd bx', re.UNICODE).group(1), 'bx')
        self.assertEqual(re.search('\\B(b.)\\B', 'abc bcd bc abxd', re.UNICODE).group(1), 'bx')
        self.assertEqual(re.search('^abc$', '\nabc\n', re.M).group(0), 'abc')
        self.assertEqual(re.search('^\\Aabc\\Z$', 'abc', re.M).group(0), 'abc')
        self.assertEqual(re.search('^\\Aabc\\Z$', '\nabc\n', re.M), None)
        self.assertEqual(re.search('\\b(b.)\\b', u'abcd abc bcd bx').group(1), 'bx')
        self.assertEqual(re.search('\\B(b.)\\B', u'abc bcd bc abxd').group(1), 'bx')
        self.assertEqual(re.search('^abc$', u'\nabc\n', re.M).group(0), 'abc')
        self.assertEqual(re.search('^\\Aabc\\Z$', u'abc', re.M).group(0), 'abc')
        self.assertEqual(re.search('^\\Aabc\\Z$', u'\nabc\n', re.M), None)
        self.assertEqual(re.search('\\d\\D\\w\\W\\s\\S', '1aa! a').group(0), '1aa! a')
        self.assertEqual(re.search('\\d\\D\\w\\W\\s\\S', '1aa! a', re.LOCALE).group(0), '1aa! a')
        self.assertEqual(re.search('\\d\\D\\w\\W\\s\\S', '1aa! a', re.UNICODE).group(0), '1aa! a')
        return

    def test_bigcharset(self):
        self.assertEqual(re.match(u'([\u2222\u2223])', u'\u2222').group(1), u'\u2222')
        self.assertEqual(re.match(u'([\u2222\u2223])', u'\u2222', re.UNICODE).group(1), u'\u2222')

    def test_anyall(self):
        self.assertEqual(re.match('a.b', 'a\nb', re.DOTALL).group(0), 'a\nb')
        self.assertEqual(re.match('a.*b', 'a\n\nb', re.DOTALL).group(0), 'a\n\nb')

    def test_non_consuming(self):
        self.assertEqual(re.match('(a(?=\\s[^a]))', 'a b').group(1), 'a')
        self.assertEqual(re.match('(a(?=\\s[^a]*))', 'a b').group(1), 'a')
        self.assertEqual(re.match('(a(?=\\s[abc]))', 'a b').group(1), 'a')
        self.assertEqual(re.match('(a(?=\\s[abc]*))', 'a bc').group(1), 'a')
        self.assertEqual(re.match('(a)(?=\\s\\1)', 'a a').group(1), 'a')
        self.assertEqual(re.match('(a)(?=\\s\\1*)', 'a aa').group(1), 'a')
        self.assertEqual(re.match('(a)(?=\\s(abc|a))', 'a a').group(1), 'a')
        self.assertEqual(re.match('(a(?!\\s[^a]))', 'a a').group(1), 'a')
        self.assertEqual(re.match('(a(?!\\s[abc]))', 'a d').group(1), 'a')
        self.assertEqual(re.match('(a)(?!\\s\\1)', 'a b').group(1), 'a')
        self.assertEqual(re.match('(a)(?!\\s(abc|a))', 'a b').group(1), 'a')

    def test_ignore_case(self):
        self.assertEqual(re.match('abc', 'ABC', re.I).group(0), 'ABC')
        self.assertEqual(re.match('abc', u'ABC', re.I).group(0), 'ABC')
        self.assertEqual(re.match('(a\\s[^a])', 'a b', re.I).group(1), 'a b')
        self.assertEqual(re.match('(a\\s[^a]*)', 'a bb', re.I).group(1), 'a bb')
        self.assertEqual(re.match('(a\\s[abc])', 'a b', re.I).group(1), 'a b')
        self.assertEqual(re.match('(a\\s[abc]*)', 'a bb', re.I).group(1), 'a bb')
        self.assertEqual(re.match('((a)\\s\\2)', 'a a', re.I).group(1), 'a a')
        self.assertEqual(re.match('((a)\\s\\2*)', 'a aa', re.I).group(1), 'a aa')
        self.assertEqual(re.match('((a)\\s(abc|a))', 'a a', re.I).group(1), 'a a')
        self.assertEqual(re.match('((a)\\s(abc|a)*)', 'a aa', re.I).group(1), 'a aa')

    def test_category(self):
        self.assertEqual(re.match('(\\s)', ' ').group(1), ' ')

    def test_getlower(self):
        import _sre
        self.assertEqual(_sre.getlower(ord('A'), 0), ord('a'))
        self.assertEqual(_sre.getlower(ord('A'), re.LOCALE), ord('a'))
        self.assertEqual(_sre.getlower(ord('A'), re.UNICODE), ord('a'))
        self.assertEqual(re.match('abc', 'ABC', re.I).group(0), 'ABC')
        self.assertEqual(re.match('abc', u'ABC', re.I).group(0), 'ABC')

    def test_not_literal(self):
        self.assertEqual(re.search('\\s([^a])', ' b').group(1), 'b')
        self.assertEqual(re.search('\\s([^a]*)', ' bb').group(1), 'bb')

    def test_search_coverage(self):
        self.assertEqual(re.search('\\s(b)', ' b').group(1), 'b')
        self.assertEqual(re.search('a\\s', 'a ').group(0), 'a ')

    def assertMatch(self, pattern, text, match = None, span = None, matcher = re.match):
        if match is None and span is None:
            match = text
            span = (0, len(text))
        elif match is None or span is None:
            raise ValueError('If match is not None, span should be specified (and vice versa).')
        m = matcher(pattern, text)
        self.assertTrue(m)
        self.assertEqual(m.group(), match)
        self.assertEqual(m.span(), span)
        return

    def test_re_escape(self):
        alnum_chars = string.ascii_letters + string.digits
        p = u''.join((unichr(i) for i in range(256)))
        for c in p:
            if c in alnum_chars:
                self.assertEqual(re.escape(c), c)
            elif c == u'\x00':
                self.assertEqual(re.escape(c), u'\\000')
            else:
                self.assertEqual(re.escape(c), u'\\' + c)
            self.assertMatch(re.escape(c), c)

        self.assertMatch(re.escape(p), p)

    def test_re_escape_byte(self):
        alnum_chars = (string.ascii_letters + string.digits).encode('ascii')
        p = ''.join((chr(i) for i in range(256)))
        for b in p:
            if b in alnum_chars:
                self.assertEqual(re.escape(b), b)
            elif b == '\x00':
                self.assertEqual(re.escape(b), '\\000')
            else:
                self.assertEqual(re.escape(b), '\\' + b)
            self.assertMatch(re.escape(b), b)

        self.assertMatch(re.escape(p), p)

    def test_re_escape_non_ascii(self):
        s = u'xxx\u2620\u2620\u2620xxx'
        s_escaped = re.escape(s)
        self.assertEqual(s_escaped, u'xxx\\\u2620\\\u2620\\\u2620xxx')
        self.assertMatch(s_escaped, s)
        self.assertMatch(u'.%s+.' % re.escape(u'\u2620'), s, u'x\u2620\u2620\u2620x', (2, 7), re.search)

    def test_re_escape_non_ascii_bytes(self):
        b = u'y\u2620y\u2620y'.encode('utf-8')
        b_escaped = re.escape(b)
        self.assertEqual(b_escaped, 'y\\\xe2\\\x98\\\xa0y\\\xe2\\\x98\\\xa0y')
        self.assertMatch(b_escaped, b)
        res = re.findall(re.escape(u'\u2620'.encode('utf-8')), b)
        self.assertEqual(len(res), 2)

    def test_pickling(self):
        import pickle
        self.pickle_test(pickle)
        import cPickle
        self.pickle_test(cPickle)
        import_module('sre', deprecated=True)
        from sre import _compile

    def pickle_test(self, pickle):
        oldpat = re.compile('a(?:b|(c|e){1,2}?|d)+?(.)')
        s = pickle.dumps(oldpat)
        newpat = pickle.loads(s)
        self.assertEqual(oldpat, newpat)

    def test_constants(self):
        self.assertEqual(re.I, re.IGNORECASE)
        self.assertEqual(re.L, re.LOCALE)
        self.assertEqual(re.M, re.MULTILINE)
        self.assertEqual(re.S, re.DOTALL)
        self.assertEqual(re.X, re.VERBOSE)

    def test_flags(self):
        for flag in [re.I,
         re.M,
         re.X,
         re.S,
         re.L]:
            self.assertNotEqual(re.compile('^pattern$', flag), None)

        return

    def test_sre_character_literals(self):
        for i in [0,
         8,
         16,
         32,
         64,
         127,
         128,
         255]:
            self.assertNotEqual(re.match('\\%03o' % i, chr(i)), None)
            self.assertNotEqual(re.match('\\%03o0' % i, chr(i) + '0'), None)
            self.assertNotEqual(re.match('\\%03o8' % i, chr(i) + '8'), None)
            self.assertNotEqual(re.match('\\x%02x' % i, chr(i)), None)
            self.assertNotEqual(re.match('\\x%02x0' % i, chr(i) + '0'), None)
            self.assertNotEqual(re.match('\\x%02xz' % i, chr(i) + 'z'), None)

        self.assertRaises(re.error, re.match, '\\911', '')
        return

    def test_sre_character_class_literals(self):
        for i in [0,
         8,
         16,
         32,
         64,
         127,
         128,
         255]:
            self.assertNotEqual(re.match('[\\%03o]' % i, chr(i)), None)
            self.assertNotEqual(re.match('[\\%03o0]' % i, chr(i)), None)
            self.assertNotEqual(re.match('[\\%03o8]' % i, chr(i)), None)
            self.assertNotEqual(re.match('[\\x%02x]' % i, chr(i)), None)
            self.assertNotEqual(re.match('[\\x%02x0]' % i, chr(i)), None)
            self.assertNotEqual(re.match('[\\x%02xz]' % i, chr(i)), None)

        self.assertRaises(re.error, re.match, '[\\911]', '')
        return

    def test_bug_113254(self):
        self.assertEqual(re.match('(a)|(b)', 'b').start(1), -1)
        self.assertEqual(re.match('(a)|(b)', 'b').end(1), -1)
        self.assertEqual(re.match('(a)|(b)', 'b').span(1), (-1, -1))

    def test_bug_527371(self):
        self.assertEqual(re.match('(a)?a', 'a').lastindex, None)
        self.assertEqual(re.match('(a)(b)?b', 'ab').lastindex, 1)
        self.assertEqual(re.match('(?P<a>a)(?P<b>b)?b', 'ab').lastgroup, 'a')
        self.assertEqual(re.match('(?P<a>a(b))', 'ab').lastgroup, 'a')
        self.assertEqual(re.match('((a))', 'a').lastindex, 1)
        return

    def test_bug_545855(self):
        self.assertRaises(re.error, re.compile, 'foo[a-')

    def test_bug_418626(self):
        self.assertEqual(re.match('.*?c', 10000 * 'ab' + 'cd').end(0), 20001)
        self.assertEqual(re.match('.*?cd', 5000 * 'ab' + 'c' + 5000 * 'ab' + 'cde').end(0), 20003)
        self.assertEqual(re.match('.*?cd', 20000 * 'abc' + 'de').end(0), 60001)
        self.assertEqual(re.search('(a|b)*?c', 10000 * 'ab' + 'cd').end(0), 20001)

    def test_bug_612074(self):
        pat = u'[' + re.escape(u'\u2039') + u']'
        self.assertEqual(re.compile(pat) and 1, 1)

    def test_stack_overflow(self):
        self.assertEqual(re.match('(x)*', 50000 * 'x').group(1), 'x')
        self.assertEqual(re.match('(x)*y', 50000 * 'x' + 'y').group(1), 'x')
        self.assertEqual(re.match('(x)*?y', 50000 * 'x' + 'y').group(1), 'x')

    def test_scanner(self):

        def s_ident(scanner, token):
            return token

        def s_operator(scanner, token):
            return 'op%s' % token

        def s_float(scanner, token):
            return float(token)

        def s_int(scanner, token):
            return int(token)

        scanner = Scanner([('[a-zA-Z_]\\w*', s_ident),
         ('\\d+\\.\\d*', s_float),
         ('\\d+', s_int),
         ('=|\\+|-|\\*|/', s_operator),
         ('\\s+', None)])
        self.assertNotEqual(scanner.scanner.scanner('').pattern, None)
        self.assertEqual(scanner.scan('sum = 3*foo + 312.50 + bar'), (['sum',
          'op=',
          3,
          'op*',
          'foo',
          'op+',
          312.5,
          'op+',
          'bar'], ''))
        return

    def test_bug_448951(self):
        for op in ('', '?', '*'):
            self.assertEqual(re.match('((.%s):)?z' % op, 'z').groups(), (None, None))
            self.assertEqual(re.match('((.%s):)?z' % op, 'a:z').groups(), ('a:', 'a'))

        return None

    def test_bug_725106(self):
        self.assertEqual(re.match('^((a)|b)*', 'abc').groups(), ('b', 'a'))
        self.assertEqual(re.match('^(([ab])|c)*', 'abc').groups(), ('c', 'b'))
        self.assertEqual(re.match('^((d)|[ab])*', 'abc').groups(), ('b', None))
        self.assertEqual(re.match('^((a)c|[ab])*', 'abc').groups(), ('b', None))
        self.assertEqual(re.match('^((a)|b)*?c', 'abc').groups(), ('b', 'a'))
        self.assertEqual(re.match('^(([ab])|c)*?d', 'abcd').groups(), ('c', 'b'))
        self.assertEqual(re.match('^((d)|[ab])*?c', 'abc').groups(), ('b', None))
        self.assertEqual(re.match('^((a)c|[ab])*?c', 'abc').groups(), ('b', None))
        return None

    def test_bug_725149(self):
        self.assertEqual(re.match('(a)(?:(?=(b)*)c)*', 'abb').groups(), ('a', None))
        self.assertEqual(re.match('(a)((?!(b)*))*', 'abb').groups(), ('a', None, None))
        return None

    def test_bug_764548(self):
        try:
            unicode
        except NameError:
            return

        class my_unicode(unicode):
            pass

        pat = re.compile(my_unicode('abc'))
        self.assertEqual(pat.match('xyz'), None)
        return

    def test_finditer(self):
        iter = re.finditer(':+', 'a:b::c:::d')
        self.assertEqual([ item.group(0) for item in iter ], [':', '::', ':::'])

    def test_bug_926075(self):
        try:
            unicode
        except NameError:
            return

        self.assertTrue(re.compile('bug_926075') is not re.compile(eval("u'bug_926075'")))

    def test_bug_931848(self):
        try:
            unicode
        except NameError:
            pass

        pattern = eval('u"[\\u002E\\u3002\\uFF0E\\uFF61]"')
        self.assertEqual(re.compile(pattern).split('a.b.c'), ['a', 'b', 'c'])

    def test_bug_581080(self):
        iter = re.finditer('\\s', 'a b')
        self.assertEqual(iter.next().span(), (1, 2))
        self.assertRaises(StopIteration, iter.next)
        scanner = re.compile('\\s').scanner('a b')
        self.assertEqual(scanner.search().span(), (1, 2))
        self.assertEqual(scanner.search(), None)
        return

    def test_bug_817234(self):
        iter = re.finditer('.*', 'asdf')
        self.assertEqual(iter.next().span(), (0, 4))
        self.assertEqual(iter.next().span(), (4, 4))
        self.assertRaises(StopIteration, iter.next)

    def test_bug_6561(self):
        decimal_digits = [u'7', u'\u0e58', u'\uff10']
        for x in decimal_digits:
            self.assertEqual(re.match('^\\d$', x, re.UNICODE).group(0), x)

        not_decimal_digits = [u'\u2165',
         u'\u3039',
         u'\u2082',
         u'\u32b4']
        for x in not_decimal_digits:
            self.assertIsNone(re.match('^\\d$', x, re.UNICODE))

    def test_empty_array(self):
        import array
        for typecode in 'cbBuhHiIlLfd':
            a = array.array(typecode)
            self.assertEqual(re.compile('bla').match(a), None)
            self.assertEqual(re.compile('').match(a).groups(), ())

        return

    def test_inline_flags(self):
        upper_char = unichr(7840)
        lower_char = unichr(7841)
        p = re.compile(upper_char, re.I | re.U)
        q = p.match(lower_char)
        self.assertNotEqual(q, None)
        p = re.compile(lower_char, re.I | re.U)
        q = p.match(upper_char)
        self.assertNotEqual(q, None)
        p = re.compile('(?i)' + upper_char, re.U)
        q = p.match(lower_char)
        self.assertNotEqual(q, None)
        p = re.compile('(?i)' + lower_char, re.U)
        q = p.match(upper_char)
        self.assertNotEqual(q, None)
        p = re.compile('(?iu)' + upper_char)
        q = p.match(lower_char)
        self.assertNotEqual(q, None)
        p = re.compile('(?iu)' + lower_char)
        q = p.match(upper_char)
        self.assertNotEqual(q, None)
        return

    def test_dollar_matches_twice(self):
        """$ matches the end of string, and just before the terminating 
        """
        pattern = re.compile('$')
        self.assertEqual(pattern.sub('#', 'a\nb\n'), 'a\nb#\n#')
        self.assertEqual(pattern.sub('#', 'a\nb\nc'), 'a\nb\nc#')
        self.assertEqual(pattern.sub('#', '\n'), '#\n#')
        pattern = re.compile('$', re.MULTILINE)
        self.assertEqual(pattern.sub('#', 'a\nb\n'), 'a#\nb#\n#')
        self.assertEqual(pattern.sub('#', 'a\nb\nc'), 'a#\nb#\nc#')
        self.assertEqual(pattern.sub('#', '\n'), '#\n#')

    def test_dealloc(self):
        import _sre
        long_overflow = 340282366920938463463374607431768211456L
        self.assertRaises(TypeError, re.finditer, 'a', {})
        self.assertRaises(OverflowError, _sre.compile, 'abc', 0, [long_overflow])


def run_re_tests():
    from test.re_tests import tests, SUCCEED, FAIL, SYNTAX_ERROR
    if verbose:
        print 'Running re_tests test suite'
    for t in tests:
        sys.stdout.flush()
        pattern = s = outcome = repl = expected = None
        if len(t) == 5:
            pattern, s, outcome, repl, expected = t
        elif len(t) == 3:
            pattern, s, outcome = t
        else:
            raise ValueError, ('Test tuples should have 3 or 5 fields', t)
        try:
            obj = re.compile(pattern)
        except re.error:
            if outcome == SYNTAX_ERROR:
                pass
            else:
                print '=== Syntax error:', t
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print '*** Unexpected error ***', t
            if verbose:
                traceback.print_exc(file=sys.stdout)
        else:
            try:
                result = obj.search(s)
            except re.error as msg:
                print '=== Unexpected exception', t, repr(msg)

            if outcome == SYNTAX_ERROR:
                pass
            elif outcome == FAIL:
                if result is None:
                    pass
                else:
                    print '=== Succeeded incorrectly', t
            elif outcome == SUCCEED:
                if result is not None:
                    start, end = result.span(0)
                    vardict = {'found': result.group(0),
                     'groups': result.group(),
                     'flags': result.re.flags}
                    for i in range(1, 100):
                        try:
                            gi = result.group(i)
                            if gi is None:
                                gi = 'None'
                        except IndexError:
                            gi = 'Error'

                        vardict['g%d' % i] = gi

                    for i in result.re.groupindex.keys():
                        try:
                            gi = result.group(i)
                            if gi is None:
                                gi = 'None'
                        except IndexError:
                            gi = 'Error'

                        vardict[i] = gi

                    repl = eval(repl, vardict)
                    if repl != expected:
                        print '=== grouping error', t,
                        print repr(repl) + ' should be ' + repr(expected)
                else:
                    print '=== Failed incorrectly', t
                try:
                    result = obj.search(unicode(s, 'latin-1'))
                    if result is None:
                        print '=== Fails on unicode match', t
                except NameError:
                    continue
                except TypeError:
                    continue

                obj = re.compile(unicode(pattern, 'latin-1'))
                result = obj.search(s)
                if result is None:
                    print '=== Fails on unicode pattern match', t
                if pattern[:2] != '\\B' and pattern[-2:] != '\\B' and result is not None:
                    obj = re.compile(pattern)
                    result = obj.search(s, result.start(0), result.end(0) + 1)
                    if result is None:
                        print '=== Failed on range-limited match', t
                obj = re.compile(pattern, re.IGNORECASE)
                result = obj.search(s)
                if result is None:
                    print '=== Fails on case-insensitive match', t
                obj = re.compile(pattern, re.LOCALE)
                result = obj.search(s)
                if result is None:
                    print '=== Fails on locale-sensitive match', t
                obj = re.compile(pattern, re.UNICODE)
                result = obj.search(s)
                if result is None:
                    print '=== Fails on unicode-sensitive match', t

    return


def test_main():
    run_unittest(ReTests)
    run_re_tests()


if __name__ == '__main__':
    test_main()