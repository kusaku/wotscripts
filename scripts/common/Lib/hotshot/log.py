# Embedded file name: scripts/common/Lib/hotshot/log.py
import _hotshot
import os.path
import parser
import symbol
from _hotshot import WHAT_ENTER, WHAT_EXIT, WHAT_LINENO, WHAT_DEFINE_FILE, WHAT_DEFINE_FUNC, WHAT_ADD_INFO
__all__ = ['LogReader',
 'ENTER',
 'EXIT',
 'LINE']
ENTER = WHAT_ENTER
EXIT = WHAT_EXIT
LINE = WHAT_LINENO

class LogReader:

    def __init__(self, logfn):
        self._filemap = {}
        self._funcmap = {}
        self._reader = _hotshot.logreader(logfn)
        self._nextitem = self._reader.next
        self._info = self._reader.info
        if 'current-directory' in self._info:
            self.cwd = self._info['current-directory']
        else:
            self.cwd = None
        self._stack = []
        self._append = self._stack.append
        self._pop = self._stack.pop
        return

    def close(self):
        self._reader.close()

    def fileno(self):
        """Return the file descriptor of the log reader's log file."""
        return self._reader.fileno()

    def addinfo(self, key, value):
        """This method is called for each additional ADD_INFO record.
        
        This can be overridden by applications that want to receive
        these events.  The default implementation does not need to be
        called by alternate implementations.
        
        The initial set of ADD_INFO records do not pass through this
        mechanism; this is only needed to receive notification when
        new values are added.  Subclasses can inspect self._info after
        calling LogReader.__init__().
        """
        pass

    def get_filename(self, fileno):
        try:
            return self._filemap[fileno]
        except KeyError:
            raise ValueError, 'unknown fileno'

    def get_filenames(self):
        return self._filemap.values()

    def get_fileno(self, filename):
        filename = os.path.normcase(os.path.normpath(filename))
        for fileno, name in self._filemap.items():
            if name == filename:
                return fileno

        raise ValueError, 'unknown filename'

    def get_funcname(self, fileno, lineno):
        try:
            return self._funcmap[fileno, lineno]
        except KeyError:
            raise ValueError, 'unknown function location'

    def next--- This code section failed: ---

0	SETUP_LOOP        '403'

3	LOAD_FAST         'self'
6	LOAD_ATTR         '_nextitem'
9	CALL_FUNCTION_0   None
12	UNPACK_SEQUENCE_4 None
15	STORE_FAST        'what'
18	STORE_FAST        'tdelta'
21	STORE_FAST        'fileno'
24	STORE_FAST        'lineno'

27	LOAD_FAST         'what'
30	LOAD_GLOBAL       'WHAT_ENTER'
33	COMPARE_OP        '=='
36	POP_JUMP_IF_FALSE '104'

39	LOAD_FAST         'self'
42	LOAD_ATTR         '_decode_location'
45	LOAD_FAST         'fileno'
48	LOAD_FAST         'lineno'
51	CALL_FUNCTION_2   None
54	UNPACK_SEQUENCE_2 None
57	STORE_FAST        'filename'
60	STORE_FAST        'funcname'

63	LOAD_FAST         'filename'
66	LOAD_FAST         'lineno'
69	LOAD_FAST         'funcname'
72	BUILD_TUPLE_3     None
75	STORE_FAST        't'

78	LOAD_FAST         'self'
81	LOAD_ATTR         '_append'
84	LOAD_FAST         't'
87	CALL_FUNCTION_1   None
90	POP_TOP           None

91	LOAD_FAST         'what'
94	LOAD_FAST         't'
97	LOAD_FAST         'tdelta'
100	BUILD_TUPLE_3     None
103	RETURN_END_IF     None

104	LOAD_FAST         'what'
107	LOAD_GLOBAL       'WHAT_EXIT'
110	COMPARE_OP        '=='
113	POP_JUMP_IF_FALSE '168'

116	SETUP_EXCEPT      '142'

119	LOAD_FAST         'what'
122	LOAD_FAST         'self'
125	LOAD_ATTR         '_pop'
128	CALL_FUNCTION_0   None
131	LOAD_FAST         'tdelta'
134	BUILD_TUPLE_3     None
137	RETURN_VALUE      None
138	POP_BLOCK         None
139	JUMP_ABSOLUTE     '168'
142_0	COME_FROM         '116'

142	DUP_TOP           None
143	LOAD_GLOBAL       'IndexError'
146	COMPARE_OP        'exception match'
149	POP_JUMP_IF_FALSE '164'
152	POP_TOP           None
153	POP_TOP           None
154	POP_TOP           None

155	LOAD_GLOBAL       'StopIteration'
158	RAISE_VARARGS_1   None
161	JUMP_ABSOLUTE     '168'
164	END_FINALLY       None
165_0	COME_FROM         '164'
165	JUMP_FORWARD      '168'
168_0	COME_FROM         '165'

