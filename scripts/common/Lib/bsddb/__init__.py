# Embedded file name: scripts/common/Lib/bsddb/__init__.py
"""Support for Berkeley DB 4.1 through 4.8 with a simple interface.

For the full featured object oriented interface use the bsddb.db module
instead.  It mirrors the Oracle Berkeley DB C API.
"""
import sys
absolute_import = sys.version_info[0] >= 3
if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
    import warnings
    if sys.py3kwarning and __name__ != 'bsddb3':
        warnings.warnpy3k('in 3.x, the bsddb module has been removed; please use the pybsddb project instead', DeprecationWarning, 2)
    warnings.filterwarnings('ignore', '.*CObject.*', DeprecationWarning, 'bsddb.__init__')
try:
    if __name__ == 'bsddb3':
        if absolute_import:
            exec 'from . import _pybsddb'
        else:
            import _pybsddb
        _bsddb = _pybsddb
        from bsddb3.dbutils import DeadlockWrap as _DeadlockWrap
    else:
        import _bsddb
        from bsddb.dbutils import DeadlockWrap as _DeadlockWrap
except ImportError:
    import sys
    del sys.modules[__name__]
    raise

db = _db = _bsddb
__version__ = db.__version__
error = db.DBError
import sys, os
from weakref import ref
if sys.version_info < (2, 6):
    import UserDict
    MutableMapping = UserDict.DictMixin
else:
    import collections
    MutableMapping = collections.MutableMapping

class _iter_mixin(MutableMapping):

    def _make_iter_cursor(self):
        cur = _DeadlockWrap(self.db.cursor)
        key = id(cur)
        self._cursor_refs[key] = ref(cur, self._gen_cref_cleaner(key))
        return cur

    def _gen_cref_cleaner(self, key):
        return lambda ref: self._cursor_refs.pop(key, None)

    def __iter__--- This code section failed: ---

0	LOAD_GLOBAL       'False'
3	LOAD_FAST         'self'
6	STORE_ATTR        '_kill_iteration'

9	LOAD_FAST         'self'
12	DUP_TOP           None
13	LOAD_ATTR         '_in_iter'
16	LOAD_CONST        1
19	INPLACE_ADD       None
20	ROT_TWO           None
21	STORE_ATTR        '_in_iter'

24	SETUP_EXCEPT      '277'

27	SETUP_EXCEPT      '234'

30	LOAD_FAST         'self'
33	LOAD_ATTR         '_make_iter_cursor'
36	CALL_FUNCTION_0   None
39	STORE_FAST        'cur'

42	LOAD_GLOBAL       '_DeadlockWrap'
45	LOAD_FAST         'cur'
48	LOAD_ATTR         'first'
51	LOAD_CONST        0
54	LOAD_CONST        0
57	LOAD_CONST        0
60	CALL_FUNCTION_4   None
63	LOAD_CONST        0
66	BINARY_SUBSCR     None
67	STORE_FAST        'key'

70	LOAD_FAST         'key'
73	YIELD_VALUE       None
74	POP_TOP           None

75	LOAD_GLOBAL       'getattr'
78	LOAD_FAST         'cur'
81	LOAD_CONST        'next'
84	CALL_FUNCTION_2   None
87	STORE_FAST        'next'

90	SETUP_LOOP        '230'

93	SETUP_EXCEPT      '130'

96	LOAD_GLOBAL       '_DeadlockWrap'
99	LOAD_FAST         'next'
102	LOAD_CONST        0
105	LOAD_CONST        0
108	LOAD_CONST        0
111	CALL_FUNCTION_4   None
114	LOAD_CONST        0
117	BINARY_SUBSCR     None
118	STORE_FAST        'key'

121	LOAD_FAST         'key'
124	YIELD_VALUE       None
125	POP_TOP           None
126	POP_BLOCK         None
127	JUMP_BACK         '93'
130_0	COME_FROM         '93'

