# Embedded file name: scripts/common/db/DBHUDHints.py
__author__ = 's_karchavets'
from DBHelpers import readValue
from debug_utils import LOG_ERROR, LOG_DEBUG

class _HudHint:
    pass


class HudHints:

    def __init__(self, data = None):
        self.__hints = dict()
        if data is not None:
            self.readData(data)
        return

    def readData(self, rootSection):
        for name, data in rootSection.items():
            hint = _HudHint()
            readValue(hint, data, 'id', '')
            if hint.id:
                readValue(hint, data, 'textID', '')
                readValue(hint, data, 'soundID', '')
                readValue(hint, data, 'mindist', 0)
                readValue(hint, data, 'maxdist', 0)
                readValue(hint, data, 'countForUse', -1)
                readValue(hint, data, 'altitude', 0.0)
                readValue(hint, data, 'priority', 0)
                readValue(hint, data, 'delayTime', 0.0)
                readValue(hint, data, 'timeForShow', 5.0)
                readValue(hint, data, 'enabled', True)
                readValue(hint, data, 'distStateFP', 0)
                readValue(hint, data, 'areaK', 1.0)
                readValue(hint, data, 'hitTime', 1.0)
                self.__hints[hint.id] = hint
                LOG_DEBUG('readData - added hint:', hint.id, hint.__dict__)
            else:
                LOG_ERROR('readData - hint without ID. Check it!')

    def getHint(self, id):
        return self.__hints.get(id, None)

    def getAllHints(self):
        return self.__hints