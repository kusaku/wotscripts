# Embedded file name: scripts/common/Lib/plat-mac/Audio_mac.py
QSIZE = 100000
error = 'Audio_mac.error'
from warnings import warnpy3k
warnpy3k('In 3.x, the Play_Audio_mac module is removed.', stacklevel=2)

class Play_Audio_mac:

    def __init__(self, qsize = QSIZE):
        self._chan = None
        self._qsize = qsize
        self._outrate = 22254
        self._sampwidth = 1
        self._nchannels = 1
        self._gc = []
        self._usercallback = None
        return

    def __del__(self):
        self.stop()
        self._usercallback = None
        return

    def wait(self):
        import time
        while self.getfilled():
            time.sleep(0.1)

        self._chan = None
        self._gc = []
        return

    def stop(self, quietNow = 1):
        self._chan = None
        self._gc = []
        return

    def setoutrate(self, outrate):
        self._outrate = outrate

    def setsampwidth(self, sampwidth):
        self._sampwidth = sampwidth

    def setnchannels(self, nchannels):
        self._nchannels = nchannels

    def writeframes(self, data):
        import time
        from Carbon.Sound import bufferCmd, callBackCmd, extSH
        import struct
        import MacOS
        if not self._chan:
            from Carbon import Snd
            self._chan = Snd.SndNewChannel(5, 0, self._callback)
        nframes = len(data) / self._nchannels / self._sampwidth
        if len(data) != nframes * self._nchannels * self._sampwidth:
            raise error, 'data is not a whole number of frames'
        while self._gc and self.getfilled() + nframes > self._qsize / self._nchannels / self._sampwidth:
            time.sleep(0.1)

        if self._sampwidth == 1:
            import audioop
            data = audioop.add(data, '\x80' * len(data), 1)
        h1 = struct.pack('llHhllbbl', id(data) + MacOS.string_id_to_buffer, self._nchannels, self._outrate, 0, 0, 0, extSH, 60, nframes)
        h2 = 22 * '\x00'
        h3 = struct.pack('hhlll', self._sampwidth * 8, 0, 0, 0, 0)
        header = h1 + h2 + h3
        self._gc.append((header, data))
        self._chan.SndDoCommand((bufferCmd, 0, header), 0)
        self._chan.SndDoCommand((callBackCmd, 0, 0), 0)

    def _callback(self, *args):
        del self._gc[0]
        if self._usercallback:
            self._usercallback()

    def setcallback(self, callback):
        self._usercallback = callback

    def getfilled(self):
        filled = 0
        for header, data in self._gc:
            filled = filled + len(data)

        return filled / self._nchannels / self._sampwidth

    def getfillable(self):
        return self._qsize / self._nchannels / self._sampwidth - self.getfilled()

    def ulaw2lin(self, data):
        import audioop
        return audioop.ulaw2lin(data, 2)


def test--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'aifc'
9	STORE_FAST        'aifc'

12	LOAD_CONST        -1
15	LOAD_CONST        None
18	IMPORT_NAME       'EasyDialogs'
21	STORE_FAST        'EasyDialogs'

24	LOAD_FAST         'EasyDialogs'
27	LOAD_ATTR         'AskFileForOpen'
30	LOAD_CONST        'message'
33	LOAD_CONST        'Select an AIFF soundfile'
36	LOAD_CONST        'typeList'
39	LOAD_CONST        ('AIFF',)
42	CALL_FUNCTION_512 None
45	STORE_FAST        'fn'

48	LOAD_FAST         'fn'
51	POP_JUMP_IF_TRUE  '58'
54	LOAD_CONST        None
57	RETURN_END_IF     None

58	LOAD_FAST         'aifc'
61	LOAD_ATTR         'open'
64	LOAD_FAST         'fn'
67	LOAD_CONST        'r'
70	CALL_FUNCTION_2   None
73	STORE_FAST        'af'

76	LOAD_FAST         'af'
79	LOAD_ATTR         'getparams'
82	CALL_FUNCTION_0   None
85	PRINT_ITEM        None
86	PRINT_NEWLINE_CONT None

87	LOAD_GLOBAL       'Play_Audio_mac'
90	CALL_FUNCTION_0   None
93	STORE_FAST        'p'

96	LOAD_FAST         'p'
99	LOAD_ATTR         'setoutrate'
102	LOAD_FAST         'af'
105	LOAD_ATTR         'getframerate'
108	CALL_FUNCTION_0   None
111	CALL_FUNCTION_1   None
114	POP_TOP           None

115	LOAD_FAST         'p'
118	LOAD_ATTR         'setsampwidth'
121	LOAD_FAST         'af'
124	LOAD_ATTR         'getsampwidth'
127	CALL_FUNCTION_0   None
130	CALL_FUNCTION_1   None
133	POP_TOP           None

134	LOAD_FAST         'p'
137	LOAD_ATTR         'setnchannels'
140	LOAD_FAST         'af'
143	LOAD_ATTR         'getnchannels'
146	CALL_FUNCTION_0   None
149	CALL_FUNCTION_1   None
152	POP_TOP           None

153	LOAD_CONST        10000
156	STORE_FAST        'BUFSIZ'

159	SETUP_LOOP        '233'

162	LOAD_FAST         'af'
165	LOAD_ATTR         'readframes'
168	LOAD_FAST         'BUFSIZ'
171	CALL_FUNCTION_1   None
174	STORE_FAST        'data'

177	LOAD_FAST         'data'
180	POP_JUMP_IF_TRUE  '187'
183	BREAK_LOOP        None
184	JUMP_FORWARD      '187'
187_0	COME_FROM         '184'

187	LOAD_FAST         'p'
190	LOAD_ATTR         'writeframes'
193	LOAD_FAST         'data'
196	CALL_FUNCTION_1   None
199	POP_TOP           None

200	LOAD_CONST        'wrote'
203	PRINT_ITEM        None
204	LOAD_GLOBAL       'len'
207	LOAD_FAST         'data'
210	CALL_FUNCTION_1   None
213	PRINT_ITEM_CONT   None
214	LOAD_CONST        'space'
217	PRINT_ITEM_CONT   None
218	LOAD_FAST         'p'
221	LOAD_ATTR         'getfillable'
224	CALL_FUNCTION_0   None
227	PRINT_ITEM_CONT   None
228	PRINT_NEWLINE_CONT None
229	JUMP_BACK         '162'
232	POP_BLOCK         None
233_0	COME_FROM         '159'

233	LOAD_FAST         'p'
236	LOAD_ATTR         'wait'
239	CALL_FUNCTION_0   None
242	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 232


if __name__ == '__main__':
    test()