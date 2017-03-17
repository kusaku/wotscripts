# Embedded file name: scripts/common/Lib/plat-irix6/cdplayer.py
from warnings import warnpy3k
warnpy3k('the cdplayer module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
cdplayerrc = '.cdplayerrc'

class Cdplayer:

    def __init__--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'string'
9	STORE_FAST        'string'

12	LOAD_CONST        ''
15	LOAD_FAST         'self'
18	STORE_ATTR        'artist'

21	LOAD_CONST        ''
24	LOAD_FAST         'self'
27	STORE_ATTR        'title'

30	LOAD_GLOBAL       'type'
33	LOAD_FAST         'tracklist'
36	CALL_FUNCTION_1   None
39	LOAD_GLOBAL       'type'
42	LOAD_CONST        ''
45	CALL_FUNCTION_1   None
48	COMPARE_OP        '=='
51	POP_JUMP_IF_FALSE '167'

54	BUILD_LIST_0      None
57	STORE_FAST        't'

60	SETUP_LOOP        '158'
63	LOAD_GLOBAL       'range'
66	LOAD_CONST        2
69	LOAD_GLOBAL       'len'
72	LOAD_FAST         'tracklist'
75	CALL_FUNCTION_1   None
78	LOAD_CONST        4
81	CALL_FUNCTION_3   None
84	GET_ITER          None
85	FOR_ITER          '157'
88	STORE_FAST        'i'

91	LOAD_FAST         't'
94	LOAD_ATTR         'append'
97	LOAD_CONST        None

100	LOAD_GLOBAL       'int'
103	LOAD_FAST         'tracklist'
106	LOAD_FAST         'i'
109	LOAD_FAST         'i'
112	LOAD_CONST        2
115	BINARY_ADD        None
116	SLICE+3           None
117	CALL_FUNCTION_1   None

120	LOAD_GLOBAL       'int'
123	LOAD_FAST         'tracklist'
126	LOAD_FAST         'i'
129	LOAD_CONST        2
132	BINARY_ADD        None
133	LOAD_FAST         'i'
136	LOAD_CONST        4
139	BINARY_ADD        None
140	SLICE+3           None
141	CALL_FUNCTION_1   None
144	BUILD_TUPLE_2     None
147	BUILD_TUPLE_2     None
150	CALL_FUNCTION_1   None
153	POP_TOP           None
154	JUMP_BACK         '85'
157	POP_BLOCK         None
158_0	COME_FROM         '60'

158	LOAD_FAST         't'
161	STORE_FAST        'tracklist'
164	JUMP_FORWARD      '167'
167_0	COME_FROM         '164'

167	LOAD_CONST        None
170	BUILD_LIST_1      None
173	LOAD_CONST        ''
176	BUILD_LIST_1      None
179	LOAD_GLOBAL       'len'
182	LOAD_FAST         'tracklist'
185	CALL_FUNCTION_1   None
188	BINARY_MULTIPLY   None
189	BINARY_ADD        None
190	LOAD_FAST         'self'
193	STORE_ATTR        'track'

196	LOAD_CONST        'd'
199	LOAD_FAST         'string'
202	LOAD_ATTR         'zfill'
205	LOAD_GLOBAL       'len'
208	LOAD_FAST         'tracklist'
211	CALL_FUNCTION_1   None
214	LOAD_CONST        2
217	CALL_FUNCTION_2   None
220	BINARY_ADD        None
221	LOAD_FAST         'self'
224	STORE_ATTR        'id'

227	SETUP_LOOP        '308'
230	LOAD_FAST         'tracklist'
233	GET_ITER          None
234	FOR_ITER          '307'
237	STORE_FAST        'track'

240	LOAD_FAST         'track'
243	UNPACK_SEQUENCE_2 None
246	STORE_FAST        'start'
249	STORE_FAST        'length'

252	LOAD_FAST         'self'
255	LOAD_ATTR         'id'
258	LOAD_FAST         'string'
261	LOAD_ATTR         'zfill'
264	LOAD_FAST         'length'
267	LOAD_CONST        0
270	BINARY_SUBSCR     None
271	LOAD_CONST        2
274	CALL_FUNCTION_2   None
277	BINARY_ADD        None

278	LOAD_FAST         'string'
281	LOAD_ATTR         'zfill'
284	LOAD_FAST         'length'
287	LOAD_CONST        1
290	BINARY_SUBSCR     None
291	LOAD_CONST        2
294	CALL_FUNCTION_2   None
297	BINARY_ADD        None
298	LOAD_FAST         'self'
301	STORE_ATTR        'id'
304	JUMP_BACK         '234'
307	POP_BLOCK         None
308_0	COME_FROM         '227'

308	SETUP_EXCEPT      '357'

311	LOAD_CONST        -1
314	LOAD_CONST        None
317	IMPORT_NAME       'posix'
320	STORE_FAST        'posix'

323	LOAD_GLOBAL       'open'
326	LOAD_FAST         'posix'
329	LOAD_ATTR         'environ'
332	LOAD_CONST        'HOME'
335	BINARY_SUBSCR     None
336	LOAD_CONST        '/'
339	BINARY_ADD        None
340	LOAD_GLOBAL       'cdplayerrc'
343	BINARY_ADD        None
344	LOAD_CONST        'r'
347	CALL_FUNCTION_2   None
350	STORE_FAST        'f'
353	POP_BLOCK         None
354	JUMP_FORWARD      '375'
357_0	COME_FROM         '308'

357	DUP_TOP           None
358	LOAD_GLOBAL       'IOError'
361	COMPARE_OP        'exception match'
364	POP_JUMP_IF_FALSE '374'
367	POP_TOP           None
368	POP_TOP           None
369	POP_TOP           None

370	LOAD_CONST        None
373	RETURN_VALUE      None
374	END_FINALLY       None
375_0	COME_FROM         '354'
375_1	COME_FROM         '374'

375	LOAD_CONST        -1
378	LOAD_CONST        None
381	IMPORT_NAME       're'
384	STORE_FAST        're'

387	LOAD_FAST         're'
390	LOAD_ATTR         'compile'
393	LOAD_CONST        '^([^:]*):\\t(.*)'
396	CALL_FUNCTION_1   None
399	STORE_FAST        'reg'

402	LOAD_FAST         'self'
405	LOAD_ATTR         'id'
408	LOAD_CONST        '.'
411	BINARY_ADD        None
412	STORE_FAST        's'

415	LOAD_GLOBAL       'len'
418	LOAD_FAST         's'
421	CALL_FUNCTION_1   None
424	STORE_FAST        'l'

427	SETUP_LOOP        '647'

430	LOAD_FAST         'f'
433	LOAD_ATTR         'readline'
436	CALL_FUNCTION_0   None
439	STORE_FAST        'line'

442	LOAD_FAST         'line'
445	LOAD_CONST        ''
448	COMPARE_OP        '=='
451	POP_JUMP_IF_FALSE '458'

454	BREAK_LOOP        None
455	JUMP_FORWARD      '458'
458_0	COME_FROM         '455'

458	LOAD_FAST         'line'
461	LOAD_FAST         'l'
464	SLICE+2           None
465	LOAD_FAST         's'
468	COMPARE_OP        '=='
471	POP_JUMP_IF_FALSE '430'

474	LOAD_FAST         'line'
477	LOAD_FAST         'l'
480	SLICE+1           None
481	STORE_FAST        'line'

484	LOAD_FAST         'reg'
487	LOAD_ATTR         'match'
490	LOAD_FAST         'line'
493	CALL_FUNCTION_1   None
496	STORE_FAST        'match'

499	LOAD_FAST         'match'
502	POP_JUMP_IF_TRUE  '520'

505	LOAD_CONST        'syntax error in ~/'
508	LOAD_GLOBAL       'cdplayerrc'
511	BINARY_ADD        None
512	PRINT_ITEM        None
513	PRINT_NEWLINE_CONT None

514	CONTINUE          '430'
517	JUMP_FORWARD      '520'
520_0	COME_FROM         '517'

520	LOAD_FAST         'match'
523	LOAD_ATTR         'group'
526	LOAD_CONST        1
529	LOAD_CONST        2
532	CALL_FUNCTION_2   None
535	UNPACK_SEQUENCE_2 None
538	STORE_FAST        'name'
541	STORE_FAST        'value'

544	LOAD_FAST         'name'
547	LOAD_CONST        'title'
550	COMPARE_OP        '=='
553	POP_JUMP_IF_FALSE '568'

556	LOAD_FAST         'value'
559	LOAD_FAST         'self'
562	STORE_ATTR        'title'
565	JUMP_ABSOLUTE     '643'

568	LOAD_FAST         'name'
571	LOAD_CONST        'artist'
574	COMPARE_OP        '=='
577	POP_JUMP_IF_FALSE '592'

580	LOAD_FAST         'value'
583	LOAD_FAST         'self'
586	STORE_ATTR        'artist'
589	JUMP_ABSOLUTE     '643'

592	LOAD_FAST         'name'
595	LOAD_CONST        5
598	SLICE+2           None
599	LOAD_CONST        'track'
602	COMPARE_OP        '=='
605	POP_JUMP_IF_FALSE '643'

608	LOAD_GLOBAL       'int'
611	LOAD_FAST         'name'
614	LOAD_CONST        6
617	SLICE+1           None
618	CALL_FUNCTION_1   None
621	STORE_FAST        'trackno'

624	LOAD_FAST         'value'
627	LOAD_FAST         'self'
630	LOAD_ATTR         'track'
633	LOAD_FAST         'trackno'
636	STORE_SUBSCR      None
637	JUMP_ABSOLUTE     '643'
640	JUMP_BACK         '430'
643	JUMP_BACK         '430'
646	POP_BLOCK         None
647_0	COME_FROM         '427'

647	LOAD_FAST         'f'
650	LOAD_ATTR         'close'
653	CALL_FUNCTION_0   None
656	POP_TOP           None
657	LOAD_CONST        None
660	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 646

    def write--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'posix'
9	STORE_FAST        'posix'

12	LOAD_FAST         'posix'
15	LOAD_ATTR         'environ'
18	LOAD_CONST        'HOME'
21	BINARY_SUBSCR     None
22	LOAD_CONST        '/'
25	BINARY_ADD        None
26	LOAD_GLOBAL       'cdplayerrc'
29	BINARY_ADD        None
30	STORE_FAST        'filename'

33	SETUP_EXCEPT      '55'

36	LOAD_GLOBAL       'open'
39	LOAD_FAST         'filename'
42	LOAD_CONST        'r'
45	CALL_FUNCTION_2   None
48	STORE_FAST        'old'
51	POP_BLOCK         None
52	JUMP_FORWARD      '87'
55_0	COME_FROM         '33'

55	DUP_TOP           None
56	LOAD_GLOBAL       'IOError'
59	COMPARE_OP        'exception match'
62	POP_JUMP_IF_FALSE '86'
65	POP_TOP           None
66	POP_TOP           None
67	POP_TOP           None

68	LOAD_GLOBAL       'open'
71	LOAD_CONST        '/dev/null'
74	LOAD_CONST        'r'
77	CALL_FUNCTION_2   None
80	STORE_FAST        'old'
83	JUMP_FORWARD      '87'
86	END_FINALLY       None
87_0	COME_FROM         '52'
87_1	COME_FROM         '86'

87	LOAD_GLOBAL       'open'
90	LOAD_FAST         'filename'
93	LOAD_CONST        '.new'
96	BINARY_ADD        None
97	LOAD_CONST        'w'
100	CALL_FUNCTION_2   None
103	STORE_FAST        'new'

106	LOAD_FAST         'self'
109	LOAD_ATTR         'id'
112	LOAD_CONST        '.'
115	BINARY_ADD        None
116	STORE_FAST        's'

119	LOAD_GLOBAL       'len'
122	LOAD_FAST         's'
125	CALL_FUNCTION_1   None
128	STORE_FAST        'l'

131	SETUP_LOOP        '198'

134	LOAD_FAST         'old'
137	LOAD_ATTR         'readline'
140	CALL_FUNCTION_0   None
143	STORE_FAST        'line'

146	LOAD_FAST         'line'
149	LOAD_CONST        ''
152	COMPARE_OP        '=='
155	POP_JUMP_IF_FALSE '162'

158	BREAK_LOOP        None
159	JUMP_FORWARD      '162'
162_0	COME_FROM         '159'

162	LOAD_FAST         'line'
165	LOAD_FAST         'l'
168	SLICE+2           None
169	LOAD_FAST         's'
172	COMPARE_OP        '!='
175	POP_JUMP_IF_FALSE '134'

178	LOAD_FAST         'new'
181	LOAD_ATTR         'write'
184	LOAD_FAST         'line'
187	CALL_FUNCTION_1   None
190	POP_TOP           None
191	JUMP_BACK         '134'
194	JUMP_BACK         '134'
197	POP_BLOCK         None
198_0	COME_FROM         '131'

198	LOAD_FAST         'new'
201	LOAD_ATTR         'write'
204	LOAD_FAST         'self'
207	LOAD_ATTR         'id'
210	LOAD_CONST        '.title:\t'
213	BINARY_ADD        None
214	LOAD_FAST         'self'
217	LOAD_ATTR         'title'
220	BINARY_ADD        None
221	LOAD_CONST        '\n'
224	BINARY_ADD        None
225	CALL_FUNCTION_1   None
228	POP_TOP           None

229	LOAD_FAST         'new'
232	LOAD_ATTR         'write'
235	LOAD_FAST         'self'
238	LOAD_ATTR         'id'
241	LOAD_CONST        '.artist:\t'
244	BINARY_ADD        None
245	LOAD_FAST         'self'
248	LOAD_ATTR         'artist'
251	BINARY_ADD        None
252	LOAD_CONST        '\n'
255	BINARY_ADD        None
256	CALL_FUNCTION_1   None
259	POP_TOP           None

260	SETUP_LOOP        '331'
263	LOAD_GLOBAL       'range'
266	LOAD_CONST        1
269	LOAD_GLOBAL       'len'
272	LOAD_FAST         'self'
275	LOAD_ATTR         'track'
278	CALL_FUNCTION_1   None
281	CALL_FUNCTION_2   None
284	GET_ITER          None
285	FOR_ITER          '330'
288	STORE_FAST        'i'

291	LOAD_FAST         'new'
294	LOAD_ATTR         'write'
297	LOAD_CONST        '%s.track.%r:\t%s\n'
300	LOAD_FAST         'self'
303	LOAD_ATTR         'id'
306	LOAD_FAST         'i'
309	LOAD_FAST         'self'
312	LOAD_ATTR         'track'
315	LOAD_FAST         'i'
318	BINARY_SUBSCR     None
319	BUILD_TUPLE_3     None
322	BINARY_MODULO     None
323	CALL_FUNCTION_1   None
326	POP_TOP           None
327	JUMP_BACK         '285'
330	POP_BLOCK         None
331_0	COME_FROM         '260'

331	LOAD_FAST         'old'
334	LOAD_ATTR         'close'
337	CALL_FUNCTION_0   None
340	POP_TOP           None

341	LOAD_FAST         'new'
344	LOAD_ATTR         'close'
347	CALL_FUNCTION_0   None
350	POP_TOP           None

351	LOAD_FAST         'posix'
354	LOAD_ATTR         'rename'
357	LOAD_FAST         'filename'
360	LOAD_CONST        '.new'
363	BINARY_ADD        None
364	LOAD_FAST         'filename'
367	CALL_FUNCTION_2   None
370	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 197