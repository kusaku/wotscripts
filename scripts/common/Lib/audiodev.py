# Embedded file name: scripts/common/Lib/audiodev.py
"""Classes for manipulating audio devices (currently only for Sun and SGI)"""
from warnings import warnpy3k
warnpy3k('the audiodev module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
__all__ = ['error', 'AudioDev']

class error(Exception):
    pass


class Play_Audio_sgi:
    classinited = 0
    frameratelist = nchannelslist = sampwidthlist = None

    def initclass(self):
        import AL
        self.frameratelist = [(48000, AL.RATE_48000),
         (44100, AL.RATE_44100),
         (32000, AL.RATE_32000),
         (22050, AL.RATE_22050),
         (16000, AL.RATE_16000),
         (11025, AL.RATE_11025),
         (8000, AL.RATE_8000)]
        self.nchannelslist = [(1, AL.MONO), (2, AL.STEREO), (4, AL.QUADRO)]
        self.sampwidthlist = [(1, AL.SAMPLE_8), (2, AL.SAMPLE_16), (3, AL.SAMPLE_24)]
        self.classinited = 1

    def __init__(self):
        import al, AL
        if not self.classinited:
            self.initclass()
        self.oldparams = []
        self.params = [AL.OUTPUT_RATE, 0]
        self.config = al.newconfig()
        self.inited_outrate = 0
        self.inited_width = 0
        self.inited_nchannels = 0
        self.converter = None
        self.port = None
        return

    def __del__(self):
        if self.port:
            self.stop()
        if self.oldparams:
            import al, AL
            al.setparams(AL.DEFAULT_DEVICE, self.oldparams)
            self.oldparams = []

    def wait(self):
        if not self.port:
            return
        import time
        while self.port.getfilled() > 0:
            time.sleep(0.1)

        self.stop()

    def stop(self):
        if self.port:
            self.port.closeport()
            self.port = None
        if self.oldparams:
            import al, AL
            al.setparams(AL.DEFAULT_DEVICE, self.oldparams)
            self.oldparams = []
        return

    def setoutrate(self, rate):
        for raw, cooked in self.frameratelist:
            if rate == raw:
                self.params[1] = cooked
                self.inited_outrate = 1
                break
        else:
            raise error, 'bad output rate'

    def setsampwidth(self, width):
        for raw, cooked in self.sampwidthlist:
            if width == raw:
                self.config.setwidth(cooked)
                self.inited_width = 1
                break
        else:
            if width == 0:
                import AL
                self.inited_width = 0
                self.config.setwidth(AL.SAMPLE_16)
                self.converter = self.ulaw2lin
            else:
                raise error, 'bad sample width'

    def setnchannels(self, nchannels):
        for raw, cooked in self.nchannelslist:
            if nchannels == raw:
                self.config.setchannels(cooked)
                self.inited_nchannels = 1
                break
        else:
            raise error, 'bad # of channels'

    def writeframes(self, data):
        if not (self.inited_outrate and self.inited_nchannels):
            raise error, 'params not specified'
        if not self.port:
            import al, AL
            self.port = al.openport('Python', 'w', self.config)
            self.oldparams = self.params[:]
            al.getparams(AL.DEFAULT_DEVICE, self.oldparams)
            al.setparams(AL.DEFAULT_DEVICE, self.params)
        if self.converter:
            data = self.converter(data)
        self.port.writesamps(data)

    def getfilled(self):
        if self.port:
            return self.port.getfilled()
        else:
            return 0

    def getfillable(self):
        if self.port:
            return self.port.getfillable()
        else:
            return self.config.getqueuesize()

    def ulaw2lin(self, data):
        import audioop
        return audioop.ulaw2lin(data, 2)


class Play_Audio_sun:

    def __init__(self):
        self.outrate = 0
        self.sampwidth = 0
        self.nchannels = 0
        self.inited_outrate = 0
        self.inited_width = 0
        self.inited_nchannels = 0
        self.converter = None
        self.port = None
        return

    def __del__(self):
        self.stop()

    def setoutrate(self, rate):
        self.outrate = rate
        self.inited_outrate = 1

    def setsampwidth(self, width):
        self.sampwidth = width
        self.inited_width = 1

    def setnchannels(self, nchannels):
        self.nchannels = nchannels
        self.inited_nchannels = 1

    def writeframes(self, data):
        if not (self.inited_outrate and self.inited_width and self.inited_nchannels):
            raise error, 'params not specified'
        if not self.port:
            import sunaudiodev, SUNAUDIODEV
            self.port = sunaudiodev.open('w')
            info = self.port.getinfo()
            info.o_sample_rate = self.outrate
            info.o_channels = self.nchannels
            if self.sampwidth == 0:
                info.o_precision = 8
                self.o_encoding = SUNAUDIODEV.ENCODING_ULAW
            else:
                info.o_precision = 8 * self.sampwidth
                info.o_encoding = SUNAUDIODEV.ENCODING_LINEAR
                self.port.setinfo(info)
        if self.converter:
            data = self.converter(data)
        self.port.write(data)

    def wait(self):
        if not self.port:
            return
        self.port.drain()
        self.stop()

    def stop(self):
        if self.port:
            self.port.flush()
            self.port.close()
            self.port = None
        return

    def getfilled(self):
        if self.port:
            return self.port.obufcount()
        else:
            return 0


def AudioDev():
    try:
        import al
    except ImportError:
        try:
            import sunaudiodev
            return Play_Audio_sun()
        except ImportError:
            try:
                import Audio_mac
            except ImportError:
                raise error, 'no audio device'
            else:
                return Audio_mac.Play_Audio_mac()

    else:
        return Play_Audio_sgi()


def test--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'sys'
9	STORE_FAST        'sys'

12	LOAD_FAST         'sys'
15	LOAD_ATTR         'argv'
18	LOAD_CONST        1
21	SLICE+1           None
22	POP_JUMP_IF_FALSE '41'

25	LOAD_FAST         'sys'
28	LOAD_ATTR         'argv'
31	LOAD_CONST        1
34	BINARY_SUBSCR     None
35	STORE_FAST        'fn'
38	JUMP_FORWARD      '47'

41	LOAD_CONST        'f:just samples:just.aif'
44	STORE_FAST        'fn'
47_0	COME_FROM         '38'

47	LOAD_CONST        -1
50	LOAD_CONST        None
53	IMPORT_NAME       'aifc'
56	STORE_FAST        'aifc'

59	LOAD_FAST         'aifc'
62	LOAD_ATTR         'open'
65	LOAD_FAST         'fn'
68	LOAD_CONST        'r'
71	CALL_FUNCTION_2   None
74	STORE_FAST        'af'

77	LOAD_FAST         'fn'
80	PRINT_ITEM        None
81	LOAD_FAST         'af'
84	LOAD_ATTR         'getparams'
87	CALL_FUNCTION_0   None
90	PRINT_ITEM_CONT   None
91	PRINT_NEWLINE_CONT None

92	LOAD_GLOBAL       'AudioDev'
95	CALL_FUNCTION_0   None
98	STORE_FAST        'p'

101	LOAD_FAST         'p'
104	LOAD_ATTR         'setoutrate'
107	LOAD_FAST         'af'
110	LOAD_ATTR         'getframerate'
113	CALL_FUNCTION_0   None
116	CALL_FUNCTION_1   None
119	POP_TOP           None

120	LOAD_FAST         'p'
123	LOAD_ATTR         'setsampwidth'
126	LOAD_FAST         'af'
129	LOAD_ATTR         'getsampwidth'
132	CALL_FUNCTION_0   None
135	CALL_FUNCTION_1   None
138	POP_TOP           None

139	LOAD_FAST         'p'
142	LOAD_ATTR         'setnchannels'
145	LOAD_FAST         'af'
148	LOAD_ATTR         'getnchannels'
151	CALL_FUNCTION_0   None
154	CALL_FUNCTION_1   None
157	POP_TOP           None

158	LOAD_FAST         'af'
161	LOAD_ATTR         'getframerate'
164	CALL_FUNCTION_0   None
167	LOAD_FAST         'af'
170	LOAD_ATTR         'getsampwidth'
173	CALL_FUNCTION_0   None
176	BINARY_DIVIDE     None
177	LOAD_FAST         'af'
180	LOAD_ATTR         'getnchannels'
183	CALL_FUNCTION_0   None
186	BINARY_DIVIDE     None
187	STORE_FAST        'BUFSIZ'

190	SETUP_LOOP        '246'

193	LOAD_FAST         'af'
196	LOAD_ATTR         'readframes'
199	LOAD_FAST         'BUFSIZ'
202	CALL_FUNCTION_1   None
205	STORE_FAST        'data'

208	LOAD_FAST         'data'
211	POP_JUMP_IF_TRUE  '218'
214	BREAK_LOOP        None
215	JUMP_FORWARD      '218'
218_0	COME_FROM         '215'

218	LOAD_GLOBAL       'len'
221	LOAD_FAST         'data'
224	CALL_FUNCTION_1   None
227	PRINT_ITEM        None
228	PRINT_NEWLINE_CONT None

229	LOAD_FAST         'p'
232	LOAD_ATTR         'writeframes'
235	LOAD_FAST         'data'
238	CALL_FUNCTION_1   None
241	POP_TOP           None
242	JUMP_BACK         '193'
245	POP_BLOCK         None
246_0	COME_FROM         '190'

246	LOAD_FAST         'p'
249	LOAD_ATTR         'wait'
252	CALL_FUNCTION_0   None
255	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 245


if __name__ == '__main__':
    test()