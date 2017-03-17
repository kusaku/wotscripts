# Embedded file name: scripts/common/Lib/idlelib/ReplaceDialog.py
from Tkinter import *
from idlelib import SearchEngine
from idlelib.SearchDialogBase import SearchDialogBase

def replace(text):
    root = text._root()
    engine = SearchEngine.get(root)
    if not hasattr(engine, '_replacedialog'):
        engine._replacedialog = ReplaceDialog(root, engine)
    dialog = engine._replacedialog
    dialog.open(text)


class ReplaceDialog(SearchDialogBase):
    title = 'Replace Dialog'
    icon = 'Replace'

    def __init__(self, root, engine):
        SearchDialogBase.__init__(self, root, engine)
        self.replvar = StringVar(root)

    def open(self, text):
        SearchDialogBase.open(self, text)
        try:
            first = text.index('sel.first')
        except TclError:
            first = None

        try:
            last = text.index('sel.last')
        except TclError:
            last = None

        first = first or text.index('insert')
        last = last or first
        self.show_hit(first, last)
        self.ok = 1
        return

    def create_entries(self):
        SearchDialogBase.create_entries(self)
        self.replent = self.make_entry('Replace with:', self.replvar)

    def create_command_buttons(self):
        SearchDialogBase.create_command_buttons(self)
        self.make_button('Find', self.find_it)
        self.make_button('Replace', self.replace_it)
        self.make_button('Replace+Find', self.default_command, 1)
        self.make_button('Replace All', self.replace_all)

    def find_it(self, event = None):
        self.do_find(0)

    def replace_it(self, event = None):
        if self.do_find(self.ok):
            self.do_replace()

    def default_command(self, event = None):
        if self.do_find(self.ok):
            self.do_replace()
            self.do_find(0)

    def replace_all--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'engine'
6	LOAD_ATTR         'getprog'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'prog'

15	LOAD_FAST         'prog'
18	POP_JUMP_IF_TRUE  '25'

21	LOAD_CONST        None
24	RETURN_END_IF     None

25	LOAD_FAST         'self'
28	LOAD_ATTR         'replvar'
31	LOAD_ATTR         'get'
34	CALL_FUNCTION_0   None
37	STORE_FAST        'repl'

40	LOAD_FAST         'self'
43	LOAD_ATTR         'text'
46	STORE_FAST        'text'

49	LOAD_FAST         'self'
52	LOAD_ATTR         'engine'
55	LOAD_ATTR         'search_text'
58	LOAD_FAST         'text'
61	LOAD_FAST         'prog'
64	CALL_FUNCTION_2   None
67	STORE_FAST        'res'

70	LOAD_FAST         'res'
73	POP_JUMP_IF_TRUE  '90'

76	LOAD_FAST         'text'
79	LOAD_ATTR         'bell'
82	CALL_FUNCTION_0   None
85	POP_TOP           None

86	LOAD_CONST        None
89	RETURN_END_IF     None

90	LOAD_FAST         'text'
93	LOAD_ATTR         'tag_remove'
96	LOAD_CONST        'sel'
99	LOAD_CONST        '1.0'
102	LOAD_CONST        'end'
105	CALL_FUNCTION_3   None
108	POP_TOP           None

109	LOAD_FAST         'text'
112	LOAD_ATTR         'tag_remove'
115	LOAD_CONST        'hit'
118	LOAD_CONST        '1.0'
121	LOAD_CONST        'end'
124	CALL_FUNCTION_3   None
127	POP_TOP           None

128	LOAD_FAST         'res'
131	LOAD_CONST        0
134	BINARY_SUBSCR     None
135	STORE_FAST        'line'

138	LOAD_FAST         'res'
141	LOAD_CONST        1
144	BINARY_SUBSCR     None
145	LOAD_ATTR         'start'
148	CALL_FUNCTION_0   None
151	STORE_FAST        'col'

