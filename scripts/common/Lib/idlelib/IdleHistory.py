# Embedded file name: scripts/common/Lib/idlelib/IdleHistory.py
from idlelib.configHandler import idleConf

class History:

    def __init__(self, text, output_sep = '\n'):
        self.text = text
        self.history = []
        self.history_prefix = None
        self.history_pointer = None
        self.output_sep = output_sep
        self.cyclic = idleConf.GetOption('main', 'History', 'cyclic', 1, 'bool')
        text.bind('<<history-previous>>', self.history_prev)
        text.bind('<<history-next>>', self.history_next)
        return

    def history_next(self, event):
        self.history_do(0)
        return 'break'

    def history_prev(self, event):
        self.history_do(1)
        return 'break'

    def _get_source(self, start, end):
        lines = self.text.get(start, end).split(self.output_sep)
        return '\n'.join(lines)

    def _put_source(self, where, source):
        output = self.output_sep.join(source.split('\n'))
        self.text.insert(where, output)

    def history_do--- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'history'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'nhist'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'history_pointer'
21	STORE_FAST        'pointer'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'history_prefix'
30	STORE_FAST        'prefix'

33	LOAD_FAST         'pointer'
36	LOAD_CONST        None
39	COMPARE_OP        'is not'
42	POP_JUMP_IF_FALSE '128'
45	LOAD_FAST         'prefix'
48	LOAD_CONST        None
51	COMPARE_OP        'is not'
54_0	COME_FROM         '42'
54	POP_JUMP_IF_FALSE '128'

57	LOAD_FAST         'self'
60	LOAD_ATTR         'text'
63	LOAD_ATTR         'compare'
66	LOAD_CONST        'insert'
69	LOAD_CONST        '!='
72	LOAD_CONST        'end-1c'
75	CALL_FUNCTION_3   None
78	POP_JUMP_IF_TRUE  '112'

81	LOAD_FAST         'self'
84	LOAD_ATTR         '_get_source'
87	LOAD_CONST        'iomark'
90	LOAD_CONST        'end-1c'
93	CALL_FUNCTION_2   None
96	LOAD_FAST         'self'
99	LOAD_ATTR         'history'
102	LOAD_FAST         'pointer'
105	BINARY_SUBSCR     None
106	COMPARE_OP        '!='
109_0	COME_FROM         '78'
109	POP_JUMP_IF_FALSE '128'

112	LOAD_CONST        None
115	DUP_TOP           None
116	STORE_FAST        'pointer'
119	STORE_FAST        'prefix'
122	JUMP_ABSOLUTE     '128'
125	JUMP_FORWARD      '128'
128_0	COME_FROM         '125'

128	LOAD_FAST         'pointer'
131	LOAD_CONST        None
134	COMPARE_OP        'is'
137	POP_JUMP_IF_TRUE  '152'
140	LOAD_FAST         'prefix'
143	LOAD_CONST        None
146	COMPARE_OP        'is'
149_0	COME_FROM         '137'
149	POP_JUMP_IF_FALSE '223'

152	LOAD_FAST         'self'
155	LOAD_ATTR         '_get_source'
158	LOAD_CONST        'iomark'
161	LOAD_CONST        'end-1c'
164	CALL_FUNCTION_2   None
167	STORE_FAST        'prefix'

170	LOAD_FAST         'reverse'
173	POP_JUMP_IF_FALSE '185'

176	LOAD_FAST         'nhist'
179	STORE_FAST        'pointer'
182	JUMP_ABSOLUTE     '223'

185	LOAD_FAST         'self'
188	LOAD_ATTR         'cyclic'
191	POP_JUMP_IF_FALSE '203'

194	LOAD_CONST        -1
197	STORE_FAST        'pointer'
200	JUMP_ABSOLUTE     '223'

203	LOAD_FAST         'self'
206	LOAD_ATTR         'text'
209	LOAD_ATTR         'bell'
212	CALL_FUNCTION_0   None
215	POP_TOP           None

216	LOAD_CONST        None
219	RETURN_VALUE      None
220	JUMP_FORWARD      '223'
223_0	COME_FROM         '220'

223	LOAD_GLOBAL       'len'
226	LOAD_FAST         'prefix'
229	CALL_FUNCTION_1   None
232	STORE_FAST        'nprefix'

235	SETUP_LOOP        '496'

238	LOAD_FAST         'reverse'
241	POP_JUMP_IF_FALSE '257'

244	LOAD_FAST         'pointer'
247	LOAD_CONST        1
250	BINARY_SUBTRACT   None
251	STORE_FAST        'pointer'
254	JUMP_FORWARD      '267'

257	LOAD_FAST         'pointer'
260	LOAD_CONST        1
263	BINARY_ADD        None
264	STORE_FAST        'pointer'
267_0	COME_FROM         '254'

