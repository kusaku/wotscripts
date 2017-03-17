# Embedded file name: scripts/common/Lib/test/test_wait4.py
"""This test checks for correct wait4() behavior.
"""
import os
import time
from test.fork_wait import ForkWait
from test.test_support import run_unittest, reap_children, get_attribute
get_attribute(os, 'fork')
get_attribute(os, 'wait4')

class Wait4Test(ForkWait):

    def wait_impl(self, cpid):
        for i in range(10):
            spid, status, rusage = os.wait4(cpid, os.WNOHANG)
            if spid == cpid:
                break
            time.sleep(1.0)

        self.assertEqual(spid, cpid)
        self.assertEqual(status, 0, 'cause = %d, exit = %d' % (status & 255, status >> 8))
        self.assertTrue(rusage)


def test_main():
    run_unittest(Wait4Test)
    reap_children()


if __name__ == '__main__':
    test_main()