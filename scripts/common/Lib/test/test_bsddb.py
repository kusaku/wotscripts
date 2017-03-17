# Embedded file name: scripts/common/Lib/test/test_bsddb.py
"""Test script for the bsddb C module by Roger E. Masse
   Adapted to unittest format and expanded scope by Raymond Hettinger
"""
import os, sys
import unittest
from test import test_support
test_support.import_module('_bsddb')
bsddb = test_support.import_module('bsddb', deprecated=True)
test_support.import_module('dbhash', deprecated=True)

class TestBSDDB(unittest.TestCase):
    openflag = 'c'

    def setUp(self):
        self.f = self.openmethod[0](self.fname, self.openflag, cachesize=32768)
        self.d = dict(q='Guido', w='van', e='Rossum', r='invented', t='Python', y='')
        for k, v in self.d.iteritems():
            self.f[k] = v

    def tearDown(self):
        self.f.sync()
        self.f.close()
        if self.fname is None:
            return
        else:
            try:
                os.remove(self.fname)
            except os.error:
                pass

            return

    def test_getitem(self):
        for k, v in self.d.iteritems():
            self.assertEqual(self.f[k], v)

    def test_len(self):
        self.assertEqual(len(self.f), len(self.d))

    def test_change(self):
        self.f['r'] = 'discovered'
        self.assertEqual(self.f['r'], 'discovered')
        self.assertIn('r', self.f.keys())
        self.assertIn('discovered', self.f.values())

    def test_close_and_reopen(self):
        if self.fname is None:
            return
        else:
            self.f.close()
            self.f = self.openmethod[0](self.fname, 'w')
            for k, v in self.d.iteritems():
                self.assertEqual(self.f[k], v)

            return

    def assertSetEquals(self, seqn1, seqn2):
        self.assertEqual(set(seqn1), set(seqn2))

    def test_mapping_iteration_methods(self):
        f = self.f
        d = self.d
        self.assertSetEquals(d, f)
        self.assertSetEquals(d.keys(), f.keys())
        self.assertSetEquals(d.values(), f.values())
        self.assertSetEquals(d.items(), f.items())
        self.assertSetEquals(d.iterkeys(), f.iterkeys())
        self.assertSetEquals(d.itervalues(), f.itervalues())
        self.assertSetEquals(d.iteritems(), f.iteritems())

    def test_iter_while_modifying_values--- This code section failed: ---

0	LOAD_GLOBAL       'iter'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'd'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'di'

15	SETUP_LOOP        '76'

18	SETUP_EXCEPT      '54'

21	LOAD_FAST         'di'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	STORE_FAST        'key'

33	LOAD_CONST        'modified '
36	LOAD_FAST         'key'
39	BINARY_ADD        None
40	LOAD_FAST         'self'
43	LOAD_ATTR         'd'
46	LOAD_FAST         'key'
49	STORE_SUBSCR      None
50	POP_BLOCK         None
51	JUMP_BACK         '18'
54_0	COME_FROM         '18'

54	DUP_TOP           None
55	LOAD_GLOBAL       'StopIteration'
58	COMPARE_OP        'exception match'
61	POP_JUMP_IF_FALSE '71'
64	POP_TOP           None
65	POP_TOP           None
66	POP_TOP           None

67	BREAK_LOOP        None
68	JUMP_BACK         '18'
71	END_FINALLY       None
72_0	COME_FROM         '71'
72	JUMP_BACK         '18'
75	POP_BLOCK         None
76_0	COME_FROM         '15'

76	LOAD_GLOBAL       'len'
79	LOAD_FAST         'self'
82	LOAD_ATTR         'f'
85	CALL_FUNCTION_1   None
88	STORE_FAST        'loops_left'

91	LOAD_GLOBAL       'iter'
94	LOAD_FAST         'self'
97	LOAD_ATTR         'f'
100	CALL_FUNCTION_1   None
103	STORE_FAST        'fi'

106	SETUP_LOOP        '177'

109	SETUP_EXCEPT      '155'

