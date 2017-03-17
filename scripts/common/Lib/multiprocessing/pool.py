# Embedded file name: scripts/common/Lib/multiprocessing/pool.py
__all__ = ['Pool']
import threading
import Queue
import itertools
import collections
import time
from multiprocessing import Process, cpu_count, TimeoutError
from multiprocessing.util import Finalize, debug
RUN = 0
CLOSE = 1
TERMINATE = 2
job_counter = itertools.count()

def mapstar(args):
    return map(*args)


def worker(inqueue, outqueue, initializer = None, initargs = (), maxtasks = None):
    if not (maxtasks is None or type(maxtasks) == int and maxtasks > 0):
        raise AssertionError
        put = outqueue.put
        get = inqueue.get
        if hasattr(inqueue, '_writer'):
            inqueue._writer.close()
            outqueue._reader.close()
        initializer is not None and initializer(*initargs)
    completed = 0
    while maxtasks is None or maxtasks and completed < maxtasks:
        try:
            task = get()
        except (EOFError, IOError):
            debug('worker got EOFError or IOError -- exiting')
            break

        if task is None:
            debug('worker got sentinel -- exiting')
            break
        job, i, func, args, kwds = task
        try:
            result = (True, func(*args, **kwds))
        except Exception as e:
            result = (False, e)

        put((job, i, result))
        completed += 1

    debug('worker exiting after %d tasks' % completed)
    return


