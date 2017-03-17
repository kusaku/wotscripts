# Embedded file name: scripts/common/Lib/xml/etree/ElementPath.py
import re
xpath_tokenizer_re = re.compile('(\'[^\']*\'|"[^"]*"|::|//?|\\.\\.|\\(\\)|[/.*:\\[\\]\\(\\)@=])|((?:\\{[^}]+\\})?[^/\\[\\]\\(\\)@=\\s]+)|\\s+')

def xpath_tokenizer(pattern, namespaces = None):
    for token in xpath_tokenizer_re.findall(pattern):
        tag = token[1]
        if tag and tag[0] != '{' and ':' in tag:
            try:
                prefix, uri = tag.split(':', 1)
                if not namespaces:
                    raise KeyError
                yield (token[0], '{%s}%s' % (namespaces[prefix], uri))
            except KeyError:
                raise SyntaxError('prefix %r not found in prefix map' % prefix)

        else:
            yield token


def get_parent_map(context):
    parent_map = context.parent_map
    if parent_map is None:
        context.parent_map = parent_map = {}
        for p in context.root.iter():
            for e in p:
                parent_map[e] = p

    return parent_map


def prepare_child(next, token):
    tag = token[1]

    def select(context, result):
        for elem in result:
            for e in elem:
                if e.tag == tag:
                    yield e

    return select


def prepare_star(next, token):

    def select(context, result):
        for elem in result:
            for e in elem:
                yield e

    return select


def prepare_self(next, token):

    def select(context, result):
        for elem in result:
            yield elem

    return select


def prepare_descendant(next, token):
    token = next()
    if token[0] == '*':
        tag = '*'
    elif not token[0]:
        tag = token[1]
    else:
        raise SyntaxError('invalid descendant')

    def select(context, result):
        for elem in result:
            for e in elem.iter(tag):
                if e is not elem:
                    yield e

    return select


def prepare_parent(next, token):

    def select(context, result):
        parent_map = get_parent_map(context)
        result_map = {}
        for elem in result:
            if elem in parent_map:
                parent = parent_map[elem]
                if parent not in result_map:
                    result_map[parent] = None
                    yield parent

        return

    return select


def prepare_predicate--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'signature'

6	BUILD_LIST_0      None
9	STORE_FAST        'predicate'

12	SETUP_LOOP        '144'

15	LOAD_FAST         'next'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'token'

24	LOAD_FAST         'token'
27	LOAD_CONST        0
30	BINARY_SUBSCR     None
31	LOAD_CONST        ']'
34	COMPARE_OP        '=='
37	POP_JUMP_IF_FALSE '44'

40	BREAK_LOOP        None
41	JUMP_FORWARD      '44'
44_0	COME_FROM         '41'

44	LOAD_FAST         'token'
47	LOAD_CONST        0
50	BINARY_SUBSCR     None
51	POP_JUMP_IF_FALSE '100'
54	LOAD_FAST         'token'
57	LOAD_CONST        0
60	BINARY_SUBSCR     None
61	LOAD_CONST        1
64	SLICE+2           None
65	LOAD_CONST        '\'"'
68	COMPARE_OP        'in'
71_0	COME_FROM         '51'
71	POP_JUMP_IF_FALSE '100'

74	LOAD_CONST        "'"
77	LOAD_FAST         'token'
80	LOAD_CONST        0
83	BINARY_SUBSCR     None
84	LOAD_CONST        1
87	LOAD_CONST        -1
90	SLICE+3           None
91	BUILD_TUPLE_2     None
94	STORE_FAST        'token'
97	JUMP_FORWARD      '100'
100_0	COME_FROM         '97'

100	LOAD_FAST         'signature'
103	LOAD_ATTR         'append'
106	LOAD_FAST         'token'
109	LOAD_CONST        0
112	BINARY_SUBSCR     None
113	JUMP_IF_TRUE_OR_POP '119'
116	LOAD_CONST        '-'
119_0	COME_FROM         '113'
119	CALL_FUNCTION_1   None
122	POP_TOP           None

123	LOAD_FAST         'predicate'
126	LOAD_ATTR         'append'
129	LOAD_FAST         'token'
132	LOAD_CONST        1
135	BINARY_SUBSCR     None
136	CALL_FUNCTION_1   None
139	POP_TOP           None
140	JUMP_BACK         '15'
143	POP_BLOCK         None
144_0	COME_FROM         '12'

144	LOAD_CONST        ''
147	LOAD_ATTR         'join'
150	LOAD_FAST         'signature'
153	CALL_FUNCTION_1   None
156	STORE_FAST        'signature'

