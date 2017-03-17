# Embedded file name: scripts/common/Lib/test/test_threaded_import.py
import unittest
from test.test_support import verbose, TestFailed, import_module
thread = import_module('thread')
critical_section = thread.allocate_lock()
done = thread.allocate_lock()

def task():
    global N
    global done
    global critical_section
    import random
    x = random.randrange(1, 3)
    critical_section.acquire()
    N -= 1
    finished = N == 0
    critical_section.release()
    if finished:
        done.release()


def test_import_hangers():
    import sys
    if verbose:
        print 'testing import hangers ...',
    import test.threaded_import_hangers
    try:
        if test.threaded_import_hangers.errors:
            raise TestFailed(test.threaded_import_hangers.errors)
        elif verbose:
            print 'OK.'
    finally:
        del sys.modules['test.threaded_import_hangers']


def test_main():
    global N
    import imp
    if imp.lock_held():
        raise unittest.SkipTest("can't run when import lock is held")
    done.acquire()
    for N in (20, 50, 20, 50, 20, 50):
        if verbose:
            print 'Trying', N, 'threads ...',
        for i in range(N):
            thread.start_new_thread(task, ())

        done.acquire()
        if verbose:
            print 'OK.'

    done.release()
    test_import_hangers()


if __name__ == '__main__':
    test_main()