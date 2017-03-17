# Embedded file name: scripts/common/Lib/distutils/text_file.py
"""text_file

provides the TextFile class, which gives an interface to text files
that (optionally) takes care of stripping comments, ignoring blank
lines, and joining lines with backslashes."""
__revision__ = '$Id$'
import sys

class TextFile:
    """Provides a file-like object that takes care of all the things you
    commonly want to do when processing a text file that has some
    line-by-line syntax: strip comments (as long as "#" is your
    comment character), skip blank lines, join adjacent lines by
    escaping the newline (ie. backslash at end of line), strip
    leading and/or trailing whitespace.  All of these are optional
    and independently controllable.
    
    Provides a 'warn()' method so you can generate warning messages that
    report physical line number, even if the logical line in question
    spans multiple physical lines.  Also provides 'unreadline()' for
    implementing line-at-a-time lookahead.
    
    Constructor is called as:
    
        TextFile (filename=None, file=None, **options)
    
    It bombs (RuntimeError) if both 'filename' and 'file' are None;
    'filename' should be a string, and 'file' a file object (or
    something that provides 'readline()' and 'close()' methods).  It is
    recommended that you supply at least 'filename', so that TextFile
    can include it in warning messages.  If 'file' is not supplied,
    TextFile creates its own using the 'open()' builtin.
    
    The options are all boolean, and affect the value returned by
    'readline()':
      strip_comments [default: true]
        strip from "#" to end-of-line, as well as any whitespace
        leading up to the "#" -- unless it is escaped by a backslash
      lstrip_ws [default: false]
        strip leading whitespace from each line before returning it
      rstrip_ws [default: true]
        strip trailing whitespace (including line terminator!) from
        each line before returning it
      skip_blanks [default: true}
        skip lines that are empty *after* stripping comments and
        whitespace.  (If both lstrip_ws and rstrip_ws are false,
        then some lines may consist of solely whitespace: these will
        *not* be skipped, even if 'skip_blanks' is true.)
      join_lines [default: false]
        if a backslash is the last non-newline character on a line
        after stripping comments and whitespace, join the following line
        to it to form one "logical line"; if N consecutive lines end
        with a backslash, then N+1 physical lines will be joined to
        form one logical line.
      collapse_join [default: false]
        strip leading whitespace from lines that are joined to their
        predecessor; only matters if (join_lines and not lstrip_ws)
    
    Note that since 'rstrip_ws' can strip the trailing newline, the
    semantics of 'readline()' must differ from those of the builtin file
    object's 'readline()' method!  In particular, 'readline()' returns
    None for end-of-file: an empty string might just be a blank line (or
    an all-whitespace line), if 'rstrip_ws' is true but 'skip_blanks' is
    not."""
    default_options = {'strip_comments': 1,
     'skip_blanks': 1,
     'lstrip_ws': 0,
     'rstrip_ws': 1,
     'join_lines': 0,
     'collapse_join': 0}

    def __init__(self, filename = None, file = None, **options):
        """Construct a new TextFile object.  At least one of 'filename'
        (a string) and 'file' (a file-like object) must be supplied.
        They keyword argument options are described above and affect
        the values returned by 'readline()'."""
        if filename is None and file is None:
            raise RuntimeError, "you must supply either or both of 'filename' and 'file'"
        for opt in self.default_options.keys():
            if opt in options:
                setattr(self, opt, options[opt])
            else:
                setattr(self, opt, self.default_options[opt])

        for opt in options.keys():
            if opt not in self.default_options:
                raise KeyError, "invalid TextFile option '%s'" % opt

        if file is None:
            self.open(filename)
        else:
            self.filename = filename
            self.file = file
            self.current_line = 0
        self.linebuf = []
        return

    def open(self, filename):
        """Open a new file named 'filename'.  This overrides both the
        'filename' and 'file' arguments to the constructor."""
        self.filename = filename
        self.file = open(self.filename, 'r')
        self.current_line = 0

    def close(self):
        """Close the current file and forget everything we know about it
        (filename, current line number)."""
        self.file.close()
        self.file = None
        self.filename = None
        self.current_line = None
        return

    def gen_error(self, msg, line = None):
        outmsg = []
        if line is None:
            line = self.current_line
        outmsg.append(self.filename + ', ')
        if isinstance(line, (list, tuple)):
            outmsg.append('lines %d-%d: ' % tuple(line))
        else:
            outmsg.append('line %d: ' % line)
        outmsg.append(str(msg))
        return ''.join(outmsg)

    def error(self, msg, line = None):
        raise ValueError, 'error: ' + self.gen_error(msg, line)

    def warn(self, msg, line = None):
        """Print (to stderr) a warning message tied to the current logical
        line in the current file.  If the current logical line in the
        file spans multiple physical lines, the warning refers to the
        whole range, eg. "lines 3-5".  If 'line' supplied, it overrides
        the current line number; it may be a list or tuple to indicate a
        range of physical lines, or an integer for a single physical
        line."""
        sys.stderr.write('warning: ' + self.gen_error(msg, line) + '\n')

    def readline--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'linebuf'
