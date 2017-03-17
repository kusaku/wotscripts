# Embedded file name: scripts/common/Lib/test/test_gettext.py
import os
import base64
import shutil
import gettext
import unittest
from test import test_support
GNU_MO_DATA = '3hIElQAAAAAGAAAAHAAAAEwAAAALAAAAfAAAAAAAAACoAAAAFQAAAKkAAAAjAAAAvwAAAKEAAADj\nAAAABwAAAIUBAAALAAAAjQEAAEUBAACZAQAAFgAAAN8CAAAeAAAA9gIAAKEAAAAVAwAABQAAALcD\nAAAJAAAAvQMAAAEAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABQAAAAYAAAACAAAAAFJh\neW1vbmQgTHV4dXJ5IFlhY2gtdABUaGVyZSBpcyAlcyBmaWxlAFRoZXJlIGFyZSAlcyBmaWxlcwBU\naGlzIG1vZHVsZSBwcm92aWRlcyBpbnRlcm5hdGlvbmFsaXphdGlvbiBhbmQgbG9jYWxpemF0aW9u\nCnN1cHBvcnQgZm9yIHlvdXIgUHl0aG9uIHByb2dyYW1zIGJ5IHByb3ZpZGluZyBhbiBpbnRlcmZh\nY2UgdG8gdGhlIEdOVQpnZXR0ZXh0IG1lc3NhZ2UgY2F0YWxvZyBsaWJyYXJ5LgBtdWxsdXNrAG51\nZGdlIG51ZGdlAFByb2plY3QtSWQtVmVyc2lvbjogMi4wClBPLVJldmlzaW9uLURhdGU6IDIwMDAt\nMDgtMjkgMTI6MTktMDQ6MDAKTGFzdC1UcmFuc2xhdG9yOiBKLiBEYXZpZCBJYsOhw7FleiA8ai1k\nYXZpZEBub29zLmZyPgpMYW5ndWFnZS1UZWFtOiBYWCA8cHl0aG9uLWRldkBweXRob24ub3JnPgpN\nSU1FLVZlcnNpb246IDEuMApDb250ZW50LVR5cGU6IHRleHQvcGxhaW47IGNoYXJzZXQ9aXNvLTg4\nNTktMQpDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiBub25lCkdlbmVyYXRlZC1CeTogcHlnZXR0\nZXh0LnB5IDEuMQpQbHVyYWwtRm9ybXM6IG5wbHVyYWxzPTI7IHBsdXJhbD1uIT0xOwoAVGhyb2F0\nd29iYmxlciBNYW5ncm92ZQBIYXkgJXMgZmljaGVybwBIYXkgJXMgZmljaGVyb3MAR3V2ZiB6YnFo\neXIgY2ViaXZxcmYgdmFncmVhbmd2YmFueXZtbmd2YmEgbmFxIHlicG55dm1uZ3ZiYQpmaGNjYmVn\nIHNiZSBsYmhlIENsZ3ViYSBjZWJ0ZW56ZiBvbCBjZWJpdnF2YXQgbmEgdmFncmVzbnByIGdiIGd1\nciBUQUgKdHJnZ3JrZyB6cmZmbnRyIHBuZ255YnQgeXZvZW5lbC4AYmFjb24Ad2luayB3aW5rAA==\n'
UMO_DATA = '3hIElQAAAAACAAAAHAAAACwAAAAFAAAAPAAAAAAAAABQAAAABAAAAFEAAAAPAQAAVgAAAAQAAABm\nAQAAAQAAAAIAAAAAAAAAAAAAAAAAAAAAYWLDngBQcm9qZWN0LUlkLVZlcnNpb246IDIuMApQTy1S\nZXZpc2lvbi1EYXRlOiAyMDAzLTA0LTExIDEyOjQyLTA0MDAKTGFzdC1UcmFuc2xhdG9yOiBCYXJy\neSBBLiBXQXJzYXcgPGJhcnJ5QHB5dGhvbi5vcmc+Ckxhbmd1YWdlLVRlYW06IFhYIDxweXRob24t\nZGV2QHB5dGhvbi5vcmc+Ck1JTUUtVmVyc2lvbjogMS4wCkNvbnRlbnQtVHlwZTogdGV4dC9wbGFp\nbjsgY2hhcnNldD11dGYtOApDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiA3Yml0CkdlbmVyYXRl\nZC1CeTogbWFudWFsbHkKAMKkeXoA\n'
MMO_DATA = '3hIElQAAAAABAAAAHAAAACQAAAADAAAALAAAAAAAAAA4AAAAeAEAADkAAAABAAAAAAAAAAAAAAAA\nUHJvamVjdC1JZC1WZXJzaW9uOiBObyBQcm9qZWN0IDAuMApQT1QtQ3JlYXRpb24tRGF0ZTogV2Vk\nIERlYyAxMSAwNzo0NDoxNSAyMDAyClBPLVJldmlzaW9uLURhdGU6IDIwMDItMDgtMTQgMDE6MTg6\nNTgrMDA6MDAKTGFzdC1UcmFuc2xhdG9yOiBKb2huIERvZSA8amRvZUBleGFtcGxlLmNvbT4KSmFu\nZSBGb29iYXIgPGpmb29iYXJAZXhhbXBsZS5jb20+Ckxhbmd1YWdlLVRlYW06IHh4IDx4eEBleGFt\ncGxlLmNvbT4KTUlNRS1WZXJzaW9uOiAxLjAKQ29udGVudC1UeXBlOiB0ZXh0L3BsYWluOyBjaGFy\nc2V0PWlzby04ODU5LTE1CkNvbnRlbnQtVHJhbnNmZXItRW5jb2Rpbmc6IHF1b3RlZC1wcmludGFi\nbGUKR2VuZXJhdGVkLUJ5OiBweWdldHRleHQucHkgMS4zCgA=\n'
LOCALEDIR = os.path.join('xx', 'LC_MESSAGES')
MOFILE = os.path.join(LOCALEDIR, 'gettext.mo')
UMOFILE = os.path.join(LOCALEDIR, 'ugettext.mo')
MMOFILE = os.path.join(LOCALEDIR, 'metadata.mo')

