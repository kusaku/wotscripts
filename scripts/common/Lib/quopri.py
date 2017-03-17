# Embedded file name: scripts/common/Lib/quopri.py
"""Conversions to/from quoted-printable transport encoding as per RFC 1521."""
__all__ = ['encode',
 'decode',
 'encodestring',
 'decodestring']
ESCAPE = '='
MAXLINESIZE = 76
HEX = '0123456789ABCDEF'
EMPTYSTRING = ''
try:
    from binascii import a2b_qp, b2a_qp
except ImportError:
    a2b_qp = None
    b2a_qp = None

def needsquoting(c, quotetabs, header):
    """Decide whether a particular character needs to be quoted.
    
    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    """
    if c in ' \t':
        return quotetabs
    if c == '_':
        return header
    return c == ESCAPE or not ' ' <= c <= '~'


def quote(c):
    """Quote a single character."""
    i = ord(c)
    return ESCAPE + HEX[i // 16] + HEX[i % 16]


def encode--- This code section failed: ---

0	LOAD_GLOBAL       'b2a_qp'
3	LOAD_CONST        None
6	COMPARE_OP        'is not'
9	POP_JUMP_IF_FALSE '65'

12	LOAD_FAST         'input'
15	LOAD_ATTR         'read'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'data'

24	LOAD_GLOBAL       'b2a_qp'
27	LOAD_FAST         'data'
30	LOAD_CONST        'quotetabs'
33	LOAD_FAST         'quotetabs'
36	LOAD_CONST        'header'
39	LOAD_FAST         'header'
42	CALL_FUNCTION_513 None
45	STORE_FAST        'odata'

48	LOAD_FAST         'output'
51	LOAD_ATTR         'write'
54	LOAD_FAST         'odata'
57	CALL_FUNCTION_1   None
60	POP_TOP           None

61	LOAD_CONST        None
64	RETURN_END_IF     None

65	LOAD_FAST         'output'
68	LOAD_CONST        '\n'
71	LOAD_CONST        '<code_object write>'
74	MAKE_FUNCTION_2   None
77	STORE_FAST        'write'

80	LOAD_CONST        None
83	STORE_FAST        'prevline'

86	SETUP_LOOP        '368'

89	LOAD_FAST         'input'
92	LOAD_ATTR         'readline'
95	CALL_FUNCTION_0   None
98	STORE_FAST        'line'

101	LOAD_FAST         'line'
104	POP_JUMP_IF_TRUE  '111'

107	BREAK_LOOP        None
108	JUMP_FORWARD      '111'
111_0	COME_FROM         '108'

111	BUILD_LIST_0      None
114	STORE_FAST        'outline'

117	LOAD_CONST        ''
120	STORE_FAST        'stripped'

123	LOAD_FAST         'line'
126	LOAD_CONST        -1
129	SLICE+1           None
130	LOAD_CONST        '\n'
133	COMPARE_OP        '=='
136	POP_JUMP_IF_FALSE '158'

139	LOAD_FAST         'line'
142	LOAD_CONST        -1
145	SLICE+2           None
146	STORE_FAST        'line'

149	LOAD_CONST        '\n'
152	STORE_FAST        'stripped'
155	JUMP_FORWARD      '158'
158_0	COME_FROM         '155'

158	SETUP_LOOP        '255'
161	LOAD_FAST         'line'
164	GET_ITER          None
165	FOR_ITER          '254'
168	STORE_FAST        'c'

171	LOAD_GLOBAL       'needsquoting'
174	LOAD_FAST         'c'
177	LOAD_FAST         'quotetabs'
180	LOAD_FAST         'header'
183	CALL_FUNCTION_3   None
186	POP_JUMP_IF_FALSE '204'

189	LOAD_GLOBAL       'quote'
192	LOAD_FAST         'c'
195	CALL_FUNCTION_1   None
198	STORE_FAST        'c'
201	JUMP_FORWARD      '204'
204_0	COME_FROM         '201'

204	LOAD_FAST         'header'
207	POP_JUMP_IF_FALSE '238'
210	LOAD_FAST         'c'
213	LOAD_CONST        ' '
216	COMPARE_OP        '=='
219_0	COME_FROM         '207'
219	POP_JUMP_IF_FALSE '238'

222	LOAD_FAST         'outline'
225	LOAD_ATTR         'append'
228	LOAD_CONST        '_'
231	CALL_FUNCTION_1   None
234	POP_TOP           None
235	JUMP_BACK         '165'

238	LOAD_FAST         'outline'
241	LOAD_ATTR         'append'
244	LOAD_FAST         'c'
247	CALL_FUNCTION_1   None
250	POP_TOP           None
251	JUMP_BACK         '165'
254	POP_BLOCK         None
255_0	COME_FROM         '158'

255	LOAD_FAST         'prevline'
258	LOAD_CONST        None
261	COMPARE_OP        'is not'
264	POP_JUMP_IF_FALSE '280'

267	LOAD_FAST         'write'
270	LOAD_FAST         'prevline'
273	CALL_FUNCTION_1   None
276	POP_TOP           None
277	JUMP_FORWARD      '280'
280_0	COME_FROM         '277'

280	LOAD_GLOBAL       'EMPTYSTRING'
283	LOAD_ATTR         'join'
286	LOAD_FAST         'outline'
289	CALL_FUNCTION_1   None
292	STORE_FAST        'thisline'

295	SETUP_LOOP        '358'
298	LOAD_GLOBAL       'len'
301	LOAD_FAST         'thisline'
304	CALL_FUNCTION_1   None
307	LOAD_GLOBAL       'MAXLINESIZE'
310	COMPARE_OP        '>'
313	POP_JUMP_IF_FALSE '357'

316	LOAD_FAST         'write'
319	LOAD_FAST         'thisline'
322	LOAD_GLOBAL       'MAXLINESIZE'
325	LOAD_CONST        1
328	BINARY_SUBTRACT   None
329	SLICE+2           None
330	LOAD_CONST        'lineEnd'
333	LOAD_CONST        '=\n'
336	CALL_FUNCTION_257 None
339	POP_TOP           None

340	LOAD_FAST         'thisline'
343	LOAD_GLOBAL       'MAXLINESIZE'
346	LOAD_CONST        1
349	BINARY_SUBTRACT   None
350	SLICE+1           None
351	STORE_FAST        'thisline'
354	JUMP_BACK         '298'
357	POP_BLOCK         None
358_0	COME_FROM         '295'

358	LOAD_FAST         'thisline'
361	STORE_FAST        'prevline'
364	JUMP_BACK         '89'
367	POP_BLOCK         None
368_0	COME_FROM         '86'

368	LOAD_FAST         'prevline'
371	LOAD_CONST        None
374	COMPARE_OP        'is not'
377	POP_JUMP_IF_FALSE '399'

380	LOAD_FAST         'write'
383	LOAD_FAST         'prevline'
386	LOAD_CONST        'lineEnd'
389	LOAD_FAST         'stripped'
392	CALL_FUNCTION_257 None
395	POP_TOP           None
396	JUMP_FORWARD      '399'
399_0	COME_FROM         '396'
399	LOAD_CONST        None
402	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 367


def encodestring(s, quotetabs = 0, header = 0):
    if b2a_qp is not None:
        return b2a_qp(s, quotetabs=quotetabs, header=header)
    else:
        from cStringIO import StringIO
        infp = StringIO(s)
        outfp = StringIO()
        encode(infp, outfp, quotetabs, header)
        return outfp.getvalue()


def decode--- This code section failed: ---

0	LOAD_GLOBAL       'a2b_qp'
3	LOAD_CONST        None
6	COMPARE_OP        'is not'
9	POP_JUMP_IF_FALSE '59'

12	LOAD_FAST         'input'
15	LOAD_ATTR         'read'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'data'

24	LOAD_GLOBAL       'a2b_qp'
27	LOAD_FAST         'data'
30	LOAD_CONST        'header'
33	LOAD_FAST         'header'
36	CALL_FUNCTION_257 None
39	STORE_FAST        'odata'

42	LOAD_FAST         'output'
45	LOAD_ATTR         'write'
48	LOAD_FAST         'odata'
51	CALL_FUNCTION_1   None
54	POP_TOP           None

55	LOAD_CONST        None
58	RETURN_END_IF     None

59	LOAD_CONST        ''
62	STORE_FAST        'new'

65	SETUP_LOOP        '574'

68	LOAD_FAST         'input'
71	LOAD_ATTR         'readline'
74	CALL_FUNCTION_0   None
77	STORE_FAST        'line'

80	LOAD_FAST         'line'
83	POP_JUMP_IF_TRUE  '90'
86	BREAK_LOOP        None
87	JUMP_FORWARD      '90'
90_0	COME_FROM         '87'

90	LOAD_CONST        0
93	LOAD_GLOBAL       'len'
96	LOAD_FAST         'line'
99	CALL_FUNCTION_1   None
102	ROT_TWO           None
103	STORE_FAST        'i'
106	STORE_FAST        'n'

109	LOAD_FAST         'n'
112	LOAD_CONST        0
115	COMPARE_OP        '>'
118	POP_JUMP_IF_FALSE '209'
121	LOAD_FAST         'line'
124	LOAD_FAST         'n'
127	LOAD_CONST        1
130	BINARY_SUBTRACT   None
131	BINARY_SUBSCR     None
132	LOAD_CONST        '\n'
135	COMPARE_OP        '=='
138_0	COME_FROM         '118'
138	POP_JUMP_IF_FALSE '209'

141	LOAD_CONST        0
144	STORE_FAST        'partial'
147	LOAD_FAST         'n'
150	LOAD_CONST        1
153	BINARY_SUBTRACT   None
154	STORE_FAST        'n'

157	SETUP_LOOP        '215'
160	LOAD_FAST         'n'
163	LOAD_CONST        0
166	COMPARE_OP        '>'
169	POP_JUMP_IF_FALSE '205'
172	LOAD_FAST         'line'
175	LOAD_FAST         'n'
178	LOAD_CONST        1
181	BINARY_SUBTRACT   None
182	BINARY_SUBSCR     None
183	LOAD_CONST        ' \t\r'
186	COMPARE_OP        'in'
189_0	COME_FROM         '169'
189	POP_JUMP_IF_FALSE '205'

192	LOAD_FAST         'n'
195	LOAD_CONST        1
198	BINARY_SUBTRACT   None
199	STORE_FAST        'n'
202	JUMP_BACK         '160'
205	POP_BLOCK         None
206_0	COME_FROM         '157'
206	JUMP_FORWARD      '215'

209	LOAD_CONST        1
212	STORE_FAST        'partial'
215_0	COME_FROM         '206'

215	SETUP_LOOP        '538'
218	LOAD_FAST         'i'
221	LOAD_FAST         'n'
224	COMPARE_OP        '<'
227	POP_JUMP_IF_FALSE '537'

230	LOAD_FAST         'line'
233	LOAD_FAST         'i'
236	BINARY_SUBSCR     None
237	STORE_FAST        'c'

240	LOAD_FAST         'c'
243	LOAD_CONST        '_'
246	COMPARE_OP        '=='
249	POP_JUMP_IF_FALSE '281'
252	LOAD_FAST         'header'
255_0	COME_FROM         '249'
255	POP_JUMP_IF_FALSE '281'

258	LOAD_FAST         'new'
261	LOAD_CONST        ' '
264	BINARY_ADD        None
265	STORE_FAST        'new'
268	LOAD_FAST         'i'
271	LOAD_CONST        1
274	BINARY_ADD        None
275	STORE_FAST        'i'
278	JUMP_BACK         '218'

281	LOAD_FAST         'c'
284	LOAD_GLOBAL       'ESCAPE'
287	COMPARE_OP        '!='
290	POP_JUMP_IF_FALSE '316'

293	LOAD_FAST         'new'
296	LOAD_FAST         'c'
299	BINARY_ADD        None
300	STORE_FAST        'new'
303	LOAD_FAST         'i'
306	LOAD_CONST        1
309	BINARY_ADD        None
310	STORE_FAST        'i'
313	JUMP_BACK         '218'

316	LOAD_FAST         'i'
319	LOAD_CONST        1
322	BINARY_ADD        None
323	LOAD_FAST         'n'
326	COMPARE_OP        '=='
329	POP_JUMP_IF_FALSE '349'
332	LOAD_FAST         'partial'
335	UNARY_NOT         None
336_0	COME_FROM         '329'
336	POP_JUMP_IF_FALSE '349'

339	LOAD_CONST        1
342	STORE_FAST        'partial'
345	BREAK_LOOP        None
346	JUMP_BACK         '218'

349	LOAD_FAST         'i'
352	LOAD_CONST        1
355	BINARY_ADD        None
356	LOAD_FAST         'n'
359	COMPARE_OP        '<'
362	POP_JUMP_IF_FALSE '408'
365	LOAD_FAST         'line'
368	LOAD_FAST         'i'
371	LOAD_CONST        1
374	BINARY_ADD        None
375	BINARY_SUBSCR     None
376	LOAD_GLOBAL       'ESCAPE'
379	COMPARE_OP        '=='
382_0	COME_FROM         '362'
382	POP_JUMP_IF_FALSE '408'

385	LOAD_FAST         'new'
388	LOAD_GLOBAL       'ESCAPE'
391	BINARY_ADD        None
392	STORE_FAST        'new'
395	LOAD_FAST         'i'
398	LOAD_CONST        2
401	BINARY_ADD        None
402	STORE_FAST        'i'
405	JUMP_BACK         '218'

408	LOAD_FAST         'i'
411	LOAD_CONST        2
414	BINARY_ADD        None
415	LOAD_FAST         'n'
418	COMPARE_OP        '<'
421	POP_JUMP_IF_FALSE '514'
424	LOAD_GLOBAL       'ishex'
427	LOAD_FAST         'line'
430	LOAD_FAST         'i'
433	LOAD_CONST        1
436	BINARY_ADD        None
437	BINARY_SUBSCR     None
438	CALL_FUNCTION_1   None
441	POP_JUMP_IF_FALSE '514'
444	LOAD_GLOBAL       'ishex'
447	LOAD_FAST         'line'
450	LOAD_FAST         'i'
453	LOAD_CONST        2
456	BINARY_ADD        None
457	BINARY_SUBSCR     None
458	CALL_FUNCTION_1   None
461_0	COME_FROM         '421'
461_1	COME_FROM         '441'
461	POP_JUMP_IF_FALSE '514'

464	LOAD_FAST         'new'
467	LOAD_GLOBAL       'chr'
470	LOAD_GLOBAL       'unhex'
473	LOAD_FAST         'line'
476	LOAD_FAST         'i'
479	LOAD_CONST        1
482	BINARY_ADD        None
483	LOAD_FAST         'i'
486	LOAD_CONST        3
489	BINARY_ADD        None
490	SLICE+3           None
491	CALL_FUNCTION_1   None
494	CALL_FUNCTION_1   None
497	BINARY_ADD        None
498	STORE_FAST        'new'
501	LOAD_FAST         'i'
504	LOAD_CONST        3
507	BINARY_ADD        None
508	STORE_FAST        'i'
511	JUMP_BACK         '218'

514	LOAD_FAST         'new'
517	LOAD_FAST         'c'
520	BINARY_ADD        None
521	STORE_FAST        'new'
524	LOAD_FAST         'i'
527	LOAD_CONST        1
530	BINARY_ADD        None
531	STORE_FAST        'i'
534	JUMP_BACK         '218'
537	POP_BLOCK         None
538_0	COME_FROM         '215'

538	LOAD_FAST         'partial'
541	POP_JUMP_IF_TRUE  '68'

544	LOAD_FAST         'output'
547	LOAD_ATTR         'write'
550	LOAD_FAST         'new'
553	LOAD_CONST        '\n'
556	BINARY_ADD        None
557	CALL_FUNCTION_1   None
560	POP_TOP           None

561	LOAD_CONST        ''
564	STORE_FAST        'new'
567	JUMP_BACK         '68'
570	JUMP_BACK         '68'
573	POP_BLOCK         None
574_0	COME_FROM         '65'

574	LOAD_FAST         'new'
577	POP_JUMP_IF_FALSE '596'

580	LOAD_FAST         'output'
583	LOAD_ATTR         'write'
586	LOAD_FAST         'new'
589	CALL_FUNCTION_1   None
592	POP_TOP           None
593	JUMP_FORWARD      '596'
596_0	COME_FROM         '593'
596	LOAD_CONST        None
599	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 573


def decodestring(s, header = 0):
    if a2b_qp is not None:
        return a2b_qp(s, header=header)
    else:
        from cStringIO import StringIO
        infp = StringIO(s)
        outfp = StringIO()
        decode(infp, outfp, header=header)
        return outfp.getvalue()


def ishex(c):
    """Return true if the character 'c' is a hexadecimal digit."""
    return '0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'


def unhex(s):
    """Get the integer value of a hexadecimal number."""
    bits = 0
    for c in s:
        if '0' <= c <= '9':
            i = ord('0')
        elif 'a' <= c <= 'f':
            i = ord('a') - 10
        elif 'A' <= c <= 'F':
            i = ord('A') - 10
        else:
            break
        bits = bits * 16 + (ord(c) - i)

    return bits


def main():
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'td')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print msg
        print 'usage: quopri [-t | -d] [file] ...'
        print '-t: quote tabs'
        print '-d: decode; default encode'
        sys.exit(2)

    deco = 0
    tabs = 0
    for o, a in opts:
        if o == '-t':
            tabs = 1
        if o == '-d':
            deco = 1

    if tabs and deco:
        sys.stdout = sys.stderr
        print '-t and -d are mutually exclusive'
        sys.exit(2)
    if not args:
        args = ['-']
    sts = 0
    for file in args:
        if file == '-':
            fp = sys.stdin
        else:
            try:
                fp = open(file)
            except IOError as msg:
                sys.stderr.write("%s: can't open (%s)\n" % (file, msg))
                sts = 1
                continue

        if deco:
            decode(fp, sys.stdout)
        else:
            encode(fp, sys.stdout, tabs)
        if fp is not sys.stdin:
            fp.close()

    if sts:
        sys.exit(sts)


if __name__ == '__main__':
    main()