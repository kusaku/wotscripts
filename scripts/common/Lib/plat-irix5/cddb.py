# Embedded file name: scripts/common/Lib/plat-irix5/cddb.py
from warnings import warnpy3k
warnpy3k('the cddb module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
import string, posix, os
_cddbrc = '.cddb'
_DB_ID_NTRACKS = 5
_dbid_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@_=+abcdefghijklmnopqrstuvwxyz'

def _dbid(v):
    if v >= len(_dbid_map):
        return string.zfill(v, 2)
    else:
        return _dbid_map[v]


def tochash(toc):
    if type(toc) == type(''):
        tracklist = []
        for i in range(2, len(toc), 4):
            tracklist.append((None, (int(toc[i:i + 2]), int(toc[i + 2:i + 4]))))

    else:
        tracklist = toc
    ntracks = len(tracklist)
    hash = _dbid(ntracks >> 4 & 15) + _dbid(ntracks & 15)
    if ntracks <= _DB_ID_NTRACKS:
        nidtracks = ntracks
    else:
        nidtracks = _DB_ID_NTRACKS - 1
        min = 0
        sec = 0
        for track in tracklist:
            start, length = track
            min = min + length[0]
            sec = sec + length[1]

        min = min + sec / 60
        sec = sec % 60
        hash = hash + _dbid(min) + _dbid(sec)
    for i in range(nidtracks):
        start, length = tracklist[i]
        hash = hash + _dbid(length[0]) + _dbid(length[1])

    return hash


class Cddb:

    def __init__--- This code section failed: ---

0	LOAD_GLOBAL       'os'
3	LOAD_ATTR         'environ'
6	LOAD_ATTR         'has_key'
9	LOAD_CONST        'CDDB_PATH'
12	CALL_FUNCTION_1   None
15	POP_JUMP_IF_FALSE '49'

18	LOAD_GLOBAL       'os'
21	LOAD_ATTR         'environ'
24	LOAD_CONST        'CDDB_PATH'
27	BINARY_SUBSCR     None
28	STORE_FAST        'path'

31	LOAD_FAST         'path'
34	LOAD_ATTR         'split'
37	LOAD_CONST        ','
40	CALL_FUNCTION_1   None
43	STORE_FAST        'cddb_path'
46	JUMP_FORWARD      '79'

49	LOAD_GLOBAL       'os'
52	LOAD_ATTR         'environ'
55	LOAD_CONST        'HOME'
58	BINARY_SUBSCR     None
59	STORE_FAST        'home'

62	LOAD_FAST         'home'
65	LOAD_CONST        '/'
68	BINARY_ADD        None
69	LOAD_GLOBAL       '_cddbrc'
72	BINARY_ADD        None
73	BUILD_LIST_1      None
76	STORE_FAST        'cddb_path'
79_0	COME_FROM         '46'

79	LOAD_FAST         'self'
82	LOAD_ATTR         '_get_id'
85	LOAD_FAST         'tracklist'
88	CALL_FUNCTION_1   None
91	POP_TOP           None

92	SETUP_LOOP        '179'
95	LOAD_FAST         'cddb_path'
98	GET_ITER          None
99	FOR_ITER          '178'
102	STORE_FAST        'dir'

105	LOAD_FAST         'dir'
108	LOAD_CONST        '/'
111	BINARY_ADD        None
112	LOAD_FAST         'self'
115	LOAD_ATTR         'id'
118	BINARY_ADD        None
119	LOAD_CONST        '.rdb'
122	BINARY_ADD        None
123	STORE_FAST        'file'

126	SETUP_EXCEPT      '158'

129	LOAD_GLOBAL       'open'
132	LOAD_FAST         'file'
135	LOAD_CONST        'r'
138	CALL_FUNCTION_2   None
141	STORE_FAST        'f'

144	LOAD_FAST         'file'
147	LOAD_FAST         'self'
150	STORE_ATTR        'file'

153	BREAK_LOOP        None
154	POP_BLOCK         None
155	JUMP_BACK         '99'
158_0	COME_FROM         '126'

158	DUP_TOP           None
159	LOAD_GLOBAL       'IOError'
162	COMPARE_OP        'exception match'
165	POP_JUMP_IF_FALSE '174'
168	POP_TOP           None
169	POP_TOP           None
170	POP_TOP           None

171	JUMP_BACK         '99'
174	END_FINALLY       None
175_0	COME_FROM         '174'
175	JUMP_BACK         '99'
178	POP_BLOCK         None
179_0	COME_FROM         '92'

179	LOAD_GLOBAL       'int'
182	LOAD_FAST         'self'
185	LOAD_ATTR         'id'
188	LOAD_CONST        2
191	SLICE+2           None
192	LOAD_CONST        16
195	CALL_FUNCTION_2   None
198	STORE_FAST        'ntracks'

201	LOAD_CONST        ''
204	LOAD_FAST         'self'
207	STORE_ATTR        'artist'

210	LOAD_CONST        ''
213	LOAD_FAST         'self'
216	STORE_ATTR        'title'

219	LOAD_CONST        None
222	BUILD_LIST_1      None
225	LOAD_CONST        ''
228	BUILD_LIST_1      None
231	LOAD_FAST         'ntracks'
234	BINARY_MULTIPLY   None
235	BINARY_ADD        None
236	LOAD_FAST         'self'
239	STORE_ATTR        'track'

242	LOAD_CONST        None
245	BUILD_LIST_1      None
248	LOAD_CONST        ''
251	BUILD_LIST_1      None
254	LOAD_FAST         'ntracks'
257	BINARY_MULTIPLY   None
258	BINARY_ADD        None
259	LOAD_FAST         'self'
262	STORE_ATTR        'trackartist'

265	BUILD_LIST_0      None
268	LOAD_FAST         'self'
271	STORE_ATTR        'notes'

274	LOAD_GLOBAL       'hasattr'
277	LOAD_FAST         'self'
280	LOAD_CONST        'file'
283	CALL_FUNCTION_2   None
286	POP_JUMP_IF_TRUE  '293'

289	LOAD_CONST        None
292	RETURN_END_IF     None

293	LOAD_CONST        -1
296	LOAD_CONST        None
299	IMPORT_NAME       're'
302	STORE_FAST        're'

305	LOAD_FAST         're'
308	LOAD_ATTR         'compile'
311	LOAD_CONST        '^([^.]*)\\.([^:]*):[\\t ]+(.*)'
314	CALL_FUNCTION_1   None
317	STORE_FAST        'reg'

320	SETUP_LOOP        '731'

323	LOAD_FAST         'f'
326	LOAD_ATTR         'readline'
329	CALL_FUNCTION_0   None
332	STORE_FAST        'line'

335	LOAD_FAST         'line'
338	POP_JUMP_IF_TRUE  '345'

341	BREAK_LOOP        None
342	JUMP_FORWARD      '345'
345_0	COME_FROM         '342'

345	LOAD_FAST         'reg'
348	LOAD_ATTR         'match'
351	LOAD_FAST         'line'
354	CALL_FUNCTION_1   None
357	STORE_FAST        'match'

360	LOAD_FAST         'match'
363	POP_JUMP_IF_TRUE  '381'

366	LOAD_CONST        'syntax error in '
369	LOAD_FAST         'file'
372	BINARY_ADD        None
373	PRINT_ITEM        None
374	PRINT_NEWLINE_CONT None

375	CONTINUE          '323'
378	JUMP_FORWARD      '381'
381_0	COME_FROM         '378'

381	LOAD_FAST         'match'
384	LOAD_ATTR         'group'
387	LOAD_CONST        1
390	LOAD_CONST        2
393	LOAD_CONST        3
396	CALL_FUNCTION_3   None
399	UNPACK_SEQUENCE_3 None
402	STORE_FAST        'name1'
405	STORE_FAST        'name2'
408	STORE_FAST        'value'

411	LOAD_FAST         'name1'
414	LOAD_CONST        'album'
417	COMPARE_OP        '=='
420	POP_JUMP_IF_FALSE '564'

423	LOAD_FAST         'name2'
426	LOAD_CONST        'artist'
429	COMPARE_OP        '=='
432	POP_JUMP_IF_FALSE '447'

435	LOAD_FAST         'value'
438	LOAD_FAST         'self'
441	STORE_ATTR        'artist'
444	JUMP_ABSOLUTE     '727'

447	LOAD_FAST         'name2'
450	LOAD_CONST        'title'
453	COMPARE_OP        '=='
456	POP_JUMP_IF_FALSE '471'

459	LOAD_FAST         'value'
462	LOAD_FAST         'self'
465	STORE_ATTR        'title'
468	JUMP_ABSOLUTE     '727'

471	LOAD_FAST         'name2'
474	LOAD_CONST        'toc'
477	COMPARE_OP        '=='
480	POP_JUMP_IF_FALSE '530'

483	LOAD_FAST         'self'
486	LOAD_ATTR         'toc'
489	POP_JUMP_IF_TRUE  '504'

492	LOAD_FAST         'value'
495	LOAD_FAST         'self'
498	STORE_ATTR        'toc'
501	JUMP_FORWARD      '504'
504_0	COME_FROM         '501'

504	LOAD_FAST         'self'
507	LOAD_ATTR         'toc'
510	LOAD_FAST         'value'
513	COMPARE_OP        '!='
516	POP_JUMP_IF_FALSE '561'

519	LOAD_CONST        "toc's don't match"
522	PRINT_ITEM        None
523	PRINT_NEWLINE_CONT None
524	JUMP_ABSOLUTE     '561'
527	JUMP_ABSOLUTE     '727'

530	LOAD_FAST         'name2'
533	LOAD_CONST        'notes'
536	COMPARE_OP        '=='
539	POP_JUMP_IF_FALSE '727'

542	LOAD_FAST         'self'
545	LOAD_ATTR         'notes'
548	LOAD_ATTR         'append'
551	LOAD_FAST         'value'
554	CALL_FUNCTION_1   None
557	POP_TOP           None
558	JUMP_ABSOLUTE     '727'
561	JUMP_BACK         '323'

564	LOAD_FAST         'name1'
567	LOAD_CONST        5
570	SLICE+2           None
571	LOAD_CONST        'track'
574	COMPARE_OP        '=='
577	POP_JUMP_IF_FALSE '323'

580	SETUP_EXCEPT      '603'

583	LOAD_GLOBAL       'int'
586	LOAD_FAST         'name1'
589	LOAD_CONST        5
592	SLICE+1           None
593	CALL_FUNCTION_1   None
596	STORE_FAST        'trackno'
599	POP_BLOCK         None
600	JUMP_FORWARD      '635'
603_0	COME_FROM         '580'

603	DUP_TOP           None
604	LOAD_GLOBAL       'strings'
607	LOAD_ATTR         'atoi_error'
610	COMPARE_OP        'exception match'
613	POP_JUMP_IF_FALSE '634'
616	POP_TOP           None
617	POP_TOP           None
618	POP_TOP           None

619	LOAD_CONST        'syntax error in '
622	LOAD_FAST         'file'
625	BINARY_ADD        None
626	PRINT_ITEM        None
627	PRINT_NEWLINE_CONT None

628	CONTINUE          '323'
631	JUMP_FORWARD      '635'
634	END_FINALLY       None
635_0	COME_FROM         '600'
635_1	COME_FROM         '634'

635	LOAD_FAST         'trackno'
638	LOAD_FAST         'ntracks'
641	COMPARE_OP        '>'
644	POP_JUMP_IF_FALSE '668'

647	LOAD_CONST        'track number %r in file %r out of range'
650	LOAD_FAST         'trackno'
653	LOAD_FAST         'file'
656	BUILD_TUPLE_2     None
659	BINARY_MODULO     None
660	PRINT_ITEM        None
661	PRINT_NEWLINE_CONT None

662	CONTINUE          '323'
665	JUMP_FORWARD      '668'
668_0	COME_FROM         '665'

668	LOAD_FAST         'name2'
671	LOAD_CONST        'title'
674	COMPARE_OP        '=='
677	POP_JUMP_IF_FALSE '696'

680	LOAD_FAST         'value'
683	LOAD_FAST         'self'
686	LOAD_ATTR         'track'
689	LOAD_FAST         'trackno'
692	STORE_SUBSCR      None
693	JUMP_ABSOLUTE     '727'

696	LOAD_FAST         'name2'
699	LOAD_CONST        'artist'
702	COMPARE_OP        '=='
705	POP_JUMP_IF_FALSE '727'

708	LOAD_FAST         'value'
711	LOAD_FAST         'self'
714	LOAD_ATTR         'trackartist'
717	LOAD_FAST         'trackno'
720	STORE_SUBSCR      None
721	JUMP_ABSOLUTE     '727'
724	JUMP_BACK         '323'
727	JUMP_BACK         '323'
730	POP_BLOCK         None
731_0	COME_FROM         '320'

731	LOAD_FAST         'f'
734	LOAD_ATTR         'close'
737	CALL_FUNCTION_0   None
740	POP_TOP           None

741	SETUP_LOOP        '896'
744	LOAD_GLOBAL       'range'
747	LOAD_CONST        2
750	LOAD_GLOBAL       'len'
753	LOAD_FAST         'self'
756	LOAD_ATTR         'track'
759	CALL_FUNCTION_1   None
762	CALL_FUNCTION_2   None
765	GET_ITER          None
766	FOR_ITER          '895'
769	STORE_FAST        'i'

772	LOAD_FAST         'self'
775	LOAD_ATTR         'track'
778	LOAD_FAST         'i'
781	BINARY_SUBSCR     None
782	STORE_FAST        'track'

785	LOAD_FAST         'track'
788	POP_JUMP_IF_FALSE '766'
791	LOAD_FAST         'track'
794	LOAD_CONST        0
797	BINARY_SUBSCR     None
798	LOAD_CONST        ','
801	COMPARE_OP        '=='
804_0	COME_FROM         '788'
804	POP_JUMP_IF_FALSE '766'

807	SETUP_EXCEPT      '840'

810	LOAD_FAST         'self'
813	LOAD_ATTR         'track'
816	LOAD_FAST         'i'
819	LOAD_CONST        1
822	BINARY_SUBTRACT   None
823	BINARY_SUBSCR     None
824	LOAD_ATTR         'index'
827	LOAD_CONST        ','
830	CALL_FUNCTION_1   None
833	STORE_FAST        'off'
836	POP_BLOCK         None
837	JUMP_FORWARD      '857'
840_0	COME_FROM         '807'

840	DUP_TOP           None
841	LOAD_GLOBAL       'ValueError'
844	COMPARE_OP        'exception match'
847	POP_JUMP_IF_FALSE '856'
850	POP_TOP           None
851	POP_TOP           None
852	POP_TOP           None

853	JUMP_ABSOLUTE     '892'
856	END_FINALLY       None
857_0	COME_FROM         '837'

857	LOAD_FAST         'self'
860	LOAD_ATTR         'track'
863	LOAD_FAST         'i'
866	LOAD_CONST        1
869	BINARY_SUBTRACT   None
870	BINARY_SUBSCR     None
871	LOAD_FAST         'off'
874	SLICE+2           None

875	LOAD_FAST         'track'
878	BINARY_ADD        None
879	LOAD_FAST         'self'
882	LOAD_ATTR         'track'
885	LOAD_FAST         'i'
888	STORE_SUBSCR      None
889_0	COME_FROM         '856'
889	JUMP_BACK         '766'
892	JUMP_BACK         '766'
895	POP_BLOCK         None
896_0	COME_FROM         '741'
896	LOAD_CONST        None
899	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 730

    def _get_id(self, tracklist):
        if type(tracklist) == type(''):
            if tracklist[-4:] == '.rdb':
                self.id = tracklist[:-4]
                self.toc = ''
                return
            t = []
            for i in range(2, len(tracklist), 4):
                t.append((None, (int(tracklist[i:i + 2]), int(tracklist[i + 2:i + 4]))))

            tracklist = t
        ntracks = len(tracklist)
        self.id = _dbid(ntracks >> 4 & 15) + _dbid(ntracks & 15)
        if ntracks <= _DB_ID_NTRACKS:
            nidtracks = ntracks
        else:
            nidtracks = _DB_ID_NTRACKS - 1
            min = 0
            sec = 0
            for track in tracklist:
                start, length = track
                min = min + length[0]
                sec = sec + length[1]

            min = min + sec / 60
            sec = sec % 60
            self.id = self.id + _dbid(min) + _dbid(sec)
        for i in range(nidtracks):
            start, length = tracklist[i]
            self.id = self.id + _dbid(length[0]) + _dbid(length[1])

        self.toc = string.zfill(ntracks, 2)
        for track in tracklist:
            start, length = track
            self.toc = self.toc + string.zfill(length[0], 2) + string.zfill(length[1], 2)

        return

    def write(self):
        import posixpath
        if os.environ.has_key('CDDB_WRITE_DIR'):
            dir = os.environ['CDDB_WRITE_DIR']
        else:
            dir = os.environ['HOME'] + '/' + _cddbrc
        file = dir + '/' + self.id + '.rdb'
        if posixpath.exists(file):
            posix.rename(file, file + '~')
        f = open(file, 'w')
        f.write('album.title:\t' + self.title + '\n')
        f.write('album.artist:\t' + self.artist + '\n')
        f.write('album.toc:\t' + self.toc + '\n')
        for note in self.notes:
            f.write('album.notes:\t' + note + '\n')

        prevpref = None
        for i in range(1, len(self.track)):
            if self.trackartist[i]:
                f.write('track%r.artist:\t%s\n' % (i, self.trackartist[i]))
            track = self.track[i]
            try:
                off = track.index(',')
            except ValuError:
                prevpref = None
            else:
                if prevpref and track[:off] == prevpref:
                    track = track[off:]
                else:
                    prevpref = track[:off]

            f.write('track%r.title:\t%s\n' % (i, track))

        f.close()
        return