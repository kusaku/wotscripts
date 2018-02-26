# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/AlertMessageBlockMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

class AlertMessageBlockMeta(BaseDAAPIComponent):

    def onButtonClick(self):
        self._printOverrideError('onButtonClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by AlertMessageBlockVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)