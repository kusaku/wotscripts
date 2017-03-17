# Embedded file name: scripts/common/Lib/test/test_opcodes.py
from test.test_support import run_unittest, check_py3k_warnings
import unittest

class OpcodeTest(unittest.TestCase):

    def test_try_inside_for_loop--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'n'

6	SETUP_LOOP        '135'
9	LOAD_GLOBAL       'range'
12	LOAD_CONST        10
15	CALL_FUNCTION_1   None
18	GET_ITER          None
19	FOR_ITER          '134'
22	STORE_FAST        'i'

25	LOAD_FAST         'n'
28	LOAD_FAST         'i'
31	BINARY_ADD        None
32	STORE_FAST        'n'

35	SETUP_EXCEPT      '50'
38	LOAD_CONST        1
41	LOAD_CONST        0
44	BINARY_FLOOR_DIVIDE None
45	POP_TOP           None
46	POP_BLOCK         None
47	JUMP_FORWARD      '99'
50_0	COME_FROM         '35'

50	DUP_TOP           None
51	LOAD_GLOBAL       'NameError'
54	COMPARE_OP        'exception match'
57	POP_JUMP_IF_FALSE '66'
60	POP_TOP           None
61	POP_TOP           None
62	POP_TOP           None
63	JUMP_FORWARD      '99'

66	DUP_TOP           None
67	LOAD_GLOBAL       'ZeroDivisionError'
70	COMPARE_OP        'exception match'
73	POP_JUMP_IF_FALSE '82'
76	POP_TOP           None
77	POP_TOP           None
78	POP_TOP           None
79	JUMP_FORWARD      '99'

82	DUP_TOP           None
83	LOAD_GLOBAL       'TypeError'
86	COMPARE_OP        'exception match'
89	POP_JUMP_IF_FALSE '98'
92	POP_TOP           None
93	POP_TOP           None
94	POP_TOP           None
95	JUMP_FORWARD      '99'
98	END_FINALLY       None
99_0	COME_FROM         '47'
99_1	COME_FROM         '98'

99	SETUP_EXCEPT      '106'
102	POP_BLOCK         None
103	JUMP_FORWARD      '113'
106_0	COME_FROM         '99'

106	POP_TOP           None
107	POP_TOP           None
108	POP_TOP           None
109	JUMP_FORWARD      '113'
112	END_FINALLY       None
113_0	COME_FROM         '103'
113_1	COME_FROM         '112'

113	SETUP_FINALLY     '120'
116	POP_BLOCK         None
117	LOAD_CONST        None
120_0	COME_FROM         '113'

120	END_FINALLY       None

121	LOAD_FAST         'n'
124	LOAD_FAST         'i'
127	BINARY_ADD        None
128	STORE_FAST        'n'
131	JUMP_BACK         '19'
134	POP_BLOCK         None
135_0	COME_FROM         '6'

135	LOAD_FAST         'n'
138	LOAD_CONST        90
141	COMPARE_OP        '!='
144	POP_JUMP_IF_FALSE '163'

147	LOAD_FAST         'self'
150	LOAD_ATTR         'fail'
153	LOAD_CONST        'try inside for'
156	CALL_FUNCTION_1   None
159	POP_TOP           None
160	JUMP_FORWARD      '163'
163_0	COME_FROM         '160'

Syntax error at or near `POP_BLOCK' token at offset 116

    def test_raise_class_exceptions(self):

        class AClass:
            pass

        class BClass(AClass):
            pass

        class CClass:
            pass

        class DClass(AClass):

            def __init__(self, ignore):
                pass

        try:
            raise AClass()
        except:
            pass

        try:
            raise AClass()
        except AClass:
            pass

        try:
            raise BClass()
        except AClass:
            pass

        try:
            raise BClass()
        except CClass:
            self.fail()
        except:
            pass

        a = AClass()
        b = BClass()
        try:
            raise AClass, b
        except BClass as v:
            self.assertEqual(v, b)
        else:
            self.fail('no exception')

        try:
            raise b
        except AClass as v:
            self.assertEqual(v, b)
        else:
            self.fail('no exception')

        try:
            raise BClass, a
        except TypeError:
            pass
        else:
            self.fail('no exception')

        try:
            raise DClass, a
        except DClass as v:
            self.assertIsInstance(v, DClass)
        else:
            self.fail('no exception')

    def test_compare_function_objects(self):
        f = eval('lambda: None')
        g = eval('lambda: None')
        self.assertNotEqual(f, g)
        f = eval('lambda a: a')
        g = eval('lambda a: a')
        self.assertNotEqual(f, g)
        f = eval('lambda a=1: a')
        g = eval('lambda a=1: a')
        self.assertNotEqual(f, g)
        f = eval('lambda: 0')
        g = eval('lambda: 1')
        self.assertNotEqual(f, g)
        f = eval('lambda: None')
        g = eval('lambda a: None')
        self.assertNotEqual(f, g)
        f = eval('lambda a: None')
        g = eval('lambda b: None')
        self.assertNotEqual(f, g)
        f = eval('lambda a: None')
        g = eval('lambda a=None: None')
        self.assertNotEqual(f, g)
        f = eval('lambda a=0: None')
        g = eval('lambda a=1: None')
        self.assertNotEqual(f, g)

    def test_modulo_of_string_subclasses(self):

        class MyString(str):

            def __mod__(self, value):
                return 42

        self.assertEqual(MyString() % 3, 42)


def test_main():
    with check_py3k_warnings(('exceptions must derive from BaseException', DeprecationWarning), ("catching classes that don't inherit from BaseException is not allowed", DeprecationWarning)):
        run_unittest(OpcodeTest)


if __name__ == '__main__':
    test_main()