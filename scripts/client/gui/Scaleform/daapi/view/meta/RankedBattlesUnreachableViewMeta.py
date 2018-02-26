# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RankedBattlesUnreachableViewMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.meta.WrapperViewMeta import WrapperViewMeta

class RankedBattlesUnreachableViewMeta(WrapperViewMeta):

    def onCloseBtnClick(self):
        self._printOverrideError('onCloseBtnClick')

    def onEscapePress(self):
        self._printOverrideError('onEscapePress')

    def as_setDataS(self, data):
        """
        :param data: Represented by RankedBattlesUnreachableViewVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)