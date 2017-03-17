# Embedded file name: scripts/common/BWAutoImport.py
import __builtin__
import encodings
import pydoc
import logging
import BigWorld
DEFAULT_ENCODING = 'utf-8'

class _Helper(object):
    """Define the built-in 'help'.
    This is a wrapper around pydoc.help (with a twist).
    
    """

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        return pydoc.help(*args, **kwds)


def sethelper():
    __builtin__.help = _Helper()


def setDefaultEncoding():
    import sys
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding(DEFAULT_ENCODING)
        del sys.setdefaultencoding


def testUnicode():
    import unicode_test
    unicode_test.run()


def main():
    sethelper()
    setDefaultEncoding()
    logging.basicConfig(format='%(levelname)s: %(message)s', level=1)


main()