112	LOAD_FAST         'fi'
115	LOAD_ATTR         'next'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'key'

124	LOAD_CONST        'modified '
127	LOAD_FAST         'key'
130	BINARY_ADD        None
131	LOAD_FAST         'self'
134	LOAD_ATTR         'f'
137	LOAD_FAST         'key'
140	STORE_SUBSCR      None

141	LOAD_FAST         'loops_left'
144	LOAD_CONST        1
147	INPLACE_SUBTRACT  None
148	STORE_FAST        'loops_left'
151	POP_BLOCK         None
152	JUMP_BACK         '109'
155_0	COME_FROM         '109'

155	DUP_TOP           None
156	LOAD_GLOBAL       'StopIteration'
159	COMPARE_OP        'exception match'
162	POP_JUMP_IF_FALSE '172'
165	POP_TOP           None
166	POP_TOP           None
167	POP_TOP           None

168	BREAK_LOOP        None
169	JUMP_BACK         '109'
172	END_FINALLY       None
173_0	COME_FROM         '172'
173	JUMP_BACK         '109'
176	POP_BLOCK         None
177_0	COME_FROM         '106'

177	LOAD_FAST         'self'
180	LOAD_ATTR         'assertEqual'
183	LOAD_FAST         'loops_left'
186	LOAD_CONST        0
189	CALL_FUNCTION_2   None
192	POP_TOP           None

193	LOAD_FAST         'self'
196	LOAD_ATTR         'test_mapping_iteration_methods'
199	CALL_FUNCTION_0   None
202	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 75

    def test_iter_abort_on_changed_size(self):

        def DictIterAbort--- This code section failed: ---

0	LOAD_GLOBAL       'iter'
3	LOAD_DEREF        'self'
6	LOAD_ATTR         'd'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'di'

15	SETUP_LOOP        '70'

18	SETUP_EXCEPT      '48'

21	LOAD_FAST         'di'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	POP_TOP           None

31	LOAD_CONST        'SPAM'
34	LOAD_DEREF        'self'
37	LOAD_ATTR         'd'
40	LOAD_CONST        'newkey'
43	STORE_SUBSCR      None
44	POP_BLOCK         None
45	JUMP_BACK         '18'
48_0	COME_FROM         '18'

48	DUP_TOP           None
49	LOAD_GLOBAL       'StopIteration'
52	COMPARE_OP        'exception match'
55	POP_JUMP_IF_FALSE '65'
58	POP_TOP           None
59	POP_TOP           None
60	POP_TOP           None

61	BREAK_LOOP        None
62	JUMP_BACK         '18'
65	END_FINALLY       None
66_0	COME_FROM         '65'
66	JUMP_BACK         '18'
69	POP_BLOCK         None
70_0	COME_FROM         '15'

Syntax error at or near `POP_BLOCK' token at offset 69

        self.assertRaises(RuntimeError, DictIterAbort)

        def DbIterAbort--- This code section failed: ---

0	LOAD_GLOBAL       'iter'
3	LOAD_DEREF        'self'
6	LOAD_ATTR         'f'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'fi'

15	SETUP_LOOP        '70'

18	SETUP_EXCEPT      '48'

21	LOAD_FAST         'fi'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	POP_TOP           None

31	LOAD_CONST        'SPAM'
34	LOAD_DEREF        'self'
37	LOAD_ATTR         'f'
40	LOAD_CONST        'newkey'
43	STORE_SUBSCR      None
44	POP_BLOCK         None
45	JUMP_BACK         '18'
48_0	COME_FROM         '18'

48	DUP_TOP           None
49	LOAD_GLOBAL       'StopIteration'
52	COMPARE_OP        'exception match'
55	POP_JUMP_IF_FALSE '65'
58	POP_TOP           None
59	POP_TOP           None
60	POP_TOP           None

61	BREAK_LOOP        None
62	JUMP_BACK         '18'
65	END_FINALLY       None
66_0	COME_FROM         '65'
66	JUMP_BACK         '18'
69	POP_BLOCK         None
70_0	COME_FROM         '15'

Syntax error at or near `POP_BLOCK' token at offset 69

        self.assertRaises(RuntimeError, DbIterAbort)

    def test_iteritems_abort_on_changed_size(self):

        def DictIteritemsAbort--- This code section failed: ---

