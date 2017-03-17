# Embedded file name: scripts/common/Lib/test/test_cd.py
"""Whimpy test script for the cd module
   Roger E. Masse
"""
from test.test_support import verbose, import_module
cd = import_module('cd')
cdattrs = ['BLOCKSIZE',
 'CDROM',
 'DATASIZE',
 'ERROR',
 'NODISC',
 'PAUSED',
 'PLAYING',
 'READY',
 'STILL',
 '__doc__',
 '__name__',
 'atime',
 'audio',
 'catalog',
 'control',
 'createparser',
 'error',
 'ident',
 'index',
 'msftoframe',
 'open',
 'pnum',
 'ptime']

def test_main():
    if verbose:
        print 'Touching cd module attributes...'
    for attr in cdattrs:
        if verbose:
            print 'touching: ', attr
        getattr(cd, attr)


if __name__ == '__main__':
    test_main()