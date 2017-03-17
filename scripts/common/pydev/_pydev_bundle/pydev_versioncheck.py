# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_versioncheck.py
import sys

def versionok_for_gui():
    """ Return True if running Python is suitable for GUI Event Integration and deeper IPython integration """
    if sys.hexversion < 33947648:
        return False
    if sys.hexversion >= 50331648 and sys.hexversion < 50462720:
        return False
    if sys.platform.startswith('java') or sys.platform.startswith('cli'):
        return False
    return True