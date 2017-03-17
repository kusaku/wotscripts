# Embedded file name: scripts/common/Lib/test/test_textwrap.py
import unittest
from test import test_support
from textwrap import TextWrapper, wrap, fill, dedent

class BaseTestCase(unittest.TestCase):
    """Parent class with utility methods for textwrap tests."""

    def show(self, textin):
        if isinstance(textin, list):
            result = []
            for i in range(len(textin)):
                result.append('  %d: %r' % (i, textin[i]))

            result = '\n'.join(result)
        elif isinstance(textin, basestring):
            result = '  %s\n' % repr(textin)
        return result

    def check(self, result, expect):
        self.assertEqual(result, expect, 'expected:\n%s\nbut got:\n%s' % (self.show(expect), self.show(result)))

    def check_wrap(self, text, width, expect, **kwargs):
        result = wrap(text, width, **kwargs)
        self.check(result, expect)

    def check_split(self, text, expect):
        result = self.wrapper._split(text)
        self.assertEqual(result, expect, '\nexpected %r\nbut got  %r' % (expect, result))


class WrapTestCase(BaseTestCase):

    def setUp(self):
        self.wrapper = TextWrapper(width=45)

    def test_simple(self):
        text = "Hello there, how are you this fine day?  I'm glad to hear it!"
        self.check_wrap(text, 12, ['Hello there,',
         'how are you',
         'this fine',
         "day?  I'm",
         'glad to hear',
         'it!'])
        self.check_wrap(text, 42, ['Hello there, how are you this fine day?', "I'm glad to hear it!"])
        self.check_wrap(text, 80, [text])

    def test_whitespace(self):
        text = 'This is a paragraph that already has\nline breaks.  But some of its lines are much longer than the others,\nso it needs to be wrapped.\nSome lines are \ttabbed too.\nWhat a mess!\n'
        expect = ['This is a paragraph that already has line',
         'breaks.  But some of its lines are much',
         'longer than the others, so it needs to be',
         'wrapped.  Some lines are  tabbed too.  What a',
         'mess!']
        wrapper = TextWrapper(45, fix_sentence_endings=True)
        result = wrapper.wrap(text)
        self.check(result, expect)
        result = wrapper.fill(text)
        self.check(result, '\n'.join(expect))

    def test_fix_sentence_endings(self):
        wrapper = TextWrapper(60, fix_sentence_endings=True)
        text = 'A short line. Note the single space.'
        expect = ['A short line.  Note the single space.']
        self.check(wrapper.wrap(text), expect)
        text = 'Well, Doctor? What do you think?'
        expect = ['Well, Doctor?  What do you think?']
        self.check(wrapper.wrap(text), expect)
        text = 'Well, Doctor?\nWhat do you think?'
        self.check(wrapper.wrap(text), expect)
        text = 'I say, chaps! Anyone for "tennis?"\nHmmph!'
        expect = ['I say, chaps!  Anyone for "tennis?"  Hmmph!']
        self.check(wrapper.wrap(text), expect)
        wrapper.width = 20
        expect = ['I say, chaps!', 'Anyone for "tennis?"', 'Hmmph!']
        self.check(wrapper.wrap(text), expect)
        text = 'And she said, "Go to hell!"\nCan you believe that?'
        expect = ['And she said, "Go to', 'hell!"  Can you', 'believe that?']
        self.check(wrapper.wrap(text), expect)
        wrapper.width = 60
        expect = ['And she said, "Go to hell!"  Can you believe that?']
        self.check(wrapper.wrap(text), expect)
        text = 'File stdio.h is nice.'
        expect = ['File stdio.h is nice.']
        self.check(wrapper.wrap(text), expect)

    def test_wrap_short(self):
        text = 'This is a\nshort paragraph.'
        self.check_wrap(text, 20, ['This is a short', 'paragraph.'])
        self.check_wrap(text, 40, ['This is a short paragraph.'])

    def test_wrap_short_1line(self):
        text = 'This is a short line.'
        self.check_wrap(text, 30, ['This is a short line.'])
        self.check_wrap(text, 30, ['(1) This is a short line.'], initial_indent='(1) ')

    def test_hyphenated(self):
        text = "this-is-a-useful-feature-for-reformatting-posts-from-tim-peters'ly"
        self.check_wrap(text, 40, ['this-is-a-useful-feature-for-', "reformatting-posts-from-tim-peters'ly"])
        self.check_wrap(text, 41, ['this-is-a-useful-feature-for-', "reformatting-posts-from-tim-peters'ly"])
        self.check_wrap(text, 42, ['this-is-a-useful-feature-for-reformatting-', "posts-from-tim-peters'ly"])

    def test_hyphenated_numbers(self):
        text = 'Python 1.0.0 was released on 1994-01-26.  Python 1.0.1 was\nreleased on 1994-02-15.'
        self.check_wrap(text, 35, ['Python 1.0.0 was released on', '1994-01-26.  Python 1.0.1 was', 'released on 1994-02-15.'])
        self.check_wrap(text, 40, ['Python 1.0.0 was released on 1994-01-26.', 'Python 1.0.1 was released on 1994-02-15.'])
        text = 'I do all my shopping at 7-11.'
        self.check_wrap(text, 25, ['I do all my shopping at', '7-11.'])
        self.check_wrap(text, 27, ['I do all my shopping at', '7-11.'])
        self.check_wrap(text, 29, ['I do all my shopping at 7-11.'])

    def test_em_dash(self):
        text = 'Em-dashes should be written -- thus.'
        self.check_wrap(text, 25, ['Em-dashes should be', 'written -- thus.'])
        self.check_wrap(text, 29, ['Em-dashes should be written', '-- thus.'])
        expect = ['Em-dashes should be written --', 'thus.']
        self.check_wrap(text, 30, expect)
        self.check_wrap(text, 35, expect)
        self.check_wrap(text, 36, ['Em-dashes should be written -- thus.'])
        text = 'You can also do--this or even---this.'
        expect = ['You can also do', '--this or even', '---this.']
        self.check_wrap(text, 15, expect)
        self.check_wrap(text, 16, expect)
        expect = ['You can also do--', 'this or even---', 'this.']
        self.check_wrap(text, 17, expect)
        self.check_wrap(text, 19, expect)
        expect = ['You can also do--this or even', '---this.']
        self.check_wrap(text, 29, expect)
        self.check_wrap(text, 31, expect)
        expect = ['You can also do--this or even---', 'this.']
        self.check_wrap(text, 32, expect)
        self.check_wrap(text, 35, expect)
        text = "Here's an -- em-dash and--here's another---and another!"
        expect = ["Here's",
         ' ',
         'an',
         ' ',
         '--',
         ' ',
         'em-',
         'dash',
         ' ',
         'and',
         '--',
         "here's",
         ' ',
         'another',
         '---',
         'and',
         ' ',
         'another!']
        self.check_split(text, expect)
        text = 'and then--bam!--he was gone'
        expect = ['and',
         ' ',
         'then',
         '--',
         'bam!',
         '--',
         'he',
         ' ',
         'was',
         ' ',
         'gone']
        self.check_split(text, expect)

    def test_unix_options(self):
        text = 'You should use the -n option, or --dry-run in its long form.'
        self.check_wrap(text, 20, ['You should use the',
         '-n option, or --dry-',
         'run in its long',
         'form.'])
        self.check_wrap(text, 21, ['You should use the -n', 'option, or --dry-run', 'in its long form.'])
        expect = ['You should use the -n option, or', '--dry-run in its long form.']
        self.check_wrap(text, 32, expect)
        self.check_wrap(text, 34, expect)
        self.check_wrap(text, 35, expect)
        self.check_wrap(text, 38, expect)
        expect = ['You should use the -n option, or --dry-', 'run in its long form.']
        self.check_wrap(text, 39, expect)
        self.check_wrap(text, 41, expect)
        expect = ['You should use the -n option, or --dry-run', 'in its long form.']
        self.check_wrap(text, 42, expect)
        text = 'the -n option, or --dry-run or --dryrun'
        expect = ['the',
         ' ',
         '-n',
         ' ',
         'option,',
         ' ',
         'or',
         ' ',
         '--dry-',
         'run',
         ' ',
         'or',
         ' ',
         '--dryrun']
        self.check_split(text, expect)

    def test_funky_hyphens(self):
        self.check_split('what the--hey!', ['what',
         ' ',
         'the',
         '--',
         'hey!'])
        self.check_split('what the--', ['what', ' ', 'the--'])
        self.check_split('what the--.', ['what', ' ', 'the--.'])
        self.check_split('--text--.', ['--text--.'])
        self.check_split('--option', ['--option'])
        self.check_split('--option-opt', ['--option-', 'opt'])
        self.check_split('foo --option-opt bar', ['foo',
         ' ',
         '--option-',
         'opt',
         ' ',
         'bar'])

    def test_punct_hyphens(self):
        self.check_split("the 'wibble-wobble' widget", ['the',
         ' ',
         "'wibble-",
         "wobble'",
         ' ',
         'widget'])
        self.check_split('the "wibble-wobble" widget', ['the',
         ' ',
         '"wibble-',
         'wobble"',
         ' ',
         'widget'])
        self.check_split('the (wibble-wobble) widget', ['the',
         ' ',
         '(wibble-',
         'wobble)',
         ' ',
         'widget'])
        self.check_split("the ['wibble-wobble'] widget", ['the',
         ' ',
         "['wibble-",
         "wobble']",
         ' ',
         'widget'])

    def test_funky_parens(self):
        self.check_split('foo (--option) bar', ['foo',
         ' ',
         '(--option)',
         ' ',
         'bar'])
        self.check_split('foo (bar) baz', ['foo',
         ' ',
         '(bar)',
         ' ',
         'baz'])
        self.check_split('blah (ding dong), wubba', ['blah',
         ' ',
         '(ding',
         ' ',
         'dong),',
         ' ',
         'wubba'])

    def test_initial_whitespace(self):
        text = ' This is a sentence with leading whitespace.'
        self.check_wrap(text, 50, [' This is a sentence with leading whitespace.'])
        self.check_wrap(text, 30, [' This is a sentence with', 'leading whitespace.'])

    def test_no_drop_whitespace(self):
        text = ' This is a    sentence with     much whitespace.'
        self.check_wrap(text, 10, [' This is a',
         '    ',
         'sentence ',
         'with     ',
         'much white',
         'space.'], drop_whitespace=False)

    if test_support.have_unicode:

        def test_unicode(self):
            text = u'Hello there, how are you today?'
            self.check_wrap(text, 50, [u'Hello there, how are you today?'])
            self.check_wrap(text, 20, [u'Hello there, how are', 'you today?'])
            olines = self.wrapper.wrap(text)
            self.assertIsInstance(olines, list)
            self.assertIsInstance(olines[0], unicode)
            otext = self.wrapper.fill(text)
            self.assertIsInstance(otext, unicode)

        def test_no_split_at_umlaut(self):
            text = u'Die Empf\xe4nger-Auswahl'
            self.check_wrap(text, 13, [u'Die', u'Empf\xe4nger-', u'Auswahl'])

        def test_umlaut_followed_by_dash(self):
            text = u'aa \xe4\xe4-\xe4\xe4'
            self.check_wrap(text, 7, [u'aa \xe4\xe4-', u'\xe4\xe4'])

    def test_split(self):
        text = 'Hello there -- you goof-ball, use the -b option!'
        result = self.wrapper._split(text)
        self.check(result, ['Hello',
         ' ',
         'there',
         ' ',
         '--',
         ' ',
         'you',
         ' ',
         'goof-',
         'ball,',
         ' ',
         'use',
         ' ',
         'the',
         ' ',
         '-b',
         ' ',
         'option!'])

    def test_break_on_hyphens(self):
        text = 'yaba daba-doo'
        self.check_wrap(text, 10, ['yaba daba-', 'doo'], break_on_hyphens=True)
        self.check_wrap(text, 10, ['yaba', 'daba-doo'], break_on_hyphens=False)

    def test_bad_width(self):
        text = "Whatever, it doesn't matter."
        self.assertRaises(ValueError, wrap, text, 0)
        self.assertRaises(ValueError, wrap, text, -1)