154	LOAD_FAST         'self'
157	LOAD_ATTR         'engine'
160	LOAD_ATTR         'iswrap'
163	CALL_FUNCTION_0   None
166	POP_JUMP_IF_FALSE '184'

169	LOAD_CONST        1
172	STORE_FAST        'line'

175	LOAD_CONST        0
178	STORE_FAST        'col'
181	JUMP_FORWARD      '184'
184_0	COME_FROM         '181'

184	LOAD_CONST        1
187	STORE_FAST        'ok'

190	LOAD_CONST        None
193	DUP_TOP           None
194	STORE_FAST        'first'
197	STORE_FAST        'last'

200	LOAD_FAST         'text'
203	LOAD_ATTR         'undo_block_start'
206	CALL_FUNCTION_0   None
209	POP_TOP           None

210	SETUP_LOOP        '504'

213	LOAD_FAST         'self'
216	LOAD_ATTR         'engine'
219	LOAD_ATTR         'search_forward'
222	LOAD_FAST         'text'
225	LOAD_FAST         'prog'
228	LOAD_FAST         'line'
231	LOAD_FAST         'col'
234	LOAD_CONST        0
237	LOAD_FAST         'ok'
240	CALL_FUNCTION_6   None
243	STORE_FAST        'res'

246	LOAD_FAST         'res'
249	POP_JUMP_IF_TRUE  '256'

252	BREAK_LOOP        None
253	JUMP_FORWARD      '256'
256_0	COME_FROM         '253'

256	LOAD_FAST         'res'
259	UNPACK_SEQUENCE_2 None
262	STORE_FAST        'line'
265	STORE_FAST        'm'

268	LOAD_FAST         'text'
271	LOAD_ATTR         'get'
274	LOAD_CONST        '%d.0'
277	LOAD_FAST         'line'
280	BINARY_MODULO     None
281	LOAD_CONST        '%d.0'
284	LOAD_FAST         'line'
287	LOAD_CONST        1
290	BINARY_ADD        None
291	BINARY_MODULO     None
292	CALL_FUNCTION_2   None
295	STORE_FAST        'chars'

298	LOAD_FAST         'm'
301	LOAD_ATTR         'group'
304	CALL_FUNCTION_0   None
307	STORE_FAST        'orig'

310	LOAD_FAST         'm'
313	LOAD_ATTR         'expand'
316	LOAD_FAST         'repl'
319	CALL_FUNCTION_1   None
322	STORE_FAST        'new'

325	LOAD_FAST         'm'
328	LOAD_ATTR         'span'
331	CALL_FUNCTION_0   None
334	UNPACK_SEQUENCE_2 None
337	STORE_FAST        'i'
340	STORE_FAST        'j'

343	LOAD_CONST        '%d.%d'
346	LOAD_FAST         'line'
349	LOAD_FAST         'i'
352	BUILD_TUPLE_2     None
355	BINARY_MODULO     None
356	STORE_FAST        'first'

359	LOAD_CONST        '%d.%d'
362	LOAD_FAST         'line'
365	LOAD_FAST         'j'
368	BUILD_TUPLE_2     None
371	BINARY_MODULO     None
372	STORE_FAST        'last'

375	LOAD_FAST         'new'
378	LOAD_FAST         'orig'
381	COMPARE_OP        '=='
384	POP_JUMP_IF_FALSE '406'

387	LOAD_FAST         'text'
390	LOAD_ATTR         'mark_set'
393	LOAD_CONST        'insert'
396	LOAD_FAST         'last'
399	CALL_FUNCTION_2   None
402	POP_TOP           None
403	JUMP_FORWARD      '478'

406	LOAD_FAST         'text'
409	LOAD_ATTR         'mark_set'
412	LOAD_CONST        'insert'
415	LOAD_FAST         'first'
418	CALL_FUNCTION_2   None
421	POP_TOP           None

