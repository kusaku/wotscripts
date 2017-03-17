# Embedded file name: scripts/common/Lib/test/test_imgfile.py
"""Simple test script for imgfile.c
   Roger E. Masse
"""
from test.test_support import verbose, unlink, findfile, import_module
imgfile = import_module('imgfile', deprecated=True)
import uu

def testimage(name):
    """Run through the imgfile's battery of possible methods
       on the image passed in name.
    """
    import sys
    import os
    outputfile = '/tmp/deleteme'
    try:
        sizes = imgfile.getsizes(name)
    except imgfile.error:
        if __name__ == '__main__':
            ourname = sys.argv[0]
        else:
            ourname = sys.modules[__name__].__file__
        parts = ourname.split(os.sep)
        parts[-1] = name
        name = os.sep.join(parts)
        sizes = imgfile.getsizes(name)

    if verbose:
        print 'Opening test image: %s, sizes: %s' % (name, str(sizes))
    image = imgfile.read(name)
    if verbose:
        print 'Writing output file'
    imgfile.write(outputfile, image, sizes[0], sizes[1], sizes[2])
    if verbose:
        print 'Opening scaled test image: %s, sizes: %s' % (name, str(sizes))
    if verbose:
        print 'Filtering with "impulse"'
    simage = imgfile.readscaled(name, sizes[0] / 2, sizes[1] / 2, 'impulse', 2.0)
    if verbose:
        print 'Switching to X compatibility'
    imgfile.ttob(1)
    if verbose:
        print 'Filtering with "triangle"'
    simage = imgfile.readscaled(name, sizes[0] / 2, sizes[1] / 2, 'triangle', 3.0)
    if verbose:
        print 'Switching back to SGI compatibility'
    imgfile.ttob(0)
    if verbose:
        print 'Filtering with "quadratic"'
    simage = imgfile.readscaled(name, sizes[0] / 2, sizes[1] / 2, 'quadratic')
    if verbose:
        print 'Filtering with "gaussian"'
    simage = imgfile.readscaled(name, sizes[0] / 2, sizes[1] / 2, 'gaussian', 1.0)
    if verbose:
        print 'Writing output file'
    imgfile.write(outputfile, simage, sizes[0] / 2, sizes[1] / 2, sizes[2])
    os.unlink(outputfile)


def test_main():
    uu.decode(findfile('testrgb.uue'), 'test.rgb')
    uu.decode(findfile('greyrgb.uue'), 'greytest.rgb')
    testimage('test.rgb')
    testimage('greytest.rgb')
    unlink('test.rgb')
    unlink('greytest.rgb')


if __name__ == '__main__':
    test_main()