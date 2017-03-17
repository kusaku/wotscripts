# Embedded file name: scripts/common/Lib/test/test_commands.py
"""
   Tests for commands module
   Nick Mathewson
"""
import unittest
import os, tempfile, re
from test.test_support import run_unittest, reap_children, import_module, check_warnings
commands = import_module('commands', deprecated=True)
if os.name != 'posix':
    raise unittest.SkipTest('Not posix; skipping test_commands')

class CommandTests(unittest.TestCase):

    def test_getoutput(self):
        self.assertEqual(commands.getoutput('echo xyzzy'), 'xyzzy')
        self.assertEqual(commands.getstatusoutput('echo xyzzy'), (0, 'xyzzy'))
        dir = None
        try:
            dir = tempfile.mkdtemp()
            name = os.path.join(dir, 'foo')
            status, output = commands.getstatusoutput('cat ' + name)
            self.assertNotEqual(status, 0)
        finally:
            if dir is not None:
                os.rmdir(dir)

        return

    def test_getstatus(self):
        pat = 'd.........   # It is a directory.\n                  [.+@]?       # It may have special attributes.\n                  \\s+\\d+       # It has some number of links.\n                  [^/]*        # Skip user, group, size, and date.\n                  /\\.          # and end with the name of the file.\n               '
        with check_warnings(('.*commands.getstatus.. is deprecated', DeprecationWarning)):
            self.assertTrue(re.match(pat, commands.getstatus('/.'), re.VERBOSE))


def test_main():
    run_unittest(CommandTests)
    reap_children()


if __name__ == '__main__':
    test_main()