159	LOAD_FAST         'signature'
162	LOAD_CONST        '@-'
165	COMPARE_OP        '=='
168	POP_JUMP_IF_FALSE '200'

171	LOAD_FAST         'predicate'
174	LOAD_CONST        1
177	BINARY_SUBSCR     None
178	STORE_DEREF       'key'

181	LOAD_CLOSURE      'key'
187	LOAD_CONST        '<code_object select>'
190	MAKE_CLOSURE_0    None
193	STORE_FAST        'select'

196	LOAD_FAST         'select'
199	RETURN_END_IF     None

200	LOAD_FAST         'signature'
203	LOAD_CONST        "@-='"
206	COMPARE_OP        '=='
209	POP_JUMP_IF_FALSE '254'

212	LOAD_FAST         'predicate'
215	LOAD_CONST        1
218	BINARY_SUBSCR     None
219	STORE_DEREF       'key'

222	LOAD_FAST         'predicate'
225	LOAD_CONST        -1
228	BINARY_SUBSCR     None
229	STORE_DEREF       'value'

232	LOAD_CLOSURE      'key'
235	LOAD_CLOSURE      'value'
241	LOAD_CONST        '<code_object select>'
244	MAKE_CLOSURE_0    None
247	STORE_FAST        'select'

250	LOAD_FAST         'select'
253	RETURN_END_IF     None

254	LOAD_FAST         'signature'
257	LOAD_CONST        '-'
260	COMPARE_OP        '=='
263	POP_JUMP_IF_FALSE '318'
266	LOAD_GLOBAL       're'
269	LOAD_ATTR         'match'
272	LOAD_CONST        '\\d+$'
275	LOAD_FAST         'predicate'
278	LOAD_CONST        0
281	BINARY_SUBSCR     None
282	CALL_FUNCTION_2   None
285	UNARY_NOT         None
286_0	COME_FROM         '263'
286	POP_JUMP_IF_FALSE '318'

289	LOAD_FAST         'predicate'
292	LOAD_CONST        0
295	BINARY_SUBSCR     None
296	STORE_DEREF       'tag'

299	LOAD_CLOSURE      'tag'
305	LOAD_CONST        '<code_object select>'
308	MAKE_CLOSURE_0    None
311	STORE_FAST        'select'

314	LOAD_FAST         'select'
317	RETURN_END_IF     None

318	LOAD_FAST         'signature'
321	LOAD_CONST        "-='"
324	COMPARE_OP        '=='
327	POP_JUMP_IF_FALSE '395'
330	LOAD_GLOBAL       're'
333	LOAD_ATTR         'match'
336	LOAD_CONST        '\\d+$'
339	LOAD_FAST         'predicate'
342	LOAD_CONST        0
345	BINARY_SUBSCR     None
346	CALL_FUNCTION_2   None
349	UNARY_NOT         None
350_0	COME_FROM         '327'
350	POP_JUMP_IF_FALSE '395'

353	LOAD_FAST         'predicate'
356	LOAD_CONST        0
359	BINARY_SUBSCR     None
360	STORE_DEREF       'tag'

363	LOAD_FAST         'predicate'
366	LOAD_CONST        -1
369	BINARY_SUBSCR     None
370	STORE_DEREF       'value'

373	LOAD_CLOSURE      'tag'
376	LOAD_CLOSURE      'value'
382	LOAD_CONST        '<code_object select>'
385	MAKE_CLOSURE_0    None
388	STORE_FAST        'select'

391	LOAD_FAST         'select'
394	RETURN_END_IF     None

395	LOAD_FAST         'signature'
398	LOAD_CONST        '-'
401	COMPARE_OP        '=='
404	POP_JUMP_IF_TRUE  '431'
407	LOAD_FAST         'signature'
410	LOAD_CONST        '-()'
413	COMPARE_OP        '=='
416	POP_JUMP_IF_TRUE  '431'
419	LOAD_FAST         'signature'
422	LOAD_CONST        '-()-'
425	COMPARE_OP        '=='
428_0	COME_FROM         '404'
428_1	COME_FROM         '416'
428	POP_JUMP_IF_FALSE '593'

431	LOAD_FAST         'signature'
434	LOAD_CONST        '-'
437	COMPARE_OP        '=='
440	POP_JUMP_IF_FALSE '466'

443	LOAD_GLOBAL       'int'
446	LOAD_FAST         'predicate'
449	LOAD_CONST        0
452	BINARY_SUBSCR     None
453	CALL_FUNCTION_1   None
456	LOAD_CONST        1
459	BINARY_SUBTRACT   None
460	STORE_DEREF       'index'
463	JUMP_FORWARD      '574'