class LongWordTestCase(BaseTestCase):

    def setUp(self):
        self.wrapper = TextWrapper()
        self.text = 'Did you say "supercalifragilisticexpialidocious?"\nHow *do* you spell that odd word, anyways?\n'

    def test_break_long(self):
        self.check_wrap(self.text, 30, ['Did you say "supercalifragilis',
         'ticexpialidocious?" How *do*',
         'you spell that odd word,',
         'anyways?'])
        self.check_wrap(self.text, 50, ['Did you say "supercalifragilisticexpialidocious?"', 'How *do* you spell that odd word, anyways?'])
        self.check_wrap('----------hello', 10, ['----------',
         '               h',
         '               e',
         '               l',
         '               l',
         '               o'], subsequent_indent='               ')
        self.check_wrap(self.text, 12, ['Did you say ',
         '"supercalifr',
         'agilisticexp',
         'ialidocious?',
         '" How *do*',
         'you spell',
         'that odd',
         'word,',
         'anyways?'])

    def test_nobreak_long(self):
        self.wrapper.break_long_words = 0
        self.wrapper.width = 30
        expect = ['Did you say',
         '"supercalifragilisticexpialidocious?"',
         'How *do* you spell that odd',
         'word, anyways?']
        result = self.wrapper.wrap(self.text)
        self.check(result, expect)
        result = wrap(self.text, width=30, break_long_words=0)
        self.check(result, expect)


