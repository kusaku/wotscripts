# Embedded file name: scripts/common/Lib/test/test_string.py
import unittest, string
from test import test_support, string_tests
from UserList import UserList

class StringTest(string_tests.CommonTest, string_tests.MixinStrStringUserStringTest):
    type2test = str

    def checkequal(self, result, object, methodname, *args):
        realresult = getattr(string, methodname)(object, *args)
        self.assertEqual(result, realresult)

    def checkraises(self, exc, object, methodname, *args):
        self.assertRaises(exc, getattr(string, methodname), object, *args)

    def checkcall(self, object, methodname, *args):
        getattr(string, methodname)(object, *args)

    def test_join(self):
        self.checkequal('a b c d', ['a',
         'b',
         'c',
         'd'], 'join', ' ')
        self.checkequal('abcd', ('a', 'b', 'c', 'd'), 'join', '')
        self.checkequal('w x y z', string_tests.Sequence(), 'join', ' ')
        self.checkequal('abc', ('abc',), 'join', 'a')
        self.checkequal('z', UserList(['z']), 'join', 'a')
        if test_support.have_unicode:
            self.checkequal(unicode('a.b.c'), ['a', 'b', 'c'], 'join', unicode('.'))
            self.checkequal(unicode('a.b.c'), [unicode('a'), 'b', 'c'], 'join', '.')
            self.checkequal(unicode('a.b.c'), ['a', unicode('b'), 'c'], 'join', '.')
            self.checkequal(unicode('a.b.c'), ['a', 'b', unicode('c')], 'join', '.')
            self.checkraises(TypeError, ['a', unicode('b'), 3], 'join', '.')
        for i in [5, 25, 125]:
            self.checkequal((('a' * i + '-') * i)[:-1], ['a' * i] * i, 'join', '-')
            self.checkequal((('a' * i + '-') * i)[:-1], ('a' * i,) * i, 'join', '-')

        self.checkraises(TypeError, string_tests.BadSeq1(), 'join', ' ')
        self.checkequal('a b c', string_tests.BadSeq2(), 'join', ' ')
        try:

            def f():
                yield 4 + ''

            self.fixtype(' ').join(f())
        except TypeError as e:
            if '+' not in str(e):
                self.fail('join() ate exception message')
        else:
            self.fail('exception not raised')


