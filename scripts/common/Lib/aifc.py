# Embedded file name: scripts/common/Lib/aifc.py
--- This code section failed: ---

0	LOAD_CONST        'Stuff to parse AIFF-C and AIFF files.\n\nUnless explicitly stated otherwise, the description below is true\nboth for AIFF-C files and AIFF files.\n\nAn AIFF-C file has the following structure.\n\n  +-----------------+\n  | FORM            |\n  +-----------------+\n  | <size>          |\n  +----+------------+\n  |    | AIFC       |\n  |    +------------+\n  |    | <chunks>   |\n  |    |    .       |\n  |    |    .       |\n  |    |    .       |\n  +----+------------+\n\nAn AIFF file has the string "AIFF" instead of "AIFC".\n\nA chunk consists of an identifier (4 bytes) followed by a size (4 bytes,\nbig endian order), followed by the data.  The size field does not include\nthe size of the 8 byte header.\n\nThe following chunk types are recognized.\n\n  FVER\n      <version number of AIFF-C defining document> (AIFF-C only).\n  MARK\n      <# of markers> (2 bytes)\n      list of markers:\n          <marker ID> (2 bytes, must be > 0)\n          <position> (4 bytes)\n          <marker name> ("pstring")\n  COMM\n      <# of channels> (2 bytes)\n      <# of sound frames> (4 bytes)\n      <size of the samples> (2 bytes)\n      <sampling frequency> (10 bytes, IEEE 80-bit extended\n          floating point)\n      in AIFF-C files only:\n      <compression type> (4 bytes)\n      <human-readable version of compression type> ("pstring")\n  SSND\n      <offset> (4 bytes, not used by this program)\n      <blocksize> (4 bytes, not used by this program)\n      <sound data>\n\nA pstring consists of 1 byte length, a string of characters, and 0 or 1\nbyte pad to make the total length even.\n\nUsage.\n\nReading AIFF files:\n  f = aifc.open(file, \'r\')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods read(), seek(), and close().\nIn some types of audio files, if the setpos() method is not used,\nthe seek() method is not necessary.\n\nThis returns an instance of a class with the following public methods:\n  getnchannels()  -- returns number of audio channels (1 for\n             mono, 2 for stereo)\n  getsampwidth()  -- returns sample width in bytes\n  getframerate()  -- returns sampling frequency\n  getnframes()    -- returns number of audio frames\n  getcomptype()   -- returns compression type (\'NONE\' for AIFF files)\n  getcompname()   -- returns human-readable version of\n             compression type (\'not compressed\' for AIFF files)\n  getparams() -- returns a tuple consisting of all of the\n             above in the above order\n  getmarkers()    -- get the list of marks in the audio file or None\n             if there are no marks\n  getmark(id) -- get mark with the specified id (raises an error\n             if the mark does not exist)\n  readframes(n)   -- returns at most n frames of audio\n  rewind()    -- rewind to the beginning of the audio stream\n  setpos(pos) -- seek to the specified position\n  tell()      -- return the current position\n  close()     -- close the instance (make it unusable)\nThe position returned by tell(), the position given to setpos() and\nthe position of marks are all compatible and have nothing to do with\nthe actual position in the file.\nThe close() method is called automatically when the class instance\nis destroyed.\n\nWriting AIFF files:\n  f = aifc.open(file, \'w\')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods write(), tell(), seek(), and\nclose().\n\nThis returns an instance of a class with the following public methods:\n  aiff()      -- create an AIFF file (AIFF-C default)\n  aifc()      -- create an AIFF-C file\n  setnchannels(n) -- set the number of channels\n  setsampwidth(n) -- set the sample width\n  setframerate(n) -- set the frame rate\n  setnframes(n)   -- set the number of frames\n  setcomptype(type, name)\n          -- set the compression type and the\n             human-readable compression type\n  setparams(tuple)\n          -- set all parameters at once\n  setmark(id, pos, name)\n          -- add specified mark to the list of marks\n  tell()      -- return current position in output file (useful\n             in combination with setmark())\n  writeframesraw(data)\n          -- write audio frames without pathing up the\n             file header\n  writeframes(data)\n          -- write audio frames and patch up the file header\n  close()     -- patch up the file header and close the\n             output file\nYou should set the parameters before the first writeframesraw or\nwriteframes.  The total number of frames does not need to be set,\nbut when it is set to the correct value, the header does not have to\nbe patched up.\nIt is best to first set all parameters, perhaps possibly the\ncompression type, and then write audio frames using writeframesraw.\nWhen all frames have been written, either call writeframes(\'\') or\nclose() to patch up the sizes in the header.\nMarks can be added anytime.  If there are any marks, ypu must call\nclose() after all frames have been written.\nThe close() method is called automatically when the class instance\nis destroyed.\n\nWhen a file is opened with the extension \'.aiff\', an AIFF file is\nwritten, otherwise an AIFF-C file is written.  This default can be\nchanged by calling aiff() or aifc() before the first writeframes or\nwriteframesraw.\n'
3	STORE_NAME        '__doc__'

