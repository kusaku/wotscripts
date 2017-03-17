# Embedded file name: scripts/common/Lib/test/test_threading.py
import test.test_support
from test.test_support import verbose
import random
import re
import sys
thread = test.test_support.import_module('thread')
threading = test.test_support.import_module('threading')
import time
import unittest
import weakref
import os
import subprocess
from test import lock_tests

class Counter(object):

    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1

    def get(self):
        return self.value


class TestThread(threading.Thread):

    def __init__(self, name, testcase, sema, mutex, nrunning):
        threading.Thread.__init__(self, name=name)
        self.testcase = testcase
        self.sema = sema
        self.mutex = mutex
        self.nrunning = nrunning

    def run(self):
        delay = random.random() / 10000.0
        if verbose:
            print 'task %s will run for %.1f usec' % (self.name, delay * 1000000.0)
        with self.sema:
            with self.mutex:
                self.nrunning.inc()
                if verbose:
                    print self.nrunning.get(), 'tasks are running'
                self.testcase.assertTrue(self.nrunning.get() <= 3)
            time.sleep(delay)
            if verbose:
                print 'task', self.name, 'done'
            with self.mutex:
                self.nrunning.dec()
                self.testcase.assertTrue(self.nrunning.get() >= 0)
                if verbose:
                    print '%s is finished. %d tasks are running' % (self.name, self.nrunning.get())


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self._threads = test.test_support.threading_setup()

    def tearDown(self):
        test.test_support.threading_cleanup(*self._threads)
        test.test_support.reap_children()