466	LOAD_FAST         'predicate'
469	LOAD_CONST        0
472	BINARY_SUBSCR     None
473	LOAD_CONST        'last'
476	COMPARE_OP        '!='
479	POP_JUMP_IF_FALSE '497'

482	LOAD_GLOBAL       'SyntaxError'
485	LOAD_CONST        'unsupported function'
488	CALL_FUNCTION_1   None
491	RAISE_VARARGS_1   None
494	JUMP_FORWARD      '497'
497_0	COME_FROM         '494'

497	LOAD_FAST         'signature'
500	LOAD_CONST        '-()-'
503	COMPARE_OP        '=='
506	POP_JUMP_IF_FALSE '568'

509	SETUP_EXCEPT      '536'

512	LOAD_GLOBAL       'int'
515	LOAD_FAST         'predicate'
518	LOAD_CONST        2
521	BINARY_SUBSCR     None
522	CALL_FUNCTION_1   None
525	LOAD_CONST        1
528	BINARY_SUBTRACT   None
529	STORE_DEREF       'index'
532	POP_BLOCK         None
533	JUMP_ABSOLUTE     '574'
536_0	COME_FROM         '509'

536	DUP_TOP           None
537	LOAD_GLOBAL       'ValueError'
540	COMPARE_OP        'exception match'
543	POP_JUMP_IF_FALSE '564'
546	POP_TOP           None
547	POP_TOP           None
548	POP_TOP           None

549	LOAD_GLOBAL       'SyntaxError'
552	LOAD_CONST        'unsupported expression'
555	CALL_FUNCTION_1   None
558	RAISE_VARARGS_1   None
561	JUMP_ABSOLUTE     '574'
564	END_FINALLY       None
565_0	COME_FROM         '564'
565	JUMP_FORWARD      '574'

568	LOAD_CONST        -1
571	STORE_DEREF       'index'
574_0	COME_FROM         '463'
574_1	COME_FROM         '565'

574	LOAD_CLOSURE      'index'
580	LOAD_CONST        '<code_object select>'
583	MAKE_CLOSURE_0    None
586	STORE_FAST        'select'

589	LOAD_FAST         'select'
592	RETURN_END_IF     None

593	LOAD_GLOBAL       'SyntaxError'
596	LOAD_CONST        'invalid predicate'
599	CALL_FUNCTION_1   None
602	RAISE_VARARGS_1   None

