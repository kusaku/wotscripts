# Embedded file name: scripts/common/pydev/_pydev_bundle/_pydev_filesystem_encoding.py
import sys

def __getfilesystemencoding():
    """
    Note: there's a copy of this method in interpreterInfo.py
    """
    try:
        ret = sys.getfilesystemencoding()
        if not ret:
            raise RuntimeError('Unable to get encoding.')
        return ret
    except:
        try:
            from java.lang import System
            env = System.getProperty('os.name').lower()
            if env.find('win') != -1:
                return 'ISO-8859-1'
            return 'utf-8'
        except:
            pass

        if sys.platform == 'win32':
            return 'mbcs'
        return 'utf-8'


def getfilesystemencoding():
    try:
        ret = __getfilesystemencoding()
        if hasattr('', 'encode'):
            ''.encode(ret)
        if hasattr('', 'decode'):
            ''.decode(ret)
        return ret
    except:
        return 'utf-8'