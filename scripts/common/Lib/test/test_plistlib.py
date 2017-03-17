# Embedded file name: scripts/common/Lib/test/test_plistlib.py
import unittest
import plistlib
import os
import datetime
from test import test_support
TESTDATA = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n        <key>aDate</key>\n        <date>2004-10-26T10:33:33Z</date>\n        <key>aDict</key>\n        <dict>\n                <key>aFalseValue</key>\n                <false/>\n                <key>aTrueValue</key>\n                <true/>\n                <key>aUnicodeValue</key>\n                <string>M\xc3\xa4ssig, Ma\xc3\x9f</string>\n                <key>anotherString</key>\n                <string>&lt;hello &amp; \'hi\' there!&gt;</string>\n                <key>deeperDict</key>\n                <dict>\n                        <key>a</key>\n                        <integer>17</integer>\n                        <key>b</key>\n                        <real>32.5</real>\n                        <key>c</key>\n                        <array>\n                                <integer>1</integer>\n                                <integer>2</integer>\n                                <string>text</string>\n                        </array>\n                </dict>\n        </dict>\n        <key>aFloat</key>\n        <real>0.5</real>\n        <key>aList</key>\n        <array>\n                <string>A</string>\n                <string>B</string>\n                <integer>12</integer>\n                <real>32.5</real>\n                <array>\n                        <integer>1</integer>\n                        <integer>2</integer>\n                        <integer>3</integer>\n                </array>\n        </array>\n        <key>aString</key>\n        <string>Doodah</string>\n        <key>anInt</key>\n        <integer>728</integer>\n        <key>nestedData</key>\n        <array>\n                <data>\n                PGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAzxsb3RzIG9mIGJpbmFyeSBndW5r\n                PgABAgM8bG90cyBvZiBiaW5hcnkgZ3Vuaz4AAQIDPGxvdHMgb2YgYmluYXJ5\n                IGd1bms+AAECAzxsb3RzIG9mIGJpbmFyeSBndW5rPgABAgM8bG90cyBvZiBi\n                aW5hcnkgZ3Vuaz4AAQIDPGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAzxsb3Rz\n                IG9mIGJpbmFyeSBndW5rPgABAgM8bG90cyBvZiBiaW5hcnkgZ3Vuaz4AAQID\n                PGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAw==\n                </data>\n        </array>\n        <key>someData</key>\n        <data>\n        PGJpbmFyeSBndW5rPg==\n        </data>\n        <key>someMoreData</key>\n        <data>\n        PGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAzxsb3RzIG9mIGJpbmFyeSBndW5rPgABAgM8\n        bG90cyBvZiBiaW5hcnkgZ3Vuaz4AAQIDPGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAzxs\n        b3RzIG9mIGJpbmFyeSBndW5rPgABAgM8bG90cyBvZiBiaW5hcnkgZ3Vuaz4AAQIDPGxv\n        dHMgb2YgYmluYXJ5IGd1bms+AAECAzxsb3RzIG9mIGJpbmFyeSBndW5rPgABAgM8bG90\n        cyBvZiBiaW5hcnkgZ3Vuaz4AAQIDPGxvdHMgb2YgYmluYXJ5IGd1bms+AAECAw==\n        </data>\n        <key>\xc3\x85benraa</key>\n        <string>That was a unicode key.</string>\n</dict>\n</plist>\n'.replace('        ', '\t')

class TestPlistlib(unittest.TestCase):

    def tearDown(self):
        try:
            os.unlink(test_support.TESTFN)
        except:
            pass

    def _create(self):
        pl = dict(aString='Doodah', aList=['A',
         'B',
         12,
         32.5,
         [1, 2, 3]], aFloat=0.5, anInt=728, aDict=dict(anotherString="<hello & 'hi' there!>", aUnicodeValue=u'M\xe4ssig, Ma\xdf', aTrueValue=True, aFalseValue=False, deeperDict=dict(a=17, b=32.5, c=[1, 2, 'text'])), someData=plistlib.Data('<binary gunk>'), someMoreData=plistlib.Data('<lots of binary gunk>\x00\x01\x02\x03' * 10), nestedData=[plistlib.Data('<lots of binary gunk>\x00\x01\x02\x03' * 10)], aDate=datetime.datetime(2004, 10, 26, 10, 33, 33))
        pl[u'\xc5benraa'] = 'That was a unicode key.'
        return pl

    def test_create(self):
        pl = self._create()
        self.assertEqual(pl['aString'], 'Doodah')
        self.assertEqual(pl['aDict']['aFalseValue'], False)

    def test_io(self):
        pl = self._create()
        plistlib.writePlist(pl, test_support.TESTFN)
        pl2 = plistlib.readPlist(test_support.TESTFN)
        self.assertEqual(dict(pl), dict(pl2))

    def test_string(self):
        pl = self._create()
        data = plistlib.writePlistToString(pl)
        pl2 = plistlib.readPlistFromString(data)
        self.assertEqual(dict(pl), dict(pl2))
        data2 = plistlib.writePlistToString(pl2)
        self.assertEqual(data, data2)

    def test_appleformatting(self):
        pl = plistlib.readPlistFromString(TESTDATA)
        data = plistlib.writePlistToString(pl)
        self.assertEqual(data, TESTDATA, "generated data was not identical to Apple's output")

    def test_appleformattingfromliteral(self):
        pl = self._create()
        pl2 = plistlib.readPlistFromString(TESTDATA)
        self.assertEqual(dict(pl), dict(pl2), "generated data was not identical to Apple's output")

    def test_stringio(self):
        from StringIO import StringIO
        f = StringIO()
        pl = self._create()
        plistlib.writePlist(pl, f)
        pl2 = plistlib.readPlist(StringIO(f.getvalue()))
        self.assertEqual(dict(pl), dict(pl2))

    def test_cstringio(self):
        from cStringIO import StringIO
        f = StringIO()
        pl = self._create()
        plistlib.writePlist(pl, f)
        pl2 = plistlib.readPlist(StringIO(f.getvalue()))
        self.assertEqual(dict(pl), dict(pl2))

    def test_controlcharacters(self):
        for i in range(128):
            c = chr(i)
            testString = 'string containing %s' % c
            if i >= 32 or c in '\r\n\t':
                plistlib.writePlistToString(testString)
            else:
                self.assertRaises(ValueError, plistlib.writePlistToString, testString)

    def test_nondictroot(self):
        test1 = 'abc'
        test2 = [1,
         2,
         3,
         'abc']
        result1 = plistlib.readPlistFromString(plistlib.writePlistToString(test1))
        result2 = plistlib.readPlistFromString(plistlib.writePlistToString(test2))
        self.assertEqual(test1, result1)
        self.assertEqual(test2, result2)


def test_main():
    test_support.run_unittest(TestPlistlib)


if __name__ == '__main__':
    test_main()