class IndentTestCases(BaseTestCase):

    def setUp(self):
        self.text = 'This paragraph will be filled, first without any indentation,\nand then with some (including a hanging indent).'

    def test_fill(self):
        expect = 'This paragraph will be filled, first\nwithout any indentation, and then with\nsome (including a hanging indent).'
        result = fill(self.text, 40)
        self.check(result, expect)

    def test_initial_indent(self):
        expect = ['     This paragraph will be filled,', 'first without any indentation, and then', 'with some (including a hanging indent).']
        result = wrap(self.text, 40, initial_indent='     ')
        self.check(result, expect)
        expect = '\n'.join(expect)
        result = fill(self.text, 40, initial_indent='     ')
        self.check(result, expect)

    def test_subsequent_indent(self):
        expect = '  * This paragraph will be filled, first\n    without any indentation, and then\n    with some (including a hanging\n    indent).'
        result = fill(self.text, 40, initial_indent='  * ', subsequent_indent='    ')
        self.check(result, expect)


class DedentTestCase(unittest.TestCase):

    def assertUnchanged(self, text):
        """assert that dedent() has no effect on 'text'"""
        self.assertEqual(text, dedent(text))

    def test_dedent_nomargin(self):
        text = "Hello there.\nHow are you?\nOh good, I'm glad."
        self.assertUnchanged(text)
        text = 'Hello there.\n\nBoo!'
        self.assertUnchanged(text)
        text = 'Hello there.\n  This is indented.'
        self.assertUnchanged(text)
        text = 'Hello there.\n\n  Boo!\n'
        self.assertUnchanged(text)

    def test_dedent_even(self):
        text = '  Hello there.\n  How are ya?\n  Oh good.'
        expect = 'Hello there.\nHow are ya?\nOh good.'
        self.assertEqual(expect, dedent(text))
        text = '  Hello there.\n\n  How are ya?\n  Oh good.\n'
        expect = 'Hello there.\n\nHow are ya?\nOh good.\n'
        self.assertEqual(expect, dedent(text))
        text = '  Hello there.\n  \n  How are ya?\n  Oh good.\n'
        expect = 'Hello there.\n\nHow are ya?\nOh good.\n'
        self.assertEqual(expect, dedent(text))

    def test_dedent_uneven(self):
        text = '        def foo():\n            while 1:\n                return foo\n        '
        expect = 'def foo():\n    while 1:\n        return foo\n'
        self.assertEqual(expect, dedent(text))
        text = '  Foo\n    Bar\n\n   Baz\n'
        expect = 'Foo\n  Bar\n\n Baz\n'
        self.assertEqual(expect, dedent(text))
        text = '  Foo\n    Bar\n \n   Baz\n'
        expect = 'Foo\n  Bar\n\n Baz\n'
        self.assertEqual(expect, dedent(text))

    def test_dedent_preserve_internal_tabs(self):
        text = '  hello\tthere\n  how are\tyou?'
        expect = 'hello\tthere\nhow are\tyou?'
        self.assertEqual(expect, dedent(text))
        self.assertEqual(expect, dedent(expect))

    def test_dedent_preserve_margin_tabs(self):
        text = '  hello there\n\thow are you?'
        self.assertUnchanged(text)
        text = '        hello there\n\thow are you?'
        self.assertUnchanged(text)
        text = '\thello there\n\thow are you?'
        expect = 'hello there\nhow are you?'
        self.assertEqual(expect, dedent(text))
        text = '  \thello there\n  \thow are you?'
        self.assertEqual(expect, dedent(text))
        text = '  \t  hello there\n  \t  how are you?'
        self.assertEqual(expect, dedent(text))
        text = '  \thello there\n  \t  how are you?'
        expect = 'hello there\n  how are you?'
        self.assertEqual(expect, dedent(text))


def test_main():
    test_support.run_unittest(WrapTestCase, LongWordTestCase, IndentTestCases, DedentTestCase)


if __name__ == '__main__':
    test_main()