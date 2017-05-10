# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/TextManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class TextManagerMeta(BaseDAAPIComponent):

    def getTextStyle(self, style):
        self._printOverrideError('getTextStyle')