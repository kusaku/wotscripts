# Embedded file name: scripts/common/Lib/bsddb/test/test_compat.py
"""
Test cases adapted from the test_bsddb.py module in Python's
regression test suite.
"""
import os, string
import unittest
from test_all import db, hashopen, btopen, rnopen, verbose, get_new_database_path

class CompatibilityTestCase(unittest.TestCase):

    def setUp(self):
        self.filename = get_new_database_path()

    def tearDown(self):
        try:
            os.remove(self.filename)
        except os.error:
            pass

    def test01_btopen(self):
        self.do_bthash_test(btopen, 'btopen')

    def test02_hashopen(self):
        self.do_bthash_test(hashopen, 'hashopen')

    def test03_rnopen(self):
        data = 'The quick brown fox jumped over the lazy dog.'.split()
        if verbose:
            print '\nTesting: rnopen'
        f = rnopen(self.filename, 'c')
        for x in range(len(data)):
            f[x + 1] = data[x]

        getTest = (f[1], f[2], f[3])
        if verbose:
            print '%s %s %s' % getTest
        self.assertEqual(getTest[1], 'quick', 'data mismatch!')
        rv = f.set_location(3)
        if rv != (3, 'brown'):
            self.fail('recno database set_location failed: ' + repr(rv))
        f[25] = 'twenty-five'
        f.close()
        del f
        f = rnopen(self.filename, 'w')
        f[20] = 'twenty'

        def noRec(f):
            rec = f[15]

        self.assertRaises(KeyError, noRec, f)

        def badKey(f):
            rec = f['a string']

        self.assertRaises(TypeError, badKey, f)
        del f[3]
        rec = f.first()
        while rec:
            if verbose:
                print rec
            try:
                rec = f.next()
            except KeyError:
                break

        f.close()

    def test04_n_flag(self):
        f = hashopen(self.filename, 'n')
        f.close()

    def do_bthash_test--- This code section failed: ---

0	LOAD_GLOBAL       'verbose'
3	POP_JUMP_IF_FALSE '18'

6	LOAD_CONST        '\nTesting: '
9	PRINT_ITEM        None
10	LOAD_FAST         'what'
13	PRINT_ITEM_CONT   None
14	PRINT_NEWLINE_CONT None
15	JUMP_FORWARD      '18'
18_0	COME_FROM         '15'

18	LOAD_FAST         'factory'
21	LOAD_FAST         'self'
24	LOAD_ATTR         'filename'
27	LOAD_CONST        'c'
30	CALL_FUNCTION_2   None
33	STORE_FAST        'f'

36	LOAD_GLOBAL       'verbose'
39	POP_JUMP_IF_FALSE '50'

42	LOAD_CONST        'creation...'
45	PRINT_ITEM        None
46	PRINT_NEWLINE_CONT None
47	JUMP_FORWARD      '50'
50_0	COME_FROM         '47'

50	LOAD_FAST         'f'
53	POP_JUMP_IF_FALSE '73'

56	LOAD_GLOBAL       'verbose'
59	POP_JUMP_IF_FALSE '87'
62	LOAD_CONST        'truth test: true'
65	PRINT_ITEM        None
66	PRINT_NEWLINE_CONT None
67	JUMP_ABSOLUTE     '87'
70	JUMP_FORWARD      '87'

73	LOAD_GLOBAL       'verbose'
76	POP_JUMP_IF_FALSE '87'
79	LOAD_CONST        'truth test: false'
82	PRINT_ITEM        None
83	PRINT_NEWLINE_CONT None
84	JUMP_FORWARD      '87'
87_0	COME_FROM         '70'
87_1	COME_FROM         '84'

87	LOAD_CONST        ''
90	LOAD_FAST         'f'
93	LOAD_CONST        '0'
96	STORE_SUBSCR      None

97	LOAD_CONST        'Guido'
100	LOAD_FAST         'f'
103	LOAD_CONST        'a'
106	STORE_SUBSCR      None