168	LOAD_FAST         'what'
171	LOAD_GLOBAL       'WHAT_LINENO'
174	COMPARE_OP        '=='
177	POP_JUMP_IF_FALSE '224'

180	LOAD_FAST         'self'
183	LOAD_ATTR         '_stack'
186	LOAD_CONST        -1
189	BINARY_SUBSCR     None
190	UNPACK_SEQUENCE_3 None
193	STORE_FAST        'filename'
196	STORE_FAST        'firstlineno'
199	STORE_FAST        'funcname'

202	LOAD_FAST         'what'
205	LOAD_FAST         'filename'
208	LOAD_FAST         'lineno'
211	LOAD_FAST         'funcname'
214	BUILD_TUPLE_3     None
217	LOAD_FAST         'tdelta'
220	BUILD_TUPLE_3     None
223	RETURN_END_IF     None

224	LOAD_FAST         'what'
227	LOAD_GLOBAL       'WHAT_DEFINE_FILE'
230	COMPARE_OP        '=='
233	POP_JUMP_IF_FALSE '282'

236	LOAD_GLOBAL       'os'
239	LOAD_ATTR         'path'
242	LOAD_ATTR         'normcase'
245	LOAD_GLOBAL       'os'
248	LOAD_ATTR         'path'
251	LOAD_ATTR         'normpath'
254	LOAD_FAST         'tdelta'
257	CALL_FUNCTION_1   None
260	CALL_FUNCTION_1   None
263	STORE_FAST        'filename'

266	LOAD_FAST         'filename'
269	LOAD_FAST         'self'
272	LOAD_ATTR         '_filemap'
275	LOAD_FAST         'fileno'
278	STORE_SUBSCR      None
279	JUMP_BACK         '3'

282	LOAD_FAST         'what'
285	LOAD_GLOBAL       'WHAT_DEFINE_FUNC'
288	COMPARE_OP        '=='
291	POP_JUMP_IF_FALSE '335'

294	LOAD_FAST         'self'
297	LOAD_ATTR         '_filemap'
300	LOAD_FAST         'fileno'
303	BINARY_SUBSCR     None
304	STORE_FAST        'filename'

307	LOAD_FAST         'filename'
310	LOAD_FAST         'tdelta'
313	BUILD_TUPLE_2     None
316	LOAD_FAST         'self'
319	LOAD_ATTR         '_funcmap'
322	LOAD_FAST         'fileno'
325	LOAD_FAST         'lineno'
328	BUILD_TUPLE_2     None
331	STORE_SUBSCR      None
332	JUMP_BACK         '3'

335	LOAD_FAST         'what'
338	LOAD_GLOBAL       'WHAT_ADD_INFO'
341	COMPARE_OP        '=='
344	POP_JUMP_IF_FALSE '390'

347	LOAD_FAST         'tdelta'
350	LOAD_CONST        'current-directory'
353	COMPARE_OP        '=='
356	POP_JUMP_IF_FALSE '371'

359	LOAD_FAST         'lineno'
362	LOAD_FAST         'self'
365	STORE_ATTR        'cwd'
368	JUMP_FORWARD      '371'
371_0	COME_FROM         '368'

371	LOAD_FAST         'self'
374	LOAD_ATTR         'addinfo'
377	LOAD_FAST         'tdelta'
380	LOAD_FAST         'lineno'
383	CALL_FUNCTION_2   None
386	POP_TOP           None
387	JUMP_BACK         '3'

390	LOAD_GLOBAL       'ValueError'
393	LOAD_CONST        'unknown event type'
396	RAISE_VARARGS_2   None
399	JUMP_BACK         '3'
402	POP_BLOCK         None
403_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 402

    def __iter__(self):
        return self

    def _decode_location(self, fileno, lineno):
        try:
            return self._funcmap[fileno, lineno]
        except KeyError:
            if self._loadfile(fileno):
                filename = funcname = None
            try:
                filename, funcname = self._funcmap[fileno, lineno]
            except KeyError:
                filename = self._filemap.get(fileno)
                funcname = None
                self._funcmap[fileno, lineno] = (filename, funcname)

        return (filename, funcname)

    def _loadfile(self, fileno):
        try:
            filename = self._filemap[fileno]
        except KeyError:
            print 'Could not identify fileId', fileno
            return 1

        if filename is None:
            return 1
        else:
            absname = os.path.normcase(os.path.join(self.cwd, filename))
            try:
                fp = open(absname)
            except IOError:
                return

            st = parser.suite(fp.read())
            fp.close()
            funcdef = symbol.funcdef
            lambdef = symbol.lambdef
            stack = [st.totuple(1)]
            while stack:
                tree = stack.pop()
                try:
                    sym = tree[0]
                except (IndexError, TypeError):
                    continue

                if sym == funcdef:
                    self._funcmap[fileno, tree[2][2]] = (filename, tree[2][1])
                elif sym == lambdef:
                    self._funcmap[fileno, tree[1][2]] = (filename, '<lambda>')
                stack.extend(list(tree[1:]))

            return