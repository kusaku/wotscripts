# Embedded file name: scripts/client/gui/Version.py
from Singleton import singleton
from debug_utils import LOG_INFO
import ResMgr
VERSION_FILE_PATH = 'build.xml'

@singleton

class Version(object):

    def __init__(self):
        self.__version = 'World of Warplanes unknown version'
        res = ResMgr.openSection(VERSION_FILE_PATH)
        if res:
            self.__version = res.readString('appname') + ' ' + res.readString('build', 'Unknown') + ' ' + res.readString('date', 'Unknown') + ' ' + res.readString('suffix', '')
            ResMgr.purge(VERSION_FILE_PATH, True)
        LOG_INFO('Version::Version()', self.__version)

    def getVersion(self):
        return self.__version