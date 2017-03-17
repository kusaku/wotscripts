# Embedded file name: scripts/common/Lib/test/test_thread.py
import os
import unittest
import random
from test import test_support
thread = test_support.import_module('thread')
import time
import sys
import weakref
from test import lock_tests
NUMTASKS = 10
NUMTRIPS = 3
_print_mutex = thread.allocate_lock()

def verbose_print(arg):
    """Helper function for printing out debugging output."""
    if test_support.verbose:
        with _print_mutex:
            print arg


class BasicThreadTest(unittest.TestCase):

    def setUp(self):
        self.done_mutex = thread.allocate_lock()
        self.done_mutex.acquire()
        self.running_mutex = thread.allocate_lock()
        self.random_mutex = thread.allocate_lock()
        self.created = 0
        self.running = 0
        self.next_ident = 0


class ThreadRunningTests(BasicThreadTest):

    def newtask(self):
        with self.running_mutex:
            self.next_ident += 1
            verbose_print('creating task %s' % self.next_ident)
            thread.start_new_thread(self.task, (self.next_ident,))
            self.created += 1
            self.running += 1

    def task(self, ident):
        with self.random_mutex:
            delay = random.random() / 10000.0
        verbose_print('task %s will run for %sus' % (ident, round(delay * 1000000.0)))
        time.sleep(delay)
        verbose_print('task %s done' % ident)
        with self.running_mutex:
            self.running -= 1
            if self.created == NUMTASKS and self.running == 0:
                self.done_mutex.release()

    def test_starting_threads(self):
        for i in range(NUMTASKS):
            self.newtask()

        verbose_print('waiting for tasks to complete...')
        self.done_mutex.acquire()
        verbose_print('all tasks done')

    def test_stack_size(self):
        self.assertEqual(thread.stack_size(), 0, 'initial stack size is not 0')
        thread.stack_size(0)
        self.assertEqual(thread.stack_size(), 0, 'stack_size not reset to default')
        if os.name not in ('nt', 'os2', 'posix'):
            return
        tss_supported = True
        try:
            thread.stack_size(4096)
        except ValueError:
            verbose_print('caught expected ValueError setting stack_size(4096)')
        except thread.error:
            tss_supported = False
            verbose_print('platform does not support changing thread stack size')

        if tss_supported:
            fail_msg = 'stack_size(%d) failed - should succeed'
            for tss in (262144, 1048576, 0):
                thread.stack_size(tss)
                self.assertEqual(thread.stack_size(), tss, fail_msg % tss)
                verbose_print('successfully set stack_size(%d)' % tss)

            for tss in (262144, 1048576):
                verbose_print('trying stack_size = (%d)' % tss)
                self.next_ident = 0
                self.created = 0
                for i in range(NUMTASKS):
                    self.newtask()

                verbose_print('waiting for all tasks to complete')
                self.done_mutex.acquire()
                verbose_print('all tasks done')

            thread.stack_size(0)

    def test__count(self):
        orig = thread._count()
        mut = thread.allocate_lock()
        mut.acquire()
        started = []

        def task():
            started.append(None)
            mut.acquire()
            mut.release()
            return

        thread.start_new_thread(task, ())
        while not started:
            time.sleep(0.01)

        self.assertEqual(thread._count(), orig + 1)
        mut.release()
        done = []
        wr = weakref.ref(task, lambda _: done.append(None))
        del task
        while not done:
            time.sleep(0.01)

        self.assertEqual(thread._count(), orig)


class Barrier:

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.waiting = 0
        self.checkin_mutex = thread.allocate_lock()
        self.checkout_mutex = thread.allocate_lock()
        self.checkout_mutex.acquire()

    def enter(self):
        self.checkin_mutex.acquire()
        self.waiting = self.waiting + 1
        if self.waiting == self.num_threads:
            self.waiting = self.num_threads - 1
            self.checkout_mutex.release()
            return
        self.checkin_mutex.release()
        self.checkout_mutex.acquire()
        self.waiting = self.waiting - 1
        if self.waiting == 0:
            self.checkin_mutex.release()
            return
        self.checkout_mutex.release()


class BarrierTest(BasicThreadTest):

    def test_barrier(self):
        self.bar = Barrier(NUMTASKS)
        self.running = NUMTASKS
        for i in range(NUMTASKS):
            thread.start_new_thread(self.task2, (i,))

        verbose_print('waiting for tasks to end')
        self.done_mutex.acquire()
        verbose_print('tasks done')

    def task2(self, ident):
        for i in range(NUMTRIPS):
            if ident == 0:
                delay = 0
            else:
                with self.random_mutex:
                    delay = random.random() / 10000.0
            verbose_print('task %s will run for %sus' % (ident, round(delay * 1000000.0)))
            time.sleep(delay)
            verbose_print('task %s entering %s' % (ident, i))
            self.bar.enter()
            verbose_print('task %s leaving barrier' % ident)

        with self.running_mutex:
            self.running -= 1
            finished = self.running == 0
        if finished:
            self.done_mutex.release()


class LockTests(lock_tests.LockTests):
    locktype = thread.allocate_lock


class TestForkInThread(unittest.TestCase):

    def setUp(self):
        self.read_fd, self.write_fd = os.pipe()

    @unittest.skipIf(sys.platform.startswith('win'), 'This test is only appropriate for POSIX-like systems.')
    @test_support.reap_threads
    def test_forkinthread(self):

        def thread1():
            try:
                pid = os.fork()
            except RuntimeError:
                sys.exit(0)

            if pid == 0:
                os.close(self.read_fd)
                os.write(self.write_fd, 'OK')
                sys.exit(0)
            else:
                os.close(self.write_fd)

        thread.start_new_thread(thread1, ())
        self.assertEqual(os.read(self.read_fd, 2), 'OK', 'Unable to fork() in thread')

    def tearDown(self):
        try:
            os.close(self.read_fd)
        except OSError:
            pass

        try:
            os.close(self.write_fd)
        except OSError:
            pass


def test_main():
    test_support.run_unittest(ThreadRunningTests, BarrierTest, LockTests, TestForkInThread)


if __name__ == '__main__':
    test_main()