6	POP_JUMP_IF_FALSE '36'

9	LOAD_FAST         'self'
12	LOAD_ATTR         'linebuf'
15	LOAD_CONST        -1
18	BINARY_SUBSCR     None
19	STORE_FAST        'line'

22	LOAD_FAST         'self'
25	LOAD_ATTR         'linebuf'
28	LOAD_CONST        -1
31	DELETE_SUBSCR     None

32	LOAD_FAST         'line'
35	RETURN_END_IF     None

36	LOAD_CONST        ''
39	STORE_FAST        'buildup_line'

42	SETUP_LOOP        '683'

45	LOAD_FAST         'self'
48	LOAD_ATTR         'file'
51	LOAD_ATTR         'readline'
54	CALL_FUNCTION_0   None
57	STORE_FAST        'line'

60	LOAD_FAST         'line'
63	LOAD_CONST        ''
66	COMPARE_OP        '=='
69	POP_JUMP_IF_FALSE '81'
72	LOAD_CONST        None
75	STORE_FAST        'line'
78	JUMP_FORWARD      '81'
81_0	COME_FROM         '78'

81	LOAD_FAST         'self'
84	LOAD_ATTR         'strip_comments'
87	POP_JUMP_IF_FALSE '251'
90	LOAD_FAST         'line'
93_0	COME_FROM         '87'
93	POP_JUMP_IF_FALSE '251'

96	LOAD_FAST         'line'
99	LOAD_ATTR         'find'
102	LOAD_CONST        '#'
105	CALL_FUNCTION_1   None
108	STORE_FAST        'pos'

111	LOAD_FAST         'pos'
114	LOAD_CONST        -1
117	COMPARE_OP        '=='
120	POP_JUMP_IF_FALSE '126'

123	JUMP_ABSOLUTE     '251'

126	LOAD_FAST         'pos'
129	LOAD_CONST        0
132	COMPARE_OP        '=='
135	POP_JUMP_IF_TRUE  '158'
138	LOAD_FAST         'line'
141	LOAD_FAST         'pos'
144	LOAD_CONST        1
147	BINARY_SUBTRACT   None
148	BINARY_SUBSCR     None
149	LOAD_CONST        '\\'
152	COMPARE_OP        '!='
155_0	COME_FROM         '135'
155	POP_JUMP_IF_FALSE '230'

158	LOAD_FAST         'line'
161	LOAD_CONST        -1
164	BINARY_SUBSCR     None
165	LOAD_CONST        '\n'
168	COMPARE_OP        '=='
171	POP_JUMP_IF_FALSE '180'
174	LOAD_CONST        '\n'
177_0	COME_FROM         '171'
177	JUMP_IF_TRUE_OR_POP '183'
180	LOAD_CONST        ''
183_0	COME_FROM         '177'
183	STORE_FAST        'eol'

186	LOAD_FAST         'line'
189	LOAD_CONST        0
192	LOAD_FAST         'pos'
195	SLICE+3           None
196	LOAD_FAST         'eol'
199	BINARY_ADD        None
200	STORE_FAST        'line'

203	LOAD_FAST         'line'
206	LOAD_ATTR         'strip'
209	CALL_FUNCTION_0   None
212	LOAD_CONST        ''
215	COMPARE_OP        '=='
218	POP_JUMP_IF_FALSE '248'

