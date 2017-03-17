# Embedded file name: scripts/common/Lib/plat-irix6/jpeg.py
from warnings import warnpy3k
warnpy3k('the jpeg module has been removed in Python 3.0', stacklevel=2)
del warnpy3k

class error(Exception):
    pass


options = {'quality': 75,
 'optimize': 0,
 'smooth': 0,
 'forcegray': 0}
comp = None
decomp = None

def compress(imgdata, width, height, bytesperpixel):
    global comp
    import cl
    if comp is None:
        comp = cl.OpenCompressor(cl.JPEG)
    if bytesperpixel == 1:
        format = cl.GRAYSCALE
    elif bytesperpixel == 4:
        format = cl.RGBX
    if options['forcegray']:
        iformat = cl.GRAYSCALE
    else:
        iformat = cl.YUV
    params = [cl.IMAGE_WIDTH,
     width,
     cl.IMAGE_HEIGHT,
     height,
     cl.ORIGINAL_FORMAT,
     format,
     cl.ORIENTATION,
     cl.BOTTOM_UP,
     cl.QUALITY_FACTOR,
     options['quality'],
     cl.INTERNAL_FORMAT,
     iformat]
    comp.SetParams(params)
    jpegdata = comp.Compress(1, imgdata)
    return jpegdata


def decompress(jpegdata):
    global decomp
    import cl
    if decomp is None:
        decomp = cl.OpenDecompressor(cl.JPEG)
    headersize = decomp.ReadHeader(jpegdata)
    params = [cl.IMAGE_WIDTH,
     0,
     cl.IMAGE_HEIGHT,
     0,
     cl.INTERNAL_FORMAT,
     0]
    decomp.GetParams(params)
    width, height, format = params[1], params[3], params[5]
    if format == cl.GRAYSCALE or options['forcegray']:
        format = cl.GRAYSCALE
        bytesperpixel = 1
    else:
        format = cl.RGBX
        bytesperpixel = 4
    params = [cl.ORIGINAL_FORMAT,
     format,
     cl.ORIENTATION,
     cl.BOTTOM_UP,
     cl.FRAME_BUFFER_SIZE,
     width * height * bytesperpixel]
    decomp.SetParams(params)
    imgdata = decomp.Decompress(1, jpegdata)
    return (imgdata,
     width,
     height,
     bytesperpixel)


def setoption(name, value):
    if type(value) is not type(0):
        raise TypeError, 'jpeg.setoption: numeric options only'
    if name == 'forcegrey':
        name = 'forcegray'
    if not options.has_key(name):
        raise KeyError, 'jpeg.setoption: unknown option name'
    options[name] = int(value)


def test():
    import sys
    if sys.argv[1:2] == ['-g']:
        del sys.argv[1]
        setoption('forcegray', 1)
    if not sys.argv[1:]:
        sys.argv.append('/usr/local/images/data/jpg/asterix.jpg')
    for file in sys.argv[1:]:
        show(file)


def show--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'gl'
9	STORE_FAST        'gl'
12	LOAD_CONST        -1
15	LOAD_CONST        None
18	IMPORT_NAME_CONT  'GL'
21	STORE_FAST        'GL'
24	LOAD_CONST        -1
27	LOAD_CONST        None
30	IMPORT_NAME_CONT  'DEVICE'
33	STORE_FAST        'DEVICE'

36	LOAD_GLOBAL       'open'
39	LOAD_FAST         'file'
42	LOAD_CONST        'r'
45	CALL_FUNCTION_2   None
48	LOAD_ATTR         'read'
51	CALL_FUNCTION_0   None
54	STORE_FAST        'jpegdata'

57	LOAD_GLOBAL       'decompress'
60	LOAD_FAST         'jpegdata'
63	CALL_FUNCTION_1   None
66	UNPACK_SEQUENCE_4 None
69	STORE_FAST        'imgdata'
72	STORE_FAST        'width'
75	STORE_FAST        'height'
78	STORE_FAST        'bytesperpixel'

81	LOAD_FAST         'gl'
84	LOAD_ATTR         'foreground'
87	CALL_FUNCTION_0   None
90	POP_TOP           None

91	LOAD_FAST         'gl'
94	LOAD_ATTR         'prefsize'
97	LOAD_FAST         'width'
100	LOAD_FAST         'height'
103	CALL_FUNCTION_2   None
106	POP_TOP           None

107	LOAD_FAST         'gl'
110	LOAD_ATTR         'winopen'
113	LOAD_FAST         'file'
116	CALL_FUNCTION_1   None
119	STORE_FAST        'win'

122	LOAD_FAST         'bytesperpixel'
125	LOAD_CONST        1
128	COMPARE_OP        '=='
131	POP_JUMP_IF_FALSE '221'

134	LOAD_FAST         'gl'
137	LOAD_ATTR         'cmode'
140	CALL_FUNCTION_0   None
143	POP_TOP           None

144	LOAD_FAST         'gl'
147	LOAD_ATTR         'pixmode'
150	LOAD_FAST         'GL'
153	LOAD_ATTR         'PM_SIZE'
156	LOAD_CONST        8
159	CALL_FUNCTION_2   None
162	POP_TOP           None

163	LOAD_FAST         'gl'
166	LOAD_ATTR         'gconfig'
169	CALL_FUNCTION_0   None
172	POP_TOP           None

