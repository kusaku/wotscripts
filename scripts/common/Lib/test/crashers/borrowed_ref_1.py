# Embedded file name: scripts/common/Lib/test/crashers/borrowed_ref_1.py
--- This code section failed: ---

0	LOAD_CONST        '\n_PyType_Lookup() returns a borrowed reference.\nThis attacks the call in dictobject.c.\n'
3	STORE_NAME        '__doc__'

6	LOAD_CONST        'A'
9	LOAD_NAME         'object'
12	BUILD_TUPLE_1     None
15	LOAD_CONST        '<code_object A>'
18	MAKE_FUNCTION_0   None
21	CALL_FUNCTION_0   None
24	BUILD_CLASS       None
25	STORE_NAME        'A'

28	LOAD_CONST        'B'
31	LOAD_NAME         'object'
34	BUILD_TUPLE_1     None
37	LOAD_CONST        '<code_object B>'
40	MAKE_FUNCTION_0   None
43	CALL_FUNCTION_0   None
46	BUILD_CLASS       None
47	STORE_NAME        'B'

50	LOAD_CONST        'D'
53	LOAD_NAME         'dict'
56	BUILD_TUPLE_1     None
59	LOAD_CONST        '<code_object D>'
62	MAKE_FUNCTION_0   None
65	CALL_FUNCTION_0   None
68	BUILD_CLASS       None
69	STORE_NAME        'D'

72	LOAD_NAME         'D'
75	CALL_FUNCTION_0   None
78	STORE_NAME        'd'

81	LOAD_NAME         'A'
84	CALL_FUNCTION_0   None
87	STORE_NAME        'a'

90	LOAD_NAME         'a'
93	LOAD_NAME         'a'
96	STORE_ATTR        'cycle'

99	LOAD_NAME         'B'
102	CALL_FUNCTION_0   None
105	LOAD_NAME         'a'
108	STORE_ATTR        'other'

111	DELETE_NAME       'a'

114	LOAD_CONST        None
117	STORE_NAME        'prev'

120	SETUP_LOOP        '144'

123	LOAD_NAME         'd'
126	LOAD_CONST        5
129	BINARY_SUBSCR     None
130	POP_TOP           None

131	LOAD_NAME         'prev'
134	BUILD_TUPLE_1     None
137	STORE_NAME        'prev'
140	JUMP_BACK         '123'
143	POP_BLOCK         None
144_0	COME_FROM         '120'

Syntax error at or near `POP_BLOCK' token at offset 143

