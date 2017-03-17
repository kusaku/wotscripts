# Embedded file name: scripts/common/Lib/plat-irix5/cdplayer.py
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
51	POP_JUMP_IF_FALSE '173'

54	BUILD_LIST_0      None
57	STORE_FAST        't'

60	SETUP_LOOP        '164'
63	LOAD_GLOBAL       'range'
66	LOAD_CONST        2
69	LOAD_GLOBAL       'len'
72	LOAD_FAST         'tracklist'
75	CALL_FUNCTION_1   None
78	LOAD_CONST        4
81	CALL_FUNCTION_3   None
84	GET_ITER          None
85	FOR_ITER          '163'
88	STORE_FAST        'i'

91	LOAD_FAST         't'
94	LOAD_ATTR         'append'
97	LOAD_CONST        None

100	LOAD_FAST         'string'
103	LOAD_ATTR         'atoi'
106	LOAD_FAST         'tracklist'
109	LOAD_FAST         'i'
112	LOAD_FAST         'i'
115	LOAD_CONST        2
118	BINARY_ADD        None
119	SLICE+3           None
120	CALL_FUNCTION_1   None

123	LOAD_FAST         'string'
126	LOAD_ATTR         'atoi'
129	LOAD_FAST         'tracklist'
132	LOAD_FAST         'i'
135	LOAD_CONST        2
138	BINARY_ADD        None
139	LOAD_FAST         'i'
142	LOAD_CONST        4
145	BINARY_ADD        None
146	SLICE+3           None
147	CALL_FUNCTION_1   None
150	BUILD_TUPLE_2     None
153	BUILD_TUPLE_2     None
156	CALL_FUNCTION_1   None
159	POP_TOP           None
160	JUMP_BACK         '85'
163	POP_BLOCK         None
164_0	COME_FROM         '60'

164	LOAD_FAST         't'
167	STORE_FAST        'tracklist'
170	JUMP_FORWARD      '173'
173_0	COME_FROM         '170'

173	LOAD_CONST        None
176	BUILD_LIST_1      None
179	LOAD_CONST        ''
182	BUILD_LIST_1      None
185	LOAD_GLOBAL       'len'
188	LOAD_FAST         'tracklist'
191	CALL_FUNCTION_1   None
194	BINARY_MULTIPLY   None
195	BINARY_ADD        None
196	LOAD_FAST         'self'
199	STORE_ATTR        'track'

202	LOAD_CONST        'd'
205	LOAD_FAST         'string'
208	LOAD_ATTR         'zfill'
211	LOAD_GLOBAL       'len'
214	LOAD_FAST         'tracklist'
217	CALL_FUNCTION_1   None
220	LOAD_CONST        2
223	CALL_FUNCTION_2   None
226	BINARY_ADD        None
227	LOAD_FAST         'self'
230	STORE_ATTR        'id'

233	SETUP_LOOP        '314'
236	LOAD_FAST         'tracklist'
239	GET_ITER          None
240	FOR_ITER          '313'
243	STORE_FAST        'track'

246	LOAD_FAST         'track'
249	UNPACK_SEQUENCE_2 None
252	STORE_FAST        'start'
255	STORE_FAST        'length'

258	LOAD_FAST         'self'
261	LOAD_ATTR         'id'
264	LOAD_FAST         'string'
267	LOAD_ATTR         'zfill'
270	LOAD_FAST         'length'
273	LOAD_CONST        0
276	BINARY_SUBSCR     None
277	LOAD_CONST        2
280	CALL_FUNCTION_2   None
283	BINARY_ADD        None

284	LOAD_FAST         'string'
287	LOAD_ATTR         'zfill'
290	LOAD_FAST         'length'
293	LOAD_CONST        1
296	BINARY_SUBSCR     None
297	LOAD_CONST        2
300	CALL_FUNCTION_2   None
303	BINARY_ADD        None
304	LOAD_FAST         'self'
307	STORE_ATTR        'id'
310	JUMP_BACK         '240'
313	POP_BLOCK         None
314_0	COME_FROM         '233'

314	SETUP_EXCEPT      '363'

317	LOAD_CONST        -1
320	LOAD_CONST        None
323	IMPORT_NAME       'posix'
326	STORE_FAST        'posix'

329	LOAD_GLOBAL       'open'
332	LOAD_FAST         'posix'
335	LOAD_ATTR         'environ'
338	LOAD_CONST        'HOME'
341	BINARY_SUBSCR     None
342	LOAD_CONST        '/'
345	BINARY_ADD        None
346	LOAD_GLOBAL       'cdplayerrc'
349	BINARY_ADD        None
350	LOAD_CONST        'r'
353	CALL_FUNCTION_2   None
356	STORE_FAST        'f'
359	POP_BLOCK         None
360	JUMP_FORWARD      '381'
363_0	COME_FROM         '314'