6	LOAD_CONST        -1
9	LOAD_CONST        None
12	IMPORT_NAME       'struct'
15	STORE_NAME        'struct'

18	LOAD_CONST        -1
21	LOAD_CONST        None
24	IMPORT_NAME       '__builtin__'
27	STORE_NAME        '__builtin__'

30	LOAD_CONST        'Error'
33	LOAD_CONST        'open'
36	LOAD_CONST        'openfp'
39	BUILD_LIST_3      None
42	STORE_NAME        '__all__'

45	LOAD_CONST        'Error'
48	LOAD_NAME         'Exception'
51	BUILD_TUPLE_1     None
54	LOAD_CONST        '<code_object Error>'
57	MAKE_FUNCTION_0   None
60	CALL_FUNCTION_0   None
63	BUILD_CLASS       None
64	STORE_NAME        'Error'

67	LOAD_CONST        2726318400L
70	STORE_NAME        '_AIFC_version'

73	LOAD_CONST        '<code_object _read_long>'
76	MAKE_FUNCTION_0   None
79	STORE_NAME        '_read_long'

82	LOAD_CONST        '<code_object _read_ulong>'
85	MAKE_FUNCTION_0   None
88	STORE_NAME        '_read_ulong'

91	LOAD_CONST        '<code_object _read_short>'
94	MAKE_FUNCTION_0   None
97	STORE_NAME        '_read_short'

100	LOAD_CONST        '<code_object _read_ushort>'
103	MAKE_FUNCTION_0   None
106	STORE_NAME        '_read_ushort'

109	LOAD_CONST        '<code_object _read_string>'
112	MAKE_FUNCTION_0   None
115	STORE_NAME        '_read_string'

118	LOAD_CONST        1.79769313486231e+308
121	STORE_NAME        '_HUGE_VAL'

124	LOAD_CONST        '<code_object _read_float>'
127	MAKE_FUNCTION_0   None
130	STORE_NAME        '_read_float'

133	LOAD_CONST        '<code_object _write_short>'
136	MAKE_FUNCTION_0   None
139	STORE_NAME        '_write_short'

142	LOAD_CONST        '<code_object _write_ushort>'
145	MAKE_FUNCTION_0   None
148	STORE_NAME        '_write_ushort'

151	LOAD_CONST        '<code_object _write_long>'
154	MAKE_FUNCTION_0   None
157	STORE_NAME        '_write_long'

160	LOAD_CONST        '<code_object _write_ulong>'
163	MAKE_FUNCTION_0   None
166	STORE_NAME        '_write_ulong'

169	LOAD_CONST        '<code_object _write_string>'
172	MAKE_FUNCTION_0   None
175	STORE_NAME        '_write_string'

178	LOAD_CONST        '<code_object _write_float>'
181	MAKE_FUNCTION_0   None
184	STORE_NAME        '_write_float'

187	LOAD_CONST        -1
190	LOAD_CONST        ('Chunk',)
193	IMPORT_NAME       'chunk'
196	IMPORT_FROM       'Chunk'
199	STORE_NAME        'Chunk'
202	POP_TOP           None

203	LOAD_CONST        'Aifc_read'
206	BUILD_TUPLE_0     None
209	LOAD_CONST        '<code_object Aifc_read>'
212	MAKE_FUNCTION_0   None
215	CALL_FUNCTION_0   None
218	BUILD_CLASS       None
219	STORE_NAME        'Aifc_read'

222	LOAD_CONST        'Aifc_write'
225	BUILD_TUPLE_0     None
228	LOAD_CONST        '<code_object Aifc_write>'
231	MAKE_FUNCTION_0   None
234	CALL_FUNCTION_0   None
237	BUILD_CLASS       None
238	STORE_NAME        'Aifc_write'

241	LOAD_NAME         'None'
244	LOAD_CONST        '<code_object open>'
247	MAKE_FUNCTION_1   None
250	STORE_NAME        'open'

253	LOAD_NAME         'open'
256	STORE_NAME        'openfp'

259	LOAD_NAME         '__name__'
262	LOAD_CONST        '__main__'
265	COMPARE_OP        '=='
268	POP_JUMP_IF_FALSE '589'

271	LOAD_CONST        -1
274	LOAD_CONST        None
277	IMPORT_NAME       'sys'
280	STORE_NAME        'sys'

283	LOAD_NAME         'sys'
286	LOAD_ATTR         'argv'
289	LOAD_CONST        1
292	SLICE+1           None
293	UNARY_NOT         None
294	POP_JUMP_IF_FALSE '316'

297	LOAD_NAME         'sys'
300	LOAD_ATTR         'argv'
303	LOAD_ATTR         'append'
306	LOAD_CONST        '/usr/demos/data/audio/bach.aiff'
309	CALL_FUNCTION_1   None
312	POP_TOP           None
313	JUMP_FORWARD      '316'
316_0	COME_FROM         '313'

