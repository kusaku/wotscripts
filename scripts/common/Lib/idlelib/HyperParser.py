# Embedded file name: scripts/common/Lib/idlelib/HyperParser.py
"""
HyperParser
===========
This module defines the HyperParser class, which provides advanced parsing
abilities for the ParenMatch and other extensions.
The HyperParser uses PyParser. PyParser is intended mostly to give information
on the proper indentation of code. HyperParser gives some information on the
structure of code, used by extensions to help the user.
"""
import string
import keyword
from idlelib import PyParse

class HyperParser:

    def __init__(self, editwin, index):
        """Initialize the HyperParser to analyze the surroundings of the given
        index.
        """
        self.editwin = editwin
        self.text = text = editwin.text
        parser = PyParse.Parser(editwin.indentwidth, editwin.tabwidth)

        def index2line(index):
            return int(float(index))

        lno = index2line(text.index(index))
        if not editwin.context_use_ps1:
            for context in editwin.num_context_lines:
                startat = max(lno - context, 1)
                startatindex = repr(startat) + '.0'
                stopatindex = '%d.end' % lno
                parser.set_str(text.get(startatindex, stopatindex) + ' \n')
                bod = parser.find_good_parse_start(editwin._build_char_in_string_func(startatindex))
                if bod is not None or startat == 1:
                    break

            parser.set_lo(bod or 0)
        else:
            r = text.tag_prevrange('console', index)
            if r:
                startatindex = r[1]
            else:
                startatindex = '1.0'
            stopatindex = '%d.end' % lno
            parser.set_str(text.get(startatindex, stopatindex) + ' \n')
            parser.set_lo(0)
        self.rawtext = parser.str[:-2]
        self.stopatindex = stopatindex
        self.bracketing = parser.get_last_stmt_bracketing()
        self.isopener = [ i > 0 and self.bracketing[i][1] > self.bracketing[i - 1][1] for i in range(len(self.bracketing)) ]
        self.set_index(index)
        return

    def set_index(self, index):
        """Set the index to which the functions relate. Note that it must be
        in the same statement.
        """
        indexinrawtext = len(self.rawtext) - len(self.text.get(index, self.stopatindex))
        if indexinrawtext < 0:
            raise ValueError('The index given is before the analyzed statement')
        self.indexinrawtext = indexinrawtext
        self.indexbracket = 0
        while self.indexbracket < len(self.bracketing) - 1 and self.bracketing[self.indexbracket + 1][0] < self.indexinrawtext:
            self.indexbracket += 1

        if self.indexbracket < len(self.bracketing) - 1 and self.bracketing[self.indexbracket + 1][0] == self.indexinrawtext and not self.isopener[self.indexbracket + 1]:
            self.indexbracket += 1

    def is_in_string(self):
        """Is the index given to the HyperParser is in a string?"""
        return self.isopener[self.indexbracket] and self.rawtext[self.bracketing[self.indexbracket][0]] in ('"', "'")

    def is_in_code(self):
        """Is the index given to the HyperParser is in a normal code?"""
        return not self.isopener[self.indexbracket] or self.rawtext[self.bracketing[self.indexbracket][0]] not in ('#', '"', "'")

    def get_surrounding_brackets(self, openers = '([{', mustclose = False):
        """If the index given to the HyperParser is surrounded by a bracket
        defined in openers (or at least has one before it), return the
        indices of the opening bracket and the closing bracket (or the
        end of line, whichever comes first).
        If it is not surrounded by brackets, or the end of line comes before
        the closing bracket and mustclose is True, returns None.
        """
        bracketinglevel = self.bracketing[self.indexbracket][1]
        before = self.indexbracket
        while not self.isopener[before] or self.rawtext[self.bracketing[before][0]] not in openers or self.bracketing[before][1] > bracketinglevel:
            before -= 1
            if before < 0:
                return None
            bracketinglevel = min(bracketinglevel, self.bracketing[before][1])

        after = self.indexbracket + 1
        while after < len(self.bracketing) and self.bracketing[after][1] >= bracketinglevel:
            after += 1

        beforeindex = self.text.index('%s-%dc' % (self.stopatindex, len(self.rawtext) - self.bracketing[before][0]))
        if after >= len(self.bracketing) or self.bracketing[after][0] > len(self.rawtext):
            if mustclose:
                return None
            afterindex = self.stopatindex
        else:
            afterindex = self.text.index('%s-%dc' % (self.stopatindex, len(self.rawtext) - (self.bracketing[after][0] - 1)))
        return (beforeindex, afterindex)

    _whitespace_chars = ' \t\n\\'
    _id_chars = string.ascii_letters + string.digits + '_'
    _id_first_chars = string.ascii_letters + '_'

    def _eat_identifier(self, str, limit, pos):
        i = pos
        while i > limit and str[i - 1] in self._id_chars:
            i -= 1

        if i < pos and (str[i] not in self._id_first_chars or keyword.iskeyword(str[i:pos])):
            i = pos
        return pos - i

    def get_expression--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'is_in_code'
