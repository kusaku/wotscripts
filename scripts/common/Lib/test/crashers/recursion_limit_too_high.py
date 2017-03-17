# Embedded file name: scripts/common/Lib/test/crashers/recursion_limit_too_high.py
import sys
if 'recursion_limit_too_high' in sys.modules:
    del sys.modules['recursion_limit_too_high']
import recursion_limit_too_high