107	LOAD_CONST        'van'
110	LOAD_FAST         'f'
113	LOAD_CONST        'b'
116	STORE_SUBSCR      None

117	LOAD_CONST        'Rossum'
120	LOAD_FAST         'f'
123	LOAD_CONST        'c'
126	STORE_SUBSCR      None

127	LOAD_CONST        'invented'
130	LOAD_FAST         'f'
133	LOAD_CONST        'd'
136	STORE_SUBSCR      None

137	LOAD_CONST        'Python'
140	LOAD_FAST         'f'
143	LOAD_CONST        'f'
146	STORE_SUBSCR      None

147	LOAD_GLOBAL       'verbose'
150	POP_JUMP_IF_FALSE '186'

153	LOAD_CONST        '%s %s %s'
156	LOAD_FAST         'f'
159	LOAD_CONST        'a'
162	BINARY_SUBSCR     None
163	LOAD_FAST         'f'
166	LOAD_CONST        'b'
169	BINARY_SUBSCR     None
170	LOAD_FAST         'f'
173	LOAD_CONST        'c'
176	BINARY_SUBSCR     None
177	BUILD_TUPLE_3     None
180	BINARY_MODULO     None
181	PRINT_ITEM        None
182	PRINT_NEWLINE_CONT None
183	JUMP_FORWARD      '186'
186_0	COME_FROM         '183'

186	LOAD_GLOBAL       'verbose'
189	POP_JUMP_IF_FALSE '200'

192	LOAD_CONST        'key ordering...'
195	PRINT_ITEM        None
196	PRINT_NEWLINE_CONT None
197	JUMP_FORWARD      '200'
200_0	COME_FROM         '197'

200	LOAD_FAST         'f'
203	LOAD_ATTR         'set_location'
206	LOAD_FAST         'f'
209	LOAD_ATTR         'first'
212	CALL_FUNCTION_0   None
215	LOAD_CONST        0
218	BINARY_SUBSCR     None
219	CALL_FUNCTION_1   None
222	STORE_FAST        'start'

225	LOAD_FAST         'start'
228	LOAD_CONST        ('0', '')
231	COMPARE_OP        '!='
234	POP_JUMP_IF_FALSE '263'

237	LOAD_FAST         'self'
240	LOAD_ATTR         'fail'
243	LOAD_CONST        'incorrect first() result: '
246	LOAD_GLOBAL       'repr'
249	LOAD_FAST         'start'
252	CALL_FUNCTION_1   None
255	BINARY_ADD        None
256	CALL_FUNCTION_1   None
259	POP_TOP           None
260	JUMP_FORWARD      '263'
263_0	COME_FROM         '260'

263	SETUP_LOOP        '356'

266	SETUP_EXCEPT      '285'

269	LOAD_FAST         'f'
272	LOAD_ATTR         'next'
275	CALL_FUNCTION_0   None
278	STORE_FAST        'rec'
281	POP_BLOCK         None
282	JUMP_FORWARD      '338'
285_0	COME_FROM         '266'

285	DUP_TOP           None
286	LOAD_GLOBAL       'KeyError'
289	COMPARE_OP        'exception match'
292	POP_JUMP_IF_FALSE '337'
295	POP_TOP           None
296	POP_TOP           None
297	POP_TOP           None

298	LOAD_FAST         'self'
301	LOAD_ATTR         'assertEqual'
304	LOAD_FAST         'rec'
307	LOAD_FAST         'f'
310	LOAD_ATTR         'last'
313	CALL_FUNCTION_0   None
316	LOAD_CONST        'Error, last <> last!'
319	CALL_FUNCTION_3   None
322	POP_TOP           None

323	LOAD_FAST         'f'
326	LOAD_ATTR         'previous'
329	CALL_FUNCTION_0   None
332	POP_TOP           None