class Pool(object):
    """
    Class which supports an async version of the `apply()` builtin
    """
    Process = Process

    def __init__(self, processes = None, initializer = None, initargs = (), maxtasksperchild = None):
        self._setup_queues()
        self._taskqueue = Queue.Queue()
        self._cache = {}
        self._state = RUN
        self._maxtasksperchild = maxtasksperchild
        self._initializer = initializer
        self._initargs = initargs
        if processes is None:
            try:
                processes = cpu_count()
            except NotImplementedError:
                processes = 1

        if processes < 1:
            raise ValueError('Number of processes must be at least 1')
        if initializer is not None and not hasattr(initializer, '__call__'):
            raise TypeError('initializer must be a callable')
        self._processes = processes
        self._pool = []
        self._repopulate_pool()
        self._worker_handler = threading.Thread(target=Pool._handle_workers, args=(self,))
        self._worker_handler.daemon = True
        self._worker_handler._state = RUN
        self._worker_handler.start()
        self._task_handler = threading.Thread(target=Pool._handle_tasks, args=(self._taskqueue,
         self._quick_put,
         self._outqueue,
         self._pool))
        self._task_handler.daemon = True
        self._task_handler._state = RUN
        self._task_handler.start()
        self._result_handler = threading.Thread(target=Pool._handle_results, args=(self._outqueue, self._quick_get, self._cache))
        self._result_handler.daemon = True
        self._result_handler._state = RUN
        self._result_handler.start()
        self._terminate = Finalize(self, self._terminate_pool, args=(self._taskqueue,
         self._inqueue,
         self._outqueue,
         self._pool,
         self._worker_handler,
         self._task_handler,
         self._result_handler,
         self._cache), exitpriority=15)
        return

    def _join_exited_workers(self):
        """Cleanup after any worker processes which have exited due to reaching
        their specified lifetime.  Returns True if any workers were cleaned up.
        """
        cleaned = False
        for i in reversed(range(len(self._pool))):
            worker = self._pool[i]
            if worker.exitcode is not None:
                debug('cleaning up worker %d' % i)
                worker.join()
                cleaned = True
                del self._pool[i]

        return cleaned

    def _repopulate_pool(self):
        """Bring the number of pool processes up to the specified number,
        for use after reaping workers which have exited.
        """
        for i in range(self._processes - len(self._pool)):
            w = self.Process(target=worker, args=(self._inqueue,
             self._outqueue,
             self._initializer,
             self._initargs,
             self._maxtasksperchild))
            self._pool.append(w)
            w.name = w.name.replace('Process', 'PoolWorker')
            w.daemon = True
            w.start()
            debug('added worker')

    def _maintain_pool(self):
        """Clean up any exited workers and start replacements for them.
        """
        if self._join_exited_workers():
            self._repopulate_pool()

    def _setup_queues(self):
        from .queues import SimpleQueue
        self._inqueue = SimpleQueue()
        self._outqueue = SimpleQueue()
        self._quick_put = self._inqueue._writer.send
        self._quick_get = self._outqueue._reader.recv

    def apply(self, func, args = (), kwds = {}):
        """
        Equivalent of `apply()` builtin
        """
        raise self._state == RUN or AssertionError
        return self.apply_async(func, args, kwds).get()

    def map(self, func, iterable, chunksize = None):
        """
        Equivalent of `map()` builtin
        """
        raise self._state == RUN or AssertionError
        return self.map_async(func, iterable, chunksize).get()

    def imap(self, func, iterable, chunksize = 1):
        """
        Equivalent of `itertools.imap()` -- can be MUCH slower than `Pool.map()`
        """
        if not self._state == RUN:
            raise AssertionError
            result = chunksize == 1 and IMapIterator(self._cache)
            self._taskqueue.put((((result._job,
              i,
              func,
              (x,),
              {}) for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            raise chunksize > 1 or AssertionError
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapIterator(self._cache)
            self._taskqueue.put((((result._job,
              i,
              mapstar,
              (x,),
              {}) for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def imap_unordered(self, func, iterable, chunksize = 1):
        """
        Like `imap()` method but ordering of results is arbitrary
        """
        if not self._state == RUN:
            raise AssertionError
            result = chunksize == 1 and IMapUnorderedIterator(self._cache)
            self._taskqueue.put((((result._job,
              i,
              func,
              (x,),
              {}) for i, x in enumerate(iterable)), result._set_length))
            return result
        else:
            raise chunksize > 1 or AssertionError
            task_batches = Pool._get_tasks(func, iterable, chunksize)
            result = IMapUnorderedIterator(self._cache)
            self._taskqueue.put((((result._job,
              i,
              mapstar,
              (x,),
              {}) for i, x in enumerate(task_batches)), result._set_length))
            return (item for chunk in result for item in chunk)

    def apply_async(self, func, args = (), kwds = {}, callback = None):
        """
        Asynchronous equivalent of `apply()` builtin
        """
        raise self._state == RUN or AssertionError
        result = ApplyResult(self._cache, callback)
        self._taskqueue.put(([(result._job,
           None,
           func,
           args,
           kwds)], None))
        return result

    def map_async(self, func, iterable, chunksize = None, callback = None):
        """
        Asynchronous equivalent of `map()` builtin
        """
        if not self._state == RUN:
            raise AssertionError
            if not hasattr(iterable, '__len__'):
                iterable = list(iterable)
            if chunksize is None:
                chunksize, extra = divmod(len(iterable), len(self._pool) * 4)
                if extra:
                    chunksize += 1
            chunksize = len(iterable) == 0 and 0
        task_batches = Pool._get_tasks(func, iterable, chunksize)
        result = MapResult(self._cache, chunksize, len(iterable), callback)
        self._taskqueue.put((((result._job,
          i,
          mapstar,
          (x,),
          {}) for i, x in enumerate(task_batches)), None))
        return result

    @staticmethod
    def _handle_workers(pool):
        thread = threading.current_thread()
        while thread._state == RUN or pool._cache and thread._state != TERMINATE:
            pool._maintain_pool()
            time.sleep(0.1)

        pool._taskqueue.put(None)
        debug('worker handler exiting')
        return

    @staticmethod
    def _handle_tasks(taskqueue, put, outqueue, pool):
        thread = threading.current_thread()
        for taskseq, set_length in iter(taskqueue.get, None):
            i = -1
            for i, task in enumerate(taskseq):
                if thread._state:
                    debug('task handler found thread._state != RUN')
                    break
                try:
                    put(task)
                except IOError:
                    debug('could not put task on queue')
                    break

            else:
                if set_length:
                    debug('doing set_length()')
                    set_length(i + 1)
                continue

            break
        else:
            debug('task handler got sentinel')

        try:
            debug('task handler sending sentinel to result handler')
            outqueue.put(None)
            debug('task handler sending sentinel to workers')
            for p in pool:
                put(None)

        except IOError:
            debug('task handler got IOError when sending sentinels')

        debug('task handler exiting')
        return

    @staticmethod
    def _handle_results--- This code section failed: ---

0	LOAD_GLOBAL       'threading'
3	LOAD_ATTR         'current_thread'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'thread'

12	SETUP_LOOP        '198'

15	SETUP_EXCEPT      '31'

18	LOAD_FAST         'get'
21	CALL_FUNCTION_0   None
24	STORE_FAST        'task'
27	POP_BLOCK         None
28	JUMP_FORWARD      '65'
31_0	COME_FROM         '15'

31	DUP_TOP           None
32	LOAD_GLOBAL       'IOError'
35	LOAD_GLOBAL       'EOFError'
38	BUILD_TUPLE_2     None
41	COMPARE_OP        'exception match'
44	POP_JUMP_IF_FALSE '64'
47	POP_TOP           None
48	POP_TOP           None
49	POP_TOP           None

50	LOAD_GLOBAL       'debug'
53	LOAD_CONST        'result handler got EOFError/IOError -- exiting'
56	CALL_FUNCTION_1   None
59	POP_TOP           None

60	LOAD_CONST        None
63	RETURN_VALUE      None
64	END_FINALLY       None
65_0	COME_FROM         '28'
65_1	COME_FROM         '64'

65	LOAD_FAST         'thread'
68	LOAD_ATTR         '_state'
71	POP_JUMP_IF_FALSE '109'

74	LOAD_FAST         'thread'
77	LOAD_ATTR         '_state'
80	LOAD_GLOBAL       'TERMINATE'
83	COMPARE_OP        '=='
86	POP_JUMP_IF_TRUE  '95'
89	LOAD_ASSERT       'AssertionError'
92	RAISE_VARARGS_1   None

95	LOAD_GLOBAL       'debug'
98	LOAD_CONST        'result handler found thread._state=TERMINATE'
101	CALL_FUNCTION_1   None
104	POP_TOP           None

105	BREAK_LOOP        None
106	JUMP_FORWARD      '109'
109_0	COME_FROM         '106'

109	LOAD_FAST         'task'
112	LOAD_CONST        None
115	COMPARE_OP        'is'
118	POP_JUMP_IF_FALSE '135'

121	LOAD_GLOBAL       'debug'
124	LOAD_CONST        'result handler got sentinel'
127	CALL_FUNCTION_1   None
130	POP_TOP           None

131	BREAK_LOOP        None
132	JUMP_FORWARD      '135'
135_0	COME_FROM         '132'

135	LOAD_FAST         'task'
138	UNPACK_SEQUENCE_3 None
141	STORE_FAST        'job'
144	STORE_FAST        'i'
147	STORE_FAST        'obj'

150	SETUP_EXCEPT      '177'

153	LOAD_FAST         'cache'
156	LOAD_FAST         'job'
159	BINARY_SUBSCR     None
160	LOAD_ATTR         '_set'
163	LOAD_FAST         'i'
166	LOAD_FAST         'obj'
169	CALL_FUNCTION_2   None
172	POP_TOP           None
173	POP_BLOCK         None
174	JUMP_BACK         '15'
177_0	COME_FROM         '150'

177	DUP_TOP           None
178	LOAD_GLOBAL       'KeyError'
181	COMPARE_OP        'exception match'
184	POP_JUMP_IF_FALSE '193'
187	POP_TOP           None
188	POP_TOP           None
189	POP_TOP           None

190	JUMP_BACK         '15'
193	END_FINALLY       None
194_0	COME_FROM         '193'
194	JUMP_BACK         '15'
197	POP_BLOCK         None
198_0	COME_FROM         '12'

198	SETUP_LOOP        '363'
201	LOAD_FAST         'cache'
204	POP_JUMP_IF_FALSE '362'
207	LOAD_FAST         'thread'
210	LOAD_ATTR         '_state'
213	LOAD_GLOBAL       'TERMINATE'
216	COMPARE_OP        '!='
219_0	COME_FROM         '204'
219	POP_JUMP_IF_FALSE '362'

222	SETUP_EXCEPT      '238'

225	LOAD_FAST         'get'
228	CALL_FUNCTION_0   None
231	STORE_FAST        'task'
234	POP_BLOCK         None
235	JUMP_FORWARD      '272'
238_0	COME_FROM         '222'

238	DUP_TOP           None
239	LOAD_GLOBAL       'IOError'
242	LOAD_GLOBAL       'EOFError'
245	BUILD_TUPLE_2     None
248	COMPARE_OP        'exception match'
251	POP_JUMP_IF_FALSE '271'
254	POP_TOP           None
255	POP_TOP           None
256	POP_TOP           None

257	LOAD_GLOBAL       'debug'
260	LOAD_CONST        'result handler got EOFError/IOError -- exiting'
263	CALL_FUNCTION_1   None
266	POP_TOP           None

267	LOAD_CONST        None
270	RETURN_VALUE      None
271	END_FINALLY       None
272_0	COME_FROM         '235'
272_1	COME_FROM         '271'

272	LOAD_FAST         'task'
275	LOAD_CONST        None
278	COMPARE_OP        'is'
281	POP_JUMP_IF_FALSE '300'

284	LOAD_GLOBAL       'debug'
287	LOAD_CONST        'result handler ignoring extra sentinel'
290	CALL_FUNCTION_1   None
293	POP_TOP           None

294	CONTINUE          '201'
297	JUMP_FORWARD      '300'
300_0	COME_FROM         '297'

300	LOAD_FAST         'task'
303	UNPACK_SEQUENCE_3 None
306	STORE_FAST        'job'
309	STORE_FAST        'i'
312	STORE_FAST        'obj'

315	SETUP_EXCEPT      '342'

318	LOAD_FAST         'cache'
321	LOAD_FAST         'job'
324	BINARY_SUBSCR     None
325	LOAD_ATTR         '_set'
328	LOAD_FAST         'i'
331	LOAD_FAST         'obj'
334	CALL_FUNCTION_2   None
337	POP_TOP           None
338	POP_BLOCK         None
339	JUMP_BACK         '201'
342_0	COME_FROM         '315'

342	DUP_TOP           None
343	LOAD_GLOBAL       'KeyError'
346	COMPARE_OP        'exception match'
349	POP_JUMP_IF_FALSE '358'
352	POP_TOP           None
353	POP_TOP           None
354	POP_TOP           None

355	JUMP_BACK         '201'
358	END_FINALLY       None
359_0	COME_FROM         '358'
359	JUMP_BACK         '201'
362	POP_BLOCK         None
363_0	COME_FROM         '198'

363	LOAD_GLOBAL       'hasattr'
366	LOAD_FAST         'outqueue'
369	LOAD_CONST        '_reader'
372	CALL_FUNCTION_2   None
375	POP_JUMP_IF_FALSE '470'

378	LOAD_GLOBAL       'debug'
381	LOAD_CONST        'ensuring that outqueue is not full'
384	CALL_FUNCTION_1   None
387	POP_TOP           None

388	SETUP_EXCEPT      '444'

391	SETUP_LOOP        '440'
394	LOAD_GLOBAL       'range'
397	LOAD_CONST        10
400	CALL_FUNCTION_1   None
403	GET_ITER          None
404	FOR_ITER          '439'
407	STORE_FAST        'i'

410	LOAD_FAST         'outqueue'
413	LOAD_ATTR         '_reader'
416	LOAD_ATTR         'poll'
419	CALL_FUNCTION_0   None
422	POP_JUMP_IF_TRUE  '429'

425	BREAK_LOOP        None
426	JUMP_FORWARD      '429'
429_0	COME_FROM         '426'

429	LOAD_FAST         'get'
432	CALL_FUNCTION_0   None
435	POP_TOP           None
436	JUMP_BACK         '404'
439	POP_BLOCK         None
440_0	COME_FROM         '391'
440	POP_BLOCK         None
441	JUMP_ABSOLUTE     '470'
444_0	COME_FROM         '388'

444	DUP_TOP           None
445	LOAD_GLOBAL       'IOError'
448	LOAD_GLOBAL       'EOFError'
451	BUILD_TUPLE_2     None
454	COMPARE_OP        'exception match'
457	POP_JUMP_IF_FALSE '466'
460	POP_TOP           None
461	POP_TOP           None
462	POP_TOP           None

463	JUMP_ABSOLUTE     '470'
466	END_FINALLY       None
467_0	COME_FROM         '466'
467	JUMP_FORWARD      '470'
470_0	COME_FROM         '467'

470	LOAD_GLOBAL       'debug'
473	LOAD_CONST        'result handler exiting: len(cache)=%s, thread._state=%s'

476	LOAD_GLOBAL       'len'
479	LOAD_FAST         'cache'
482	CALL_FUNCTION_1   None
485	LOAD_FAST         'thread'
488	LOAD_ATTR         '_state'
491	CALL_FUNCTION_3   None
494	POP_TOP           None
495	LOAD_CONST        None
498	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 197

    @staticmethod
    def _get_tasks--- This code section failed: ---

0	LOAD_GLOBAL       'iter'
3	LOAD_FAST         'it'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'it'

12	SETUP_LOOP        '64'

15	LOAD_GLOBAL       'tuple'
18	LOAD_GLOBAL       'itertools'
21	LOAD_ATTR         'islice'
24	LOAD_FAST         'it'
27	LOAD_FAST         'size'
30	CALL_FUNCTION_2   None
33	CALL_FUNCTION_1   None
36	STORE_FAST        'x'

39	LOAD_FAST         'x'
42	POP_JUMP_IF_TRUE  '49'

45	LOAD_CONST        None
48	RETURN_END_IF     None

49	LOAD_FAST         'func'
52	LOAD_FAST         'x'
55	BUILD_TUPLE_2     None
58	YIELD_VALUE       None
59	POP_TOP           None
60	JUMP_BACK         '15'
63	POP_BLOCK         None
64_0	COME_FROM         '12'

Syntax error at or near `POP_BLOCK' token at offset 63

    def __reduce__(self):
        raise NotImplementedError('pool objects cannot be passed between processes or pickled')

    def close(self):
        debug('closing pool')
        if self._state == RUN:
            self._state = CLOSE
            self._worker_handler._state = CLOSE

    def terminate(self):
        debug('terminating pool')
        self._state = TERMINATE
        self._worker_handler._state = TERMINATE
        self._terminate()

    def join(self):
        debug('joining pool')
        raise self._state in (CLOSE, TERMINATE) or AssertionError
        self._worker_handler.join()
        self._task_handler.join()
        self._result_handler.join()
        for p in self._pool:
            p.join()

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        debug('removing tasks from inqueue until task handler finished')
        inqueue._rlock.acquire()
        while task_handler.is_alive() and inqueue._reader.poll():
            inqueue._reader.recv()
            time.sleep(0)

    @classmethod
    def _terminate_pool(cls, taskqueue, inqueue, outqueue, pool, worker_handler, task_handler, result_handler, cache):
        debug('finalizing pool')
        worker_handler._state = TERMINATE
        task_handler._state = TERMINATE
        debug('helping task handler/workers to finish')
        cls._help_stuff_finish(inqueue, task_handler, len(pool))
        if not (result_handler.is_alive() or len(cache) == 0):
            raise AssertionError
            result_handler._state = TERMINATE
            outqueue.put(None)
            debug('joining worker handler')
            worker_handler.join()
            if pool and hasattr(pool[0], 'terminate'):
                debug('terminating workers')
                for p in pool:
                    if p.exitcode is None:
                        p.terminate()

            debug('joining task handler')
            task_handler.join(1e+100)
            debug('joining result handler')
            result_handler.join(1e+100)
            pool and hasattr(pool[0], 'terminate') and debug('joining pool workers')
            for p in pool:
                if p.is_alive():
                    debug('cleaning up worker %d' % p.pid)
                    p.join()

        return


class ApplyResult(object):

    def __init__(self, cache, callback):
        self._cond = threading.Condition(threading.Lock())
        self._job = job_counter.next()
        self._cache = cache
        self._ready = False
        self._callback = callback
        cache[self._job] = self

    def ready(self):
        return self._ready

    def successful(self):
        raise self._ready or AssertionError
        return self._success

    def wait(self, timeout = None):
        self._cond.acquire()
        try:
            if not self._ready:
                self._cond.wait(timeout)
        finally:
            self._cond.release()

    def get(self, timeout = None):
        self.wait(timeout)
        if not self._ready:
            raise TimeoutError
        if self._success:
            return self._value
        raise self._value

    def _set(self, i, obj):
        self._success, self._value = obj
        if self._callback and self._success:
            self._callback(self._value)
        self._cond.acquire()
        try:
            self._ready = True
            self._cond.notify()
        finally:
            self._cond.release()

        del self._cache[self._job]


class MapResult(ApplyResult):

    def __init__(self, cache, chunksize, length, callback):
        ApplyResult.__init__(self, cache, callback)
        self._success = True
        self._value = [None] * length
        self._chunksize = chunksize
        if chunksize <= 0:
            self._number_left = 0
            self._ready = True
        else:
            self._number_left = length // chunksize + bool(length % chunksize)
        return

    def _set(self, i, success_result):
        success, result = success_result
        if success:
            self._value[i * self._chunksize:(i + 1) * self._chunksize] = result
            self._number_left -= 1
            if self._number_left == 0:
                if self._callback:
                    self._callback(self._value)
                del self._cache[self._job]
                self._cond.acquire()
                try:
                    self._ready = True
                    self._cond.notify()
                finally:
                    self._cond.release()

        else:
            self._success = False
            self._value = result
            del self._cache[self._job]
            self._cond.acquire()
            try:
                self._ready = True
                self._cond.notify()
            finally:
                self._cond.release()


class IMapIterator(object):

    def __init__(self, cache):
        self._cond = threading.Condition(threading.Lock())
        self._job = job_counter.next()
        self._cache = cache
        self._items = collections.deque()
        self._index = 0
        self._length = None
        self._unsorted = {}
        cache[self._job] = self
        return

    def __iter__(self):
        return self

    def next(self, timeout = None):
        self._cond.acquire()
        try:
            item = self._items.popleft()
        except IndexError:
            if self._index == self._length:
                raise StopIteration
            self._cond.wait(timeout)
            try:
                item = self._items.popleft()
            except IndexError:
                if self._index == self._length:
                    raise StopIteration
                raise TimeoutError

        finally:
            self._cond.release()

        success, value = item
        if success:
            return value
        raise value

    __next__ = next

    def _set(self, i, obj):
        self._cond.acquire()
        try:
            if self._index == i:
                self._items.append(obj)
                self._index += 1
                while self._index in self._unsorted:
                    obj = self._unsorted.pop(self._index)
                    self._items.append(obj)
                    self._index += 1

                self._cond.notify()
            else:
                self._unsorted[i] = obj
            if self._index == self._length:
                del self._cache[self._job]
        finally:
            self._cond.release()

    def _set_length(self, length):
        self._cond.acquire()
        try:
            self._length = length
            if self._index == self._length:
                self._cond.notify()
                del self._cache[self._job]
        finally:
            self._cond.release()


class IMapUnorderedIterator(IMapIterator):

    def _set(self, i, obj):
        self._cond.acquire()
        try:
            self._items.append(obj)
            self._index += 1
            self._cond.notify()
            if self._index == self._length:
                del self._cache[self._job]
        finally:
            self._cond.release()


class ThreadPool(Pool):
    from .dummy import Process

    def __init__(self, processes = None, initializer = None, initargs = ()):
        Pool.__init__(self, processes, initializer, initargs)

    def _setup_queues(self):
        self._inqueue = Queue.Queue()
        self._outqueue = Queue.Queue()
        self._quick_put = self._inqueue.put
        self._quick_get = self._outqueue.get

    @staticmethod
    def _help_stuff_finish(inqueue, task_handler, size):
        inqueue.not_empty.acquire()
        try:
            inqueue.queue.clear()
            inqueue.queue.extend([None] * size)
            inqueue.not_empty.notify_all()
        finally:
            inqueue.not_empty.release()

        return