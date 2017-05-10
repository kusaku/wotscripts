# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/CacheManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class CacheManagerMeta(BaseDAAPIComponent):

    def getSettings(self):
        self._printOverrideError('getSettings')