333	BREAK_LOOP        None
334	JUMP_FORWARD      '338'
337	END_FINALLY       None
338_0	COME_FROM         '282'
338_1	COME_FROM         '337'

338	LOAD_GLOBAL       'verbose'
341	POP_JUMP_IF_FALSE '266'

344	LOAD_FAST         'rec'
347	PRINT_ITEM        None
348	PRINT_NEWLINE_CONT None
349	JUMP_BACK         '266'
352	JUMP_BACK         '266'
355	POP_BLOCK         None
356_0	COME_FROM         '263'

356	LOAD_FAST         'self'
359	LOAD_ATTR         'assertTrue'
362	LOAD_FAST         'f'
365	LOAD_ATTR         'has_key'
368	LOAD_CONST        'f'
371	CALL_FUNCTION_1   None
374	LOAD_CONST        'Error, missing key!'
377	CALL_FUNCTION_2   None
380	POP_TOP           None

381	LOAD_FAST         'factory'
384	LOAD_GLOBAL       'btopen'
387	COMPARE_OP        '=='
390	POP_JUMP_IF_FALSE '449'

393	LOAD_FAST         'f'
396	LOAD_ATTR         'set_location'
399	LOAD_CONST        'e'
402	CALL_FUNCTION_1   None
405	STORE_FAST        'e'

408	LOAD_FAST         'e'
411	LOAD_CONST        ('f', 'Python')
414	COMPARE_OP        '!='
417	POP_JUMP_IF_FALSE '501'

420	LOAD_FAST         'self'
423	LOAD_ATTR         'fail'
426	LOAD_CONST        'wrong key,value returned: '
429	LOAD_GLOBAL       'repr'
432	LOAD_FAST         'e'
435	CALL_FUNCTION_1   None
438	BINARY_ADD        None
439	CALL_FUNCTION_1   None
442	POP_TOP           None
443	JUMP_ABSOLUTE     '501'
446	JUMP_FORWARD      '501'

449	SETUP_EXCEPT      '471'

452	LOAD_FAST         'f'
455	LOAD_ATTR         'set_location'
458	LOAD_CONST        'e'
461	CALL_FUNCTION_1   None
464	STORE_FAST        'e'
467	POP_BLOCK         None
468	JUMP_FORWARD      '488'
471_0	COME_FROM         '449'

471	DUP_TOP           None
472	LOAD_GLOBAL       'KeyError'
475	COMPARE_OP        'exception match'
478	POP_JUMP_IF_FALSE '487'
481	POP_TOP           None
482	POP_TOP           None
483	POP_TOP           None

484	JUMP_FORWARD      '501'
487	END_FINALLY       None
488_0	COME_FROM         '468'

488	LOAD_FAST         'self'
491	LOAD_ATTR         'fail'
494	LOAD_CONST        'set_location on non-existent key did not raise KeyError'
497	CALL_FUNCTION_1   None
500	POP_TOP           None
501_0	COME_FROM         '446'
501_1	COME_FROM         '487'

501	LOAD_FAST         'f'
504	LOAD_ATTR         'sync'
507	CALL_FUNCTION_0   None
510	POP_TOP           None

511	LOAD_FAST         'f'
514	LOAD_ATTR         'close'
517	CALL_FUNCTION_0   None
520	POP_TOP           None

521	SETUP_EXCEPT      '565'

524	LOAD_FAST         'f'
527	POP_JUMP_IF_FALSE '547'

530	LOAD_GLOBAL       'verbose'
533	POP_JUMP_IF_FALSE '561'
536	LOAD_CONST        'truth test: true'
539	PRINT_ITEM        None
540	PRINT_NEWLINE_CONT None
541	JUMP_ABSOLUTE     '561'
544	JUMP_FORWARD      '561'