class GettextBaseTest(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(LOCALEDIR):
            os.makedirs(LOCALEDIR)
        with open(MOFILE, 'wb') as fp:
            fp.write(base64.decodestring(GNU_MO_DATA))
        with open(UMOFILE, 'wb') as fp:
            fp.write(base64.decodestring(UMO_DATA))
        with open(MMOFILE, 'wb') as fp:
            fp.write(base64.decodestring(MMO_DATA))
        self.env = test_support.EnvironmentVarGuard()
        self.env['LANGUAGE'] = 'xx'
        gettext._translations.clear()

    def tearDown(self):
        self.env.__exit__()
        del self.env
        shutil.rmtree(os.path.split(LOCALEDIR)[0])


class GettextTestCase1(GettextBaseTest):

    def setUp(self):
        GettextBaseTest.setUp(self)
        self.localedir = os.curdir
        self.mofile = MOFILE
        gettext.install('gettext', self.localedir)

    def test_some_translations(self):
        eq = self.assertEqual
        eq(_('albatross'), 'albatross')
        eq(_(u'mullusk'), 'bacon')
        eq(_('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(_(u'nudge nudge'), 'wink wink')

    def test_double_quotes(self):
        eq = self.assertEqual
        eq(_('albatross'), 'albatross')
        eq(_(u'mullusk'), 'bacon')
        eq(_('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(_(u'nudge nudge'), 'wink wink')

    def test_triple_single_quotes(self):
        eq = self.assertEqual
        eq(_('albatross'), 'albatross')
        eq(_(u'mullusk'), 'bacon')
        eq(_('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(_(u'nudge nudge'), 'wink wink')

    def test_triple_double_quotes(self):
        eq = self.assertEqual
        eq(_('albatross'), 'albatross')
        eq(_(u'mullusk'), 'bacon')
        eq(_('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(_(u'nudge nudge'), 'wink wink')

    def test_multiline_strings(self):
        eq = self.assertEqual
        eq(_('This module provides internationalization and localization\nsupport for your Python programs by providing an interface to the GNU\ngettext message catalog library.'), 'Guvf zbqhyr cebivqrf vagreangvbanyvmngvba naq ybpnyvmngvba\nfhccbeg sbe lbhe Clguba cebtenzf ol cebivqvat na vagresnpr gb gur TAH\ntrggrkg zrffntr pngnybt yvoenel.')

    def test_the_alternative_interface(self):
        eq = self.assertEqual
        with open(self.mofile, 'rb') as fp:
            t = gettext.GNUTranslations(fp)
        t.install()
        eq(_('nudge nudge'), 'wink wink')
        t.install(unicode=True)
        eq(_('mullusk'), 'bacon')
        import __builtin__
        t.install(unicode=True, names=['gettext', 'lgettext'])
        eq(_, t.ugettext)
        eq(__builtin__.gettext, t.ugettext)
        eq(lgettext, t.lgettext)
        del __builtin__.gettext
        del __builtin__.lgettext


class GettextTestCase2(GettextBaseTest):

    def setUp(self):
        GettextBaseTest.setUp(self)
        self.localedir = os.curdir
        gettext.bindtextdomain('gettext', self.localedir)
        gettext.textdomain('gettext')
        self._ = gettext.gettext

    def test_bindtextdomain(self):
        self.assertEqual(gettext.bindtextdomain('gettext'), self.localedir)

    def test_textdomain(self):
        self.assertEqual(gettext.textdomain(), 'gettext')

    def test_some_translations(self):
        eq = self.assertEqual
        eq(self._('albatross'), 'albatross')
        eq(self._(u'mullusk'), 'bacon')
        eq(self._('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(self._(u'nudge nudge'), 'wink wink')

    def test_double_quotes(self):
        eq = self.assertEqual
        eq(self._('albatross'), 'albatross')
        eq(self._(u'mullusk'), 'bacon')
        eq(self._('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(self._(u'nudge nudge'), 'wink wink')

    def test_triple_single_quotes(self):
        eq = self.assertEqual
        eq(self._('albatross'), 'albatross')
        eq(self._(u'mullusk'), 'bacon')
        eq(self._('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(self._(u'nudge nudge'), 'wink wink')

    def test_triple_double_quotes(self):
        eq = self.assertEqual
        eq(self._('albatross'), 'albatross')
        eq(self._(u'mullusk'), 'bacon')
        eq(self._('Raymond Luxury Yach-t'), 'Throatwobbler Mangrove')
        eq(self._(u'nudge nudge'), 'wink wink')

    def test_multiline_strings(self):
        eq = self.assertEqual
        eq(self._('This module provides internationalization and localization\nsupport for your Python programs by providing an interface to the GNU\ngettext message catalog library.'), 'Guvf zbqhyr cebivqrf vagreangvbanyvmngvba naq ybpnyvmngvba\nfhccbeg sbe lbhe Clguba cebtenzf ol cebivqvat na vagresnpr gb gur TAH\ntrggrkg zrffntr pngnybt yvoenel.')


class PluralFormsTestCase(GettextBaseTest):

    def setUp(self):
        GettextBaseTest.setUp(self)
        self.mofile = MOFILE

    def test_plural_forms1(self):
        eq = self.assertEqual
        x = gettext.ngettext('There is %s file', 'There are %s files', 1)
        eq(x, 'Hay %s fichero')
        x = gettext.ngettext('There is %s file', 'There are %s files', 2)
        eq(x, 'Hay %s ficheros')

    def test_plural_forms2(self):
        eq = self.assertEqual
        with open(self.mofile, 'rb') as fp:
            t = gettext.GNUTranslations(fp)
        x = t.ngettext('There is %s file', 'There are %s files', 1)
        eq(x, 'Hay %s fichero')
        x = t.ngettext('There is %s file', 'There are %s files', 2)
        eq(x, 'Hay %s ficheros')

    def test_hu(self):
        eq = self.assertEqual
        f = gettext.c2py('0')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def test_de(self):
        eq = self.assertEqual
        f = gettext.c2py('n != 1')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '10111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')

    def test_fr(self):
        eq = self.assertEqual
        f = gettext.c2py('n>1')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '00111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111')

    def test_gd(self):
        eq = self.assertEqual
        f = gettext.c2py('n==1 ? 0 : n==2 ? 1 : 2')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '20122222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    def test_gd2(self):
        eq = self.assertEqual
        f = gettext.c2py('n==1 ? 0 : (n==2 ? 1 : 2)')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '20122222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')

    def test_lt(self):
        eq = self.assertEqual
        f = gettext.c2py('n%10==1 && n%100!=11 ? 0 : n%10>=2 && (n%100<10 || n%100>=20) ? 1 : 2')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '20111111112222222222201111111120111111112011111111201111111120111111112011111111201111111120111111112011111111222222222220111111112011111111201111111120111111112011111111201111111120111111112011111111')

    def test_ru(self):
        eq = self.assertEqual
        f = gettext.c2py('n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '20111222222222222222201112222220111222222011122222201112222220111222222011122222201112222220111222222011122222222222222220111222222011122222201112222220111222222011122222201112222220111222222011122222')

    def test_pl(self):
        eq = self.assertEqual
        f = gettext.c2py('n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '20111222222222222222221112222222111222222211122222221112222222111222222211122222221112222222111222222211122222222222222222111222222211122222221112222222111222222211122222221112222222111222222211122222')

    def test_sl(self):
        eq = self.assertEqual
        f = gettext.c2py('n%100==1 ? 0 : n%100==2 ? 1 : n%100==3 || n%100==4 ? 2 : 3')
        s = ''.join([ str(f(x)) for x in range(200) ])
        eq(s, '30122333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333012233333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')

    def test_security(self):
        raises = self.assertRaises
        raises(ValueError, gettext.c2py, "os.chmod('/etc/passwd',0777)")


class UnicodeTranslationsTest(GettextBaseTest):

    def setUp(self):
        GettextBaseTest.setUp(self)
        with open(UMOFILE, 'rb') as fp:
            self.t = gettext.GNUTranslations(fp)
        self._ = self.t.ugettext

    def test_unicode_msgid(self):
        unless = self.assertTrue
        unless(isinstance(self._(''), unicode))
        unless(isinstance(self._(u''), unicode))

    def test_unicode_msgstr(self):
        eq = self.assertEqual
        eq(self._(u'ab\xde'), u'\xa4yz')


class WeirdMetadataTest(GettextBaseTest):

    def setUp(self):
        GettextBaseTest.setUp(self)
        with open(MMOFILE, 'rb') as fp:
            try:
                self.t = gettext.GNUTranslations(fp)
            except:
                self.tearDown()
                raise

    def test_weird_metadata(self):
        info = self.t.info()
        self.assertEqual(info['last-translator'], 'John Doe <jdoe@example.com>\nJane Foobar <jfoobar@example.com>')


class DummyGNUTranslations(gettext.GNUTranslations):

    def foo(self):
        return 'foo'


class GettextCacheTestCase(GettextBaseTest):

    def test_cache(self):
        self.localedir = os.curdir
        self.mofile = MOFILE
        self.assertEqual(len(gettext._translations), 0)
        t = gettext.translation('gettext', self.localedir)
        self.assertEqual(len(gettext._translations), 1)
        t = gettext.translation('gettext', self.localedir, class_=DummyGNUTranslations)
        self.assertEqual(len(gettext._translations), 2)
        self.assertEqual(t.__class__, DummyGNUTranslations)
        t = gettext.translation('gettext', self.localedir, class_=DummyGNUTranslations)
        self.assertEqual(len(gettext._translations), 2)
        self.assertEqual(t.__class__, DummyGNUTranslations)


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()