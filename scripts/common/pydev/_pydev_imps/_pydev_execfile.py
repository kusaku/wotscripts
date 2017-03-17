# Embedded file name: scripts/common/pydev/_pydev_imps/_pydev_execfile.py


def execfile(file, glob = None, loc = None):
    if glob is None:
        import sys
        glob = sys._getframe().f_back.f_globals
    if loc is None:
        loc = glob
    import tokenize
    stream = tokenize.open(file)
    try:
        contents = stream.read()
    finally:
        stream.close()

    exec compile(contents + '\n', file, 'exec') in glob, loc
    return