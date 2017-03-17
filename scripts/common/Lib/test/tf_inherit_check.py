# Embedded file name: scripts/common/Lib/test/tf_inherit_check.py
import sys
import os
verbose = sys.argv[1] == 'v'
try:
    fd = int(sys.argv[2])
    try:
        os.write(fd, 'blat')
    except os.error:
        sys.exit(0)
    else:
        if verbose:
            sys.stderr.write('fd %d is open in child' % fd)
        sys.exit(1)

except StandardError:
    if verbose:
        raise
    sys.exit(1)