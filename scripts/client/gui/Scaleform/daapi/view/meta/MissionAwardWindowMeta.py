# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/MissionAwardWindowMeta.py
"""
This file was generated using the wgpygen.
Please, don't edit this file manually.
"""
from gui.Scaleform.daapi.view.lobby.award_window_base import AwardWindowBase

class MissionAwardWindowMeta(AwardWindowBase):

    def onCurrentQuestClick(self):
        self._printOverrideError('onCurrentQuestClick')

    def onNextQuestClick(self):
        self._printOverrideError('onNextQuestClick')

    def as_setDataS(self, data):
        """
        :param data: Represented by MissionAwardWindowVO (AS)
        """
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)