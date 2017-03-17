# Embedded file name: scripts/common/Lib/multiprocessing/queues.py
__all__ = ['Queue', 'SimpleQueue', 'JoinableQueue']
import sys
import os
import threading
import collections
import time
import atexit
import weakref
from Queue import Empty, Full
import _multiprocessing
from multiprocessing import Pipe
from multiprocessing.synchronize import Lock, BoundedSemaphore, Semaphore, Condition
from multiprocessing.util import debug, info, Finalize, register_after_fork
from multiprocessing.forking import assert_spawning

class Queue(object):

    def __init__(self, maxsize = 0):
        if maxsize <= 0:
            maxsize = _multiprocessing.SemLock.SEM_VALUE_MAX
        self._maxsize = maxsize
        self._reader, self._writer = Pipe(duplex=False)
        self._rlock = Lock()
        self._opid = os.getpid()
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = Lock()
        self._sem = BoundedSemaphore(maxsize)
        self._after_fork()
        if sys.platform != 'win32':
            register_after_fork(self, Queue._after_fork)
        return

    def __getstate__(self):
        assert_spawning(self)
        return (self._maxsize,
         self._reader,
         self._writer,
         self._rlock,
         self._wlock,
         self._sem,
         self._opid)

    def __setstate__(self, state):
        self._maxsize, self._reader, self._writer, self._rlock, self._wlock, self._sem, self._opid = state
        self._after_fork()

    def _after_fork(self):
        debug('Queue._after_fork()')
        self._notempty = threading.Condition(threading.Lock())
        self._buffer = collections.deque()
        self._thread = None
        self._jointhread = None
        self._joincancelled = False
        self._closed = False
        self._close = None
        self._send = self._writer.send
        self._recv = self._reader.recv
        self._poll = self._reader.poll
        return

    def put(self, obj, block = True, timeout = None):
        if not not self._closed:
            raise AssertionError
            raise self._sem.acquire(block, timeout) or Full
        self._notempty.acquire()
        try:
            if self._thread is None:
                self._start_thread()
            self._buffer.append(obj)
            self._notempty.notify()
        finally:
            self._notempty.release()

        return

    def get(self, block = True, timeout = None):
        if block and timeout is None:
            self._rlock.acquire()
            try:
                res = self._recv()
                self._sem.release()
                return res
            finally:
                self._rlock.release()

        else:
            if block:
                deadline = time.time() + timeout
            if not self._rlock.acquire(block, timeout):
                raise Empty
            try:
                if block:
                    timeout = deadline - time.time()
                    if timeout < 0 or not self._poll(timeout):
                        raise Empty
                elif not self._poll():
                    raise Empty
                res = self._recv()
                self._sem.release()
                return res
            finally:
                self._rlock.release()

        return

    def qsize(self):
        return self._maxsize - self._sem._semlock._get_value()

    def empty(self):
        return not self._poll()

    def full(self):
        return self._sem._semlock._is_zero()

    def get_nowait(self):
        return self.get(False)

    def put_nowait(self, obj):
        return self.put(obj, False)

    def close(self):
        self._closed = True
        self._reader.close()
        if self._close:
            self._close()

    def join_thread(self):
        debug('Queue.join_thread()')
        if not self._closed:
            raise AssertionError
            self._jointhread and self._jointhread()

    def cancel_join_thread(self):
        debug('Queue.cancel_join_thread()')
        self._joincancelled = True
        try:
            self._jointhread.cancel()
        except AttributeError:
            pass

    def _start_thread(self):
        debug('Queue._start_thread()')
        self._buffer.clear()
        self._thread = threading.Thread(target=Queue._feed, args=(self._buffer,
         self._notempty,
         self._send,
         self._wlock,
         self._writer.close), name='QueueFeederThread')
        self._thread.daemon = True
        debug('doing self._thread.start()')
        self._thread.start()
        debug('... done self._thread.start()')
        if not self._joincancelled:
            self._jointhread = Finalize(self._thread, Queue._finalize_join, [weakref.ref(self._thread)], exitpriority=-5)
        self._close = Finalize(self, Queue._finalize_close, [self._buffer, self._notempty], exitpriority=10)

    @staticmethod
    def _finalize_join(twr):
        debug('joining queue thread')
        thread = twr()
        if thread is not None:
            thread.join()
            debug('... queue thread joined')
        else:
            debug('... queue thread already dead')
        return

    @staticmethod
    def _finalize_close(buffer, notempty):
        debug('telling queue thread to quit')
        notempty.acquire()
        try:
            buffer.append(_sentinel)
            notempty.notify()
        finally:
            notempty.release()

    @staticmethod
    def _feed--- This code section failed: ---