0	LOAD_DEREF        'self'
3	LOAD_ATTR         'd'
6	LOAD_ATTR         'iteritems'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'di'

15	SETUP_LOOP        '70'

18	SETUP_EXCEPT      '48'

21	LOAD_FAST         'di'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	POP_TOP           None

31	LOAD_CONST        'SPAM'
34	LOAD_DEREF        'self'
37	LOAD_ATTR         'd'
40	LOAD_CONST        'newkey'
43	STORE_SUBSCR      None
44	POP_BLOCK         None
45	JUMP_BACK         '18'
48_0	COME_FROM         '18'

48	DUP_TOP           None
49	LOAD_GLOBAL       'StopIteration'
52	COMPARE_OP        'exception match'
55	POP_JUMP_IF_FALSE '65'
58	POP_TOP           None
59	POP_TOP           None
60	POP_TOP           None

61	BREAK_LOOP        None
62	JUMP_BACK         '18'
65	END_FINALLY       None
66_0	COME_FROM         '65'
66	JUMP_BACK         '18'
69	POP_BLOCK         None
70_0	COME_FROM         '15'

Syntax error at or near `POP_BLOCK' token at offset 69

        self.assertRaises(RuntimeError, DictIteritemsAbort)

        def DbIteritemsAbort--- This code section failed: ---

0	LOAD_DEREF        'self'
3	LOAD_ATTR         'f'
6	LOAD_ATTR         'iteritems'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'fi'

15	SETUP_LOOP        '75'

18	SETUP_EXCEPT      '53'

21	LOAD_FAST         'fi'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	UNPACK_SEQUENCE_2 None
33	STORE_FAST        'key'
36	STORE_FAST        'value'

39	LOAD_DEREF        'self'
42	LOAD_ATTR         'f'
45	LOAD_FAST         'key'
48	DELETE_SUBSCR     None
49	POP_BLOCK         None
50	JUMP_BACK         '18'
53_0	COME_FROM         '18'

53	DUP_TOP           None
54	LOAD_GLOBAL       'StopIteration'
57	COMPARE_OP        'exception match'
60	POP_JUMP_IF_FALSE '70'
63	POP_TOP           None
64	POP_TOP           None
65	POP_TOP           None

66	BREAK_LOOP        None
67	JUMP_BACK         '18'
70	END_FINALLY       None
71_0	COME_FROM         '70'
71	JUMP_BACK         '18'
74	POP_BLOCK         None
75_0	COME_FROM         '15'

Syntax error at or near `POP_BLOCK' token at offset 74

        self.assertRaises(RuntimeError, DbIteritemsAbort)

    def test_iteritems_while_modifying_values--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'd'
6	LOAD_ATTR         'iteritems'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'di'

15	SETUP_LOOP        '82'

18	SETUP_EXCEPT      '60'

21	LOAD_FAST         'di'
24	LOAD_ATTR         'next'
27	CALL_FUNCTION_0   None
30	UNPACK_SEQUENCE_2 None
33	STORE_FAST        'k'
36	STORE_FAST        'v'

39	LOAD_CONST        'modified '
42	LOAD_FAST         'v'
45	BINARY_ADD        None
46	LOAD_FAST         'self'
49	LOAD_ATTR         'd'
52	LOAD_FAST         'k'
55	STORE_SUBSCR      None
56	POP_BLOCK         None
57	JUMP_BACK         '18'
60_0	COME_FROM         '18'

60	DUP_TOP           None
61	LOAD_GLOBAL       'StopIteration'
64	COMPARE_OP        'exception match'
67	POP_JUMP_IF_FALSE '77'
70	POP_TOP           None
71	POP_TOP           None
72	POP_TOP           None

