# Embedded file name: scripts/common/Lib/shlex.py
--- This code section failed: ---

0	LOAD_CONST        'A lexical analyzer class for simple shell-like syntaxes.'
3	STORE_NAME        '__doc__'

6	LOAD_CONST        -1
9	LOAD_CONST        None
12	IMPORT_NAME       'os.path'
15	STORE_NAME        'os'

18	LOAD_CONST        -1
21	LOAD_CONST        None
24	IMPORT_NAME       'sys'
27	STORE_NAME        'sys'

30	LOAD_CONST        -1
33	LOAD_CONST        ('deque',)
36	IMPORT_NAME       'collections'
39	IMPORT_FROM       'deque'
42	STORE_NAME        'deque'
45	POP_TOP           None

46	SETUP_EXCEPT      '69'

49	LOAD_CONST        -1
52	LOAD_CONST        ('StringIO',)
55	IMPORT_NAME       'cStringIO'
58	IMPORT_FROM       'StringIO'
61	STORE_NAME        'StringIO'
64	POP_TOP           None
65	POP_BLOCK         None
66	JUMP_FORWARD      '102'
69_0	COME_FROM         '46'

69	DUP_TOP           None
70	LOAD_NAME         'ImportError'
73	COMPARE_OP        'exception match'
76	POP_JUMP_IF_FALSE '101'
79	POP_TOP           None
80	POP_TOP           None
81	POP_TOP           None

82	LOAD_CONST        -1
85	LOAD_CONST        ('StringIO',)
88	IMPORT_NAME       'StringIO'
91	IMPORT_FROM       'StringIO'
94	STORE_NAME        'StringIO'
97	POP_TOP           None
98	JUMP_FORWARD      '102'
101	END_FINALLY       None
102_0	COME_FROM         '66'
102_1	COME_FROM         '101'

102	LOAD_CONST        'shlex'
105	LOAD_CONST        'split'
108	BUILD_LIST_2      None
111	STORE_NAME        '__all__'

114	LOAD_CONST        'shlex'
117	LOAD_CONST        ()
120	LOAD_CONST        '<code_object shlex>'
123	MAKE_FUNCTION_0   None
126	CALL_FUNCTION_0   None
129	BUILD_CLASS       None
130	STORE_NAME        'shlex'

133	LOAD_NAME         'False'
136	LOAD_NAME         'True'
139	LOAD_CONST        '<code_object split>'
142	MAKE_FUNCTION_2   None
145	STORE_NAME        'split'

148	LOAD_NAME         '__name__'
151	LOAD_CONST        '__main__'
154	COMPARE_OP        '=='
157	POP_JUMP_IF_FALSE '274'

160	LOAD_NAME         'len'
163	LOAD_NAME         'sys'
166	LOAD_ATTR         'argv'
169	CALL_FUNCTION_1   None
172	LOAD_CONST        1
175	COMPARE_OP        '=='
178	POP_JUMP_IF_FALSE '193'

181	LOAD_NAME         'shlex'
184	CALL_FUNCTION_0   None
187	STORE_NAME        'lexer'
190	JUMP_FORWARD      '227'

193	LOAD_NAME         'sys'
196	LOAD_ATTR         'argv'
199	LOAD_CONST        1
202	BINARY_SUBSCR     None
203	STORE_NAME        'file'

206	LOAD_NAME         'shlex'
209	LOAD_NAME         'open'
212	LOAD_NAME         'file'
215	CALL_FUNCTION_1   None
218	LOAD_NAME         'file'
221	CALL_FUNCTION_2   None
224	STORE_NAME        'lexer'
227_0	COME_FROM         '190'

227	SETUP_LOOP        '274'

230	LOAD_NAME         'lexer'
233	LOAD_ATTR         'get_token'
236	CALL_FUNCTION_0   None
239	STORE_NAME        'tt'

242	LOAD_NAME         'tt'
245	POP_JUMP_IF_FALSE '266'

248	LOAD_CONST        'Token: '
251	LOAD_NAME         'repr'
254	LOAD_NAME         'tt'
257	CALL_FUNCTION_1   None
260	BINARY_ADD        None
261	PRINT_ITEM        None
262	PRINT_NEWLINE_CONT None
263	JUMP_BACK         '230'

266	BREAK_LOOP        None
267	JUMP_BACK         '230'
270	POP_BLOCK         None
271_0	COME_FROM         '227'
271	JUMP_FORWARD      '274'
274_0	COME_FROM         '271'

Syntax error at or near `POP_BLOCK' token at offset 270