316	LOAD_NAME         'sys'
319	LOAD_ATTR         'argv'
322	LOAD_CONST        1
325	BINARY_SUBSCR     None
326	STORE_NAME        'fn'

329	LOAD_NAME         'open'
332	LOAD_NAME         'fn'
335	LOAD_CONST        'r'
338	CALL_FUNCTION_2   None
341	STORE_NAME        'f'

344	LOAD_CONST        'Reading'
347	PRINT_ITEM        None
348	LOAD_NAME         'fn'
351	PRINT_ITEM_CONT   None
352	PRINT_NEWLINE_CONT None

353	LOAD_CONST        'nchannels ='
356	PRINT_ITEM        None
357	LOAD_NAME         'f'
360	LOAD_ATTR         'getnchannels'
363	CALL_FUNCTION_0   None
366	PRINT_ITEM_CONT   None
367	PRINT_NEWLINE_CONT None

368	LOAD_CONST        'nframes   ='
371	PRINT_ITEM        None
372	LOAD_NAME         'f'
375	LOAD_ATTR         'getnframes'
378	CALL_FUNCTION_0   None
381	PRINT_ITEM_CONT   None
382	PRINT_NEWLINE_CONT None

383	LOAD_CONST        'sampwidth ='
386	PRINT_ITEM        None
387	LOAD_NAME         'f'
390	LOAD_ATTR         'getsampwidth'
393	CALL_FUNCTION_0   None
396	PRINT_ITEM_CONT   None
397	PRINT_NEWLINE_CONT None

398	LOAD_CONST        'framerate ='
401	PRINT_ITEM        None
402	LOAD_NAME         'f'
405	LOAD_ATTR         'getframerate'
408	CALL_FUNCTION_0   None
411	PRINT_ITEM_CONT   None
412	PRINT_NEWLINE_CONT None

413	LOAD_CONST        'comptype  ='
416	PRINT_ITEM        None
417	LOAD_NAME         'f'
420	LOAD_ATTR         'getcomptype'
423	CALL_FUNCTION_0   None
426	PRINT_ITEM_CONT   None
427	PRINT_NEWLINE_CONT None

428	LOAD_CONST        'compname  ='
431	PRINT_ITEM        None
432	LOAD_NAME         'f'
435	LOAD_ATTR         'getcompname'
438	CALL_FUNCTION_0   None
441	PRINT_ITEM_CONT   None
442	PRINT_NEWLINE_CONT None

443	LOAD_NAME         'sys'
446	LOAD_ATTR         'argv'
449	LOAD_CONST        2
452	SLICE+1           None
453	POP_JUMP_IF_FALSE '586'

456	LOAD_NAME         'sys'
459	LOAD_ATTR         'argv'
462	LOAD_CONST        2
465	BINARY_SUBSCR     None
466	STORE_NAME        'gn'

469	LOAD_CONST        'Writing'
472	PRINT_ITEM        None
473	LOAD_NAME         'gn'
476	PRINT_ITEM_CONT   None
477	PRINT_NEWLINE_CONT None

478	LOAD_NAME         'open'
481	LOAD_NAME         'gn'
484	LOAD_CONST        'w'
487	CALL_FUNCTION_2   None
490	STORE_NAME        'g'

493	LOAD_NAME         'g'
496	LOAD_ATTR         'setparams'
499	LOAD_NAME         'f'
502	LOAD_ATTR         'getparams'
505	CALL_FUNCTION_0   None
508	CALL_FUNCTION_1   None
511	POP_TOP           None

512	SETUP_LOOP        '558'

515	LOAD_NAME         'f'
518	LOAD_ATTR         'readframes'
521	LOAD_CONST        1024
524	CALL_FUNCTION_1   None
527	STORE_NAME        'data'

530	LOAD_NAME         'data'
533	UNARY_NOT         None
534	POP_JUMP_IF_FALSE '541'

537	BREAK_LOOP        None
538	JUMP_FORWARD      '541'
541_0	COME_FROM         '538'

541	LOAD_NAME         'g'
544	LOAD_ATTR         'writeframes'
547	LOAD_NAME         'data'
550	CALL_FUNCTION_1   None
553	POP_TOP           None
554	JUMP_BACK         '515'
557	POP_BLOCK         None
558_0	COME_FROM         '512'

558	LOAD_NAME         'g'
561	LOAD_ATTR         'close'
564	CALL_FUNCTION_0   None
567	POP_TOP           None

568	LOAD_NAME         'f'
571	LOAD_ATTR         'close'
574	CALL_FUNCTION_0   None
577	POP_TOP           None

578	LOAD_CONST        'Done.'
581	PRINT_ITEM        None
582	PRINT_NEWLINE_CONT None
583	JUMP_FORWARD      '586'
586_0	COME_FROM         '583'
586	JUMP_FORWARD      '589'
589_0	COME_FROM         '586'

Syntax error at or near `POP_BLOCK' token at offset 557