73	BREAK_LOOP        None
74	JUMP_BACK         '18'
77	END_FINALLY       None
78_0	COME_FROM         '77'
78	JUMP_BACK         '18'
81	POP_BLOCK         None
82_0	COME_FROM         '15'

82	LOAD_GLOBAL       'len'
85	LOAD_FAST         'self'
88	LOAD_ATTR         'f'
91	CALL_FUNCTION_1   None
94	STORE_FAST        'loops_left'

97	LOAD_FAST         'self'
100	LOAD_ATTR         'f'
103	LOAD_ATTR         'iteritems'
106	CALL_FUNCTION_0   None
109	STORE_FAST        'fi'

112	SETUP_LOOP        '189'

115	SETUP_EXCEPT      '167'

118	LOAD_FAST         'fi'
121	LOAD_ATTR         'next'
124	CALL_FUNCTION_0   None
127	UNPACK_SEQUENCE_2 None
130	STORE_FAST        'k'
133	STORE_FAST        'v'

136	LOAD_CONST        'modified '
139	LOAD_FAST         'v'
142	BINARY_ADD        None
143	LOAD_FAST         'self'
146	LOAD_ATTR         'f'
149	LOAD_FAST         'k'
152	STORE_SUBSCR      None

153	LOAD_FAST         'loops_left'
156	LOAD_CONST        1
159	INPLACE_SUBTRACT  None
160	STORE_FAST        'loops_left'
163	POP_BLOCK         None
164	JUMP_BACK         '115'
167_0	COME_FROM         '115'

167	DUP_TOP           None
168	LOAD_GLOBAL       'StopIteration'
171	COMPARE_OP        'exception match'
174	POP_JUMP_IF_FALSE '184'
177	POP_TOP           None
178	POP_TOP           None
179	POP_TOP           None

180	BREAK_LOOP        None
181	JUMP_BACK         '115'
184	END_FINALLY       None
185_0	COME_FROM         '184'
185	JUMP_BACK         '115'
188	POP_BLOCK         None
189_0	COME_FROM         '112'

189	LOAD_FAST         'self'
192	LOAD_ATTR         'assertEqual'
195	LOAD_FAST         'loops_left'
198	LOAD_CONST        0
201	CALL_FUNCTION_2   None
204	POP_TOP           None

205	LOAD_FAST         'self'
208	LOAD_ATTR         'test_mapping_iteration_methods'
211	CALL_FUNCTION_0   None
214	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 81

    def test_first_next_looping(self):
        items = [self.f.first()]
        for i in xrange(1, len(self.f)):
            items.append(self.f.next())

        self.assertSetEquals(items, self.d.items())

    def test_previous_last_looping(self):
        items = [self.f.last()]
        for i in xrange(1, len(self.f)):
            items.append(self.f.previous())

        self.assertSetEquals(items, self.d.items())

    def test_first_while_deleting(self):
        self.assertTrue(len(self.d) >= 2, 'test requires >=2 items')
        for _ in self.d:
            key = self.f.first()[0]
            del self.f[key]

        self.assertEqual([], self.f.items(), 'expected empty db after test')

    def test_last_while_deleting(self):
        self.assertTrue(len(self.d) >= 2, 'test requires >=2 items')
        for _ in self.d:
            key = self.f.last()[0]
            del self.f[key]

        self.assertEqual([], self.f.items(), 'expected empty db after test')

    def test_set_location(self):
        self.assertEqual(self.f.set_location('e'), ('e', self.d['e']))

    def test_contains(self):
        for k in self.d:
            self.assertIn(k, self.f)

        self.assertNotIn('not here', self.f)

    def test_has_key(self):
        for k in self.d:
            self.assertTrue(self.f.has_key(k))

        self.assertTrue(not self.f.has_key('not here'))

    def test_clear(self):
        self.f.clear()
        self.assertEqual(len(self.f), 0)

    def test__no_deadlock_first--- This code section failed: ---