130	DUP_TOP           None
131	LOAD_GLOBAL       '_bsddb'
134	LOAD_ATTR         'DBCursorClosedError'
137	COMPARE_OP        'exception match'
140	POP_JUMP_IF_FALSE '225'
143	POP_TOP           None
144	POP_TOP           None
145	POP_TOP           None

146	LOAD_FAST         'self'
149	LOAD_ATTR         '_kill_iteration'
152	POP_JUMP_IF_FALSE '170'

155	LOAD_GLOBAL       'RuntimeError'
158	LOAD_CONST        'Database changed size during iteration.'
161	CALL_FUNCTION_1   None
164	RAISE_VARARGS_1   None
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	LOAD_FAST         'self'
173	LOAD_ATTR         '_make_iter_cursor'
176	CALL_FUNCTION_0   None
179	STORE_FAST        'cur'

182	LOAD_GLOBAL       '_DeadlockWrap'
185	LOAD_FAST         'cur'
188	LOAD_ATTR         'set'
191	LOAD_FAST         'key'
194	LOAD_CONST        0
197	LOAD_CONST        0
200	LOAD_CONST        0
203	CALL_FUNCTION_5   None
206	POP_TOP           None

207	LOAD_GLOBAL       'getattr'
210	LOAD_FAST         'cur'
213	LOAD_CONST        'next'
216	CALL_FUNCTION_2   None
219	STORE_FAST        'next'
222	JUMP_BACK         '93'
225	END_FINALLY       None
226_0	COME_FROM         '225'
226	JUMP_BACK         '93'
229	POP_BLOCK         None
230_0	COME_FROM         '90'
230	POP_BLOCK         None
231	JUMP_FORWARD      '273'
234_0	COME_FROM         '27'

234	DUP_TOP           None
235	LOAD_GLOBAL       '_bsddb'
238	LOAD_ATTR         'DBNotFoundError'
241	COMPARE_OP        'exception match'
244	POP_JUMP_IF_FALSE '253'
247	POP_TOP           None
248	POP_TOP           None
249	POP_TOP           None

250	JUMP_FORWARD      '273'

253	DUP_TOP           None
254	LOAD_GLOBAL       '_bsddb'
257	LOAD_ATTR         'DBCursorClosedError'
260	COMPARE_OP        'exception match'
263	POP_JUMP_IF_FALSE '272'
266	POP_TOP           None
267	POP_TOP           None
268	POP_TOP           None

269	JUMP_FORWARD      '273'
272	END_FINALLY       None
273_0	COME_FROM         '231'
273_1	COME_FROM         '272'
273	POP_BLOCK         None
274	JUMP_FORWARD      '302'
277_0	COME_FROM         '24'

277	POP_TOP           None
278	POP_TOP           None
279	POP_TOP           None

280	LOAD_FAST         'self'
283	DUP_TOP           None
284	LOAD_ATTR         '_in_iter'
287	LOAD_CONST        1
290	INPLACE_SUBTRACT  None
291	ROT_TWO           None
292	STORE_ATTR        '_in_iter'

295	RAISE_VARARGS_0   None
298	JUMP_FORWARD      '302'
301	END_FINALLY       None
302_0	COME_FROM         '274'
302_1	COME_FROM         '301'

302	LOAD_FAST         'self'
305	DUP_TOP           None
306	LOAD_ATTR         '_in_iter'
309	LOAD_CONST        1
312	INPLACE_SUBTRACT  None
313	ROT_TWO           None
314	STORE_ATTR        '_in_iter'

