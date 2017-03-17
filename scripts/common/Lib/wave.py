# Embedded file name: scripts/common/Lib/wave.py
"""Stuff to parse WAVE files.

Usage.

Reading WAVE files:
      f = wave.open(file, 'r')
where file is either the name of a file or an open file pointer.
The open file pointer must have methods read(), seek(), and close().
When the setpos() and rewind() methods are not used, the seek()
method is not  necessary.

This returns an instance of a class with the following public methods:
      getnchannels()  -- returns number of audio channels (1 for
                         mono, 2 for stereo)
      getsampwidth()  -- returns sample width in bytes
      getframerate()  -- returns sampling frequency
      getnframes()    -- returns number of audio frames
      getcomptype()   -- returns compression type ('NONE' for linear samples)
      getcompname()   -- returns human-readable version of
                         compression type ('not compressed' linear samples)
      getparams()     -- returns a tuple consisting of all of the
                         above in the above order
      getmarkers()    -- returns None (for compatibility with the
                         aifc module)
      getmark(id)     -- raises an error since the mark does not
                         exist (for compatibility with the aifc module)
      readframes(n)   -- returns at most n frames of audio
      rewind()        -- rewind to the beginning of the audio stream
      setpos(pos)     -- seek to the specified position
      tell()          -- return the current position
      close()         -- close the instance (make it unusable)
The position returned by tell() and the position given to setpos()
are compatible and have nothing to do with the actual position in the
file.
The close() method is called automatically when the class instance
is destroyed.

Writing WAVE files:
      f = wave.open(file, 'w')
where file is either the name of a file or an open file pointer.
The open file pointer must have methods write(), tell(), seek(), and
close().

This returns an instance of a class with the following public methods:
      setnchannels(n) -- set the number of channels
      setsampwidth(n) -- set the sample width
      setframerate(n) -- set the frame rate
      setnframes(n)   -- set the number of frames
      setcomptype(type, name)
                      -- set the compression type and the
                         human-readable compression type
      setparams(tuple)
                      -- set all parameters at once
      tell()          -- return current position in output file
      writeframesraw(data)
                      -- write audio frames without pathing up the
                         file header
      writeframes(data)
                      -- write audio frames and patch up the file header
      close()         -- patch up the file header and close the
                         output file
You should set the parameters before the first writeframesraw or
writeframes.  The total number of frames does not need to be set,
but when it is set to the correct value, the header does not have to
be patched up.
It is best to first set all parameters, perhaps possibly the
compression type, and then write audio frames using writeframesraw.
When all frames have been written, either call writeframes('') or
close() to patch up the sizes in the header.
The close() method is called automatically when the class instance
is destroyed.
"""
import __builtin__
__all__ = ['open', 'openfp', 'Error']

class Error(Exception):
    pass


WAVE_FORMAT_PCM = 1
_array_fmts = (None, 'b', 'h', None, 'l')
import struct
if struct.pack('h', 1) == '\x00\x01':
    big_endian = 1
else:
    big_endian = 0
from chunk import Chunk

class Wave_read:
    """Variables used in this class:
    
    These variables are available to the user though appropriate
    methods of this class:
    _file -- the open file with methods read(), close(), and seek()
              set through the __init__() method
    _nchannels -- the number of audio channels
              available through the getnchannels() method
    _nframes -- the number of audio frames
              available through the getnframes() method
    _sampwidth -- the number of bytes per audio sample
              available through the getsampwidth() method
    _framerate -- the sampling frequency
              available through the getframerate() method
    _comptype -- the AIFF-C compression type ('NONE' if AIFF)
              available through the getcomptype() method
    _compname -- the human-readable AIFF-C compression type
              available through the getcomptype() method
    _soundpos -- the position in the audio stream
              available through the tell() method, set through the
              setpos() method
    
    These variables are used internally only:
    _fmt_chunk_read -- 1 iff the FMT chunk has been read
    _data_seek_needed -- 1 iff positioned correctly in audio
              file for readframes()
    _data_chunk -- instantiation of a chunk class for the DATA chunk
    _framesize -- size of one frame in the file
    """

    def initfp--- This code section failed: ---