173	SETUP_LOOP        '260'
176	LOAD_GLOBAL       'range'
179	LOAD_CONST        256
182	CALL_FUNCTION_1   None
185	GET_ITER          None
186	FOR_ITER          '217'
189	STORE_FAST        'i'

192	LOAD_FAST         'gl'
195	LOAD_ATTR         'mapcolor'
198	LOAD_FAST         'i'
201	LOAD_FAST         'i'
204	LOAD_FAST         'i'
207	LOAD_FAST         'i'
210	CALL_FUNCTION_4   None
213	POP_TOP           None
214	JUMP_BACK         '186'
217	POP_BLOCK         None
218_0	COME_FROM         '173'
218	JUMP_FORWARD      '260'

221	LOAD_FAST         'gl'
224	LOAD_ATTR         'RGBmode'
227	CALL_FUNCTION_0   None
230	POP_TOP           None

231	LOAD_FAST         'gl'
234	LOAD_ATTR         'pixmode'
237	LOAD_FAST         'GL'
240	LOAD_ATTR         'PM_SIZE'
243	LOAD_CONST        32
246	CALL_FUNCTION_2   None
249	POP_TOP           None

250	LOAD_FAST         'gl'
253	LOAD_ATTR         'gconfig'
256	CALL_FUNCTION_0   None
259	POP_TOP           None
260_0	COME_FROM         '218'

260	LOAD_FAST         'gl'
263	LOAD_ATTR         'qdevice'
266	LOAD_FAST         'DEVICE'
269	LOAD_ATTR         'REDRAW'
272	CALL_FUNCTION_1   None
275	POP_TOP           None

276	LOAD_FAST         'gl'
279	LOAD_ATTR         'qdevice'
282	LOAD_FAST         'DEVICE'
285	LOAD_ATTR         'ESCKEY'
288	CALL_FUNCTION_1   None
291	POP_TOP           None

292	LOAD_FAST         'gl'
295	LOAD_ATTR         'qdevice'
298	LOAD_FAST         'DEVICE'
301	LOAD_ATTR         'WINQUIT'
304	CALL_FUNCTION_1   None
307	POP_TOP           None

308	LOAD_FAST         'gl'
311	LOAD_ATTR         'qdevice'
314	LOAD_FAST         'DEVICE'
317	LOAD_ATTR         'WINSHUT'
320	CALL_FUNCTION_1   None
323	POP_TOP           None

324	LOAD_FAST         'gl'
327	LOAD_ATTR         'lrectwrite'
330	LOAD_CONST        0
333	LOAD_CONST        0
336	LOAD_FAST         'width'
339	LOAD_CONST        1
342	BINARY_SUBTRACT   None
343	LOAD_FAST         'height'
346	LOAD_CONST        1
349	BINARY_SUBTRACT   None
350	LOAD_FAST         'imgdata'
353	CALL_FUNCTION_5   None
356	POP_TOP           None

357	SETUP_LOOP        '467'

360	LOAD_FAST         'gl'
363	LOAD_ATTR         'qread'
366	CALL_FUNCTION_0   None
369	UNPACK_SEQUENCE_2 None
372	STORE_FAST        'dev'
375	STORE_FAST        'val'

378	LOAD_FAST         'dev'
381	LOAD_FAST         'DEVICE'
384	LOAD_ATTR         'ESCKEY'
387	LOAD_FAST         'DEVICE'
390	LOAD_ATTR         'WINSHUT'
393	LOAD_FAST         'DEVICE'
396	LOAD_ATTR         'WINQUIT'
399	BUILD_TUPLE_3     None
402	COMPARE_OP        'in'
405	POP_JUMP_IF_FALSE '412'

408	BREAK_LOOP        None
409	JUMP_FORWARD      '412'
412_0	COME_FROM         '409'

412	LOAD_FAST         'dev'
415	LOAD_FAST         'DEVICE'
418	LOAD_ATTR         'REDRAW'
421	COMPARE_OP        '=='
424	POP_JUMP_IF_FALSE '360'

427	LOAD_FAST         'gl'
430	LOAD_ATTR         'lrectwrite'
433	LOAD_CONST        0
436	LOAD_CONST        0
439	LOAD_FAST         'width'
442	LOAD_CONST        1
445	BINARY_SUBTRACT   None
446	LOAD_FAST         'height'
449	LOAD_CONST        1
452	BINARY_SUBTRACT   None
453	LOAD_FAST         'imgdata'
456	CALL_FUNCTION_5   None
459	POP_TOP           None
460	JUMP_BACK         '360'
463	JUMP_BACK         '360'
466	POP_BLOCK         None
467_0	COME_FROM         '357'

467	LOAD_FAST         'gl'
470	LOAD_ATTR         'winclose'
473	LOAD_FAST         'win'
476	CALL_FUNCTION_1   None
479	POP_TOP           None

480	LOAD_GLOBAL       'compress'
483	LOAD_FAST         'imgdata'
486	LOAD_FAST         'width'
489	LOAD_FAST         'height'
492	LOAD_FAST         'bytesperpixel'
495	CALL_FUNCTION_4   None
498	STORE_FAST        'newjpegdata'

501	LOAD_GLOBAL       'open'
504	LOAD_CONST        '/tmp/j.jpg'
507	LOAD_CONST        'w'
510	CALL_FUNCTION_2   None
513	LOAD_ATTR         'write'
516	LOAD_FAST         'newjpegdata'
519	CALL_FUNCTION_1   None
522	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 466