0	LOAD_GLOBAL       'sys'
3	LOAD_ATTR         'stdout'
6	LOAD_ATTR         'flush'
9	CALL_FUNCTION_0   None
12	POP_TOP           None

13	LOAD_FAST         'debug'
16	POP_JUMP_IF_FALSE '27'
19	LOAD_CONST        'A'
22	PRINT_ITEM        None
23	PRINT_NEWLINE_CONT None
24	JUMP_FORWARD      '27'
27_0	COME_FROM         '24'

27	LOAD_FAST         'self'
30	LOAD_ATTR         'f'
33	LOAD_ATTR         'first'
36	CALL_FUNCTION_0   None
39	UNPACK_SEQUENCE_2 None
42	STORE_FAST        'k'
45	STORE_FAST        'v'

48	LOAD_FAST         'debug'
51	POP_JUMP_IF_FALSE '66'
54	LOAD_CONST        'B'
57	PRINT_ITEM        None
58	LOAD_FAST         'k'
61	PRINT_ITEM_CONT   None
62	PRINT_NEWLINE_CONT None
63	JUMP_FORWARD      '66'
66_0	COME_FROM         '63'

66	LOAD_CONST        'deadlock.  do not pass go.  do not collect $200.'
69	LOAD_FAST         'self'
72	LOAD_ATTR         'f'
75	LOAD_FAST         'k'
78	STORE_SUBSCR      None

79	LOAD_FAST         'debug'
82	POP_JUMP_IF_FALSE '93'
85	LOAD_CONST        'C'
88	PRINT_ITEM        None
89	PRINT_NEWLINE_CONT None
90	JUMP_FORWARD      '93'
93_0	COME_FROM         '90'

93	LOAD_GLOBAL       'True'
96	POP_JUMP_IF_FALSE '407'

99	LOAD_FAST         'debug'
102	POP_JUMP_IF_FALSE '113'
105	LOAD_CONST        'D'
108	PRINT_ITEM        None
109	PRINT_NEWLINE_CONT None
110	JUMP_FORWARD      '113'
113_0	COME_FROM         '110'

113	LOAD_FAST         'self'
116	LOAD_ATTR         'f'
119	LOAD_ATTR         'iteritems'
122	CALL_FUNCTION_0   None
125	STORE_FAST        'i'

128	LOAD_FAST         'i'
131	LOAD_ATTR         'next'
134	CALL_FUNCTION_0   None
137	UNPACK_SEQUENCE_2 None
140	STORE_FAST        'k'
143	STORE_FAST        'v'

146	LOAD_FAST         'debug'
149	POP_JUMP_IF_FALSE '160'
152	LOAD_CONST        'E'
155	PRINT_ITEM        None
156	PRINT_NEWLINE_CONT None
157	JUMP_FORWARD      '160'
160_0	COME_FROM         '157'

160	LOAD_CONST        "please don't deadlock"
163	LOAD_FAST         'self'
166	LOAD_ATTR         'f'
169	LOAD_FAST         'k'
172	STORE_SUBSCR      None

173	LOAD_FAST         'debug'
176	POP_JUMP_IF_FALSE '187'
179	LOAD_CONST        'F'
182	PRINT_ITEM        None
183	PRINT_NEWLINE_CONT None
184	JUMP_FORWARD      '187'
187_0	COME_FROM         '184'

187	SETUP_LOOP        '237'

190	SETUP_EXCEPT      '215'

193	LOAD_FAST         'i'
196	LOAD_ATTR         'next'
199	CALL_FUNCTION_0   None
202	UNPACK_SEQUENCE_2 None
205	STORE_FAST        'k'
208	STORE_FAST        'v'
211	POP_BLOCK         None
212	JUMP_BACK         '190'
215_0	COME_FROM         '190'

215	DUP_TOP           None
216	LOAD_GLOBAL       'StopIteration'
219	COMPARE_OP        'exception match'
222	POP_JUMP_IF_FALSE '232'
225	POP_TOP           None
226	POP_TOP           None
227	POP_TOP           None

