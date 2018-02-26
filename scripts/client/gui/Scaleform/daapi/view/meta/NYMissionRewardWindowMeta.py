# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/NYMissionRewardWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class NYMissionRewardWindowMeta(AbstractWindowView):

    def onGetRewardClick(self, settings):
        self._printOverrideError('onGetRewardClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by NYMissionRewardWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)