class ThreadTests(BaseTestCase):

    def test_various_ops(self):
        NUMTASKS = 10
        sema = threading.BoundedSemaphore(value=3)
        mutex = threading.RLock()
        numrunning = Counter()
        threads = []
        for i in range(NUMTASKS):
            t = TestThread('<thread %d>' % i, self, sema, mutex, numrunning)
            threads.append(t)
            self.assertEqual(t.ident, None)
            self.assertTrue(re.match('<TestThread\\(.*, initial\\)>', repr(t)))
            t.start()

        if verbose:
            print 'waiting for all tasks to complete'
        for t in threads:
            t.join(NUMTASKS)
            self.assertTrue(not t.is_alive())
            self.assertNotEqual(t.ident, 0)
            self.assertFalse(t.ident is None)
            self.assertTrue(re.match('<TestThread\\(.*, \\w+ -?\\d+\\)>', repr(t)))

        if verbose:
            print 'all tasks done'
        self.assertEqual(numrunning.get(), 0)
        return

    def test_ident_of_no_threading_threads(self):
        self.assertFalse(threading.currentThread().ident is None)

        def f():
            ident.append(threading.currentThread().ident)
            done.set()

        done = threading.Event()
        ident = []
        thread.start_new_thread(f, ())
        done.wait()
        self.assertFalse(ident[0] is None)
        del threading._active[ident[0]]
        return

    def test_various_ops_small_stack(self):
        if verbose:
            print 'with 256kB thread stack size...'
        try:
            threading.stack_size(262144)
        except thread.error:
            if verbose:
                print 'platform does not support changing thread stack size'
            return

        self.test_various_ops()
        threading.stack_size(0)

    def test_various_ops_large_stack(self):
        if verbose:
            print 'with 1MB thread stack size...'
        try:
            threading.stack_size(1048576)
        except thread.error:
            if verbose:
                print 'platform does not support changing thread stack size'
            return

        self.test_various_ops()
        threading.stack_size(0)

    def test_foreign_thread(self):

        def f(mutex):
            threading.current_thread()
            mutex.release()

        mutex = threading.Lock()
        mutex.acquire()
        tid = thread.start_new_thread(f, (mutex,))
        mutex.acquire()
        self.assertIn(tid, threading._active)
        self.assertIsInstance(threading._active[tid], threading._DummyThread)
        del threading._active[tid]

    def test_PyThreadState_SetAsyncExc(self):
        try:
            import ctypes
        except ImportError:
            if verbose:
                print "test_PyThreadState_SetAsyncExc can't import ctypes"
            return

        set_async_exc = ctypes.pythonapi.PyThreadState_SetAsyncExc

        class AsyncExc(Exception):
            pass

        exception = ctypes.py_object(AsyncExc)
        tid = thread.get_ident()
        try:
            result = set_async_exc(ctypes.c_long(tid), exception)
            while True:
                pass

        except AsyncExc:
            pass
        else:
            self.fail('AsyncExc not raised')

        try:
            self.assertEqual(result, 1)
        except UnboundLocalError:
            pass

        worker_started = threading.Event()
        worker_saw_exception = threading.Event()

        class Worker(threading.Thread):

            def run(self):
                self.id = thread.get_ident()
                self.finished = False
                try:
                    while True:
                        worker_started.set()
                        time.sleep(0.1)

                except AsyncExc:
                    self.finished = True
                    worker_saw_exception.set()

        t = Worker()
        t.daemon = True
        t.start()
        if verbose:
            print '    started worker thread'
        if verbose:
            print '    trying nonsensical thread id'
        result = set_async_exc(ctypes.c_long(-1), exception)
        self.assertEqual(result, 0)
        if verbose:
            print '    waiting for worker thread to get started'
        ret = worker_started.wait()
        self.assertTrue(ret)
        if verbose:
            print "    verifying worker hasn't exited"
        self.assertTrue(not t.finished)
        if verbose:
            print '    attempting to raise asynch exception in worker'
        result = set_async_exc(ctypes.c_long(t.id), exception)
        self.assertEqual(result, 1)
        if verbose:
            print '    waiting for worker to say it caught the exception'
        worker_saw_exception.wait(timeout=10)
        self.assertTrue(t.finished)
        if verbose:
            print '    all OK -- joining worker'
        if t.finished:
            t.join()

    def test_limbo_cleanup(self):

        def fail_new_thread(*args):
            raise thread.error()

        _start_new_thread = threading._start_new_thread
        threading._start_new_thread = fail_new_thread
        try:
            t = threading.Thread(target=lambda : None)
            self.assertRaises(thread.error, t.start)
            self.assertFalse(t in threading._limbo, 'Failed to cleanup _limbo map on failure of Thread.start().')
        finally:
            threading._start_new_thread = _start_new_thread

    def test_finalize_runnning_thread(self):
        try:
            import ctypes
        except ImportError:
            if verbose:
                print "test_finalize_with_runnning_thread can't import ctypes"
            return

        rc = subprocess.call([sys.executable, '-c', 'if 1:\n            import ctypes, sys, time, thread\n\n            # This lock is used as a simple event variable.\n            ready = thread.allocate_lock()\n            ready.acquire()\n\n            # Module globals are cleared before __del__ is run\n            # So we save the functions in class dict\n            class C:\n                ensure = ctypes.pythonapi.PyGILState_Ensure\n                release = ctypes.pythonapi.PyGILState_Release\n                def __del__(self):\n                    state = self.ensure()\n                    self.release(state)\n\n            def waitingThread():\n                x = C()\n                ready.release()\n                time.sleep(100)\n\n            thread.start_new_thread(waitingThread, ())\n            ready.acquire()  # Be sure the other thread is waiting.\n            sys.exit(42)\n            '])
        self.assertEqual(rc, 42)

    def test_finalize_with_trace(self):
        p = subprocess.Popen([sys.executable, '-c', "if 1:\n            import sys, threading\n\n            # A deadlock-killer, to prevent the\n            # testsuite to hang forever\n            def killer():\n                import os, time\n                time.sleep(2)\n                print 'program blocked; aborting'\n                os._exit(2)\n            t = threading.Thread(target=killer)\n            t.daemon = True\n            t.start()\n\n            # This is the trace function\n            def func(frame, event, arg):\n                threading.current_thread()\n                return func\n\n            sys.settrace(func)\n            "], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(p.stdout.close)
        self.addCleanup(p.stderr.close)
        stdout, stderr = p.communicate()
        rc = p.returncode
        self.assertFalse(rc == 2, 'interpreted was blocked')
        self.assertTrue(rc == 0, 'Unexpected error: ' + repr(stderr))

    def test_join_nondaemon_on_shutdown(self):
        p = subprocess.Popen([sys.executable, '-c', 'if 1:\n                import threading\n                from time import sleep\n\n                def child():\n                    sleep(1)\n                    # As a non-daemon thread we SHOULD wake up and nothing\n                    # should be torn down yet\n                    print "Woke up, sleep function is:", sleep\n\n                threading.Thread(target=child).start()\n                raise SystemExit\n            '], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(p.stdout.close)
        self.addCleanup(p.stderr.close)
        stdout, stderr = p.communicate()
        self.assertEqual(stdout.strip(), 'Woke up, sleep function is: <built-in function sleep>')
        stderr = re.sub('^\\[\\d+ refs\\]', '', stderr, re.MULTILINE).strip()
        self.assertEqual(stderr, '')

    def test_enumerate_after_join(self):
        enum = threading.enumerate
        old_interval = sys.getcheckinterval()
        try:
            for i in xrange(1, 100):
                sys.setcheckinterval(i // 5)
                t = threading.Thread(target=lambda : None)
                t.start()
                t.join()
                l = enum()
                self.assertNotIn(t, l, '#1703448 triggered after %d trials: %s' % (i, l))

        finally:
            sys.setcheckinterval(old_interval)

    def test_no_refcycle_through_target(self):

        class RunSelfFunction(object):

            def __init__(self, should_raise):
                self.should_raise = should_raise
                self.thread = threading.Thread(target=self._run, args=(self,), kwargs={'yet_another': self})
                self.thread.start()

            def _run(self, other_ref, yet_another):
                if self.should_raise:
                    raise SystemExit

        cyclic_object = RunSelfFunction(should_raise=False)
        weak_cyclic_object = weakref.ref(cyclic_object)
        cyclic_object.thread.join()
        del cyclic_object
        self.assertEqual(None, weak_cyclic_object(), msg='%d references still around' % sys.getrefcount(weak_cyclic_object()))
        raising_cyclic_object = RunSelfFunction(should_raise=True)
        weak_raising_cyclic_object = weakref.ref(raising_cyclic_object)
        raising_cyclic_object.thread.join()
        del raising_cyclic_object
        self.assertEqual(None, weak_raising_cyclic_object(), msg='%d references still around' % sys.getrefcount(weak_raising_cyclic_object()))
        return


class ThreadJoinOnShutdown(BaseTestCase):
    platforms_to_skip = ('freebsd4', 'freebsd5', 'freebsd6', 'netbsd5', 'os2emx')

    def _run_and_join(self, script):
        script = "if 1:\n            import sys, os, time, threading\n\n            # a thread, which waits for the main program to terminate\n            def joiningfunc(mainthread):\n                mainthread.join()\n                print 'end of thread'\n        \n" + script
        p = subprocess.Popen([sys.executable, '-c', script], stdout=subprocess.PIPE)
        rc = p.wait()
        data = p.stdout.read().replace('\r', '')
        p.stdout.close()
        self.assertEqual(data, 'end of main\nend of thread\n')
        self.assertFalse(rc == 2, 'interpreter was blocked')
        self.assertTrue(rc == 0, 'Unexpected error')

    def test_1_join_on_shutdown(self):
        script = "if 1:\n            import os\n            t = threading.Thread(target=joiningfunc,\n                                 args=(threading.current_thread(),))\n            t.start()\n            time.sleep(0.1)\n            print 'end of main'\n            "
        self._run_and_join(script)

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork()')
    @unittest.skipIf(sys.platform in platforms_to_skip, 'due to known OS bug')
    def test_2_join_in_forked_process(self):
        script = "if 1:\n            childpid = os.fork()\n            if childpid != 0:\n                os.waitpid(childpid, 0)\n                sys.exit(0)\n\n            t = threading.Thread(target=joiningfunc,\n                                 args=(threading.current_thread(),))\n            t.start()\n            print 'end of main'\n            "
        self._run_and_join(script)

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork()')
    @unittest.skipIf(sys.platform in platforms_to_skip, 'due to known OS bug')
    def test_3_join_in_forked_from_thread(self):
        script = "if 1:\n            main_thread = threading.current_thread()\n            def worker():\n                childpid = os.fork()\n                if childpid != 0:\n                    os.waitpid(childpid, 0)\n                    sys.exit(0)\n\n                t = threading.Thread(target=joiningfunc,\n                                     args=(main_thread,))\n                print 'end of main'\n                t.start()\n                t.join() # Should not block: main_thread is already stopped\n\n            w = threading.Thread(target=worker)\n            w.start()\n            "
        self._run_and_join(script)

    def assertScriptHasOutput(self, script, expected_output):
        p = subprocess.Popen([sys.executable, '-c', script], stdout=subprocess.PIPE)
        rc = p.wait()
        data = p.stdout.read().decode().replace('\r', '')
        self.assertEqual(rc, 0, 'Unexpected error')
        self.assertEqual(data, expected_output)

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork()')
    @unittest.skipIf(sys.platform in platforms_to_skip, 'due to known OS bug')
    def test_4_joining_across_fork_in_worker_thread(self):
        script = "if 1:\n            import os, time, threading\n\n            finish_join = False\n            start_fork = False\n\n            def worker():\n                # Wait until this thread's lock is acquired before forking to\n                # create the deadlock.\n                global finish_join\n                while not start_fork:\n                    time.sleep(0.01)\n                # LOCK HELD: Main thread holds lock across this call.\n                childpid = os.fork()\n                finish_join = True\n                if childpid != 0:\n                    # Parent process just waits for child.\n                    os.waitpid(childpid, 0)\n                # Child process should just return.\n\n            w = threading.Thread(target=worker)\n\n            # Stub out the private condition variable's lock acquire method.\n            # This acquires the lock and then waits until the child has forked\n            # before returning, which will release the lock soon after.  If\n            # someone else tries to fix this test case by acquiring this lock\n            # before forking instead of resetting it, the test case will\n            # deadlock when it shouldn't.\n            condition = w._block\n            orig_acquire = condition.acquire\n            call_count_lock = threading.Lock()\n            call_count = 0\n            def my_acquire():\n                global call_count\n                global start_fork\n                orig_acquire()  # LOCK ACQUIRED HERE\n                start_fork = True\n                if call_count == 0:\n                    while not finish_join:\n                        time.sleep(0.01)  # WORKER THREAD FORKS HERE\n                with call_count_lock:\n                    call_count += 1\n            condition.acquire = my_acquire\n\n            w.start()\n            w.join()\n            print('end of main')\n            "
        self.assertScriptHasOutput(script, 'end of main\n')

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork()')
    @unittest.skipIf(sys.platform in platforms_to_skip, 'due to known OS bug')
    def test_5_clear_waiter_locks_to_avoid_crash(self):
        script = "if True:\n            import os, time, threading\n\n            start_fork = False\n\n            def worker():\n                # Wait until the main thread has attempted to join this thread\n                # before continuing.\n                while not start_fork:\n                    time.sleep(0.01)\n                childpid = os.fork()\n                if childpid != 0:\n                    # Parent process just waits for child.\n                    (cpid, rc) = os.waitpid(childpid, 0)\n                    assert cpid == childpid\n                    assert rc == 0\n                    print('end of worker thread')\n                else:\n                    # Child process should just return.\n                    pass\n\n            w = threading.Thread(target=worker)\n\n            # Stub out the private condition variable's _release_save method.\n            # This releases the condition's lock and flips the global that\n            # causes the worker to fork.  At this point, the problematic waiter\n            # lock has been acquired once by the waiter and has been put onto\n            # the waiters list.\n            condition = w._block\n            orig_release_save = condition._release_save\n            def my_release_save():\n                global start_fork\n                orig_release_save()\n                # Waiter lock held here, condition lock released.\n                start_fork = True\n            condition._release_save = my_release_save\n\n            w.start()\n            w.join()\n            print('end of main thread')\n            "
        output = 'end of worker thread\nend of main thread\n'
        self.assertScriptHasOutput(script, output)

    @unittest.skipUnless(hasattr(os, 'fork'), 'needs os.fork()')
    @unittest.skipIf(sys.platform in platforms_to_skip, 'due to known OS bug')
    def test_reinit_tls_after_fork(self):

        def do_fork_and_wait():
            pid = os.fork()
            if pid > 0:
                os.waitpid(pid, 0)
            else:
                os._exit(0)

        threads = []
        for i in range(16):
            t = threading.Thread(target=do_fork_and_wait)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


class ThreadingExceptionTests(BaseTestCase):

    def test_start_thread_again(self):
        thread = threading.Thread()
        thread.start()
        self.assertRaises(RuntimeError, thread.start)

    def test_joining_current_thread(self):
        current_thread = threading.current_thread()
        self.assertRaises(RuntimeError, current_thread.join)

    def test_joining_inactive_thread(self):
        thread = threading.Thread()
        self.assertRaises(RuntimeError, thread.join)

    def test_daemonize_active_thread(self):
        thread = threading.Thread()
        thread.start()
        self.assertRaises(RuntimeError, setattr, thread, 'daemon', True)


class LockTests(lock_tests.LockTests):
    locktype = staticmethod(threading.Lock)


class RLockTests(lock_tests.RLockTests):
    locktype = staticmethod(threading.RLock)


class EventTests(lock_tests.EventTests):
    eventtype = staticmethod(threading.Event)


class ConditionAsRLockTests(lock_tests.RLockTests):
    locktype = staticmethod(threading.Condition)


class ConditionTests(lock_tests.ConditionTests):
    condtype = staticmethod(threading.Condition)


class SemaphoreTests(lock_tests.SemaphoreTests):
    semtype = staticmethod(threading.Semaphore)


class BoundedSemaphoreTests(lock_tests.BoundedSemaphoreTests):
    semtype = staticmethod(threading.BoundedSemaphore)

    @unittest.skipUnless(sys.platform == 'darwin', 'test macosx problem')
    def test_recursion_limit(self):
        script = "if True:\n            import threading\n\n            def recurse():\n                return recurse()\n\n            def outer():\n                try:\n                    recurse()\n                except RuntimeError:\n                    pass\n\n            w = threading.Thread(target=outer)\n            w.start()\n            w.join()\n            print('end of main thread')\n            "
        expected_output = 'end of main thread\n'
        p = subprocess.Popen([sys.executable, '-c', script], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        data = stdout.decode().replace('\r', '')
        self.assertEqual(p.returncode, 0, 'Unexpected error')
        self.assertEqual(data, expected_output)


def test_main():
    test.test_support.run_unittest(LockTests, RLockTests, EventTests, ConditionAsRLockTests, ConditionTests, SemaphoreTests, BoundedSemaphoreTests, ThreadTests, ThreadJoinOnShutdown, ThreadingExceptionTests)


if __name__ == '__main__':
    test_main()