Syntax error at or near `POP_BLOCK' token at offset 229

    def iteritems--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'db'
6	POP_JUMP_IF_TRUE  '13'

9	LOAD_CONST        None
12	RETURN_END_IF     None

13	LOAD_GLOBAL       'False'
16	LOAD_FAST         'self'
19	STORE_ATTR        '_kill_iteration'

22	LOAD_FAST         'self'
25	DUP_TOP           None
26	LOAD_ATTR         '_in_iter'
29	LOAD_CONST        1
32	INPLACE_ADD       None
33	ROT_TWO           None
34	STORE_ATTR        '_in_iter'

37	SETUP_EXCEPT      '284'

40	SETUP_EXCEPT      '241'

43	LOAD_FAST         'self'
46	LOAD_ATTR         '_make_iter_cursor'
49	CALL_FUNCTION_0   None
52	STORE_FAST        'cur'

55	LOAD_GLOBAL       '_DeadlockWrap'
58	LOAD_FAST         'cur'
61	LOAD_ATTR         'first'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'kv'

70	LOAD_FAST         'kv'
73	LOAD_CONST        0
76	BINARY_SUBSCR     None
77	STORE_FAST        'key'

80	LOAD_FAST         'kv'
83	YIELD_VALUE       None
84	POP_TOP           None

85	LOAD_GLOBAL       'getattr'
88	LOAD_FAST         'cur'
91	LOAD_CONST        'next'
94	CALL_FUNCTION_2   None
97	STORE_FAST        'next'

100	SETUP_LOOP        '237'

103	SETUP_EXCEPT      '137'

106	LOAD_GLOBAL       '_DeadlockWrap'
109	LOAD_FAST         'next'
112	CALL_FUNCTION_1   None
115	STORE_FAST        'kv'

118	LOAD_FAST         'kv'
121	LOAD_CONST        0
124	BINARY_SUBSCR     None
125	STORE_FAST        'key'

128	LOAD_FAST         'kv'
131	YIELD_VALUE       None
132	POP_TOP           None
133	POP_BLOCK         None
134	JUMP_BACK         '103'
137_0	COME_FROM         '103'

137	DUP_TOP           None
138	LOAD_GLOBAL       '_bsddb'
141	LOAD_ATTR         'DBCursorClosedError'
144	COMPARE_OP        'exception match'
147	POP_JUMP_IF_FALSE '232'
150	POP_TOP           None
151	POP_TOP           None
152	POP_TOP           None

153	LOAD_FAST         'self'
156	LOAD_ATTR         '_kill_iteration'
159	POP_JUMP_IF_FALSE '177'

162	LOAD_GLOBAL       'RuntimeError'
165	LOAD_CONST        'Database changed size during iteration.'
168	CALL_FUNCTION_1   None
171	RAISE_VARARGS_1   None
174	JUMP_FORWARD      '177'
177_0	COME_FROM         '174'

177	LOAD_FAST         'self'
180	LOAD_ATTR         '_make_iter_cursor'
183	CALL_FUNCTION_0   None
186	STORE_FAST        'cur'

189	LOAD_GLOBAL       '_DeadlockWrap'
192	LOAD_FAST         'cur'
195	LOAD_ATTR         'set'
198	LOAD_FAST         'key'
201	LOAD_CONST        0
204	LOAD_CONST        0
207	LOAD_CONST        0
210	CALL_FUNCTION_5   None
213	POP_TOP           None

214	LOAD_GLOBAL       'getattr'
217	LOAD_FAST         'cur'
220	LOAD_CONST        'next'
223	CALL_FUNCTION_2   None
226	STORE_FAST        'next'
229	JUMP_BACK         '103'
232	END_FINALLY       None
233_0	COME_FROM         '232'
233	JUMP_BACK         '103'
236	POP_BLOCK         None
237_0	COME_FROM         '100'
237	POP_BLOCK         None
238	JUMP_FORWARD      '280'
241_0	COME_FROM         '40'

241	DUP_TOP           None
242	LOAD_GLOBAL       '_bsddb'
245	LOAD_ATTR         'DBNotFoundError'
248	COMPARE_OP        'exception match'
251	POP_JUMP_IF_FALSE '260'
254	POP_TOP           None
255	POP_TOP           None
256	POP_TOP           None

257	JUMP_FORWARD      '280'

260	DUP_TOP           None
261	LOAD_GLOBAL       '_bsddb'
264	LOAD_ATTR         'DBCursorClosedError'
267	COMPARE_OP        'exception match'
270	POP_JUMP_IF_FALSE '279'
273	POP_TOP           None
274	POP_TOP           None
275	POP_TOP           None

276	JUMP_FORWARD      '280'
279	END_FINALLY       None
280_0	COME_FROM         '238'
280_1	COME_FROM         '279'
280	POP_BLOCK         None
281	JUMP_FORWARD      '309'
284_0	COME_FROM         '37'

284	POP_TOP           None
285	POP_TOP           None
286	POP_TOP           None

287	LOAD_FAST         'self'
290	DUP_TOP           None
291	LOAD_ATTR         '_in_iter'
294	LOAD_CONST        1
297	INPLACE_SUBTRACT  None
298	ROT_TWO           None
299	STORE_ATTR        '_in_iter'

302	RAISE_VARARGS_0   None
305	JUMP_FORWARD      '309'
308	END_FINALLY       None
309_0	COME_FROM         '281'
309_1	COME_FROM         '308'

309	LOAD_FAST         'self'
312	DUP_TOP           None
313	LOAD_ATTR         '_in_iter'
316	LOAD_CONST        1
319	INPLACE_SUBTRACT  None
320	ROT_TWO           None
321	STORE_ATTR        '_in_iter'

Syntax error at or near `POP_BLOCK' token at offset 236


