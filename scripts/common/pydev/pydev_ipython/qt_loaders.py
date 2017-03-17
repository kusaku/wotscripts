# Embedded file name: scripts/common/pydev/pydev_ipython/qt_loaders.py
"""
This module contains factory functions that attempt
to return Qt submodules from the various python Qt bindings.

It also protects against double-importing Qt with different
bindings, which is unstable and likely to crash

This is used primarily by qt and qt_for_kernel, and shouldn't
be accessed directly from the outside
"""
import sys
from functools import partial
from pydev_ipython.version import check_version
QT_API_PYQT = 'pyqt'
QT_API_PYQTv1 = 'pyqtv1'
QT_API_PYQT_DEFAULT = 'pyqtdefault'
QT_API_PYSIDE = 'pyside'

class ImportDenier(object):
    """Import Hook that will guard against bad Qt imports
    once IPython commits to a specific binding
    """

    def __init__(self):
        self.__forbidden = None
        return

    def forbid(self, module_name):
        sys.modules.pop(module_name, None)
        self.__forbidden = module_name
        return

    def find_module(self, mod_name, pth):
        if pth:
            return
        if mod_name == self.__forbidden:
            return self

    def load_module(self, mod_name):
        raise ImportError('\n    Importing %s disabled by IPython, which has\n    already imported an Incompatible QT Binding: %s\n    ' % (mod_name, loaded_api()))


ID = ImportDenier()
sys.meta_path.append(ID)

def commit_api(api):
    """Commit to a particular API, and trigger ImportErrors on subsequent
    dangerous imports"""
    if api == QT_API_PYSIDE:
        ID.forbid('PyQt4')
    else:
        ID.forbid('PySide')


def loaded_api():
    """Return which API is loaded, if any
    
    If this returns anything besides None,
    importing any other Qt binding is unsafe.
    
    Returns
    -------
    None, 'pyside', 'pyqt', or 'pyqtv1'
    """
    if 'PyQt4.QtCore' in sys.modules:
        if qtapi_version() == 2:
            return QT_API_PYQT
        else:
            return QT_API_PYQTv1
    elif 'PySide.QtCore' in sys.modules:
        return QT_API_PYSIDE
    return None


def has_binding(api):
    """Safely check for PyQt4 or PySide, without importing
       submodules
    
       Parameters
       ----------
       api : str [ 'pyqtv1' | 'pyqt' | 'pyside' | 'pyqtdefault']
            Which module to check for
    
       Returns
       -------
       True if the relevant module appears to be importable
    """
    module_name = {QT_API_PYSIDE: 'PySide',
     QT_API_PYQT: 'PyQt4',
     QT_API_PYQTv1: 'PyQt4',
     QT_API_PYQT_DEFAULT: 'PyQt4'}
    module_name = module_name[api]
    import imp
    try:
        mod = __import__(module_name)
        imp.find_module('QtCore', mod.__path__)
        imp.find_module('QtGui', mod.__path__)
        imp.find_module('QtSvg', mod.__path__)
        if api == QT_API_PYSIDE:
            return check_version(mod.__version__, '1.0.3')
        return True
    except ImportError:
        return False


def qtapi_version():
    """Return which QString API has been set, if any
    
    Returns
    -------
    The QString API version (1 or 2), or None if not set
    """
    try:
        import sip
    except ImportError:
        return

    try:
        return sip.getapi('QString')
    except ValueError:
        return


def can_import(api):
    """Safely query whether an API is importable, without importing it"""
    if not has_binding(api):
        return False
    else:
        current = loaded_api()
        if api == QT_API_PYQT_DEFAULT:
            return current in [QT_API_PYQT, QT_API_PYQTv1, None]
        return current in [api, None]
        return None


def import_pyqt4(version = 2):
    """
    Import PyQt4
    
    Parameters
    ----------
    version : 1, 2, or None
      Which QString/QVariant API to use. Set to None to use the system
      default
    
    ImportErrors rasied within this function are non-recoverable
    """
    import sip
    if version is not None:
        sip.setapi('QString', version)
        sip.setapi('QVariant', version)
    from PyQt4 import QtGui, QtCore, QtSvg
    if not check_version(QtCore.PYQT_VERSION_STR, '4.7'):
        raise ImportError('IPython requires PyQt4 >= 4.7, found %s' % QtCore.PYQT_VERSION_STR)
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    version = sip.getapi('QString')
    api = QT_API_PYQTv1 if version == 1 else QT_API_PYQT
    return (QtCore,
     QtGui,
     QtSvg,
     api)