Syntax error at or near `POP_BLOCK' token at offset 143


ops = {'': prepare_child,
 '*': prepare_star,
 '.': prepare_self,
 '..': prepare_parent,
 '//': prepare_descendant,
 '[': prepare_predicate}
_cache = {}

class _SelectorContext:
    parent_map = None

    def __init__(self, root):
        self.root = root


def iterfind--- This code section failed: ---

0	LOAD_FAST         'path'
3	LOAD_CONST        -1
6	SLICE+1           None
7	LOAD_CONST        '/'
10	COMPARE_OP        '=='
13	POP_JUMP_IF_FALSE '29'

16	LOAD_FAST         'path'
19	LOAD_CONST        '*'
22	BINARY_ADD        None
23	STORE_FAST        'path'
26	JUMP_FORWARD      '29'
29_0	COME_FROM         '26'

29	SETUP_EXCEPT      '46'

32	LOAD_GLOBAL       '_cache'
35	LOAD_FAST         'path'
38	BINARY_SUBSCR     None
39	STORE_FAST        'selector'
42	POP_BLOCK         None
43	JUMP_FORWARD      '309'
46_0	COME_FROM         '29'

46	DUP_TOP           None
47	LOAD_GLOBAL       'KeyError'
50	COMPARE_OP        'exception match'
53	POP_JUMP_IF_FALSE '308'
56	POP_TOP           None
57	POP_TOP           None
58	POP_TOP           None

59	LOAD_GLOBAL       'len'
62	LOAD_GLOBAL       '_cache'
65	CALL_FUNCTION_1   None
68	LOAD_CONST        100
71	COMPARE_OP        '>'
74	POP_JUMP_IF_FALSE '90'

77	LOAD_GLOBAL       '_cache'
80	LOAD_ATTR         'clear'
83	CALL_FUNCTION_0   None
86	POP_TOP           None
87	JUMP_FORWARD      '90'
90_0	COME_FROM         '87'

90	LOAD_FAST         'path'
93	LOAD_CONST        1
96	SLICE+2           None
97	LOAD_CONST        '/'
100	COMPARE_OP        '=='
103	POP_JUMP_IF_FALSE '121'

106	LOAD_GLOBAL       'SyntaxError'
109	LOAD_CONST        'cannot use absolute path on element'
112	CALL_FUNCTION_1   None
115	RAISE_VARARGS_1   None
118	JUMP_FORWARD      '121'
121_0	COME_FROM         '118'

121	LOAD_GLOBAL       'iter'
124	LOAD_GLOBAL       'xpath_tokenizer'
127	LOAD_FAST         'path'
130	LOAD_FAST         'namespaces'
133	CALL_FUNCTION_2   None
136	CALL_FUNCTION_1   None
139	LOAD_ATTR         'next'
142	STORE_FAST        'next'

145	LOAD_FAST         'next'
148	CALL_FUNCTION_0   None
151	STORE_FAST        'token'

154	BUILD_LIST_0      None
157	STORE_FAST        'selector'

160	SETUP_LOOP        '295'

163	SETUP_EXCEPT      '200'

166	LOAD_FAST         'selector'
169	LOAD_ATTR         'append'
172	LOAD_GLOBAL       'ops'
175	LOAD_FAST         'token'
178	LOAD_CONST        0
181	BINARY_SUBSCR     None
182	BINARY_SUBSCR     None
183	LOAD_FAST         'next'
186	LOAD_FAST         'token'
189	CALL_FUNCTION_2   None
192	CALL_FUNCTION_1   None
195	POP_TOP           None
196	POP_BLOCK         None
197	JUMP_FORWARD      '229'
200_0	COME_FROM         '163'

200	DUP_TOP           None
201	LOAD_GLOBAL       'StopIteration'
204	COMPARE_OP        'exception match'
207	POP_JUMP_IF_FALSE '228'
210	POP_TOP           None
211	POP_TOP           None
212	POP_TOP           None

213	LOAD_GLOBAL       'SyntaxError'
216	LOAD_CONST        'invalid path'
219	CALL_FUNCTION_1   None
222	RAISE_VARARGS_1   None
225	JUMP_FORWARD      '229'
228	END_FINALLY       None
229_0	COME_FROM         '197'
229_1	COME_FROM         '228'

229	SETUP_EXCEPT      '273'

232	LOAD_FAST         'next'
235	CALL_FUNCTION_0   None
238	STORE_FAST        'token'

241	LOAD_FAST         'token'
244	LOAD_CONST        0
247	BINARY_SUBSCR     None
248	LOAD_CONST        '/'
251	COMPARE_OP        '=='
254	POP_JUMP_IF_FALSE '269'

257	LOAD_FAST         'next'
260	CALL_FUNCTION_0   None
263	STORE_FAST        'token'
266	JUMP_FORWARD      '269'
269_0	COME_FROM         '266'
269	POP_BLOCK         None
270	JUMP_BACK         '163'
273_0	COME_FROM         '229'

273	DUP_TOP           None
274	LOAD_GLOBAL       'StopIteration'
277	COMPARE_OP        'exception match'
280	POP_JUMP_IF_FALSE '290'
283	POP_TOP           None
284	POP_TOP           None
285	POP_TOP           None

286	BREAK_LOOP        None
287	JUMP_BACK         '163'
290	END_FINALLY       None
291_0	COME_FROM         '290'
291	JUMP_BACK         '163'
294	POP_BLOCK         None
295_0	COME_FROM         '160'

295	LOAD_FAST         'selector'
298	LOAD_GLOBAL       '_cache'
301	LOAD_FAST         'path'
304	STORE_SUBSCR      None
305	JUMP_FORWARD      '309'
308	END_FINALLY       None
309_0	COME_FROM         '43'
309_1	COME_FROM         '308'

309	LOAD_FAST         'elem'
312	BUILD_LIST_1      None
315	STORE_FAST        'result'

318	LOAD_GLOBAL       '_SelectorContext'
321	LOAD_FAST         'elem'
324	CALL_FUNCTION_1   None
327	STORE_FAST        'context'

330	SETUP_LOOP        '362'
333	LOAD_FAST         'selector'
336	GET_ITER          None
337	FOR_ITER          '361'
340	STORE_FAST        'select'

343	LOAD_FAST         'select'
346	LOAD_FAST         'context'
349	LOAD_FAST         'result'
352	CALL_FUNCTION_2   None
355	STORE_FAST        'result'
358	JUMP_BACK         '337'
361	POP_BLOCK         None
362_0	COME_FROM         '330'

362	LOAD_FAST         'result'
365	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 294


def find(elem, path, namespaces = None):
    try:
        return iterfind(elem, path, namespaces).next()
    except StopIteration:
        return None

    return None


def findall(elem, path, namespaces = None):
    return list(iterfind(elem, path, namespaces))


def findtext(elem, path, default = None, namespaces = None):
    try:
        elem = iterfind(elem, path, namespaces).next()
        return elem.text or ''
    except StopIteration:
        return default