class ModuleTest(unittest.TestCase):

    def test_attrs(self):
        string.whitespace
        string.lowercase
        string.uppercase
        string.letters
        string.digits
        string.hexdigits
        string.octdigits
        string.punctuation
        string.printable

    def test_atoi(self):
        self.assertEqual(string.atoi(' 1 '), 1)
        self.assertRaises(ValueError, string.atoi, ' 1x')
        self.assertRaises(ValueError, string.atoi, ' x1 ')

    def test_atol(self):
        self.assertEqual(string.atol('  1  '), 1L)
        self.assertRaises(ValueError, string.atol, '  1x ')
        self.assertRaises(ValueError, string.atol, '  x1 ')

    def test_atof(self):
        self.assertAlmostEqual(string.atof('  1  '), 1.0)
        self.assertRaises(ValueError, string.atof, '  1x ')
        self.assertRaises(ValueError, string.atof, '  x1 ')

    def test_maketrans(self):
        transtable = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`xyzdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
        self.assertEqual(string.maketrans('abc', 'xyz'), transtable)
        self.assertRaises(ValueError, string.maketrans, 'abc', 'xyzq')

    def test_capwords(self):
        self.assertEqual(string.capwords('abc def ghi'), 'Abc Def Ghi')
        self.assertEqual(string.capwords('abc\tdef\nghi'), 'Abc Def Ghi')
        self.assertEqual(string.capwords('abc\t   def  \nghi'), 'Abc Def Ghi')
        self.assertEqual(string.capwords('ABC DEF GHI'), 'Abc Def Ghi')
        self.assertEqual(string.capwords('ABC-DEF-GHI', '-'), 'Abc-Def-Ghi')
        self.assertEqual(string.capwords('ABC-def DEF-ghi GHI'), 'Abc-def Def-ghi Ghi')
        self.assertEqual(string.capwords('   aBc  DeF   '), 'Abc Def')
        self.assertEqual(string.capwords('\taBc\tDeF\t'), 'Abc Def')
        self.assertEqual(string.capwords('\taBc\tDeF\t', '\t'), '\tAbc\tDef\t')

    def test_formatter(self):
        fmt = string.Formatter()
        self.assertEqual(fmt.format('foo'), 'foo')
        self.assertEqual(fmt.format('foo{0}', 'bar'), 'foobar')
        self.assertEqual(fmt.format('foo{1}{0}-{1}', 'bar', 6), 'foo6bar-6')
        self.assertEqual(fmt.format('-{arg!r}-', arg='test'), "-'test'-")

        class NamespaceFormatter(string.Formatter):

            def __init__(self, namespace = {}):
                string.Formatter.__init__(self)
                self.namespace = namespace

            def get_value(self, key, args, kwds):
                if isinstance(key, str):
                    try:
                        return kwds[key]
                    except KeyError:
                        return self.namespace[key]

                else:
                    string.Formatter.get_value(key, args, kwds)

        fmt = NamespaceFormatter({'greeting': 'hello'})
        self.assertEqual(fmt.format('{greeting}, world!'), 'hello, world!')

        class CallFormatter(string.Formatter):

            def format_field(self, value, format_spec):
                return format(value(), format_spec)

        fmt = CallFormatter()
        self.assertEqual(fmt.format('*{0}*', lambda : 'result'), '*result*')

        class XFormatter(string.Formatter):

            def convert_field(self, value, conversion):
                if conversion == 'x':
                    return None
                else:
                    return super(XFormatter, self).convert_field(value, conversion)

        fmt = XFormatter()
        self.assertEqual(fmt.format('{0!r}:{0!x}', 'foo', 'foo'), "'foo':None")

        class BarFormatter(string.Formatter):

            def parse(self, format_string):
                for field in format_string.split('|'):
                    if field[0] == '+':
                        field_name, _, format_spec = field[1:].partition(':')
                        yield ('',
                         field_name,
                         format_spec,
                         None)
                    else:
                        yield (field,
                         None,
                         None,
                         None)

                return

        fmt = BarFormatter()
        self.assertEqual(fmt.format('*|+0:^10s|*', 'foo'), '*   foo    *')

        class CheckAllUsedFormatter(string.Formatter):

            def check_unused_args(self, used_args, args, kwargs):
                unused_args = set(kwargs.keys())
                unused_args.update(range(0, len(args)))
                for arg in used_args:
                    unused_args.remove(arg)

                if unused_args:
                    raise ValueError('unused arguments')

        fmt = CheckAllUsedFormatter()
        self.assertEqual(fmt.format('{0}', 10), '10')
        self.assertEqual(fmt.format('{0}{i}', 10, i=100), '10100')
        self.assertEqual(fmt.format('{0}{i}{1}', 10, 20, i=100), '1010020')
        self.assertRaises(ValueError, fmt.format, '{0}{i}{1}', 10, 20, i=100, j=0)
        self.assertRaises(ValueError, fmt.format, '{0}', 10, 20)
        self.assertRaises(ValueError, fmt.format, '{0}', 10, 20, i=100)
        self.assertRaises(ValueError, fmt.format, '{i}', 10, 20, i=100)
        self.assertRaises(ValueError, format, '', '#')
        self.assertRaises(ValueError, format, '', '#20')


class BytesAliasTest(unittest.TestCase):

    def test_builtin(self):
        self.assertTrue(str is bytes)

    def test_syntax(self):
        self.assertEqual('spam', 'spam')
        self.assertEqual('egg\\foo', 'egg\\foo')
        self.assertTrue(type(''), str)
        self.assertTrue(type(''), str)


def test_main():
    test_support.run_unittest(StringTest, ModuleTest, BytesAliasTest)


if __name__ == '__main__':
    test_main()