547	LOAD_GLOBAL       'verbose'
550	POP_JUMP_IF_FALSE '561'
553	LOAD_CONST        'truth test: false'
556	PRINT_ITEM        None
557	PRINT_NEWLINE_CONT None
558	JUMP_FORWARD      '561'
561_0	COME_FROM         '544'
561_1	COME_FROM         '558'
561	POP_BLOCK         None
562	JUMP_FORWARD      '585'
565_0	COME_FROM         '521'

565	DUP_TOP           None
566	LOAD_GLOBAL       'db'
569	LOAD_ATTR         'DBError'
572	COMPARE_OP        'exception match'
575	POP_JUMP_IF_FALSE '584'
578	POP_TOP           None
579	POP_TOP           None
580	POP_TOP           None

581	JUMP_FORWARD      '598'
584	END_FINALLY       None
585_0	COME_FROM         '562'

585	LOAD_FAST         'self'
588	LOAD_ATTR         'fail'
591	LOAD_CONST        'Exception expected'
594	CALL_FUNCTION_1   None
597	POP_TOP           None
598_0	COME_FROM         '584'

598	DELETE_FAST       'f'

601	LOAD_GLOBAL       'verbose'
604	POP_JUMP_IF_FALSE '615'

607	LOAD_CONST        'modification...'
610	PRINT_ITEM        None
611	PRINT_NEWLINE_CONT None
612	JUMP_FORWARD      '615'
615_0	COME_FROM         '612'

615	LOAD_FAST         'factory'
618	LOAD_FAST         'self'
621	LOAD_ATTR         'filename'
624	LOAD_CONST        'w'
627	CALL_FUNCTION_2   None
630	STORE_FAST        'f'

633	LOAD_CONST        'discovered'
636	LOAD_FAST         'f'
639	LOAD_CONST        'd'
642	STORE_SUBSCR      None

643	LOAD_GLOBAL       'verbose'
646	POP_JUMP_IF_FALSE '657'

649	LOAD_CONST        'access...'
652	PRINT_ITEM        None
653	PRINT_NEWLINE_CONT None
654	JUMP_FORWARD      '657'
657_0	COME_FROM         '654'

657	SETUP_LOOP        '704'
660	LOAD_FAST         'f'
663	LOAD_ATTR         'keys'
666	CALL_FUNCTION_0   None
669	GET_ITER          None
670	FOR_ITER          '703'
673	STORE_FAST        'key'

676	LOAD_FAST         'f'
679	LOAD_FAST         'key'
682	BINARY_SUBSCR     None
683	STORE_FAST        'word'

686	LOAD_GLOBAL       'verbose'
689	POP_JUMP_IF_FALSE '670'

692	LOAD_FAST         'word'
695	PRINT_ITEM        None
696	PRINT_NEWLINE_CONT None
697	JUMP_BACK         '670'
700	JUMP_BACK         '670'
703	POP_BLOCK         None
704_0	COME_FROM         '657'

704	LOAD_CONST        '<code_object noRec>'
707	MAKE_FUNCTION_0   None
710	STORE_FAST        'noRec'

713	LOAD_FAST         'self'
716	LOAD_ATTR         'assertRaises'
719	LOAD_GLOBAL       'KeyError'
722	LOAD_FAST         'noRec'
725	LOAD_FAST         'f'
728	CALL_FUNCTION_3   None
731	POP_TOP           None

732	LOAD_CONST        '<code_object badKey>'
735	MAKE_FUNCTION_0   None
738	STORE_FAST        'badKey'

741	LOAD_FAST         'self'
744	LOAD_ATTR         'assertRaises'
747	LOAD_GLOBAL       'TypeError'
750	LOAD_FAST         'badKey'
753	LOAD_FAST         'f'
756	CALL_FUNCTION_3   None
759	POP_TOP           None

760	LOAD_FAST         'f'
763	LOAD_ATTR         'close'
766	CALL_FUNCTION_0   None
769	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 355


def test_suite():
    return unittest.makeSuite(CompatibilityTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')