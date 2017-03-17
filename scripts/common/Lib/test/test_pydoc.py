# Embedded file name: scripts/common/Lib/test/test_pydoc.py
import os
import sys
import difflib
import __builtin__
import re
import pydoc
import inspect
import keyword
import unittest
import xml.etree
import test.test_support
from collections import namedtuple
from test.script_helper import assert_python_ok
from test.test_support import TESTFN, rmtree, reap_children, captured_stdout
from test import pydoc_mod
expected_text_pattern = "\nNAME\n    test.pydoc_mod - This is a test module for test_pydoc\n\nFILE\n    %s\n%s\nCLASSES\n    __builtin__.object\n        B\n    A\n    \n    class A\n     |  Hello and goodbye\n     |  \n     |  Methods defined here:\n     |  \n     |  __init__()\n     |      Wow, I have no function!\n    \n    class B(__builtin__.object)\n     |  Data descriptors defined here:\n     |  \n     |  __dict__\n     |      dictionary for instance variables (if defined)\n     |  \n     |  __weakref__\n     |      list of weak references to the object (if defined)\n     |  \n     |  ----------------------------------------------------------------------\n     |  Data and other attributes defined here:\n     |  \n     |  NO_MEANING = 'eggs'\n\nFUNCTIONS\n    doc_func()\n        This function solves all of the world's problems:\n        hunger\n        lack of Python\n        war\n    \n    nodoc_func()\n\nDATA\n    __author__ = 'Benjamin Peterson'\n    __credits__ = 'Nobody'\n    __version__ = '1.2.3.4'\n\nVERSION\n    1.2.3.4\n\nAUTHOR\n    Benjamin Peterson\n\nCREDITS\n    Nobody\n".strip()
expected_html_pattern = '\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="heading">\n<tr bgcolor="#7799ee">\n<td valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial">&nbsp;<br><big><big><strong><a href="test.html"><font color="#ffffff">test</font></a>.pydoc_mod</strong></big></big> (version 1.2.3.4)</font></td\n><td align=right valign=bottom\n><font color="#ffffff" face="helvetica, arial"><a href=".">index</a><br><a href="file:%s">%s</a>%s</font></td></tr></table>\n    <p><tt>This&nbsp;is&nbsp;a&nbsp;test&nbsp;module&nbsp;for&nbsp;test_pydoc</tt></p>\n<p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#ee77aa">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial"><big><strong>Classes</strong></big></font></td></tr>\n    \n<tr><td bgcolor="#ee77aa"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%"><dl>\n<dt><font face="helvetica, arial"><a href="__builtin__.html#object">__builtin__.object</a>\n</font></dt><dd>\n<dl>\n<dt><font face="helvetica, arial"><a href="test.pydoc_mod.html#B">B</a>\n</font></dt></dl>\n</dd>\n<dt><font face="helvetica, arial"><a href="test.pydoc_mod.html#A">A</a>\n</font></dt></dl>\n <p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#ffc8d8">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#000000" face="helvetica, arial"><a name="A">class <strong>A</strong></a></font></td></tr>\n    \n<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>\n<td colspan=2><tt>Hello&nbsp;and&nbsp;goodbye<br>&nbsp;</tt></td></tr>\n<tr><td>&nbsp;</td>\n<td width="100%%">Methods defined here:<br>\n<dl><dt><a name="A-__init__"><strong>__init__</strong></a>()</dt><dd><tt>Wow,&nbsp;I&nbsp;have&nbsp;no&nbsp;function!</tt></dd></dl>\n\n</td></tr></table> <p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#ffc8d8">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#000000" face="helvetica, arial"><a name="B">class <strong>B</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>\n    \n<tr><td bgcolor="#ffc8d8"><tt>&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%">Data descriptors defined here:<br>\n<dl><dt><strong>__dict__</strong></dt>\n<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>\n</dl>\n<dl><dt><strong>__weakref__</strong></dt>\n<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>\n</dl>\n<hr>\nData and other attributes defined here:<br>\n<dl><dt><strong>NO_MEANING</strong> = \'eggs\'</dl>\n\n</td></tr></table></td></tr></table><p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#eeaa77">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial"><big><strong>Functions</strong></big></font></td></tr>\n    \n<tr><td bgcolor="#eeaa77"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%"><dl><dt><a name="-doc_func"><strong>doc_func</strong></a>()</dt><dd><tt>This&nbsp;function&nbsp;solves&nbsp;all&nbsp;of&nbsp;the&nbsp;world\'s&nbsp;problems:<br>\nhunger<br>\nlack&nbsp;of&nbsp;Python<br>\nwar</tt></dd></dl>\n <dl><dt><a name="-nodoc_func"><strong>nodoc_func</strong></a>()</dt></dl>\n</td></tr></table><p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#55aa55">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>\n    \n<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%"><strong>__author__</strong> = \'Benjamin Peterson\'<br>\n<strong>__credits__</strong> = \'Nobody\'<br>\n<strong>__version__</strong> = \'1.2.3.4\'</td></tr></table><p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#7799ee">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial"><big><strong>Author</strong></big></font></td></tr>\n    \n<tr><td bgcolor="#7799ee"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%">Benjamin&nbsp;Peterson</td></tr></table><p>\n<table width="100%%" cellspacing=0 cellpadding=2 border=0 summary="section">\n<tr bgcolor="#7799ee">\n<td colspan=3 valign=bottom>&nbsp;<br>\n<font color="#ffffff" face="helvetica, arial"><big><strong>Credits</strong></big></font></td></tr>\n    \n<tr><td bgcolor="#7799ee"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>\n<td width="100%%">Nobody</td></tr></table>\n'.strip()
missing_pattern = "no Python documentation found for '%s'"
badimport_pattern = "problem in %s - <type 'exceptions.ImportError'>: No module named %s"