228	BREAK_LOOP        None
229	JUMP_BACK         '190'
232	END_FINALLY       None
233_0	COME_FROM         '232'
233	JUMP_BACK         '190'
236	POP_BLOCK         None
237_0	COME_FROM         '187'

237	LOAD_FAST         'debug'
240	POP_JUMP_IF_FALSE '251'
243	LOAD_CONST        'F2'
246	PRINT_ITEM        None
247	PRINT_NEWLINE_CONT None
248	JUMP_FORWARD      '251'
251_0	COME_FROM         '248'

251	LOAD_GLOBAL       'iter'
254	LOAD_FAST         'self'
257	LOAD_ATTR         'f'
260	CALL_FUNCTION_1   None
263	STORE_FAST        'i'

266	LOAD_FAST         'debug'
269	POP_JUMP_IF_FALSE '280'
272	LOAD_CONST        'G'
275	PRINT_ITEM        None
276	PRINT_NEWLINE_CONT None
277	JUMP_FORWARD      '280'
280_0	COME_FROM         '277'

280	SETUP_LOOP        '390'
283	LOAD_FAST         'i'
286	POP_JUMP_IF_FALSE '389'

289	SETUP_EXCEPT      '363'

292	LOAD_FAST         'debug'
295	POP_JUMP_IF_FALSE '306'
298	LOAD_CONST        'H'
301	PRINT_ITEM        None
302	PRINT_NEWLINE_CONT None
303	JUMP_FORWARD      '306'
306_0	COME_FROM         '303'

306	LOAD_FAST         'i'
309	LOAD_ATTR         'next'
312	CALL_FUNCTION_0   None
315	STORE_FAST        'k'

318	LOAD_FAST         'debug'
321	POP_JUMP_IF_FALSE '332'
324	LOAD_CONST        'I'
327	PRINT_ITEM        None
328	PRINT_NEWLINE_CONT None
329	JUMP_FORWARD      '332'
332_0	COME_FROM         '329'

332	LOAD_CONST        'deadlocks-r-us'
335	LOAD_FAST         'self'
338	LOAD_ATTR         'f'
341	LOAD_FAST         'k'
344	STORE_SUBSCR      None

345	LOAD_FAST         'debug'
348	POP_JUMP_IF_FALSE '359'
351	LOAD_CONST        'J'
354	PRINT_ITEM        None
355	PRINT_NEWLINE_CONT None
356	JUMP_FORWARD      '359'
359_0	COME_FROM         '356'
359	POP_BLOCK         None
360	JUMP_BACK         '283'
363_0	COME_FROM         '289'

363	DUP_TOP           None
364	LOAD_GLOBAL       'StopIteration'
367	COMPARE_OP        'exception match'
370	POP_JUMP_IF_FALSE '385'
373	POP_TOP           None
374	POP_TOP           None
375	POP_TOP           None

376	LOAD_CONST        None
379	STORE_FAST        'i'
382	JUMP_BACK         '283'
385	END_FINALLY       None
386_0	COME_FROM         '385'
386	JUMP_BACK         '283'
389	POP_BLOCK         None
390_0	COME_FROM         '280'

390	LOAD_FAST         'debug'
393	POP_JUMP_IF_FALSE '407'
396	LOAD_CONST        'K'
399	PRINT_ITEM        None
400	PRINT_NEWLINE_CONT None
401	JUMP_ABSOLUTE     '407'
404	JUMP_FORWARD      '407'
407_0	COME_FROM         '404'

407	LOAD_FAST         'self'
410	LOAD_ATTR         'assertIn'
413	LOAD_FAST         'self'
416	LOAD_ATTR         'f'
419	LOAD_ATTR         'first'
422	CALL_FUNCTION_0   None
425	LOAD_CONST        0
428	BINARY_SUBSCR     None
429	LOAD_FAST         'self'
432	LOAD_ATTR         'd'
435	CALL_FUNCTION_2   None
438	POP_TOP           None

439	LOAD_FAST         'self'
442	LOAD_ATTR         'f'
445	LOAD_ATTR         'next'
448	CALL_FUNCTION_0   None
451	LOAD_CONST        0
454	BINARY_SUBSCR     None
455	STORE_FAST        'k'

