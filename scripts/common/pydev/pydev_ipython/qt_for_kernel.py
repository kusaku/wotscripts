# Embedded file name: scripts/common/pydev/pydev_ipython/qt_for_kernel.py
""" Import Qt in a manner suitable for an IPython kernel.

This is the import used for the `gui=qt` or `matplotlib=qt` initialization.

Import Priority:

if Qt4 has been imported anywhere else:
   use that

if matplotlib has been imported and doesn't support v2 (<= 1.0.1):
    use PyQt4 @v1

Next, ask ETS' QT_API env variable

if QT_API not set:
    ask matplotlib via rcParams['backend.qt4']
    if it said PyQt:
        use PyQt4 @v1
    elif it said PySide:
        use PySide

    else: (matplotlib said nothing)
        # this is the default path - nobody told us anything
        try:
            PyQt @v1
        except:
            fallback on PySide
else:
    use PyQt @v2 or PySide, depending on QT_API
    because ETS doesn't work with PyQt @v1.

"""
import os
import sys
from pydev_ipython.version import check_version
from pydev_ipython.qt_loaders import load_qt, QT_API_PYSIDE, QT_API_PYQT, QT_API_PYQT_DEFAULT, loaded_api

def matplotlib_options(mpl):
    if mpl is None:
        return
    else:
        mpqt = mpl.rcParams.get('backend.qt4', None)
        if mpqt is None:
            return
        if mpqt.lower() == 'pyside':
            return [QT_API_PYSIDE]
        if mpqt.lower() == 'pyqt4':
            return [QT_API_PYQT_DEFAULT]
        raise ImportError('unhandled value for backend.qt4 from matplotlib: %r' % mpqt)
        return


def get_options():
    """Return a list of acceptable QT APIs, in decreasing order of
    preference
    """
    loaded = loaded_api()
    if loaded is not None:
        return [loaded]
    mpl = sys.modules.get('matplotlib', None)
    if mpl is not None and not check_version(mpl.__version__, '1.0.2'):
        return [QT_API_PYQT_DEFAULT]
    elif os.environ.get('QT_API', None) is None:
        return matplotlib_options(mpl) or [QT_API_PYQT_DEFAULT, QT_API_PYSIDE]
    else:
        return


api_opts = get_options()
if api_opts is not None:
    QtCore, QtGui, QtSvg, QT_API = load_qt(api_opts)
else:
    from pydev_ipython.qt import QtCore, QtGui, QtSvg, QT_API