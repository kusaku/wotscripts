# Embedded file name: scripts/common/Lib/test/test_pwd.py
import sys
import unittest
from test import test_support
pwd = test_support.import_module('pwd')

class PwdTest(unittest.TestCase):

    def test_values(self):
        entries = pwd.getpwall()
        entriesbyname = {}
        entriesbyuid = {}
        for e in entries:
            self.assertEqual(len(e), 7)
            self.assertEqual(e[0], e.pw_name)
            self.assertIsInstance(e.pw_name, basestring)
            self.assertEqual(e[1], e.pw_passwd)
            self.assertIsInstance(e.pw_passwd, basestring)
            self.assertEqual(e[2], e.pw_uid)
            self.assertIsInstance(e.pw_uid, int)
            self.assertEqual(e[3], e.pw_gid)
            self.assertIsInstance(e.pw_gid, int)
            self.assertEqual(e[4], e.pw_gecos)
            self.assertIsInstance(e.pw_gecos, basestring)
            self.assertEqual(e[5], e.pw_dir)
            self.assertIsInstance(e.pw_dir, basestring)
            self.assertEqual(e[6], e.pw_shell)
            self.assertIsInstance(e.pw_shell, basestring)
            entriesbyname.setdefault(e.pw_name, []).append(e)
            entriesbyuid.setdefault(e.pw_uid, []).append(e)

        if len(entries) > 1000:
            return
        for e in entries:
            if not e[0] or e[0] == '+':
                continue
            self.assertIn(pwd.getpwnam(e.pw_name), entriesbyname[e.pw_name])
            self.assertIn(pwd.getpwuid(e.pw_uid), entriesbyuid[e.pw_uid])

    def test_errors(self):
        self.assertRaises(TypeError, pwd.getpwuid)
        self.assertRaises(TypeError, pwd.getpwnam)
        self.assertRaises(TypeError, pwd.getpwall, 42)
        bynames = {}
        byuids = {}
        for n, p, u, g, gecos, d, s in pwd.getpwall():
            bynames[n] = u
            byuids[u] = n

        allnames = bynames.keys()
        namei = 0
        fakename = allnames[namei]
        while fakename in bynames:
            chars = list(fakename)
            for i in xrange(len(chars)):
                if chars[i] == 'z':
                    chars[i] = 'A'
                    break
                elif chars[i] == 'Z':
                    continue
                else:
                    chars[i] = chr(ord(chars[i]) + 1)
                    break
            else:
                namei = namei + 1
                try:
                    fakename = allnames[namei]
                except IndexError:
                    break

            fakename = ''.join(chars)

        self.assertRaises(KeyError, pwd.getpwnam, fakename)
        fakeuid = sys.maxint
        self.assertNotIn(fakeuid, byuids)
        self.assertRaises(KeyError, pwd.getpwuid, fakeuid)


def test_main():
    test_support.run_unittest(PwdTest)


if __name__ == '__main__':
    test_main()