# Embedded file name: scripts/common/Lib/idlelib/GrepDialog.py
import os
import fnmatch
import sys
from Tkinter import *
from idlelib import SearchEngine
from idlelib.SearchDialogBase import SearchDialogBase

def grep(text, io = None, flist = None):
    root = text._root()
    engine = SearchEngine.get(root)
    if not hasattr(engine, '_grepdialog'):
        engine._grepdialog = GrepDialog(root, engine, flist)
    dialog = engine._grepdialog
    searchphrase = text.get('sel.first', 'sel.last')
    dialog.open(text, searchphrase, io)


class GrepDialog(SearchDialogBase):
    title = 'Find in Files Dialog'
    icon = 'Grep'
    needwrapbutton = 0

    def __init__(self, root, engine, flist):
        SearchDialogBase.__init__(self, root, engine)
        self.flist = flist
        self.globvar = StringVar(root)
        self.recvar = BooleanVar(root)

    def open(self, text, searchphrase, io = None):
        SearchDialogBase.open(self, text, searchphrase)
        if io:
            path = io.filename or ''
        else:
            path = ''
        dir, base = os.path.split(path)
        head, tail = os.path.splitext(base)
        if not tail:
            tail = '.py'
        self.globvar.set(os.path.join(dir, '*' + tail))

    def create_entries(self):
        SearchDialogBase.create_entries(self)
        self.globent = self.make_entry('In files:', self.globvar)

    def create_other_buttons(self):
        f = self.make_frame()
        btn = Checkbutton(f, anchor='w', variable=self.recvar, text='Recurse down subdirectories')
        btn.pack(side='top', fill='both')
        btn.select()

    def create_command_buttons(self):
        SearchDialogBase.create_command_buttons(self)
        self.make_button('Search Files', self.default_command, 1)

    def default_command(self, event = None):
        prog = self.engine.getprog()
        if not prog:
            return
        path = self.globvar.get()
        if not path:
            self.top.bell()
            return
        from idlelib.OutputWindow import OutputWindow
        save = sys.stdout
        try:
            sys.stdout = OutputWindow(self.flist)
            self.grep_it(prog, path)
        finally:
            sys.stdout = save

    def grep_it--- This code section failed: ---

0	LOAD_GLOBAL       'os'
3	LOAD_ATTR         'path'
6	LOAD_ATTR         'split'
9	LOAD_FAST         'path'
12	CALL_FUNCTION_1   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'dir'
21	STORE_FAST        'base'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'findfiles'
30	LOAD_FAST         'dir'
33	LOAD_FAST         'base'
36	LOAD_FAST         'self'
39	LOAD_ATTR         'recvar'
42	LOAD_ATTR         'get'
45	CALL_FUNCTION_0   None
48	CALL_FUNCTION_3   None
51	STORE_FAST        'list'

54	LOAD_FAST         'list'
57	LOAD_ATTR         'sort'
60	CALL_FUNCTION_0   None
63	POP_TOP           None

64	LOAD_FAST         'self'
67	LOAD_ATTR         'close'
70	CALL_FUNCTION_0   None
73	POP_TOP           None

74	LOAD_FAST         'self'
77	LOAD_ATTR         'engine'
80	LOAD_ATTR         'getpat'
83	CALL_FUNCTION_0   None
86	STORE_FAST        'pat'

89	LOAD_CONST        'Searching %r in %s ...'
92	LOAD_FAST         'pat'
95	LOAD_FAST         'path'
98	BUILD_TUPLE_2     None
101	BINARY_MODULO     None
102	PRINT_ITEM        None
103	PRINT_NEWLINE_CONT None

104	LOAD_CONST        0
107	STORE_FAST        'hits'

110	SETUP_LOOP        '324'
113	LOAD_FAST         'list'
116	GET_ITER          None
117	FOR_ITER          '323'
120	STORE_FAST        'fn'

123	SETUP_EXCEPT      '142'

126	LOAD_GLOBAL       'open'
129	LOAD_FAST         'fn'
132	CALL_FUNCTION_1   None
135	STORE_FAST        'f'
138	POP_BLOCK         None
139	JUMP_FORWARD      '169'
142_0	COME_FROM         '123'

142	DUP_TOP           None
143	LOAD_GLOBAL       'IOError'
146	COMPARE_OP        'exception match'
149	POP_JUMP_IF_FALSE '168'
152	POP_TOP           None
153	STORE_FAST        'msg'
156	POP_TOP           None

157	LOAD_FAST         'msg'
160	PRINT_ITEM        None
161	PRINT_NEWLINE_CONT None

