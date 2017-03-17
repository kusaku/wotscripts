# Embedded file name: scripts/common/Lib/sre_parse.py
"""Internal support module for sre"""
import sys
from sre_constants import *
SPECIAL_CHARS = '.\\[{()*+?^$|'
REPEAT_CHARS = '*+?{'
DIGITS = set('0123456789')
OCTDIGITS = set('01234567')
HEXDIGITS = set('0123456789abcdefABCDEF')
WHITESPACE = set(' \t\n\r\x0b\x0c')
ESCAPES = {'\\a': (LITERAL, ord('\x07')),
 '\\b': (LITERAL, ord('\x08')),
 '\\f': (LITERAL, ord('\x0c')),
 '\\n': (LITERAL, ord('\n')),
 '\\r': (LITERAL, ord('\r')),
 '\\t': (LITERAL, ord('\t')),
 '\\v': (LITERAL, ord('\x0b')),
 '\\\\': (LITERAL, ord('\\'))}
CATEGORIES = {'\\A': (AT, AT_BEGINNING_STRING),
 '\\b': (AT, AT_BOUNDARY),
 '\\B': (AT, AT_NON_BOUNDARY),
 '\\d': (IN, [(CATEGORY, CATEGORY_DIGIT)]),
 '\\D': (IN, [(CATEGORY, CATEGORY_NOT_DIGIT)]),
 '\\s': (IN, [(CATEGORY, CATEGORY_SPACE)]),
 '\\S': (IN, [(CATEGORY, CATEGORY_NOT_SPACE)]),
 '\\w': (IN, [(CATEGORY, CATEGORY_WORD)]),
 '\\W': (IN, [(CATEGORY, CATEGORY_NOT_WORD)]),
 '\\Z': (AT, AT_END_STRING)}
FLAGS = {'i': SRE_FLAG_IGNORECASE,
 'L': SRE_FLAG_LOCALE,
 'm': SRE_FLAG_MULTILINE,
 's': SRE_FLAG_DOTALL,
 'x': SRE_FLAG_VERBOSE,
 't': SRE_FLAG_TEMPLATE,
 'u': SRE_FLAG_UNICODE}

class Pattern():

    def __init__(self):
        self.flags = 0
        self.open = []
        self.groups = 1
        self.groupdict = {}

    def opengroup(self, name = None):
        gid = self.groups
        self.groups = gid + 1
        if name is not None:
            ogid = self.groupdict.get(name, None)
            if ogid is not None:
                raise error, 'redefinition of group name %s as group %d; was group %d' % (repr(name), gid, ogid)
            self.groupdict[name] = gid
        self.open.append(gid)
        return gid

    def closegroup(self, gid):
        self.open.remove(gid)

    def checkgroup(self, gid):
        return gid < self.groups and gid not in self.open


class SubPattern():

    def __init__(self, pattern, data = None):
        self.pattern = pattern
        if data is None:
            data = []
        self.data = data
        self.width = None
        return

    def dump(self, level = 0):
        nl = 1
        seqtypes = (type(()), type([]))
        for op, av in self.data:
            print level * '  ' + op,
            nl = 0
            if op == 'in':
                print
                nl = 1
                for op, a in av:
                    print (level + 1) * '  ' + op, a

            elif op == 'branch':
                print
                nl = 1
                i = 0
                for a in av[1]:
                    if i > 0:
                        print level * '  ' + 'or'
                    a.dump(level + 1)
                    nl = 1
                    i = i + 1

            elif type(av) in seqtypes:
                for a in av:
                    if isinstance(a, SubPattern):
                        if not nl:
                            print
                        a.dump(level + 1)
                        nl = 1
                    else:
                        print a,
                        nl = 0

            else:
                print av,
                nl = 0
            if not nl:
                print

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, index):
        del self.data[index]

    def __getitem__(self, index):
        if isinstance(index, slice):
            return SubPattern(self.pattern, self.data[index])
        return self.data[index]

    def __setitem__(self, index, code):
        self.data[index] = code

    def insert(self, index, code):
        self.data.insert(index, code)

    def append(self, code):
        self.data.append(code)

    def getwidth(self):
        if self.width:
            return self.width
        lo = hi = 0L
        UNITCODES = (ANY,
         RANGE,
         IN,
         LITERAL,
         NOT_LITERAL,
         CATEGORY)
        REPEATCODES = (MIN_REPEAT, MAX_REPEAT)
        for op, av in self.data:
            if op is BRANCH:
                i = sys.maxint
                j = 0
                for av in av[1]:
                    l, h = av.getwidth()
                    i = min(i, l)
                    j = max(j, h)

                lo = lo + i
                hi = hi + j
            elif op is CALL:
                i, j = av.getwidth()
                lo = lo + i
                hi = hi + j
            elif op is SUBPATTERN:
                i, j = av[1].getwidth()
                lo = lo + i
                hi = hi + j
            elif op in REPEATCODES:
                i, j = av[2].getwidth()
                lo = lo + long(i) * av[0]
                hi = hi + long(j) * av[1]
            elif op in UNITCODES:
                lo = lo + 1
                hi = hi + 1
            elif op == SUCCESS:
                break

        self.width = (int(min(lo, sys.maxint)), int(min(hi, sys.maxint)))
        return self.width


class Tokenizer():

    def __init__(self, string):
        self.string = string
        self.index = 0
        self.__next()

    def __next(self):
        if self.index >= len(self.string):
            self.next = None
            return
        else:
            char = self.string[self.index]
            if char[0] == '\\':
                try:
                    c = self.string[self.index + 1]
                except IndexError:
                    raise error, 'bogus escape (end of line)'

                char = char + c
            self.index = self.index + len(char)
            self.next = char
            return

    def match(self, char, skip = 1):
        if char == self.next:
            if skip:
                self.__next()
            return 1
        return 0

    def get(self):
        this = self.next
        self.__next()
        return this

    def tell(self):
        return (self.index, self.next)

    def seek(self, index):
        self.index, self.next = index