422	LOAD_FAST         'first'
425	LOAD_FAST         'last'
428	COMPARE_OP        '!='
431	POP_JUMP_IF_FALSE '453'

434	LOAD_FAST         'text'
437	LOAD_ATTR         'delete'
440	LOAD_FAST         'first'
443	LOAD_FAST         'last'
446	CALL_FUNCTION_2   None
449	POP_TOP           None
450	JUMP_FORWARD      '453'
453_0	COME_FROM         '450'

453	LOAD_FAST         'new'
456	POP_JUMP_IF_FALSE '478'

459	LOAD_FAST         'text'
462	LOAD_ATTR         'insert'
465	LOAD_FAST         'first'
468	LOAD_FAST         'new'
471	CALL_FUNCTION_2   None
474	POP_TOP           None
475	JUMP_FORWARD      '478'
478_0	COME_FROM         '403'
478_1	COME_FROM         '475'

478	LOAD_FAST         'i'
481	LOAD_GLOBAL       'len'
484	LOAD_FAST         'new'
487	CALL_FUNCTION_1   None
490	BINARY_ADD        None
491	STORE_FAST        'col'

494	LOAD_CONST        0
497	STORE_FAST        'ok'
500	JUMP_BACK         '213'
503	POP_BLOCK         None
504_0	COME_FROM         '210'

504	LOAD_FAST         'text'
507	LOAD_ATTR         'undo_block_stop'
510	CALL_FUNCTION_0   None
513	POP_TOP           None

514	LOAD_FAST         'first'
517	POP_JUMP_IF_FALSE '545'
520	LOAD_FAST         'last'
523_0	COME_FROM         '517'
523	POP_JUMP_IF_FALSE '545'

526	LOAD_FAST         'self'
529	LOAD_ATTR         'show_hit'
532	LOAD_FAST         'first'
535	LOAD_FAST         'last'
538	CALL_FUNCTION_2   None
541	POP_TOP           None
542	JUMP_FORWARD      '545'
545_0	COME_FROM         '542'

545	LOAD_FAST         'self'
548	LOAD_ATTR         'close'
551	CALL_FUNCTION_0   None
554	POP_TOP           None
555	LOAD_CONST        None
558	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 503

    def do_find(self, ok = 0):
        if not self.engine.getprog():
            return False
        else:
            text = self.text
            res = self.engine.search_text(text, None, ok)
            if not res:
                text.bell()
                return False
            line, m = res
            i, j = m.span()
            first = '%d.%d' % (line, i)
            last = '%d.%d' % (line, j)
            self.show_hit(first, last)
            self.ok = 1
            return True

    def do_replace(self):
        prog = self.engine.getprog()
        if not prog:
            return False
        else:
            text = self.text
            try:
                first = pos = text.index('sel.first')
                last = text.index('sel.last')
            except TclError:
                pos = None

            if not pos:
                first = last = pos = text.index('insert')
            line, col = SearchEngine.get_line_col(pos)
            chars = text.get('%d.0' % line, '%d.0' % (line + 1))
            m = prog.match(chars, col)
            if not prog:
                return False
            new = m.expand(self.replvar.get())
            text.mark_set('insert', first)
            text.undo_block_start()
            if m.group():
                text.delete(first, last)
            if new:
                text.insert(first, new)
            text.undo_block_stop()
            self.show_hit(first, text.index('insert'))
            self.ok = 0
            return True

    def show_hit(self, first, last):
        text = self.text
        text.mark_set('insert', first)
        text.tag_remove('sel', '1.0', 'end')
        text.tag_add('sel', first, last)
        text.tag_remove('hit', '1.0', 'end')
        if first == last:
            text.tag_add('hit', first)
        else:
            text.tag_add('hit', first, last)
        text.see('insert')
        text.update_idletasks()

    def close(self, event = None):
        SearchDialogBase.close(self, event)
        self.text.tag_remove('hit', '1.0', 'end')