0	LOAD_GLOBAL       'debug'
3	LOAD_CONST        'starting thread to feed data to pipe'
6	CALL_FUNCTION_1   None
9	POP_TOP           None

10	LOAD_CONST        1
13	LOAD_CONST        ('is_exiting',)
16	IMPORT_NAME       'util'
19	IMPORT_FROM       'is_exiting'
22	STORE_FAST        'is_exiting'
25	POP_TOP           None

26	LOAD_FAST         'notempty'
29	LOAD_ATTR         'acquire'
32	STORE_FAST        'nacquire'

35	LOAD_FAST         'notempty'
38	LOAD_ATTR         'release'
41	STORE_FAST        'nrelease'

44	LOAD_FAST         'notempty'
47	LOAD_ATTR         'wait'
50	STORE_FAST        'nwait'

53	LOAD_FAST         'buffer'
56	LOAD_ATTR         'popleft'
59	STORE_FAST        'bpopleft'

62	LOAD_GLOBAL       '_sentinel'
65	STORE_FAST        'sentinel'

68	LOAD_GLOBAL       'sys'
71	LOAD_ATTR         'platform'
74	LOAD_CONST        'win32'
77	COMPARE_OP        '!='
80	POP_JUMP_IF_FALSE '104'

83	LOAD_FAST         'writelock'
86	LOAD_ATTR         'acquire'
89	STORE_FAST        'wacquire'

92	LOAD_FAST         'writelock'
95	LOAD_ATTR         'release'
98	STORE_FAST        'wrelease'
101	JUMP_FORWARD      '110'

104	LOAD_CONST        None
107	STORE_FAST        'wacquire'
110_0	COME_FROM         '101'

110	SETUP_EXCEPT      '292'

113	SETUP_LOOP        '288'

116	LOAD_FAST         'nacquire'
119	CALL_FUNCTION_0   None
122	POP_TOP           None

123	SETUP_FINALLY     '146'

126	LOAD_FAST         'buffer'
129	POP_JUMP_IF_TRUE  '142'

132	LOAD_FAST         'nwait'
135	CALL_FUNCTION_0   None
138	POP_TOP           None
139	JUMP_FORWARD      '142'
142_0	COME_FROM         '139'
142	POP_BLOCK         None
143	LOAD_CONST        None
146_0	COME_FROM         '123'

146	LOAD_FAST         'nrelease'
149	CALL_FUNCTION_0   None
152	POP_TOP           None
153	END_FINALLY       None

154	SETUP_EXCEPT      '267'

157	SETUP_LOOP        '263'

160	LOAD_FAST         'bpopleft'
163	CALL_FUNCTION_0   None
166	STORE_FAST        'obj'

169	LOAD_FAST         'obj'
172	LOAD_FAST         'sentinel'
175	COMPARE_OP        'is'
178	POP_JUMP_IF_FALSE '202'

181	LOAD_GLOBAL       'debug'
184	LOAD_CONST        'feeder thread got sentinel -- exiting'
187	CALL_FUNCTION_1   None
190	POP_TOP           None

191	LOAD_FAST         'close'
194	CALL_FUNCTION_0   None
197	POP_TOP           None

198	LOAD_CONST        None
201	RETURN_END_IF     None

202	LOAD_FAST         'wacquire'
205	LOAD_CONST        None
208	COMPARE_OP        'is'
211	POP_JUMP_IF_FALSE '227'

214	LOAD_FAST         'send'
217	LOAD_FAST         'obj'
220	CALL_FUNCTION_1   None
223	POP_TOP           None
224	JUMP_BACK         '160'

227	LOAD_FAST         'wacquire'
230	CALL_FUNCTION_0   None
233	POP_TOP           None

234	SETUP_FINALLY     '251'

237	LOAD_FAST         'send'
240	LOAD_FAST         'obj'
243	CALL_FUNCTION_1   None
246	POP_TOP           None
247	POP_BLOCK         None
248	LOAD_CONST        None
251_0	COME_FROM         '234'

251	LOAD_FAST         'wrelease'
254	CALL_FUNCTION_0   None
257	POP_TOP           None
258	END_FINALLY       None
259	JUMP_BACK         '160'
262	POP_BLOCK         None
263_0	COME_FROM         '157'
263	POP_BLOCK         None
264	JUMP_BACK         '116'
267_0	COME_FROM         '154'

267	DUP_TOP           None
268	LOAD_GLOBAL       'IndexError'
271	COMPARE_OP        'exception match'
274	POP_JUMP_IF_FALSE '283'
277	POP_TOP           None
278	POP_TOP           None
279	POP_TOP           None

