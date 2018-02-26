# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYLevelUpMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.View import View

class NYLevelUpMeta(View):

    def onClose(self):
        self._printOverrideError('onClose')

    def onOpenClick(self):
        self._printOverrideError('onOpenClick')

    def onAnimFinished(self, isBoxOpened):
        self._printOverrideError('onAnimFinished')

    def onPlaySound(self, soundType):
        self._printOverrideError('onPlaySound')

    def as_setDataS(self, data):
        """
        :param data: Represented by NYLevelUpDataVo (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)

    def as_boxOpenS(self, isApprove):
        if self._isDAAPIInited():
            return self.flashObject.as_boxOpen(isApprove)