221	CONTINUE          '45'
224	JUMP_ABSOLUTE     '248'
227	JUMP_ABSOLUTE     '251'

230	LOAD_FAST         'line'
233	LOAD_ATTR         'replace'
236	LOAD_CONST        '\\#'
239	LOAD_CONST        '#'
242	CALL_FUNCTION_2   None
245	STORE_FAST        'line'
248	JUMP_FORWARD      '251'
251_0	COME_FROM         '248'

251	LOAD_FAST         'self'
254	LOAD_ATTR         'join_lines'
257	POP_JUMP_IF_FALSE '402'
260	LOAD_FAST         'buildup_line'
263_0	COME_FROM         '257'
263	POP_JUMP_IF_FALSE '402'

266	LOAD_FAST         'line'
269	LOAD_CONST        None
272	COMPARE_OP        'is'
275	POP_JUMP_IF_FALSE '295'

278	LOAD_FAST         'self'
281	LOAD_ATTR         'warn'
284	LOAD_CONST        'continuation line immediately precedes end-of-file'
287	CALL_FUNCTION_1   None
290	POP_TOP           None

291	LOAD_FAST         'buildup_line'
294	RETURN_END_IF     None

295	LOAD_FAST         'self'
298	LOAD_ATTR         'collapse_join'
301	POP_JUMP_IF_FALSE '319'

304	LOAD_FAST         'line'
307	LOAD_ATTR         'lstrip'
310	CALL_FUNCTION_0   None
313	STORE_FAST        'line'
316	JUMP_FORWARD      '319'
319_0	COME_FROM         '316'

319	LOAD_FAST         'buildup_line'
322	LOAD_FAST         'line'
325	BINARY_ADD        None
326	STORE_FAST        'line'

329	LOAD_GLOBAL       'isinstance'
332	LOAD_FAST         'self'
335	LOAD_ATTR         'current_line'
338	LOAD_GLOBAL       'list'
341	CALL_FUNCTION_2   None
344	POP_JUMP_IF_FALSE '374'

347	LOAD_FAST         'self'
350	LOAD_ATTR         'current_line'
353	LOAD_CONST        1
356	BINARY_SUBSCR     None
357	LOAD_CONST        1
360	BINARY_ADD        None
361	LOAD_FAST         'self'
364	LOAD_ATTR         'current_line'
367	LOAD_CONST        1
370	STORE_SUBSCR      None
371	JUMP_ABSOLUTE     '475'

374	LOAD_FAST         'self'
377	LOAD_ATTR         'current_line'

380	LOAD_FAST         'self'
383	LOAD_ATTR         'current_line'
386	LOAD_CONST        1
389	BINARY_ADD        None
390	BUILD_LIST_2      None
393	LOAD_FAST         'self'
396	STORE_ATTR        'current_line'
399	JUMP_FORWARD      '475'

402	LOAD_FAST         'line'
405	LOAD_CONST        None
408	COMPARE_OP        'is'
411	POP_JUMP_IF_FALSE '418'

414	LOAD_CONST        None
417	RETURN_END_IF     None

418	LOAD_GLOBAL       'isinstance'
421	LOAD_FAST         'self'
424	LOAD_ATTR         'current_line'
427	LOAD_GLOBAL       'list'
430	CALL_FUNCTION_2   None
433	POP_JUMP_IF_FALSE '459'

436	LOAD_FAST         'self'
439	LOAD_ATTR         'current_line'
442	LOAD_CONST        1
445	BINARY_SUBSCR     None
446	LOAD_CONST        1
449	BINARY_ADD        None
450	LOAD_FAST         'self'
453	STORE_ATTR        'current_line'
456	JUMP_FORWARD      '475'

459	LOAD_FAST         'self'
462	LOAD_ATTR         'current_line'
465	LOAD_CONST        1
468	BINARY_ADD        None
469	LOAD_FAST         'self'
472	STORE_ATTR        'current_line'
475_0	COME_FROM         '399'
475_1	COME_FROM         '456'

475	LOAD_FAST         'self'
478	LOAD_ATTR         'lstrip_ws'
481	POP_JUMP_IF_FALSE '508'
484	LOAD_FAST         'self'
487	LOAD_ATTR         'rstrip_ws'
490_0	COME_FROM         '481'
490	POP_JUMP_IF_FALSE '508'