def run_pydoc(module_name, *args, **env):
    """
    Runs pydoc on the specified module. Returns the stripped
    output of pydoc.
    """
    args = args + (module_name,)
    rc, out, err = assert_python_ok('-B', pydoc.__file__, *args, **env)
    return out.strip()


def get_pydoc_html(module):
    """Returns pydoc generated output as html"""
    doc = pydoc.HTMLDoc()
    output = doc.docmodule(module)
    loc = doc.getdocloc(pydoc_mod) or ''
    if loc:
        loc = '<br><a href="' + loc + '">Module Docs</a>'
    return (output.strip(), loc)


def get_pydoc_text(module):
    """Returns pydoc generated output as text"""
    doc = pydoc.TextDoc()
    loc = doc.getdocloc(pydoc_mod) or ''
    if loc:
        loc = '\nMODULE DOCS\n    ' + loc + '\n'
    output = doc.docmodule(module)
    patt = re.compile('\x08.')
    output = patt.sub('', output)
    return (output.strip(), loc)


def print_diffs(text1, text2):
    """Prints unified diffs for two texts"""
    lines1 = text1.splitlines(True)
    lines2 = text2.splitlines(True)
    diffs = difflib.unified_diff(lines1, lines2, n=0, fromfile='expected', tofile='got')
    print '\n' + ''.join(diffs)


class PyDocDocTest(unittest.TestCase):

    @unittest.skipIf(sys.flags.optimize >= 2, 'Docstrings are omitted with -O2 and above')
    def test_html_doc(self):
        result, doc_loc = get_pydoc_html(pydoc_mod)
        mod_file = inspect.getabsfile(pydoc_mod)
        if sys.platform == 'win32':
            import nturl2path
            mod_url = nturl2path.pathname2url(mod_file)
        else:
            mod_url = mod_file
        expected_html = expected_html_pattern % (mod_url, mod_file, doc_loc)
        if result != expected_html:
            print_diffs(expected_html, result)
            self.fail('outputs are not equal, see diff above')

    @unittest.skipIf(sys.flags.optimize >= 2, 'Docstrings are omitted with -O2 and above')
    def test_text_doc(self):
        result, doc_loc = get_pydoc_text(pydoc_mod)
        expected_text = expected_text_pattern % (inspect.getabsfile(pydoc_mod), doc_loc)
        if result != expected_text:
            print_diffs(expected_text, result)
            self.fail('outputs are not equal, see diff above')

    def test_issue8225(self):
        result, doc_loc = get_pydoc_text(xml.etree)
        self.assertEqual(doc_loc, '', 'MODULE DOCS incorrectly includes a link')

    def test_not_here(self):
        missing_module = 'test.i_am_not_here'
        result = run_pydoc(missing_module)
        expected = missing_pattern % missing_module
        self.assertEqual(expected, result, 'documentation for missing module found')

    def test_input_strip(self):
        missing_module = ' test.i_am_not_here '
        result = run_pydoc(missing_module)
        expected = missing_pattern % missing_module.strip()
        self.assertEqual(expected, result, 'white space was not stripped from module name or other error output mismatch')

    def test_stripid(self):
        stripid = pydoc.stripid
        self.assertEqual(stripid('<function stripid at 0x88dcee4>'), '<function stripid>')
        self.assertEqual(stripid('<function stripid at 0x01F65390>'), '<function stripid>')
        self.assertEqual(stripid('42'), '42')
        self.assertEqual(stripid("<type 'exceptions.Exception'>"), "<type 'exceptions.Exception'>")


class PydocImportTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.mkdir(TESTFN)
        self.addCleanup(rmtree, TESTFN)

    def test_badimport(self):
        modname = 'testmod_xyzzy'
        testpairs = (('i_am_not_here', 'i_am_not_here'),
         ('test.i_am_not_here_either', 'i_am_not_here_either'),
         ('test.i_am_not_here.neither_am_i', 'i_am_not_here.neither_am_i'),
         ('i_am_not_here.{}'.format(modname), 'i_am_not_here.{}'.format(modname)),
         ('test.{}'.format(modname), modname))
        sourcefn = os.path.join(TESTFN, modname) + os.extsep + 'py'
        for importstring, expectedinmsg in testpairs:
            with open(sourcefn, 'w') as f:
                f.write('import {}\n'.format(importstring))
            result = run_pydoc(modname, PYTHONPATH=TESTFN)
            expected = badimport_pattern % (modname, expectedinmsg)
            self.assertEqual(expected, result)

    def test_apropos_with_bad_package(self):
        pkgdir = os.path.join(TESTFN, 'syntaxerr')
        os.mkdir(pkgdir)
        badsyntax = os.path.join(pkgdir, '__init__') + os.extsep + 'py'
        with open(badsyntax, 'w') as f:
            f.write('invalid python syntax = $1\n')
        result = run_pydoc('zqwykjv', '-k', PYTHONPATH=TESTFN)
        self.assertEqual('', result)

    def test_apropos_with_unreadable_dir(self):
        self.unreadable_dir = os.path.join(TESTFN, 'unreadable')
        os.mkdir(self.unreadable_dir, 0)
        self.addCleanup(os.rmdir, self.unreadable_dir)
        result = run_pydoc('zqwykjv', '-k', PYTHONPATH=TESTFN)
        self.assertEqual('', result)


class TestDescriptions(unittest.TestCase):

    def test_module(self):
        from test import pydocfodder
        doc = pydoc.render_doc(pydocfodder)
        self.assertIn('pydocfodder', doc)

    def test_classic_class(self):

        class C:
            """Classic class"""
            pass

        c = C()
        self.assertEqual(pydoc.describe(C), 'class C')
        self.assertEqual(pydoc.describe(c), 'instance of C')
        expected = 'instance of C in module %s' % __name__
        self.assertIn(expected, pydoc.render_doc(c))

    def test_class(self):

        class C(object):
            """New-style class"""
            pass

        c = C()
        self.assertEqual(pydoc.describe(C), 'class C')
        self.assertEqual(pydoc.describe(c), 'C')
        expected = 'C in module %s object' % __name__
        self.assertIn(expected, pydoc.render_doc(c))

    def test_namedtuple_public_underscore(self):
        NT = namedtuple('NT', ['abc', 'def'], rename=True)
        with captured_stdout() as help_io:
            help(NT)
        helptext = help_io.getvalue()
        self.assertIn('_1', helptext)
        self.assertIn('_replace', helptext)
        self.assertIn('_asdict', helptext)


class TestHelper(unittest.TestCase):

    def test_keywords(self):
        self.assertEqual(sorted(pydoc.Helper.keywords), sorted(keyword.kwlist))

    def test_builtin(self):
        for name in ('str', 'str.translate', '__builtin__.str', '__builtin__.str.translate'):
            self.assertIsNotNone(pydoc.locate(name))
            try:
                pydoc.render_doc(name)
            except ImportError:
                self.fail('finding the doc of {!r} failed'.format(o))

        for name in ('not__builtin__', 'strrr', 'strr.translate', 'str.trrrranslate', '__builtin__.strrr', '__builtin__.str.trrranslate'):
            self.assertIsNone(pydoc.locate(name))
            self.assertRaises(ImportError, pydoc.render_doc, name)


def test_main():
    try:
        test.test_support.run_unittest(PyDocDocTest, PydocImportTest, TestDescriptions, TestHelper)
    finally:
        reap_children()


if __name__ == '__main__':
    test_main()