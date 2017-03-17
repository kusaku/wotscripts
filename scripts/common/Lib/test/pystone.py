# Embedded file name: scripts/common/Lib/test/pystone.py
"""
"PYSTONE" Benchmark Program

Version:        Python/1.1 (corresponds to C/1.1 plus 2 Pystone fixes)

Author:         Reinhold P. Weicker,  CACM Vol 27, No 10, 10/84 pg. 1013.

                Translated from ADA to C by Rick Richardson.
                Every method to preserve ADA-likeness has been used,
                at the expense of C-ness.

                Translated from C to Python by Guido van Rossum.

Version History:

                Version 1.1 corrects two bugs in version 1.0:

                First, it leaked memory: in Proc1(), NextRecord ends
                up having a pointer to itself.  I have corrected this
                by zapping NextRecord.PtrComp at the end of Proc1().

                Second, Proc3() used the operator != to compare a
                record to None.  This is rather inefficient and not
                true to the intention of the original benchmark (where
                a pointer comparison to None is intended; the !=
                operator attempts to find a method __cmp__ to do value
                comparison of the record).  Version 1.1 runs 5-10
                percent faster than version 1.0, so benchmark figures
                of different versions can't be compared directly.

"""
LOOPS = 50000
from time import clock
__version__ = '1.1'
Ident1, Ident2, Ident3, Ident4, Ident5 = range(1, 6)

class Record:

    def __init__(self, PtrComp = None, Discr = 0, EnumComp = 0, IntComp = 0, StringComp = 0):
        self.PtrComp = PtrComp
        self.Discr = Discr
        self.EnumComp = EnumComp
        self.IntComp = IntComp
        self.StringComp = StringComp

    def copy(self):
        return Record(self.PtrComp, self.Discr, self.EnumComp, self.IntComp, self.StringComp)


TRUE = 1
FALSE = 0

def main(loops = LOOPS):
    benchtime, stones = pystones(loops)
    print 'Pystone(%s) time for %d passes = %g' % (__version__, loops, benchtime)
    print 'This machine benchmarks at %g pystones/second' % stones


def pystones(loops = LOOPS):
    return Proc0(loops)


IntGlob = 0
BoolGlob = FALSE
Char1Glob = '\x00'
Char2Glob = '\x00'
Array1Glob = [0] * 51
Array2Glob = map(lambda x: x[:], [Array1Glob] * 51)
PtrGlb = None
PtrGlbNext = None

def Proc0(loops = LOOPS):
    global Char2Glob
    global Array2Glob
    global PtrGlb
    global PtrGlbNext
    global Array1Glob
    global BoolGlob
    starttime = clock()
    for i in range(loops):
        pass

    nulltime = clock() - starttime
    PtrGlbNext = Record()
    PtrGlb = Record()
    PtrGlb.PtrComp = PtrGlbNext
    PtrGlb.Discr = Ident1
    PtrGlb.EnumComp = Ident3
    PtrGlb.IntComp = 40
    PtrGlb.StringComp = 'DHRYSTONE PROGRAM, SOME STRING'
    String1Loc = "DHRYSTONE PROGRAM, 1'ST STRING"
    Array2Glob[8][7] = 10
    starttime = clock()
    for i in range(loops):
        Proc5()
        Proc4()
        IntLoc1 = 2
        IntLoc2 = 3
        String2Loc = "DHRYSTONE PROGRAM, 2'ND STRING"
        EnumLoc = Ident2
        BoolGlob = not Func2(String1Loc, String2Loc)
        while IntLoc1 < IntLoc2:
            IntLoc3 = 5 * IntLoc1 - IntLoc2
            IntLoc3 = Proc7(IntLoc1, IntLoc2)
            IntLoc1 = IntLoc1 + 1

        Proc8(Array1Glob, Array2Glob, IntLoc1, IntLoc3)
        PtrGlb = Proc1(PtrGlb)
        CharIndex = 'A'
        while CharIndex <= Char2Glob:
            if EnumLoc == Func1(CharIndex, 'C'):
                EnumLoc = Proc6(Ident1)
            CharIndex = chr(ord(CharIndex) + 1)

        IntLoc3 = IntLoc2 * IntLoc1
        IntLoc2 = IntLoc3 / IntLoc1
        IntLoc2 = 7 * (IntLoc3 - IntLoc2) - IntLoc1
        IntLoc1 = Proc2(IntLoc1)

    benchtime = clock() - starttime - nulltime
    if benchtime == 0.0:
        loopsPerBenchtime = 0.0
    else:
        loopsPerBenchtime = loops / benchtime
    return (benchtime, loopsPerBenchtime)


def Proc1(PtrParIn):
    PtrParIn.PtrComp = NextRecord = PtrGlb.copy()
    PtrParIn.IntComp = 5
    NextRecord.IntComp = PtrParIn.IntComp
    NextRecord.PtrComp = PtrParIn.PtrComp
    NextRecord.PtrComp = Proc3(NextRecord.PtrComp)
    if NextRecord.Discr == Ident1:
        NextRecord.IntComp = 6
        NextRecord.EnumComp = Proc6(PtrParIn.EnumComp)
        NextRecord.PtrComp = PtrGlb.PtrComp
        NextRecord.IntComp = Proc7(NextRecord.IntComp, 10)
    else:
        PtrParIn = NextRecord.copy()
    NextRecord.PtrComp = None
    return PtrParIn


