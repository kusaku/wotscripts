# Embedded file name: scripts/common/Lib/test/test_exception_variations.py
from test.test_support import run_unittest
import unittest

class ExceptionTestCase(unittest.TestCase):

    def test_try_except_else_finally(self):
        hit_except = False
        hit_else = False
        hit_finally = False
        try:
            raise Exception, 'nyaa!'
        except:
            hit_except = True
        else:
            hit_else = True
        finally:
            hit_finally = True

        self.assertTrue(hit_except)
        self.assertTrue(hit_finally)
        self.assertFalse(hit_else)

    def test_try_except_else_finally_no_exception(self):
        hit_except = False
        hit_else = False
        hit_finally = False
        try:
            pass
        except:
            hit_except = True
        else:
            hit_else = True
        finally:
            hit_finally = True

        self.assertFalse(hit_except)
        self.assertTrue(hit_finally)
        self.assertTrue(hit_else)

    def test_try_except_finally(self):
        hit_except = False
        hit_finally = False
        try:
            raise Exception, 'yarr!'
        except:
            hit_except = True
        finally:
            hit_finally = True

        self.assertTrue(hit_except)
        self.assertTrue(hit_finally)

    def test_try_except_finally_no_exception(self):
        hit_except = False
        hit_finally = False
        try:
            pass
        except:
            hit_except = True
        finally:
            hit_finally = True

        self.assertFalse(hit_except)
        self.assertTrue(hit_finally)

    def test_try_except(self):
        hit_except = False
        try:
            raise Exception, 'ahoy!'
        except:
            hit_except = True

        self.assertTrue(hit_except)

    def test_try_except_no_exception(self):
        hit_except = False
        try:
            pass
        except:
            hit_except = True

        self.assertFalse(hit_except)

    def test_try_except_else(self):
        hit_except = False
        hit_else = False
        try:
            raise Exception, 'foo!'
        except:
            hit_except = True
        else:
            hit_else = True

        self.assertFalse(hit_else)
        self.assertTrue(hit_except)

    def test_try_except_else_no_exception(self):
        hit_except = False
        hit_else = False
        try:
            pass
        except:
            hit_except = True
        else:
            hit_else = True

        self.assertFalse(hit_except)
        self.assertTrue(hit_else)

    def test_try_finally_no_exception--- This code section failed: ---

0	LOAD_GLOBAL       'False'
3	STORE_FAST        'hit_finally'

6	SETUP_FINALLY     '13'

9	POP_BLOCK         None
10	LOAD_CONST        None
13_0	COME_FROM         '6'

13	LOAD_GLOBAL       'True'
16	STORE_FAST        'hit_finally'
19	END_FINALLY       None

20	LOAD_FAST         'self'
23	LOAD_ATTR         'assertTrue'
26	LOAD_FAST         'hit_finally'
29	CALL_FUNCTION_1   None
32	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 9

    def test_nested(self):
        hit_finally = False
        hit_inner_except = False
        hit_inner_finally = False
        try:
            try:
                raise Exception, 'inner exception'
            except:
                hit_inner_except = True
            finally:
                hit_inner_finally = True

        finally:
            hit_finally = True

        self.assertTrue(hit_inner_except)
        self.assertTrue(hit_inner_finally)
        self.assertTrue(hit_finally)

    def test_nested_else(self):
        hit_else = False
        hit_finally = False
        hit_except = False
        hit_inner_except = False
        hit_inner_else = False
        try:
            try:
                pass
            except:
                hit_inner_except = True
            else:
                hit_inner_else = True

            raise Exception, 'outer exception'
        except:
            hit_except = True
        else:
            hit_else = True
        finally:
            hit_finally = True

        self.assertFalse(hit_inner_except)
        self.assertTrue(hit_inner_else)
        self.assertFalse(hit_else)
        self.assertTrue(hit_finally)
        self.assertTrue(hit_except)


def test_main():
    run_unittest(ExceptionTestCase)


if __name__ == '__main__':
    test_main()