# Embedded file name: scripts/client/gui/Scaleform/framework/entities/abstract/ContextMenuManagerMeta.py
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class ContextMenuManagerMeta(BaseDAAPIComponent):

    def requestOptions(self, type, ctx):
        self._printOverrideError('requestOptions')

    def onOptionSelect(self, optionId):
        self._printOverrideError('onOptionSelect')

    def onHide(self):
        self._printOverrideError('onHide')

    def as_setOptionsS(self, data):
        """
        :param data: Represented by ContextMenuOptionsVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setOptions(data)

    def as_hideS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_hide()