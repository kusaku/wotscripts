# Embedded file name: scripts/common/Lib/test/reperf.py
import re
import time

def main():
    s = '\x0bhello\x0c \x0bworld\x0c ' * 1000
    p = re.compile('([\\13\\14])')
    timefunc(10, p.sub, '', s)
    timefunc(10, p.split, s)
    timefunc(10, p.findall, s)


def timefunc(n, func, *args, **kw):
    t0 = time.clock()
    try:
        for i in range(n):
            result = func(*args, **kw)

        return result
    finally:
        t1 = time.clock()
        if n > 1:
            print n, 'times',
        print func.__name__, '%.3f' % (t1 - t0), 'CPU seconds'


main()