0	LOAD_CONST        None
3	LOAD_FAST         'self'
6	STORE_ATTR        '_convert'

9	LOAD_CONST        0
12	LOAD_FAST         'self'
15	STORE_ATTR        '_soundpos'

18	LOAD_GLOBAL       'Chunk'
21	LOAD_FAST         'file'
24	LOAD_CONST        'bigendian'
27	LOAD_CONST        0
30	CALL_FUNCTION_257 None
33	LOAD_FAST         'self'
36	STORE_ATTR        '_file'

39	LOAD_FAST         'self'
42	LOAD_ATTR         '_file'
45	LOAD_ATTR         'getname'
48	CALL_FUNCTION_0   None
51	LOAD_CONST        'RIFF'
54	COMPARE_OP        '!='
57	POP_JUMP_IF_FALSE '72'

60	LOAD_GLOBAL       'Error'
63	LOAD_CONST        'file does not start with RIFF id'
66	RAISE_VARARGS_2   None
69	JUMP_FORWARD      '72'
72_0	COME_FROM         '69'

72	LOAD_FAST         'self'
75	LOAD_ATTR         '_file'
78	LOAD_ATTR         'read'
81	LOAD_CONST        4
84	CALL_FUNCTION_1   None
87	LOAD_CONST        'WAVE'
90	COMPARE_OP        '!='
93	POP_JUMP_IF_FALSE '108'

96	LOAD_GLOBAL       'Error'
99	LOAD_CONST        'not a WAVE file'
102	RAISE_VARARGS_2   None
105	JUMP_FORWARD      '108'
108_0	COME_FROM         '105'

108	LOAD_CONST        0
111	LOAD_FAST         'self'
114	STORE_ATTR        '_fmt_chunk_read'

117	LOAD_CONST        None
120	LOAD_FAST         'self'
123	STORE_ATTR        '_data_chunk'

126	SETUP_LOOP        '321'

129	LOAD_CONST        1
132	LOAD_FAST         'self'
135	STORE_ATTR        '_data_seek_needed'

138	SETUP_EXCEPT      '166'

141	LOAD_GLOBAL       'Chunk'
144	LOAD_FAST         'self'
147	LOAD_ATTR         '_file'
150	LOAD_CONST        'bigendian'
153	LOAD_CONST        0
156	CALL_FUNCTION_257 None
159	STORE_FAST        'chunk'
162	POP_BLOCK         None
163	JUMP_FORWARD      '184'
166_0	COME_FROM         '138'

166	DUP_TOP           None
167	LOAD_GLOBAL       'EOFError'
170	COMPARE_OP        'exception match'
173	POP_JUMP_IF_FALSE '183'
176	POP_TOP           None
177	POP_TOP           None
178	POP_TOP           None

179	BREAK_LOOP        None
180	JUMP_FORWARD      '184'
183	END_FINALLY       None
184_0	COME_FROM         '163'
184_1	COME_FROM         '183'

184	LOAD_FAST         'chunk'
187	LOAD_ATTR         'getname'
190	CALL_FUNCTION_0   None
193	STORE_FAST        'chunkname'

196	LOAD_FAST         'chunkname'
199	LOAD_CONST        'fmt '
202	COMPARE_OP        '=='
205	POP_JUMP_IF_FALSE '233'

208	LOAD_FAST         'self'
211	LOAD_ATTR         '_read_fmt_chunk'
214	LOAD_FAST         'chunk'
217	CALL_FUNCTION_1   None
220	POP_TOP           None

221	LOAD_CONST        1
224	LOAD_FAST         'self'
227	STORE_ATTR        '_fmt_chunk_read'
230	JUMP_FORWARD      '307'

233	LOAD_FAST         'chunkname'
236	LOAD_CONST        'data'
239	COMPARE_OP        '=='
242	POP_JUMP_IF_FALSE '307'