363	DUP_TOP           None
364	LOAD_GLOBAL       'IOError'
367	COMPARE_OP        'exception match'
370	POP_JUMP_IF_FALSE '380'
373	POP_TOP           None
374	POP_TOP           None
375	POP_TOP           None

376	LOAD_CONST        None
379	RETURN_VALUE      None
380	END_FINALLY       None
381_0	COME_FROM         '360'
381_1	COME_FROM         '380'

381	LOAD_CONST        -1
384	LOAD_CONST        None
387	IMPORT_NAME       're'
390	STORE_FAST        're'

393	LOAD_FAST         're'
396	LOAD_ATTR         'compile'
399	LOAD_CONST        '^([^:]*):\\t(.*)'
402	CALL_FUNCTION_1   None
405	STORE_FAST        'reg'

408	LOAD_FAST         'self'
411	LOAD_ATTR         'id'
414	LOAD_CONST        '.'
417	BINARY_ADD        None
418	STORE_FAST        's'

421	LOAD_GLOBAL       'len'
424	LOAD_FAST         's'
427	CALL_FUNCTION_1   None
430	STORE_FAST        'l'

433	SETUP_LOOP        '656'

436	LOAD_FAST         'f'
439	LOAD_ATTR         'readline'
442	CALL_FUNCTION_0   None
445	STORE_FAST        'line'

448	LOAD_FAST         'line'
451	LOAD_CONST        ''
454	COMPARE_OP        '=='
457	POP_JUMP_IF_FALSE '464'

460	BREAK_LOOP        None
461	JUMP_FORWARD      '464'
464_0	COME_FROM         '461'

464	LOAD_FAST         'line'
467	LOAD_FAST         'l'
470	SLICE+2           None
471	LOAD_FAST         's'
474	COMPARE_OP        '=='
477	POP_JUMP_IF_FALSE '436'

480	LOAD_FAST         'line'
483	LOAD_FAST         'l'
486	SLICE+1           None
487	STORE_FAST        'line'

490	LOAD_FAST         'reg'
493	LOAD_ATTR         'match'
496	LOAD_FAST         'line'
499	CALL_FUNCTION_1   None
502	STORE_FAST        'match'

505	LOAD_FAST         'match'
508	POP_JUMP_IF_TRUE  '526'

511	LOAD_CONST        'syntax error in ~/'
514	LOAD_GLOBAL       'cdplayerrc'
517	BINARY_ADD        None
518	PRINT_ITEM        None
519	PRINT_NEWLINE_CONT None

520	CONTINUE          '436'
523	JUMP_FORWARD      '526'
526_0	COME_FROM         '523'

526	LOAD_FAST         'match'
529	LOAD_ATTR         'group'
532	LOAD_CONST        1
535	LOAD_CONST        2
538	CALL_FUNCTION_2   None
541	UNPACK_SEQUENCE_2 None
544	STORE_FAST        'name'
547	STORE_FAST        'value'

550	LOAD_FAST         'name'
553	LOAD_CONST        'title'
556	COMPARE_OP        '=='
559	POP_JUMP_IF_FALSE '574'

562	LOAD_FAST         'value'
565	LOAD_FAST         'self'
568	STORE_ATTR        'title'
571	JUMP_ABSOLUTE     '652'

574	LOAD_FAST         'name'
577	LOAD_CONST        'artist'
580	COMPARE_OP        '=='
583	POP_JUMP_IF_FALSE '598'

586	LOAD_FAST         'value'
589	LOAD_FAST         'self'
592	STORE_ATTR        'artist'
595	JUMP_ABSOLUTE     '652'

598	LOAD_FAST         'name'
601	LOAD_CONST        5
604	SLICE+2           None
605	LOAD_CONST        'track'
608	COMPARE_OP        '=='
611	POP_JUMP_IF_FALSE '652'

614	LOAD_FAST         'string'
617	LOAD_ATTR         'atoi'
620	LOAD_FAST         'name'
623	LOAD_CONST        6
626	SLICE+1           None
627	CALL_FUNCTION_1   None
630	STORE_FAST        'trackno'

633	LOAD_FAST         'value'
636	LOAD_FAST         'self'
639	LOAD_ATTR         'track'
642	LOAD_FAST         'trackno'
645	STORE_SUBSCR      None
646	JUMP_ABSOLUTE     '652'
649	JUMP_BACK         '436'
652	JUMP_BACK         '436'
655	POP_BLOCK         None
656_0	COME_FROM         '433'

656	LOAD_FAST         'f'
659	LOAD_ATTR         'close'
662	CALL_FUNCTION_0   None
665	POP_TOP           None
666	LOAD_CONST        None
669	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 655

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