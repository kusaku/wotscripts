# Embedded file name: scripts/common/Lib/test/test_dummy_thread.py
"""Generic thread tests.

Meant to be used by dummy_thread and thread.  To allow for different modules
to be used, test_main() can be called with the module to use as the thread
implementation as its sole argument.

"""
import dummy_thread as _thread
import time
import Queue
import random
import unittest
from test import test_support
DELAY = 0

class LockTests(unittest.TestCase):
    """Test lock objects."""

    def setUp(self):
        global _thread
        self.lock = _thread.allocate_lock()

    def test_initlock(self):
        self.assertTrue(not self.lock.locked(), 'Lock object is not initialized unlocked.')

    def test_release(self):
        self.lock.acquire()
        self.lock.release()
        self.assertTrue(not self.lock.locked(), 'Lock object did not release properly.')

    def test_improper_release(self):
        self.assertRaises(_thread.error, self.lock.release)

    def test_cond_acquire_success(self):
        self.assertTrue(self.lock.acquire(0), 'Conditional acquiring of the lock failed.')

    def test_cond_acquire_fail(self):
        self.lock.acquire(0)
        self.assertTrue(not self.lock.acquire(0), 'Conditional acquiring of a locked lock incorrectly succeeded.')

    def test_uncond_acquire_success(self):
        self.lock.acquire()
        self.assertTrue(self.lock.locked(), 'Uncondional locking failed.')

    def test_uncond_acquire_return_val(self):
        self.assertTrue(self.lock.acquire(1) is True, 'Unconditional locking did not return True.')
        self.assertTrue(self.lock.acquire() is True)

    def test_uncond_acquire_blocking(self):
        global DELAY

        def delay_unlock(to_unlock, delay):
            """Hold on to lock for a set amount of time before unlocking."""
            time.sleep(delay)
            to_unlock.release()

        self.lock.acquire()
        start_time = int(time.time())
        _thread.start_new_thread(delay_unlock, (self.lock, DELAY))
        if test_support.verbose:
            print
            print '*** Waiting for thread to release the lock (approx. %s sec.) ***' % DELAY
        self.lock.acquire()
        end_time = int(time.time())
        if test_support.verbose:
            print 'done'
        self.assertTrue(end_time - start_time >= DELAY, 'Blocking by unconditional acquiring failed.')


class MiscTests(unittest.TestCase):
    """Miscellaneous tests."""

    def test_exit(self):
        self.assertRaises(SystemExit, _thread.exit)

    def test_ident(self):
        self.assertIsInstance(_thread.get_ident(), int, '_thread.get_ident() returned a non-integer')
        self.assertTrue(_thread.get_ident() != 0, '_thread.get_ident() returned 0')

    def test_LockType(self):
        self.assertIsInstance(_thread.allocate_lock(), _thread.LockType, '_thread.LockType is not an instance of what is returned by _thread.allocate_lock()')

    def test_interrupt_main(self):

        def call_interrupt():
            _thread.interrupt_main()

        self.assertRaises(KeyboardInterrupt, _thread.start_new_thread, call_interrupt, tuple())

    def test_interrupt_in_main(self):
        self.assertRaises(KeyboardInterrupt, _thread.interrupt_main)


class ThreadTests(unittest.TestCase):
    """Test thread creation."""

    def test_arg_passing(self):

        def arg_tester(queue, arg1 = False, arg2 = False):
            """Use to test _thread.start_new_thread() passes args properly."""
            queue.put((arg1, arg2))

        testing_queue = Queue.Queue(1)
        _thread.start_new_thread(arg_tester, (testing_queue, True, True))
        result = testing_queue.get()
        self.assertTrue(result[0] and result[1], 'Argument passing for thread creation using tuple failed')
        _thread.start_new_thread(arg_tester, tuple(), {'queue': testing_queue,
         'arg1': True,
         'arg2': True})
        result = testing_queue.get()
        self.assertTrue(result[0] and result[1], 'Argument passing for thread creation using kwargs failed')
        _thread.start_new_thread(arg_tester, (testing_queue, True), {'arg2': True})
        result = testing_queue.get()
        self.assertTrue(result[0] and result[1], 'Argument passing for thread creation using both tuple and kwargs failed')

    def test_multi_creation(self):

        def queue_mark(queue, delay):
            """Wait for ``delay`` seconds and then put something into ``queue``"""
            time.sleep(delay)
            queue.put(_thread.get_ident())

        thread_count = 5
        testing_queue = Queue.Queue(thread_count)
        if test_support.verbose:
            print
            print '*** Testing multiple thread creation (will take approx. %s to %s sec.) ***' % (DELAY, thread_count)
        for count in xrange(thread_count):
            if DELAY:
                local_delay = round(random.random(), 1)
            else:
                local_delay = 0
            _thread.start_new_thread(queue_mark, (testing_queue, local_delay))

        time.sleep(DELAY)
        if test_support.verbose:
            print 'done'
        self.assertTrue(testing_queue.qsize() == thread_count, 'Not all %s threads executed properly after %s sec.' % (thread_count, DELAY))


def test_main(imported_module = None):
    global DELAY
    global _thread
    if imported_module:
        _thread = imported_module
        DELAY = 2
    if test_support.verbose:
        print
        print '*** Using %s as _thread module ***' % _thread
    test_support.run_unittest(LockTests, MiscTests, ThreadTests)


if __name__ == '__main__':
    test_main()