493	LOAD_FAST         'line'
496	LOAD_ATTR         'strip'
499	CALL_FUNCTION_0   None
502	STORE_FAST        'line'
505	JUMP_FORWARD      '556'

508	LOAD_FAST         'self'
511	LOAD_ATTR         'lstrip_ws'
514	POP_JUMP_IF_FALSE '532'

517	LOAD_FAST         'line'
520	LOAD_ATTR         'lstrip'
523	CALL_FUNCTION_0   None
526	STORE_FAST        'line'
529	JUMP_FORWARD      '556'

532	LOAD_FAST         'self'
535	LOAD_ATTR         'rstrip_ws'
538	POP_JUMP_IF_FALSE '556'

541	LOAD_FAST         'line'
544	LOAD_ATTR         'rstrip'
547	CALL_FUNCTION_0   None
550	STORE_FAST        'line'
553	JUMP_FORWARD      '556'
556_0	COME_FROM         '505'
556_1	COME_FROM         '529'
556_2	COME_FROM         '553'

556	LOAD_FAST         'line'
559	LOAD_CONST        ''
562	COMPARE_OP        '=='
565	POP_JUMP_IF_TRUE  '580'
568	LOAD_FAST         'line'
571	LOAD_CONST        '\n'
574	COMPARE_OP        '=='
577_0	COME_FROM         '565'
577	POP_JUMP_IF_FALSE '595'
580	LOAD_FAST         'self'
583	LOAD_ATTR         'skip_blanks'
586_0	COME_FROM         '577'
586	POP_JUMP_IF_FALSE '595'

589	CONTINUE          '45'
592	JUMP_FORWARD      '595'
595_0	COME_FROM         '592'

595	LOAD_FAST         'self'
598	LOAD_ATTR         'join_lines'
601	POP_JUMP_IF_FALSE '678'

604	LOAD_FAST         'line'
607	LOAD_CONST        -1
610	BINARY_SUBSCR     None
611	LOAD_CONST        '\\'
614	COMPARE_OP        '=='
617	POP_JUMP_IF_FALSE '636'

620	LOAD_FAST         'line'
623	LOAD_CONST        -1
626	SLICE+2           None
627	STORE_FAST        'buildup_line'

630	CONTINUE          '45'
633	JUMP_FORWARD      '636'
636_0	COME_FROM         '633'

636	LOAD_FAST         'line'
639	LOAD_CONST        -2
642	SLICE+1           None
643	LOAD_CONST        '\\\n'
646	COMPARE_OP        '=='
649	POP_JUMP_IF_FALSE '678'

652	LOAD_FAST         'line'
655	LOAD_CONST        0
658	LOAD_CONST        -2
661	SLICE+3           None
662	LOAD_CONST        '\n'
665	BINARY_ADD        None
666	STORE_FAST        'buildup_line'

669	CONTINUE          '45'
672	JUMP_ABSOLUTE     '678'
675	JUMP_FORWARD      '678'
678_0	COME_FROM         '675'

678	LOAD_FAST         'line'
681	RETURN_VALUE      None
682	POP_BLOCK         None
683_0	COME_FROM         '42'
683	LOAD_CONST        None
686	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 682

    def readlines--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'lines'

6	SETUP_LOOP        '54'

9	LOAD_FAST         'self'
12	LOAD_ATTR         'readline'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'line'

21	LOAD_FAST         'line'
24	LOAD_CONST        None
27	COMPARE_OP        'is'
30	POP_JUMP_IF_FALSE '37'

33	LOAD_FAST         'lines'
36	RETURN_END_IF     None

37	LOAD_FAST         'lines'
40	LOAD_ATTR         'append'
43	LOAD_FAST         'line'
46	CALL_FUNCTION_1   None
49	POP_TOP           None
50	JUMP_BACK         '9'
53	POP_BLOCK         None
54_0	COME_FROM         '6'
54	LOAD_CONST        None
57	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 53

    def unreadline(self, line):
        """Push 'line' (a string) onto an internal buffer that will be
        checked by future 'readline()' calls.  Handy for implementing
        a parser with line-at-a-time lookahead."""
        self.linebuf.append(line)