267	LOAD_FAST         'pointer'
270	LOAD_CONST        0
273	COMPARE_OP        '<'
276	POP_JUMP_IF_TRUE  '291'
279	LOAD_FAST         'pointer'
282	LOAD_FAST         'nhist'
285	COMPARE_OP        '>='
288_0	COME_FROM         '276'
288	POP_JUMP_IF_FALSE '406'

291	LOAD_FAST         'self'
294	LOAD_ATTR         'text'
297	LOAD_ATTR         'bell'
300	CALL_FUNCTION_0   None
303	POP_TOP           None

304	LOAD_FAST         'self'
307	LOAD_ATTR         'cyclic'
310	UNARY_NOT         None
311	POP_JUMP_IF_FALSE '330'
314	LOAD_FAST         'pointer'
317	LOAD_CONST        0
320	COMPARE_OP        '<'
323_0	COME_FROM         '311'
323	POP_JUMP_IF_FALSE '330'

326	LOAD_CONST        None
329	RETURN_END_IF     None

330	LOAD_FAST         'self'
333	LOAD_ATTR         '_get_source'
336	LOAD_CONST        'iomark'
339	LOAD_CONST        'end-1c'
342	CALL_FUNCTION_2   None
345	LOAD_FAST         'prefix'
348	COMPARE_OP        '!='
351	POP_JUMP_IF_FALSE '392'

354	LOAD_FAST         'self'
357	LOAD_ATTR         'text'
360	LOAD_ATTR         'delete'
363	LOAD_CONST        'iomark'
366	LOAD_CONST        'end-1c'
369	CALL_FUNCTION_2   None
372	POP_TOP           None

373	LOAD_FAST         'self'
376	LOAD_ATTR         '_put_source'
379	LOAD_CONST        'iomark'
382	LOAD_FAST         'prefix'
385	CALL_FUNCTION_2   None
388	POP_TOP           None
389	JUMP_FORWARD      '392'
392_0	COME_FROM         '389'

392	LOAD_CONST        None
395	DUP_TOP           None
396	STORE_FAST        'pointer'
399	STORE_FAST        'prefix'

402	BREAK_LOOP        None
403	JUMP_FORWARD      '406'
406_0	COME_FROM         '403'

406	LOAD_FAST         'self'
409	LOAD_ATTR         'history'
412	LOAD_FAST         'pointer'
415	BINARY_SUBSCR     None
416	STORE_FAST        'item'

419	LOAD_FAST         'item'
422	LOAD_FAST         'nprefix'
425	SLICE+2           None
426	LOAD_FAST         'prefix'
429	COMPARE_OP        '=='
432	POP_JUMP_IF_FALSE '238'
435	LOAD_GLOBAL       'len'
438	LOAD_FAST         'item'
441	CALL_FUNCTION_1   None
444	LOAD_FAST         'nprefix'
447	COMPARE_OP        '>'
450_0	COME_FROM         '432'
450	POP_JUMP_IF_FALSE '238'

453	LOAD_FAST         'self'
456	LOAD_ATTR         'text'
459	LOAD_ATTR         'delete'
462	LOAD_CONST        'iomark'
465	LOAD_CONST        'end-1c'
468	CALL_FUNCTION_2   None
471	POP_TOP           None

472	LOAD_FAST         'self'
475	LOAD_ATTR         '_put_source'
478	LOAD_CONST        'iomark'
481	LOAD_FAST         'item'
484	CALL_FUNCTION_2   None
487	POP_TOP           None

488	BREAK_LOOP        None
489	JUMP_BACK         '238'
492	JUMP_BACK         '238'
495	POP_BLOCK         None
496_0	COME_FROM         '235'

496	LOAD_FAST         'self'
499	LOAD_ATTR         'text'
502	LOAD_ATTR         'mark_set'
505	LOAD_CONST        'insert'
508	LOAD_CONST        'end-1c'
511	CALL_FUNCTION_2   None
514	POP_TOP           None

515	LOAD_FAST         'self'
518	LOAD_ATTR         'text'
521	LOAD_ATTR         'see'
524	LOAD_CONST        'insert'
527	CALL_FUNCTION_1   None
530	POP_TOP           None

531	LOAD_FAST         'self'
534	LOAD_ATTR         'text'
537	LOAD_ATTR         'tag_remove'
540	LOAD_CONST        'sel'
543	LOAD_CONST        '1.0'
546	LOAD_CONST        'end'
549	CALL_FUNCTION_3   None
552	POP_TOP           None

553	LOAD_FAST         'pointer'
556	LOAD_FAST         'self'
559	STORE_ATTR        'history_pointer'

562	LOAD_FAST         'prefix'
565	LOAD_FAST         'self'
568	STORE_ATTR        'history_prefix'
571	LOAD_CONST        None
574	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 495

    def history_store(self, source):
        source = source.strip()
        if len(source) > 2:
            try:
                self.history.remove(source)
            except ValueError:
                pass

            self.history.append(source)
        self.history_pointer = None
        self.history_prefix = None
        return