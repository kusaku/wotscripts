# Embedded file name: scripts/common/pydev/pydev_ipython/version.py
"""
Utilities for version comparison

It is a bit ridiculous that we need these.
"""
from distutils.version import LooseVersion

def check_version(v, check):
    """check version string v >= check
    
    If dev/prerelease tags result in TypeError for string-number comparison,
    it is assumed that the dependency is satisfied.
    Users on dev branches are responsible for keeping their own packages up to date.
    """
    try:
        return LooseVersion(v) >= LooseVersion(check)
    except TypeError:
        return True