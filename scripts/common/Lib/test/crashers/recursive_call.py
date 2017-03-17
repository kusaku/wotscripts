# Embedded file name: scripts/common/Lib/test/crashers/recursive_call.py
import sys
sys.setrecursionlimit(1073741824)
f = lambda f: f(f)
if __name__ == '__main__':
    f(f)