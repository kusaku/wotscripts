# Embedded file name: scripts/common/Lib/test/sample_doctest.py
"""This is a sample module that doesn't really test anything all that
   interesting.

It simply has a few tests, some of which succeed and some of which fail.

It's important that the numbers remain constant as another test is
testing the running of these tests.


>>> 2+2
4
"""

def foo():
    """
    
    >>> 2+2
    5
    
    >>> 2+2
    4
    """
    pass


def bar():
    """
    
    >>> 2+2
    4
    """
    pass


def test_silly_setup():
    """
    
    >>> import test.test_doctest
    >>> test.test_doctest.sillySetup
    True
    """
    pass


def w_blank():
    """
    >>> if 1:
    ...    print 'a'
    ...    print
    ...    print 'b'
    a
    <BLANKLINE>
    b
    """
    pass


x = 1

def x_is_one():
    """
    >>> x
    1
    """
    pass


def y_is_one():
    """
    >>> y
    1
    """
    pass


__test__ = {'good': '\n                    >>> 42\n                    42\n                    ',
 'bad': '\n                    >>> 42\n                    666\n                    '}

def test_suite():
    import doctest
    return doctest.DocTestSuite()