245	LOAD_FAST         'self'
248	LOAD_ATTR         '_fmt_chunk_read'
251	POP_JUMP_IF_TRUE  '266'

254	LOAD_GLOBAL       'Error'
257	LOAD_CONST        'data chunk before fmt chunk'
260	RAISE_VARARGS_2   None
263	JUMP_FORWARD      '266'
266_0	COME_FROM         '263'

266	LOAD_FAST         'chunk'
269	LOAD_FAST         'self'
272	STORE_ATTR        '_data_chunk'

275	LOAD_FAST         'chunk'
278	LOAD_ATTR         'chunksize'
281	LOAD_FAST         'self'
284	LOAD_ATTR         '_framesize'
287	BINARY_FLOOR_DIVIDE None
288	LOAD_FAST         'self'
291	STORE_ATTR        '_nframes'

294	LOAD_CONST        0
297	LOAD_FAST         'self'
300	STORE_ATTR        '_data_seek_needed'

303	BREAK_LOOP        None
304	JUMP_FORWARD      '307'
307_0	COME_FROM         '230'
307_1	COME_FROM         '304'

307	LOAD_FAST         'chunk'
310	LOAD_ATTR         'skip'
313	CALL_FUNCTION_0   None
316	POP_TOP           None
317	JUMP_BACK         '129'
320	POP_BLOCK         None
321_0	COME_FROM         '126'

321	LOAD_FAST         'self'
324	LOAD_ATTR         '_fmt_chunk_read'
327	UNARY_NOT         None
328	POP_JUMP_IF_TRUE  '341'
331	LOAD_FAST         'self'
334	LOAD_ATTR         '_data_chunk'
337	UNARY_NOT         None
338_0	COME_FROM         '328'
338	POP_JUMP_IF_FALSE '353'

341	LOAD_GLOBAL       'Error'
344	LOAD_CONST        'fmt chunk and/or data chunk missing'
347	RAISE_VARARGS_2   None
350	JUMP_FORWARD      '353'
353_0	COME_FROM         '350'
353	LOAD_CONST        None
356	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 320

    def __init__(self, f):
        self._i_opened_the_file = None
        if isinstance(f, basestring):
            f = __builtin__.open(f, 'rb')
            self._i_opened_the_file = f
        try:
            self.initfp(f)
        except:
            if self._i_opened_the_file:
                f.close()
            raise

        return

    def __del__(self):
        self.close()

    def getfp(self):
        return self._file

    def rewind(self):
        self._data_seek_needed = 1
        self._soundpos = 0

    def close(self):
        if self._i_opened_the_file:
            self._i_opened_the_file.close()
            self._i_opened_the_file = None
        self._file = None
        return

    def tell(self):
        return self._soundpos

    def getnchannels(self):
        return self._nchannels

    def getnframes(self):
        return self._nframes

    def getsampwidth(self):
        return self._sampwidth

    def getframerate(self):
        return self._framerate

    def getcomptype(self):
        return self._comptype

    def getcompname(self):
        return self._compname

    def getparams(self):
        return (self.getnchannels(),
         self.getsampwidth(),
         self.getframerate(),
         self.getnframes(),
         self.getcomptype(),
         self.getcompname())

    def getmarkers(self):
        return None

    def getmark(self, id):
        raise Error, 'no marks'

    def setpos(self, pos):
        if pos < 0 or pos > self._nframes:
            raise Error, 'position not in range'
        self._soundpos = pos
        self._data_seek_needed = 1

    def readframes(self, nframes):
        if self._data_seek_needed:
            self._data_chunk.seek(0, 0)
            pos = self._soundpos * self._framesize
            if pos:
                self._data_chunk.seek(pos, 0)
            self._data_seek_needed = 0
        if nframes == 0:
            return ''
        if self._sampwidth > 1 and big_endian:
            import array
            chunk = self._data_chunk
            data = array.array(_array_fmts[self._sampwidth])
            nitems = nframes * self._nchannels
            if nitems * self._sampwidth > chunk.chunksize - chunk.size_read:
                nitems = (chunk.chunksize - chunk.size_read) / self._sampwidth
            data.fromfile(chunk.file.file, nitems)
            chunk.size_read = chunk.size_read + nitems * self._sampwidth
            chunk = chunk.file
            chunk.size_read = chunk.size_read + nitems * self._sampwidth
            data.byteswap()
            data = data.tostring()
        else:
            data = self._data_chunk.read(nframes * self._framesize)
        if self._convert and data:
            data = self._convert(data)
        self._soundpos = self._soundpos + len(data) // (self._nchannels * self._sampwidth)
        return data

    def _read_fmt_chunk(self, chunk):
        wFormatTag, self._nchannels, self._framerate, dwAvgBytesPerSec, wBlockAlign = struct.unpack('<hhllh', chunk.read(14))
        if wFormatTag == WAVE_FORMAT_PCM:
            sampwidth = struct.unpack('<h', chunk.read(2))[0]
            self._sampwidth = (sampwidth + 7) // 8
        else:
            raise Error, 'unknown format: %r' % (wFormatTag,)
        self._framesize = self._nchannels * self._sampwidth
        self._comptype = 'NONE'
        self._compname = 'not compressed'


