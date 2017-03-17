# Embedded file name: scripts/common/Lib/test/leakers/test_gestalt.py
import sys
if sys.platform != 'darwin':
    raise ValueError, 'This test only leaks on Mac OS X'

def leak():
    from gestalt import gestalt
    import MacOS
    try:
        gestalt('sysu')
    except MacOS.Error:
        pass