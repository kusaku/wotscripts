# Embedded file name: scripts/common/Lib/fpformat.py
"""General floating point formatting functions.

Functions:
fix(x, digits_behind)
sci(x, digits_behind)

Each takes a number or a string and a number of digits as arguments.

Parameters:
x:             number to be formatted; or a string resembling a number
digits_behind: number of digits behind the decimal point
"""
from warnings import warnpy3k
warnpy3k('the fpformat module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
import re
__all__ = ['fix', 'sci', 'NotANumber']
decoder = re.compile('^([-+]?)0*(\\d*)((?:\\.\\d*)?)(([eE][-+]?\\d+)?)$')
try:

    class NotANumber(ValueError):
        pass


except TypeError:
    NotANumber = 'fpformat.NotANumber'

def extract(s):
    """Return (sign, intpart, fraction, expo) or raise an exception:
    sign is '+' or '-'
    intpart is 0 or more digits beginning with a nonzero
    fraction is 0 or more digits
    expo is an integer"""
    res = decoder.match(s)
    if res is None:
        raise NotANumber, s
    sign, intpart, fraction, exppart = res.group(1, 2, 3, 4)
    if sign == '+':
        sign = ''
    if fraction:
        fraction = fraction[1:]
    if exppart:
        expo = int(exppart[1:])
    else:
        expo = 0
    return (sign,
     intpart,
     fraction,
     expo)


def unexpo(intpart, fraction, expo):
    """Remove the exponent by changing intpart and fraction."""
    if expo > 0:
        f = len(fraction)
        intpart, fraction = intpart + fraction[:expo], fraction[expo:]
        if expo > f:
            intpart = intpart + '0' * (expo - f)
    elif expo < 0:
        i = len(intpart)
        intpart, fraction = intpart[:expo], intpart[expo:] + fraction
        if expo < -i:
            fraction = '0' * (-expo - i) + fraction
    return (intpart, fraction)


def roundfrac(intpart, fraction, digs):
    """Round or extend the fraction to size digs."""
    f = len(fraction)
    if f <= digs:
        return (intpart, fraction + '0' * (digs - f))
    i = len(intpart)
    if i + digs < 0:
        return ('0' * -digs, '')
    total = intpart + fraction
    nextdigit = total[i + digs]
    if nextdigit >= '5':
        n = i + digs - 1
        while n >= 0:
            if total[n] != '9':
                break
            n = n - 1
        else:
            total = '0' + total
            i = i + 1
            n = 0

        total = total[:n] + chr(ord(total[n]) + 1) + '0' * (len(total) - n - 1)
        intpart, fraction = total[:i], total[i:]
    if digs >= 0:
        return (intpart, fraction[:digs])
    else:
        return (intpart[:digs] + '0' * -digs, '')


def fix(x, digs):
    """Format x as [-]ddd.ddd with 'digs' digits after the point
    and at least one digit before.
    If digs <= 0, the point is suppressed."""
    if type(x) != type(''):
        x = repr(x)
    try:
        sign, intpart, fraction, expo = extract(x)
    except NotANumber:
        return x

    intpart, fraction = unexpo(intpart, fraction, expo)
    intpart, fraction = roundfrac(intpart, fraction, digs)
    while intpart and intpart[0] == '0':
        intpart = intpart[1:]

    if intpart == '':
        intpart = '0'
    if digs > 0:
        return sign + intpart + '.' + fraction
    else:
        return sign + intpart


def sci(x, digs):
    """Format x as [-]d.dddE[+-]ddd with 'digs' digits after the point
    and exactly one digit before.
    If digs is <= 0, one digit is kept and the point is suppressed."""
    if type(x) != type(''):
        x = repr(x)
    sign, intpart, fraction, expo = extract(x)
    if not intpart:
        while fraction and fraction[0] == '0':
            fraction = fraction[1:]
            expo = expo - 1

        if fraction:
            intpart, fraction = fraction[0], fraction[1:]
            expo = expo - 1
        else:
            intpart = '0'
    else:
        expo = expo + len(intpart) - 1
        intpart, fraction = intpart[0], intpart[1:] + fraction
    digs = max(0, digs)
    intpart, fraction = roundfrac(intpart, fraction, digs)
    if len(intpart) > 1:
        intpart, fraction, expo = intpart[0], intpart[1:] + fraction[:-1], expo + len(intpart) - 1
    s = sign + intpart
    if digs > 0:
        s = s + '.' + fraction
    e = repr(abs(expo))
    e = '0' * (3 - len(e)) + e
    if expo < 0:
        e = '-' + e
    else:
        e = '+' + e
    return s + 'e' + e


def test--- This code section failed: ---

0	SETUP_EXCEPT      '63'

3	SETUP_LOOP        '59'

6	LOAD_GLOBAL       'input'
9	LOAD_CONST        'Enter (x, digs): '
12	CALL_FUNCTION_1   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'x'
21	STORE_FAST        'digs'

24	LOAD_FAST         'x'
27	PRINT_ITEM        None
28	LOAD_GLOBAL       'fix'
31	LOAD_FAST         'x'
34	LOAD_FAST         'digs'
37	CALL_FUNCTION_2   None
40	PRINT_ITEM_CONT   None
41	LOAD_GLOBAL       'sci'
44	LOAD_FAST         'x'
47	LOAD_FAST         'digs'
50	CALL_FUNCTION_2   None
53	PRINT_ITEM_CONT   None
54	PRINT_NEWLINE_CONT None
55	JUMP_BACK         '6'
58	POP_BLOCK         None
59_0	COME_FROM         '3'
59	POP_BLOCK         None
60	JUMP_FORWARD      '86'
63_0	COME_FROM         '0'

63	DUP_TOP           None
64	LOAD_GLOBAL       'EOFError'
67	LOAD_GLOBAL       'KeyboardInterrupt'
70	BUILD_TUPLE_2     None
73	COMPARE_OP        'exception match'
76	POP_JUMP_IF_FALSE '85'
79	POP_TOP           None
80	POP_TOP           None
81	POP_TOP           None

82	JUMP_FORWARD      '86'
85	END_FINALLY       None
86_0	COME_FROM         '60'
86_1	COME_FROM         '85'

Syntax error at or near `POP_BLOCK' token at offset 58