162	CONTINUE          '117'
165	JUMP_FORWARD      '169'
168	END_FINALLY       None
169_0	COME_FROM         '139'
169_1	COME_FROM         '168'

169	LOAD_CONST        0
172	STORE_FAST        'lineno'

175	SETUP_LOOP        '320'

178	LOAD_FAST         'f'
181	LOAD_ATTR         'readlines'
184	LOAD_CONST        100000
187	CALL_FUNCTION_1   None
190	STORE_FAST        'block'

193	LOAD_FAST         'block'
196	POP_JUMP_IF_TRUE  '203'

199	BREAK_LOOP        None
200	JUMP_FORWARD      '203'
203_0	COME_FROM         '200'

203	SETUP_LOOP        '316'
206	LOAD_FAST         'block'
209	GET_ITER          None
210	FOR_ITER          '315'
213	STORE_FAST        'line'

216	LOAD_FAST         'lineno'
219	LOAD_CONST        1
222	BINARY_ADD        None
223	STORE_FAST        'lineno'

226	LOAD_FAST         'line'
229	LOAD_CONST        -1
232	SLICE+1           None
233	LOAD_CONST        '\n'
236	COMPARE_OP        '=='
239	POP_JUMP_IF_FALSE '255'

242	LOAD_FAST         'line'
245	LOAD_CONST        -1
248	SLICE+2           None
249	STORE_FAST        'line'
252	JUMP_FORWARD      '255'
255_0	COME_FROM         '252'

255	LOAD_FAST         'prog'
258	LOAD_ATTR         'search'
261	LOAD_FAST         'line'
264	CALL_FUNCTION_1   None
267	POP_JUMP_IF_FALSE '210'

270	LOAD_GLOBAL       'sys'
273	LOAD_ATTR         'stdout'
276	LOAD_ATTR         'write'
279	LOAD_CONST        '%s: %s: %s\n'
282	LOAD_FAST         'fn'
285	LOAD_FAST         'lineno'
288	LOAD_FAST         'line'
291	BUILD_TUPLE_3     None
294	BINARY_MODULO     None
295	CALL_FUNCTION_1   None
298	POP_TOP           None

299	LOAD_FAST         'hits'
302	LOAD_CONST        1
305	BINARY_ADD        None
306	STORE_FAST        'hits'
309	JUMP_BACK         '210'
312	JUMP_BACK         '210'
315	POP_BLOCK         None
316_0	COME_FROM         '203'
316	JUMP_BACK         '178'
319	POP_BLOCK         None
320_0	COME_FROM         '175'
320	JUMP_BACK         '117'
323	POP_BLOCK         None
324_0	COME_FROM         '110'

324	LOAD_FAST         'hits'
327	POP_JUMP_IF_FALSE '382'

330	LOAD_FAST         'hits'
333	LOAD_CONST        1
336	COMPARE_OP        '=='
339	POP_JUMP_IF_FALSE '351'

342	LOAD_CONST        ''
345	STORE_FAST        's'
348	JUMP_FORWARD      '357'

351	LOAD_CONST        's'
354	STORE_FAST        's'
357_0	COME_FROM         '348'

357	LOAD_CONST        'Found'
360	PRINT_ITEM        None
361	LOAD_FAST         'hits'
364	PRINT_ITEM_CONT   None
365	LOAD_CONST        'hit%s.'
368	LOAD_FAST         's'
371	BINARY_MODULO     None
372	PRINT_ITEM_CONT   None
373	PRINT_NEWLINE_CONT None

374	LOAD_CONST        '(Hint: right-click to open locations.)'
377	PRINT_ITEM        None
378	PRINT_NEWLINE_CONT None
379	JUMP_FORWARD      '387'

382	LOAD_CONST        'No hits.'
385	PRINT_ITEM        None
386	PRINT_NEWLINE_CONT None
387_0	COME_FROM         '379'

Syntax error at or near `POP_BLOCK' token at offset 319

    def findfiles(self, dir, base, rec):
        try:
            names = os.listdir(dir or os.curdir)
        except os.error as msg:
            print msg
            return []

        list = []
        subdirs = []
        for name in names:
            fn = os.path.join(dir, name)
            if os.path.isdir(fn):
                subdirs.append(fn)
            elif fnmatch.fnmatch(name, base):
                list.append(fn)

        if rec:
            for subdir in subdirs:
                list.extend(self.findfiles(subdir, base, rec))

        return list

    def close(self, event = None):
        if self.top:
            self.top.grab_release()
            self.top.withdraw()