class _DBWithCursor(_iter_mixin):
    """
    A simple wrapper around DB that makes it look like the bsddbobject in
    the old module.  It uses a cursor as needed to provide DB traversal.
    """

    def __init__(self, db):
        self.db = db
        self.db.set_get_returns_none(0)
        self.dbc = None
        self.saved_dbc_key = None
        self._cursor_refs = {}
        self._in_iter = 0
        self._kill_iteration = False
        return

    def __del__(self):
        self.close()

    def _checkCursor(self):
        if self.dbc is None:
            self.dbc = _DeadlockWrap(self.db.cursor)
            if self.saved_dbc_key is not None:
                _DeadlockWrap(self.dbc.set, self.saved_dbc_key)
                self.saved_dbc_key = None
        return

    def _closeCursors(self, save = 1):
        if self.dbc:
            c = self.dbc
            self.dbc = None
            if save:
                try:
                    self.saved_dbc_key = _DeadlockWrap(c.current, 0, 0, 0)[0]
                except db.DBError:
                    pass

            _DeadlockWrap(c.close)
            del c
        for cref in self._cursor_refs.values():
            c = cref()
            if c is not None:
                _DeadlockWrap(c.close)

        return

    def _checkOpen(self):
        if self.db is None:
            raise error, 'BSDDB object has already been closed'
        return

    def isOpen(self):
        return self.db is not None

    def __len__(self):
        self._checkOpen()
        return _DeadlockWrap(lambda : len(self.db))

    if sys.version_info >= (2, 6):

        def __repr__(self):
            if self.isOpen():
                return repr(dict(_DeadlockWrap(self.db.items)))
            return repr(dict())

    def __getitem__(self, key):
        self._checkOpen()
        return _DeadlockWrap(lambda : self.db[key])

    def __setitem__(self, key, value):
        self._checkOpen()
        self._closeCursors()
        if self._in_iter and key not in self:
            self._kill_iteration = True

        def wrapF():
            self.db[key] = value

        _DeadlockWrap(wrapF)

    def __delitem__(self, key):
        self._checkOpen()
        self._closeCursors()
        if self._in_iter and key in self:
            self._kill_iteration = True

        def wrapF():
            del self.db[key]

        _DeadlockWrap(wrapF)

    def close(self):
        self._closeCursors(save=0)
        if self.dbc is not None:
            _DeadlockWrap(self.dbc.close)
        v = 0
        if self.db is not None:
            v = _DeadlockWrap(self.db.close)
        self.dbc = None
        self.db = None
        return v

    def keys(self):
        self._checkOpen()
        return _DeadlockWrap(self.db.keys)

    def has_key(self, key):
        self._checkOpen()
        return _DeadlockWrap(self.db.has_key, key)

    def set_location(self, key):
        self._checkOpen()
        self._checkCursor()
        return _DeadlockWrap(self.dbc.set_range, key)

    def next(self):
        self._checkOpen()
        self._checkCursor()
        rv = _DeadlockWrap(getattr(self.dbc, 'next'))
        return rv

    if sys.version_info[0] >= 3:
        next = __next__

    def previous(self):
        self._checkOpen()
        self._checkCursor()
        rv = _DeadlockWrap(self.dbc.prev)
        return rv

    def first(self):
        self._checkOpen()
        self.saved_dbc_key = None
        self._checkCursor()
        rv = _DeadlockWrap(self.dbc.first)
        return rv

    def last(self):
        self._checkOpen()
        self.saved_dbc_key = None
        self._checkCursor()
        rv = _DeadlockWrap(self.dbc.last)
        return rv

    def sync(self):
        self._checkOpen()
        return _DeadlockWrap(self.db.sync)