6	CALL_FUNCTION_0   None
9	POP_JUMP_IF_TRUE  '27'

12	LOAD_GLOBAL       'ValueError'
15	LOAD_CONST        'get_expression should only be called if index is inside a code.'
18	CALL_FUNCTION_1   None
21	RAISE_VARARGS_1   None
24	JUMP_FORWARD      '27'
27_0	COME_FROM         '24'

27	LOAD_FAST         'self'
30	LOAD_ATTR         'rawtext'
33	STORE_FAST        'rawtext'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'bracketing'
42	STORE_FAST        'bracketing'

45	LOAD_FAST         'self'
48	LOAD_ATTR         'indexbracket'
51	STORE_FAST        'brck_index'

54	LOAD_FAST         'bracketing'
57	LOAD_FAST         'brck_index'
60	BINARY_SUBSCR     None
61	LOAD_CONST        0
64	BINARY_SUBSCR     None
65	STORE_FAST        'brck_limit'

68	LOAD_FAST         'self'
71	LOAD_ATTR         'indexinrawtext'
74	STORE_FAST        'pos'

77	LOAD_FAST         'pos'
80	STORE_FAST        'last_identifier_pos'

83	LOAD_GLOBAL       'True'
86	STORE_FAST        'postdot_phase'

89	SETUP_LOOP        '540'

92	SETUP_LOOP        '303'

95	LOAD_FAST         'pos'
98	LOAD_FAST         'brck_limit'
101	COMPARE_OP        '>'
104	POP_JUMP_IF_FALSE '143'
107	LOAD_FAST         'rawtext'
110	LOAD_FAST         'pos'
113	LOAD_CONST        1
116	BINARY_SUBTRACT   None
117	BINARY_SUBSCR     None
118	LOAD_FAST         'self'
121	LOAD_ATTR         '_whitespace_chars'
124	COMPARE_OP        'in'
127_0	COME_FROM         '104'
127	POP_JUMP_IF_FALSE '143'

130	LOAD_FAST         'pos'
133	LOAD_CONST        1
136	INPLACE_SUBTRACT  None
137	STORE_FAST        'pos'
140	JUMP_BACK         '95'

143	LOAD_FAST         'postdot_phase'
146	UNARY_NOT         None
147	POP_JUMP_IF_FALSE '201'

150	LOAD_FAST         'pos'
153	LOAD_FAST         'brck_limit'
156	COMPARE_OP        '>'
159	POP_JUMP_IF_FALSE '201'
162	LOAD_FAST         'rawtext'
165	LOAD_FAST         'pos'
168	LOAD_CONST        1
171	BINARY_SUBTRACT   None
172	BINARY_SUBSCR     None
173	LOAD_CONST        '.'
176	COMPARE_OP        '=='
179_0	COME_FROM         '147'
179_1	COME_FROM         '159'
179	POP_JUMP_IF_FALSE '201'

182	LOAD_FAST         'pos'
185	LOAD_CONST        1
188	INPLACE_SUBTRACT  None
189	STORE_FAST        'pos'

192	LOAD_GLOBAL       'True'
195	STORE_FAST        'postdot_phase'
198	JUMP_BACK         '95'

201	LOAD_FAST         'pos'
204	LOAD_FAST         'brck_limit'
207	COMPARE_OP        '=='
210	POP_JUMP_IF_FALSE '298'
213	LOAD_FAST         'brck_index'
216	LOAD_CONST        0
219	COMPARE_OP        '>'
222	POP_JUMP_IF_FALSE '298'

225	LOAD_FAST         'rawtext'
228	LOAD_FAST         'bracketing'
231	LOAD_FAST         'brck_index'
234	LOAD_CONST        1
237	BINARY_SUBTRACT   None
238	BINARY_SUBSCR     None
239	LOAD_CONST        0
242	BINARY_SUBSCR     None
243	BINARY_SUBSCR     None
244	LOAD_CONST        '#'
247	COMPARE_OP        '=='
250_0	COME_FROM         '210'
250_1	COME_FROM         '222'
250	POP_JUMP_IF_FALSE '298'

253	LOAD_FAST         'brck_index'
256	LOAD_CONST        2
259	INPLACE_SUBTRACT  None
260	STORE_FAST        'brck_index'

263	LOAD_FAST         'bracketing'
266	LOAD_FAST         'brck_index'
269	BINARY_SUBSCR     None
270	LOAD_CONST        0
273	BINARY_SUBSCR     None
274	STORE_FAST        'brck_limit'