458	LOAD_FAST         'self'
461	LOAD_ATTR         'assertIn'
464	LOAD_FAST         'k'
467	LOAD_FAST         'self'
470	LOAD_ATTR         'd'
473	CALL_FUNCTION_2   None
476	POP_TOP           None

477	LOAD_CONST        'be gone with ye deadlocks'
480	LOAD_FAST         'self'
483	LOAD_ATTR         'f'
486	LOAD_FAST         'k'
489	STORE_SUBSCR      None

490	LOAD_FAST         'self'
493	LOAD_ATTR         'assertTrue'
496	LOAD_FAST         'self'
499	LOAD_ATTR         'f'
502	LOAD_FAST         'k'
505	BINARY_SUBSCR     None
506	LOAD_CONST        'be gone with ye deadlocks'
509	CALL_FUNCTION_2   None
512	POP_TOP           None
513	LOAD_CONST        None
516	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 236

    def test_for_cursor_memleak(self):
        nc1 = len(self.f._cursor_refs)
        i = self.f.iteritems()
        nc2 = len(self.f._cursor_refs)
        k, v = i.next()
        nc3 = len(self.f._cursor_refs)
        del i
        nc4 = len(self.f._cursor_refs)
        self.assertEqual(nc1, nc2)
        self.assertEqual(nc1, nc4)
        self.assertTrue(nc3 == nc1 + 1)

    def test_popitem(self):
        k, v = self.f.popitem()
        self.assertIn(k, self.d)
        self.assertIn(v, self.d.values())
        self.assertNotIn(k, self.f)
        self.assertEqual(len(self.d) - 1, len(self.f))

    def test_pop(self):
        k = 'w'
        v = self.f.pop(k)
        self.assertEqual(v, self.d[k])
        self.assertNotIn(k, self.f)
        self.assertNotIn(v, self.f.values())
        self.assertEqual(len(self.d) - 1, len(self.f))

    def test_get(self):
        self.assertEqual(self.f.get('NotHere'), None)
        self.assertEqual(self.f.get('NotHere', 'Default'), 'Default')
        self.assertEqual(self.f.get('q', 'Default'), self.d['q'])
        return

    def test_setdefault(self):
        self.assertEqual(self.f.setdefault('new', 'dog'), 'dog')
        self.assertEqual(self.f.setdefault('r', 'cat'), self.d['r'])

    def test_update(self):
        new = dict(y='life', u='of', i='brian')
        self.f.update(new)
        self.d.update(new)
        for k, v in self.d.iteritems():
            self.assertEqual(self.f[k], v)

    def test_keyordering(self):
        if self.openmethod[0] is not bsddb.btopen:
            return
        keys = self.d.keys()
        keys.sort()
        self.assertEqual(self.f.first()[0], keys[0])
        self.assertEqual(self.f.next()[0], keys[1])
        self.assertEqual(self.f.last()[0], keys[-1])
        self.assertEqual(self.f.previous()[0], keys[-2])
        self.assertEqual(list(self.f), keys)


class TestBTree(TestBSDDB):
    fname = test_support.TESTFN
    openmethod = [bsddb.btopen]


class TestBTree_InMemory(TestBSDDB):
    fname = None
    openmethod = [bsddb.btopen]


class TestBTree_InMemory_Truncate(TestBSDDB):
    fname = None
    openflag = 'n'
    openmethod = [bsddb.btopen]


class TestHashTable(TestBSDDB):
    fname = test_support.TESTFN
    openmethod = [bsddb.hashopen]


class TestHashTable_InMemory(TestBSDDB):
    fname = None
    openmethod = [bsddb.hashopen]


def test_main(verbose = None):
    test_support.run_unittest(TestBTree, TestHashTable, TestBTree_InMemory, TestHashTable_InMemory, TestBTree_InMemory_Truncate)


if __name__ == '__main__':
    test_main(verbose=True)