280	JUMP_BACK         '116'
283	END_FINALLY       None
284_0	COME_FROM         '283'
284	JUMP_BACK         '116'
287	POP_BLOCK         None
288_0	COME_FROM         '113'
288	POP_BLOCK         None
289	JUMP_FORWARD      '382'
292_0	COME_FROM         '110'

292	DUP_TOP           None
293	LOAD_GLOBAL       'Exception'
296	COMPARE_OP        'exception match'
299	POP_JUMP_IF_FALSE '381'
302	POP_TOP           None
303	STORE_FAST        'e'
306	POP_TOP           None

307	SETUP_EXCEPT      '361'

310	LOAD_FAST         'is_exiting'
313	CALL_FUNCTION_0   None
316	POP_JUMP_IF_FALSE '335'

319	LOAD_GLOBAL       'info'
322	LOAD_CONST        'error in queue thread: %s'
325	LOAD_FAST         'e'
328	CALL_FUNCTION_2   None
331	POP_TOP           None
332	JUMP_FORWARD      '357'

335	LOAD_CONST        -1
338	LOAD_CONST        None
341	IMPORT_NAME       'traceback'
344	STORE_FAST        'traceback'

347	LOAD_FAST         'traceback'
350	LOAD_ATTR         'print_exc'
353	CALL_FUNCTION_0   None
356	POP_TOP           None
357_0	COME_FROM         '332'
357	POP_BLOCK         None
358	JUMP_ABSOLUTE     '382'
361_0	COME_FROM         '307'

361	DUP_TOP           None
362	LOAD_GLOBAL       'Exception'
365	COMPARE_OP        'exception match'
368	POP_JUMP_IF_FALSE '377'
371	POP_TOP           None
372	POP_TOP           None
373	POP_TOP           None

374	JUMP_ABSOLUTE     '382'
377	END_FINALLY       None
378_0	COME_FROM         '377'
378	JUMP_FORWARD      '382'
381	END_FINALLY       None
382_0	COME_FROM         '289'
382_1	COME_FROM         '381'
382	LOAD_CONST        None
385	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 262


_sentinel = object()

class JoinableQueue(Queue):

    def __init__(self, maxsize = 0):
        Queue.__init__(self, maxsize)
        self._unfinished_tasks = Semaphore(0)
        self._cond = Condition()

    def __getstate__(self):
        return Queue.__getstate__(self) + (self._cond, self._unfinished_tasks)

    def __setstate__(self, state):
        Queue.__setstate__(self, state[:-2])
        self._cond, self._unfinished_tasks = state[-2:]

    def put(self, obj, block = True, timeout = None):
        if not not self._closed:
            raise AssertionError
            raise self._sem.acquire(block, timeout) or Full
        self._notempty.acquire()
        self._cond.acquire()
        try:
            if self._thread is None:
                self._start_thread()
            self._buffer.append(obj)
            self._unfinished_tasks.release()
            self._notempty.notify()
        finally:
            self._cond.release()
            self._notempty.release()

        return

    def task_done(self):
        self._cond.acquire()
        try:
            if not self._unfinished_tasks.acquire(False):
                raise ValueError('task_done() called too many times')
            if self._unfinished_tasks._semlock._is_zero():
                self._cond.notify_all()
        finally:
            self._cond.release()

    def join(self):
        self._cond.acquire()
        try:
            if not self._unfinished_tasks._semlock._is_zero():
                self._cond.wait()
        finally:
            self._cond.release()


class SimpleQueue(object):

    def __init__(self):
        self._reader, self._writer = Pipe(duplex=False)
        self._rlock = Lock()
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = Lock()
        self._make_methods()
        return

    def empty(self):
        return not self._reader.poll()

    def __getstate__(self):
        assert_spawning(self)
        return (self._reader,
         self._writer,
         self._rlock,
         self._wlock)

    def __setstate__(self, state):
        self._reader, self._writer, self._rlock, self._wlock = state
        self._make_methods()

    def _make_methods(self):
        recv = self._reader.recv
        racquire, rrelease = self._rlock.acquire, self._rlock.release

        def get():
            racquire()
            try:
                return recv()
            finally:
                rrelease()

        self.get = get
        if self._wlock is None:
            self.put = self._writer.send
        else:
            send = self._writer.send
            wacquire, wrelease = self._wlock.acquire, self._wlock.release

            def put(obj):
                wacquire()
                try:
                    return send(obj)
                finally:
                    wrelease()

            self.put = put
        return