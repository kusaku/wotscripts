# Embedded file name: scripts/common/Lib/test/test_bsddb3.py
"""
Run all test cases.
"""
import os
import sys
import tempfile
import time
import unittest
from test.test_support import requires, run_unittest, import_module
import_module('_bsddb')
import_module('bsddb', deprecated=True)
if __name__ != '__main__':
    requires('bsddb')
verbose = False
if 'verbose' in sys.argv:
    verbose = True
    sys.argv.remove('verbose')
if 'silent' in sys.argv:
    verbose = False
    sys.argv.remove('silent')

class TimingCheck(unittest.TestCase):
    """This class is not a real test.  Its purpose is to print a message
    periodically when the test runs slowly.  This will prevent the buildbots
    from timing out on slow machines."""
    _PRINT_WORKING_MSG_INTERVAL = 240
    next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL

    def testCheckElapsedTime(self):
        now = time.time()
        if self.next_time <= now:
            TimingCheck.next_time = now + self._PRINT_WORKING_MSG_INTERVAL
            sys.__stdout__.write('  test_bsddb3 still working, be patient...\n')
            sys.__stdout__.flush()


def test_main():
    from bsddb import db
    from bsddb.test import test_all
    test_all.set_test_path_prefix(os.path.join(tempfile.gettempdir(), 'z-test_bsddb3-%s' % os.getpid()))
    print >> sys.stderr, db.DB_VERSION_STRING
    print >> sys.stderr, 'Test path prefix: ', test_all.get_test_path_prefix()
    try:
        run_unittest(test_all.suite(module_prefix='bsddb.test.', timing_check=TimingCheck))
    finally:
        try:
            test_all.remove_test_path_directory()
        except:
            pass


if __name__ == '__main__':
    test_main()