def import_pyside():
    """
    Import PySide
    
    ImportErrors raised within this function are non-recoverable
    """
    from PySide import QtGui, QtCore, QtSvg
    return (QtCore,
     QtGui,
     QtSvg,
     QT_API_PYSIDE)


def load_qt--- This code section failed: ---

0	BUILD_MAP         None
3	LOAD_GLOBAL       'import_pyside'
6	LOAD_GLOBAL       'QT_API_PYSIDE'
9	STORE_MAP         None

10	LOAD_GLOBAL       'import_pyqt4'
13	LOAD_GLOBAL       'QT_API_PYQT'
16	STORE_MAP         None

17	LOAD_GLOBAL       'partial'
20	LOAD_GLOBAL       'import_pyqt4'
23	LOAD_CONST        'version'
26	LOAD_CONST        1
29	CALL_FUNCTION_257 None
32	LOAD_GLOBAL       'QT_API_PYQTv1'
35	STORE_MAP         None

36	LOAD_GLOBAL       'partial'
39	LOAD_GLOBAL       'import_pyqt4'
42	LOAD_CONST        'version'
45	LOAD_CONST        None
48	CALL_FUNCTION_257 None
51	LOAD_GLOBAL       'QT_API_PYQT_DEFAULT'
54	STORE_MAP         None
55	STORE_FAST        'loaders'

58	SETUP_LOOP        '216'
61	LOAD_FAST         'api_options'
64	GET_ITER          None
65	FOR_ITER          '172'
68	STORE_FAST        'api'

71	LOAD_FAST         'api'
74	LOAD_FAST         'loaders'
77	COMPARE_OP        'not in'
80	POP_JUMP_IF_FALSE '117'

83	LOAD_GLOBAL       'RuntimeError'

86	LOAD_CONST        'Invalid Qt API %r, valid values are: %r, %r, %r, %r'

89	LOAD_FAST         'api'
92	LOAD_GLOBAL       'QT_API_PYSIDE'
95	LOAD_GLOBAL       'QT_API_PYQT'

98	LOAD_GLOBAL       'QT_API_PYQTv1'
101	LOAD_GLOBAL       'QT_API_PYQT_DEFAULT'
104	BUILD_TUPLE_5     None
107	BINARY_MODULO     None
108	CALL_FUNCTION_1   None
111	RAISE_VARARGS_1   None
114	JUMP_FORWARD      '117'
117_0	COME_FROM         '114'

117	LOAD_GLOBAL       'can_import'
120	LOAD_FAST         'api'
123	CALL_FUNCTION_1   None
126	POP_JUMP_IF_TRUE  '135'

129	JUMP_BACK         '65'
132	JUMP_FORWARD      '135'
135_0	COME_FROM         '132'

135	LOAD_FAST         'loaders'
138	LOAD_FAST         'api'
141	BINARY_SUBSCR     None
142	CALL_FUNCTION_0   None
145	STORE_FAST        'result'

148	LOAD_FAST         'result'
151	LOAD_CONST        -1
154	BINARY_SUBSCR     None
155	STORE_FAST        'api'

158	LOAD_GLOBAL       'commit_api'
161	LOAD_FAST         'api'
164	CALL_FUNCTION_1   None
167	POP_TOP           None

168	LOAD_FAST         'result'
171	RETURN_VALUE      None
172	POP_BLOCK         None

173	LOAD_GLOBAL       'ImportError'

176	LOAD_CONST        '\n    Could not load requested Qt binding. Please ensure that\n    PyQt4 >= 4.7 or PySide >= 1.0.3 is available,\n    and only one is imported per session.\n\n    Currently-imported Qt library:   %r\n    PyQt4 installed:                 %s\n    PySide >= 1.0.3 installed:       %s\n    Tried to load:                   %r\n    '
179	LOAD_GLOBAL       'loaded_api'
182	CALL_FUNCTION_0   None

185	LOAD_GLOBAL       'has_binding'
188	LOAD_GLOBAL       'QT_API_PYQT'
191	CALL_FUNCTION_1   None

194	LOAD_GLOBAL       'has_binding'
197	LOAD_GLOBAL       'QT_API_PYSIDE'
200	CALL_FUNCTION_1   None

203	LOAD_FAST         'api_options'
206	BUILD_TUPLE_4     None
209	BINARY_MODULO     None
210	CALL_FUNCTION_1   None
213	RAISE_VARARGS_1   None
216_0	COME_FROM         '58'
216	LOAD_CONST        None
219	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 135_0