277	LOAD_FAST         'bracketing'
280	LOAD_FAST         'brck_index'
283	LOAD_CONST        1
286	BINARY_ADD        None
287	BINARY_SUBSCR     None
288	LOAD_CONST        0
291	BINARY_SUBSCR     None
292	STORE_FAST        'pos'
295	JUMP_BACK         '95'

298	BREAK_LOOP        None
299	JUMP_BACK         '95'
302	POP_BLOCK         None
303_0	COME_FROM         '92'

303	LOAD_FAST         'postdot_phase'
306	POP_JUMP_IF_TRUE  '313'

309	BREAK_LOOP        None
310	JUMP_FORWARD      '313'
313_0	COME_FROM         '310'

313	LOAD_FAST         'self'
316	LOAD_ATTR         '_eat_identifier'
319	LOAD_FAST         'rawtext'
322	LOAD_FAST         'brck_limit'
325	LOAD_FAST         'pos'
328	CALL_FUNCTION_3   None
331	STORE_FAST        'ret'

334	LOAD_FAST         'ret'
337	POP_JUMP_IF_FALSE '365'

340	LOAD_FAST         'pos'
343	LOAD_FAST         'ret'
346	BINARY_SUBTRACT   None
347	STORE_FAST        'pos'

350	LOAD_FAST         'pos'
353	STORE_FAST        'last_identifier_pos'

356	LOAD_GLOBAL       'False'
359	STORE_FAST        'postdot_phase'
362	JUMP_BACK         '92'

365	LOAD_FAST         'pos'
368	LOAD_FAST         'brck_limit'
371	COMPARE_OP        '=='
374	POP_JUMP_IF_FALSE '535'

377	LOAD_FAST         'bracketing'
380	LOAD_FAST         'brck_index'
383	BINARY_SUBSCR     None
384	LOAD_CONST        1
387	BINARY_SUBSCR     None
388	STORE_FAST        'level'

391	SETUP_LOOP        '444'
394	LOAD_FAST         'brck_index'
397	LOAD_CONST        0
400	COMPARE_OP        '>'
403	POP_JUMP_IF_FALSE '443'
406	LOAD_FAST         'bracketing'
409	LOAD_FAST         'brck_index'
412	LOAD_CONST        1
415	BINARY_SUBTRACT   None
416	BINARY_SUBSCR     None
417	LOAD_CONST        1
420	BINARY_SUBSCR     None
421	LOAD_FAST         'level'
424	COMPARE_OP        '>'
427_0	COME_FROM         '403'
427	POP_JUMP_IF_FALSE '443'

430	LOAD_FAST         'brck_index'
433	LOAD_CONST        1
436	INPLACE_SUBTRACT  None
437	STORE_FAST        'brck_index'
440	JUMP_BACK         '394'
443	POP_BLOCK         None
444_0	COME_FROM         '391'

444	LOAD_FAST         'bracketing'
447	LOAD_FAST         'brck_index'
450	BINARY_SUBSCR     None
451	LOAD_CONST        0
454	BINARY_SUBSCR     None
455	LOAD_FAST         'brck_limit'
458	COMPARE_OP        '=='
461	POP_JUMP_IF_FALSE '468'

464	BREAK_LOOP        None
465	JUMP_FORWARD      '468'
468_0	COME_FROM         '465'

468	LOAD_FAST         'bracketing'
471	LOAD_FAST         'brck_index'
474	BINARY_SUBSCR     None
475	LOAD_CONST        0
478	BINARY_SUBSCR     None
479	STORE_FAST        'pos'

482	LOAD_FAST         'brck_index'
485	LOAD_CONST        1
488	INPLACE_SUBTRACT  None
489	STORE_FAST        'brck_index'

492	LOAD_FAST         'bracketing'
495	LOAD_FAST         'brck_index'
498	BINARY_SUBSCR     None
499	LOAD_CONST        0
502	BINARY_SUBSCR     None
503	STORE_FAST        'brck_limit'

506	LOAD_FAST         'pos'
509	STORE_FAST        'last_identifier_pos'

512	LOAD_FAST         'rawtext'
515	LOAD_FAST         'pos'
518	BINARY_SUBSCR     None
519	LOAD_CONST        '(['
522	COMPARE_OP        'in'
525	POP_JUMP_IF_FALSE '531'

528	JUMP_ABSOLUTE     '536'

531	BREAK_LOOP        None
532	JUMP_BACK         '92'

535	BREAK_LOOP        None
536	JUMP_BACK         '92'
539	POP_BLOCK         None
540_0	COME_FROM         '89'

540	LOAD_FAST         'rawtext'
543	LOAD_FAST         'last_identifier_pos'
546	LOAD_FAST         'self'
549	LOAD_ATTR         'indexinrawtext'
552	SLICE+3           None
553	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 302