def Proc2--- This code section failed: ---

0	LOAD_FAST         'IntParIO'
3	LOAD_CONST        10
6	BINARY_ADD        None
7	STORE_FAST        'IntLoc'

10	SETUP_LOOP        '74'

13	LOAD_GLOBAL       'Char1Glob'
16	LOAD_CONST        'A'
19	COMPARE_OP        '=='
22	POP_JUMP_IF_FALSE '54'

25	LOAD_FAST         'IntLoc'
28	LOAD_CONST        1
31	BINARY_SUBTRACT   None
32	STORE_FAST        'IntLoc'

35	LOAD_FAST         'IntLoc'
38	LOAD_GLOBAL       'IntGlob'
41	BINARY_SUBTRACT   None
42	STORE_FAST        'IntParIO'

45	LOAD_GLOBAL       'Ident1'
48	STORE_FAST        'EnumLoc'
51	JUMP_FORWARD      '54'
54_0	COME_FROM         '51'

54	LOAD_FAST         'EnumLoc'
57	LOAD_GLOBAL       'Ident1'
60	COMPARE_OP        '=='
63	POP_JUMP_IF_FALSE '13'

66	BREAK_LOOP        None
67	JUMP_BACK         '13'
70	JUMP_BACK         '13'
73	POP_BLOCK         None
74_0	COME_FROM         '10'

74	LOAD_FAST         'IntParIO'
77	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 73


def Proc3(PtrParOut):
    global IntGlob
    if PtrGlb is not None:
        PtrParOut = PtrGlb.PtrComp
    else:
        IntGlob = 100
    PtrGlb.IntComp = Proc7(10, IntGlob)
    return PtrParOut


def Proc4():
    global Char2Glob
    global Char1Glob
    BoolLoc = Char1Glob == 'A'
    BoolLoc = BoolLoc or BoolGlob
    Char2Glob = 'B'


def Proc5():
    global Char1Glob
    global BoolGlob
    Char1Glob = 'A'
    BoolGlob = FALSE


def Proc6(EnumParIn):
    EnumParOut = EnumParIn
    if not Func3(EnumParIn):
        EnumParOut = Ident4
    if EnumParIn == Ident1:
        EnumParOut = Ident1
    elif EnumParIn == Ident2:
        if IntGlob > 100:
            EnumParOut = Ident1
        else:
            EnumParOut = Ident4
    elif EnumParIn == Ident3:
        EnumParOut = Ident2
    elif EnumParIn == Ident4:
        pass
    elif EnumParIn == Ident5:
        EnumParOut = Ident3
    return EnumParOut


def Proc7(IntParI1, IntParI2):
    IntLoc = IntParI1 + 2
    IntParOut = IntParI2 + IntLoc
    return IntParOut


def Proc8(Array1Par, Array2Par, IntParI1, IntParI2):
    global IntGlob
    IntLoc = IntParI1 + 5
    Array1Par[IntLoc] = IntParI2
    Array1Par[IntLoc + 1] = Array1Par[IntLoc]
    Array1Par[IntLoc + 30] = IntLoc
    for IntIndex in range(IntLoc, IntLoc + 2):
        Array2Par[IntLoc][IntIndex] = IntLoc

    Array2Par[IntLoc][IntLoc - 1] = Array2Par[IntLoc][IntLoc - 1] + 1
    Array2Par[IntLoc + 20][IntLoc] = Array1Par[IntLoc]
    IntGlob = 5


def Func1(CharPar1, CharPar2):
    CharLoc1 = CharPar1
    CharLoc2 = CharLoc1
    if CharLoc2 != CharPar2:
        return Ident1
    else:
        return Ident2


def Func2(StrParI1, StrParI2):
    IntLoc = 1
    while IntLoc <= 1:
        if Func1(StrParI1[IntLoc], StrParI2[IntLoc + 1]) == Ident1:
            CharLoc = 'A'
            IntLoc = IntLoc + 1

    if CharLoc >= 'W' and CharLoc <= 'Z':
        IntLoc = 7
    if CharLoc == 'X':
        return TRUE
    elif StrParI1 > StrParI2:
        IntLoc = IntLoc + 7
        return TRUE
    else:
        return FALSE


def Func3(EnumParIn):
    EnumLoc = EnumParIn
    if EnumLoc == Ident3:
        return TRUE
    return FALSE


if __name__ == '__main__':
    import sys

    def error(msg):
        print >> sys.stderr, msg,
        print >> sys.stderr, 'usage: %s [number_of_loops]' % sys.argv[0]
        sys.exit(100)


    nargs = len(sys.argv) - 1
    if nargs > 1:
        error('%d arguments are too many;' % nargs)
    elif nargs == 1:
        try:
            loops = int(sys.argv[1])
        except ValueError:
            error('Invalid argument %r;' % sys.argv[1])

    else:
        loops = LOOPS
    main(loops)