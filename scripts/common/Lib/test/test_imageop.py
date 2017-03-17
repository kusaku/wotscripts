# Embedded file name: scripts/common/Lib/test/test_imageop.py
"""Test script for the imageop module.  This has the side
   effect of partially testing the imgfile module as well.
   Roger E. Masse
"""
from test.test_support import verbose, unlink, import_module, run_unittest
imageop = import_module('imageop', deprecated=True)
import uu, os, unittest
SIZES = (1, 2, 3, 4)
_VALUES = (1,
 2,
 1024,
 32767,
 32768,
 32769,
 2147483646L,
 2147483647L)
VALUES = tuple((-x for x in reversed(_VALUES))) + (0,) + _VALUES
AAAAA = 'A' * 1024
MAX_LEN = 1048576

class InputValidationTests(unittest.TestCase):

    def _check(self, name, size = None, *extra):
        func = getattr(imageop, name)
        for height in VALUES:
            for width in VALUES:
                strlen = abs(width * height)
                if size:
                    strlen *= size
                if strlen < MAX_LEN:
                    data = 'A' * strlen
                else:
                    data = AAAAA
                if size:
                    arguments = (data,
                     size,
                     width,
                     height) + extra
                else:
                    arguments = (data, width, height) + extra
                try:
                    func(*arguments)
                except (ValueError, imageop.error):
                    pass

    def check_size(self, name, *extra):
        for size in SIZES:
            self._check(name, size, *extra)

    def check(self, name, *extra):
        self._check(name, None, *extra)
        return

    def test_input_validation(self):
        self.check_size('crop', 0, 0, 0, 0)
        self.check_size('scale', 1, 0)
        self.check_size('scale', -1, -1)
        self.check_size('tovideo')
        self.check('grey2mono', 128)
        self.check('grey2grey4')
        self.check('grey2grey2')
        self.check('dither2mono')
        self.check('dither2grey2')
        self.check('mono2grey', 0, 0)
        self.check('grey22grey')
        self.check('rgb2rgb8')
        self.check('rgb82rgb')
        self.check('rgb2grey')
        self.check('grey2rgb')


def test_main():
    run_unittest(InputValidationTests)
    try:
        import imgfile
    except ImportError:
        return

    uu.decode(get_qualified_path('testrgb' + os.extsep + 'uue'), 'test' + os.extsep + 'rgb')
    image, width, height = getimage('test' + os.extsep + 'rgb')
    if verbose:
        print 'crop'
    newimage = imageop.crop(image, 4, width, height, 0, 0, 1, 1)
    if verbose:
        print 'scale'
    scaleimage = imageop.scale(image, 4, width, height, 1, 1)
    if verbose:
        print 'tovideo'
    videoimage = imageop.tovideo(image, 4, width, height)
    if verbose:
        print 'rgb2rgb8'
    greyimage = imageop.rgb2rgb8(image, width, height)
    if verbose:
        print 'rgb82rgb'
    image = imageop.rgb82rgb(greyimage, width, height)
    if verbose:
        print 'rgb2grey'
    greyimage = imageop.rgb2grey(image, width, height)
    if verbose:
        print 'grey2rgb'
    image = imageop.grey2rgb(greyimage, width, height)
    if verbose:
        print 'grey2mono'
    monoimage = imageop.grey2mono(greyimage, width, height, 0)
    if verbose:
        print 'mono2grey'
    greyimage = imageop.mono2grey(monoimage, width, height, 0, 255)
    if verbose:
        print 'dither2mono'
    monoimage = imageop.dither2mono(greyimage, width, height)
    if verbose:
        print 'grey2grey4'
    grey4image = imageop.grey2grey4(greyimage, width, height)
    if verbose:
        print 'grey2grey2'
    grey2image = imageop.grey2grey2(greyimage, width, height)
    if verbose:
        print 'dither2grey2'
    grey2image = imageop.dither2grey2(greyimage, width, height)
    if verbose:
        print 'grey42grey'
    greyimage = imageop.grey42grey(grey4image, width, height)
    if verbose:
        print 'grey22grey'
    image = imageop.grey22grey(grey2image, width, height)
    unlink('test' + os.extsep + 'rgb')


def getimage(name):
    """return a tuple consisting of
       image (in 'imgfile' format) width and height
    """
    import imgfile
    try:
        sizes = imgfile.getsizes(name)
    except imgfile.error:
        name = get_qualified_path(name)
        sizes = imgfile.getsizes(name)

    if verbose:
        print 'imgfile opening test image: %s, sizes: %s' % (name, str(sizes))
    image = imgfile.read(name)
    return (image, sizes[0], sizes[1])


def get_qualified_path(name):
    """ return a more qualified path to name"""
    import sys
    import os
    path = sys.path
    try:
        path = [os.path.dirname(__file__)] + path
    except NameError:
        pass

    for dir in path:
        fullname = os.path.join(dir, name)
        if os.path.exists(fullname):
            return fullname

    return name


if __name__ == '__main__':
    test_main()