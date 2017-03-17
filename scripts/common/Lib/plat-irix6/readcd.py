# Embedded file name: scripts/common/Lib/plat-irix6/readcd.py
from warnings import warnpy3k
warnpy3k('the readcd module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
import cd, CD

class Error(Exception):
    pass


class _Stop(Exception):
    pass


def _doatime(self, cb_type, data):
    if (data[0] * 60 + data[1]) * 75 + data[2] > self.end:
        raise _Stop
    func, arg = self.callbacks[cb_type]
    if func:
        func(arg, cb_type, data)


def _dopnum(self, cb_type, data):
    if data > self.end:
        raise _Stop
    func, arg = self.callbacks[cb_type]
    if func:
        func(arg, cb_type, data)


class Readcd:

    def __init__(self, *arg):
        if len(arg) == 0:
            self.player = cd.open()
        elif len(arg) == 1:
            self.player = cd.open(arg[0])
        elif len(arg) == 2:
            self.player = cd.open(arg[0], arg[1])
        else:
            raise Error, 'bad __init__ call'
        self.list = []
        self.callbacks = [(None, None)] * 8
        self.parser = cd.createparser()
        self.playing = 0
        self.end = 0
        self.status = None
        self.trackinfo = None
        return

    def eject(self):
        self.player.eject()
        self.list = []
        self.end = 0
        self.listindex = 0
        self.status = None
        self.trackinfo = None
        if self.playing:
            raise _Stop
        return

    def pmsf2msf(self, track, min, sec, frame):
        if not self.status:
            self.cachestatus()
        if track < self.status[5] or track > self.status[6]:
            raise Error, 'track number out of range'
        if not self.trackinfo:
            self.cacheinfo()
        start, total = self.trackinfo[track]
        start = (start[0] * 60 + start[1]) * 75 + start[2]
        total = (total[0] * 60 + total[1]) * 75 + total[2]
        block = (min * 60 + sec) * 75 + frame
        if block > total:
            raise Error, 'out of range'
        block = start + block
        min, block = divmod(block, 4500)
        sec, frame = divmod(block, 75)
        return (min, sec, frame)

    def reset(self):
        self.list = []

    def appendtrack(self, track):
        self.appendstretch(track, track)

    def appendstretch(self, start, end):
        if not self.status:
            self.cachestatus()
        if not start:
            start = 1
        if not end:
            end = self.status[6]
        if type(end) == type(0):
            if end < self.status[5] or end > self.status[6]:
                raise Error, 'range error'
        else:
            l = len(end)
            if l == 4:
                prog, min, sec, frame = end
                if prog < self.status[5] or prog > self.status[6]:
                    raise Error, 'range error'
                end = self.pmsf2msf(prog, min, sec, frame)
            elif l != 3:
                raise Error, 'syntax error'
        if type(start) == type(0):
            if start < self.status[5] or start > self.status[6]:
                raise Error, 'range error'
            if len(self.list) > 0:
                s, e = self.list[-1]
                if type(e) == type(0):
                    if start == e + 1:
                        start = s
                        del self.list[-1]
        else:
            l = len(start)
            if l == 4:
                prog, min, sec, frame = start
                if prog < self.status[5] or prog > self.status[6]:
                    raise Error, 'range error'
                start = self.pmsf2msf(prog, min, sec, frame)
            elif l != 3:
                raise Error, 'syntax error'
        self.list.append((start, end))

    def settracks(self, list):
        self.list = []
        for track in list:
            self.appendtrack(track)

    def setcallback(self, cb_type, func, arg):
        if cb_type < 0 or cb_type >= 8:
            raise Error, 'type out of range'
        self.callbacks[cb_type] = (func, arg)
        if self.playing:
            start, end = self.list[self.listindex]
            if type(end) == type(0):
                if cb_type != CD.PNUM:
                    self.parser.setcallback(cb_type, func, arg)
            elif cb_type != CD.ATIME:
                self.parser.setcallback(cb_type, func, arg)

    def removecallback(self, cb_type):
        if cb_type < 0 or cb_type >= 8:
            raise Error, 'type out of range'
        self.callbacks[cb_type] = (None, None)
        if self.playing:
            start, end = self.list[self.listindex]
            if type(end) == type(0):
                if cb_type != CD.PNUM:
                    self.parser.removecallback(cb_type)
            elif cb_type != CD.ATIME:
                self.parser.removecallback(cb_type)
        return None

    def gettrackinfo(self, *arg):
        if not self.status:
            self.cachestatus()
        if not self.trackinfo:
            self.cacheinfo()
        if len(arg) == 0:
            return self.trackinfo[self.status[5]:self.status[6] + 1]
        result = []
        for i in arg:
            if i < self.status[5] or i > self.status[6]:
                raise Error, 'range error'
            result.append(self.trackinfo[i])

        return result

    def cacheinfo(self):
        if not self.status:
            self.cachestatus()
        self.trackinfo = []
        for i in range(self.status[5]):
            self.trackinfo.append(None)

        for i in range(self.status[5], self.status[6] + 1):
            self.trackinfo.append(self.player.gettrackinfo(i))

        return

    def cachestatus(self):
        self.status = self.player.getstatus()
        if self.status[0] == CD.NODISC:
            self.status = None
            raise Error, 'no disc in player'
        return

    def getstatus(self):
        return self.player.getstatus()

    def play--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'status'
6	POP_JUMP_IF_TRUE  '22'

9	LOAD_FAST         'self'
12	LOAD_ATTR         'cachestatus'
15	CALL_FUNCTION_0   None
18	POP_TOP           None
19	JUMP_FORWARD      '22'
22_0	COME_FROM         '19'

22	LOAD_FAST         'self'
25	LOAD_ATTR         'player'
28	LOAD_ATTR         'bestreadsize'
31	CALL_FUNCTION_0   None
34	STORE_FAST        'size'

37	LOAD_CONST        0
40	LOAD_FAST         'self'
43	STORE_ATTR        'listindex'

46	LOAD_CONST        0
49	LOAD_FAST         'self'
52	STORE_ATTR        'playing'

55	SETUP_LOOP        '144'
58	LOAD_GLOBAL       'range'
61	LOAD_CONST        8
64	CALL_FUNCTION_1   None
67	GET_ITER          None
68	FOR_ITER          '143'
71	STORE_FAST        'i'

74	LOAD_FAST         'self'
77	LOAD_ATTR         'callbacks'
80	LOAD_FAST         'i'
83	BINARY_SUBSCR     None
84	UNPACK_SEQUENCE_2 None
87	STORE_FAST        'func'
90	STORE_FAST        'arg'

93	LOAD_FAST         'func'
96	POP_JUMP_IF_FALSE '124'

99	LOAD_FAST         'self'
102	LOAD_ATTR         'parser'
105	LOAD_ATTR         'setcallback'
108	LOAD_FAST         'i'
111	LOAD_FAST         'func'
114	LOAD_FAST         'arg'
117	CALL_FUNCTION_3   None
120	POP_TOP           None
121	JUMP_BACK         '68'

124	LOAD_FAST         'self'
127	LOAD_ATTR         'parser'
130	LOAD_ATTR         'removecallback'
133	LOAD_FAST         'i'
136	CALL_FUNCTION_1   None
139	POP_TOP           None
140	JUMP_BACK         '68'
143	POP_BLOCK         None
144_0	COME_FROM         '55'

144	LOAD_GLOBAL       'len'
147	LOAD_FAST         'self'
150	LOAD_ATTR         'list'
153	CALL_FUNCTION_1   None
156	LOAD_CONST        0
159	COMPARE_OP        '=='
162	POP_JUMP_IF_FALSE '225'

165	SETUP_LOOP        '225'
168	LOAD_GLOBAL       'range'
171	LOAD_FAST         'self'
174	LOAD_ATTR         'status'
177	LOAD_CONST        5
180	BINARY_SUBSCR     None
181	LOAD_FAST         'self'
184	LOAD_ATTR         'status'
187	LOAD_CONST        6
190	BINARY_SUBSCR     None
191	LOAD_CONST        1
194	BINARY_ADD        None
195	CALL_FUNCTION_2   None
198	GET_ITER          None
199	FOR_ITER          '221'
202	STORE_FAST        'i'

205	LOAD_FAST         'self'
208	LOAD_ATTR         'appendtrack'
211	LOAD_FAST         'i'
214	CALL_FUNCTION_1   None
217	POP_TOP           None
218	JUMP_BACK         '199'
221	POP_BLOCK         None
222_0	COME_FROM         '165'
222	JUMP_FORWARD      '225'
225_0	COME_FROM         '222'

225	SETUP_FINALLY     '796'

228	SETUP_LOOP        '792'

231	LOAD_FAST         'self'
234	LOAD_ATTR         'playing'
237	POP_JUMP_IF_TRUE  '662'

240	LOAD_FAST         'self'
243	LOAD_ATTR         'listindex'
246	LOAD_GLOBAL       'len'
249	LOAD_FAST         'self'
252	LOAD_ATTR         'list'
255	CALL_FUNCTION_1   None
258	COMPARE_OP        '>='
261	POP_JUMP_IF_FALSE '268'

264	LOAD_CONST        None
267	RETURN_END_IF     None

268	LOAD_FAST         'self'
271	LOAD_ATTR         'list'
274	LOAD_FAST         'self'
277	LOAD_ATTR         'listindex'
280	BINARY_SUBSCR     None
281	UNPACK_SEQUENCE_2 None
284	STORE_FAST        'start'
287	STORE_FAST        'end'

290	LOAD_GLOBAL       'type'
293	LOAD_FAST         'start'
296	CALL_FUNCTION_1   None
299	LOAD_GLOBAL       'type'
302	LOAD_CONST        0
305	CALL_FUNCTION_1   None
308	COMPARE_OP        '=='
311	POP_JUMP_IF_FALSE '335'

314	LOAD_FAST         'self'
317	LOAD_ATTR         'player'
320	LOAD_ATTR         'seektrack'

323	LOAD_FAST         'start'
326	CALL_FUNCTION_1   None
329	STORE_FAST        'dummy'
332	JUMP_FORWARD      '374'

335	LOAD_FAST         'start'
338	UNPACK_SEQUENCE_3 None
341	STORE_FAST        'min'
344	STORE_FAST        'sec'
347	STORE_FAST        'frame'

350	LOAD_FAST         'self'
353	LOAD_ATTR         'player'
356	LOAD_ATTR         'seek'

359	LOAD_FAST         'min'
362	LOAD_FAST         'sec'
365	LOAD_FAST         'frame'
368	CALL_FUNCTION_3   None
371	STORE_FAST        'dummy'
374_0	COME_FROM         '332'

374	LOAD_GLOBAL       'type'
377	LOAD_FAST         'end'
380	CALL_FUNCTION_1   None
383	LOAD_GLOBAL       'type'
386	LOAD_CONST        0
389	CALL_FUNCTION_1   None
392	COMPARE_OP        '=='
395	POP_JUMP_IF_FALSE '510'

398	LOAD_FAST         'self'
401	LOAD_ATTR         'parser'
404	LOAD_ATTR         'setcallback'

407	LOAD_GLOBAL       'CD'
410	LOAD_ATTR         'PNUM'
413	LOAD_GLOBAL       '_dopnum'
416	LOAD_FAST         'self'
419	CALL_FUNCTION_3   None
422	POP_TOP           None

423	LOAD_FAST         'end'
426	LOAD_FAST         'self'
429	STORE_ATTR        'end'

432	LOAD_FAST         'self'
435	LOAD_ATTR         'callbacks'
438	LOAD_GLOBAL       'CD'
441	LOAD_ATTR         'ATIME'
444	BINARY_SUBSCR     None
445	UNPACK_SEQUENCE_2 None
448	STORE_FAST        'func'
451	STORE_FAST        'arg'

454	LOAD_FAST         'func'
457	POP_JUMP_IF_FALSE '488'

460	LOAD_FAST         'self'
463	LOAD_ATTR         'parser'
466	LOAD_ATTR         'setcallback'
469	LOAD_GLOBAL       'CD'
472	LOAD_ATTR         'ATIME'
475	LOAD_FAST         'func'
478	LOAD_FAST         'arg'
481	CALL_FUNCTION_3   None
484	POP_TOP           None
485	JUMP_ABSOLUTE     '650'

488	LOAD_FAST         'self'
491	LOAD_ATTR         'parser'
494	LOAD_ATTR         'removecallback'
497	LOAD_GLOBAL       'CD'
500	LOAD_ATTR         'ATIME'
503	CALL_FUNCTION_1   None
506	POP_TOP           None
507	JUMP_FORWARD      '650'

510	LOAD_FAST         'end'
513	UNPACK_SEQUENCE_3 None
516	STORE_FAST        'min'
519	STORE_FAST        'sec'
522	STORE_FAST        'frame'

525	LOAD_FAST         'self'
528	LOAD_ATTR         'parser'
531	LOAD_ATTR         'setcallback'

534	LOAD_GLOBAL       'CD'
537	LOAD_ATTR         'ATIME'
540	LOAD_GLOBAL       '_doatime'

543	LOAD_FAST         'self'
546	CALL_FUNCTION_3   None
549	POP_TOP           None

550	LOAD_FAST         'min'
553	LOAD_CONST        60
556	BINARY_MULTIPLY   None
557	LOAD_FAST         'sec'
560	BINARY_ADD        None

561	LOAD_CONST        75
564	BINARY_MULTIPLY   None
565	LOAD_FAST         'frame'
568	BINARY_ADD        None
569	LOAD_FAST         'self'
572	STORE_ATTR        'end'

575	LOAD_FAST         'self'
578	LOAD_ATTR         'callbacks'
581	LOAD_GLOBAL       'CD'
584	LOAD_ATTR         'PNUM'
587	BINARY_SUBSCR     None
588	UNPACK_SEQUENCE_2 None
591	STORE_FAST        'func'
594	STORE_FAST        'arg'

597	LOAD_FAST         'func'
600	POP_JUMP_IF_FALSE '631'

603	LOAD_FAST         'self'
606	LOAD_ATTR         'parser'
609	LOAD_ATTR         'setcallback'
612	LOAD_GLOBAL       'CD'
615	LOAD_ATTR         'PNUM'
618	LOAD_FAST         'func'
621	LOAD_FAST         'arg'
624	CALL_FUNCTION_3   None
627	POP_TOP           None
628	JUMP_FORWARD      '650'

631	LOAD_FAST         'self'
634	LOAD_ATTR         'parser'
637	LOAD_ATTR         'removecallback'
640	LOAD_GLOBAL       'CD'
643	LOAD_ATTR         'PNUM'
646	CALL_FUNCTION_1   None
649	POP_TOP           None
650_0	COME_FROM         '507'
650_1	COME_FROM         '628'

650	LOAD_CONST        1
653	LOAD_FAST         'self'
656	STORE_ATTR        'playing'
659	JUMP_FORWARD      '662'
662_0	COME_FROM         '659'

662	LOAD_FAST         'self'
665	LOAD_ATTR         'player'
668	LOAD_ATTR         'readda'
671	LOAD_FAST         'size'
674	CALL_FUNCTION_1   None
677	STORE_FAST        'data'

680	LOAD_FAST         'data'
683	LOAD_CONST        ''
686	COMPARE_OP        '=='
689	POP_JUMP_IF_FALSE '723'

692	LOAD_CONST        0
695	LOAD_FAST         'self'
698	STORE_ATTR        'playing'

701	LOAD_FAST         'self'
704	LOAD_ATTR         'listindex'
707	LOAD_CONST        1
710	BINARY_ADD        None
711	LOAD_FAST         'self'
714	STORE_ATTR        'listindex'

717	CONTINUE          '231'
720	JUMP_FORWARD      '723'
723_0	COME_FROM         '720'

723	SETUP_EXCEPT      '746'

726	LOAD_FAST         'self'
729	LOAD_ATTR         'parser'
732	LOAD_ATTR         'parseframe'
735	LOAD_FAST         'data'
738	CALL_FUNCTION_1   None
741	POP_TOP           None
742	POP_BLOCK         None
743	JUMP_BACK         '231'
746_0	COME_FROM         '723'

746	DUP_TOP           None
747	LOAD_GLOBAL       '_Stop'
750	COMPARE_OP        'exception match'
753	POP_JUMP_IF_FALSE '787'
756	POP_TOP           None
757	POP_TOP           None
758	POP_TOP           None

759	LOAD_CONST        0
762	LOAD_FAST         'self'
765	STORE_ATTR        'playing'

768	LOAD_FAST         'self'
771	LOAD_ATTR         'listindex'
774	LOAD_CONST        1
777	BINARY_ADD        None
778	LOAD_FAST         'self'
781	STORE_ATTR        'listindex'
784	JUMP_BACK         '231'
787	END_FINALLY       None
788_0	COME_FROM         '787'
788	JUMP_BACK         '231'
791	POP_BLOCK         None
792_0	COME_FROM         '228'
792	POP_BLOCK         None
793	LOAD_CONST        None
796_0	COME_FROM         '225'

796	LOAD_CONST        0
799	LOAD_FAST         'self'
802	STORE_ATTR        'playing'
805	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 791