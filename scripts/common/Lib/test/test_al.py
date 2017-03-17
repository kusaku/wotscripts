# Embedded file name: scripts/common/Lib/test/test_al.py
"""Whimpy test script for the al module
   Roger E. Masse
"""
from test.test_support import verbose, import_module
al = import_module('al', deprecated=True)
alattrs = ['__doc__',
 '__name__',
 'getdefault',
 'getminmax',
 'getname',
 'getparams',
 'newconfig',
 'openport',
 'queryparams',
 'setparams']

def test_main():
    if verbose:
        print 'Touching al module attributes...'
    for attr in alattrs:
        if verbose:
            print 'touching: ', attr
        getattr(al, attr)


if __name__ == '__main__':
    test_main()