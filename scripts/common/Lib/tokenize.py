# Embedded file name: scripts/common/Lib/tokenize.py
"""Tokenization help for Python programs.

generate_tokens(readline) is a generator that breaks a stream of
text into Python tokens.  It accepts a readline-like method which is called
repeatedly to get the next line of input (or "" for EOF).  It generates
5-tuples with these members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators

Older entry points
    tokenize_loop(readline, tokeneater)
    tokenize(readline, tokeneater=printtoken)
are the same, except instead of generating tokens, tokeneater is a callback
function to which the 5 fields described above are passed as 5 arguments,
each time a new token is found."""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger'
import string, re
from token import *
import token
__all__ = [ x for x in dir(token) if not x.startswith('_') ]
__all__ += ['COMMENT',
 'tokenize',
 'generate_tokens',
 'NL',
 'untokenize']
del x
del token
COMMENT = N_TOKENS
tok_name[COMMENT] = 'COMMENT'
NL = N_TOKENS + 1
tok_name[NL] = 'NL'
N_TOKENS += 2

def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '[a-zA-Z_]\\w*'
Hexnumber = '0[xX][\\da-fA-F]+[lL]?'
Octnumber = '(0[oO][0-7]+)|(0[0-7]*)[lL]?'
Binnumber = '0[bB][01]+[lL]?'
Decnumber = '[1-9]\\d*[lL]?'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?\\d+'
Pointfloat = group('\\d+\\.\\d*', '\\.\\d+') + maybe(Exponent)
Expfloat = '\\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('\\d+[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group("[uU]?[rR]?'''", '[uU]?[rR]?"""')
String = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '<>', '!=', '//=?', '[+\\-*/%&|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '[:;.,`@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
tokenprog, pseudoprog, single3prog, double3prog = map(re.compile, (Token,
 PseudoToken,
 Single3,
 Double3))
endprogs = {"'": re.compile(Single),
 '"': re.compile(Double),
 "'''": single3prog,
 '"""': double3prog,
 "r'''": single3prog,
 'r"""': double3prog,
 "u'''": single3prog,
 'u"""': double3prog,
 "ur'''": single3prog,
 'ur"""': double3prog,
 "R'''": single3prog,
 'R"""': double3prog,
 "U'''": single3prog,
 'U"""': double3prog,
 "uR'''": single3prog,
 'uR"""': double3prog,
 "Ur'''": single3prog,
 'Ur"""': double3prog,
 "UR'''": single3prog,
 'UR"""': double3prog,
 "b'''": single3prog,
 'b"""': double3prog,
 "br'''": single3prog,
 'br"""': double3prog,
 "B'''": single3prog,
 'B"""': double3prog,
 "bR'''": single3prog,
 'bR"""': double3prog,
 "Br'''": single3prog,
 'Br"""': double3prog,
 "BR'''": single3prog,
 'BR"""': double3prog,
 'r': None,
 'R': None,
 'u': None,
 'U': None,
 'b': None,
 'B': None}
triple_quoted = {}
for t in ("'''", '"""', "r'''", 'r"""', "R'''", 'R"""', "u'''", 'u"""', "U'''", 'U"""', "ur'''", 'ur"""', "Ur'''", 'Ur"""', "uR'''", 'uR"""', "UR'''", 'UR"""', "b'''", 'b"""', "B'''", 'B"""', "br'''", 'br"""', "Br'''", 'Br"""', "bR'''", 'bR"""', "BR'''", 'BR"""'):
    triple_quoted[t] = t

single_quoted = {}
for t in ("'", '"', "r'", 'r"', "R'", 'R"', "u'", 'u"', "U'", 'U"', "ur'", 'ur"', "Ur'", 'Ur"', "uR'", 'uR"', "UR'", 'UR"', "b'", 'b"', "B'", 'B"', "br'", 'br"', "Br'", 'Br"', "bR'", 'bR"', "BR'", 'BR"'):
    single_quoted[t] = t

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


def printtoken(type, token, srow_scol, erow_ecol, line):
    srow, scol = srow_scol
    erow, ecol = erow_ecol
    print '%d,%d-%d,%d:\t%s\t%s' % (srow,
     scol,
     erow,
     ecol,
     tok_name[type],
     repr(token))


def tokenize(readline, tokeneater = printtoken):
    """
    The tokenize() function accepts two parameters: one representing the
    input stream, and one providing an output mechanism for tokenize().
    
    The first parameter, readline, must be a callable object which provides
    the same interface as the readline() method of built-in file objects.
    Each call to the function should return one line of input as a string.
    
    The second parameter, tokeneater, must also be a callable object. It is
    called once for each token, with five arguments, corresponding to the
    tuples generated by generate_tokens().
    """
    try:
        tokenize_loop(readline, tokeneater)
    except StopTokenizing:
        pass


def tokenize_loop(readline, tokeneater):
    for token_info in generate_tokens(readline):
        tokeneater(*token_info)


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0

    def add_whitespace(self, start):
        row, col = start
        if not row <= self.prev_row:
            raise AssertionError
            col_offset = col - self.prev_col
            col_offset and self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        for t in iterable:
            if len(t) == 2:
                self.compat(t, iterable)
                break
            tok_type, token, start, end, line = t
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        startline = False
        indents = []
        toks_append = self.tokens.append
        toknum, tokval = token
        if toknum in (NAME, NUMBER):
            tokval += ' '
        if toknum in (NEWLINE, NL):
            startline = True
        prevstring = False
        for tok in iterable:
            toknum, tokval = tok[:2]
            if toknum in (NAME, NUMBER):
                tokval += ' '
            if toknum == STRING:
                if prevstring:
                    tokval = ' ' + tokval
                prevstring = True
            else:
                prevstring = False
            if toknum == INDENT:
                indents.append(tokval)
                continue
            elif toknum == DEDENT:
                indents.pop()
                continue
            elif toknum in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                toks_append(indents[-1])
                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    
    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.
    
    Round-trip invariant for full input:
        Untokenized source will match input source exactly
    
    Round-trip invariant for limited intput:
        # Output text will tokenize the back to the input
        t1 = [tok[:2] for tok in generate_tokens(f.readline)]
        newcode = untokenize(t1)
        readline = iter(newcode.splitlines(1)).next
        t2 = [tok[:2] for tok in generate_tokens(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    return ut.untokenize(iterable)


def generate_tokens--- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'lnum'
7	DUP_TOP           None
8	STORE_FAST        'parenlev'
11	STORE_FAST        'continued'

14	LOAD_GLOBAL       'string'
17	LOAD_ATTR         'ascii_letters'
20	LOAD_CONST        '_'
23	BINARY_ADD        None
24	LOAD_CONST        '0123456789'
27	ROT_TWO           None
28	STORE_FAST        'namechars'
31	STORE_FAST        'numchars'

34	LOAD_CONST        ('', 0)
37	UNPACK_SEQUENCE_2 None
40	STORE_FAST        'contstr'
43	STORE_FAST        'needcont'

46	LOAD_CONST        None
49	STORE_FAST        'contline'

52	LOAD_CONST        0
55	BUILD_LIST_1      None
58	STORE_FAST        'indents'

61	SETUP_LOOP        '1754'

64	SETUP_EXCEPT      '80'

67	LOAD_FAST         'readline'
70	CALL_FUNCTION_0   None
73	STORE_FAST        'line'
76	POP_BLOCK         None
77	JUMP_FORWARD      '103'
80_0	COME_FROM         '64'

80	DUP_TOP           None
81	LOAD_GLOBAL       'StopIteration'
84	COMPARE_OP        'exception match'
87	POP_JUMP_IF_FALSE '102'
90	POP_TOP           None
91	POP_TOP           None
92	POP_TOP           None

93	LOAD_CONST        ''
96	STORE_FAST        'line'
99	JUMP_FORWARD      '103'
102	END_FINALLY       None
103_0	COME_FROM         '77'
103_1	COME_FROM         '102'

103	LOAD_FAST         'lnum'
106	LOAD_CONST        1
109	INPLACE_ADD       None
110	STORE_FAST        'lnum'

113	LOAD_CONST        0
116	LOAD_GLOBAL       'len'
119	LOAD_FAST         'line'
122	CALL_FUNCTION_1   None
125	ROT_TWO           None
126	STORE_FAST        'pos'
129	STORE_FAST        'max'

132	LOAD_FAST         'contstr'
135	POP_JUMP_IF_FALSE '379'

138	LOAD_FAST         'line'
141	POP_JUMP_IF_TRUE  '162'

144	LOAD_GLOBAL       'TokenError'
147	LOAD_CONST        'EOF in multi-line string'
150	LOAD_FAST         'strstart'
153	BUILD_TUPLE_2     None
156	RAISE_VARARGS_2   None
159	JUMP_FORWARD      '162'
162_0	COME_FROM         '159'

162	LOAD_FAST         'endprog'
165	LOAD_ATTR         'match'
168	LOAD_FAST         'line'
171	CALL_FUNCTION_1   None
174	STORE_FAST        'endmatch'

177	LOAD_FAST         'endmatch'
180	POP_JUMP_IF_FALSE '261'

183	LOAD_FAST         'endmatch'
186	LOAD_ATTR         'end'
189	LOAD_CONST        0
192	CALL_FUNCTION_1   None
195	DUP_TOP           None
196	STORE_FAST        'pos'
199	STORE_FAST        'end'

202	LOAD_GLOBAL       'STRING'
205	LOAD_FAST         'contstr'
208	LOAD_FAST         'line'
211	LOAD_FAST         'end'
214	SLICE+2           None
215	BINARY_ADD        None

216	LOAD_FAST         'strstart'
219	LOAD_FAST         'lnum'
222	LOAD_FAST         'end'
225	BUILD_TUPLE_2     None
228	LOAD_FAST         'contline'
231	LOAD_FAST         'line'
234	BINARY_ADD        None
235	BUILD_TUPLE_5     None
238	YIELD_VALUE       None
239	POP_TOP           None

240	LOAD_CONST        ('', 0)
243	UNPACK_SEQUENCE_2 None
246	STORE_FAST        'contstr'
249	STORE_FAST        'needcont'

252	LOAD_CONST        None
255	STORE_FAST        'contline'
258	JUMP_ABSOLUTE     '987'

261	LOAD_FAST         'needcont'
264	POP_JUMP_IF_FALSE '353'
267	LOAD_FAST         'line'
270	LOAD_CONST        -2
273	SLICE+1           None
274	LOAD_CONST        '\\\n'
277	COMPARE_OP        '!='
280	POP_JUMP_IF_FALSE '353'
283	LOAD_FAST         'line'
286	LOAD_CONST        -3
289	SLICE+1           None
290	LOAD_CONST        '\\\r\n'
293	COMPARE_OP        '!='
296_0	COME_FROM         '264'
296_1	COME_FROM         '280'
296	POP_JUMP_IF_FALSE '353'

299	LOAD_GLOBAL       'ERRORTOKEN'
302	LOAD_FAST         'contstr'
305	LOAD_FAST         'line'
308	BINARY_ADD        None

309	LOAD_FAST         'strstart'
312	LOAD_FAST         'lnum'
315	LOAD_GLOBAL       'len'
318	LOAD_FAST         'line'
321	CALL_FUNCTION_1   None
324	BUILD_TUPLE_2     None
327	LOAD_FAST         'contline'
330	BUILD_TUPLE_5     None
333	YIELD_VALUE       None
334	POP_TOP           None

335	LOAD_CONST        ''
338	STORE_FAST        'contstr'

341	LOAD_CONST        None
344	STORE_FAST        'contline'

347	CONTINUE          '64'
350	JUMP_ABSOLUTE     '987'

353	LOAD_FAST         'contstr'
356	LOAD_FAST         'line'
359	BINARY_ADD        None
360	STORE_FAST        'contstr'

363	LOAD_FAST         'contline'
366	LOAD_FAST         'line'
369	BINARY_ADD        None
370	STORE_FAST        'contline'

373	CONTINUE          '64'
376	JUMP_FORWARD      '987'

379	LOAD_FAST         'parenlev'
382	LOAD_CONST        0
385	COMPARE_OP        '=='
388	POP_JUMP_IF_FALSE '951'
391	LOAD_FAST         'continued'
394	UNARY_NOT         None
395_0	COME_FROM         '388'
395	POP_JUMP_IF_FALSE '951'

398	LOAD_FAST         'line'
401	POP_JUMP_IF_TRUE  '408'
404	BREAK_LOOP        None
405	JUMP_FORWARD      '408'
408_0	COME_FROM         '405'

408	LOAD_CONST        0
411	STORE_FAST        'column'

414	SETUP_LOOP        '535'
417	LOAD_FAST         'pos'
420	LOAD_FAST         'max'
423	COMPARE_OP        '<'
426	POP_JUMP_IF_FALSE '534'

429	LOAD_FAST         'line'
432	LOAD_FAST         'pos'
435	BINARY_SUBSCR     None
436	LOAD_CONST        ' '
439	COMPARE_OP        '=='
442	POP_JUMP_IF_FALSE '458'

445	LOAD_FAST         'column'
448	LOAD_CONST        1
451	INPLACE_ADD       None
452	STORE_FAST        'column'
455	JUMP_FORWARD      '521'

458	LOAD_FAST         'line'
461	LOAD_FAST         'pos'
464	BINARY_SUBSCR     None
465	LOAD_CONST        '\t'
468	COMPARE_OP        '=='
471	POP_JUMP_IF_FALSE '495'

474	LOAD_FAST         'column'
477	LOAD_GLOBAL       'tabsize'
480	BINARY_FLOOR_DIVIDE None
481	LOAD_CONST        1
484	BINARY_ADD        None
485	LOAD_GLOBAL       'tabsize'
488	BINARY_MULTIPLY   None
489	STORE_FAST        'column'
492	JUMP_FORWARD      '521'

495	LOAD_FAST         'line'
498	LOAD_FAST         'pos'
501	BINARY_SUBSCR     None
502	LOAD_CONST        '\x0c'
505	COMPARE_OP        '=='
508	POP_JUMP_IF_FALSE '520'

511	LOAD_CONST        0
514	STORE_FAST        'column'
517	JUMP_FORWARD      '521'

520	BREAK_LOOP        None
521_0	COME_FROM         '455'
521_1	COME_FROM         '492'
521_2	COME_FROM         '517'

521	LOAD_FAST         'pos'
524	LOAD_CONST        1
527	INPLACE_ADD       None
528	STORE_FAST        'pos'
531	JUMP_BACK         '417'
534	POP_BLOCK         None
535_0	COME_FROM         '414'

535	LOAD_FAST         'pos'
538	LOAD_FAST         'max'
541	COMPARE_OP        '=='
544	POP_JUMP_IF_FALSE '551'

547	BREAK_LOOP        None
548	JUMP_FORWARD      '551'
551_0	COME_FROM         '548'

551	LOAD_FAST         'line'
554	LOAD_FAST         'pos'
557	BINARY_SUBSCR     None
558	LOAD_CONST        '#\r\n'
561	COMPARE_OP        'in'
564	POP_JUMP_IF_FALSE '773'

567	LOAD_FAST         'line'
570	LOAD_FAST         'pos'
573	BINARY_SUBSCR     None
574	LOAD_CONST        '#'
577	COMPARE_OP        '=='
580	POP_JUMP_IF_FALSE '705'

583	LOAD_FAST         'line'
586	LOAD_FAST         'pos'
589	SLICE+1           None
590	LOAD_ATTR         'rstrip'
593	LOAD_CONST        '\r\n'
596	CALL_FUNCTION_1   None
599	STORE_FAST        'comment_token'

602	LOAD_FAST         'pos'
605	LOAD_GLOBAL       'len'
608	LOAD_FAST         'comment_token'
611	CALL_FUNCTION_1   None
614	BINARY_ADD        None
615	STORE_FAST        'nl_pos'

618	LOAD_GLOBAL       'COMMENT'
621	LOAD_FAST         'comment_token'

624	LOAD_FAST         'lnum'
627	LOAD_FAST         'pos'
630	BUILD_TUPLE_2     None
633	LOAD_FAST         'lnum'
636	LOAD_FAST         'pos'
639	LOAD_GLOBAL       'len'
642	LOAD_FAST         'comment_token'
645	CALL_FUNCTION_1   None
648	BINARY_ADD        None
649	BUILD_TUPLE_2     None
652	LOAD_FAST         'line'
655	BUILD_TUPLE_5     None
658	YIELD_VALUE       None
659	POP_TOP           None

660	LOAD_GLOBAL       'NL'
663	LOAD_FAST         'line'
666	LOAD_FAST         'nl_pos'
669	SLICE+1           None

670	LOAD_FAST         'lnum'
673	LOAD_FAST         'nl_pos'
676	BUILD_TUPLE_2     None
679	LOAD_FAST         'lnum'
682	LOAD_GLOBAL       'len'
685	LOAD_FAST         'line'
688	CALL_FUNCTION_1   None
691	BUILD_TUPLE_2     None
694	LOAD_FAST         'line'
697	BUILD_TUPLE_5     None
700	YIELD_VALUE       None
701	POP_TOP           None
702	JUMP_BACK         '64'

705	LOAD_GLOBAL       'NL'
708	LOAD_GLOBAL       'COMMENT'
711	BUILD_TUPLE_2     None
714	LOAD_FAST         'line'
717	LOAD_FAST         'pos'
720	BINARY_SUBSCR     None
721	LOAD_CONST        '#'
724	COMPARE_OP        '=='
727	BINARY_SUBSCR     None
728	LOAD_FAST         'line'
731	LOAD_FAST         'pos'
734	SLICE+1           None

735	LOAD_FAST         'lnum'
738	LOAD_FAST         'pos'
741	BUILD_TUPLE_2     None
744	LOAD_FAST         'lnum'
747	LOAD_GLOBAL       'len'
750	LOAD_FAST         'line'
753	CALL_FUNCTION_1   None
756	BUILD_TUPLE_2     None
759	LOAD_FAST         'line'
762	BUILD_TUPLE_5     None
765	YIELD_VALUE       None
766	POP_TOP           None

767	CONTINUE          '64'
770	JUMP_FORWARD      '773'
773_0	COME_FROM         '770'

773	LOAD_FAST         'column'
776	LOAD_FAST         'indents'
779	LOAD_CONST        -1
782	BINARY_SUBSCR     None
783	COMPARE_OP        '>'
786	POP_JUMP_IF_FALSE '841'

789	LOAD_FAST         'indents'
792	LOAD_ATTR         'append'
795	LOAD_FAST         'column'
798	CALL_FUNCTION_1   None
801	POP_TOP           None

802	LOAD_GLOBAL       'INDENT'
805	LOAD_FAST         'line'
808	LOAD_FAST         'pos'
811	SLICE+2           None
812	LOAD_FAST         'lnum'
815	LOAD_CONST        0
818	BUILD_TUPLE_2     None
821	LOAD_FAST         'lnum'
824	LOAD_FAST         'pos'
827	BUILD_TUPLE_2     None
830	LOAD_FAST         'line'
833	BUILD_TUPLE_5     None
836	YIELD_VALUE       None
837	POP_TOP           None
838	JUMP_FORWARD      '841'
841_0	COME_FROM         '838'

841	SETUP_LOOP        '987'
844	LOAD_FAST         'column'
847	LOAD_FAST         'indents'
850	LOAD_CONST        -1
853	BINARY_SUBSCR     None
854	COMPARE_OP        '<'
857	POP_JUMP_IF_FALSE '947'

860	LOAD_FAST         'column'
863	LOAD_FAST         'indents'
866	COMPARE_OP        'not in'
869	POP_JUMP_IF_FALSE '902'

872	LOAD_GLOBAL       'IndentationError'

875	LOAD_CONST        'unindent does not match any outer indentation level'

878	LOAD_CONST        '<tokenize>'
881	LOAD_FAST         'lnum'
884	LOAD_FAST         'pos'
887	LOAD_FAST         'line'
890	BUILD_TUPLE_4     None
893	CALL_FUNCTION_2   None
896	RAISE_VARARGS_1   None
899	JUMP_FORWARD      '902'
902_0	COME_FROM         '899'

902	LOAD_FAST         'indents'
905	LOAD_CONST        -1
908	SLICE+2           None
909	STORE_FAST        'indents'

912	LOAD_GLOBAL       'DEDENT'
915	LOAD_CONST        ''
918	LOAD_FAST         'lnum'
921	LOAD_FAST         'pos'
924	BUILD_TUPLE_2     None
927	LOAD_FAST         'lnum'
930	LOAD_FAST         'pos'
933	BUILD_TUPLE_2     None
936	LOAD_FAST         'line'
939	BUILD_TUPLE_5     None
942	YIELD_VALUE       None
943	POP_TOP           None
944	JUMP_BACK         '844'
947	POP_BLOCK         None
948_0	COME_FROM         '841'
948	JUMP_FORWARD      '987'

951	LOAD_FAST         'line'
954	POP_JUMP_IF_TRUE  '981'

957	LOAD_GLOBAL       'TokenError'
960	LOAD_CONST        'EOF in multi-line statement'
963	LOAD_FAST         'lnum'
966	LOAD_CONST        0
969	BUILD_TUPLE_2     None
972	BUILD_TUPLE_2     None
975	RAISE_VARARGS_2   None
978	JUMP_FORWARD      '981'
981_0	COME_FROM         '978'

981	LOAD_CONST        0
984	STORE_FAST        'continued'
987_0	COME_FROM         '376'
987_1	COME_FROM         '948'

987	SETUP_LOOP        '1750'
990	LOAD_FAST         'pos'
993	LOAD_FAST         'max'
996	COMPARE_OP        '<'
999	POP_JUMP_IF_FALSE '1749'

1002	LOAD_GLOBAL       'pseudoprog'
1005	LOAD_ATTR         'match'
1008	LOAD_FAST         'line'
1011	LOAD_FAST         'pos'
1014	CALL_FUNCTION_2   None
1017	STORE_FAST        'pseudomatch'

1020	LOAD_FAST         'pseudomatch'
1023	POP_JUMP_IF_FALSE '1696'

1026	LOAD_FAST         'pseudomatch'
1029	LOAD_ATTR         'span'
1032	LOAD_CONST        1
1035	CALL_FUNCTION_1   None
1038	UNPACK_SEQUENCE_2 None
1041	STORE_FAST        'start'
1044	STORE_FAST        'end'

1047	LOAD_FAST         'lnum'
1050	LOAD_FAST         'start'
1053	BUILD_TUPLE_2     None
1056	LOAD_FAST         'lnum'
1059	LOAD_FAST         'end'
1062	BUILD_TUPLE_2     None
1065	LOAD_FAST         'end'
1068	ROT_THREE         None
1069	ROT_TWO           None
1070	STORE_FAST        'spos'
1073	STORE_FAST        'epos'
1076	STORE_FAST        'pos'

1079	LOAD_FAST         'line'
1082	LOAD_FAST         'start'
1085	LOAD_FAST         'end'
1088	SLICE+3           None
1089	LOAD_FAST         'line'
1092	LOAD_FAST         'start'
1095	BINARY_SUBSCR     None
1096	ROT_TWO           None
1097	STORE_FAST        'token'
1100	STORE_FAST        'initial'

1103	LOAD_FAST         'initial'
1106	LOAD_FAST         'numchars'
1109	COMPARE_OP        'in'
1112	POP_JUMP_IF_TRUE  '1139'

1115	LOAD_FAST         'initial'
1118	LOAD_CONST        '.'
1121	COMPARE_OP        '=='
1124	POP_JUMP_IF_FALSE '1162'
1127	LOAD_FAST         'token'
1130	LOAD_CONST        '.'
1133	COMPARE_OP        '!='
1136_0	COME_FROM         '1112'
1136_1	COME_FROM         '1124'
1136	POP_JUMP_IF_FALSE '1162'

1139	LOAD_GLOBAL       'NUMBER'
1142	LOAD_FAST         'token'
1145	LOAD_FAST         'spos'
1148	LOAD_FAST         'epos'
1151	LOAD_FAST         'line'
1154	BUILD_TUPLE_5     None
1157	YIELD_VALUE       None
1158	POP_TOP           None
1159	JUMP_ABSOLUTE     '1746'

1162	LOAD_FAST         'initial'
1165	LOAD_CONST        '\r\n'
1168	COMPARE_OP        'in'
1171	POP_JUMP_IF_FALSE '1215'

1174	LOAD_FAST         'parenlev'
1177	LOAD_CONST        0
1180	COMPARE_OP        '>'
1183	POP_JUMP_IF_FALSE '1192'
1186	LOAD_GLOBAL       'NL'
1189	JUMP_FORWARD      '1195'
1192	LOAD_GLOBAL       'NEWLINE'
1195_0	COME_FROM         '1189'

1195	LOAD_FAST         'token'
1198	LOAD_FAST         'spos'
1201	LOAD_FAST         'epos'
1204	LOAD_FAST         'line'
1207	BUILD_TUPLE_5     None
1210	YIELD_VALUE       None
1211	POP_TOP           None
1212	JUMP_ABSOLUTE     '1746'

1215	LOAD_FAST         'initial'
1218	LOAD_CONST        '#'
1221	COMPARE_OP        '=='
1224	POP_JUMP_IF_FALSE '1272'

1227	LOAD_FAST         'token'
1230	LOAD_ATTR         'endswith'
1233	LOAD_CONST        '\n'
1236	CALL_FUNCTION_1   None
1239	UNARY_NOT         None
1240	POP_JUMP_IF_TRUE  '1249'
1243	LOAD_ASSERT       'AssertionError'
1246	RAISE_VARARGS_1   None

1249	LOAD_GLOBAL       'COMMENT'
1252	LOAD_FAST         'token'
1255	LOAD_FAST         'spos'
1258	LOAD_FAST         'epos'
1261	LOAD_FAST         'line'
1264	BUILD_TUPLE_5     None
1267	YIELD_VALUE       None
1268	POP_TOP           None
1269	JUMP_ABSOLUTE     '1746'

1272	LOAD_FAST         'token'
1275	LOAD_GLOBAL       'triple_quoted'
1278	COMPARE_OP        'in'
1281	POP_JUMP_IF_FALSE '1407'

1284	LOAD_GLOBAL       'endprogs'
1287	LOAD_FAST         'token'
1290	BINARY_SUBSCR     None
1291	STORE_FAST        'endprog'

1294	LOAD_FAST         'endprog'
1297	LOAD_ATTR         'match'
1300	LOAD_FAST         'line'
1303	LOAD_FAST         'pos'
1306	CALL_FUNCTION_2   None
1309	STORE_FAST        'endmatch'

1312	LOAD_FAST         'endmatch'
1315	POP_JUMP_IF_FALSE '1375'

1318	LOAD_FAST         'endmatch'
1321	LOAD_ATTR         'end'
1324	LOAD_CONST        0
1327	CALL_FUNCTION_1   None
1330	STORE_FAST        'pos'

1333	LOAD_FAST         'line'
1336	LOAD_FAST         'start'
1339	LOAD_FAST         'pos'
1342	SLICE+3           None
1343	STORE_FAST        'token'

1346	LOAD_GLOBAL       'STRING'
1349	LOAD_FAST         'token'
1352	LOAD_FAST         'spos'
1355	LOAD_FAST         'lnum'
1358	LOAD_FAST         'pos'
1361	BUILD_TUPLE_2     None
1364	LOAD_FAST         'line'
1367	BUILD_TUPLE_5     None
1370	YIELD_VALUE       None
1371	POP_TOP           None
1372	JUMP_ABSOLUTE     '1693'

1375	LOAD_FAST         'lnum'
1378	LOAD_FAST         'start'
1381	BUILD_TUPLE_2     None
1384	STORE_FAST        'strstart'

1387	LOAD_FAST         'line'
1390	LOAD_FAST         'start'
1393	SLICE+1           None
1394	STORE_FAST        'contstr'

1397	LOAD_FAST         'line'
1400	STORE_FAST        'contline'

1403	BREAK_LOOP        None
1404	JUMP_ABSOLUTE     '1746'

1407	LOAD_FAST         'initial'
1410	LOAD_GLOBAL       'single_quoted'
1413	COMPARE_OP        'in'
1416	POP_JUMP_IF_TRUE  '1451'

1419	LOAD_FAST         'token'
1422	LOAD_CONST        2
1425	SLICE+2           None
1426	LOAD_GLOBAL       'single_quoted'
1429	COMPARE_OP        'in'
1432	POP_JUMP_IF_TRUE  '1451'

1435	LOAD_FAST         'token'
1438	LOAD_CONST        3
1441	SLICE+2           None
1442	LOAD_GLOBAL       'single_quoted'
1445	COMPARE_OP        'in'
1448_0	COME_FROM         '1416'
1448_1	COME_FROM         '1432'
1448	POP_JUMP_IF_FALSE '1567'

1451	LOAD_FAST         'token'
1454	LOAD_CONST        -1
1457	BINARY_SUBSCR     None
1458	LOAD_CONST        '\n'
1461	COMPARE_OP        '=='
1464	POP_JUMP_IF_FALSE '1544'

1467	LOAD_FAST         'lnum'
1470	LOAD_FAST         'start'
1473	BUILD_TUPLE_2     None
1476	STORE_FAST        'strstart'

1479	LOAD_GLOBAL       'endprogs'
1482	LOAD_FAST         'initial'
1485	BINARY_SUBSCR     None
1486	JUMP_IF_TRUE_OR_POP '1514'
1489	LOAD_GLOBAL       'endprogs'
1492	LOAD_FAST         'token'
1495	LOAD_CONST        1
1498	BINARY_SUBSCR     None
1499	BINARY_SUBSCR     None
1500	JUMP_IF_TRUE_OR_POP '1514'

1503	LOAD_GLOBAL       'endprogs'
1506	LOAD_FAST         'token'
1509	LOAD_CONST        2
1512	BINARY_SUBSCR     None
1513	BINARY_SUBSCR     None
1514_0	COME_FROM         '1486'
1514_1	COME_FROM         '1500'
1514	STORE_FAST        'endprog'

1517	LOAD_FAST         'line'
1520	LOAD_FAST         'start'
1523	SLICE+1           None
1524	LOAD_CONST        1
1527	ROT_TWO           None
1528	STORE_FAST        'contstr'
1531	STORE_FAST        'needcont'

1534	LOAD_FAST         'line'
1537	STORE_FAST        'contline'

1540	BREAK_LOOP        None
1541	JUMP_ABSOLUTE     '1693'

1544	LOAD_GLOBAL       'STRING'
1547	LOAD_FAST         'token'
1550	LOAD_FAST         'spos'
1553	LOAD_FAST         'epos'
1556	LOAD_FAST         'line'
1559	BUILD_TUPLE_5     None
1562	YIELD_VALUE       None
1563	POP_TOP           None
1564	JUMP_ABSOLUTE     '1746'

1567	LOAD_FAST         'initial'
1570	LOAD_FAST         'namechars'
1573	COMPARE_OP        'in'
1576	POP_JUMP_IF_FALSE '1602'

1579	LOAD_GLOBAL       'NAME'
1582	LOAD_FAST         'token'
1585	LOAD_FAST         'spos'
1588	LOAD_FAST         'epos'
1591	LOAD_FAST         'line'
1594	BUILD_TUPLE_5     None
1597	YIELD_VALUE       None
1598	POP_TOP           None
1599	JUMP_ABSOLUTE     '1746'

1602	LOAD_FAST         'initial'
1605	LOAD_CONST        '\\'
1608	COMPARE_OP        '=='
1611	POP_JUMP_IF_FALSE '1623'

1614	LOAD_CONST        1
1617	STORE_FAST        'continued'
1620	JUMP_ABSOLUTE     '1746'

1623	LOAD_FAST         'initial'
1626	LOAD_CONST        '([{'
1629	COMPARE_OP        'in'
1632	POP_JUMP_IF_FALSE '1648'

1635	LOAD_FAST         'parenlev'
1638	LOAD_CONST        1
1641	INPLACE_ADD       None
1642	STORE_FAST        'parenlev'
1645	JUMP_FORWARD      '1673'

1648	LOAD_FAST         'initial'
1651	LOAD_CONST        ')]}'
1654	COMPARE_OP        'in'
1657	POP_JUMP_IF_FALSE '1673'

1660	LOAD_FAST         'parenlev'
1663	LOAD_CONST        1
1666	INPLACE_SUBTRACT  None
1667	STORE_FAST        'parenlev'
1670	JUMP_FORWARD      '1673'
1673_0	COME_FROM         '1645'
1673_1	COME_FROM         '1670'

1673	LOAD_GLOBAL       'OP'
1676	LOAD_FAST         'token'
1679	LOAD_FAST         'spos'
1682	LOAD_FAST         'epos'
1685	LOAD_FAST         'line'
1688	BUILD_TUPLE_5     None
1691	YIELD_VALUE       None
1692	POP_TOP           None
1693	JUMP_BACK         '990'

1696	LOAD_GLOBAL       'ERRORTOKEN'
1699	LOAD_FAST         'line'
1702	LOAD_FAST         'pos'
1705	BINARY_SUBSCR     None

1706	LOAD_FAST         'lnum'
1709	LOAD_FAST         'pos'
1712	BUILD_TUPLE_2     None
1715	LOAD_FAST         'lnum'
1718	LOAD_FAST         'pos'
1721	LOAD_CONST        1
1724	BINARY_ADD        None
1725	BUILD_TUPLE_2     None
1728	LOAD_FAST         'line'
1731	BUILD_TUPLE_5     None
1734	YIELD_VALUE       None
1735	POP_TOP           None

1736	LOAD_FAST         'pos'
1739	LOAD_CONST        1
1742	INPLACE_ADD       None
1743	STORE_FAST        'pos'
1746	JUMP_BACK         '990'
1749	POP_BLOCK         None
1750_0	COME_FROM         '987'
1750	JUMP_BACK         '64'
1753	POP_BLOCK         None
1754_0	COME_FROM         '61'

1754	SETUP_LOOP        '1807'
1757	LOAD_FAST         'indents'
1760	LOAD_CONST        1
1763	SLICE+1           None
1764	GET_ITER          None
1765	FOR_ITER          '1806'
1768	STORE_FAST        'indent'

1771	LOAD_GLOBAL       'DEDENT'
1774	LOAD_CONST        ''
1777	LOAD_FAST         'lnum'
1780	LOAD_CONST        0
1783	BUILD_TUPLE_2     None
1786	LOAD_FAST         'lnum'
1789	LOAD_CONST        0
1792	BUILD_TUPLE_2     None
1795	LOAD_CONST        ''
1798	BUILD_TUPLE_5     None
1801	YIELD_VALUE       None
1802	POP_TOP           None
1803	JUMP_BACK         '1765'
1806	POP_BLOCK         None
1807_0	COME_FROM         '1754'

1807	LOAD_GLOBAL       'ENDMARKER'
1810	LOAD_CONST        ''
1813	LOAD_FAST         'lnum'
1816	LOAD_CONST        0
1819	BUILD_TUPLE_2     None
1822	LOAD_FAST         'lnum'
1825	LOAD_CONST        0
1828	BUILD_TUPLE_2     None
1831	LOAD_CONST        ''
1834	BUILD_TUPLE_5     None
1837	YIELD_VALUE       None
1838	POP_TOP           None
1839	LOAD_CONST        None
1842	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 1753


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tokenize(open(sys.argv[1]).readline)
    else:
        tokenize(sys.stdin.readline)