def hashopen(file, flag = 'c', mode = 438, pgsize = None, ffactor = None, nelem = None, cachesize = None, lorder = None, hflags = 0):
    flags = _checkflag(flag, file)
    e = _openDBEnv(cachesize)
    d = db.DB(e)
    d.set_flags(hflags)
    if pgsize is not None:
        d.set_pagesize(pgsize)
    if lorder is not None:
        d.set_lorder(lorder)
    if ffactor is not None:
        d.set_h_ffactor(ffactor)
    if nelem is not None:
        d.set_h_nelem(nelem)
    d.open(file, db.DB_HASH, flags, mode)
    return _DBWithCursor(d)


def btopen(file, flag = 'c', mode = 438, btflags = 0, cachesize = None, maxkeypage = None, minkeypage = None, pgsize = None, lorder = None):
    flags = _checkflag(flag, file)
    e = _openDBEnv(cachesize)
    d = db.DB(e)
    if pgsize is not None:
        d.set_pagesize(pgsize)
    if lorder is not None:
        d.set_lorder(lorder)
    d.set_flags(btflags)
    if minkeypage is not None:
        d.set_bt_minkey(minkeypage)
    if maxkeypage is not None:
        d.set_bt_maxkey(maxkeypage)
    d.open(file, db.DB_BTREE, flags, mode)
    return _DBWithCursor(d)


def rnopen(file, flag = 'c', mode = 438, rnflags = 0, cachesize = None, pgsize = None, lorder = None, rlen = None, delim = None, source = None, pad = None):
    flags = _checkflag(flag, file)
    e = _openDBEnv(cachesize)
    d = db.DB(e)
    if pgsize is not None:
        d.set_pagesize(pgsize)
    if lorder is not None:
        d.set_lorder(lorder)
    d.set_flags(rnflags)
    if delim is not None:
        d.set_re_delim(delim)
    if rlen is not None:
        d.set_re_len(rlen)
    if source is not None:
        d.set_re_source(source)
    if pad is not None:
        d.set_re_pad(pad)
    d.open(file, db.DB_RECNO, flags, mode)
    return _DBWithCursor(d)


def _openDBEnv(cachesize):
    e = db.DBEnv()
    if cachesize is not None:
        if cachesize >= 20480:
            e.set_cachesize(0, cachesize)
        else:
            raise error, 'cachesize must be >= 20480'
    e.set_lk_detect(db.DB_LOCK_DEFAULT)
    e.open('.', db.DB_PRIVATE | db.DB_CREATE | db.DB_THREAD | db.DB_INIT_LOCK | db.DB_INIT_MPOOL)
    return e


def _checkflag(flag, file):
    if flag == 'r':
        flags = db.DB_RDONLY
    elif flag == 'rw':
        flags = 0
    elif flag == 'w':
        flags = db.DB_CREATE
    elif flag == 'c':
        flags = db.DB_CREATE
    elif flag == 'n':
        flags = db.DB_CREATE
        if file is not None and os.path.isfile(file):
            os.unlink(file)
    else:
        raise error, "flags should be one of 'r', 'w', 'c' or 'n'"
    return flags | db.DB_THREAD


try:
    import thread as T
    del T
except ImportError:
    db.DB_THREAD = 0