class Wave_write:
    """Variables used in this class:
    
    These variables are user settable through appropriate methods
    of this class:
    _file -- the open file with methods write(), close(), tell(), seek()
              set through the __init__() method
    _comptype -- the AIFF-C compression type ('NONE' in AIFF)
              set through the setcomptype() or setparams() method
    _compname -- the human-readable AIFF-C compression type
              set through the setcomptype() or setparams() method
    _nchannels -- the number of audio channels
              set through the setnchannels() or setparams() method
    _sampwidth -- the number of bytes per audio sample
              set through the setsampwidth() or setparams() method
    _framerate -- the sampling frequency
              set through the setframerate() or setparams() method
    _nframes -- the number of audio frames written to the header
              set through the setnframes() or setparams() method
    
    These variables are used internally only:
    _datalength -- the size of the audio samples written to the header
    _nframeswritten -- the number of frames actually written
    _datawritten -- the size of the audio samples actually written
    """

    def __init__(self, f):
        self._i_opened_the_file = None
        if isinstance(f, basestring):
            f = __builtin__.open(f, 'wb')
            self._i_opened_the_file = f
        try:
            self.initfp(f)
        except:
            if self._i_opened_the_file:
                f.close()
            raise

        return

    def initfp(self, file):
        self._file = file
        self._convert = None
        self._nchannels = 0
        self._sampwidth = 0
        self._framerate = 0
        self._nframes = 0
        self._nframeswritten = 0
        self._datawritten = 0
        self._datalength = 0
        self._headerwritten = False
        return

    def __del__(self):
        self.close()

    def setnchannels(self, nchannels):
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        if nchannels < 1:
            raise Error, 'bad # of channels'
        self._nchannels = nchannels

    def getnchannels(self):
        if not self._nchannels:
            raise Error, 'number of channels not set'
        return self._nchannels

    def setsampwidth(self, sampwidth):
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        if sampwidth < 1 or sampwidth > 4:
            raise Error, 'bad sample width'
        self._sampwidth = sampwidth

    def getsampwidth(self):
        if not self._sampwidth:
            raise Error, 'sample width not set'
        return self._sampwidth

    def setframerate(self, framerate):
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        if framerate <= 0:
            raise Error, 'bad frame rate'
        self._framerate = framerate

    def getframerate(self):
        if not self._framerate:
            raise Error, 'frame rate not set'
        return self._framerate

    def setnframes(self, nframes):
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        self._nframes = nframes

    def getnframes(self):
        return self._nframeswritten

    def setcomptype(self, comptype, compname):
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        if comptype not in ('NONE',):
            raise Error, 'unsupported compression type'
        self._comptype = comptype
        self._compname = compname

    def getcomptype(self):
        return self._comptype

    def getcompname(self):
        return self._compname

    def setparams(self, params):
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        if self._datawritten:
            raise Error, 'cannot change parameters after starting to write'
        self.setnchannels(nchannels)
        self.setsampwidth(sampwidth)
        self.setframerate(framerate)
        self.setnframes(nframes)
        self.setcomptype(comptype, compname)

    def getparams(self):
        if not self._nchannels or not self._sampwidth or not self._framerate:
            raise Error, 'not all parameters set'
        return (self._nchannels,
         self._sampwidth,
         self._framerate,
         self._nframes,
         self._comptype,
         self._compname)

    def setmark(self, id, pos, name):
        raise Error, 'setmark() not supported'

    def getmark(self, id):
        raise Error, 'no marks'

    def getmarkers(self):
        return None

    def tell(self):
        return self._nframeswritten

    def writeframesraw(self, data):
        self._ensure_header_written(len(data))
        nframes = len(data) // (self._sampwidth * self._nchannels)
        if self._convert:
            data = self._convert(data)
        if self._sampwidth > 1 and big_endian:
            import array
            data = array.array(_array_fmts[self._sampwidth], data)
            data.byteswap()
            data.tofile(self._file)
            self._datawritten = self._datawritten + len(data) * self._sampwidth
        else:
            self._file.write(data)
            self._datawritten = self._datawritten + len(data)
        self._nframeswritten = self._nframeswritten + nframes

    def writeframes(self, data):
        self.writeframesraw(data)
        if self._datalength != self._datawritten:
            self._patchheader()

    def close(self):
        if self._file:
            self._ensure_header_written(0)
            if self._datalength != self._datawritten:
                self._patchheader()
            self._file.flush()
            self._file = None
        if self._i_opened_the_file:
            self._i_opened_the_file.close()
            self._i_opened_the_file = None
        return

    def _ensure_header_written(self, datasize):
        if not self._headerwritten:
            if not self._nchannels:
                raise Error, '# channels not specified'
            if not self._sampwidth:
                raise Error, 'sample width not specified'
            if not self._framerate:
                raise Error, 'sampling rate not specified'
            self._write_header(datasize)

    def _write_header(self, initlength):
        if not not self._headerwritten:
            raise AssertionError
            self._file.write('RIFF')
            self._nframes = self._nframes or initlength / (self._nchannels * self._sampwidth)
        self._datalength = self._nframes * self._nchannels * self._sampwidth
        self._form_length_pos = self._file.tell()
        self._file.write(struct.pack('<l4s4slhhllhh4s', 36 + self._datalength, 'WAVE', 'fmt ', 16, WAVE_FORMAT_PCM, self._nchannels, self._framerate, self._nchannels * self._framerate * self._sampwidth, self._nchannels * self._sampwidth, self._sampwidth * 8, 'data'))
        self._data_length_pos = self._file.tell()
        self._file.write(struct.pack('<l', self._datalength))
        self._headerwritten = True

    def _patchheader(self):
        if not self._headerwritten:
            raise AssertionError
            return self._datawritten == self._datalength and None
        curpos = self._file.tell()
        self._file.seek(self._form_length_pos, 0)
        self._file.write(struct.pack('<l', 36 + self._datawritten))
        self._file.seek(self._data_length_pos, 0)
        self._file.write(struct.pack('<l', self._datawritten))
        self._file.seek(curpos, 0)
        self._datalength = self._datawritten


def open(f, mode = None):
    if mode is None:
        if hasattr(f, 'mode'):
            mode = f.mode
        else:
            mode = 'rb'
    if mode in ('r', 'rb'):
        return Wave_read(f)
    elif mode in ('w', 'wb'):
        return Wave_write(f)
    else:
        raise Error, "mode must be 'r', 'rb', 'w', or 'wb'"
        return


openfp = open