def isident(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char == '_'


def isdigit(char):
    return '0' <= char <= '9'


def isname(name):
    if not isident(name[0]):
        return False
    for char in name[1:]:
        if not isident(char) and not isdigit(char):
            return False

    return True


def _class_escape(source, escape):
    code = ESCAPES.get(escape)
    if code:
        return code
    code = CATEGORIES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == 'x':
            while source.next in HEXDIGITS and len(escape) < 4:
                escape = escape + source.get()

            escape = escape[2:]
            if len(escape) != 2:
                raise error, 'bogus escape: %s' % repr('\\' + escape)
            return (LITERAL, int(escape, 16) & 255)
        if c in OCTDIGITS:
            while source.next in OCTDIGITS and len(escape) < 4:
                escape = escape + source.get()

            escape = escape[1:]
            return (LITERAL, int(escape, 8) & 255)
        if c in DIGITS:
            raise error, 'bogus escape: %s' % repr(escape)
        if len(escape) == 2:
            return (LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise error, 'bogus escape: %s' % repr(escape)


def _escape(source, escape, state):
    code = CATEGORIES.get(escape)
    if code:
        return code
    code = ESCAPES.get(escape)
    if code:
        return code
    try:
        c = escape[1:2]
        if c == 'x':
            while source.next in HEXDIGITS and len(escape) < 4:
                escape = escape + source.get()

            if len(escape) != 4:
                raise ValueError
            return (LITERAL, int(escape[2:], 16) & 255)
        if c == '0':
            while source.next in OCTDIGITS and len(escape) < 4:
                escape = escape + source.get()

            return (LITERAL, int(escape[1:], 8) & 255)
        if c in DIGITS:
            if source.next in DIGITS:
                escape = escape + source.get()
                if escape[1] in OCTDIGITS and escape[2] in OCTDIGITS and source.next in OCTDIGITS:
                    escape = escape + source.get()
                    return (LITERAL, int(escape[1:], 8) & 255)
            group = int(escape[1:])
            if group < state.groups:
                if not state.checkgroup(group):
                    raise error, 'cannot refer to open group'
                return (GROUPREF, group)
            raise ValueError
        if len(escape) == 2:
            return (LITERAL, ord(escape[1]))
    except ValueError:
        pass

    raise error, 'bogus escape: %s' % repr(escape)


def _parse_sub--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'items'

6	LOAD_FAST         'items'
9	LOAD_ATTR         'append'
12	STORE_FAST        'itemsappend'

15	LOAD_FAST         'source'
18	LOAD_ATTR         'match'
21	STORE_FAST        'sourcematch'

24	SETUP_LOOP        '116'

27	LOAD_FAST         'itemsappend'
30	LOAD_GLOBAL       '_parse'
33	LOAD_FAST         'source'
36	LOAD_FAST         'state'
39	CALL_FUNCTION_2   None
42	CALL_FUNCTION_1   None
45	POP_TOP           None

46	LOAD_FAST         'sourcematch'
49	LOAD_CONST        '|'
52	CALL_FUNCTION_1   None
55	POP_JUMP_IF_FALSE '64'

58	CONTINUE          '27'
61	JUMP_FORWARD      '64'
64_0	COME_FROM         '61'

64	LOAD_FAST         'nested'
67	POP_JUMP_IF_TRUE  '74'

70	BREAK_LOOP        None
71	JUMP_FORWARD      '74'
74_0	COME_FROM         '71'

74	LOAD_FAST         'source'
77	LOAD_ATTR         'next'
80	UNARY_NOT         None
81	POP_JUMP_IF_TRUE  '99'
84	LOAD_FAST         'sourcematch'
87	LOAD_CONST        ')'
90	LOAD_CONST        0
93	CALL_FUNCTION_2   None
96_0	COME_FROM         '81'
96	POP_JUMP_IF_FALSE '103'

99	BREAK_LOOP        None
100	JUMP_BACK         '27'

103	LOAD_GLOBAL       'error'
106	LOAD_CONST        'pattern not properly closed'
109	RAISE_VARARGS_2   None
112	JUMP_BACK         '27'
115	POP_BLOCK         None
116_0	COME_FROM         '24'

116	LOAD_GLOBAL       'len'
119	LOAD_FAST         'items'
122	CALL_FUNCTION_1   None
125	LOAD_CONST        1
128	COMPARE_OP        '=='
131	POP_JUMP_IF_FALSE '142'

134	LOAD_FAST         'items'
137	LOAD_CONST        0
140	BINARY_SUBSCR     None
141	RETURN_END_IF     None

142	LOAD_GLOBAL       'SubPattern'
145	LOAD_FAST         'state'
148	CALL_FUNCTION_1   None
151	STORE_FAST        'subpattern'

154	LOAD_FAST         'subpattern'
157	LOAD_ATTR         'append'
160	STORE_FAST        'subpatternappend'

163	SETUP_LOOP        '286'

166	LOAD_CONST        None
169	STORE_FAST        'prefix'

172	SETUP_LOOP        '281'
175	LOAD_FAST         'items'
178	GET_ITER          None
179	FOR_ITER          '243'
182	STORE_FAST        'item'

185	LOAD_FAST         'item'
188	POP_JUMP_IF_TRUE  '195'

191	BREAK_LOOP        None
192	JUMP_FORWARD      '195'
195_0	COME_FROM         '192'

195	LOAD_FAST         'prefix'
198	LOAD_CONST        None
201	COMPARE_OP        'is'
204	POP_JUMP_IF_FALSE '220'

207	LOAD_FAST         'item'
210	LOAD_CONST        0
213	BINARY_SUBSCR     None
214	STORE_FAST        'prefix'
217	JUMP_BACK         '179'

220	LOAD_FAST         'item'
223	LOAD_CONST        0
226	BINARY_SUBSCR     None
227	LOAD_FAST         'prefix'
230	COMPARE_OP        '!='
233	POP_JUMP_IF_FALSE '179'

236	BREAK_LOOP        None
237	JUMP_BACK         '179'
240	JUMP_BACK         '179'
243	POP_BLOCK         None

244	SETUP_LOOP        '268'
247	LOAD_FAST         'items'
250	GET_ITER          None
251	FOR_ITER          '267'
254	STORE_FAST        'item'

257	LOAD_FAST         'item'
260	LOAD_CONST        0
263	DELETE_SUBSCR     None
264	JUMP_BACK         '251'
267	POP_BLOCK         None
268_0	COME_FROM         '244'

268	LOAD_FAST         'subpatternappend'
271	LOAD_FAST         'prefix'
274	CALL_FUNCTION_1   None
277	POP_TOP           None

278	CONTINUE          '166'
281_0	COME_FROM         '172'

281	BREAK_LOOP        None
282	JUMP_BACK         '166'
285	POP_BLOCK         None
286_0	COME_FROM         '163'

286	SETUP_LOOP        '411'
289	LOAD_FAST         'items'
292	GET_ITER          None
293	FOR_ITER          '344'
296	STORE_FAST        'item'

299	LOAD_GLOBAL       'len'
302	LOAD_FAST         'item'
305	CALL_FUNCTION_1   None
308	LOAD_CONST        1
311	COMPARE_OP        '!='
314	POP_JUMP_IF_TRUE  '337'
317	LOAD_FAST         'item'
320	LOAD_CONST        0
323	BINARY_SUBSCR     None
324	LOAD_CONST        0
327	BINARY_SUBSCR     None
328	LOAD_GLOBAL       'LITERAL'
331	COMPARE_OP        '!='
334_0	COME_FROM         '314'
334	POP_JUMP_IF_FALSE '293'

337	BREAK_LOOP        None
338	JUMP_BACK         '293'
341	JUMP_BACK         '293'
344	POP_BLOCK         None

345	BUILD_LIST_0      None
348	STORE_FAST        'set'

351	LOAD_FAST         'set'
354	LOAD_ATTR         'append'
357	STORE_FAST        'setappend'

360	SETUP_LOOP        '391'
363	LOAD_FAST         'items'
366	GET_ITER          None
367	FOR_ITER          '390'
370	STORE_FAST        'item'

373	LOAD_FAST         'setappend'
376	LOAD_FAST         'item'
379	LOAD_CONST        0
382	BINARY_SUBSCR     None
383	CALL_FUNCTION_1   None
386	POP_TOP           None
387	JUMP_BACK         '367'
390	POP_BLOCK         None
391_0	COME_FROM         '360'

391	LOAD_FAST         'subpatternappend'
394	LOAD_GLOBAL       'IN'
397	LOAD_FAST         'set'
400	BUILD_TUPLE_2     None
403	CALL_FUNCTION_1   None
406	POP_TOP           None

407	LOAD_FAST         'subpattern'
410	RETURN_VALUE      None
411_0	COME_FROM         '286'

411	LOAD_FAST         'subpattern'
414	LOAD_ATTR         'append'
417	LOAD_GLOBAL       'BRANCH'
420	LOAD_CONST        None
423	LOAD_FAST         'items'
426	BUILD_TUPLE_2     None
429	BUILD_TUPLE_2     None
432	CALL_FUNCTION_1   None
435	POP_TOP           None

436	LOAD_FAST         'subpattern'
439	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 115


def _parse_sub_cond(source, state, condgroup):
    item_yes = _parse(source, state)
    if source.match('|'):
        item_no = _parse(source, state)
        if source.match('|'):
            raise error, 'conditional backref with more than two branches'
    else:
        item_no = None
    if source.next and not source.match(')', 0):
        raise error, 'pattern not properly closed'
    subpattern = SubPattern(state)
    subpattern.append((GROUPREF_EXISTS, (condgroup, item_yes, item_no)))
    return subpattern


_PATTERNENDERS = set('|)')
_ASSERTCHARS = set('=!<')
_LOOKBEHINDASSERTCHARS = set('=!')
_REPEATCODES = set([MIN_REPEAT, MAX_REPEAT])

def _parse--- This code section failed: ---

0	LOAD_GLOBAL       'SubPattern'
3	LOAD_FAST         'state'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'subpattern'

12	LOAD_FAST         'subpattern'
15	LOAD_ATTR         'append'
18	STORE_FAST        'subpatternappend'

21	LOAD_FAST         'source'
24	LOAD_ATTR         'get'
27	STORE_FAST        'sourceget'

30	LOAD_FAST         'source'
33	LOAD_ATTR         'match'
36	STORE_FAST        'sourcematch'

39	LOAD_GLOBAL       'len'
42	STORE_FAST        '_len'

45	LOAD_GLOBAL       '_PATTERNENDERS'
48	STORE_FAST        'PATTERNENDERS'

51	LOAD_GLOBAL       '_ASSERTCHARS'
54	STORE_FAST        'ASSERTCHARS'

57	LOAD_GLOBAL       '_LOOKBEHINDASSERTCHARS'
60	STORE_FAST        'LOOKBEHINDASSERTCHARS'

63	LOAD_GLOBAL       '_REPEATCODES'
66	STORE_FAST        'REPEATCODES'

69	SETUP_LOOP        '2882'

72	LOAD_FAST         'source'
75	LOAD_ATTR         'next'
78	LOAD_FAST         'PATTERNENDERS'
81	COMPARE_OP        'in'
84	POP_JUMP_IF_FALSE '91'

87	BREAK_LOOP        None
88	JUMP_FORWARD      '91'
91_0	COME_FROM         '88'

91	LOAD_FAST         'sourceget'
94	CALL_FUNCTION_0   None
97	STORE_FAST        'this'

100	LOAD_FAST         'this'
103	LOAD_CONST        None
106	COMPARE_OP        'is'
109	POP_JUMP_IF_FALSE '116'

112	BREAK_LOOP        None
113	JUMP_FORWARD      '116'
116_0	COME_FROM         '113'

116	LOAD_FAST         'state'
119	LOAD_ATTR         'flags'
122	LOAD_GLOBAL       'SRE_FLAG_VERBOSE'
125	BINARY_AND        None
126	POP_JUMP_IF_FALSE '200'

129	LOAD_FAST         'this'
132	LOAD_GLOBAL       'WHITESPACE'
135	COMPARE_OP        'in'
138	POP_JUMP_IF_FALSE '147'

141	CONTINUE          '72'
144	JUMP_FORWARD      '147'
147_0	COME_FROM         '144'

147	LOAD_FAST         'this'
150	LOAD_CONST        '#'
153	COMPARE_OP        '=='
156	POP_JUMP_IF_FALSE '200'

159	SETUP_LOOP        '191'

162	LOAD_FAST         'sourceget'
165	CALL_FUNCTION_0   None
168	STORE_FAST        'this'

171	LOAD_FAST         'this'
174	LOAD_CONST        (None, '\n')
177	COMPARE_OP        'in'
180	POP_JUMP_IF_FALSE '162'

183	BREAK_LOOP        None
184	JUMP_BACK         '162'
187	JUMP_BACK         '162'
190	POP_BLOCK         None
191_0	COME_FROM         '159'

191	CONTINUE          '72'
194	JUMP_ABSOLUTE     '200'
197	JUMP_FORWARD      '200'
200_0	COME_FROM         '197'

200	LOAD_FAST         'this'
203	POP_JUMP_IF_FALSE '247'
206	LOAD_FAST         'this'
209	LOAD_CONST        0
212	BINARY_SUBSCR     None
213	LOAD_GLOBAL       'SPECIAL_CHARS'
216	COMPARE_OP        'not in'
219_0	COME_FROM         '203'
219	POP_JUMP_IF_FALSE '247'

222	LOAD_FAST         'subpatternappend'
225	LOAD_GLOBAL       'LITERAL'
228	LOAD_GLOBAL       'ord'
231	LOAD_FAST         'this'
234	CALL_FUNCTION_1   None
237	BUILD_TUPLE_2     None
240	CALL_FUNCTION_1   None
243	POP_TOP           None
244	JUMP_BACK         '72'

247	LOAD_FAST         'this'
250	LOAD_CONST        '['
253	COMPARE_OP        '=='
256	POP_JUMP_IF_FALSE '919'

259	BUILD_LIST_0      None
262	STORE_FAST        'set'

265	LOAD_FAST         'set'
268	LOAD_ATTR         'append'
271	STORE_FAST        'setappend'

274	LOAD_FAST         'sourcematch'
277	LOAD_CONST        '^'
280	CALL_FUNCTION_1   None
283	POP_JUMP_IF_FALSE '305'

286	LOAD_FAST         'setappend'
289	LOAD_GLOBAL       'NEGATE'
292	LOAD_CONST        None
295	BUILD_TUPLE_2     None
298	CALL_FUNCTION_1   None
301	POP_TOP           None
302	JUMP_FORWARD      '305'
305_0	COME_FROM         '302'

305	LOAD_FAST         'set'
308	SLICE+0           None
309	STORE_FAST        'start'

312	SETUP_LOOP        '760'

315	LOAD_FAST         'sourceget'
318	CALL_FUNCTION_0   None
321	STORE_FAST        'this'

324	LOAD_FAST         'this'
327	LOAD_CONST        ']'
330	COMPARE_OP        '=='
333	POP_JUMP_IF_FALSE '352'
336	LOAD_FAST         'set'
339	LOAD_FAST         'start'
342	COMPARE_OP        '!='
345_0	COME_FROM         '333'
345	POP_JUMP_IF_FALSE '352'

348	BREAK_LOOP        None
349	JUMP_FORWARD      '428'

352	LOAD_FAST         'this'
355	POP_JUMP_IF_FALSE '392'
358	LOAD_FAST         'this'
361	LOAD_CONST        0
364	BINARY_SUBSCR     None
365	LOAD_CONST        '\\'
368	COMPARE_OP        '=='
371_0	COME_FROM         '355'
371	POP_JUMP_IF_FALSE '392'

374	LOAD_GLOBAL       '_class_escape'
377	LOAD_FAST         'source'
380	LOAD_FAST         'this'
383	CALL_FUNCTION_2   None
386	STORE_FAST        'code1'
389	JUMP_FORWARD      '428'

392	LOAD_FAST         'this'
395	POP_JUMP_IF_FALSE '419'

398	LOAD_GLOBAL       'LITERAL'
401	LOAD_GLOBAL       'ord'
404	LOAD_FAST         'this'
407	CALL_FUNCTION_1   None
410	BUILD_TUPLE_2     None
413	STORE_FAST        'code1'
416	JUMP_FORWARD      '428'

419	LOAD_GLOBAL       'error'
422	LOAD_CONST        'unexpected end of regular expression'
425	RAISE_VARARGS_2   None
428_0	COME_FROM         '349'
428_1	COME_FROM         '389'
428_2	COME_FROM         '416'

428	LOAD_FAST         'sourcematch'
431	LOAD_CONST        '-'
434	CALL_FUNCTION_1   None
437	POP_JUMP_IF_FALSE '713'

440	LOAD_FAST         'sourceget'
443	CALL_FUNCTION_0   None
446	STORE_FAST        'this'

449	LOAD_FAST         'this'
452	LOAD_CONST        ']'
455	COMPARE_OP        '=='
458	POP_JUMP_IF_FALSE '530'

461	LOAD_FAST         'code1'
464	LOAD_CONST        0
467	BINARY_SUBSCR     None
468	LOAD_GLOBAL       'IN'
471	COMPARE_OP        'is'
474	POP_JUMP_IF_FALSE '494'

477	LOAD_FAST         'code1'
480	LOAD_CONST        1
483	BINARY_SUBSCR     None
484	LOAD_CONST        0
487	BINARY_SUBSCR     None
488	STORE_FAST        'code1'
491	JUMP_FORWARD      '494'
494_0	COME_FROM         '491'

494	LOAD_FAST         'setappend'
497	LOAD_FAST         'code1'
500	CALL_FUNCTION_1   None
503	POP_TOP           None

504	LOAD_FAST         'setappend'
507	LOAD_GLOBAL       'LITERAL'
510	LOAD_GLOBAL       'ord'
513	LOAD_CONST        '-'
516	CALL_FUNCTION_1   None
519	BUILD_TUPLE_2     None
522	CALL_FUNCTION_1   None
525	POP_TOP           None

526	BREAK_LOOP        None
527	JUMP_ABSOLUTE     '756'

530	LOAD_FAST         'this'
533	POP_JUMP_IF_FALSE '701'

536	LOAD_FAST         'this'
539	LOAD_CONST        0
542	BINARY_SUBSCR     None
543	LOAD_CONST        '\\'
546	COMPARE_OP        '=='
549	POP_JUMP_IF_FALSE '570'

552	LOAD_GLOBAL       '_class_escape'
555	LOAD_FAST         'source'
558	LOAD_FAST         'this'
561	CALL_FUNCTION_2   None
564	STORE_FAST        'code2'
567	JUMP_FORWARD      '588'

570	LOAD_GLOBAL       'LITERAL'
573	LOAD_GLOBAL       'ord'
576	LOAD_FAST         'this'
579	CALL_FUNCTION_1   None
582	BUILD_TUPLE_2     None
585	STORE_FAST        'code2'
588_0	COME_FROM         '567'

588	LOAD_FAST         'code1'
591	LOAD_CONST        0
594	BINARY_SUBSCR     None
595	LOAD_GLOBAL       'LITERAL'
598	COMPARE_OP        '!='
601	POP_JUMP_IF_TRUE  '620'
604	LOAD_FAST         'code2'
607	LOAD_CONST        0
610	BINARY_SUBSCR     None
611	LOAD_GLOBAL       'LITERAL'
614	COMPARE_OP        '!='
617_0	COME_FROM         '601'
617	POP_JUMP_IF_FALSE '632'

620	LOAD_GLOBAL       'error'
623	LOAD_CONST        'bad character range'
626	RAISE_VARARGS_2   None
629	JUMP_FORWARD      '632'
632_0	COME_FROM         '629'

632	LOAD_FAST         'code1'
635	LOAD_CONST        1
638	BINARY_SUBSCR     None
639	STORE_FAST        'lo'

642	LOAD_FAST         'code2'
645	LOAD_CONST        1
648	BINARY_SUBSCR     None
649	STORE_FAST        'hi'

652	LOAD_FAST         'hi'
655	LOAD_FAST         'lo'
658	COMPARE_OP        '<'
661	POP_JUMP_IF_FALSE '676'

664	LOAD_GLOBAL       'error'
667	LOAD_CONST        'bad character range'
670	RAISE_VARARGS_2   None
673	JUMP_FORWARD      '676'
676_0	COME_FROM         '673'

676	LOAD_FAST         'setappend'
679	LOAD_GLOBAL       'RANGE'
682	LOAD_FAST         'lo'
685	LOAD_FAST         'hi'
688	BUILD_TUPLE_2     None
691	BUILD_TUPLE_2     None
694	CALL_FUNCTION_1   None
697	POP_TOP           None
698	JUMP_ABSOLUTE     '756'

701	LOAD_GLOBAL       'error'
704	LOAD_CONST        'unexpected end of regular expression'
707	RAISE_VARARGS_2   None
710	JUMP_BACK         '315'

713	LOAD_FAST         'code1'
716	LOAD_CONST        0
719	BINARY_SUBSCR     None
720	LOAD_GLOBAL       'IN'
723	COMPARE_OP        'is'
726	POP_JUMP_IF_FALSE '746'

729	LOAD_FAST         'code1'
732	LOAD_CONST        1
735	BINARY_SUBSCR     None
736	LOAD_CONST        0
739	BINARY_SUBSCR     None
740	STORE_FAST        'code1'
743	JUMP_FORWARD      '746'
746_0	COME_FROM         '743'

746	LOAD_FAST         'setappend'
749	LOAD_FAST         'code1'
752	CALL_FUNCTION_1   None
755	POP_TOP           None
756	JUMP_BACK         '315'
759	POP_BLOCK         None
760_0	COME_FROM         '312'

760	LOAD_FAST         '_len'
763	LOAD_FAST         'set'
766	CALL_FUNCTION_1   None
769	LOAD_CONST        1
772	COMPARE_OP        '=='
775	POP_JUMP_IF_FALSE '815'
778	LOAD_FAST         'set'
781	LOAD_CONST        0
784	BINARY_SUBSCR     None
785	LOAD_CONST        0
788	BINARY_SUBSCR     None
789	LOAD_GLOBAL       'LITERAL'
792	COMPARE_OP        'is'
795_0	COME_FROM         '775'
795	POP_JUMP_IF_FALSE '815'

798	LOAD_FAST         'subpatternappend'
801	LOAD_FAST         'set'
804	LOAD_CONST        0
807	BINARY_SUBSCR     None
808	CALL_FUNCTION_1   None
811	POP_TOP           None
812	JUMP_ABSOLUTE     '2878'

815	LOAD_FAST         '_len'
818	LOAD_FAST         'set'
821	CALL_FUNCTION_1   None
824	LOAD_CONST        2
827	COMPARE_OP        '=='
830	POP_JUMP_IF_FALSE '900'
833	LOAD_FAST         'set'
836	LOAD_CONST        0
839	BINARY_SUBSCR     None
840	LOAD_CONST        0
843	BINARY_SUBSCR     None
844	LOAD_GLOBAL       'NEGATE'
847	COMPARE_OP        'is'
850	POP_JUMP_IF_FALSE '900'
853	LOAD_FAST         'set'
856	LOAD_CONST        1
859	BINARY_SUBSCR     None
860	LOAD_CONST        0
863	BINARY_SUBSCR     None
864	LOAD_GLOBAL       'LITERAL'
867	COMPARE_OP        'is'
870_0	COME_FROM         '830'
870_1	COME_FROM         '850'
870	POP_JUMP_IF_FALSE '900'

873	LOAD_FAST         'subpatternappend'
876	LOAD_GLOBAL       'NOT_LITERAL'
879	LOAD_FAST         'set'
882	LOAD_CONST        1
885	BINARY_SUBSCR     None
886	LOAD_CONST        1
889	BINARY_SUBSCR     None
890	BUILD_TUPLE_2     None
893	CALL_FUNCTION_1   None
896	POP_TOP           None
897	JUMP_ABSOLUTE     '2878'

900	LOAD_FAST         'subpatternappend'
903	LOAD_GLOBAL       'IN'
906	LOAD_FAST         'set'
909	BUILD_TUPLE_2     None
912	CALL_FUNCTION_1   None
915	POP_TOP           None
916	JUMP_BACK         '72'

919	LOAD_FAST         'this'
922	POP_JUMP_IF_FALSE '1521'
925	LOAD_FAST         'this'
928	LOAD_CONST        0
931	BINARY_SUBSCR     None
932	LOAD_GLOBAL       'REPEAT_CHARS'
935	COMPARE_OP        'in'
938_0	COME_FROM         '922'
938	POP_JUMP_IF_FALSE '1521'

941	LOAD_FAST         'this'
944	LOAD_CONST        '?'
947	COMPARE_OP        '=='
950	POP_JUMP_IF_FALSE '968'

953	LOAD_CONST        (0, 1)
956	UNPACK_SEQUENCE_2 None
959	STORE_FAST        'min'
962	STORE_FAST        'max'
965	JUMP_FORWARD      '1339'

968	LOAD_FAST         'this'
971	LOAD_CONST        '*'
974	COMPARE_OP        '=='
977	POP_JUMP_IF_FALSE '996'

980	LOAD_CONST        0
983	LOAD_GLOBAL       'MAXREPEAT'
986	ROT_TWO           None
987	STORE_FAST        'min'
990	STORE_FAST        'max'
993	JUMP_FORWARD      '1339'

996	LOAD_FAST         'this'
999	LOAD_CONST        '+'
1002	COMPARE_OP        '=='
1005	POP_JUMP_IF_FALSE '1024'

1008	LOAD_CONST        1
1011	LOAD_GLOBAL       'MAXREPEAT'
1014	ROT_TWO           None
1015	STORE_FAST        'min'
1018	STORE_FAST        'max'
1021	JUMP_FORWARD      '1339'

1024	LOAD_FAST         'this'
1027	LOAD_CONST        '{'
1030	COMPARE_OP        '=='
1033	POP_JUMP_IF_FALSE '1330'

1036	LOAD_FAST         'source'
1039	LOAD_ATTR         'next'
1042	LOAD_CONST        '}'
1045	COMPARE_OP        '=='
1048	POP_JUMP_IF_FALSE '1079'

1051	LOAD_FAST         'subpatternappend'
1054	LOAD_GLOBAL       'LITERAL'
1057	LOAD_GLOBAL       'ord'
1060	LOAD_FAST         'this'
1063	CALL_FUNCTION_1   None
1066	BUILD_TUPLE_2     None
1069	CALL_FUNCTION_1   None
1072	POP_TOP           None

1073	CONTINUE          '72'
1076	JUMP_FORWARD      '1079'
1079_0	COME_FROM         '1076'

1079	LOAD_FAST         'source'
1082	LOAD_ATTR         'tell'
1085	CALL_FUNCTION_0   None
1088	STORE_FAST        'here'

1091	LOAD_CONST        0
1094	LOAD_GLOBAL       'MAXREPEAT'
1097	ROT_TWO           None
1098	STORE_FAST        'min'
1101	STORE_FAST        'max'

1104	LOAD_CONST        ''
1107	DUP_TOP           None
1108	STORE_FAST        'lo'
1111	STORE_FAST        'hi'

1114	SETUP_LOOP        '1152'
1117	LOAD_FAST         'source'
1120	LOAD_ATTR         'next'
1123	LOAD_GLOBAL       'DIGITS'
1126	COMPARE_OP        'in'
1129	POP_JUMP_IF_FALSE '1151'

1132	LOAD_FAST         'lo'
1135	LOAD_FAST         'source'
1138	LOAD_ATTR         'get'
1141	CALL_FUNCTION_0   None
1144	BINARY_ADD        None
1145	STORE_FAST        'lo'
1148	JUMP_BACK         '1117'
1151	POP_BLOCK         None
1152_0	COME_FROM         '1114'

1152	LOAD_FAST         'sourcematch'
1155	LOAD_CONST        ','
1158	CALL_FUNCTION_1   None
1161	POP_JUMP_IF_FALSE '1202'

1164	SETUP_LOOP        '1208'
1167	LOAD_FAST         'source'
1170	LOAD_ATTR         'next'
1173	LOAD_GLOBAL       'DIGITS'
1176	COMPARE_OP        'in'
1179	POP_JUMP_IF_FALSE '1198'

1182	LOAD_FAST         'hi'
1185	LOAD_FAST         'sourceget'
1188	CALL_FUNCTION_0   None
1191	BINARY_ADD        None
1192	STORE_FAST        'hi'
1195	JUMP_BACK         '1167'
1198	POP_BLOCK         None
1199_0	COME_FROM         '1164'
1199	JUMP_FORWARD      '1208'

1202	LOAD_FAST         'lo'
1205	STORE_FAST        'hi'
1208_0	COME_FROM         '1199'

1208	LOAD_FAST         'sourcematch'
1211	LOAD_CONST        '}'
1214	CALL_FUNCTION_1   None
1217	POP_JUMP_IF_TRUE  '1261'

1220	LOAD_FAST         'subpatternappend'
1223	LOAD_GLOBAL       'LITERAL'
1226	LOAD_GLOBAL       'ord'
1229	LOAD_FAST         'this'
1232	CALL_FUNCTION_1   None
1235	BUILD_TUPLE_2     None
1238	CALL_FUNCTION_1   None
1241	POP_TOP           None

1242	LOAD_FAST         'source'
1245	LOAD_ATTR         'seek'
1248	LOAD_FAST         'here'
1251	CALL_FUNCTION_1   None
1254	POP_TOP           None

1255	CONTINUE          '72'
1258	JUMP_FORWARD      '1261'
1261_0	COME_FROM         '1258'

1261	LOAD_FAST         'lo'
1264	POP_JUMP_IF_FALSE '1282'

1267	LOAD_GLOBAL       'int'
1270	LOAD_FAST         'lo'
1273	CALL_FUNCTION_1   None
1276	STORE_FAST        'min'
1279	JUMP_FORWARD      '1282'
1282_0	COME_FROM         '1279'

1282	LOAD_FAST         'hi'
1285	POP_JUMP_IF_FALSE '1303'

1288	LOAD_GLOBAL       'int'
1291	LOAD_FAST         'hi'
1294	CALL_FUNCTION_1   None
1297	STORE_FAST        'max'
1300	JUMP_FORWARD      '1303'
1303_0	COME_FROM         '1300'

1303	LOAD_FAST         'max'
1306	LOAD_FAST         'min'
1309	COMPARE_OP        '<'
1312	POP_JUMP_IF_FALSE '1339'

1315	LOAD_GLOBAL       'error'
1318	LOAD_CONST        'bad repeat interval'
1321	RAISE_VARARGS_2   None
1324	JUMP_ABSOLUTE     '1339'
1327	JUMP_FORWARD      '1339'

1330	LOAD_GLOBAL       'error'
1333	LOAD_CONST        'not supported'
1336	RAISE_VARARGS_2   None
1339_0	COME_FROM         '965'
1339_1	COME_FROM         '993'
1339_2	COME_FROM         '1021'
1339_3	COME_FROM         '1327'

1339	LOAD_FAST         'subpattern'
1342	POP_JUMP_IF_FALSE '1358'

1345	LOAD_FAST         'subpattern'
1348	LOAD_CONST        -1
1351	SLICE+1           None
1352	STORE_FAST        'item'
1355	JUMP_FORWARD      '1364'

1358	LOAD_CONST        None
1361	STORE_FAST        'item'
1364_0	COME_FROM         '1355'

1364	LOAD_FAST         'item'
1367	UNARY_NOT         None
1368	POP_JUMP_IF_TRUE  '1409'
1371	LOAD_FAST         '_len'
1374	LOAD_FAST         'item'
1377	CALL_FUNCTION_1   None
1380	LOAD_CONST        1
1383	COMPARE_OP        '=='
1386	POP_JUMP_IF_FALSE '1421'
1389	LOAD_FAST         'item'
1392	LOAD_CONST        0
1395	BINARY_SUBSCR     None
1396	LOAD_CONST        0
1399	BINARY_SUBSCR     None
1400	LOAD_GLOBAL       'AT'
1403	COMPARE_OP        '=='
1406_0	COME_FROM         '1368'
1406_1	COME_FROM         '1386'
1406	POP_JUMP_IF_FALSE '1421'

1409	LOAD_GLOBAL       'error'
1412	LOAD_CONST        'nothing to repeat'
1415	RAISE_VARARGS_2   None
1418	JUMP_FORWARD      '1421'
1421_0	COME_FROM         '1418'

1421	LOAD_FAST         'item'
1424	LOAD_CONST        0
1427	BINARY_SUBSCR     None
1428	LOAD_CONST        0
1431	BINARY_SUBSCR     None
1432	LOAD_FAST         'REPEATCODES'
1435	COMPARE_OP        'in'
1438	POP_JUMP_IF_FALSE '1453'

1441	LOAD_GLOBAL       'error'
1444	LOAD_CONST        'multiple repeat'
1447	RAISE_VARARGS_2   None
1450	JUMP_FORWARD      '1453'
1453_0	COME_FROM         '1450'

1453	LOAD_FAST         'sourcematch'
1456	LOAD_CONST        '?'
1459	CALL_FUNCTION_1   None
1462	POP_JUMP_IF_FALSE '1493'

1465	LOAD_GLOBAL       'MIN_REPEAT'
1468	LOAD_FAST         'min'
1471	LOAD_FAST         'max'
1474	LOAD_FAST         'item'
1477	BUILD_TUPLE_3     None
1480	BUILD_TUPLE_2     None
1483	LOAD_FAST         'subpattern'
1486	LOAD_CONST        -1
1489	STORE_SUBSCR      None
1490	JUMP_ABSOLUTE     '2878'

1493	LOAD_GLOBAL       'MAX_REPEAT'
1496	LOAD_FAST         'min'
1499	LOAD_FAST         'max'
1502	LOAD_FAST         'item'
1505	BUILD_TUPLE_3     None
1508	BUILD_TUPLE_2     None
1511	LOAD_FAST         'subpattern'
1514	LOAD_CONST        -1
1517	STORE_SUBSCR      None
1518	JUMP_BACK         '72'

1521	LOAD_FAST         'this'
1524	LOAD_CONST        '.'
1527	COMPARE_OP        '=='
1530	POP_JUMP_IF_FALSE '1552'

1533	LOAD_FAST         'subpatternappend'
1536	LOAD_GLOBAL       'ANY'
1539	LOAD_CONST        None
1542	BUILD_TUPLE_2     None
1545	CALL_FUNCTION_1   None
1548	POP_TOP           None
1549	JUMP_BACK         '72'

1552	LOAD_FAST         'this'
1555	LOAD_CONST        '('
1558	COMPARE_OP        '=='
1561	POP_JUMP_IF_FALSE '2751'

1564	LOAD_CONST        1
1567	STORE_FAST        'group'

1570	LOAD_CONST        None
1573	STORE_FAST        'name'

1576	LOAD_CONST        None
1579	STORE_FAST        'condgroup'

1582	LOAD_FAST         'sourcematch'
1585	LOAD_CONST        '?'
1588	CALL_FUNCTION_1   None
1591	POP_JUMP_IF_FALSE '2522'

1594	LOAD_CONST        0
1597	STORE_FAST        'group'

1600	LOAD_FAST         'sourcematch'
1603	LOAD_CONST        'P'
1606	CALL_FUNCTION_1   None
1609	POP_JUMP_IF_FALSE '1950'

1612	LOAD_FAST         'sourcematch'
1615	LOAD_CONST        '<'
1618	CALL_FUNCTION_1   None
1621	POP_JUMP_IF_FALSE '1729'

1624	LOAD_CONST        ''
1627	STORE_FAST        'name'

1630	SETUP_LOOP        '1696'

1633	LOAD_FAST         'sourceget'
1636	CALL_FUNCTION_0   None
1639	STORE_FAST        'char'

1642	LOAD_FAST         'char'
1645	LOAD_CONST        None
1648	COMPARE_OP        'is'
1651	POP_JUMP_IF_FALSE '1666'

1654	LOAD_GLOBAL       'error'
1657	LOAD_CONST        'unterminated name'
1660	RAISE_VARARGS_2   None
1663	JUMP_FORWARD      '1666'
1666_0	COME_FROM         '1663'

1666	LOAD_FAST         'char'
1669	LOAD_CONST        '>'
1672	COMPARE_OP        '=='
1675	POP_JUMP_IF_FALSE '1682'

1678	BREAK_LOOP        None
1679	JUMP_FORWARD      '1682'
1682_0	COME_FROM         '1679'

1682	LOAD_FAST         'name'
1685	LOAD_FAST         'char'
1688	BINARY_ADD        None
1689	STORE_FAST        'name'
1692	JUMP_BACK         '1633'
1695	POP_BLOCK         None
1696_0	COME_FROM         '1630'

1696	LOAD_CONST        1
1699	STORE_FAST        'group'

1702	LOAD_GLOBAL       'isname'
1705	LOAD_FAST         'name'
1708	CALL_FUNCTION_1   None
1711	POP_JUMP_IF_TRUE  '1947'

1714	LOAD_GLOBAL       'error'
1717	LOAD_CONST        'bad character in group name'
1720	RAISE_VARARGS_2   None
1723	JUMP_ABSOLUTE     '1947'
1726	JUMP_ABSOLUTE     '2519'

1729	LOAD_FAST         'sourcematch'
1732	LOAD_CONST        '='
1735	CALL_FUNCTION_1   None
1738	POP_JUMP_IF_FALSE '1901'

1741	LOAD_CONST        ''
1744	STORE_FAST        'name'

1747	SETUP_LOOP        '1813'

1750	LOAD_FAST         'sourceget'
1753	CALL_FUNCTION_0   None
1756	STORE_FAST        'char'

1759	LOAD_FAST         'char'
1762	LOAD_CONST        None
1765	COMPARE_OP        'is'
1768	POP_JUMP_IF_FALSE '1783'

1771	LOAD_GLOBAL       'error'
1774	LOAD_CONST        'unterminated name'
1777	RAISE_VARARGS_2   None
1780	JUMP_FORWARD      '1783'
1783_0	COME_FROM         '1780'

1783	LOAD_FAST         'char'
1786	LOAD_CONST        ')'
1789	COMPARE_OP        '=='
1792	POP_JUMP_IF_FALSE '1799'

1795	BREAK_LOOP        None
1796	JUMP_FORWARD      '1799'
1799_0	COME_FROM         '1796'

1799	LOAD_FAST         'name'
1802	LOAD_FAST         'char'
1805	BINARY_ADD        None
1806	STORE_FAST        'name'
1809	JUMP_BACK         '1750'
1812	POP_BLOCK         None
1813_0	COME_FROM         '1747'

1813	LOAD_GLOBAL       'isname'
1816	LOAD_FAST         'name'
1819	CALL_FUNCTION_1   None
1822	POP_JUMP_IF_TRUE  '1837'

1825	LOAD_GLOBAL       'error'
1828	LOAD_CONST        'bad character in group name'
1831	RAISE_VARARGS_2   None
1834	JUMP_FORWARD      '1837'
1837_0	COME_FROM         '1834'

1837	LOAD_FAST         'state'
1840	LOAD_ATTR         'groupdict'
1843	LOAD_ATTR         'get'
1846	LOAD_FAST         'name'
1849	CALL_FUNCTION_1   None
1852	STORE_FAST        'gid'

1855	LOAD_FAST         'gid'
1858	LOAD_CONST        None
1861	COMPARE_OP        'is'
1864	POP_JUMP_IF_FALSE '1879'

1867	LOAD_GLOBAL       'error'
1870	LOAD_CONST        'unknown group name'
1873	RAISE_VARARGS_2   None
1876	JUMP_FORWARD      '1879'
1879_0	COME_FROM         '1876'

1879	LOAD_FAST         'subpatternappend'
1882	LOAD_GLOBAL       'GROUPREF'
1885	LOAD_FAST         'gid'
1888	BUILD_TUPLE_2     None
1891	CALL_FUNCTION_1   None
1894	POP_TOP           None

1895	CONTINUE          '72'
1898	JUMP_ABSOLUTE     '2519'

1901	LOAD_FAST         'sourceget'
1904	CALL_FUNCTION_0   None
1907	STORE_FAST        'char'

1910	LOAD_FAST         'char'
1913	LOAD_CONST        None
1916	COMPARE_OP        'is'
1919	POP_JUMP_IF_FALSE '1934'

1922	LOAD_GLOBAL       'error'
1925	LOAD_CONST        'unexpected end of pattern'
1928	RAISE_VARARGS_2   None
1931	JUMP_FORWARD      '1934'
1934_0	COME_FROM         '1931'

1934	LOAD_GLOBAL       'error'
1937	LOAD_CONST        'unknown specifier: ?P%s'
1940	LOAD_FAST         'char'
1943	BINARY_MODULO     None
1944	RAISE_VARARGS_2   None
1947	JUMP_ABSOLUTE     '2522'

1950	LOAD_FAST         'sourcematch'
1953	LOAD_CONST        ':'
1956	CALL_FUNCTION_1   None
1959	POP_JUMP_IF_FALSE '1971'

1962	LOAD_CONST        2
1965	STORE_FAST        'group'
1968	JUMP_ABSOLUTE     '2522'

1971	LOAD_FAST         'sourcematch'
1974	LOAD_CONST        '#'
1977	CALL_FUNCTION_1   None
1980	POP_JUMP_IF_FALSE '2061'

1983	SETUP_LOOP        '2031'

1986	LOAD_FAST         'source'
1989	LOAD_ATTR         'next'
1992	LOAD_CONST        None
1995	COMPARE_OP        'is'
1998	POP_JUMP_IF_TRUE  '2016'
2001	LOAD_FAST         'source'
2004	LOAD_ATTR         'next'
2007	LOAD_CONST        ')'
2010	COMPARE_OP        '=='
2013_0	COME_FROM         '1998'
2013	POP_JUMP_IF_FALSE '2020'

2016	BREAK_LOOP        None
2017	JUMP_FORWARD      '2020'
2020_0	COME_FROM         '2017'

2020	LOAD_FAST         'sourceget'
2023	CALL_FUNCTION_0   None
2026	POP_TOP           None
2027	JUMP_BACK         '1986'
2030	POP_BLOCK         None
2031_0	COME_FROM         '1983'

2031	LOAD_FAST         'sourcematch'
2034	LOAD_CONST        ')'
2037	CALL_FUNCTION_1   None
2040	POP_JUMP_IF_TRUE  '72'

2043	LOAD_GLOBAL       'error'
2046	LOAD_CONST        'unbalanced parenthesis'
2049	RAISE_VARARGS_2   None
2052	JUMP_BACK         '72'

2055	CONTINUE          '72'
2058	JUMP_ABSOLUTE     '2522'

2061	LOAD_FAST         'source'
2064	LOAD_ATTR         'next'
2067	LOAD_FAST         'ASSERTCHARS'
2070	COMPARE_OP        'in'
2073	POP_JUMP_IF_FALSE '2252'

2076	LOAD_FAST         'sourceget'
2079	CALL_FUNCTION_0   None
2082	STORE_FAST        'char'

2085	LOAD_CONST        1
2088	STORE_FAST        'dir'

2091	LOAD_FAST         'char'
2094	LOAD_CONST        '<'
2097	COMPARE_OP        '=='
2100	POP_JUMP_IF_FALSE '2148'

2103	LOAD_FAST         'source'
2106	LOAD_ATTR         'next'
2109	LOAD_FAST         'LOOKBEHINDASSERTCHARS'
2112	COMPARE_OP        'not in'
2115	POP_JUMP_IF_FALSE '2130'

2118	LOAD_GLOBAL       'error'
2121	LOAD_CONST        'syntax error'
2124	RAISE_VARARGS_2   None
2127	JUMP_FORWARD      '2130'
2130_0	COME_FROM         '2127'

2130	LOAD_CONST        -1
2133	STORE_FAST        'dir'

2136	LOAD_FAST         'sourceget'
2139	CALL_FUNCTION_0   None
2142	STORE_FAST        'char'
2145	JUMP_FORWARD      '2148'
2148_0	COME_FROM         '2145'

2148	LOAD_GLOBAL       '_parse_sub'
2151	LOAD_FAST         'source'
2154	LOAD_FAST         'state'
2157	CALL_FUNCTION_2   None
2160	STORE_FAST        'p'

2163	LOAD_FAST         'sourcematch'
2166	LOAD_CONST        ')'
2169	CALL_FUNCTION_1   None
2172	POP_JUMP_IF_TRUE  '2187'

2175	LOAD_GLOBAL       'error'
2178	LOAD_CONST        'unbalanced parenthesis'
2181	RAISE_VARARGS_2   None
2184	JUMP_FORWARD      '2187'
2187_0	COME_FROM         '2184'

2187	LOAD_FAST         'char'
2190	LOAD_CONST        '='
2193	COMPARE_OP        '=='
2196	POP_JUMP_IF_FALSE '2224'

2199	LOAD_FAST         'subpatternappend'
2202	LOAD_GLOBAL       'ASSERT'
2205	LOAD_FAST         'dir'
2208	LOAD_FAST         'p'
2211	BUILD_TUPLE_2     None
2214	BUILD_TUPLE_2     None
2217	CALL_FUNCTION_1   None
2220	POP_TOP           None
2221	JUMP_BACK         '72'

2224	LOAD_FAST         'subpatternappend'
2227	LOAD_GLOBAL       'ASSERT_NOT'
2230	LOAD_FAST         'dir'
2233	LOAD_FAST         'p'
2236	BUILD_TUPLE_2     None
2239	BUILD_TUPLE_2     None
2242	CALL_FUNCTION_1   None
2245	POP_TOP           None

2246	CONTINUE          '72'
2249	JUMP_ABSOLUTE     '2522'

2252	LOAD_FAST         'sourcematch'
2255	LOAD_CONST        '('
2258	CALL_FUNCTION_1   None
2261	POP_JUMP_IF_FALSE '2447'

2264	LOAD_CONST        ''
2267	STORE_FAST        'condname'

2270	SETUP_LOOP        '2336'

2273	LOAD_FAST         'sourceget'
2276	CALL_FUNCTION_0   None
2279	STORE_FAST        'char'

2282	LOAD_FAST         'char'
2285	LOAD_CONST        None
2288	COMPARE_OP        'is'
2291	POP_JUMP_IF_FALSE '2306'

2294	LOAD_GLOBAL       'error'
2297	LOAD_CONST        'unterminated name'
2300	RAISE_VARARGS_2   None
2303	JUMP_FORWARD      '2306'
2306_0	COME_FROM         '2303'

2306	LOAD_FAST         'char'
2309	LOAD_CONST        ')'
2312	COMPARE_OP        '=='
2315	POP_JUMP_IF_FALSE '2322'

2318	BREAK_LOOP        None
2319	JUMP_FORWARD      '2322'
2322_0	COME_FROM         '2319'

2322	LOAD_FAST         'condname'
2325	LOAD_FAST         'char'
2328	BINARY_ADD        None
2329	STORE_FAST        'condname'
2332	JUMP_BACK         '2273'
2335	POP_BLOCK         None
2336_0	COME_FROM         '2270'

2336	LOAD_CONST        2
2339	STORE_FAST        'group'

2342	LOAD_GLOBAL       'isname'
2345	LOAD_FAST         'condname'
2348	CALL_FUNCTION_1   None
2351	POP_JUMP_IF_FALSE '2399'

2354	LOAD_FAST         'state'
2357	LOAD_ATTR         'groupdict'
2360	LOAD_ATTR         'get'
2363	LOAD_FAST         'condname'
2366	CALL_FUNCTION_1   None
2369	STORE_FAST        'condgroup'

2372	LOAD_FAST         'condgroup'
2375	LOAD_CONST        None
2378	COMPARE_OP        'is'
2381	POP_JUMP_IF_FALSE '2444'

2384	LOAD_GLOBAL       'error'
2387	LOAD_CONST        'unknown group name'
2390	RAISE_VARARGS_2   None
2393	JUMP_ABSOLUTE     '2444'
2396	JUMP_ABSOLUTE     '2519'

2399	SETUP_EXCEPT      '2418'

2402	LOAD_GLOBAL       'int'
2405	LOAD_FAST         'condname'
2408	CALL_FUNCTION_1   None
2411	STORE_FAST        'condgroup'
2414	POP_BLOCK         None
2415	JUMP_ABSOLUTE     '2519'
2418_0	COME_FROM         '2399'

2418	DUP_TOP           None
2419	LOAD_GLOBAL       'ValueError'
2422	COMPARE_OP        'exception match'
2425	POP_JUMP_IF_FALSE '2443'
2428	POP_TOP           None
2429	POP_TOP           None
2430	POP_TOP           None

2431	LOAD_GLOBAL       'error'
2434	LOAD_CONST        'bad character in group name'
2437	RAISE_VARARGS_2   None
2440	JUMP_ABSOLUTE     '2519'
2443	END_FINALLY       None
2444_0	COME_FROM         '2443'
2444	JUMP_ABSOLUTE     '2522'

2447	LOAD_FAST         'source'
2450	LOAD_ATTR         'next'
2453	LOAD_GLOBAL       'FLAGS'
2456	COMPARE_OP        'not in'
2459	POP_JUMP_IF_FALSE '2474'

2462	LOAD_GLOBAL       'error'
2465	LOAD_CONST        'unexpected end of pattern'
2468	RAISE_VARARGS_2   None
2471	JUMP_FORWARD      '2474'
2474_0	COME_FROM         '2471'

2474	SETUP_LOOP        '2522'
2477	LOAD_FAST         'source'
2480	LOAD_ATTR         'next'
2483	LOAD_GLOBAL       'FLAGS'
2486	COMPARE_OP        'in'
2489	POP_JUMP_IF_FALSE '2518'

2492	LOAD_FAST         'state'
2495	LOAD_ATTR         'flags'
2498	LOAD_GLOBAL       'FLAGS'
2501	LOAD_FAST         'sourceget'
2504	CALL_FUNCTION_0   None
2507	BINARY_SUBSCR     None
2508	BINARY_OR         None
2509	LOAD_FAST         'state'
2512	STORE_ATTR        'flags'
2515	JUMP_BACK         '2477'
2518	POP_BLOCK         None
2519_0	COME_FROM         '2474'
2519	JUMP_FORWARD      '2522'
2522_0	COME_FROM         '2519'

2522	LOAD_FAST         'group'
2525	POP_JUMP_IF_FALSE '2683'

2528	LOAD_FAST         'group'
2531	LOAD_CONST        2
2534	COMPARE_OP        '=='
2537	POP_JUMP_IF_FALSE '2549'

2540	LOAD_CONST        None
2543	STORE_FAST        'group'
2546	JUMP_FORWARD      '2564'

2549	LOAD_FAST         'state'
2552	LOAD_ATTR         'opengroup'
2555	LOAD_FAST         'name'
2558	CALL_FUNCTION_1   None
2561	STORE_FAST        'group'
2564_0	COME_FROM         '2546'

2564	LOAD_FAST         'condgroup'
2567	POP_JUMP_IF_FALSE '2591'

2570	LOAD_GLOBAL       '_parse_sub_cond'
2573	LOAD_FAST         'source'
2576	LOAD_FAST         'state'
2579	LOAD_FAST         'condgroup'
2582	CALL_FUNCTION_3   None
2585	STORE_FAST        'p'
2588	JUMP_FORWARD      '2606'

2591	LOAD_GLOBAL       '_parse_sub'
2594	LOAD_FAST         'source'
2597	LOAD_FAST         'state'
2600	CALL_FUNCTION_2   None
2603	STORE_FAST        'p'
2606_0	COME_FROM         '2588'

2606	LOAD_FAST         'sourcematch'
2609	LOAD_CONST        ')'
2612	CALL_FUNCTION_1   None
2615	POP_JUMP_IF_TRUE  '2630'

2618	LOAD_GLOBAL       'error'
2621	LOAD_CONST        'unbalanced parenthesis'
2624	RAISE_VARARGS_2   None
2627	JUMP_FORWARD      '2630'
2630_0	COME_FROM         '2627'

2630	LOAD_FAST         'group'
2633	LOAD_CONST        None
2636	COMPARE_OP        'is not'
2639	POP_JUMP_IF_FALSE '2658'

2642	LOAD_FAST         'state'
2645	LOAD_ATTR         'closegroup'
2648	LOAD_FAST         'group'
2651	CALL_FUNCTION_1   None
2654	POP_TOP           None
2655	JUMP_FORWARD      '2658'
2658_0	COME_FROM         '2655'

2658	LOAD_FAST         'subpatternappend'
2661	LOAD_GLOBAL       'SUBPATTERN'
2664	LOAD_FAST         'group'
2667	LOAD_FAST         'p'
2670	BUILD_TUPLE_2     None
2673	BUILD_TUPLE_2     None
2676	CALL_FUNCTION_1   None
2679	POP_TOP           None
2680	JUMP_ABSOLUTE     '2878'

2683	SETUP_LOOP        '2878'

2686	LOAD_FAST         'sourceget'
2689	CALL_FUNCTION_0   None
2692	STORE_FAST        'char'

2695	LOAD_FAST         'char'
2698	LOAD_CONST        None
2701	COMPARE_OP        'is'
2704	POP_JUMP_IF_FALSE '2719'

2707	LOAD_GLOBAL       'error'
2710	LOAD_CONST        'unexpected end of pattern'
2713	RAISE_VARARGS_2   None
2716	JUMP_FORWARD      '2719'
2719_0	COME_FROM         '2716'

2719	LOAD_FAST         'char'
2722	LOAD_CONST        ')'
2725	COMPARE_OP        '=='
2728	POP_JUMP_IF_FALSE '2735'

2731	BREAK_LOOP        None
2732	JUMP_FORWARD      '2735'
2735_0	COME_FROM         '2732'

2735	LOAD_GLOBAL       'error'
2738	LOAD_CONST        'unknown extension'
2741	RAISE_VARARGS_2   None
2744	JUMP_BACK         '2686'
2747	POP_BLOCK         None
2748_0	COME_FROM         '2683'
2748	JUMP_BACK         '72'

2751	LOAD_FAST         'this'
2754	LOAD_CONST        '^'
2757	COMPARE_OP        '=='
2760	POP_JUMP_IF_FALSE '2782'

2763	LOAD_FAST         'subpatternappend'
2766	LOAD_GLOBAL       'AT'
2769	LOAD_GLOBAL       'AT_BEGINNING'
2772	BUILD_TUPLE_2     None
2775	CALL_FUNCTION_1   None
2778	POP_TOP           None
2779	JUMP_BACK         '72'

2782	LOAD_FAST         'this'
2785	LOAD_CONST        '$'
2788	COMPARE_OP        '=='
2791	POP_JUMP_IF_FALSE '2816'

2794	LOAD_FAST         'subpattern'
2797	LOAD_ATTR         'append'
2800	LOAD_GLOBAL       'AT'
2803	LOAD_GLOBAL       'AT_END'
2806	BUILD_TUPLE_2     None
2809	CALL_FUNCTION_1   None
2812	POP_TOP           None
2813	JUMP_BACK         '72'

2816	LOAD_FAST         'this'
2819	POP_JUMP_IF_FALSE '2869'
2822	LOAD_FAST         'this'
2825	LOAD_CONST        0
2828	BINARY_SUBSCR     None
2829	LOAD_CONST        '\\'
2832	COMPARE_OP        '=='
2835_0	COME_FROM         '2819'
2835	POP_JUMP_IF_FALSE '2869'

2838	LOAD_GLOBAL       '_escape'
2841	LOAD_FAST         'source'
2844	LOAD_FAST         'this'
2847	LOAD_FAST         'state'
2850	CALL_FUNCTION_3   None
2853	STORE_FAST        'code'

2856	LOAD_FAST         'subpatternappend'
2859	LOAD_FAST         'code'
2862	CALL_FUNCTION_1   None
2865	POP_TOP           None
2866	JUMP_BACK         '72'

2869	LOAD_GLOBAL       'error'
2872	LOAD_CONST        'parser error'
2875	RAISE_VARARGS_2   None
2878	JUMP_BACK         '72'
2881	POP_BLOCK         None
2882_0	COME_FROM         '69'

2882	LOAD_FAST         'subpattern'
2885	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 190


def parse(str, flags = 0, pattern = None):
    source = Tokenizer(str)
    if pattern is None:
        pattern = Pattern()
    pattern.flags = flags
    pattern.str = str
    p = _parse_sub(source, pattern, 0)
    tail = source.get()
    if tail == ')':
        raise error, 'unbalanced parenthesis'
    elif tail:
        raise error, 'bogus characters at end of regular expression'
    if flags & SRE_FLAG_DEBUG:
        p.dump()
    if not flags & SRE_FLAG_VERBOSE and p.pattern.flags & SRE_FLAG_VERBOSE:
        return parse(str, p.pattern.flags)
    else:
        return p


def parse_template--- This code section failed: ---

0	LOAD_GLOBAL       'Tokenizer'
3	LOAD_FAST         'source'
6	CALL_FUNCTION_1   None
9	STORE_FAST        's'

12	LOAD_FAST         's'
15	LOAD_ATTR         'get'
18	STORE_FAST        'sget'

21	BUILD_LIST_0      None
24	STORE_FAST        'p'

27	LOAD_FAST         'p'
30	LOAD_ATTR         'append'
33	STORE_FAST        'a'

36	LOAD_FAST         'p'
39	LOAD_FAST         'a'
42	LOAD_CONST        '<code_object literal>'
45	MAKE_FUNCTION_2   None
48	STORE_FAST        'literal'

51	LOAD_FAST         'source'
54	LOAD_CONST        0
57	SLICE+2           None
58	STORE_FAST        'sep'

61	LOAD_GLOBAL       'type'
64	LOAD_FAST         'sep'
67	CALL_FUNCTION_1   None
70	LOAD_GLOBAL       'type'
73	LOAD_CONST        ''
76	CALL_FUNCTION_1   None
79	COMPARE_OP        'is'
82	POP_JUMP_IF_FALSE '94'

85	LOAD_GLOBAL       'chr'
88	STORE_FAST        'makechar'
91	JUMP_FORWARD      '100'

94	LOAD_GLOBAL       'unichr'
97	STORE_FAST        'makechar'
100_0	COME_FROM         '91'

100	SETUP_LOOP        '798'

103	LOAD_FAST         'sget'
106	CALL_FUNCTION_0   None
109	STORE_FAST        'this'

112	LOAD_FAST         'this'
115	LOAD_CONST        None
118	COMPARE_OP        'is'
121	POP_JUMP_IF_FALSE '128'

124	BREAK_LOOP        None
125	JUMP_FORWARD      '128'
128_0	COME_FROM         '125'

128	LOAD_FAST         'this'
131	POP_JUMP_IF_FALSE '784'
134	LOAD_FAST         'this'
137	LOAD_CONST        0
140	BINARY_SUBSCR     None
141	LOAD_CONST        '\\'
144	COMPARE_OP        '=='
147_0	COME_FROM         '131'
147	POP_JUMP_IF_FALSE '784'

150	LOAD_FAST         'this'
153	LOAD_CONST        1
156	LOAD_CONST        2
159	SLICE+3           None
160	STORE_FAST        'c'

163	LOAD_FAST         'c'
166	LOAD_CONST        'g'
169	COMPARE_OP        '=='
172	POP_JUMP_IF_FALSE '432'

175	LOAD_CONST        ''
178	STORE_FAST        'name'

181	LOAD_FAST         's'
184	LOAD_ATTR         'match'
187	LOAD_CONST        '<'
190	CALL_FUNCTION_1   None
193	POP_JUMP_IF_FALSE '265'

196	SETUP_LOOP        '265'

199	LOAD_FAST         'sget'
202	CALL_FUNCTION_0   None
205	STORE_FAST        'char'

208	LOAD_FAST         'char'
211	LOAD_CONST        None
214	COMPARE_OP        'is'
217	POP_JUMP_IF_FALSE '232'

220	LOAD_GLOBAL       'error'
223	LOAD_CONST        'unterminated group name'
226	RAISE_VARARGS_2   None
229	JUMP_FORWARD      '232'
232_0	COME_FROM         '229'

232	LOAD_FAST         'char'
235	LOAD_CONST        '>'
238	COMPARE_OP        '=='
241	POP_JUMP_IF_FALSE '248'

244	BREAK_LOOP        None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_FAST         'name'
251	LOAD_FAST         'char'
254	BINARY_ADD        None
255	STORE_FAST        'name'
258	JUMP_BACK         '199'
261	POP_BLOCK         None
262_0	COME_FROM         '196'
262	JUMP_FORWARD      '265'
265_0	COME_FROM         '262'

265	LOAD_FAST         'name'
268	POP_JUMP_IF_TRUE  '283'

271	LOAD_GLOBAL       'error'
274	LOAD_CONST        'bad group name'
277	RAISE_VARARGS_2   None
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	SETUP_EXCEPT      '326'

286	LOAD_GLOBAL       'int'
289	LOAD_FAST         'name'
292	CALL_FUNCTION_1   None
295	STORE_FAST        'index'

298	LOAD_FAST         'index'
301	LOAD_CONST        0
304	COMPARE_OP        '<'
307	POP_JUMP_IF_FALSE '322'

310	LOAD_GLOBAL       'error'
313	LOAD_CONST        'negative group number'
316	RAISE_VARARGS_2   None
319	JUMP_FORWARD      '322'
322_0	COME_FROM         '319'
322	POP_BLOCK         None
323	JUMP_FORWARD      '413'
326_0	COME_FROM         '283'

326	DUP_TOP           None
327	LOAD_GLOBAL       'ValueError'
330	COMPARE_OP        'exception match'
333	POP_JUMP_IF_FALSE '412'
336	POP_TOP           None
337	POP_TOP           None
338	POP_TOP           None

339	LOAD_GLOBAL       'isname'
342	LOAD_FAST         'name'
345	CALL_FUNCTION_1   None
348	POP_JUMP_IF_TRUE  '363'

351	LOAD_GLOBAL       'error'
354	LOAD_CONST        'bad character in group name'
357	RAISE_VARARGS_2   None
360	JUMP_FORWARD      '363'
363_0	COME_FROM         '360'

363	SETUP_EXCEPT      '383'

366	LOAD_FAST         'pattern'
369	LOAD_ATTR         'groupindex'
372	LOAD_FAST         'name'
375	BINARY_SUBSCR     None
376	STORE_FAST        'index'
379	POP_BLOCK         None
380	JUMP_ABSOLUTE     '413'
383_0	COME_FROM         '363'

383	DUP_TOP           None
384	LOAD_GLOBAL       'KeyError'
387	COMPARE_OP        'exception match'
390	POP_JUMP_IF_FALSE '408'
393	POP_TOP           None
394	POP_TOP           None
395	POP_TOP           None

396	LOAD_GLOBAL       'IndexError'
399	LOAD_CONST        'unknown group name'
402	RAISE_VARARGS_2   None
405	JUMP_ABSOLUTE     '413'
408	END_FINALLY       None
409_0	COME_FROM         '408'
409	JUMP_FORWARD      '413'
412	END_FINALLY       None
413_0	COME_FROM         '323'
413_1	COME_FROM         '412'

413	LOAD_FAST         'a'
416	LOAD_GLOBAL       'MARK'
419	LOAD_FAST         'index'
422	BUILD_TUPLE_2     None
425	CALL_FUNCTION_1   None
428	POP_TOP           None
429	JUMP_ABSOLUTE     '794'

432	LOAD_FAST         'c'
435	LOAD_CONST        '0'
438	COMPARE_OP        '=='
441	POP_JUMP_IF_FALSE '542'

444	LOAD_FAST         's'
447	LOAD_ATTR         'next'
450	LOAD_GLOBAL       'OCTDIGITS'
453	COMPARE_OP        'in'
456	POP_JUMP_IF_FALSE '506'

459	LOAD_FAST         'this'
462	LOAD_FAST         'sget'
465	CALL_FUNCTION_0   None
468	BINARY_ADD        None
469	STORE_FAST        'this'

472	LOAD_FAST         's'
475	LOAD_ATTR         'next'
478	LOAD_GLOBAL       'OCTDIGITS'
481	COMPARE_OP        'in'
484	POP_JUMP_IF_FALSE '506'

487	LOAD_FAST         'this'
490	LOAD_FAST         'sget'
493	CALL_FUNCTION_0   None
496	BINARY_ADD        None
497	STORE_FAST        'this'
500	JUMP_ABSOLUTE     '506'
503	JUMP_FORWARD      '506'
506_0	COME_FROM         '503'

506	LOAD_FAST         'literal'
509	LOAD_FAST         'makechar'
512	LOAD_GLOBAL       'int'
515	LOAD_FAST         'this'
518	LOAD_CONST        1
521	SLICE+1           None
522	LOAD_CONST        8
525	CALL_FUNCTION_2   None
528	LOAD_CONST        255
531	BINARY_AND        None
532	CALL_FUNCTION_1   None
535	CALL_FUNCTION_1   None
538	POP_TOP           None
539	JUMP_ABSOLUTE     '794'

542	LOAD_FAST         'c'
545	LOAD_GLOBAL       'DIGITS'
548	COMPARE_OP        'in'
551	POP_JUMP_IF_FALSE '727'

554	LOAD_GLOBAL       'False'
557	STORE_FAST        'isoctal'

560	LOAD_FAST         's'
563	LOAD_ATTR         'next'
566	LOAD_GLOBAL       'DIGITS'
569	COMPARE_OP        'in'
572	POP_JUMP_IF_FALSE '689'

575	LOAD_FAST         'this'
578	LOAD_FAST         'sget'
581	CALL_FUNCTION_0   None
584	BINARY_ADD        None
585	STORE_FAST        'this'

588	LOAD_FAST         'c'
591	LOAD_GLOBAL       'OCTDIGITS'
594	COMPARE_OP        'in'
597	POP_JUMP_IF_FALSE '689'
600	LOAD_FAST         'this'
603	LOAD_CONST        2
606	BINARY_SUBSCR     None
607	LOAD_GLOBAL       'OCTDIGITS'
610	COMPARE_OP        'in'
613_0	COME_FROM         '597'
613	POP_JUMP_IF_FALSE '689'

616	LOAD_FAST         's'
619	LOAD_ATTR         'next'
622	LOAD_GLOBAL       'OCTDIGITS'
625	COMPARE_OP        'in'
628_0	COME_FROM         '613'
628	POP_JUMP_IF_FALSE '689'

631	LOAD_FAST         'this'
634	LOAD_FAST         'sget'
637	CALL_FUNCTION_0   None
640	BINARY_ADD        None
641	STORE_FAST        'this'

644	LOAD_GLOBAL       'True'
647	STORE_FAST        'isoctal'

650	LOAD_FAST         'literal'
653	LOAD_FAST         'makechar'
656	LOAD_GLOBAL       'int'
659	LOAD_FAST         'this'
662	LOAD_CONST        1
665	SLICE+1           None
666	LOAD_CONST        8
669	CALL_FUNCTION_2   None
672	LOAD_CONST        255
675	BINARY_AND        None
676	CALL_FUNCTION_1   None
679	CALL_FUNCTION_1   None
682	POP_TOP           None
683	JUMP_ABSOLUTE     '689'
686	JUMP_FORWARD      '689'
689_0	COME_FROM         '686'

689	LOAD_FAST         'isoctal'
692	POP_JUMP_IF_TRUE  '781'

695	LOAD_FAST         'a'
698	LOAD_GLOBAL       'MARK'
701	LOAD_GLOBAL       'int'
704	LOAD_FAST         'this'
707	LOAD_CONST        1
710	SLICE+1           None
711	CALL_FUNCTION_1   None
714	BUILD_TUPLE_2     None
717	CALL_FUNCTION_1   None
720	POP_TOP           None
721	JUMP_ABSOLUTE     '781'
724	JUMP_ABSOLUTE     '794'

727	SETUP_EXCEPT      '754'

730	LOAD_FAST         'makechar'
733	LOAD_GLOBAL       'ESCAPES'
736	LOAD_FAST         'this'
739	BINARY_SUBSCR     None
740	LOAD_CONST        1
743	BINARY_SUBSCR     None
744	CALL_FUNCTION_1   None
747	STORE_FAST        'this'
750	POP_BLOCK         None
751	JUMP_FORWARD      '771'
754_0	COME_FROM         '727'

754	DUP_TOP           None
755	LOAD_GLOBAL       'KeyError'
758	COMPARE_OP        'exception match'
761	POP_JUMP_IF_FALSE '770'
764	POP_TOP           None
765	POP_TOP           None
766	POP_TOP           None

767	JUMP_FORWARD      '771'
770	END_FINALLY       None
771_0	COME_FROM         '751'
771_1	COME_FROM         '770'

771	LOAD_FAST         'literal'
774	LOAD_FAST         'this'
777	CALL_FUNCTION_1   None
780	POP_TOP           None
781	JUMP_BACK         '103'

784	LOAD_FAST         'literal'
787	LOAD_FAST         'this'
790	CALL_FUNCTION_1   None
793	POP_TOP           None
794	JUMP_BACK         '103'
797	POP_BLOCK         None
798_0	COME_FROM         '100'

798	LOAD_CONST        0
801	STORE_FAST        'i'

804	BUILD_LIST_0      None
807	STORE_FAST        'groups'

810	LOAD_FAST         'groups'
813	LOAD_ATTR         'append'
816	STORE_FAST        'groupsappend'

819	LOAD_CONST        None
822	BUILD_LIST_1      None
825	LOAD_GLOBAL       'len'
828	LOAD_FAST         'p'
831	CALL_FUNCTION_1   None
834	BINARY_MULTIPLY   None
835	STORE_FAST        'literals'

838	SETUP_LOOP        '912'
841	LOAD_FAST         'p'
844	GET_ITER          None
845	FOR_ITER          '911'
848	UNPACK_SEQUENCE_2 None
851	STORE_FAST        'c'
854	STORE_FAST        's'

857	LOAD_FAST         'c'
860	LOAD_GLOBAL       'MARK'
863	COMPARE_OP        'is'
866	POP_JUMP_IF_FALSE '888'

869	LOAD_FAST         'groupsappend'
872	LOAD_FAST         'i'
875	LOAD_FAST         's'
878	BUILD_TUPLE_2     None
881	CALL_FUNCTION_1   None
884	POP_TOP           None
885	JUMP_FORWARD      '898'

888	LOAD_FAST         's'
891	LOAD_FAST         'literals'
894	LOAD_FAST         'i'
897	STORE_SUBSCR      None
898_0	COME_FROM         '885'

898	LOAD_FAST         'i'
901	LOAD_CONST        1
904	BINARY_ADD        None
905	STORE_FAST        'i'
908	JUMP_BACK         '845'
911	POP_BLOCK         None
912_0	COME_FROM         '838'

912	LOAD_FAST         'groups'
915	LOAD_FAST         'literals'
918	BUILD_TUPLE_2     None
921	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 261


def expand_template(template, match):
    g = match.group
    sep = match.string[:0]
    groups, literals = template
    literals = literals[:]
    try:
        for index, group in groups:
            literals[index] = s = g(group)
            if s is None:
                raise error, 'unmatched group'

    except IndexError:
        raise error, 'invalid group reference'

    return sep.join(literals)